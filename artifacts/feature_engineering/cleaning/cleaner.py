"""
Data Cleaning Module for Census Data Analysis
Provides intelligent handling of nulls, zeros, and missing values
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class SmartDataCleaner:
    """Intelligent handling of nulls and zeros in census data"""

    @staticmethod
    def handle_economic_zeros(df: pd.DataFrame, economic_cols: List[str],
                              strategy: str = 'filter') -> Tuple[pd.DataFrame, Dict]:
        """
        Handle zeros in economic variables intelligently

        Args:
            df: Input dataframe
            economic_cols: List of economic columns (income, rent, etc.)
            strategy: 'filter' (remove zeros), 'impute' (replace with median),
                     'flag' (keep but add flag column), 'keep' (do nothing)

        Returns:
            Tuple of (cleaned_df, metadata_dict)
        """
        df_clean = df.copy()
        created_features = []
        processed_cols = []

        for col in economic_cols:
            if col not in df_clean.columns:
                continue

            processed_cols.append(col)

            if strategy == 'filter':
                # Remove rows where economic value is zero (likely not applicable)
                df_clean = df_clean[df_clean[col] > 0]

            elif strategy == 'impute':
                # Replace zeros with median of non-zero values
                non_zero_median = df_clean[df_clean[col] > 0][col].median()
                df_clean.loc[df_clean[col] == 0, col] = non_zero_median

            elif strategy == 'flag':
                # Keep zeros but add a binary flag column
                # Handle NA values: treat NA as not zero (0), zero as 1, non-zero as 0
                flag_col = f'{col}_is_zero'
                df_clean[flag_col] = (df_clean[col] == 0).fillna(False).astype(int)
                created_features.append(flag_col)

            # 'keep' does nothing

        metadata = {
            'features': created_features,
            'transform': f'Flagged zeros in {len(processed_cols)} economic columns' if created_features else ''
        }
        return df_clean, metadata

    @staticmethod
    def distinguish_null_vs_zero(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """
        Create separate indicators for null vs zero values
        Useful for understanding missingness patterns
        """
        df_enhanced = df.copy()

        for col in cols:
            if col not in df_enhanced.columns:
                continue
            df_enhanced[f'{col}_is_null'] = df_enhanced[col].isna().astype(int)
            df_enhanced[f'{col}_is_zero'] = (df_enhanced[col] == 0).fillna(False).astype(int)

        return df_enhanced

    @staticmethod
    def impute_missing(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
        """
        Impute missing values intelligently

        Args:
            strategy: 'median', 'mean', 'mode', 'forward_fill', 'backward_fill'
        """
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_imputed = df.copy()
        numeric_cols = df_imputed.select_dtypes(include=[np.number]).columns

        # Exclude temporal, ID, and categorical-like columns from imputation
        exclude_patterns = ['Year', 'ID', 'SERIALNO', 'PUMA', 'State', 'Sex', 'Nativity']
        cols_to_impute = [col for col in numeric_cols
                         if not any(pattern in col for pattern in exclude_patterns)]

        logger.debug(f"Imputing {len(cols_to_impute)} columns, excluding "
                     f"{len(numeric_cols) - len(cols_to_impute)} temporal/ID columns")

        for col in cols_to_impute:
            if df_imputed[col].isna().sum() == 0:
                continue

            if strategy == 'median':
                fill_value = df_imputed[col].median()
                if pd.notna(fill_value):
                    df_imputed[col] = df_imputed[col].fillna(fill_value)
            elif strategy == 'mean':
                fill_value = df_imputed[col].mean()
                if pd.notna(fill_value):
                    df_imputed[col] = df_imputed[col].fillna(fill_value)
            elif strategy == 'mode':
                mode_vals = df_imputed[col].mode()
                if len(mode_vals) > 0:
                    df_imputed[col] = df_imputed[col].fillna(mode_vals[0])
            elif strategy == 'forward_fill':
                df_imputed[col] = df_imputed[col].ffill()
            elif strategy == 'backward_fill':
                df_imputed[col] = df_imputed[col].bfill()

        return df_imputed

    @staticmethod
    def impute_knn(df: pd.DataFrame, n_neighbors: int = 5,
                   cols: Optional[List[str]] = None) -> pd.DataFrame:
        """KNN-based imputation for missing values"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            logger.warning("KNN imputation: sklearn not available")
            return df

        try:
            from sklearn.impute import KNNImputer

            df_imputed = df.copy()
            numeric_cols = df_imputed.select_dtypes(include=[np.number]).columns.tolist()

            if cols:
                numeric_cols = [c for c in cols if c in numeric_cols]

            if not numeric_cols:
                return df_imputed

            imputer = KNNImputer(n_neighbors=n_neighbors)
            df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])

            logger.debug(f"KNN imputed {len(numeric_cols)} columns with k={n_neighbors}")
            return df_imputed
        except Exception as e:
            logger.warning(f"KNN imputation failed: {e}")
            return df

    @staticmethod
    def impute_iterative(df: pd.DataFrame, max_iter: int = 10,
                         cols: Optional[List[str]] = None) -> pd.DataFrame:
        """MICE-like iterative imputation for missing values"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            logger.warning("Iterative imputation: sklearn not available")
            return df

        try:
            from sklearn.experimental import enable_iterative_imputer
            from sklearn.impute import IterativeImputer

            df_imputed = df.copy()
            numeric_cols = df_imputed.select_dtypes(include=[np.number]).columns.tolist()

            if cols:
                numeric_cols = [c for c in cols if c in numeric_cols]

            if not numeric_cols:
                return df_imputed

            imputer = IterativeImputer(max_iter=max_iter, random_state=42)
            df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])

            logger.debug(f"Iteratively imputed {len(numeric_cols)} columns (max_iter={max_iter})")
            return df_imputed
        except Exception as e:
            logger.warning(f"Iterative imputation failed: {e}")
            return df

    @staticmethod
    def impute_by_group(df: pd.DataFrame, group_cols: List[str],
                        target_cols: List[str], strategy: str = 'median') -> pd.DataFrame:
        """Group-based imputation (e.g., by year, region)"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_imputed = df.copy()

        for col in target_cols:
            if col not in df_imputed.columns:
                continue

            valid_group_cols = [g for g in group_cols if g in df_imputed.columns]
            if not valid_group_cols:
                continue

            if strategy == 'median':
                fill_values = df_imputed.groupby(valid_group_cols)[col].transform('median')
            elif strategy == 'mean':
                fill_values = df_imputed.groupby(valid_group_cols)[col].transform('mean')
            else:
                continue

            df_imputed[col] = df_imputed[col].fillna(fill_values)

        logger.debug(f"Group-imputed {len(target_cols)} columns by {group_cols}")
        return df_imputed

    @staticmethod
    def detect_missingness_pattern(df: pd.DataFrame,
                                   cols: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze missingness patterns (MCAR/MAR/MNAR indicators)"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if cols:
            analysis_cols = [c for c in cols if c in df.columns]
        else:
            analysis_cols = df.columns.tolist()

        results = {
            'summary': {},
            'correlations': {},
            'patterns': []
        }

        # Missing counts per column
        for col in analysis_cols:
            missing_count = df[col].isna().sum()
            missing_pct = missing_count / len(df) * 100
            results['summary'][col] = {
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_pct)
            }

        # Check if missingness is correlated with other variables
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in analysis_cols:
            if col not in numeric_cols:
                continue

            missing_indicator = df[col].isna().astype(int)
            if missing_indicator.sum() < 10:
                continue

            correlations = {}
            for other_col in numeric_cols:
                if other_col == col:
                    continue
                try:
                    corr = df[other_col].corr(missing_indicator)
                    if abs(corr) > 0.1:
                        correlations[other_col] = float(corr)
                except Exception:
                    pass

            if correlations:
                results['correlations'][col] = correlations

        logger.debug(f"Analyzed missingness for {len(analysis_cols)} columns")
        return results

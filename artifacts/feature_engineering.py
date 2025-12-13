"""
Feature Engineering Module for Census Data Analysis
Provides feature creation, selection, transformation, and encoding capabilities
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings
warnings.filterwarnings('ignore')

# Import zero exclusion function from processing
from processing import should_exclude_zeros

try:
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
    from sklearn.feature_selection import SelectKBest, f_regression, f_classif, mutual_info_regression, mutual_info_classif
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. Feature engineering will be limited.")


# ============================================================================
# NULL AND ZERO HANDLING
# ============================================================================

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


# ============================================================================
# FEATURE CREATION
# ============================================================================

class FeatureCreator:
    """Create new features from existing census data"""
    
    @staticmethod
    def create_ratio_features(df: pd.DataFrame, numerators: List[str],
                             denominators: List[str]) -> pd.DataFrame:
        """Create ratio features from pairs of columns"""
        df_enhanced = df.copy()
        
        for num in numerators:
            for denom in denominators:
                if num in df_enhanced.columns and denom in df_enhanced.columns:
                    # Avoid division by zero
                    mask = df_enhanced[denom] != 0
                    feature_name = f'{num}_to_{denom}_ratio'
                    df_enhanced[feature_name] = np.nan
                    df_enhanced.loc[mask, feature_name] = (
                        df_enhanced.loc[mask, num] / df_enhanced.loc[mask, denom]
                    )
                    
        return df_enhanced
    
    @staticmethod
    def create_income_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create income-related derived features.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        # Income per hour worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Hours_Worked_Per_Week' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Hour'] = np.nan
            # Assuming 52 weeks per year
            df_enhanced.loc[mask, 'Income_Per_Hour'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] /
                (df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * 52)
            )
            created.append('Income_Per_Hour')

        # Income per week worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Weeks_Worked_Past_Year'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Week_Worked'] = np.nan
            df_enhanced.loc[mask, 'Income_Per_Week_Worked'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] /
                df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
            created.append('Income_Per_Week_Worked')

        # Total annual hours worked
        if 'Hours_Worked_Per_Week' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Weeks_Worked_Past_Year'] > 0)
            df_enhanced['Total_Annual_Hours'] = np.nan
            df_enhanced.loc[mask, 'Total_Annual_Hours'] = (
                df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
            created.append('Total_Annual_Hours')

        metadata = {
            'features': created,
            'transform': 'Income ratios derived from work metrics' if created else ''
        }
        return df_enhanced, metadata
    
    @staticmethod
    def create_housing_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create housing-related derived features.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        # Rent to property value ratio
        if 'Gross_Rent' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Annual_Rent_to_Value_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Annual_Rent_to_Value_Ratio'] = (
                (df_enhanced.loc[mask, 'Gross_Rent'] * 12) /
                df_enhanced.loc[mask, 'Property_Value']
            )
            created.append('Annual_Rent_to_Value_Ratio')

        # Total monthly housing cost
        cost_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly']
        available_cost_cols = [col for col in cost_cols if col in df_enhanced.columns]
        if available_cost_cols:
            df_enhanced['Total_Monthly_Utility_Cost'] = df_enhanced[available_cost_cols].sum(axis=1)
            created.append('Total_Monthly_Utility_Cost')

        # Property tax as percentage of value
        if 'Property_Taxes_Yearly' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Property_Tax_Rate'] = np.nan
            df_enhanced.loc[mask, 'Property_Tax_Rate'] = (
                df_enhanced.loc[mask, 'Property_Taxes_Yearly'] /
                df_enhanced.loc[mask, 'Property_Value'] * 100
            )
            created.append('Property_Tax_Rate')

        metadata = {
            'features': created,
            'transform': 'Housing cost ratios calculated' if created else ''
        }
        return df_enhanced, metadata
    
    @staticmethod
    def create_age_groups(df: pd.DataFrame, age_col: str = 'Age') -> Tuple[pd.DataFrame, Dict]:
        """Create age group categories.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        if age_col not in df_enhanced.columns:
            return df_enhanced, {'features': [], 'transform': ''}

        # Filter out NA values before pd.cut to avoid "boolean value of NA is ambiguous" error
        valid_age_mask = df_enhanced[age_col].notna()

        bins = [0, 18, 25, 35, 45, 55, 65, 100]
        labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']

        # Initialize Age_Group column with NaN
        df_enhanced['Age_Group'] = pd.NA

        # Apply pd.cut only to valid (non-NA) age values
        if valid_age_mask.any():
            df_enhanced.loc[valid_age_mask, 'Age_Group'] = pd.cut(
                df_enhanced.loc[valid_age_mask, age_col],
                bins=bins,
                labels=labels,
                right=False
            )
            created.append('Age_Group')

        metadata = {
            'features': created,
            'transform': 'Age binned into demographic groups' if created else ''
        }
        return df_enhanced, metadata
    
    @staticmethod
    def create_temporal_features(df: pd.DataFrame, year_col: str = 'Census_Year') -> Tuple[pd.DataFrame, Dict]:
        """Create temporal features from year.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        if year_col not in df_enhanced.columns:
            return df_enhanced, {'features': [], 'transform': ''}

        # Years since earliest year in dataset
        min_year = df_enhanced[year_col].min()
        df_enhanced['Years_Since_Start'] = df_enhanced[year_col] - min_year
        created.append('Years_Since_Start')

        # Decade
        df_enhanced['Decade'] = (df_enhanced[year_col] // 10) * 10
        created.append('Decade')

        metadata = {
            'features': created,
            'transform': 'Temporal features extracted from year' if created else ''
        }
        return df_enhanced, metadata
    
    @staticmethod
    def create_interaction_features(df: pd.DataFrame, 
                                   col_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create interaction features (products) between column pairs"""
        df_enhanced = df.copy()
        
        for col1, col2 in col_pairs:
            if col1 in df_enhanced.columns and col2 in df_enhanced.columns:
                feature_name = f'{col1}_x_{col2}'
                df_enhanced[feature_name] = df_enhanced[col1] * df_enhanced[col2]
        
        return df_enhanced
    
    @staticmethod
    def create_polynomial_features(df: pd.DataFrame, cols: List[str],
                                  degree: int = 2) -> pd.DataFrame:
        """Create polynomial features (squared, cubed, etc.)"""
        df_enhanced = df.copy()
        
        for col in cols:
            if col not in df_enhanced.columns:
                continue
            for d in range(2, degree + 1):
                df_enhanced[f'{col}_power_{d}'] = df_enhanced[col] ** d
        
        return df_enhanced


# ============================================================================
# FEATURE SELECTION
# ============================================================================

class FeatureSelector:
    """Select most important features for modeling"""
    
    @staticmethod
    def select_by_correlation(df: pd.DataFrame, target_col: str,
                            threshold: float = 0.1, top_k: Optional[int] = None) -> List[str]:
        """Select features based on correlation with target"""
        numeric_df = df.select_dtypes(include=[np.number])

        if target_col not in numeric_df.columns:
            return []

        # Filter zeros for each column before correlation
        df_filtered = numeric_df.copy()
        for col in numeric_df.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan

        # Calculate correlations
        correlations = df_filtered.corr()[target_col].abs().sort_values(ascending=False)
        
        # Remove target itself
        correlations = correlations.drop(target_col, errors='ignore')
        
        # Filter by threshold
        selected = correlations[correlations >= threshold].index.tolist()
        
        # Limit to top k if specified
        if top_k is not None:
            selected = selected[:top_k]
        
        return selected
    
    @staticmethod
    def select_by_variance(df: pd.DataFrame, threshold: float = 0.01) -> List[str]:
        """Remove low-variance features"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate variance
        variances = numeric_df.var()
        
        # Select features above threshold
        selected = variances[variances > threshold].index.tolist()
        
        return selected
    
    @staticmethod
    def select_by_mutual_information(df: pd.DataFrame, target_col: str,
                                    task: str = 'regression', top_k: int = 10) -> List[str]:
        """Select features using mutual information"""
        if not SKLEARN_AVAILABLE:
            return []
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if target_col not in numeric_df.columns:
            return []
        
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Calculate mutual information
        if task == 'regression':
            mi_scores = mutual_info_regression(X, y, random_state=42)
        else:
            mi_scores = mutual_info_classif(X, y, random_state=42)
        
        # Create feature importance dataframe
        mi_df = pd.DataFrame({'feature': X.columns, 'mi_score': mi_scores})
        mi_df = mi_df.sort_values('mi_score', ascending=False)
        
        return mi_df.head(top_k)['feature'].tolist()
    
    @staticmethod
    def select_by_sklearn(df: pd.DataFrame, target_col: str,
                         task: str = 'regression', k: int = 10) -> List[str]:
        """Select top k features using sklearn's SelectKBest"""
        if not SKLEARN_AVAILABLE:
            return []
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if target_col not in numeric_df.columns:
            return []
        
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Select score function
        score_func = f_regression if task == 'regression' else f_classif
        
        # Fit selector
        selector = SelectKBest(score_func=score_func, k=min(k, X.shape[1]))
        selector.fit(X, y)
        
        # Get selected features
        selected_mask = selector.get_support()
        selected_features = X.columns[selected_mask].tolist()
        
        return selected_features


# ============================================================================
# ECONOMIC FEATURE CREATOR
# ============================================================================

class EconomicFeatureCreator:
    """Domain-specific economic and housing features for census analysis"""

    @staticmethod
    def _validate_columns(df: pd.DataFrame, required: List[str],
                          operation: str) -> List[str]:
        """Return list of available columns from required list."""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")
        available = [c for c in required if c in df.columns]
        missing = set(required) - set(available)
        if missing:
            logger.warning(f"{operation}: Missing columns {missing}")
        return available

    @staticmethod
    def create_gini_coefficient(df: pd.DataFrame,
                                income_col: str = 'Total_Person_Income',
                                group_by: Optional[str] = 'Census_Year') -> pd.DataFrame:
        """Calculate Gini coefficient for income inequality"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        def gini(values):
            """Calculate Gini coefficient using Lorenz curve"""
            values = np.array(values)
            values = values[~np.isnan(values)]
            values = values[values > 0]
            if len(values) < 2:
                return np.nan
            values = np.sort(values)
            n = len(values)
            cumulative = np.cumsum(values)
            return (2 * np.sum((np.arange(1, n + 1) * values)) / (n * cumulative[-1])) - (n + 1) / n

        if income_col not in df.columns:
            logger.warning(f"Gini coefficient: {income_col} not found")
            return df_enhanced

        if group_by and group_by in df.columns:
            gini_by_group = df.groupby(group_by)[income_col].apply(gini)
            gini_map = gini_by_group.to_dict()
            df_enhanced[f'{income_col}_gini'] = df_enhanced[group_by].map(gini_map)
            logger.debug(f"Created Gini coefficient by {group_by}")
        else:
            overall_gini = gini(df[income_col].dropna().values)
            df_enhanced[f'{income_col}_gini'] = overall_gini
            logger.debug(f"Created overall Gini coefficient: {overall_gini:.4f}")

        return df_enhanced

    @staticmethod
    def create_affordability_indices(df: pd.DataFrame) -> pd.DataFrame:
        """Create comprehensive housing affordability indices"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        # Rent-to-Income Ratio (monthly rent / monthly income)
        if 'Gross_Rent' in df.columns and 'Total_Person_Income' in df.columns:
            monthly_income = df['Total_Person_Income'] / 12
            mask = (monthly_income > 0) & (df['Gross_Rent'] > 0)
            df_enhanced['Rent_to_Income_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Rent_to_Income_Ratio'] = df.loc[mask, 'Gross_Rent'] / monthly_income[mask]
            created.append('Rent_to_Income_Ratio')

            # Housing Cost Burden (30% threshold)
            df_enhanced['Housing_Cost_Burden'] = (df_enhanced['Rent_to_Income_Ratio'] > 0.30).astype(int)
            created.append('Housing_Cost_Burden')

            # Severe Cost Burden (50% threshold)
            df_enhanced['Severe_Cost_Burden'] = (df_enhanced['Rent_to_Income_Ratio'] > 0.50).astype(int)
            created.append('Severe_Cost_Burden')

        # Price-to-Income Ratio (property value / annual income)
        if 'Property_Value' in df.columns and 'Total_Person_Income' in df.columns:
            mask = (df['Total_Person_Income'] > 0) & (df['Property_Value'] > 0)
            df_enhanced['Price_to_Income_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Price_to_Income_Ratio'] = (
                df.loc[mask, 'Property_Value'] / df.loc[mask, 'Total_Person_Income']
            )
            created.append('Price_to_Income_Ratio')

        # Housing Affordability Index (HAI)
        # HAI = (Median Income / Qualifying Income) * 100
        # Qualifying Income = (Mortgage Payment * 12) / 0.25
        if 'Property_Value' in df.columns and 'Total_Person_Income' in df.columns:
            # Estimate monthly mortgage (assume 30yr @ 7% rate, 20% down)
            principal = df['Property_Value'] * 0.80
            monthly_rate = 0.07 / 12
            n_payments = 360
            mortgage_payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)

            qualifying_income = (mortgage_payment * 12) / 0.25
            mask = qualifying_income > 0
            df_enhanced['Housing_Affordability_Index'] = np.nan
            df_enhanced.loc[mask, 'Housing_Affordability_Index'] = (
                df.loc[mask, 'Total_Person_Income'] / qualifying_income[mask]
            ) * 100
            created.append('Housing_Affordability_Index')

        logger.debug(f"Created affordability indices: {created}")
        return df_enhanced

    @staticmethod
    def create_poverty_intensity(df: pd.DataFrame,
                                 poverty_line: float = 15000,
                                 survey_type: str = 'population') -> pd.DataFrame:
        """
        Create poverty gap and severity indices.

        Note: Only applicable to population surveys (uses Total_Person_Income).
        """
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        # Skip for housing surveys - poverty metrics require person-level income
        if survey_type != 'population':
            logger.debug("Poverty intensity: Skipped for non-population survey")
            return df_enhanced

        if 'Total_Person_Income' not in df.columns:
            logger.warning("Poverty intensity: Total_Person_Income not found")
            return df_enhanced

        income = df['Total_Person_Income']

        # Poverty status (binary)
        df_enhanced['In_Poverty'] = (income < poverty_line).astype(int)

        # Poverty Gap (distance from poverty line, normalized)
        df_enhanced['Poverty_Gap'] = np.maximum(0, (poverty_line - income) / poverty_line)

        # Poverty Severity (squared poverty gap)
        df_enhanced['Poverty_Severity'] = df_enhanced['Poverty_Gap'] ** 2

        logger.debug(f"Created poverty indices with poverty line ${poverty_line:,}")
        return df_enhanced

    @staticmethod
    def create_housing_quality_index(df: pd.DataFrame,
                                     survey_type: str = 'housing') -> pd.DataFrame:
        """
        Create composite housing quality index.

        Note: Only applicable to housing surveys (uses housing-specific columns).
        """
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        # Skip for population surveys - quality index requires housing-specific columns
        if survey_type != 'housing':
            logger.debug("Housing quality index: Skipped for non-housing survey")
            return df_enhanced

        quality_cols = []

        # Age of structure (newer = higher quality)
        if 'Year_Structure_Built' in df.columns:
            current_year = 2024
            df_enhanced['Structure_Age'] = current_year - df['Year_Structure_Built']
            df_enhanced['Structure_Age_Score'] = 1 - (df_enhanced['Structure_Age'] / 100).clip(0, 1)
            quality_cols.append('Structure_Age_Score')

        # Rooms and bedrooms (more = higher quality)
        if 'Number_of_Rooms' in df.columns:
            df_enhanced['Rooms_Score'] = (df['Number_of_Rooms'] / 10).clip(0, 1)
            quality_cols.append('Rooms_Score')

        if 'Number_of_Bedrooms' in df.columns:
            df_enhanced['Bedrooms_Score'] = (df['Number_of_Bedrooms'] / 5).clip(0, 1)
            quality_cols.append('Bedrooms_Score')

        # Create composite index
        if quality_cols:
            df_enhanced['Housing_Quality_Index'] = df_enhanced[quality_cols].mean(axis=1)
            logger.debug(f"Created housing quality index from {len(quality_cols)} components")

        return df_enhanced


# ============================================================================
# ADVANCED FEATURE SELECTOR
# ============================================================================

class AdvancedFeatureSelector:
    """Advanced feature selection with stability and importance methods"""

    @staticmethod
    def select_by_rfe(df: pd.DataFrame, target_col: str,
                      n_features: int = 10,
                      estimator: str = 'random_forest') -> List[str]:
        """Recursive Feature Elimination"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            logger.warning("RFE: sklearn not available")
            return []

        try:
            from sklearn.feature_selection import RFE
            from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 50 or X.shape[1] < n_features:
                return X.columns.tolist()[:n_features]

            # Select estimator
            if estimator == 'random_forest':
                est = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            else:
                est = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)

            rfe = RFE(estimator=est, n_features_to_select=min(n_features, X.shape[1]))
            rfe.fit(X, y)

            selected = X.columns[rfe.support_].tolist()
            logger.debug(f"RFE selected {len(selected)} features")
            return selected
        except Exception as e:
            logger.warning(f"RFE failed: {e}")
            return []

    @staticmethod
    def select_by_permutation_importance(df: pd.DataFrame, target_col: str,
                                         n_features: int = 10,
                                         n_repeats: int = 10) -> List[str]:
        """Permutation-based feature importance"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            return []

        try:
            from sklearn.inspection import permutation_importance
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split

            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 100:
                return X.columns.tolist()[:n_features]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)

            perm_importance = permutation_importance(
                model, X_test, y_test, n_repeats=n_repeats, random_state=42, n_jobs=-1
            )

            importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': perm_importance.importances_mean
            }).sort_values('importance', ascending=False)

            selected = importance_df.head(n_features)['feature'].tolist()
            logger.debug(f"Permutation importance selected {len(selected)} features")
            return selected
        except Exception as e:
            logger.warning(f"Permutation importance failed: {e}")
            return []

    @staticmethod
    def select_by_stability(df: pd.DataFrame, target_col: str,
                           n_bootstrap: int = 50,
                           threshold: float = 0.6) -> List[str]:
        """Stability selection - robust feature selection across bootstrap samples"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            return []

        try:
            from sklearn.linear_model import Lasso
            from sklearn.preprocessing import StandardScaler

            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 100:
                return X.columns.tolist()

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            selection_counts = {col: 0 for col in X.columns}
            n_samples = len(X)

            for i in range(n_bootstrap):
                # Bootstrap sample
                indices = np.random.choice(n_samples, size=n_samples, replace=True)
                X_boot = X_scaled[indices]
                y_boot = y.iloc[indices].values

                # Fit Lasso
                lasso = Lasso(alpha=0.01, max_iter=1000, random_state=i)
                lasso.fit(X_boot, y_boot)

                # Count non-zero coefficients
                for j, coef in enumerate(lasso.coef_):
                    if abs(coef) > 1e-5:
                        selection_counts[X.columns[j]] += 1

            # Select features appearing in > threshold of bootstrap samples
            selected = [col for col, count in selection_counts.items()
                       if count / n_bootstrap > threshold]

            logger.debug(f"Stability selection: {len(selected)} features (threshold={threshold})")
            return selected
        except Exception as e:
            logger.warning(f"Stability selection failed: {e}")
            return []

    @staticmethod
    def get_shap_importance(df: pd.DataFrame, target_col: str,
                           n_features: int = 10,
                           sample_size: int = 1000) -> Dict[str, float]:
        """SHAP-based feature importance (optional - requires shap package)"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        try:
            import shap
            from sklearn.ensemble import RandomForestRegressor

            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return {}

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            # Sample if needed
            if len(X) > sample_size:
                sample_idx = np.random.choice(len(X), sample_size, replace=False)
                X_sample = X.iloc[sample_idx]
                y_sample = y.iloc[sample_idx]
            else:
                X_sample, y_sample = X, y

            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_sample, y_sample)

            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_sample)

            importance = np.abs(shap_values).mean(axis=0)
            importance_dict = dict(zip(X.columns, importance))
            sorted_importance = dict(sorted(importance_dict.items(),
                                           key=lambda x: x[1], reverse=True)[:n_features])

            logger.debug(f"SHAP importance calculated for {len(sorted_importance)} features")
            return sorted_importance
        except ImportError:
            logger.warning("SHAP package not available")
            return {}
        except Exception as e:
            logger.warning(f"SHAP importance failed: {e}")
            return {}


# ============================================================================
# FEATURE TRANSFORMATION
# ============================================================================

class FeatureTransformer:
    """Transform features for better model performance"""
    
    @staticmethod
    def log_transform(df: pd.DataFrame, cols: List[str],
                     add_constant: float = 1.0) -> pd.DataFrame:
        """Apply log transformation to skewed features"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Add constant to handle zeros, then log transform
            df_transformed[f'{col}_log'] = np.log(df_transformed[col] + add_constant)
        
        return df_transformed
    
    @staticmethod
    def sqrt_transform(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Apply square root transformation"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Only transform non-negative values
            mask = df_transformed[col] >= 0
            df_transformed[f'{col}_sqrt'] = np.nan
            df_transformed.loc[mask, f'{col}_sqrt'] = np.sqrt(df_transformed.loc[mask, col])
        
        return df_transformed
    
    @staticmethod
    def box_cox_transform(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Apply Box-Cox transformation for normalization"""
        try:
            from scipy.stats import boxcox
        except ImportError:
            print("[WARNING] scipy not available for Box-Cox transformation")
            return df
        
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Box-Cox requires positive values
            if (df_transformed[col] > 0).all():
                try:
                    df_transformed[f'{col}_boxcox'], _ = boxcox(df_transformed[col])
                except:
                    pass
        
        return df_transformed
    
    @staticmethod
    def standardize(df: pd.DataFrame, cols: List[str],
                   method: str = 'robust') -> pd.DataFrame:
        """Standardize features using different methods"""
        if not SKLEARN_AVAILABLE:
            return df
        
        df_transformed = df.copy()
        
        # Select scaler
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            return df_transformed
        
        # Transform specified columns
        available_cols = [c for c in cols if c in df_transformed.columns]
        if available_cols:
            df_transformed[available_cols] = scaler.fit_transform(df_transformed[available_cols])
        
        return df_transformed
    
    @staticmethod
    def bin_numeric_features(df: pd.DataFrame, cols: List[str],
                            n_bins: int = 5, strategy: str = 'quantile') -> pd.DataFrame:
        """Bin continuous features into categories"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            
            if strategy == 'quantile':
                df_transformed[f'{col}_binned'] = pd.qcut(
                    df_transformed[col], q=n_bins, labels=False, duplicates='drop'
                )
            else:  # uniform
                df_transformed[f'{col}_binned'] = pd.cut(
                    df_transformed[col], bins=n_bins, labels=False
                )
        
        return df_transformed


# ============================================================================
# ENCODING
# ============================================================================

class CategoricalEncoder:
    """Encode categorical variables for modeling"""
    
    @staticmethod
    def one_hot_encode(df: pd.DataFrame, cols: List[str],
                      drop_first: bool = True) -> pd.DataFrame:
        """One-hot encode categorical variables"""
        df_encoded = df.copy()
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            # Create dummies
            dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=drop_first)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            df_encoded = df_encoded.drop(columns=[col])
        
        return df_encoded
    
    @staticmethod
    def label_encode(df: pd.DataFrame, cols: List[str]) -> Tuple[pd.DataFrame, Dict]:
        """Label encode categorical variables"""
        if not SKLEARN_AVAILABLE:
            return df, {}
        
        df_encoded = df.copy()
        encoders = {}
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            encoder = LabelEncoder()
            df_encoded[col] = encoder.fit_transform(df_encoded[col].astype(str))
            encoders[col] = encoder
        
        return df_encoded, encoders
    
    @staticmethod
    def frequency_encode(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Encode categories by their frequency"""
        df_encoded = df.copy()
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            freq_map = df_encoded[col].value_counts(normalize=True).to_dict()
            df_encoded[f'{col}_freq'] = df_encoded[col].map(freq_map)
        
        return df_encoded


# ============================================================================
# DIMENSIONALITY REDUCTION
# ============================================================================

class DimensionalityReducer:
    """Reduce feature dimensionality"""
    
    @staticmethod
    def pca_transform(df: pd.DataFrame, n_components: int = 10) -> Tuple[pd.DataFrame, Any]:
        """Apply PCA for dimensionality reduction"""
        if not SKLEARN_AVAILABLE:
            return df, None
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        # Standardize before PCA
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)
        
        # Apply PCA
        pca = PCA(n_components=min(n_components, scaled_data.shape[1]))
        pca_data = pca.fit_transform(scaled_data)
        
        # Create dataframe with PCA components
        pca_cols = [f'PC{i+1}' for i in range(pca_data.shape[1])]
        pca_df = pd.DataFrame(pca_data, columns=pca_cols, index=numeric_df.index)
        
        return pca_df, pca
    
    @staticmethod
    def get_pca_explained_variance(pca: Any) -> Dict[str, float]:
        """Get explained variance from fitted PCA"""
        if pca is None:
            return {}
        
        return {
            'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist()
        }

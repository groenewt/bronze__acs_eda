"""
Feature Transformation Module
Provides transformation capabilities for features to improve model performance
"""
import pandas as pd
import numpy as np
from typing import List

try:
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. Standardization will be limited.")


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

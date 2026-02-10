"""
Basic Feature Selection Module for Census Data Analysis
Provides fundamental feature selection methods
"""
import pandas as pd
import numpy as np
from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')

# Import zero exclusion function from processing
from processing import should_exclude_zeros

try:
    from sklearn.feature_selection import SelectKBest, f_regression, f_classif, mutual_info_regression, mutual_info_classif
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


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

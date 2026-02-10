"""
Dimensionality Reduction Module
Provides dimensionality reduction capabilities for feature sets
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. PCA will be limited.")


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

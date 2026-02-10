# Suppress sklearn warnings in child processes BEFORE any imports
import os
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'

"""
Base classes and data structures for ML models
Provides common functionality and result containers
"""
import warnings
# Comprehensive sklearn warning suppression
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

try:
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
    from sklearn.ensemble import (RandomForestRegressor, RandomForestClassifier,
                                  GradientBoostingRegressor, GradientBoostingClassifier,
                                  AdaBoostRegressor, AdaBoostClassifier,
                                  ExtraTreesRegressor, ExtraTreesClassifier,
                                  BaggingClassifier, VotingClassifier, StackingClassifier)
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
    from sklearn.svm import SVR, SVC
    from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
    from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                                 accuracy_score, precision_score, recall_score, f1_score,
                                 confusion_matrix, classification_report, silhouette_score)
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. ML models will be disabled.")

# SHAP for model explainability
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("[WARNING] SHAP not available. Model explainability will be disabled.")


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ModelResults:
    """Container for model results"""
    model_type: str
    model_name: str
    train_score: float
    test_score: Optional[float]
    cv_scores: Optional[List[float]]
    predictions: Optional[np.ndarray]
    feature_importance: Optional[Dict[str, float]]
    metadata: Dict[str, Any]


@dataclass
class ClusterResults:
    """Container for clustering results"""
    method: str
    n_clusters: int
    labels: np.ndarray
    silhouette_score: float
    cluster_sizes: Dict[int, int]
    cluster_centers: Optional[np.ndarray]
    metadata: Dict[str, Any]


# ============================================================================
# BASE MODEL CLASS
# ============================================================================

class BaseMLModel:
    """Base class for ML models with common functionality"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.is_fitted = False

    def _prepare_data(self, X: pd.DataFrame, y: pd.Series = None,
                     scale: bool = True) -> Tuple:
        """Prepare data for modeling with proper handling of nulls/zeros"""
        # Remove rows with any nulls in features
        if y is not None:
            mask = ~(X.isna().any(axis=1) | y.isna())
            X_clean = X[mask].copy()
            y_clean = y[mask].copy()
        else:
            mask = ~X.isna().any(axis=1)
            X_clean = X[mask].copy()
            y_clean = None

        # Scale if requested
        if scale and self.scaler is None:
            self.scaler = RobustScaler()  # Better for data with outliers
            X_scaled = self.scaler.fit_transform(X_clean)
            X_clean = pd.DataFrame(X_scaled, columns=X_clean.columns, index=X_clean.index)
        elif scale and self.scaler is not None:
            X_scaled = self.scaler.transform(X_clean)
            X_clean = pd.DataFrame(X_scaled, columns=X_clean.columns, index=X_clean.index)

        return X_clean, y_clean

    def _get_feature_importance(self, feature_names: List[str]) -> Dict[str, float]:
        """Extract feature importance if available"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            return dict(zip(feature_names, importances))
        elif hasattr(self.model, 'coef_'):
            coefs = np.abs(self.model.coef_).flatten()
            return dict(zip(feature_names, coefs))
        return {}

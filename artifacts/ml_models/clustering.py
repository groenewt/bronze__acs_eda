"""
Clustering Models Module
Provides clustering analysis with multiple algorithms
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
import numpy as np
from .base import BaseMLModel, ClusterResults, SKLEARN_AVAILABLE

try:
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.metrics import silhouette_score
except ImportError:
    pass  # SKLEARN_AVAILABLE flag from base handles this

from exceptions import (ModelTrainingError, InsufficientDataError)


class ClusteringModeler(BaseMLModel):
    """Handles clustering analysis"""

    def __init__(self, random_state: int = 42):
        super().__init__(random_state)

    def kmeans_clustering(self, X: pd.DataFrame, n_clusters: int = 3,
                         scale: bool = True) -> ClusterResults:
        """Perform K-Means clustering"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('kmeans', "scikit-learn not available")

            if len(X) < n_clusters:
                raise InsufficientDataError('kmeans_clustering', n_clusters, len(X))

            X_clean, _ = self._prepare_data(X, scale=scale)

            # Fit K-Means
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X_clean)

            # Calculate silhouette score
            silhouette = silhouette_score(X_clean, labels)

            # Cluster sizes
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))

            return ClusterResults(
                method='kmeans',
                n_clusters=n_clusters,
                labels=labels,
                silhouette_score=silhouette,
                cluster_sizes=cluster_sizes,
                cluster_centers=kmeans.cluster_centers_,
                metadata={
                    'inertia': kmeans.inertia_,
                    'n_features': X_clean.shape[1],
                    'n_samples': len(X_clean)
                }
            )
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('kmeans', str(e))

    def hierarchical_clustering(self, X: pd.DataFrame, n_clusters: int = 3,
                               linkage: str = 'ward', scale: bool = True) -> ClusterResults:
        """Perform hierarchical clustering with smart sampling for large datasets.

        Uses O(n²) memory for distance matrix, so samples large datasets to prevent
        segfaults. Following pattern from processing/analyzers/multivariate.py:311.
        """
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('hierarchical', "scikit-learn not available")

            if len(X) < n_clusters:
                raise InsufficientDataError('hierarchical_clustering', n_clusters, len(X))

            # Smart sampling for O(n²) distance matrix to prevent segfault
            from memory_utils import get_safe_sample_size_quadratic
            from logging_config import get_logger
            logger = get_logger("ml.clustering")

            safe_n = get_safe_sample_size_quadratic(len(X), X.shape[1])
            if safe_n < len(X):
                X_sampled = X.sample(n=safe_n, random_state=self.random_state)
                logger.info(f"[HIERARCHICAL] Sampled {len(X):,} -> {safe_n:,} for O(n²) distance matrix")
            else:
                X_sampled = X

            X_clean, _ = self._prepare_data(X_sampled, scale=scale)

            # Fit hierarchical clustering
            hc = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
            labels = hc.fit_predict(X_clean)

            # Calculate silhouette score
            silhouette = silhouette_score(X_clean, labels)

            # Cluster sizes
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))

            return ClusterResults(
                method='hierarchical',
                n_clusters=n_clusters,
                labels=labels,
                silhouette_score=silhouette,
                cluster_sizes=cluster_sizes,
                cluster_centers=None,
                metadata={
                    'linkage': linkage,
                    'n_features': X_clean.shape[1],
                    'n_samples': len(X_clean)
                }
            )
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('hierarchical', str(e))

    def find_optimal_clusters(self, X: pd.DataFrame, max_clusters: int = 10) -> dict:
        """Find optimal number of clusters using silhouette method"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('find_optimal_clusters', "scikit-learn not available")

            if len(X) < 2:
                raise InsufficientDataError('find_optimal_clusters', 2, len(X))

            X_clean, _ = self._prepare_data(X, scale=True)

            silhouette_scores = {}
            for k in range(2, min(max_clusters + 1, len(X_clean))):
                kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                labels = kmeans.fit_predict(X_clean)
                score = silhouette_score(X_clean, labels)
                silhouette_scores[k] = score

            return silhouette_scores
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('find_optimal_clusters', str(e))

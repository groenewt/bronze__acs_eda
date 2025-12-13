"""Clustering Visualizations"""
import numpy as np
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer


class ClusteringVisualizer(BaseMLVisualizer):
    """Visualizes clustering model results"""

    def viz_clustering(self, result, X):
        self.cluster_method = getattr(result, 'method', 'kmeans')
        self._sizes(result)
        self._scatter(result, X)
        self._silhouette(result)
        self._cluster_distributions(result, X)
        self._cluster_variance(result, X)

    def _sizes(self, r):
        plt.figure(figsize=(10, 6))
        sizes = [r.cluster_sizes.get(i, 0) for i in range(r.n_clusters)]
        plt.bar(range(r.n_clusters), sizes, color='steelblue')
        plt.xlabel('Cluster')
        plt.ylabel('Size')
        plt.title(f'Cluster Sizes (Silhouette={r.silhouette_score:.3f})', fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('sizes.png', 'clustering', self.cluster_method)

    def _scatter(self, r, X):
        if X.shape[1] < 2:
            return
        plt.figure(figsize=(10, 8))
        cols = X.columns[:2]
        plt.scatter(X[cols[0]], X[cols[1]], c=r.labels, cmap='viridis', alpha=0.6, s=30)
        plt.xlabel(cols[0])
        plt.ylabel(cols[1])
        plt.title('Clusters (2D) - Original Scale\n(Clusters computed on standardized data)', fontweight='bold')
        plt.colorbar(label='Cluster')
        self._save('scatter.png', 'clustering', self.cluster_method)

    def _silhouette(self, r):
        plt.figure(figsize=(10, 6))
        plt.bar([0], [r.silhouette_score], color='teal', width=0.5)
        plt.ylim(0, 1)
        plt.ylabel('Score')
        plt.title(f'Silhouette: {r.silhouette_score:.3f}', fontweight='bold')
        plt.xticks([])
        plt.grid(alpha=0.3)
        self._save('silhouette.png', 'clustering', self.cluster_method)

    def _cluster_distributions(self, r, X):
        """Visualize feature distributions across clusters"""
        if X.shape[1] == 0:
            return

        # Select up to 4 features for visualization
        n_features = min(4, X.shape[1])
        features = X.columns[:n_features]

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for idx, feature in enumerate(features):
            if idx >= 4:
                break
            ax = axes[idx]
            for cluster_id in range(r.n_clusters):
                cluster_data = X[r.labels == cluster_id][feature]
                ax.hist(cluster_data, alpha=0.5, label=f'Cluster {cluster_id}', bins=20)
            ax.set_xlabel(feature)
            ax.set_ylabel('Frequency')
            ax.set_title(f'{feature} Distribution by Cluster', fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)

        plt.tight_layout()
        self._save('feature_distributions.png', 'clustering', self.cluster_method)

    def _cluster_variance(self, r, X):
        """Visualize variance of features across clusters"""
        if X.shape[1] == 0:
            return

        # Calculate variance for each feature in each cluster
        variances = []
        for cluster_id in range(r.n_clusters):
            cluster_data = X[r.labels == cluster_id]
            cluster_var = cluster_data.var().values
            variances.append(cluster_var)

        # Plot variance comparison
        features = X.columns[:min(6, X.shape[1])]  # Limit to 6 features for readability
        x = np.arange(len(features))
        width = 0.15

        fig, ax = plt.subplots(figsize=(12, 6))
        for cluster_id in range(r.n_clusters):
            offset = width * (cluster_id - r.n_clusters / 2)
            cluster_vars = [variances[cluster_id][i] for i in range(len(features))]
            ax.bar(x + offset, cluster_vars, width, label=f'Cluster {cluster_id}', alpha=0.8)

        ax.set_xlabel('Features')
        ax.set_ylabel('Variance')
        ax.set_title('Feature Variance by Cluster', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(features, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('variance_by_cluster.png', 'clustering', self.cluster_method)

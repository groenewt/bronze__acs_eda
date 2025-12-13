"""Regression Visualizations"""
import numpy as np
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer


class RegressionVisualizer(BaseMLVisualizer):
    """Visualizes regression model results with comprehensive plots"""

    def viz_regression(self, result, X, y, target_name: str = None):
        self.target_name = target_name or 'Target'
        self.current_target = target_name  # Set for directory path
        self.model_name = getattr(result, 'model_name', 'unknown')
        self.feature_names = ', '.join(X.columns[:3].tolist())  # First 3 features for titles
        self._pred_actual(result)
        self._residuals(result)
        self._cv(result)
        self._features(result)
        self._learning_curve(result)
        self._feature_correlations(result, X, y)

    def _pred_actual(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, r.predictions, alpha=0.5, s=20)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel(f'Actual {self.target_name}')
        plt.ylabel(f'Predicted {self.target_name}')
        title = f'{r.model_name.upper()} - Target: {self.target_name}\nFeatures: {self.feature_names} (R²={r.test_score:.3f})'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('predictions.png', 'regression', self.model_name)

    def _residuals(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        res = y_test - r.predictions
        plt.figure(figsize=(10, 6))
        plt.scatter(r.predictions, res, alpha=0.5, s=20)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Predicted')
        plt.ylabel('Residuals')
        title = f'{r.model_name.upper()} Residuals - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('residuals.png', 'regression', self.model_name)

    def _cv(self, r):
        if not r.cv_scores:
            return
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, len(r.cv_scores) + 1), r.cv_scores, color='steelblue')
        mean = r.metadata.get('cv_mean', 0)
        plt.axhline(y=mean, color='r', linestyle='--', label=f'Mean: {mean:.3f}')
        plt.xlabel('Fold')
        plt.ylabel('R²')
        title = f'{r.model_name.upper()} Cross-Validation - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        self._save('cv_scores.png', 'regression', self.model_name)

    def _features(self, r):
        if not r.feature_importance:
            return
        plt.figure(figsize=(10, 6))
        items = sorted(r.feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
        names, vals = zip(*items)
        plt.barh(range(len(names)), vals, color='teal')
        plt.yticks(range(len(names)), names)
        plt.xlabel('Importance')
        title = f'{r.model_name.upper()} Top Features - Target: {self.target_name}'
        plt.title(title, fontweight='bold')
        plt.tight_layout()
        self._save('features.png', 'regression', self.model_name)

    def _learning_curve(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        res = y_test - r.predictions

        # Error distribution
        plt.figure(figsize=(10, 6))
        plt.hist(res, bins=30, edgecolor='black', alpha=0.7, color='coral')
        plt.axvline(x=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Error')
        plt.ylabel('Frequency')
        title = f'{r.model_name.upper()} Error Distribution - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('error_distribution.png', 'regression', self.model_name)

        # Actual vs Predicted distribution comparison
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(y_test, bins=30, alpha=0.7, color='blue', edgecolor='black', label='Actual')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Actual Distribution')
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.hist(r.predictions, bins=30, alpha=0.7, color='green', edgecolor='black', label='Predicted')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Predicted Distribution')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        self._save('distribution_comparison.png', 'regression', self.model_name)

        # Variance analysis
        actual_var = np.var(y_test)
        pred_var = np.var(r.predictions)
        plt.figure(figsize=(8, 6))
        plt.bar(['Actual', 'Predicted'], [actual_var, pred_var],
                color=['blue', 'green'], alpha=0.7, edgecolor='black')
        plt.ylabel('Variance')
        title = f'{r.model_name.upper()} Variance - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3, axis='y')
        for i, v in enumerate([actual_var, pred_var]):
            plt.text(i, v + actual_var * 0.02, f'{v:.2f}', ha='center', fontweight='bold')
        self._save('variance_comparison.png', 'regression', self.model_name)

    def _feature_correlations(self, r, X, y):
        """Visualize top feature correlations with target"""
        if not r.feature_importance or len(X) == 0:
            return

        top_features = sorted(r.feature_importance.items(),
                            key=lambda x: x[1], reverse=True)[:5]
        if not top_features:
            return

        fig, axes = plt.subplots(1, min(3, len(top_features)),
                                figsize=(15, 4))
        if len(top_features) == 1:
            axes = [axes]

        for idx, (feat_name, _) in enumerate(top_features[:3]):
            if feat_name in X.columns:
                ax = axes[idx] if len(top_features) > 1 else axes[0]
                ax.scatter(X[feat_name], y, alpha=0.3, s=10)
                ax.set_xlabel(feat_name)
                ax.set_ylabel(self.target_name)
                ax.set_title(f'{feat_name} vs {self.target_name}')
                ax.grid(alpha=0.3)

        plt.tight_layout()
        self._save('feature_target_correlation.png', 'regression', self.model_name)

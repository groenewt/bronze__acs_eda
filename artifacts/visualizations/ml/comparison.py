"""Model Comparison Visualizations"""
import numpy as np
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer


class ModelComparisonVisualizer(BaseMLVisualizer):
    """Visualizes comparison across multiple models"""

    def viz_model_comparison(self, model_results_dict, target_name: str = None):
        """Compare performance across multiple models"""
        self.target_name = target_name or 'Target'
        self.current_target = target_name  # Set for directory path
        self._compare_scores(model_results_dict)
        self._compare_cv_scores(model_results_dict)
        self._compare_metrics(model_results_dict)

    def _compare_scores(self, results_dict):
        """Compare R² scores across models"""
        if not results_dict:
            return

        models = []
        train_scores = []
        test_scores = []

        for model_name, result in results_dict.items():
            if hasattr(result, 'train_score') and hasattr(result, 'test_score'):
                models.append(model_name.replace('_', ' ').title())
                train_scores.append(result.train_score)
                test_scores.append(result.test_score or 0)

        if not models:
            return

        x = np.arange(len(models))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x - width/2, train_scores, width, label='Train R²', alpha=0.8, color='steelblue')
        ax.bar(x + width/2, test_scores, width, label='Test R²', alpha=0.8, color='coral')

        ax.set_xlabel('Model')
        ax.set_ylabel('R² Score')
        ax.set_title(f'Model Comparison - {self.target_name}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('model_comparison_scores.png', 'model_comparison')

    def _compare_cv_scores(self, results_dict):
        """Compare cross-validation scores across models"""
        if not results_dict:
            return

        models_with_cv = {}
        for model_name, result in results_dict.items():
            if hasattr(result, 'metadata') and result.metadata.get('cv_mean') is not None:
                models_with_cv[model_name] = {
                    'mean': result.metadata['cv_mean'],
                    'std': result.metadata.get('cv_std', 0)
                }

        if not models_with_cv:
            return

        models = [m.replace('_', ' ').title() for m in models_with_cv.keys()]
        means = [v['mean'] for v in models_with_cv.values()]
        stds = [v['std'] for v in models_with_cv.values()]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(range(len(models)), means, yerr=stds, alpha=0.8,
              color='teal', capsize=5, edgecolor='black')
        ax.set_xlabel('Model')
        ax.set_ylabel('CV R² (Mean ± Std)')
        ax.set_title(f'Cross-Validation Comparison - {self.target_name}', fontweight='bold')
        ax.set_xticks(range(len(models)))
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('model_comparison_cv.png', 'model_comparison')

    def _compare_metrics(self, results_dict):
        """Compare additional metrics (RMSE, MAE) across models"""
        if not results_dict:
            return

        models_with_metrics = {}
        for model_name, result in results_dict.items():
            if hasattr(result, 'metadata'):
                rmse = result.metadata.get('rmse')
                mae = result.metadata.get('mae')
                if rmse is not None and mae is not None:
                    models_with_metrics[model_name] = {'rmse': rmse, 'mae': mae}

        if not models_with_metrics:
            return

        models = [m.replace('_', ' ').title() for m in models_with_metrics.keys()]
        rmse_vals = [v['rmse'] for v in models_with_metrics.values()]
        mae_vals = [v['mae'] for v in models_with_metrics.values()]

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # RMSE comparison
        axes[0].bar(range(len(models)), rmse_vals, alpha=0.8, color='purple', edgecolor='black')
        axes[0].set_xlabel('Model')
        axes[0].set_ylabel('RMSE')
        axes[0].set_title('Root Mean Squared Error', fontweight='bold')
        axes[0].set_xticks(range(len(models)))
        axes[0].set_xticklabels(models, rotation=45, ha='right')
        axes[0].grid(alpha=0.3, axis='y')

        # MAE comparison
        axes[1].bar(range(len(models)), mae_vals, alpha=0.8, color='orange', edgecolor='black')
        axes[1].set_xlabel('Model')
        axes[1].set_ylabel('MAE')
        axes[1].set_title('Mean Absolute Error', fontweight='bold')
        axes[1].set_xticks(range(len(models)))
        axes[1].set_xticklabels(models, rotation=45, ha='right')
        axes[1].grid(alpha=0.3, axis='y')

        plt.tight_layout()
        self._save('model_comparison_metrics.png', 'model_comparison')

"""SHAP Visualizations"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend - must be before pyplot import
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer


class SHAPVisualizer(BaseMLVisualizer):
    """Visualizes SHAP explanations for model interpretability"""

    def viz_shap(self, shap_results: dict, target_name: str = None):
        """
        Visualize SHAP explanations for model interpretability.

        Args:
            shap_results: Dict from ModelExplainer.explain_model()
            target_name: Name of target variable
        """
        if not shap_results or 'error' in shap_results:
            return

        self.target_name = target_name or 'Target'
        self.current_target = target_name

        try:
            self._shap_summary_bar(shap_results)
            self._shap_summary_beeswarm(shap_results)
            self._shap_feature_importance(shap_results)
        except Exception as e:
            print(f"[WARNING] SHAP visualization failed: {e}")

    def _shap_summary_bar(self, shap_results: dict):
        """SHAP summary bar plot showing mean absolute SHAP values"""
        feature_importance = shap_results.get('feature_importance', {})
        if not feature_importance:
            return

        # Sort by importance
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15]
        features, values = zip(*sorted_features)

        plt.figure(figsize=(10, 8))
        y_pos = np.arange(len(features))
        plt.barh(y_pos, values, color='#ff6b6b', edgecolor='#c92a2a')
        plt.yticks(y_pos, features)
        plt.xlabel('Mean |SHAP Value|')
        plt.title(f'SHAP Feature Importance - {self.target_name}', fontweight='bold')
        plt.gca().invert_yaxis()  # Most important at top
        plt.tight_layout()
        self._save('shap_importance_bar.png', 'shap')

    def _shap_summary_beeswarm(self, shap_results: dict):
        """SHAP beeswarm plot showing distribution of SHAP values"""
        try:
            import shap as shap_lib
            shap_values = shap_results.get('shap_values')
            X_test = shap_results.get('X_test')
            feature_names = shap_results.get('feature_names', [])

            if shap_values is None or X_test is None:
                return

            plt.figure(figsize=(12, 8))
            # Use SHAP's built-in summary plot
            shap_lib.summary_plot(shap_values, X_test, feature_names=feature_names,
                                 show=False, max_display=15)
            plt.title(f'SHAP Summary - {self.target_name}', fontweight='bold')
            plt.tight_layout()
            self._save('shap_summary_beeswarm.png', 'shap')
        except Exception as e:
            print(f"[WARNING] SHAP beeswarm plot failed: {e}")

    def _shap_feature_importance(self, shap_results: dict):
        """Detailed SHAP feature importance with statistics"""
        feature_importance = shap_results.get('feature_importance', {})
        if not feature_importance:
            return

        # Get top 10 features
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: Bar chart
        features, values = zip(*sorted_features)
        axes[0].barh(range(len(features)), values, color='steelblue')
        axes[0].set_yticks(range(len(features)))
        axes[0].set_yticklabels(features)
        axes[0].set_xlabel('Mean |SHAP Value|')
        axes[0].set_title('Top 10 Features by SHAP', fontweight='bold')
        axes[0].invert_yaxis()

        # Right: Pie chart for relative importance
        total = sum(values)
        percentages = [v/total*100 for v in values]
        colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(features)))
        axes[1].pie(percentages, labels=[f[:15] for f in features], autopct='%1.1f%%',
                   colors=colors, startangle=90)
        axes[1].set_title('Relative Feature Importance', fontweight='bold')

        plt.tight_layout()
        self._save('shap_feature_analysis.png', 'shap')

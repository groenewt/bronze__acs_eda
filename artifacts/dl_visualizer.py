"""
Deep Learning Visualization Module
Provides comprehensive visualization for deep learning results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

from config import Config
from exceptions import VisualizationError, PlotCreationError
from deep_learning import DLResults, TrainingConfig
from visual_registry import get_registry, register_visual

# Set plotting style
sns.set_style("whitegrid")
sns.set_palette("husl")


# ============================================================================
# DEEP LEARNING VISUALIZER
# ============================================================================

class DLVisualizer:
    """Comprehensive deep learning visualization suite"""

    def __init__(self, config: Config, survey_type: str):
        self.config = config
        self.survey_type = survey_type
        self.fig_dir = os.path.join(config.figure_dir, 'ml', 'deep_learning')
        os.makedirs(self.fig_dir, exist_ok=True)

    def visualize_all(self, results: Dict[str, DLResults]):
        """Create all visualizations - each task uses own test data (≤10 lines)"""
        for task_name, dl_results in results.items():
            self._create_task_dir(task_name)
            # Use test data stored in each DLResults object (avoids shape mismatch)
            self._visualize_task(task_name, dl_results, dl_results.X_test, dl_results.y_test)
        self.plot_learning_curves(results)
        self.plot_model_comparison(results)
        self.plot_comprehensive_dashboard(results)

    def _create_task_dir(self, task_name: str):
        """Create task-specific directory (≤10 lines)"""
        task_dir = os.path.join(self.fig_dir, task_name)
        os.makedirs(task_dir, exist_ok=True)
        return task_dir

    def _visualize_task(self, task_name: str, results: DLResults,
                       X_test: np.ndarray, y_test: np.ndarray):
        """Create all task-specific visualizations (≤10 lines)"""
        self.plot_training_history(results, task_name)
        self.plot_predictions_vs_actual(results, y_test, task_name)
        self.plot_residuals(results, y_test, task_name)
        self.plot_error_distribution(results, y_test, task_name)
        self.plot_architecture_summary(results, task_name)
        self.plot_target_specific_analysis(results, y_test, task_name)
        self.plot_convergence_analysis(results, task_name)
        self.plot_error_evolution(results, task_name)

    def plot_training_history(self, results: DLResults, task_name: str):
        """Plot training/validation loss and metrics (≤10 lines)"""
        try:
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            self._plot_loss_curve(axes[0], results)
            self._plot_metric_curve(axes[1], results)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/training_history')
        except Exception as e:
            raise PlotCreationError('training_history', str(e))

    def _plot_loss_curve(self, ax, results: DLResults):
        """Plot loss curves with detailed title (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        ax.plot(epochs, results.history['loss'], 'b-', label='Training Loss', linewidth=2)
        ax.plot(epochs, results.history['val_loss'], 'r-', label='Validation Loss', linewidth=2)
        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel('Loss', fontsize=12)
        targets_str = ', '.join(results.targets[:3]) + ('...' if len(results.targets) > 3 else '')
        ax.set_title(f'{results.model_type} | Targets: [{targets_str}]', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_metric_curve(self, ax, results: DLResults):
        """Plot metric curves with task type (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        metric_key = 'mae' if 'mae' in results.history else 'accuracy'
        val_key = f'val_{metric_key}'
        ax.plot(epochs, results.history[metric_key], 'b-', label=f'Train {metric_key.upper()}', linewidth=2)
        ax.plot(epochs, results.history[val_key], 'r-', label=f'Val {metric_key.upper()}', linewidth=2)
        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel(metric_key.upper(), fontsize=12)
        ax.set_title(f'{results.task_type.title()} Task | {metric_key.upper()} Evolution', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def plot_predictions_vs_actual(self, results: DLResults, y_test: np.ndarray,
                                   task_name: str):
        """Plot predictions vs actual values (≤10 lines)"""
        try:
            if results.task_type in ['regression', 'multi_output']:
                self._plot_regression_predictions(results, y_test, task_name)
            else:
                self._plot_classification_predictions(results, y_test, task_name)
        except Exception as e:
            raise PlotCreationError('predictions_vs_actual', str(e))

    def _plot_regression_predictions(self, results: DLResults, y_test: np.ndarray,
                                     task_name: str):
        """Plot regression predictions (≤10 lines)"""
        num_targets = results.predictions.shape[1] if len(results.predictions.shape) > 1 else 1
        fig, axes = plt.subplots(1, min(num_targets, 3), figsize=(15, 5))
        if num_targets == 1:
            axes = [axes]
        for i, ax in enumerate(axes):
            self._scatter_pred_actual(ax, y_test[:, i], results.predictions[:, i],
                                     results.targets[i])
        plt.tight_layout()
        self._save_dl_fig(f'{task_name}/predictions_vs_actual')

    def _scatter_pred_actual(self, ax, y_true, y_pred, target_name):
        """Create scatter plot with enhanced metrics (≤10 lines)"""
        ax.scatter(y_true, y_pred, alpha=0.5, s=20, c='steelblue', edgecolors='black', linewidths=0.5)
        min_val, max_val = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        ax.set_xlabel(f'Actual {target_name}', fontsize=11)
        ax.set_ylabel(f'Predicted {target_name}', fontsize=11)
        r2 = r2_score(y_true, y_pred)
        mae = np.mean(np.abs(y_true - y_pred))
        ax.set_title(f'{target_name} | R²={r2:.3f} | MAE={mae:.2f}', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_classification_predictions(self, results: DLResults, y_test: np.ndarray,
                                         task_name: str):
        """Plot classification confusion matrix (≤10 lines)"""
        from sklearn.metrics import confusion_matrix
        y_true_classes = y_test.argmax(axis=1) if len(y_test.shape) > 1 else y_test
        y_pred_classes = results.predictions.argmax(axis=1)
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'})
        plt.xlabel('Predicted Class', fontsize=12)
        plt.ylabel('True Class', fontsize=12)
        plt.title(f'Confusion Matrix: {results.model_type}', fontsize=14, fontweight='bold')
        self._save_dl_fig(f'{task_name}/confusion_matrix')

    def plot_residuals(self, results: DLResults, y_test: np.ndarray, task_name: str):
        """Plot residual analysis with shape validation (≤10 lines)"""
        try:
            if results.task_type not in ['regression', 'multi_output']:
                return
            # Ensure shapes match before calculating residuals
            if y_test.shape != results.predictions.shape:
                print(f"[WARNING] Shape mismatch for {task_name}: y_test {y_test.shape} vs predictions {results.predictions.shape}")
                return
            residuals = y_test - results.predictions
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            self._plot_residual_scatter(axes[0], results.predictions, residuals, task_name, results.model_type)
            self._plot_residual_histogram(axes[1], residuals, task_name)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/residual_analysis')
        except Exception as e:
            print(f"[WARNING] DL visualization failed: {e}  [plot_type=residuals, reason={e}]")

    def _plot_residual_scatter(self, ax, predictions, residuals, task_name, model_type):
        """Plot residual scatter with task info (≤10 lines)"""
        ax.scatter(predictions.flatten(), residuals.flatten(), alpha=0.5, s=20)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax.set_xlabel('Predicted Values', fontsize=12)
        ax.set_ylabel('Residuals', fontsize=12)
        title = f'{task_name.replace("_", " ").title()} | {model_type} | Residuals'
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)

    def _plot_residual_histogram(self, ax, residuals, task_name):
        """Plot residual distribution with normality test (≤10 lines)"""
        ax.hist(residuals.flatten(), bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax.axvline(x=0, color='r', linestyle='--', linewidth=2, label='Zero')
        mean_res = residuals.flatten().mean()
        ax.axvline(x=mean_res, color='g', linestyle=':', linewidth=2, label=f'Mean: {mean_res:.2e}')
        ax.set_xlabel('Residual Value', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'{task_name.replace("_", " ").title()} | Residual Distribution', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def plot_error_distribution(self, results: DLResults, y_test: np.ndarray,
                               task_name: str):
        """Plot error distribution analysis (≤10 lines)"""
        try:
            if results.task_type not in ['regression', 'multi_output']:
                return
            errors = np.abs(y_test - results.predictions)
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            self._plot_error_histogram(axes[0], errors)
            self._plot_error_boxplot(axes[1], errors, results.targets)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/error_distribution')
        except Exception as e:
            raise PlotCreationError('error_distribution', str(e))

    def _plot_error_histogram(self, ax, errors):
        """Plot error histogram (≤10 lines)"""
        ax.hist(errors.flatten(), bins=50, edgecolor='black', alpha=0.7, color='salmon')
        ax.set_xlabel('Absolute Error', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Prediction Error Distribution', fontsize=14, fontweight='bold')
        ax.axvline(x=errors.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {errors.mean():.2f}')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_error_boxplot(self, ax, errors, targets):
        """Plot error boxplot by target (≤10 lines)"""
        if len(errors.shape) > 1 and errors.shape[1] > 1:
            bp = ax.boxplot([errors[:, i] for i in range(errors.shape[1])],
                            labels=targets, patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
        else:
            bp = ax.boxplot(errors.flatten(), labels=['All'], patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
        ax.set_ylabel('Absolute Error', fontsize=12)
        ax.set_title('Error Distribution by Target', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

    def plot_architecture_summary(self, results: DLResults, task_name: str):
        """Plot architecture summary (≤10 lines)"""
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            self._create_architecture_text(ax, results)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/architecture_summary')
        except Exception as e:
            raise PlotCreationError('architecture_summary', str(e))

    def _create_architecture_text(self, ax, results: DLResults):
        """Create architecture text visualization (≤10 lines)"""
        ax.axis('off')
        info_lines = [
            f"Model: {results.model_type}",
            f"Task Type: {results.task_type}",
            f"Targets: {', '.join(results.targets)}",
            f"\nArchitecture:",
            f"  Total Layers: {results.architecture.get('layers', 'N/A')}",
            f"  Total Parameters: {results.architecture.get('params', 'N/A'):,}",
            f"\nPerformance:",
        ]
        for metric, value in results.test_metrics.items():
            info_lines.append(f"  {metric.upper()}: {value:.4f}")
        ax.text(0.1, 0.9, '\n'.join(info_lines), transform=ax.transAxes,
               fontsize=12, verticalalignment='top', family='monospace')

    def plot_feature_importance(self, results: DLResults, feature_names: List[str],
                               task_name: str):
        """Plot feature importance (≤10 lines)"""
        try:
            if results.feature_importance is None:
                return
            importances = sorted(results.feature_importance.items(),
                               key=lambda x: x[1], reverse=True)[:20]
            fig, ax = plt.subplots(figsize=(12, 8))
            features, values = zip(*importances)
            ax.barh(range(len(features)), values, color='steelblue')
            ax.set_yticks(range(len(features)))
            ax.set_yticklabels(features)
            ax.set_xlabel('Importance Score', fontsize=12)
            ax.set_title('Top 20 Feature Importances', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/feature_importance')
        except Exception as e:
            raise PlotCreationError('feature_importance', str(e))

    def plot_learning_curves(self, results: Dict[str, DLResults]):
        """Plot learning curves comparison (≤10 lines)"""
        try:
            fig, axes = plt.subplots(len(results), 2, figsize=(15, 5 * len(results)))
            for idx, (task_name, dl_results) in enumerate(results.items()):
                row_axes = axes[idx] if len(results) > 1 else axes
                self._plot_loss_curve(row_axes[0], dl_results)
                self._plot_metric_curve(row_axes[1], dl_results)
                row_axes[0].set_title(f'{task_name}: Loss', fontsize=12, fontweight='bold')
                row_axes[1].set_title(f'{task_name}: Metrics', fontsize=12, fontweight='bold')
            plt.tight_layout()
            self._save_dl_fig('learning_curves_comparison')
        except Exception as e:
            raise PlotCreationError('learning_curves', str(e))

    def plot_model_comparison(self, results: Dict[str, DLResults]):
        """Plot model performance comparison (≤10 lines)"""
        try:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            self._plot_metric_comparison_bar(axes[0], results)
            self._plot_loss_comparison_bar(axes[1], results)
            plt.tight_layout()
            self._save_dl_fig('model_comparison')
        except Exception as e:
            raise PlotCreationError('model_comparison', str(e))

    def _plot_metric_comparison_bar(self, ax, results: Dict[str, DLResults]):
        """Plot metric comparison (≤10 lines)"""
        tasks = list(results.keys())
        metric_key = 'r2' if 'r2' in list(results.values())[0].test_metrics else 'accuracy'
        values = [res.test_metrics.get(metric_key, 0) for res in results.values()]
        ax.bar(range(len(tasks)), values, color='steelblue', edgecolor='black')
        ax.set_xticks(range(len(tasks)))
        ax.set_xticklabels(tasks, rotation=45, ha='right')
        ax.set_ylabel(metric_key.upper(), fontsize=12)
        ax.set_title(f'{metric_key.upper()} Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

    def _plot_loss_comparison_bar(self, ax, results: Dict[str, DLResults]):
        """Plot loss comparison (≤10 lines)"""
        tasks = list(results.keys())
        train_loss = [res.train_loss for res in results.values()]
        val_loss = [res.val_loss for res in results.values()]
        x = np.arange(len(tasks))
        ax.bar(x - 0.2, train_loss, 0.4, label='Train Loss', color='skyblue', edgecolor='black')
        ax.bar(x + 0.2, val_loss, 0.4, label='Val Loss', color='salmon', edgecolor='black')
        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=45, ha='right')
        ax.set_ylabel('Loss', fontsize=12)
        ax.set_title('Loss Comparison', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    def plot_target_specific_analysis(self, results: DLResults, y_test: np.ndarray,
                                      task_name: str):
        """Plot per-target detailed analysis (≤10 lines)"""
        try:
            if results.task_type not in ['regression', 'multi_output']:
                return
            for idx, target in enumerate(results.targets):
                fig = self._create_target_figure(y_test[:, idx], results.predictions[:, idx], target)
                self._save_dl_fig(f'{task_name}/{target}_detailed_analysis')
        except Exception as e:
            raise PlotCreationError('target_specific_analysis', str(e))

    def _create_target_figure(self, y_true, y_pred, target_name):
        """Create detailed target analysis (≤10 lines)"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        self._plot_target_scatter(axes[0, 0], y_true, y_pred, target_name)
        self._plot_target_residuals(axes[0, 1], y_true, y_pred, target_name)
        self._plot_target_qq(axes[1, 0], y_true - y_pred, target_name)
        self._plot_target_percentiles(axes[1, 1], y_true, y_pred, target_name)
        plt.tight_layout()
        return fig

    def _plot_target_scatter(self, ax, y_true, y_pred, target):
        """Plot target scatter with error bands and metrics (≤10 lines)"""
        ax.scatter(y_true, y_pred, alpha=0.4, s=15, c='steelblue', edgecolors='black', linewidths=0.3)
        min_val, max_val = y_true.min(), y_true.max()
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect')
        margin = (max_val - min_val) * 0.1
        ax.fill_between([min_val, max_val], [min_val-margin, max_val-margin],
                        [min_val+margin, max_val+margin], alpha=0.2, color='red', label='±10%')
        r2 = r2_score(y_true, y_pred)
        ax.set_xlabel(f'Actual {target}', fontsize=11)
        ax.set_ylabel(f'Predicted {target}', fontsize=11)
        ax.set_title(f'{target} | R²={r2:.3f} | Predictions vs Actual', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_target_residuals(self, ax, y_true, y_pred, target):
        """Plot target residuals with fit line (≤10 lines)"""
        residuals = y_true - y_pred
        ax.scatter(y_pred, residuals, alpha=0.4, s=15, c='coral')
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        z = np.polyfit(y_pred, residuals, 1)
        p = np.poly1d(z)
        ax.plot(sorted(y_pred), p(sorted(y_pred)), "g-", linewidth=2, label='Trend')
        ax.set_xlabel(f'Predicted {target}', fontsize=11)
        ax.set_ylabel('Residuals', fontsize=11)
        ax.set_title(f'{target}: Residual Analysis', fontsize=12, fontweight='bold')
        ax.legend()

    def _plot_target_qq(self, ax, residuals, target):
        """Plot Q-Q plot for residuals (≤10 lines)"""
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=ax)
        ax.set_title(f'{target}: Q-Q Plot (Normality Check)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)

    def _plot_target_percentiles(self, ax, y_true, y_pred, target):
        """Plot percentile comparison (≤10 lines)"""
        percentiles = [10, 25, 50, 75, 90]
        true_pct = np.percentile(y_true, percentiles)
        pred_pct = np.percentile(y_pred, percentiles)
        x = np.arange(len(percentiles))
        ax.plot(x, true_pct, 'o-', label='Actual', linewidth=2, markersize=8)
        ax.plot(x, pred_pct, 's-', label='Predicted', linewidth=2, markersize=8)
        ax.set_xticks(x)
        ax.set_xticklabels([f'{p}%' for p in percentiles])
        ax.set_ylabel('Value', fontsize=11)
        ax.set_title(f'{target}: Percentile Comparison', fontsize=12, fontweight='bold')
        ax.legend()

    def plot_convergence_analysis(self, results: DLResults, task_name: str):
        """Plot convergence diagnostics (≤10 lines)"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            self._plot_loss_delta(axes[0, 0], results)
            self._plot_metric_delta(axes[0, 1], results)
            self._plot_overfitting_gap(axes[1, 0], results)
            self._plot_early_stopping_point(axes[1, 1], results)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/{task_name}_convergence_diagnostics')
        except Exception as e:
            raise PlotCreationError('convergence_analysis', str(e))

    def _plot_loss_delta(self, ax, results: DLResults):
        """Plot loss change rate with model info (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        loss_delta = np.diff(results.history['loss'], prepend=results.history['loss'][0])
        ax.plot(epochs, loss_delta, 'b-', linewidth=2, label='Train Loss Δ')
        ax.axhline(y=0, color='r', linestyle='--', linewidth=1, label='Zero Change')
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Loss Change', fontsize=11)
        ax.set_title(f'{results.model_type} | Loss Convergence Rate', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_metric_delta(self, ax, results: DLResults):
        """Plot metric improvement rate (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        metric_key = 'mae' if 'mae' in results.history else 'accuracy'
        metric_delta = np.diff(results.history[metric_key], prepend=results.history[metric_key][0])
        ax.plot(epochs, metric_delta, 'g-', linewidth=2, label=f'{metric_key.upper()} Δ')
        ax.axhline(y=0, color='r', linestyle='--', linewidth=1)
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Metric Change', fontsize=11)
        ax.set_title('Metric Improvement Rate', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_overfitting_gap(self, ax, results: DLResults):
        """Plot train-validation gap (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        gap = np.array(results.history['val_loss']) - np.array(results.history['loss'])
        ax.plot(epochs, gap, 'r-', linewidth=2, label='Val - Train Loss')
        ax.fill_between(epochs, 0, gap, where=(gap > 0), alpha=0.3, color='red', label='Overfitting')
        ax.axhline(y=0, color='k', linestyle='-', linewidth=1)
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Loss Gap', fontsize=11)
        ax.set_title('Overfitting Monitor', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_early_stopping_point(self, ax, results: DLResults):
        """Plot early stopping analysis (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        val_loss = results.history['val_loss']
        best_epoch = np.argmin(val_loss) + 1
        ax.plot(epochs, val_loss, 'b-', linewidth=2, label='Val Loss')
        ax.axvline(x=best_epoch, color='g', linestyle='--', linewidth=2, label=f'Best: Epoch {best_epoch}')
        ax.scatter([best_epoch], [val_loss[best_epoch-1]], color='red', s=100, zorder=5)
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Validation Loss', fontsize=11)
        ax.set_title('Early Stopping Point', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def plot_error_evolution(self, results: DLResults, task_name: str):
        """Plot error metrics over epochs (≤10 lines)"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            self._plot_mae_evolution(axes[0, 0], results)
            self._plot_mse_evolution(axes[0, 1], results)
            self._plot_loss_ratio(axes[1, 0], results)
            self._plot_validation_stability(axes[1, 1], results)
            plt.tight_layout()
            self._save_dl_fig(f'{task_name}/{task_name}_error_evolution')
        except Exception as e:
            raise PlotCreationError('error_evolution', str(e))

    def _plot_mae_evolution(self, ax, results: DLResults):
        """Plot MAE over epochs (≤10 lines)"""
        if 'mae' not in results.history:
            ax.text(0.5, 0.5, 'MAE not available', ha='center', va='center', transform=ax.transAxes)
            return
        epochs = range(1, len(results.history['mae']) + 1)
        ax.plot(epochs, results.history['mae'], 'b-', linewidth=2, label='Train MAE')
        ax.plot(epochs, results.history['val_mae'], 'r-', linewidth=2, label='Val MAE')
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Mean Absolute Error', fontsize=11)
        ax.set_title('MAE Evolution', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_mse_evolution(self, ax, results: DLResults):
        """Plot MSE over epochs (≤10 lines)"""
        if 'mse' not in results.history:
            ax.text(0.5, 0.5, 'MSE not available', ha='center', va='center', transform=ax.transAxes)
            return
        epochs = range(1, len(results.history['mse']) + 1)
        ax.plot(epochs, results.history['mse'], 'b-', linewidth=2, label='Train MSE')
        ax.plot(epochs, results.history['val_mse'], 'r-', linewidth=2, label='Val MSE')
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Mean Squared Error', fontsize=11)
        ax.set_title('MSE Evolution', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_loss_ratio(self, ax, results: DLResults):
        """Plot validation/train loss ratio (≤10 lines)"""
        epochs = range(1, len(results.history['loss']) + 1)
        ratio = np.array(results.history['val_loss']) / (np.array(results.history['loss']) + 1e-10)
        ax.plot(epochs, ratio, 'purple', linewidth=2, label='Val/Train Loss Ratio')
        ax.axhline(y=1.0, color='g', linestyle='--', linewidth=1, label='Ideal (1.0)')
        ax.fill_between(epochs, 1.0, ratio, where=(ratio > 1.0), alpha=0.2, color='red')
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Loss Ratio', fontsize=11)
        ax.set_title('Generalization Monitor', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_validation_stability(self, ax, results: DLResults):
        """Plot validation loss stability (≤10 lines)"""
        val_loss = results.history['val_loss']
        window = min(5, len(val_loss) // 4)
        rolling_std = pd.Series(val_loss).rolling(window=window, min_periods=1).std()
        epochs = range(1, len(val_loss) + 1)
        ax.plot(epochs, rolling_std, 'orange', linewidth=2, label=f'{window}-Epoch Rolling Std')
        ax.fill_between(epochs, 0, rolling_std, alpha=0.3, color='orange')
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Val Loss Std Dev', fontsize=11)
        ax.set_title('Validation Stability', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def plot_comprehensive_dashboard(self, results: Dict[str, DLResults]):
        """Create comprehensive performance dashboard (≤10 lines)"""
        try:
            num_tasks = len(results)
            fig = plt.figure(figsize=(20, 12))
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
            self._add_dashboard_summary(fig, gs[0, :], results)
            self._add_dashboard_comparisons(fig, gs[1:, :], results)
            self._save_dl_fig('comprehensive_performance_dashboard')
        except Exception as e:
            raise PlotCreationError('comprehensive_dashboard', str(e))

    def _add_dashboard_summary(self, fig, grid_spec, results):
        """Add summary section to dashboard (≤10 lines)"""
        ax = fig.add_subplot(grid_spec)
        ax.axis('off')
        summary_lines = ['DEEP LEARNING PERFORMANCE SUMMARY\n' + '='*60]
        for task, res in results.items():
            summary_lines.append(f'\n{task.upper()}:')
            summary_lines.append(f'  Model: {res.model_type} | Task: {res.task_type}')
            summary_lines.append(f'  Targets: {", ".join(res.targets[:3])}{"..." if len(res.targets) > 3 else ""}')
            summary_lines.append(f'  Metrics: ' + ' | '.join([f'{k.upper()}={v:.4f}' for k, v in list(res.test_metrics.items())[:3]]))
        ax.text(0.05, 0.95, '\n'.join(summary_lines), transform=ax.transAxes,
               fontsize=10, verticalalignment='top', family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    def _add_dashboard_comparisons(self, fig, grid_spec, results):
        """Add comparison plots to dashboard (≤10 lines)"""
        from matplotlib.gridspec import GridSpecFromSubplotSpec
        inner_gs = GridSpecFromSubplotSpec(2, 3, subplot_spec=grid_spec)
        ax1 = fig.add_subplot(inner_gs[0, 0])
        ax2 = fig.add_subplot(inner_gs[0, 1])
        ax3 = fig.add_subplot(inner_gs[0, 2])
        ax4 = fig.add_subplot(inner_gs[1, 0:2])
        ax5 = fig.add_subplot(inner_gs[1, 2])
        self._plot_metric_comparison_bar(ax1, results)
        self._plot_loss_comparison_bar(ax2, results)
        self._dashboard_task_metrics(ax3, results)
        self._dashboard_convergence_comparison(ax4, results)
        self._dashboard_architecture_comparison(ax5, results)

    def _dashboard_task_metrics(self, ax, results):
        """Plot task metrics heatmap (≤10 lines)"""
        tasks = list(results.keys())
        metrics = ['mae', 'mse', 'r2']
        data = [[res.test_metrics.get(m, 0) for m in metrics] for res in results.values()]
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto')
        ax.set_xticks(range(len(metrics)))
        ax.set_xticklabels([m.upper() for m in metrics])
        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels(tasks, fontsize=9)
        ax.set_title('Metrics Heatmap', fontsize=11, fontweight='bold')
        plt.colorbar(im, ax=ax)

    def _dashboard_convergence_comparison(self, ax, results):
        """Plot convergence comparison (≤10 lines)"""
        for task, res in results.items():
            epochs = range(1, len(res.history['val_loss']) + 1)
            ax.plot(epochs, res.history['val_loss'], label=task, linewidth=2, alpha=0.8)
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Validation Loss', fontsize=11)
        ax.set_title('Convergence Comparison', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    def _dashboard_architecture_comparison(self, ax, results):
        """Plot architecture size comparison (≤10 lines)"""
        tasks = list(results.keys())
        params = [res.architecture.get('params', 0) for res in results.values()]
        colors = plt.cm.viridis(np.linspace(0, 1, len(tasks)))
        ax.barh(range(len(tasks)), params, color=colors, edgecolor='black')
        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels(tasks, fontsize=9)
        ax.set_xlabel('Parameters (count)', fontsize=11)
        ax.set_title('Model Complexity', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

    def _save_dl_fig(self, filename: str):
        """Save deep learning figure and register (≤10 lines)"""
        if not filename.endswith('.png'):
            filename = f"{filename}.png"
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = os.path.join(self.fig_dir, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        self._register_dl_visual(path, filename)

    def _register_dl_visual(self, path: str, filename: str):
        """Register DL visualization in registry (≤10 lines)"""
        try:
            title = filename.replace('_', ' ').replace('.png', '')
            task_name = filename.split('/')[0] if '/' in filename else None
            register_visual(path=path, visual_type='deep_learning', title=title,
                          category='ml', task_name=task_name,
                          subdirectory=task_name)
        except Exception as e:
            print(f"[WARNING] Failed to register DL visual {path}: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def r2_score(y_true, y_pred):
    """Calculate R² score (≤10 lines)"""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / (ss_tot + 1e-10))

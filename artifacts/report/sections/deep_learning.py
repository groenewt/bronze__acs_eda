"""
Deep Learning Models Section - Neural network analysis and performance reporting.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class DeepLearningSection(BaseReportSection):
    """Deep learning models section with comprehensive neural network reporting."""

    def get_filename(self) -> str:
        return "11b_deep_learning_models.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Deep Learning Models")]

        # Add section description
        content.append(self.md.blockquote(
            "Neural network analysis using TensorFlow/Keras for complex pattern recognition "
            "and multi-output prediction tasks."
        ))
        content.append("")

        if not data or not isinstance(data, dict) or len(data) == 0:
            content.append("_No deep learning models were trained for this dataset._")
            return "\n".join(content)

        content.append(self._dl_summary(data))
        content.append(self._dl_tasks(data))
        content.append(self._model_comparison(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _dl_summary(self, data: Dict) -> str:
        """Generate deep learning summary section."""
        lines = [self.md.h2("Deep Learning Summary")]

        # Count tasks and models
        task_count = len(data)
        task_names = list(data.keys())

        lines.append(self.md.metric("Total Tasks", task_count))
        lines.append(self.md.metric("Tasks", ", ".join(t.replace('_', ' ').title() for t in task_names[:5])))

        # Aggregate performance
        total_params = 0
        avg_val_loss = 0
        valid_count = 0

        for task_name, dl_result in data.items():
            if hasattr(dl_result, 'architecture'):
                params = dl_result.architecture.get('params', 0)
                total_params += params
            if hasattr(dl_result, 'val_loss'):
                avg_val_loss += dl_result.val_loss
                valid_count += 1

        if valid_count > 0:
            avg_val_loss /= valid_count

        lines.append("")
        lines.append(self.md.h3("Aggregate Statistics"))

        headers = ["Metric", "Value"]
        rows = [
            ["Total Parameters", f"{total_params:,}"],
            ["Average Validation Loss", f"{avg_val_loss:.4f}"],
            ["Number of Tasks", str(task_count)],
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines) + "\n"

    def _dl_tasks(self, data: Dict) -> str:
        """Generate detailed task sections."""
        lines = []
        for task_name, dl_result in data.items():
            lines.append(self._format_task(task_name, dl_result))
        return "\n".join(lines)

    def _format_task(self, task_name: str, dl_result) -> str:
        """Format a single deep learning task with comprehensive details."""
        lines = [self.md.h2(f"Task: {task_name.replace('_', ' ').title()}")]

        # Model details
        lines.append(self._task_details(dl_result))

        # Architecture details
        lines.append(self._architecture_details(dl_result))

        # Performance metrics
        lines.append(self._task_metrics(dl_result))

        # Training history analysis
        lines.append(self._training_analysis(dl_result))

        return "\n".join(lines) + "\n"

    def _task_details(self, dl_result) -> str:
        """Generate task details section."""
        lines = [self.md.h3("Model Configuration")]

        model_type = getattr(dl_result, 'model_type', 'N/A')
        task_type = getattr(dl_result, 'task_type', 'N/A')
        targets = getattr(dl_result, 'targets', [])
        metadata = getattr(dl_result, 'metadata', {})
        features = metadata.get('features', [])

        headers = ["Property", "Value"]
        rows = [
            ["Model Type", model_type],
            ["Task Type", task_type.title()],
            ["Target Variables", ", ".join(targets[:5]) + ("..." if len(targets) > 5 else "")],
            ["Number of Targets", str(len(targets))],
            ["Input Features", str(len(features))],
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines) + "\n"

    def _architecture_details(self, dl_result) -> str:
        """Generate architecture details section."""
        lines = [self.md.h3("Network Architecture")]

        architecture = getattr(dl_result, 'architecture', {})
        layers = architecture.get('layers', 'N/A')
        params = architecture.get('params', 0)
        layer_config = architecture.get('layer_config', [])

        headers = ["Component", "Value", "Notes"]
        rows = [
            ["Total Layers", str(layers), "Including input and output"],
            ["Total Parameters", f"{params:,}", "Trainable weights"],
            ["Parameters per Layer", f"{params // max(layers, 1):,}" if isinstance(layers, int) else "—", "Average"],
        ]
        lines.append(self.md.table(headers, rows))

        # Layer-by-layer breakdown if available
        if layer_config:
            lines.append("")
            lines.append(self.md.h4("Layer Configuration"))

            layer_headers = ["Layer", "Type", "Units/Filters", "Activation"]
            layer_rows = []
            for i, layer in enumerate(layer_config[:10]):  # Limit to 10 layers
                if isinstance(layer, dict):
                    layer_rows.append([
                        f"Layer {i+1}",
                        layer.get('type', '—'),
                        str(layer.get('units', layer.get('filters', '—'))),
                        layer.get('activation', '—')
                    ])
            if layer_rows:
                lines.append(self.md.table(layer_headers, layer_rows))

        return "\n".join(lines) + "\n"

    def _task_metrics(self, dl_result) -> str:
        """Generate performance metrics section."""
        lines = [self.md.h3("Performance Metrics")]

        train_loss = getattr(dl_result, 'train_loss', 0)
        val_loss = getattr(dl_result, 'val_loss', 0)
        test_metrics = getattr(dl_result, 'test_metrics', {})

        # Calculate overfitting risk
        overfitting_gap = val_loss - train_loss
        if overfitting_gap > 0.5:
            risk_level = "HIGH"
            risk_desc = "Model may be overfitting significantly"
        elif overfitting_gap > 0.2:
            risk_level = "MODERATE"
            risk_desc = "Some overfitting detected"
        elif overfitting_gap > 0.05:
            risk_level = "LOW"
            risk_desc = "Minimal overfitting"
        else:
            risk_level = "NONE"
            risk_desc = "Good generalization"

        headers = ["Metric", "Value", "Assessment"]
        rows = [
            ["Training Loss", f"{train_loss:.4f}", "Final epoch"],
            ["Validation Loss", f"{val_loss:.4f}", "Final epoch"],
            ["Loss Gap", f"{overfitting_gap:.4f}", f"{risk_level} overfitting risk"],
        ]
        lines.append(self.md.table(headers, rows))

        lines.append("")
        lines.append(self.md.interpretation(risk_desc))

        # Test metrics
        if test_metrics:
            lines.append("")
            lines.append(self.md.h4("Test Set Metrics"))

            headers = ["Metric", "Value", "Description"]
            rows = []
            for metric_name, metric_val in test_metrics.items():
                desc = self._get_metric_description(metric_name)
                rows.append([metric_name.upper(), f"{metric_val:.4f}", desc])
            lines.append(self.md.table(headers, rows))

        return "\n".join(lines) + "\n"

    def _get_metric_description(self, metric_name: str) -> str:
        """Get description for common metrics."""
        descriptions = {
            'mae': "Mean Absolute Error (lower is better)",
            'mse': "Mean Squared Error (lower is better)",
            'rmse': "Root Mean Squared Error (lower is better)",
            'r2': "R-squared (higher is better)",
            'mape': "Mean Absolute Percentage Error (%)",
            'accuracy': "Classification accuracy (higher is better)",
            'precision': "Precision score (higher is better)",
            'recall': "Recall score (higher is better)",
            'f1': "F1 score (higher is better)",
        }
        return descriptions.get(metric_name.lower(), "—")

    def _training_analysis(self, dl_result) -> str:
        """Generate training history analysis."""
        lines = [self.md.h3("Training Analysis")]

        history = getattr(dl_result, 'history', {})
        if not history:
            lines.append("_Training history not available._")
            return "\n".join(lines)

        loss_history = history.get('loss', [])
        val_loss_history = history.get('val_loss', [])

        if loss_history:
            epochs_trained = len(loss_history)
            initial_loss = loss_history[0]
            final_loss = loss_history[-1]
            improvement = ((initial_loss - final_loss) / initial_loss) * 100 if initial_loss > 0 else 0

            headers = ["Training Statistic", "Value"]
            rows = [
                ["Epochs Trained", str(epochs_trained)],
                ["Initial Training Loss", f"{initial_loss:.4f}"],
                ["Final Training Loss", f"{final_loss:.4f}"],
                ["Loss Improvement", f"{improvement:.1f}%"],
            ]

            if val_loss_history:
                initial_val = val_loss_history[0]
                final_val = val_loss_history[-1]
                val_improvement = ((initial_val - final_val) / initial_val) * 100 if initial_val > 0 else 0
                rows.append(["Initial Validation Loss", f"{initial_val:.4f}"])
                rows.append(["Final Validation Loss", f"{final_val:.4f}"])
                rows.append(["Validation Improvement", f"{val_improvement:.1f}%"])

            lines.append(self.md.table(headers, rows))

            # Convergence analysis
            lines.append("")
            lines.append(self.md.h4("Convergence Assessment"))

            # Check if loss plateaued
            if len(loss_history) >= 10:
                last_10_loss = loss_history[-10:]
                loss_change = abs(last_10_loss[-1] - last_10_loss[0]) / last_10_loss[0] * 100 if last_10_loss[0] > 0 else 0

                if loss_change < 1:
                    convergence = "Fully converged (< 1% change in last 10 epochs)"
                elif loss_change < 5:
                    convergence = "Near convergence (< 5% change)"
                else:
                    convergence = "Still improving (> 5% change)"

                lines.append(self.md.bullet(f"**Status**: {convergence}"))
                lines.append(self.md.bullet(f"**Last 10 epochs change**: {loss_change:.2f}%"))

        return "\n".join(lines) + "\n"

    def _model_comparison(self, data: Dict) -> str:
        """Generate model comparison across tasks."""
        if len(data) < 2:
            return ""

        lines = [self.md.h2("Cross-Task Comparison")]

        headers = ["Task", "Model Type", "Parameters", "Train Loss", "Val Loss", "Gap"]
        rows = []

        for task_name, dl_result in data.items():
            architecture = getattr(dl_result, 'architecture', {})
            params = architecture.get('params', 0)
            train_loss = getattr(dl_result, 'train_loss', 0)
            val_loss = getattr(dl_result, 'val_loss', 0)
            gap = val_loss - train_loss

            rows.append([
                task_name.replace('_', ' ').title(),
                getattr(dl_result, 'model_type', 'N/A'),
                f"{params:,}",
                f"{train_loss:.4f}",
                f"{val_loss:.4f}",
                f"{gap:.4f}"
            ])

        lines.append(self.md.table(headers, rows))

        return "\n".join(lines) + "\n"

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_from_registry(visual_type='deep_learning') or self._link_images("ml/deep_learning")
        if img_links:
            for link in img_links:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No deep learning visualizations available._")

        return "\n".join(lines) + "\n"

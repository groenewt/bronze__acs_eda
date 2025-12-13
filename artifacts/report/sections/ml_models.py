"""
Machine Learning Models Section - Clustering, regression, and time series analysis.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class MLModelsSection(BaseReportSection):
    """ML models section with comprehensive model reporting and metrics."""

    def get_filename(self) -> str:
        return "11_ml_models.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Machine Learning Models")]

        # Add section description
        content.append(self.md.blockquote(
            "Machine learning analysis including clustering, time series forecasting, "
            "and regression modeling with comprehensive performance metrics."
        ))
        content.append("")

        has_models = False

        # Handle multiple regression targets (keys ending with _regression)
        reg_keys = [k for k in data.keys() if k.endswith('_regression')]
        if reg_keys:
            has_models = True
            for key in reg_keys:
                if data[key]:
                    content.append(self._regression(data[key]))
        elif 'regression' in data and data['regression']:
            has_models = True
            content.append(self._regression(data['regression']))

        if 'clustering' in data and data['clustering']:
            has_models = True
            content.append(self._clustering(data['clustering']))

        # Handle multiple time series targets (keys ending with _timeseries)
        ts_keys = [k for k in data.keys() if k.endswith('_timeseries')]
        if ts_keys:
            has_models = True
            for key in ts_keys:
                if data[key]:
                    content.append(self._timeseries(data[key]))
        elif 'timeseries' in data and data['timeseries']:
            has_models = True
            content.append(self._timeseries(data['timeseries']))
        elif 'time_series' in data and data['time_series']:
            has_models = True
            content.append(self._timeseries(data['time_series']))

        content.append(self._model_comparison())

        if not has_models:
            content.append("_No ML models were trained for this dataset._")

        return "\n".join(filter(None, content))

    def _regression(self, reg: Dict) -> str:
        """Generate comprehensive regression section."""
        lines = [self.md.h2("Regression Models")]

        target = reg.get('target', 'N/A')
        lines.append(self.md.h3(f"Target Variable: {self.md.bold(target)}"))

        # Model performance metrics
        lines.append(self.md.h4("Model Performance"))

        best_model = reg.get('best_model', 'N/A')
        r2 = reg.get('test_score', reg.get('r2_score', 0))
        rmse = reg.get('rmse', None)
        mae = reg.get('mae', None)
        adj_r2 = reg.get('adjusted_r2', None)

        headers = ["Metric", "Value", "Interpretation"]
        rows = [
            ["Best Model", best_model, "—"],
            ["R² Score", f"{r2:.4f}", self._interpret_r2(r2)],
        ]

        if adj_r2 is not None:
            rows.append(["Adjusted R²", f"{adj_r2:.4f}", "Penalizes for added predictors"])
        if rmse is not None:
            rows.append(["RMSE", f"{rmse:,.2f}", "Root Mean Square Error"])
        if mae is not None:
            rows.append(["MAE", f"{mae:,.2f}", "Mean Absolute Error"])

        if reg.get('sample_weighted'):
            rows.append(["Sample Weights", "Applied", "ACS weights used"])

        lines.append(self.md.table(headers, rows))

        # Cross-validation scores
        cv_scores = reg.get('cv_scores', reg.get('cross_val_scores', None))
        if cv_scores:
            lines.append("")
            lines.append(self.md.h4("Cross-Validation"))
            if isinstance(cv_scores, list):
                avg_cv = sum(cv_scores) / len(cv_scores)
                std_cv = (sum((s - avg_cv) ** 2 for s in cv_scores) / len(cv_scores)) ** 0.5
                lines.append(self.md.metric("CV Mean Score", avg_cv, "", 4))
                lines.append(self.md.metric("CV Std Dev", std_cv, "", 4))
                lines.append(self.md.metric("Number of Folds", len(cv_scores)))

        # SHAP feature importance (preferred)
        shap_info = reg.get('shap', {})
        if shap_info and 'feature_importance' in shap_info:
            lines.append("")
            lines.append(self.md.h4("SHAP Feature Importance"))
            lines.append(self.md.blockquote(
                "SHAP (SHapley Additive exPlanations) values show the contribution of each "
                "feature to predictions. Higher absolute values indicate stronger influence."
            ))
            lines.append("")

            shap_imp = shap_info['feature_importance']
            sorted_imp = sorted(shap_imp.items(), key=lambda x: abs(x[1]), reverse=True)[:15]

            headers = ["Feature", "SHAP Value", "Impact"]
            rows = []
            for feat, imp in sorted_imp:
                impact = "Positive" if imp > 0 else "Negative"
                rows.append([feat, f"{imp:.4f}", impact])
            lines.append(self.md.table(headers, rows))

        # Fallback to regular feature importance
        elif reg.get('feature_importance'):
            lines.append("")
            lines.append(self.md.h4("Feature Importance"))

            feat_imp = reg['feature_importance']
            sorted_imp = sorted(feat_imp.items(), key=lambda x: abs(x[1]), reverse=True)[:15]

            headers = ["Feature", "Importance", "Rank"]
            rows = []
            for rank, (f, i) in enumerate(sorted_imp, 1):
                rows.append([f, f"{i:.4f}", str(rank)])
            lines.append(self.md.table(headers, rows))

        # Residual statistics
        residuals = reg.get('residuals', reg.get('residual_stats', {}))
        if residuals:
            lines.append("")
            lines.append(self.md.h4("Residual Analysis"))
            if isinstance(residuals, dict):
                lines.append(self.md.metric("Mean Residual", residuals.get('mean', 0), "", 4))
                lines.append(self.md.metric("Std Residual", residuals.get('std', 0), "", 4))

        # Visualizations
        lines.append("")
        lines.append(self.md.h4("Visualizations"))
        img_links = self._link_from_registry(visual_type='regression') or self._link_images("ml/regression")
        if img_links:
            lines.extend(img_links)
        else:
            lines.append("_No regression visualizations available._")

        return "\n".join(lines) + "\n"

    def _interpret_r2(self, r2: float) -> str:
        """Interpret R² score."""
        if r2 >= 0.9:
            return "Excellent fit"
        elif r2 >= 0.7:
            return "Good fit"
        elif r2 >= 0.5:
            return "Moderate fit"
        elif r2 >= 0.3:
            return "Weak fit"
        else:
            return "Poor fit"

    def _clustering(self, clust: Dict) -> str:
        """Generate comprehensive clustering section."""
        lines = [self.md.h2("Clustering Analysis")]

        # Basic clustering info
        method = clust.get('method', 'N/A')
        n_clusters = clust.get('n_clusters', 0)
        silhouette = clust.get('silhouette', 0)

        lines.append(self.md.h3("Clustering Configuration"))

        headers = ["Parameter", "Value", "Description"]
        rows = [
            ["Method", method.title(), "Clustering algorithm used"],
            ["Number of Clusters", str(n_clusters), "Optimal or specified K"],
            ["Silhouette Score", f"{silhouette:.4f}", self._interpret_silhouette(silhouette)],
        ]

        # Add additional metrics if available
        inertia = clust.get('inertia', clust.get('wcss', None))
        if inertia is not None:
            rows.append(["Inertia/WCSS", f"{inertia:,.2f}", "Within-cluster sum of squares"])

        calinski = clust.get('calinski_harabasz', clust.get('ch_score', None))
        if calinski is not None:
            rows.append(["Calinski-Harabasz", f"{calinski:.2f}", "Higher is better"])

        davies = clust.get('davies_bouldin', clust.get('db_score', None))
        if davies is not None:
            rows.append(["Davies-Bouldin", f"{davies:.4f}", "Lower is better"])

        lines.append(self.md.table(headers, rows))

        # Cluster sizes
        if 'cluster_sizes' in clust:
            lines.append("")
            lines.append(self.md.h3("Cluster Size Distribution"))

            sizes = clust['cluster_sizes']
            total = sum(sizes) if sizes else 1

            headers = ["Cluster", "Size", "Percentage", "Description"]
            rows = []
            for i, size in enumerate(sizes):
                pct = (size / total) * 100
                if pct > 40:
                    desc = "Dominant cluster"
                elif pct > 20:
                    desc = "Major cluster"
                elif pct > 10:
                    desc = "Moderate cluster"
                else:
                    desc = "Minor cluster"
                rows.append([f"Cluster {i}", f"{size:,}", f"{pct:.1f}%", desc])

            lines.append(self.md.table(headers, rows))

            # Add balance assessment
            lines.append("")
            cv = (sum((s - total/len(sizes))**2 for s in sizes) / len(sizes))**0.5 / (total/len(sizes)) * 100
            if cv < 20:
                balance = "well-balanced"
            elif cv < 50:
                balance = "moderately balanced"
            else:
                balance = "imbalanced"
            lines.append(self.md.interpretation(f"Cluster distribution is {balance} (CV: {cv:.1f}%)."))

        # Cluster profiles/centroids
        centroids = clust.get('centroids', clust.get('cluster_centers', None))
        if centroids and isinstance(centroids, dict):
            lines.append("")
            lines.append(self.md.h3("Cluster Profiles (Centroid Features)"))

            # Get feature names
            features = list(list(centroids.values())[0].keys()) if centroids else []
            if features:
                headers = ["Feature"] + [f"Cluster {i}" for i in range(len(centroids))]
                rows = []
                for feat in features[:10]:  # Limit to 10 features
                    row = [feat]
                    for cluster_id in sorted(centroids.keys()):
                        val = centroids[cluster_id].get(feat, 0)
                        row.append(f"{val:.2f}")
                    rows.append(row)
                lines.append(self.md.table(headers, rows))

        # Feature statistics by cluster
        cluster_stats = clust.get('cluster_stats', clust.get('feature_by_cluster', None))
        if cluster_stats and isinstance(cluster_stats, dict):
            lines.append("")
            lines.append(self.md.h3("Feature Means by Cluster"))

            for feat, stats in list(cluster_stats.items())[:5]:
                lines.append(f"**{feat}**:")
                if isinstance(stats, dict):
                    for cluster_id, val in stats.items():
                        lines.append(self.md.bullet(f"Cluster {cluster_id}: {val:.2f}"))
                lines.append("")

        # Visualizations
        lines.append("")
        lines.append(self.md.h3("Visualizations"))
        img_links = self._link_from_registry(visual_type='clustering') or self._link_images("ml/clustering")
        if img_links:
            lines.extend(img_links)
        else:
            lines.append("_No clustering visualizations available._")

        return "\n".join(lines) + "\n"

    def _interpret_silhouette(self, score: float) -> str:
        """Interpret silhouette score."""
        if score >= 0.7:
            return "Strong cluster structure"
        elif score >= 0.5:
            return "Reasonable structure"
        elif score >= 0.25:
            return "Weak structure"
        else:
            return "No substantial structure"

    def _timeseries(self, ts: Dict) -> str:
        """Generate comprehensive time series section."""
        lines = [self.md.h2("Time Series Forecasting")]

        target = ts.get('target', 'N/A')
        lines.append(self.md.h3(f"Target Variable: {self.md.bold(target)}"))

        # Best model summary
        best_model = ts.get('best_model', ts.get('method', 'N/A'))
        r2 = ts.get('r2_score', 0)
        periods = ts.get('forecast_periods', ts.get('periods', 0))

        lines.append(self.md.h4("Best Model Summary"))

        headers = ["Metric", "Value"]
        rows = [
            ["Best Model", best_model],
            ["R² Score", f"{r2:.4f}"],
            ["Forecast Periods", str(periods)],
        ]

        # Additional metrics if available
        mae = ts.get('mae', ts.get('mean_absolute_error', None))
        rmse = ts.get('rmse', ts.get('root_mean_square_error', None))
        mape = ts.get('mape', ts.get('mean_absolute_percentage_error', None))

        if mae is not None:
            rows.append(["MAE", f"{mae:.4f}"])
        if rmse is not None:
            rows.append(["RMSE", f"{rmse:.4f}"])
        if mape is not None:
            rows.append(["MAPE", f"{mape:.2f}%"])

        lines.append(self.md.table(headers, rows))

        # All models comparison
        all_models = ts.get('all_timeseries_models', ts.get('all_models', {}))
        if all_models:
            lines.append("")
            lines.append(self.md.h4("All Models Performance Comparison"))

            # Sort by R² descending
            sorted_models = sorted(
                all_models.items(),
                key=lambda x: x[1].get('r2_score', 0) if isinstance(x[1], dict) else 0,
                reverse=True
            )

            headers = ["Model", "R²", "MAE", "RMSE", "MAPE", "Rank"]
            rows = []
            for rank, (model_name, model_data) in enumerate(sorted_models, 1):
                if isinstance(model_data, dict):
                    r2_val = model_data.get('r2_score', 0)
                    mae_val = model_data.get('mae', model_data.get('mean_absolute_error', None))
                    rmse_val = model_data.get('rmse', model_data.get('root_mean_square_error', None))
                    mape_val = model_data.get('mape', model_data.get('mean_absolute_percentage_error', None))

                    mae_str = f"{mae_val:.2f}" if mae_val is not None else "—"
                    rmse_str = f"{rmse_val:.2f}" if rmse_val is not None else "—"
                    mape_str = f"{mape_val:.1f}%" if mape_val is not None else "—"

                    rows.append([model_name, f"{r2_val:.4f}", mae_str, rmse_str, mape_str, str(rank)])

            lines.append(self.md.table(headers, rows))

            # Model interpretation
            lines.append("")
            lines.append(self.md.interpretation(
                f"The {best_model} model achieved the best fit with R² = {r2:.4f}. "
                f"Models are ranked by R² score."
            ))

        # Model parameters if available
        params = ts.get('parameters', ts.get('model_params', None))
        if params and isinstance(params, dict):
            lines.append("")
            lines.append(self.md.h4("Model Parameters"))
            for param, val in params.items():
                lines.append(self.md.bullet(f"**{param}**: {val}"))

        # Forecasted values
        forecast_vals = ts.get('forecast_values', ts.get('forecast', []))
        if forecast_vals:
            lines.append("")
            lines.append(self.md.h4("Forecasted Values"))

            headers = ["Period", "Forecast", "Lower CI", "Upper CI"]
            rows = []

            # Check if we have confidence intervals
            lower_ci = ts.get('lower_ci', ts.get('confidence_lower', []))
            upper_ci = ts.get('upper_ci', ts.get('confidence_upper', []))

            for i, val in enumerate(forecast_vals, 1):
                lower = lower_ci[i-1] if i-1 < len(lower_ci) else None
                upper = upper_ci[i-1] if i-1 < len(upper_ci) else None

                lower_str = f"{lower:.2f}" if lower is not None else "—"
                upper_str = f"{upper:.2f}" if upper is not None else "—"

                rows.append([f"Period {i}", f"{val:.2f}", lower_str, upper_str])

            lines.append(self.md.table(headers, rows))

        # Trend analysis
        trend = ts.get('trend', ts.get('trend_direction', None))
        if trend:
            lines.append("")
            lines.append(self.md.h4("Trend Analysis"))
            lines.append(self.md.bullet(f"**Trend Direction**: {trend}"))

            slope = ts.get('slope', ts.get('trend_slope', None))
            if slope is not None:
                direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
                lines.append(self.md.bullet(f"**Slope**: {slope:.4f} ({direction})"))

        # Visualizations
        lines.append("")
        lines.append(self.md.h4("Visualizations"))
        img_links = self._link_from_registry(visual_type='time_series') or self._link_images("ml/time_series")
        if img_links:
            lines.extend(img_links)
        else:
            lines.append("_No time series visualizations available._")

        return "\n".join(lines) + "\n"

    def _model_comparison(self) -> str:
        """Generate model comparison section."""
        lines = [self.md.h2("Model Comparison")]

        img_links = self._link_images("ml/model_comparison")
        if img_links:
            for link in img_links:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No model comparison visualizations available._")

        return "\n".join(lines) + "\n"

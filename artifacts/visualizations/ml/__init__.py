"""ML Visualizations"""
from .base import BaseMLVisualizer
from .regression import RegressionVisualizer
from .clustering import ClusteringVisualizer
from .timeseries import TimeSeriesVisualizer
from .comparison import ModelComparisonVisualizer
from .shap import SHAPVisualizer

# Conditional import for QuantileRegressionVisualizer
try:
    from .quantile import QuantileRegressionVisualizer
    _has_quantile = True
except ImportError:
    _has_quantile = False


class MLVisualizer:
    def __init__(self, config, survey_type=""):
        self.regression = RegressionVisualizer(config, survey_type)
        self.clustering = ClusteringVisualizer(config, survey_type)
        self.timeseries = TimeSeriesVisualizer(config, survey_type)
        self.comparison = ModelComparisonVisualizer(config, survey_type)
        self.shap_viz = SHAPVisualizer(config, survey_type)
        if _has_quantile:
            self.quantile = QuantileRegressionVisualizer(config, survey_type)

    def viz_regression(self, result, X, y, target_name=None):
        return self.regression.viz_regression(result, X, y, target_name)

    def viz_clustering(self, result, X):
        return self.clustering.viz_clustering(result, X)

    def viz_timeseries(self, result, df, target_col):
        return self.timeseries.viz_timeseries(result, df, target_col)

    def viz_model_comparison(self, results, target_name=None):
        return self.comparison.viz_model_comparison(results, target_name)

    def viz_shap(self, shap_results, target_name=None):
        return self.shap_viz.viz_shap(shap_results, target_name)

    def viz_quantile_regression(self, X, y, feature_name, target_name):
        if _has_quantile:
            return self.quantile.viz_quantile_regression(X, y, feature_name, target_name)
        else:
            print("[WARNING] QuantileRegressionVisualizer not available")

    def viz_quantile_coefficients(self, X, y, feature_names, target_name):
        if _has_quantile:
            return self.quantile.viz_quantile_coefficients(X, y, feature_names, target_name)
        else:
            print("[WARNING] QuantileRegressionVisualizer not available")


__all__ = ['MLVisualizer', 'BaseMLVisualizer', 'RegressionVisualizer', 'ClusteringVisualizer', 'TimeSeriesVisualizer', 'ModelComparisonVisualizer', 'SHAPVisualizer']

# Conditionally add QuantileRegressionVisualizer to __all__
if _has_quantile:
    __all__.append('QuantileRegressionVisualizer')

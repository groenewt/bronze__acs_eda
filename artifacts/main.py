#!/usr/bin/env python3
import os
import warnings
# Suppress warnings BEFORE any sklearn/ML imports
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')
warnings.filterwarnings('ignore', message='.*sklearn.utils.parallel.delayed.*')
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn.utils.parallel')
warnings.filterwarnings('ignore', category=UserWarning, module='joblib')

import sys
import gc
import argparse
import pandas as pd
import traceback
from typing import List, Dict, Optional, Any
from datetime import datetime
from config import Config, FIPS_MAP
from processing import (FileLoader, TemporalAnalyzer,
                        HousingEconomicAnalyzer, PopulationEconomicAnalyzer,
                        CorrelationAnalyzer, StatisticalAnalyzer, OutlierAnalyzer,
                        AnomalyAnalyzer, TrendAnalyzer, CrossVariableAnalyzer,
                        RegionalComparisonAnalyzer, get_weight_column)
from visualizations import Visualizer
from visualizations.ml import MLVisualizer
from ml_models import (RegressionModeler, ClusteringModeler, TimeSeriesForecaster,
                       ModelComparator, ModelExplainer, SHAP_AVAILABLE)
from report import ReportGenerator
from feature_engineering import SmartDataCleaner, FeatureCreator
from ml import LLMAnalyzer, LLMClient
from visual_registry import get_registry
from logging_config import get_logger, get_log_context, log_success, log_complete
from memory_utils import (get_memory_monitor, clear_all_caches, memory_phase,
                          adaptive_sample, log_dataframe_memory)

# Module-level logger
logger = get_logger("main")

# Deep Learning imports (with fallback)
try:
    from deep_learning import (DeepLearningTrainer, TrainingConfig,
                               train_population_dl, train_housing_dl, DLResults)
    from dl_visualizer import DLVisualizer
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False
    logger.warning("Deep learning modules not available")


# ============================================================================
# CONFIGURATION & SETUP (All <= 10 lines)
# ============================================================================

def get_fips(state_name: str) -> str:
    name_map = {v.lower(): k for k, v in FIPS_MAP.items()}
    return name_map.get(state_name.lower().strip(), "20")


def create_config(state: str) -> Config:
    config = Config()
    config.set_state(get_fips(state))
    return config


def create_dirs(config: Config, survey: str):
    """Create output directories and initialize registry (≤10 lines)"""
    os.makedirs(config.output_dir, exist_ok=True)
    os.makedirs(config.figure_dir, exist_ok=True)
    ml_dir = os.path.join(config.figure_dir, 'ml')
    os.makedirs(ml_dir, exist_ok=True)
    # Initialize visual registry for this run
    registry = get_registry()
    registry.reset()
    registry.set_output_dir(config.output_dir)


# ============================================================================
# DATA LOADING & TRANSFORMATION (All <= 10 lines)
# ============================================================================

def load_data(state: str, survey: str, config: Config, scope: str):
    """Load data with era-specific schema applied per-file in loader."""
    loader = FileLoader(config)
    df = loader.load(survey, scope)
    return df, loader


def clean_economic_zeros(df: pd.DataFrame) -> tuple:
    """Clean economic zeros and return metadata."""
    econ_cols = ['Total_Person_Income', 'Wage_Income', 'Property_Value', 'Gross_Rent']
    existing = [c for c in econ_cols if c in df.columns]
    if existing:
        return SmartDataCleaner.handle_economic_zeros(df, existing, strategy='flag')
    return df.copy(), {'features': [], 'transform': ''}


# ============================================================================
# FEATURE ENGINEERING (All <= 10 lines)
# ============================================================================

def create_income_features(df: pd.DataFrame) -> tuple:
    """Create income features and return metadata."""
    if 'Total_Person_Income' in df.columns:
        return FeatureCreator.create_income_features(df)
    return df, {'features': [], 'transform': ''}


def create_housing_features(df: pd.DataFrame) -> tuple:
    """Create housing features and return metadata."""
    if 'Property_Value' in df.columns or 'Gross_Rent' in df.columns:
        return FeatureCreator.create_housing_features(df)
    return df, {'features': [], 'transform': ''}


def create_age_groups(df: pd.DataFrame) -> tuple:
    """Create age groups and return metadata."""
    if 'Age' in df.columns:
        return FeatureCreator.create_age_groups(df)
    return df, {'features': [], 'transform': ''}


def create_temporal_features(df: pd.DataFrame) -> tuple:
    """Create temporal features and return metadata."""
    if 'Census_Year' in df.columns:
        return FeatureCreator.create_temporal_features(df)
    return df, {'features': [], 'transform': ''}


def log_census_year(stage: str, df: pd.DataFrame):
    """Log Census_Year column status"""
    if 'Census_Year' in df.columns:
        valid = df['Census_Year'].notna().sum()
        unique = df['Census_Year'].nunique()
        logger.debug(f"CENSUS_YEAR_TRACK {stage}: {valid} valid, {unique} unique")
    else:
        logger.debug(f"CENSUS_YEAR_TRACK {stage}: Column not found")


def apply_features_pipeline(df: pd.DataFrame, survey_type: str = "") -> tuple:
    """Apply feature engineering pipeline using FeatureEngineer orchestrator."""
    from feature_engineering import FeatureEngineer
    engineer = FeatureEngineer(df, survey_type=survey_type)
    df, metadata = engineer.create_all_features()
    return df, {
        'features_created': metadata.get('created_features', []),
        'transformations': metadata.get('transforms_applied', [])
    }


def apply_feature_engineering(df: pd.DataFrame, survey_type: str = "") -> tuple:
    """Apply feature engineering with tracking."""
    rows_before = len(df)
    df, pipeline_results = apply_features_pipeline(df, survey_type)
    results = {
        'cleaning': {'rows_before': rows_before, 'rows_after': len(df)},
        'final_shape': df.shape,
        'features_created': pipeline_results.get('features_created', []),
        'transformations': pipeline_results.get('transformations', [])
    }
    return df, results


# ============================================================================
# ANALYSIS COMPONENTS (All <= 10 lines)
# ============================================================================

def run_temporal_analysis(df: pd.DataFrame) -> dict:
    try:
        return TemporalAnalyzer(df).analyze()
    except Exception as e:
        logger.warning(f" Temporal analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_economic_analysis(df: pd.DataFrame, survey: str) -> dict:
    try:
        if survey == 'housing':
            return {'housing': HousingEconomicAnalyzer(df).analyze()}
        elif survey == 'population':
            return {'population': PopulationEconomicAnalyzer(df).analyze()}
        return {}
    except Exception as e:
        logger.warning(f" Economic analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_correlation_analysis(df: pd.DataFrame, survey: str = None) -> dict:
    try:
        focus = ['Age', 'Total_Person_Income', 'Wage_Income',
                 'Property_Value', 'Gross_Rent', 'Hours_Worked_Per_Week']
        weight_col = get_weight_column(survey) if survey else None
        return CorrelationAnalyzer(df, weight_col=weight_col).analyze(focus)
    except Exception as e:
        logger.warning(f" Correlation analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_statistical_analysis(df: pd.DataFrame, survey: str = None) -> dict:
    try:
        weight_col = get_weight_column(survey) if survey else None
        return StatisticalAnalyzer(df, weight_col=weight_col).analyze(None)
    except Exception as e:
        logger.warning(f" Statistical analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_outlier_analysis(df: pd.DataFrame) -> dict:
    try:
        return OutlierAnalyzer(df).analyze(None)
    except Exception as e:
        logger.warning(f" Outlier analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_anomaly_analysis(df: pd.DataFrame) -> dict:
    try:
        return AnomalyAnalyzer(df).analyze(None)
    except Exception as e:
        logger.warning(f" Anomaly analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_trend_analysis(df: pd.DataFrame) -> dict:
    try:
        return TrendAnalyzer(df).analyze(None)
    except Exception as e:
        logger.warning(f" Trend analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_cross_variable_analysis(df: pd.DataFrame) -> dict:
    try:
        return CrossVariableAnalyzer(df).analyze(None)
    except Exception as e:
        logger.warning(f" Cross-variable analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_llm_analysis(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl=None, feat_eng=None):
    logger.debug("Initializing LLM client and analyzer...")
    client = LLMClient(config)
    analyzer = LLMAnalyzer(client)
    state = config.get_state_name()
    logger.debug(f" Running LLM analysis for state: {state}")
    return analyzer.run_analysis(df, temporal, state=state, economic=economic,
                                  correlations=corr, statistics=stats,
                                  outliers=outliers, anomalies=anom, trends=trends,
                                  deep_learning=dl, feature_engineering=feat_eng)


# ============================================================================
# VISUALIZATION (All <= 10 lines)
# ============================================================================

def create_visuals(df: pd.DataFrame, config: Config, survey: str):
    try:
        logger.info(f"[VISUALS] Creating comprehensive visualization suite for {survey.upper()}...")
        viz = Visualizer(df, config, survey_type=survey)
        viz.create_all()
        logger.info(f"SUCCESS: Visualizations saved to {config.figure_dir}")
    except Exception as e:
        logger.warning(f" Visualization creation failed: {e}")


# ============================================================================
# ML MODELS (All <= 10 lines each)
# ============================================================================

def is_income_column(col_name: str) -> bool:
    """Check if column name contains income-related terms"""
    income_terms = ['income', 'wage', 'earnings', 'salary', 'pay']
    col_lower = col_name.lower()
    return any(term in col_lower for term in income_terms)


def get_ml_features(df: pd.DataFrame, limit: int = 10) -> list:
    numeric = df.select_dtypes(include=['number']).columns.tolist()
    exclude = ['Census_Year', 'State_Code', 'State_FIPS', 'Public_Use_Microdata_Area',
               'Person_Number', 'Income_Adjustment_Factor', 'Person_Weight']
    return [c for c in numeric if c not in exclude][:limit]


def get_target_col(df: pd.DataFrame, survey: str) -> str:
    """Get first available target column (for backward compatibility)"""
    targets = {'population': ['Total_Person_Income', 'Age'],
               'housing': ['Property_Value', 'Gross_Rent']}
    for t in targets.get(survey, []):
        if t in df.columns:
            return t
    return None


def get_all_target_cols(df: pd.DataFrame, survey: str) -> list:
    """Get all available target columns for supervised learning"""
    targets = {'population': ['Total_Person_Income', 'Wage_Income', 'Total_Person_Earnings',
                             'Age', 'Hours_Worked_Per_Week'],
               'housing': ['Property_Value', 'Gross_Rent', 'Monthly_Mortgage_Payment',
                          'Monthly_Rent_Payment', 'Property_Tax_Annual']}
    available = [t for t in targets.get(survey, []) if t in df.columns]
    return available


def prepare_regression_data(df, target, features, min_samples):
    existing_features = [f for f in features if f in df.columns]
    if not existing_features or target not in df.columns:
        return None, None
    X, y = df[existing_features].dropna(), df[target].dropna()
    idx = X.index.intersection(y.index)
    initial_count = len(idx)

    # Filter zeros for income-related target OR housing cost targets
    # Housing targets have many zeros (non-renters, vacant units) that would contaminate models
    housing_targets = ['Gross_Rent', 'Property_Value', 'Monthly_Mortgage_Payment',
                       'Monthly_Rent_Payment', 'Property_Tax_Annual']
    should_filter_zeros = is_income_column(target) or target in housing_targets
    if should_filter_zeros:
        y = y[y > 0]
        idx = idx.intersection(y.index)
        logger.debug(f"[REGRESSION] {target}: After zero-filter on target: {len(idx)} samples (was {initial_count})")

    # Filter zeros for income-related features
    for feat in existing_features:
        if is_income_column(feat):
            before = len(idx)
            X_feat = X[feat]
            valid_idx = X_feat[X_feat > 0].index
            idx = idx.intersection(valid_idx)
            logger.debug(f"[REGRESSION] {target}: After zero-filter on {feat}: {len(idx)} samples (was {before})")

    if len(idx) < min_samples:
        logger.warning(f"[REGRESSION] {target}: Insufficient samples after filtering: {len(idx)} < {min_samples}")
        return None, None
    return X.loc[idx], y.loc[idx]


def build_regression_result(target, X, y, best_name, best_result, models, shap_results=None, sample_weighted=False):
    """Build regression result dictionary with all fields for report.py"""
    result = {
        'target': target,
        'features': list(X.columns),
        'best_model': best_name,
        'best_r2_score': best_result.test_score,
        'test_score': best_result.test_score,  # Alias for report.py
        'rmse': best_result.metadata.get('rmse') if best_result.metadata else None,
        'mae': best_result.metadata.get('mae') if best_result.metadata else None,
        'feature_importance': best_result.feature_importance,
        'sample_weighted': sample_weighted,
        'sample_size': len(X),
        'result_obj': best_result,
        'all_models': models,
        'all_model_objects': models,
        'X': X, 'y': y
    }
    if shap_results:
        result['shap'] = shap_results
    return result


def generate_shap_explanation(best_result, X, y, best_name):
    """Generate SHAP explanation for best model"""
    if not SHAP_AVAILABLE:
        return None
    try:
        explainer = ModelExplainer()
        # Split data same way as training
        from sklearn.model_selection import train_test_split
        X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        # Get the fitted model from result
        model = best_result.metadata.get('model') if hasattr(best_result, 'metadata') else None
        if model is None and hasattr(best_result, 'result_obj'):
            model = best_result
        # Use the modeler's model directly
        modeler = RegressionModeler()
        modeler.model = modeler.models.get(best_name)
        modeler.model.fit(X_train, y.loc[X_train.index])
        shap_result = explainer.explain_model(modeler.model, X_train, X_test, best_name)
        if 'error' not in shap_result:
            logger.info(f"[SHAP] Generated explanation for {best_name}")
            return shap_result
    except Exception as e:
        logger.warning(f"[SHAP] Failed to generate explanation: {e}")
    return None


def train_regression_model(df, target, features, min_samples=100, tune=False, survey=None):
    """
    Train regression models with optional hyperparameter tuning and SHAP.

    Args:
        df: Input DataFrame
        target: Target column name
        features: List of feature column names
        min_samples: Minimum samples required
        tune: If True, run hyperparameter tuning (slower but better results)
        survey: Survey type ('population' or 'housing') for sample weights
    """
    try:
        X, y = prepare_regression_data(df, target, features, min_samples)
        if X is None:
            return None

        # Get sample weights if survey specified
        sample_weight = None
        weight_col = get_weight_column(survey) if survey else None
        if weight_col and weight_col in df.columns:
            sample_weight = df.loc[X.index, weight_col]
            logger.debug(f"[ML] Using sample weights from '{weight_col}'")

        models = ModelComparator.compare_regression_models(X, y, tune=tune, sample_weight=sample_weight)
        best_name, best_result = ModelComparator.select_best_model(models)

        # Check if all models failed
        if best_result is None:
            logger.warning(f"All regression models failed for target: {target}")
            return None

        # Generate SHAP explanation for best model
        shap_results = None
        if SHAP_AVAILABLE and best_name in {'random_forest', 'gradient_boosting'}:
            shap_results = generate_shap_explanation(best_result, X, y, best_name)

        sample_weighted = sample_weight is not None and len(sample_weight) > 0
        return build_regression_result(target, X, y, best_name, best_result, models, shap_results, sample_weighted)
    except Exception as e:
        logger.warning(f" Regression model training failed for {target}: {str(e)}")
        return None


def prepare_clustering_data(df, features, min_samples):
    existing = [f for f in features if f in df.columns]
    if len(existing) < 2:
        return None
    X = df[existing].dropna()
    if len(X) < min_samples:
        return None
    return X


def build_clustering_result(X, best_result, all_results, best_name='kmeans'):
    """Build clustering result dictionary with all fields for report.py"""
    # Convert cluster_sizes dict to list if needed
    cluster_sizes_dict = best_result.cluster_sizes if hasattr(best_result, 'cluster_sizes') else {}
    cluster_sizes_list = list(cluster_sizes_dict.values()) if isinstance(cluster_sizes_dict, dict) else cluster_sizes_dict

    return {
        'features': list(X.columns),
        'method': best_name.title(),  # e.g., 'Kmeans' -> 'KMeans'
        'n_clusters': best_result.n_clusters if hasattr(best_result, 'n_clusters') else 5,
        'silhouette_score': best_result.silhouette_score,
        'silhouette': best_result.silhouette_score,  # Alias for report.py
        'cluster_sizes': cluster_sizes_list,
        'sample_size': len(X),
        'result_obj': best_result,
        'all_clustering_models': all_results
    }


def train_all_clustering_algorithms(clusterer, X):
    """Train all clustering algorithms with smart memory handling"""
    all_results = {}

    # KMeans - O(nkd) memory, safe for large datasets
    try:
        logger.info(f"[CLUSTERING] KMeans on {len(X):,} samples...")
        flush_logs()
        all_results['kmeans'] = clusterer.kmeans_clustering(X, n_clusters=5)
        logger.info("[CLUSTERING] KMeans complete.")
    except Exception as e:
        logger.warning(f"[CLUSTERING] KMeans failed: {e}")
        all_results['kmeans'] = {'error': str(e)}

    # Hierarchical - O(n²) memory, uses internal sampling for safety
    try:
        logger.info(f"[CLUSTERING] Hierarchical on {len(X):,} samples (will sample if needed)...")
        flush_logs()
        all_results['hierarchical'] = clusterer.hierarchical_clustering(X, n_clusters=5)
        logger.info("[CLUSTERING] Hierarchical complete.")
    except Exception as e:
        logger.warning(f"[CLUSTERING] Hierarchical failed: {e}")
        all_results['hierarchical'] = {'error': str(e)}

    return all_results


def select_best_clustering_model(all_results):
    """Select best clustering model based on silhouette score"""
    best_name, best_result, best_score = None, None, -1
    for name, result in all_results.items():
        if hasattr(result, 'silhouette_score') and result.silhouette_score > best_score:
            best_score, best_name, best_result = result.silhouette_score, name, result
    return best_name, best_result


def train_clustering_model(df, features, min_samples=100):
    """Train multiple clustering models"""
    try:
        X = prepare_clustering_data(df, features, min_samples)
        if X is None:
            return None
        all_results = train_all_clustering_algorithms(ClusteringModeler(), X)
        best_name, best_result = select_best_clustering_model(all_results)
        return build_clustering_result(X, best_result, all_results, best_name) if best_result else None
    except Exception as e:
        logger.warning(f" Clustering model training failed: {str(e)}")
        return None


def prepare_timeseries_data(df, target, min_samples):
    if 'Census_Year' not in df.columns or target not in df.columns:
        return None
    df_ts = df[['Census_Year', target]].dropna()
    df_ts = df_ts[df_ts[target] > 0]
    if len(df_ts) < min_samples:
        return None
    return df_ts


def build_timeseries_result(target, forecast):
    """Build timeseries result dictionary with all models"""
    # Get forecasts from best model
    forecasts = forecast.get('forecasts', {})
    # Convert dict {year: value} to list of values
    forecast_values = list(forecasts.values()) if isinstance(forecasts, dict) else forecasts
    all_ts_models = forecast.get('all_models', {})

    # DEBUG: Print forecast structure
    logger.debug(f"[DEBUG-TS] Target: {target}, Forecasts: {forecasts}, Values: {forecast_values}")

    return {'target': target, 'forecast_periods': 3,
            'forecast_values': forecast_values,
            'forecasts': forecasts,  # Keep original dict for reference
            'all_timeseries_models': all_ts_models,
            'best_model': forecast.get('best_model', 'unknown'),
            'r2_score': forecast.get('r2_score', 0)}


def run_forecaster(df_ts, target):
    """Run time series forecasting"""
    forecaster = TimeSeriesForecaster()
    return forecaster.forecast_trend(df_ts, target, 'Census_Year', periods_ahead=3)


def train_timeseries_model(df, target, min_samples=50):
    try:
        df_ts = prepare_timeseries_data(df, target, min_samples)
        if df_ts is None:
            return None
        forecast = run_forecaster(df_ts, target)
        return build_timeseries_result(target, forecast) if forecast else None
    except Exception as e:
        logger.warning(f" Time series forecasting failed for {target}: {str(e)}")
        return None


def extract_regression_viz_data(ml_results, df, key):
    """Extract data needed for regression visualization"""
    result_obj = ml_results[key].get('result_obj')
    target = ml_results[key]['target']
    features = ml_results[key]['features']
    X, y = df[features].dropna(), df[target].dropna()
    idx = X.index.intersection(y.index)
    return result_obj, X.loc[idx], y.loc[idx], target


def prepare_regression_viz_data(ml_results, df, key):
    """Prepare data for regression visualization"""
    target = ml_results[key]['target']
    features = ml_results[key]['features']
    X, y = df[features].dropna(), df[target].dropna()
    idx = X.index.intersection(y.index)
    return X.loc[idx], y.loc[idx], target


def viz_each_regression_model(ml_viz, all_models, X, y, target):
    """Visualize each regression model"""
    for model_name, result_obj in all_models.items():
        if isinstance(result_obj, dict) and 'error' in result_obj:
            continue
        try:
            ml_viz.viz_regression(result_obj, X, y, target_name=target)
        except Exception as e:
            logger.warning(f" Viz failed for {model_name}: {str(e)}")


def viz_regression_results(ml_viz, ml_results, df, key):
    """Visualize all regression models including SHAP explanations"""
    try:
        if key not in ml_results or not ml_results[key]:
            return
        X, y, target = prepare_regression_viz_data(ml_results, df, key)
        all_models = ml_results[key].get('all_model_objects', {})
        viz_each_regression_model(ml_viz, all_models, X, y, target)

        # Visualize SHAP if available
        shap_results = ml_results[key].get('shap')
        if shap_results and 'error' not in shap_results:
            logger.info(f"[SHAP-VIZ] Creating SHAP visualizations for {target}")
            ml_viz.viz_shap(shap_results, target_name=target)
    except Exception as e:
        logger.warning(f" Regression visualization failed for {key}: {str(e)}")


def viz_each_clustering_model(ml_viz, all_models, X):
    """Visualize each clustering model"""
    for model_name, result_obj in all_models.items():
        if isinstance(result_obj, dict) and 'error' in result_obj:
            continue
        try:
            ml_viz.viz_clustering(result_obj, X)
        except Exception as e:
            logger.warning(f" Clustering viz failed for {model_name}: {str(e)}")


def viz_clustering_results(ml_viz, ml_results, df):
    """Visualize all clustering models"""
    try:
        if 'clustering' not in ml_results or not ml_results['clustering']:
            return
        features = ml_results['clustering']['features']
        X = df[features].dropna()
        all_models = ml_results['clustering'].get('all_clustering_models', {})
        viz_each_clustering_model(ml_viz, all_models, X)
    except Exception as e:
        logger.warning(f" Clustering visualization failed: {str(e)}")


def prepare_ts_model_result(target, model_name, model_data):
    """Create result dict for a specific time series model"""
    # Extract forecasts and convert to list of values
    forecasts = model_data.get('forecasts', {})
    forecast_values = list(forecasts.values()) if isinstance(forecasts, dict) else forecasts

    # Extract CI data
    ci_lower = model_data.get('ci_lower', [])
    ci_upper = model_data.get('ci_upper', [])

    logger.debug(f"[DEBUG-TS-MODEL] {model_name}: forecasts={forecasts}, values={forecast_values}, CI_lower={ci_lower}, CI_upper={ci_upper}")

    return {
        'target': target,
        'forecasts': forecasts,
        'forecast_values': forecast_values,  # Add as list for easy plotting
        'ci_lower': ci_lower,  # Confidence interval lower bounds
        'ci_upper': ci_upper,  # Confidence interval upper bounds
        'r2_score': model_data.get('r2_score', 0),
        'model_name': model_name
    }


def viz_each_timeseries_model(ml_viz, all_models, df_ts, target):
    """Visualize each time series model"""
    for model_name, model_data in all_models.items():
        try:
            model_result = prepare_ts_model_result(target, model_name, model_data)
            ml_viz.viz_timeseries(model_result, df_ts, target)
        except Exception as e:
            logger.warning(f" Time series viz failed for {model_name}: {str(e)}")


def viz_timeseries_results(ml_viz, ml_results, df):
    """Visualize all time series models for ALL targets"""
    try:
        # Find all timeseries keys (ending with _timeseries)
        ts_keys = [k for k in ml_results.keys() if k.endswith('_timeseries')]
        logger.debug(f"[VIZ-TIMESERIES] Found {len(ts_keys)} time series results: {ts_keys}")

        for ts_key in ts_keys:
            ts_result = ml_results[ts_key]
            target = ts_result.get('target')
            if not target or 'Census_Year' not in df.columns or target not in df.columns:
                logger.debug(f"[VIZ-TIMESERIES] Skipping {ts_key}: missing target or Census_Year")
                continue

            logger.debug(f"[VIZ-TIMESERIES] Visualizing time series for target: {target}")
            df_ts = df[['Census_Year', target]].dropna()
            viz_each_timeseries_model(ml_viz, ts_result.get('all_timeseries_models', {}), df_ts, target)
    except Exception as e:
        logger.warning(f" Time series visualization failed: {str(e)}")


def viz_model_comparison_results(ml_viz, ml_results, key):
    try:
        if key in ml_results and ml_results[key]:
            all_models = ml_results[key].get('all_models')
            target = ml_results[key].get('target')
            if all_models and target:
                ml_viz.viz_model_comparison(all_models, target_name=target)
    except Exception as e:
        logger.warning(f" Model comparison visualization failed for {key}: {str(e)}")


def create_ml_visualizations(ml_results, df, config, survey):
    """Create visualizations for all ML models, iterating over all targets"""
    ml_viz = MLVisualizer(config, survey)

    # Visualize all regression results (each target gets its own subdirectory)
    for key in ml_results.keys():
        if key.endswith('_regression'):
            viz_regression_results(ml_viz, ml_results, df, key)
            viz_model_comparison_results(ml_viz, ml_results, key)

    # Visualize clustering (unsupervised, no target subdirectory)
    viz_clustering_results(ml_viz, ml_results, df)

    # Visualize time series
    viz_timeseries_results(ml_viz, ml_results, df)


def train_regression_for_survey(df, survey, features, tune=False):
    """Train regression models for all available target columns with sample weights"""
    targets = get_all_target_cols(df, survey)
    if not targets:
        return None
    results = {}
    for target in targets:
        logger.info(f"[ML] Training regression models for target: {target}")
        reg = train_regression_model(df, target, features, tune=tune, survey=survey)
        if reg:
            # Use target name as key for clarity
            key = f'{target}_regression'
            results[key] = reg
    return results if results else None


def flush_logs():
    """Force flush all log handlers to ensure logs are written before potential crash"""
    sys.stdout.flush()
    sys.stderr.flush()
    for handler in logger.handlers:
        handler.flush()


def add_clustering_to_results(results, df, features):
    """Train clustering models with explicit error handling and logging"""
    try:
        logger.info("[CLUSTERING] Starting clustering model training...")
        flush_logs()
        cluster = train_clustering_model(df, features)
        if cluster:
            results['clustering'] = cluster
            logger.info("[CLUSTERING] Clustering complete.")
        else:
            logger.info("[CLUSTERING] No clustering results returned (likely insufficient data).")
    except Exception as e:
        logger.error(f"[CLUSTERING] Failed with exception: {e}")
        logger.error(traceback.format_exc())
        flush_logs()


def add_timeseries_to_results(results, df, survey):
    """Train time series models for ALL available target columns"""
    targets = get_all_target_cols(df, survey)
    logger.info(f"[ML-TIMESERIES] Training time series for {len(targets)} targets: {targets}")
    ts_results = {}
    for target in targets:
        logger.info(f"[ML-TIMESERIES] Training time series for target: {target}")
        ts = train_timeseries_model(df, target)
        if ts:
            # Store each target's time series separately
            ts_results[f'{target}_timeseries'] = ts
    if ts_results:
        results.update(ts_results)


def train_all_ml_models(df, survey, features, tune=False):
    """Train all ML models with diagnostic logging"""
    results = {}

    # Memory check before ML training
    monitor = get_memory_monitor()
    monitor.log_memory("[ML-START]", force=True)

    logger.info("[ML] Starting regression training...")
    flush_logs()
    reg_results = train_regression_for_survey(df, survey, features, tune=tune)
    if reg_results:
        results.update(reg_results)
    logger.info(f"[ML] Regression complete. {len(results)} models trained.")

    # Memory and log flush before clustering (potential crash point)
    monitor.log_memory("[PRE-CLUSTERING]", force=True)
    flush_logs()
    add_clustering_to_results(results, df, features)

    logger.info("[ML] Starting time series training...")
    flush_logs()
    add_timeseries_to_results(results, df, survey)

    logger.info(f"[ML] All ML models complete. Total: {len(results)} result keys.")
    return results


def run_ml_pipeline(df: pd.DataFrame, config: Config, survey: str, tune: bool = False):
    try:
        logger.info(f"[ML] Running ML pipeline for {survey.upper()}...")
        if tune:
            logger.info("[ML] Hyperparameter tuning ENABLED (this may take longer)")
        features = get_ml_features(df)
        results = train_all_ml_models(df, survey, features, tune=tune)
        if results:
            create_ml_visualizations(results, df, config, survey)
        return results
    except Exception as e:
        logger.warning(f" ML pipeline failed: {e}")
        return {}


# ============================================================================
# DEEP LEARNING PIPELINE (All <= 10 lines)
# ============================================================================

def get_dl_task_names(survey: str) -> List[str]:
    """Get deep learning task names for survey (≤10 lines)"""
    if survey == 'population':
        return ['income_prediction', 'employment_analysis', 'demographic_profile']
    elif survey == 'housing':
        return ['property_valuation', 'affordability_analysis', 'housing_quality',
                'cost_prediction', 'occupancy_prediction']
    return []


def train_dl_task(df: pd.DataFrame, survey: str, task_name: str,
                 features: List[str], config: TrainingConfig):
    """Train single deep learning task (≤10 lines)"""
    try:
        import gc
        logger.info(f"[DL] Training {task_name}...")
        trainer = DeepLearningTrainer()
        result = trainer.train_model(df, survey, task_name, features, config)
        logger.info(f"[DL] ✓ {task_name} complete: {result.task_type}, "
              f"Test metrics: {result.test_metrics}")
        gc.collect()  # Free memory after each task
        return result
    except Exception as e:
        logger.warning(f" DL task {task_name} failed: {e}")
        return None


def train_all_dl_tasks(df: pd.DataFrame, survey: str,
                       features: List[str]) -> Dict[str, DLResults]:
    """Train all deep learning tasks (≤10 lines)"""
    # CPU-only: i9-12900K (24 cores via threading, not multiprocessing)
    config = TrainingConfig(epochs=75, batch_size=256, verbose=1,
                           use_multiprocessing=False, workers=1)
    results = {}
    for task_name in get_dl_task_names(survey):
        result = train_dl_task(df, survey, task_name, features, config)
        if result:
            results[task_name] = result
    return results


def create_dl_visualizations(results: Dict[str, DLResults], df: pd.DataFrame,
                             config: Config, survey: str):
    """Create deep learning visualizations (≤10 lines)"""
    try:
        logger.info(f"[DL-VIZ] Creating visualizations for {len(results)} tasks...")
        viz = DLVisualizer(config, survey)
        # Each task uses its own test data (stored in DLResults)
        viz.visualize_all(results)
        viz.plot_comprehensive_dashboard(results)
        logger.info(f"[DL-VIZ] All visualizations saved to {viz.fig_dir}")
    except Exception as e:
        logger.warning(f" DL visualization failed: {e}")


def run_dl_pipeline(df: pd.DataFrame, config: Config, survey: str) -> Dict[str, DLResults]:
    """Run complete deep learning pipeline (≤10 lines)"""
    if not DL_AVAILABLE:
        logger.info(" Deep learning not available, skipping DL pipeline")
        return {}
    try:
        logger.info(f"[DL] Running deep learning pipeline for {survey.upper()}...")
        features = get_ml_features(df)
        results = train_all_dl_tasks(df, survey, features)
        if results:
            create_dl_visualizations(results, df, config, survey)
        return results
    except Exception as e:
        logger.warning(f" DL pipeline failed: {e}")
        return {}


# ============================================================================
# REPORT GENERATION (All <= 10 lines)
# ============================================================================

def create_report_name(config, survey):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    state_name = config.get_state_name().replace(' ', '_')
    return f"report_{state_name}_{survey}_{timestamp}.txt"


def rename_latest_report(config, report_name):
    old_files = sorted([f for f in os.listdir(config.output_dir) if f.startswith('report_')])
    if old_files:
        latest = os.path.join(config.output_dir, old_files[-1])
        new_path = os.path.join(config.output_dir, report_name)
        if os.path.exists(latest) and not os.path.exists(new_path):
            os.rename(latest, new_path)


def generate_report(config, loader, temporal, economic, corr, stats,
                   outliers, anom, trends, llm, feat_eng, ml, survey, state, cross_var=None, dl=None):
    report_name = create_report_name(config, survey)
    gen = ReportGenerator(config)
    gen.generate(loader.stats, temporal, llm, economic, corr, stats,
                 outliers, anom, trends, feat_eng, ml, cross_var, dl)
    rename_latest_report(config, report_name)
    logger.info(f"[REPORT] Generated: {report_name}")


# ============================================================================
# MAIN ORCHESTRATOR (All <= 10 lines)
# ============================================================================

def load_and_prepare_data(state, survey, config, scope):
    df, loader = load_data(state, survey, config, scope)
    if df.empty:
        return None, None, None
    # Schema already applied per-file in loader
    logger.info(f"Loaded {len(df):,} records")
    log_census_year("After schema application", df)
    df, feat_eng = apply_feature_engineering(df, survey)
    logger.debug(f"Feature engineering complete: {feat_eng['final_shape']}")
    gc.collect()  # Clear loading intermediates
    return df, loader, feat_eng


def run_all_analyses(df, survey):
    logger.debug("Running comprehensive analysis suite...")
    logger.debug(f"Using sample weights from '{get_weight_column(survey)}' column")
    temporal = run_temporal_analysis(df)
    gc.collect()
    economic = run_economic_analysis(df, survey)
    gc.collect()
    corr = run_correlation_analysis(df, survey)  # Pass survey for weighted correlations
    gc.collect()
    stats = run_statistical_analysis(df, survey)  # Pass survey for weighted statistics
    outliers = run_outlier_analysis(df)
    anom = run_anomaly_analysis(df)
    trends = run_trend_analysis(df)
    cross_var = run_cross_variable_analysis(df)
    gc.collect()
    return temporal, economic, corr, stats, outliers, anom, trends, cross_var


def run_llm_with_fallback(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl=None, feat_eng=None):
    try:
        logger.debug("Starting LLM analysis with fallback handler...")
        result = run_llm_analysis(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl, feat_eng)
        logger.debug("LLM analysis completed successfully")
        return result
    except Exception as e:
        logger.warning(f"LLM analysis skipped: {e}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")
        return {'interpretation': 'LLM analysis not available',
                'analysis': 'Please ensure LM Studio is running on localhost:1234',
                'suggestions': 'N/A', 'policy_recommendations': 'N/A'}


def run_visualizations_and_ml(df, config, survey, tune=False):
    create_visuals(df, config, survey)
    gc.collect()  # Clear visualization memory

    # HOUSING: Adaptive sampling before ML/DL to prevent memory explosion
    if survey.lower() == 'housing':
        df_ml = adaptive_sample(df, survey_type='housing')
    else:
        df_ml = adaptive_sample(df, survey_type='population')

    ml = run_ml_pipeline(df_ml, config, survey, tune=tune)
    gc.collect()  # Clear ML intermediates
    dl = run_dl_pipeline(df_ml, config, survey)
    gc.collect()  # Clear DL model objects
    return {'ml': ml, 'dl': dl}


def generate_full_report(config, loader, df, survey, state, temporal, economic,
                        corr, stats, outliers, anom, trends, ml_dl_results, feat_eng, cross_var):
    # Extract ML and DL results from combined structure
    ml_results = ml_dl_results.get('ml', {}) if isinstance(ml_dl_results, dict) else ml_dl_results
    dl_results = ml_dl_results.get('dl', {}) if isinstance(ml_dl_results, dict) else {}
    llm = run_llm_with_fallback(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl_results, feat_eng)
    generate_report(config, loader, temporal, economic, corr, stats,
                   outliers, anom, trends, llm, feat_eng, ml_results, survey, state, cross_var, dl_results)


def run_analysis_and_reporting(df, loader, feat_eng, config, survey, state, tune=False):
    temporal, economic, corr, stats, outliers, anom, trends, cross_var = run_all_analyses(df, survey)
    ml = run_visualizations_and_ml(df, config, survey, tune=tune)
    generate_full_report(config, loader, df, survey, state, temporal, economic,
                        corr, stats, outliers, anom, trends, ml, feat_eng, cross_var)


def process_survey(state: str, survey: str, config: Config, scope: str, tune: bool = False):
    logger.info(f"{'='*70}")
    logger.info(f"[{survey.upper()}] Processing {state} ({scope})...")
    logger.info(f"{'='*70}")

    with memory_phase(f"process_{state}_{survey}_{scope}"):
        config.set_survey(survey, scope)
        df, loader, feat_eng = load_and_prepare_data(state, survey, config, scope)
        if df is None:
            logger.warning(f"No data for {state} - {survey} ({scope})")
            return None
        run_analysis_and_reporting(df, loader, feat_eng, config, survey, state, tune=tune)
        log_success(f"{survey.upper()} ({scope}) pipeline complete for {state}!")
        return df


def process_state_surveys(state, surveys, scopes, tune=False):
    state = state.strip()
    config = create_config(state)
    log_ctx = get_log_context(config.log_base_dir)

    for survey in surveys:
        survey = survey.strip().lower()
        for scope in scopes:
            scope = scope.strip()
            config.set_survey(survey, scope)
            create_dirs(config, survey)

            # Set logging context for this state/survey/scope
            log_ctx.set_context(state=config.get_state_name(), survey=survey, scope=scope)

            process_survey(state, survey, config, scope, tune=tune)

            # Clear caches between surveys
            clear_all_caches()
            gc.collect()


def setup_parser(parser):
    """Configure argument parser with all CLI options"""
    parser.add_argument('--all-states', action='store_true',
                       help='Run analysis for all states')
    parser.add_argument('--all-scopes', action='store_true',
                       help='Run analysis for all scopes (1-Year and 5-Year)')
    parser.add_argument('--states', type=str,
                       help='Comma-separated list of states (Ex. Kansas, Missouri, South Carolina')
    parser.add_argument('--surveys', type=str,
                       help='Comma-separated list of surveys (Housing, Population)')
    parser.add_argument('--scopes', type=str,
                       help='Comma-separated list of scopes (1-Year, 5-Year)')
    parser.add_argument('--tune', action='store_true',
                       help='Enable hyperparameter tuning for ML models (slower but better results)')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Census Data Analysis Pipeline')
    setup_parser(parser)
    return parser.parse_args()


def get_states_list(args):
    if args.all_states:
        all_states = list(FIPS_MAP.values())
        logger.info(f" Running for ALL {len(all_states)} states/territories")
        return all_states
    elif args.states:
        return args.states.split(',')
    else:
        return os.getenv('CENSUS_STATES', 'Kansas').split(',')


def get_scopes_list(args):
    if args.all_scopes:
        all_scopes = ['1-Year', '5-Year']
        logger.info(f" Running for ALL scopes: {all_scopes}")
        return all_scopes
    elif args.scopes:
        return args.scopes.split(',')
    else:
        return os.getenv('CENSUS_SCOPES', '1-Year').split(',')


def main():
    args = parse_arguments()
    states = get_states_list(args)
    surveys = args.surveys.split(',') if args.surveys else os.getenv('CENSUS_SURVEYS', 'population,housing').split(',')
    scopes = get_scopes_list(args)

    # Initialize logging with console output
    log_ctx = get_log_context()
    log_ctx.enable_console(True)

    # Initialize memory monitor
    monitor = get_memory_monitor()
    monitor.log_memory("STARTUP", force=True)

    logger.info(f"CONFIG: States: {len(states)}, Surveys: {surveys}, Scopes: {scopes}")
    if args.tune:
        logger.info("CONFIG: Hyperparameter tuning ENABLED")

    try:
        for state in states:
            process_state_surveys(state, surveys, scopes, tune=args.tune)
            # Clear caches between states
            clear_all_caches()
            gc.collect()
        log_complete("All processing finished!")
        monitor.log_memory("SHUTDOWN", force=True)
    finally:
        # Cleanup logging handlers
        log_ctx.close()


if __name__ == '__main__':
    main()

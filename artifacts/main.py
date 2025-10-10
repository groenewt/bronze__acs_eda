#!/usr/bin/env python3
import os
import sys
import argparse
import pandas as pd
import traceback
from typing import List, Dict, Optional, Any
from datetime import datetime
from config import Config, FIPS_MAP
from processing import (FileLoader, SchemaFactory, SchemaApplier, TemporalAnalyzer,
                        HousingEconomicAnalyzer, PopulationEconomicAnalyzer,
                        CorrelationAnalyzer, StatisticalAnalyzer, OutlierAnalyzer,
                        AnomalyAnalyzer, TrendAnalyzer, CrossVariableAnalyzer,
                        RegionalComparisonAnalyzer)
from visualizer import Visualizer, MLVisualizer
from ml_models import RegressionModeler, ClusteringModeler, TimeSeriesForecaster, ModelComparator
from report import ReportGenerator
from feature_engineering import SmartDataCleaner, FeatureCreator
from ml import LLMAnalyzer, LLMClient
from visual_registry import get_registry
import warnings
warnings.filterwarnings('ignore')

# Deep Learning imports (with fallback)
try:
    from deep_learning import (DeepLearningTrainer, TrainingConfig,
                               train_population_dl, train_housing_dl, DLResults)
    from dl_visualizer import DLVisualizer
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False
    print("[WARNING] Deep learning modules not available")


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
    schema = SchemaFactory.create(survey, scope)
    loader = FileLoader(config)
    df = loader.load(survey, scope)
    return df, schema, loader


def apply_schema(df: pd.DataFrame, schema):
    applier = SchemaApplier(schema)
    return applier.apply(df)


def clean_economic_zeros(df: pd.DataFrame) -> pd.DataFrame:
    econ_cols = ['Total_Person_Income', 'Wage_Income', 'Property_Value', 'Gross_Rent']
    existing = [c for c in econ_cols if c in df.columns]
    if existing:
        return SmartDataCleaner.handle_economic_zeros(df, existing, strategy='flag')
    return df.copy()


# ============================================================================
# FEATURE ENGINEERING (All <= 10 lines)
# ============================================================================

def create_income_features(df: pd.DataFrame) -> pd.DataFrame:
    if 'Total_Person_Income' in df.columns:
        return FeatureCreator.create_income_features(df)
    return df


def create_housing_features(df: pd.DataFrame) -> pd.DataFrame:
    if 'Property_Value' in df.columns or 'Gross_Rent' in df.columns:
        return FeatureCreator.create_housing_features(df)
    return df


def create_age_groups(df: pd.DataFrame) -> pd.DataFrame:
    if 'Age' in df.columns:
        return FeatureCreator.create_age_groups(df)
    return df


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    if 'Census_Year' in df.columns:
        return FeatureCreator.create_temporal_features(df)
    return df


def log_census_year(stage: str, df: pd.DataFrame):
    """Log Census_Year column status"""
    if 'Census_Year' in df.columns:
        valid = df['Census_Year'].notna().sum()
        unique = df['Census_Year'].nunique()
        print(f"[CENSUS_YEAR_TRACK] {stage}: {valid} valid, {unique} unique")
    else:
        print(f"[CENSUS_YEAR_TRACK] {stage}: Column not found")


def apply_features_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Apply feature engineering pipeline"""
    df = clean_economic_zeros(df)
    df = create_income_features(df)
    df = create_housing_features(df)
    df = create_age_groups(df)
    df = create_temporal_features(df)
    return df


def apply_feature_engineering(df: pd.DataFrame) -> tuple:
    """Apply feature engineering with tracking"""
    rows_before = len(df)
    df = apply_features_pipeline(df)
    results = {'cleaning': {'rows_before': rows_before, 'rows_after': len(df)},
               'final_shape': df.shape}
    return df, results


# ============================================================================
# ANALYSIS COMPONENTS (All <= 10 lines)
# ============================================================================

def run_temporal_analysis(df: pd.DataFrame) -> dict:
    try:
        return TemporalAnalyzer(df).analyze()
    except Exception as e:
        print(f"[WARNING] Temporal analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_economic_analysis(df: pd.DataFrame, survey: str) -> dict:
    try:
        if survey == 'housing':
            return {'housing': HousingEconomicAnalyzer(df).analyze()}
        elif survey == 'population':
            return {'population': PopulationEconomicAnalyzer(df).analyze()}
        return {}
    except Exception as e:
        print(f"[WARNING] Economic analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_correlation_analysis(df: pd.DataFrame) -> dict:
    try:
        focus = ['Age', 'Total_Person_Income', 'Wage_Income', 
                 'Property_Value', 'Gross_Rent', 'Hours_Worked_Per_Week']
        return CorrelationAnalyzer(df).analyze(focus)
    except Exception as e:
        print(f"[WARNING] Correlation analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_statistical_analysis(df: pd.DataFrame) -> dict:
    try:
        return StatisticalAnalyzer(df).analyze(None)
    except Exception as e:
        print(f"[WARNING] Statistical analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_outlier_analysis(df: pd.DataFrame) -> dict:
    try:
        return OutlierAnalyzer(df).analyze(None)
    except Exception as e:
        print(f"[WARNING] Outlier analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_anomaly_analysis(df: pd.DataFrame) -> dict:
    try:
        return AnomalyAnalyzer(df).analyze(None)
    except Exception as e:
        print(f"[WARNING] Anomaly analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_trend_analysis(df: pd.DataFrame) -> dict:
    try:
        return TrendAnalyzer(df).analyze(None)
    except Exception as e:
        print(f"[WARNING] Trend analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_cross_variable_analysis(df: pd.DataFrame) -> dict:
    try:
        return CrossVariableAnalyzer(df).analyze(None)
    except Exception as e:
        print(f"[WARNING] Cross-variable analysis skipped: {e}")
        return {'skipped': True, 'reason': str(e)}


def run_llm_analysis(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl=None):
    print("[VERBOSE] Initializing LLM client and analyzer...")
    client = LLMClient(config)
    analyzer = LLMAnalyzer(client)
    state = config.get_state_name()
    print(f"[VERBOSE] Running LLM analysis for state: {state}")
    return analyzer.run_analysis(df, temporal, state=state, economic=economic,
                                  correlations=corr, statistics=stats,
                                  outliers=outliers, anomalies=anom, trends=trends,
                                  deep_learning=dl)


# ============================================================================
# VISUALIZATION (All <= 10 lines)
# ============================================================================

def create_visuals(df: pd.DataFrame, config: Config, survey: str):
    try:
        print(f"\n[VISUALS] Creating comprehensive visualization suite for {survey.upper()}...")
        viz = Visualizer(df, config, survey_type=survey)
        viz.create_all()
        print(f"[SUCCESS] Visualizations saved to {config.figure_dir}")
    except Exception as e:
        print(f"[WARNING] Visualization creation failed: {e}")


# ============================================================================
# ML MODELS (All <= 10 lines each)
# ============================================================================

def is_income_column(col_name: str) -> bool:
    """Check if column name contains income-related terms"""
    income_terms = ['income', 'wage', 'earnings', 'salary', 'pay', 'hours']
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

    # Filter zeros for income-related target
    if is_income_column(target):
        y = y[y > 0]
        idx = idx.intersection(y.index)

    # Filter zeros for income-related features
    for feat in existing_features:
        if is_income_column(feat):
            X_feat = X[feat]
            valid_idx = X_feat[X_feat > 0].index
            idx = idx.intersection(valid_idx)

    if len(idx) < min_samples:
        return None, None
    return X.loc[idx], y.loc[idx]


def build_regression_result(target, X, best_name, best_result, models):
    """Build regression result dictionary"""
    return {'target': target, 'features': list(X.columns), 'best_model': best_name,
            'best_r2_score': best_result.test_score, 'sample_size': len(X), 
            'result_obj': best_result, 'all_models': models, 'all_model_objects': models}


def train_regression_model(df, target, features, min_samples=100):
    try:
        X, y = prepare_regression_data(df, target, features, min_samples)
        if X is None:
            return None
        models = ModelComparator.compare_regression_models(X, y)
        best_name, best_result = ModelComparator.select_best_model(models)
        return build_regression_result(target, X, best_name, best_result, models)
    except Exception as e:
        print(f"[WARNING] Regression model training failed for {target}: {str(e)}")
        return None


def prepare_clustering_data(df, features, min_samples):
    existing = [f for f in features if f in df.columns]
    if len(existing) < 2:
        return None
    X = df[existing].dropna()
    if len(X) < min_samples:
        return None
    return X


def build_clustering_result(X, best_result, all_results):
    """Build clustering result dictionary"""
    return {'features': list(X.columns), 'n_clusters': 5, 
            'silhouette_score': best_result.silhouette_score,
            'sample_size': len(X), 'result_obj': best_result,
            'all_clustering_models': all_results}


def train_all_clustering_algorithms(clusterer, X):
    """Train all clustering algorithms"""
    all_results = {}
    try:
        all_results['kmeans'] = clusterer.kmeans_clustering(X, n_clusters=5)
    except Exception as e:
        all_results['kmeans'] = {'error': str(e)}
    try:
        all_results['hierarchical'] = clusterer.hierarchical_clustering(X, n_clusters=5)
    except Exception as e:
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
        return build_clustering_result(X, best_result, all_results) if best_result else None
    except Exception as e:
        print(f"[WARNING] Clustering model training failed: {str(e)}")
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
    print(f"[DEBUG-TS] Target: {target}, Forecasts: {forecasts}, Values: {forecast_values}")

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
        print(f"[WARNING] Time series forecasting failed for {target}: {str(e)}")
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
            print(f"[WARNING] Viz failed for {model_name}: {str(e)}")


def viz_regression_results(ml_viz, ml_results, df, key):
    """Visualize all regression models, not just the best one"""
    try:
        if key not in ml_results or not ml_results[key]:
            return
        X, y, target = prepare_regression_viz_data(ml_results, df, key)
        all_models = ml_results[key].get('all_model_objects', {})
        viz_each_regression_model(ml_viz, all_models, X, y, target)
    except Exception as e:
        print(f"[WARNING] Regression visualization failed for {key}: {str(e)}")


def viz_each_clustering_model(ml_viz, all_models, X):
    """Visualize each clustering model"""
    for model_name, result_obj in all_models.items():
        if isinstance(result_obj, dict) and 'error' in result_obj:
            continue
        try:
            ml_viz.viz_clustering(result_obj, X)
        except Exception as e:
            print(f"[WARNING] Clustering viz failed for {model_name}: {str(e)}")


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
        print(f"[WARNING] Clustering visualization failed: {str(e)}")


def prepare_ts_model_result(target, model_name, model_data):
    """Create result dict for a specific time series model"""
    # Extract forecasts and convert to list of values
    forecasts = model_data.get('forecasts', {})
    forecast_values = list(forecasts.values()) if isinstance(forecasts, dict) else forecasts

    # Extract CI data
    ci_lower = model_data.get('ci_lower', [])
    ci_upper = model_data.get('ci_upper', [])

    print(f"[DEBUG-TS-MODEL] {model_name}: forecasts={forecasts}, values={forecast_values}, CI_lower={ci_lower}, CI_upper={ci_upper}")

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
            print(f"[WARNING] Time series viz failed for {model_name}: {str(e)}")


def viz_timeseries_results(ml_viz, ml_results, df):
    """Visualize all time series models for ALL targets"""
    try:
        # Find all timeseries keys (ending with _timeseries)
        ts_keys = [k for k in ml_results.keys() if k.endswith('_timeseries')]
        print(f"[VIZ-TIMESERIES] Found {len(ts_keys)} time series results: {ts_keys}")

        for ts_key in ts_keys:
            ts_result = ml_results[ts_key]
            target = ts_result.get('target')
            if not target or 'Census_Year' not in df.columns or target not in df.columns:
                print(f"[VIZ-TIMESERIES] Skipping {ts_key}: missing target or Census_Year")
                continue

            print(f"[VIZ-TIMESERIES] Visualizing time series for target: {target}")
            df_ts = df[['Census_Year', target]].dropna()
            viz_each_timeseries_model(ml_viz, ts_result.get('all_timeseries_models', {}), df_ts, target)
    except Exception as e:
        print(f"[WARNING] Time series visualization failed: {str(e)}")


def viz_model_comparison_results(ml_viz, ml_results, key):
    try:
        if key in ml_results and ml_results[key]:
            all_models = ml_results[key].get('all_models')
            target = ml_results[key].get('target')
            if all_models and target:
                ml_viz.viz_model_comparison(all_models, target_name=target)
    except Exception as e:
        print(f"[WARNING] Model comparison visualization failed for {key}: {str(e)}")


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


def train_regression_for_survey(df, survey, features):
    """Train regression models for all available target columns"""
    targets = get_all_target_cols(df, survey)
    if not targets:
        return None
    results = {}
    for target in targets:
        print(f"[ML] Training regression models for target: {target}")
        reg = train_regression_model(df, target, features)
        if reg:
            # Use target name as key for clarity
            key = f'{target}_regression'
            results[key] = reg
    return results if results else None


def add_clustering_to_results(results, df, features):
    cluster = train_clustering_model(df, features)
    if cluster:
        results['clustering'] = cluster


def add_timeseries_to_results(results, df, survey):
    """Train time series models for ALL available target columns"""
    targets = get_all_target_cols(df, survey)
    print(f"[ML-TIMESERIES] Training time series for {len(targets)} targets: {targets}")
    ts_results = {}
    for target in targets:
        print(f"[ML-TIMESERIES] Training time series for target: {target}")
        ts = train_timeseries_model(df, target)
        if ts:
            # Store each target's time series separately
            ts_results[f'{target}_timeseries'] = ts
    if ts_results:
        results.update(ts_results)


def train_all_ml_models(df, survey, features):
    results = {}
    reg_results = train_regression_for_survey(df, survey, features)
    if reg_results:
        results.update(reg_results)
    add_clustering_to_results(results, df, features)
    add_timeseries_to_results(results, df, survey)
    return results


def run_ml_pipeline(df: pd.DataFrame, config: Config, survey: str):
    try:
        print(f"\n[ML] Running ML pipeline for {survey.upper()}...")
        features = get_ml_features(df)
        results = train_all_ml_models(df, survey, features)
        if results:
            create_ml_visualizations(results, df, config, survey)
        return results
    except Exception as e:
        print(f"[WARNING] ML pipeline failed: {e}")
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
        print(f"[DL] Training {task_name}...")
        trainer = DeepLearningTrainer()
        result = trainer.train_model(df, survey, task_name, features, config)
        print(f"[DL] ✓ {task_name} complete: {result.task_type}, "
              f"Test metrics: {result.test_metrics}")
        gc.collect()  # Free memory after each task
        return result
    except Exception as e:
        print(f"[WARNING] DL task {task_name} failed: {e}")
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
        print(f"[DL-VIZ] Creating visualizations for {len(results)} tasks...")
        viz = DLVisualizer(config, survey)
        # Each task uses its own test data (stored in DLResults)
        viz.visualize_all(results)
        viz.plot_comprehensive_dashboard(results)
        print(f"[DL-VIZ] ✓ All visualizations saved to {viz.fig_dir}")
    except Exception as e:
        print(f"[WARNING] DL visualization failed: {e}")


def run_dl_pipeline(df: pd.DataFrame, config: Config, survey: str) -> Dict[str, DLResults]:
    """Run complete deep learning pipeline (≤10 lines)"""
    if not DL_AVAILABLE:
        print("[INFO] Deep learning not available, skipping DL pipeline")
        return {}
    try:
        print(f"\n[DL] Running deep learning pipeline for {survey.upper()}...")
        features = get_ml_features(df)
        results = train_all_dl_tasks(df, survey, features)
        if results:
            create_dl_visualizations(results, df, config, survey)
        return results
    except Exception as e:
        print(f"[WARNING] DL pipeline failed: {e}")
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
    print(f"[REPORT] Generated: {report_name}")


# ============================================================================
# MAIN ORCHESTRATOR (All <= 10 lines)
# ============================================================================

def load_and_prepare_data(state, survey, config, scope):
    df, schema, loader = load_data(state, survey, config, scope)
    if df.empty:
        return None, None, None
    df = apply_schema(df, schema)
    # Update loader.stats with post-schema dimensions
    loader.stats.total_rows = len(df)
    loader.stats.columns_found = len(df.columns)
    print(f"[INFO] Loaded {len(df):,} records")
    log_census_year("After schema application", df)
    df, feat_eng = apply_feature_engineering(df)
    print(f"[VERBOSE] Feature engineering complete: {feat_eng['final_shape']}")
    return df, loader, feat_eng


def run_all_analyses(df, survey):
    print("[VERBOSE] Running comprehensive analysis suite...")
    temporal = run_temporal_analysis(df)
    economic = run_economic_analysis(df, survey)
    corr = run_correlation_analysis(df)
    stats = run_statistical_analysis(df)
    outliers = run_outlier_analysis(df)
    anom = run_anomaly_analysis(df)
    trends = run_trend_analysis(df)
    cross_var = run_cross_variable_analysis(df)
    return temporal, economic, corr, stats, outliers, anom, trends, cross_var


def run_llm_with_fallback(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl=None):
    try:
        print("[VERBOSE] Starting LLM analysis with fallback handler...")
        result = run_llm_analysis(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl)
        print("[VERBOSE] LLM analysis completed successfully")
        return result
    except Exception as e:
        print(f"[WARNING] LLM analysis skipped: {e}")
        print("[VERBOSE] Full traceback:")
        traceback.print_exc()
        return {'interpretation': 'LLM analysis not available',
                'analysis': 'Please ensure LM Studio is running on localhost:1234',
                'suggestions': 'N/A', 'policy_recommendations': 'N/A'}


def run_visualizations_and_ml(df, config, survey):
    create_visuals(df, config, survey)
    # HOUSING: Sample df before ML/DL to prevent memory explosion
    if survey.lower() == 'housing':
        target_cells = 10_000_000
        sample_rows = min(len(df), int(target_cells / len(df.columns)))
        if len(df) > sample_rows:
            print(f"[ML-SAMPLE] Housing: {len(df):,} → {sample_rows:,} rows ({target_cells:,} cells / {len(df.columns)} cols)")
            df_ml = df.sample(n=sample_rows, random_state=42)
        else:
            df_ml = df
    else:
        df_ml = df
    ml = run_ml_pipeline(df_ml, config, survey)
    dl = run_dl_pipeline(df_ml, config, survey)
    return {'ml': ml, 'dl': dl}


def generate_full_report(config, loader, df, survey, state, temporal, economic,
                        corr, stats, outliers, anom, trends, ml_dl_results, feat_eng, cross_var):
    # Extract ML and DL results from combined structure
    ml_results = ml_dl_results.get('ml', {}) if isinstance(ml_dl_results, dict) else ml_dl_results
    dl_results = ml_dl_results.get('dl', {}) if isinstance(ml_dl_results, dict) else {}
    llm = run_llm_with_fallback(df, config, temporal, economic, corr, stats, outliers, anom, trends, dl_results)
    generate_report(config, loader, temporal, economic, corr, stats,
                   outliers, anom, trends, llm, feat_eng, ml_results, survey, state, cross_var, dl_results)


def run_analysis_and_reporting(df, loader, feat_eng, config, survey, state):
    temporal, economic, corr, stats, outliers, anom, trends, cross_var = run_all_analyses(df, survey)
    ml = run_visualizations_and_ml(df, config, survey)
    generate_full_report(config, loader, df, survey, state, temporal, economic, 
                        corr, stats, outliers, anom, trends, ml, feat_eng, cross_var)


def process_survey(state: str, survey: str, config: Config, scope: str):
    print(f"\n{'='*70}\n[{survey.upper()}] Processing {state} ({scope})...\n{'='*70}")
    config.set_survey(survey, scope)
    df, loader, feat_eng = load_and_prepare_data(state, survey, config, scope)
    if df is None:
        print(f"[WARNING] No data for {state} - {survey} ({scope})")
        return None
    run_analysis_and_reporting(df, loader, feat_eng, config, survey, state)
    print(f"[SUCCESS] {survey.upper()} ({scope}) pipeline complete for {state}!")
    return df


def process_state_surveys(state, surveys, scopes):
    state = state.strip()
    config = create_config(state)
    for survey in surveys:
        survey = survey.strip().lower()
        for scope in scopes:
            scope = scope.strip()
            config.set_survey(survey, scope)
            create_dirs(config, survey)
            process_survey(state, survey, config, scope)


def setup_parser(parser):
    """Configure argument parser with all CLI options"""
    parser.add_argument('--all-states', action='store_true',
                       help='Run analysis for all states')
    parser.add_argument('--all-scopes', action='store_true',
                       help='Run analysis for all scopes (1-Year and 5-Year)')
    parser.add_argument('--states', type=str,
                       help='Comma-separated list of states')
    parser.add_argument('--surveys', type=str,
                       help='Comma-separated list of surveys')
    parser.add_argument('--scopes', type=str,
                       help='Comma-separated list of scopes')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Census Data Analysis Pipeline')
    setup_parser(parser)
    return parser.parse_args()


def get_states_list(args):
    if args.all_states:
        all_states = list(FIPS_MAP.values())
        print(f"[INFO] Running for ALL {len(all_states)} states/territories")
        return all_states
    elif args.states:
        return args.states.split(',')
    else:
        return os.getenv('CENSUS_STATES', 'Kansas').split(',')


def get_scopes_list(args):
    if args.all_scopes:
        all_scopes = ['1-Year', '5-Year']
        print(f"[INFO] Running for ALL scopes: {all_scopes}")
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
    
    print(f"[CONFIG] States: {len(states)}, Surveys: {surveys}, Scopes: {scopes}")
    for state in states:
        process_state_surveys(state, surveys, scopes)
    print(f"\n{'='*70}\n[COMPLETE] All processing finished!\n{'='*70}\n")


if __name__ == '__main__':
    main()

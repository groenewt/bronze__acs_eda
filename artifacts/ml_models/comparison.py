import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

from typing import Dict, Tuple, Optional
import pandas as pd
from .base import ModelResults, SKLEARN_AVAILABLE
from .regression import RegressionModeler
from .classification import ClassificationModeler
from logging_config import get_logger

logger = get_logger("ml.comparison")


# ============================================================================
# MODEL COMPARISON
# ============================================================================

class ModelComparator:
    """Compare multiple models and select the best"""

    @staticmethod
    def compare_regression_models(X: pd.DataFrame, y: pd.Series,
                                  tune: bool = False,
                                  sample_weight: Optional[pd.Series] = None) -> Dict[str, ModelResults]:
        """
        Compare multiple regression models.

        Args:
            X: Feature DataFrame
            y: Target Series
            tune: If True, run hyperparameter tuning before final training
            sample_weight: Optional sample weights for training
        """
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available'}

        modeler = RegressionModeler()
        results = {}

        for model_type in ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']:
            try:
                # Optionally tune hyperparameters first
                if tune and model_type in ['ridge', 'lasso', 'random_forest', 'gradient_boosting']:
                    if len(X) > 500_000:
                        logger.warning(f"[TUNE] Large dataset ({len(X):,} rows) - will sample for tuning")
                    logger.info(f"[TUNE] Tuning hyperparameters for {model_type}...")
                    tune_result = modeler.tune_hyperparameters(X, y, model_type)
                    if 'best_params' in tune_result:
                        # Apply best params to model before training
                        best_params = tune_result['best_params']
                        best_score = tune_result.get('best_score', 0)
                        modeler.models[model_type].set_params(**best_params)
                        logger.info(f"[TUNE] Best params for {model_type}: {best_params}")
                        logger.info(f"[TUNE] Best CV R² score: {best_score:.4f}")
                        # Log number of candidates searched
                        cv_results = tune_result.get('cv_results')
                        if cv_results:
                            n_candidates = len(cv_results['mean_test_score'])
                            logger.info(f"[TUNE] Searched {n_candidates} parameter combinations")

                result = modeler.train_model(X, y, model_type=model_type,
                                            sample_weight=sample_weight)
                results[model_type] = result
            except Exception as e:
                logger.error(f"[ML-ERROR] Model {model_type} training failed: {e}")
                results[model_type] = {'error': str(e)}

        return results

    @staticmethod
    def compare_classification_models(X: pd.DataFrame, y: pd.Series) -> Dict[str, ModelResults]:
        """Compare multiple classification models"""
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available'}

        modeler = ClassificationModeler()
        results = {}

        # Test all available classification models
        model_types = ['logistic', 'decision_tree', 'random_forest', 'gradient_boosting',
                      'adaboost', 'extratrees', 'svc', 'knn', 'gaussian_nb',
                      'mlp', 'bagging']

        for model_type in model_types:
            try:
                result = modeler.train_model(X, y, model_type=model_type)
                results[model_type] = result
            except Exception as e:
                results[model_type] = {'error': str(e)}

        return results

    @staticmethod
    def select_best_model(results: Dict[str, ModelResults], metric: str = 'test_score') -> Tuple[str, ModelResults]:
        """Select the best model based on a metric"""
        best_name = None
        best_result = None
        best_score = -float('inf')

        for name, result in results.items():
            if isinstance(result, dict) and 'error' in result:
                continue
            score = getattr(result, metric, None)
            if score is not None and score > best_score:
                best_score = score
                best_name = name
                best_result = result

        return best_name, best_result

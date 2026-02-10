import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

from logging_config import get_logger
from memory_utils import get_safe_shap_sample_size, memory_phase

logger = get_logger("ml.explainability")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


# ============================================================================
# MODEL EXPLAINABILITY (SHAP)
# ============================================================================

class ModelExplainer:
    """
    Model explainability using SHAP (SHapley Additive exPlanations).

    Provides feature importance explanations for tree-based and linear models.
    """

    # Models that work well with TreeExplainer
    TREE_MODELS = {'random_forest', 'gradient_boosting', 'adaboost', 'extratrees', 'decision_tree'}

    # Models that work with LinearExplainer
    LINEAR_MODELS = {'linear', 'ridge', 'lasso', 'elasticnet'}

    def __init__(self):
        if not SHAP_AVAILABLE:
            raise ImportError("SHAP library not available. Install with: pip install shap")

    def explain_model(self, model, X_train: pd.DataFrame, X_test: pd.DataFrame,
                      model_type: str = 'random_forest') -> Dict[str, Any]:
        """
        Generate SHAP explanations for a fitted model.

        Args:
            model: Fitted sklearn model
            X_train: Training features (for background data)
            X_test: Test features to explain
            model_type: Type of model ('random_forest', 'gradient_boosting', 'linear', etc.)

        Returns:
            Dict with shap_values, feature_importance, and explanation data
        """
        try:
            if model_type in self.TREE_MODELS:
                return self._explain_tree_model(model, X_train, X_test)
            elif model_type in self.LINEAR_MODELS:
                return self._explain_linear_model(model, X_train, X_test)
            else:
                # Fall back to KernelExplainer for other models
                return self._explain_kernel(model, X_train, X_test)
        except Exception as e:
            return {'error': f'SHAP explanation failed: {str(e)}'}

    def _explain_tree_model(self, model, X_train: pd.DataFrame, X_test: pd.DataFrame) -> Dict[str, Any]:
        """Use TreeExplainer for tree-based models"""
        # Get safe sample size using memory_utils
        n_estimators = getattr(model, 'n_estimators', 100)
        safe_n = get_safe_shap_sample_size(
            len(X_test),
            n_features=len(X_test.columns),
            n_estimators=n_estimators,
            balanced=True  # Use balanced mode (1000 samples)
        )

        if len(X_test) > safe_n:
            X_test_sample = X_test.sample(n=safe_n, random_state=42)
            logger.info(f"[SHAP] Sampled test data: {len(X_test):,} -> {safe_n:,}")
        else:
            X_test_sample = X_test

        with memory_phase("SHAP_TreeExplainer"):
            logger.info(f"[SHAP] Computing TreeExplainer for {len(X_test_sample):,} samples...")
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test_sample)

        # Handle multi-output (some models return list)
        if isinstance(shap_values, list):
            shap_values = shap_values[0] if len(shap_values) == 1 else shap_values[-1]

        # Calculate mean absolute SHAP value per feature
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_importance = dict(zip(X_test_sample.columns, mean_abs_shap))

        logger.info(f"[SHAP] TreeExplainer complete. Top feature: {max(feature_importance, key=feature_importance.get)}")

        return {
            'shap_values': shap_values,
            'expected_value': explainer.expected_value,
            'feature_importance': feature_importance,
            'feature_names': list(X_test_sample.columns),
            'X_test': X_test_sample.values,
            'explainer_type': 'tree'
        }

    def _explain_linear_model(self, model, X_train: pd.DataFrame, X_test: pd.DataFrame) -> Dict[str, Any]:
        """Use LinearExplainer for linear models"""
        # Apply same sampling strategy for consistency
        safe_n = get_safe_shap_sample_size(len(X_test), n_features=len(X_test.columns), balanced=True)

        if len(X_test) > safe_n:
            X_test_sample = X_test.sample(n=safe_n, random_state=42)
            logger.info(f"[SHAP] Sampled test data for LinearExplainer: {len(X_test):,} -> {safe_n:,}")
        else:
            X_test_sample = X_test

        with memory_phase("SHAP_LinearExplainer"):
            logger.info(f"[SHAP] Computing LinearExplainer for {len(X_test_sample):,} samples...")
            explainer = shap.LinearExplainer(model, X_train)
            shap_values = explainer.shap_values(X_test_sample)

        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_importance = dict(zip(X_test_sample.columns, mean_abs_shap))

        logger.info(f"[SHAP] LinearExplainer complete. Top feature: {max(feature_importance, key=feature_importance.get)}")

        return {
            'shap_values': shap_values,
            'expected_value': explainer.expected_value,
            'feature_importance': feature_importance,
            'feature_names': list(X_test_sample.columns),
            'X_test': X_test_sample.values,
            'explainer_type': 'linear'
        }

    def _explain_kernel(self, model, X_train: pd.DataFrame, X_test: pd.DataFrame) -> Dict[str, Any]:
        """Use KernelExplainer as fallback (slower but model-agnostic)"""
        # Sample background data to speed up KernelExplainer
        background = shap.sample(X_train, min(100, len(X_train)))

        # Limit test samples to avoid long computation
        sample_size = min(50, len(X_test))
        X_test_sample = X_test.iloc[:sample_size]
        logger.info(f"[SHAP] KernelExplainer: using {sample_size} test samples, 100 background samples")

        with memory_phase("SHAP_KernelExplainer"):
            explainer = shap.KernelExplainer(model.predict, background)
            shap_values = explainer.shap_values(X_test_sample)

        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_importance = dict(zip(X_test_sample.columns, mean_abs_shap))

        logger.info(f"[SHAP] KernelExplainer complete. Top feature: {max(feature_importance, key=feature_importance.get)}")

        return {
            'shap_values': shap_values,
            'expected_value': explainer.expected_value,
            'feature_importance': feature_importance,
            'feature_names': list(X_test_sample.columns),
            'X_test': X_test_sample.values,
            'explainer_type': 'kernel'
        }

    @staticmethod
    def get_top_features(feature_importance: Dict[str, float], top_n: int = 10) -> List[Tuple[str, float]]:
        """Get top N most important features sorted by importance"""
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        return sorted_features[:top_n]

"""
Regression Models Module
Provides regression modeling with multiple algorithms
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from .base import BaseMLModel, ModelResults, SKLEARN_AVAILABLE

try:
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.preprocessing import RobustScaler
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
    from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor,
                                  AdaBoostRegressor, ExtraTreesRegressor)
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
except ImportError:
    pass  # SKLEARN_AVAILABLE flag from base handles this

from exceptions import (ModelTrainingError, InsufficientDataError)
from logging_config import get_logger
from memory_utils import (get_ml_tuning_sample_limit, MemoryGuard, memory_phase)

logger = get_logger("ml.regression")


class RegressionModeler(BaseMLModel):
    """Handles regression modeling with multiple algorithms"""

    def __init__(self, random_state: int = 42):
        super().__init__(random_state)
        self.models = {
            'linear': LinearRegression(),
            'ridge': Ridge(alpha=1.0, random_state=random_state),
            'lasso': Lasso(alpha=1.0, random_state=random_state),
            'elasticnet': ElasticNet(alpha=1.0, random_state=random_state),
            'svr': SVR(kernel='rbf'),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=random_state),
            'adaboost': AdaBoostRegressor(n_estimators=100, random_state=random_state),
            'extratrees': ExtraTreesRegressor(n_estimators=100, random_state=random_state, n_jobs=-1),
            'knn': KNeighborsRegressor(n_neighbors=5, n_jobs=-1),
            'decision_tree': DecisionTreeRegressor(random_state=random_state)
        }

    # Models that support sample_weight parameter
    SUPPORTS_SAMPLE_WEIGHT = {'linear', 'ridge', 'lasso', 'elasticnet',
                              'random_forest', 'gradient_boosting', 'adaboost',
                              'extratrees', 'decision_tree'}

    def train_model(self, X: pd.DataFrame, y: pd.Series,
                   model_type: str = 'random_forest',
                   test_size: float = 0.2,
                   cv_folds: int = 5,
                   sample_weight: Optional[pd.Series] = None) -> ModelResults:
        """
        Train a regression model with evaluation.

        Args:
            X: Feature DataFrame
            y: Target Series
            model_type: Type of model to train
            test_size: Fraction of data to use for testing
            cv_folds: Number of cross-validation folds
            sample_weight: Optional sample weights (e.g., ACS survey weights).
                          Weights are normalized before training.
        """
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError(model_type, "scikit-learn not available")

            if len(X) < 10:
                raise InsufficientDataError('regression', 10, len(X))

            # Prepare data - scale for linear models and distance-based models
            scale_models = {'svr', 'knn', 'linear', 'ridge', 'lasso', 'elasticnet'}
            X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))

            # Align sample weights with cleaned data
            weights_train = None
            weights_test = None
            weights_clean = None
            use_weights = (sample_weight is not None and
                          model_type in self.SUPPORTS_SAMPLE_WEIGHT)

            if use_weights:
                # Align weights with cleaned indices (handle index misalignment)
                try:
                    weights_clean = sample_weight.loc[X_clean.index].values
                except KeyError:
                    # Fallback: reindex sample_weight to match
                    weights_clean = sample_weight.reindex(X_clean.index).fillna(1.0).values
                # Normalize weights for numerical stability
                weights_clean = weights_clean / weights_clean.sum() * len(weights_clean)

            # Split data
            if use_weights:
                X_train, X_test, y_train, y_test, weights_train, weights_test = train_test_split(
                    X_clean, y_clean, weights_clean, test_size=test_size, random_state=self.random_state
                )
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_clean, y_clean, test_size=test_size, random_state=self.random_state
                )

            # Train model
            self.model = self.models.get(model_type, self.models['random_forest'])
            if use_weights:
                self.model.fit(X_train, y_train, sample_weight=weights_train)
            else:
                self.model.fit(X_train, y_train)
            self.is_fitted = True

            # Evaluate
            train_score = r2_score(y_train, self.model.predict(X_train))
            test_score = r2_score(y_test, self.model.predict(X_test))
            y_pred = self.model.predict(X_test)

            # Cross-validation (skip weighted CV - fit_params deprecated in sklearn 1.4+)
            # Model was already trained with weights, CV is just for validation
            cv_scores = cross_val_score(self.model, X_clean, y_clean,
                                       cv=cv_folds, scoring='r2')

            # Feature importance
            feat_imp = self._get_feature_importance(X_clean.columns.tolist())

            # Additional metrics
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mse)

            return ModelResults(
                model_type='regression',
                model_name=model_type,
                train_score=train_score,
                test_score=test_score,
                cv_scores=cv_scores.tolist(),
                predictions=y_pred,
                feature_importance=feat_imp,
                metadata={
                    'mse': mse,
                    'rmse': rmse,
                    'mae': mae,
                    'n_features': X_clean.shape[1],
                    'n_samples': len(X_clean),
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'y_test': y_test.values if hasattr(y_test, 'values') else y_test,
                    'used_sample_weights': use_weights
                }
            )
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError(model_type, str(e))

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions on new data"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")
        X_clean, _ = self._prepare_data(X, scale=True)
        return self.model.predict(X_clean)

    def tune_hyperparameters(self, X: pd.DataFrame, y: pd.Series,
                            model_type: str = 'random_forest') -> Dict[str, Any]:
        """Tune hyperparameters using grid search with memory-safe sampling."""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for hyperparameter tuning")

        scale_models = {'svr', 'knn', 'linear', 'ridge', 'lasso', 'elasticnet'}
        X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))

        param_grids = self._get_param_grids()
        if model_type not in param_grids:
            return {'error': f'No parameter grid defined for {model_type}'}

        # Calculate grid size
        grid = param_grids[model_type]
        n_combinations = 1
        for param, values in grid.items():
            n_combinations *= len(values)

        # Adaptive CV folds for large datasets
        n_cv_folds = 3 if len(X_clean) > 500_000 else 5

        # Use memory_utils to get safe sample limit
        safe_n = get_ml_tuning_sample_limit(
            n_samples=len(X_clean),
            n_combinations=n_combinations,
            n_cv_folds=n_cv_folds
        )

        # Sample using existing utility pattern
        if safe_n < len(X_clean):
            idx = np.random.choice(len(X_clean), safe_n, replace=False)
            X_tune = X_clean.iloc[idx]
            y_tune = y_clean.iloc[idx]
        else:
            X_tune, y_tune = X_clean, y_clean

        logger.info(f"[TUNE] Data: {len(X_tune):,} samples, {X_tune.shape[1]} features")
        logger.info(f"[TUNE] Searching {n_combinations} combinations "
                    f"({n_cv_folds}-fold CV = {n_combinations * n_cv_folds} fits)")

        # Limit n_jobs based on dataset size (prevents memory explosion from worker copies)
        n_jobs = 2 if len(X_tune) > 100_000 else (4 if len(X_tune) > 50_000 else -1)

        base_model = self.models.get(model_type)

        # Use MemoryGuard from memory_utils for safety monitoring
        with memory_phase(f"tune_{model_type}"):
            with MemoryGuard(max_memory_mb=16000, action="warn"):
                grid_search = GridSearchCV(
                    base_model,
                    param_grids[model_type],
                    cv=n_cv_folds,
                    scoring='r2',
                    n_jobs=n_jobs,
                    verbose=0
                )
                grid_search.fit(X_tune, y_tune)

        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'best_estimator': grid_search.best_estimator_,
            'cv_results': grid_search.cv_results_,
            'tuning_sample_size': len(X_tune)
        }

    def _get_param_grids(self) -> Dict[str, Dict]:
        """Get comprehensive hyperparameter grids for all models"""
        return {
            'random_forest': {
                'n_estimators': [100, 200],           # was [50, 100, 200]
                'max_depth': [20, 30, None],          # was [10, 20, 30, None]
                'min_samples_split': [2, 5],          # was [2, 5, 10]
                'min_samples_leaf': [1, 2]            # was [1, 2, 4]
            },  # 2×3×2×2 = 24 combinations (down from 108)
            'gradient_boosting': {
                'n_estimators': [100, 200],           # was [50, 100, 200]
                'learning_rate': [0.1, 0.3],          # was [0.01, 0.1, 0.3]
                'max_depth': [5, 7],                  # was [3, 5, 7]
                'subsample': [0.8, 0.9, 1.0]          # was [0.8, 1.0]
            },  # 2×2×2×3 = 24 combinations (down from 54)
            'ridge': {
                'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
            },
            'lasso': {
                'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
            },
            'elasticnet': {
                'alpha': [0.01, 0.1, 1.0, 10.0],
                'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
            },
            'svr': {
                'C': [0.1, 1.0, 10.0, 100.0],
                'gamma': ['scale', 'auto', 0.01, 0.1],
                'kernel': ['rbf', 'linear']
            },
            'adaboost': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.5, 1.0]
            },
            'extratrees': {
                'n_estimators': [50, 100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5, 10]
            },
            'knn': {
                'n_neighbors': [3, 5, 7, 10, 15],
                'weights': ['uniform', 'distance'],
                'metric': ['euclidean', 'manhattan']
            },
            'decision_tree': {
                'max_depth': [5, 10, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        }

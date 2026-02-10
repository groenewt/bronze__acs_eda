"""
Advanced Feature Selection Module for Census Data Analysis
Provides sophisticated feature selection methods including RFE, permutation importance, and SHAP
"""
import pandas as pd
import numpy as np
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')
# Suppress sklearn.utils.parallel warning (Python 3.13 compatibility)
warnings.filterwarnings('ignore', message='.*sklearn.utils.parallel.*')

try:
    from sklearn.feature_selection import RFE
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import Lasso
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AdvancedFeatureSelector:
    """Advanced feature selection with stability and importance methods"""

    @staticmethod
    def select_by_rfe(df: pd.DataFrame, target_col: str,
                      n_features: int = 10,
                      estimator: str = 'random_forest') -> List[str]:
        """Recursive Feature Elimination"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            logger.warning("RFE: sklearn not available")
            return []

        try:
            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 50 or X.shape[1] < n_features:
                return X.columns.tolist()[:n_features]

            # Select estimator
            if estimator == 'random_forest':
                est = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            else:
                est = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)

            rfe = RFE(estimator=est, n_features_to_select=min(n_features, X.shape[1]))
            rfe.fit(X, y)

            selected = X.columns[rfe.support_].tolist()
            logger.debug(f"RFE selected {len(selected)} features")
            return selected
        except Exception as e:
            logger.warning(f"RFE failed: {e}")
            return []

    @staticmethod
    def select_by_permutation_importance(df: pd.DataFrame, target_col: str,
                                         n_features: int = 10,
                                         n_repeats: int = 10) -> List[str]:
        """Permutation-based feature importance"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            return []

        try:
            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 100:
                return X.columns.tolist()[:n_features]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)

            perm_importance = permutation_importance(
                model, X_test, y_test, n_repeats=n_repeats, random_state=42, n_jobs=-1
            )

            importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': perm_importance.importances_mean
            }).sort_values('importance', ascending=False)

            selected = importance_df.head(n_features)['feature'].tolist()
            logger.debug(f"Permutation importance selected {len(selected)} features")
            return selected
        except Exception as e:
            logger.warning(f"Permutation importance failed: {e}")
            return []

    @staticmethod
    def select_by_stability(df: pd.DataFrame, target_col: str,
                           n_bootstrap: int = 50,
                           threshold: float = 0.6) -> List[str]:
        """Stability selection - robust feature selection across bootstrap samples"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        if not SKLEARN_AVAILABLE:
            return []

        try:
            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return []

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            if len(X) < 100:
                return X.columns.tolist()

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            selection_counts = {col: 0 for col in X.columns}
            n_samples = len(X)

            for i in range(n_bootstrap):
                # Bootstrap sample
                indices = np.random.choice(n_samples, size=n_samples, replace=True)
                X_boot = X_scaled[indices]
                y_boot = y.iloc[indices].values

                # Fit Lasso
                lasso = Lasso(alpha=0.01, max_iter=1000, random_state=i)
                lasso.fit(X_boot, y_boot)

                # Count non-zero coefficients
                for j, coef in enumerate(lasso.coef_):
                    if abs(coef) > 1e-5:
                        selection_counts[X.columns[j]] += 1

            # Select features appearing in > threshold of bootstrap samples
            selected = [col for col, count in selection_counts.items()
                       if count / n_bootstrap > threshold]

            logger.debug(f"Stability selection: {len(selected)} features (threshold={threshold})")
            return selected
        except Exception as e:
            logger.warning(f"Stability selection failed: {e}")
            return []

    @staticmethod
    def get_shap_importance(df: pd.DataFrame, target_col: str,
                           n_features: int = 10,
                           sample_size: int = 1000) -> Dict[str, float]:
        """SHAP-based feature importance (optional - requires shap package)"""
        from logging_config import get_logger
        logger = get_logger("feature_engineering")

        try:
            import shap

            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if target_col not in numeric_df.columns:
                return {}

            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]

            # Sample if needed
            if len(X) > sample_size:
                sample_idx = np.random.choice(len(X), sample_size, replace=False)
                X_sample = X.iloc[sample_idx]
                y_sample = y.iloc[sample_idx]
            else:
                X_sample, y_sample = X, y

            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_sample, y_sample)

            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_sample)

            importance = np.abs(shap_values).mean(axis=0)
            importance_dict = dict(zip(X.columns, importance))
            sorted_importance = dict(sorted(importance_dict.items(),
                                           key=lambda x: x[1], reverse=True)[:n_features])

            logger.debug(f"SHAP importance calculated for {len(sorted_importance)} features")
            return sorted_importance
        except ImportError:
            logger.warning("SHAP package not available")
            return {}
        except Exception as e:
            logger.warning(f"SHAP importance failed: {e}")
            return {}

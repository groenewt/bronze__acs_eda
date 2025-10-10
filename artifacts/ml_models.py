"""
Machine Learning Models Module for Census Data Analysis
Provides comprehensive predictive modeling, clustering, and evaluation capabilities
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import warnings
from exceptions import (ModelTrainingError, ModelPredictionError, ModelEvaluationError,
                        InvalidModelParametersError, InsufficientDataError,
                        TimeSeriesForecastError, ConfidenceIntervalError)
warnings.filterwarnings('ignore')

try:
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
    from sklearn.ensemble import (RandomForestRegressor, RandomForestClassifier, 
                                  GradientBoostingRegressor, GradientBoostingClassifier,
                                  AdaBoostRegressor, AdaBoostClassifier, 
                                  ExtraTreesRegressor, ExtraTreesClassifier,
                                  BaggingClassifier, VotingClassifier, StackingClassifier)
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
    from sklearn.svm import SVR, SVC
    from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
    from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                                 accuracy_score, precision_score, recall_score, f1_score,
                                 confusion_matrix, classification_report, silhouette_score)
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. ML models will be disabled.")


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ModelResults:
    """Container for model results"""
    model_type: str
    model_name: str
    train_score: float
    test_score: Optional[float]
    cv_scores: Optional[List[float]]
    predictions: Optional[np.ndarray]
    feature_importance: Optional[Dict[str, float]]
    metadata: Dict[str, Any]


@dataclass
class ClusterResults:
    """Container for clustering results"""
    method: str
    n_clusters: int
    labels: np.ndarray
    silhouette_score: float
    cluster_sizes: Dict[int, int]
    cluster_centers: Optional[np.ndarray]
    metadata: Dict[str, Any]


# ============================================================================
# BASE MODEL CLASS
# ============================================================================

class BaseMLModel:
    """Base class for ML models with common functionality"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.is_fitted = False
        
    def _prepare_data(self, X: pd.DataFrame, y: pd.Series = None,
                     scale: bool = True) -> Tuple:
        """Prepare data for modeling with proper handling of nulls/zeros"""
        # Remove rows with any nulls in features
        if y is not None:
            mask = ~(X.isna().any(axis=1) | y.isna())
            X_clean = X[mask].copy()
            y_clean = y[mask].copy()
        else:
            mask = ~X.isna().any(axis=1)
            X_clean = X[mask].copy()
            y_clean = None
            
        # Scale if requested
        if scale and self.scaler is None:
            self.scaler = RobustScaler()  # Better for data with outliers
            X_scaled = self.scaler.fit_transform(X_clean)
            X_clean = pd.DataFrame(X_scaled, columns=X_clean.columns, index=X_clean.index)
        elif scale and self.scaler is not None:
            X_scaled = self.scaler.transform(X_clean)
            X_clean = pd.DataFrame(X_scaled, columns=X_clean.columns, index=X_clean.index)
            
        return X_clean, y_clean
    
    def _get_feature_importance(self, feature_names: List[str]) -> Dict[str, float]:
        """Extract feature importance if available"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            return dict(zip(feature_names, importances))
        elif hasattr(self.model, 'coef_'):
            coefs = np.abs(self.model.coef_).flatten()
            return dict(zip(feature_names, coefs))
        return {}


# ============================================================================
# REGRESSION MODELS
# ============================================================================

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
        
    def train_model(self, X: pd.DataFrame, y: pd.Series, 
                   model_type: str = 'random_forest',
                   test_size: float = 0.2,
                   cv_folds: int = 5) -> ModelResults:
        """Train a regression model with evaluation"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError(model_type, "scikit-learn not available")
            
            if len(X) < 10:
                raise InsufficientDataError('regression', 10, len(X))
            
            # Prepare data - scale for linear models and distance-based models
            scale_models = {'svr', 'knn', 'linear', 'ridge', 'lasso', 'elasticnet'}
            X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=test_size, random_state=self.random_state
            )
            
            # Train model
            self.model = self.models.get(model_type, self.models['random_forest'])
            self.model.fit(X_train, y_train)
            self.is_fitted = True
            
            # Evaluate
            train_score = r2_score(y_train, self.model.predict(X_train))
            test_score = r2_score(y_test, self.model.predict(X_test))
            y_pred = self.model.predict(X_test)
            
            # Cross-validation
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
                    'y_test': y_test.values if hasattr(y_test, 'values') else y_test
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
        """Tune hyperparameters using comprehensive grid search"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for hyperparameter tuning")
        
        scale_models = {'svr', 'knn', 'linear', 'ridge', 'lasso', 'elasticnet'}
        X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))
        
        param_grids = self._get_param_grids()
        
        if model_type not in param_grids:
            return {'error': f'No parameter grid defined for {model_type}'}
        
        base_model = self.models.get(model_type)
        grid_search = GridSearchCV(base_model, param_grids[model_type],
                                   cv=5, scoring='r2', n_jobs=-1, verbose=0)
        grid_search.fit(X_clean, y_clean)
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'best_estimator': grid_search.best_estimator_,
            'cv_results': grid_search.cv_results_
        }
    
    def _get_param_grids(self) -> Dict[str, Dict]:
        """Get comprehensive hyperparameter grids for all models"""
        return {
            'random_forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 1.0]
            },
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


# ============================================================================
# CLASSIFICATION MODELS
# ============================================================================

class ClassificationModeler(BaseMLModel):
    """Handles classification modeling with multiple algorithms"""
    
    def __init__(self, random_state: int = 42):
        super().__init__(random_state)
        self.models = {
            'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
            'decision_tree': DecisionTreeClassifier(random_state=random_state),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=random_state),
            'adaboost': AdaBoostClassifier(n_estimators=100, random_state=random_state),
            'extratrees': ExtraTreesClassifier(n_estimators=100, random_state=random_state, n_jobs=-1),
            'svc': SVC(kernel='rbf', random_state=random_state),
            'knn': KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            'gaussian_nb': GaussianNB(),
            'multinomial_nb': MultinomialNB(),
            'bernoulli_nb': BernoulliNB(),
            'mlp': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=random_state),
            'bagging': BaggingClassifier(n_estimators=100, random_state=random_state, n_jobs=-1)
        }
        
    def train_model(self, X: pd.DataFrame, y: pd.Series,
                   model_type: str = 'random_forest',
                   test_size: float = 0.2,
                   cv_folds: int = 5) -> ModelResults:
        """Train a classification model with evaluation"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for ML models")
            
        # Prepare data - scale for linear and distance-based models
        scale_models = {'logistic', 'svc', 'knn', 'mlp', 'gaussian_nb'}
        X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean, test_size=test_size, random_state=self.random_state, stratify=y_clean
        )
        
        # Train model
        self.model = self.models.get(model_type, self.models['random_forest'])
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Evaluate
        train_score = accuracy_score(y_train, self.model.predict(X_train))
        test_score = accuracy_score(y_test, self.model.predict(X_test))
        y_pred = self.model.predict(X_test)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_clean, y_clean,
                                    cv=cv_folds, scoring='accuracy')
        
        # Feature importance
        feat_imp = self._get_feature_importance(X_clean.columns.tolist())
        
        # Additional metrics
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        return ModelResults(
            model_type='classification',
            model_name=model_type,
            train_score=train_score,
            test_score=test_score,
            cv_scores=cv_scores.tolist(),
            predictions=y_pred,
            feature_importance=feat_imp,
            metadata={
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'n_features': X_clean.shape[1],
                'n_samples': len(X_clean),
                'n_classes': len(np.unique(y_clean)),
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
        )
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions on new data"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")
        X_clean, _ = self._prepare_data(X, scale=True)
        return self.model.predict(X_clean)


# ============================================================================
# CLUSTERING MODELS
# ============================================================================

class ClusteringModeler(BaseMLModel):
    """Handles clustering analysis"""
    
    def __init__(self, random_state: int = 42):
        super().__init__(random_state)
        
    def kmeans_clustering(self, X: pd.DataFrame, n_clusters: int = 3,
                         scale: bool = True) -> ClusterResults:
        """Perform K-Means clustering"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('kmeans', "scikit-learn not available")
            
            if len(X) < n_clusters:
                raise InsufficientDataError('kmeans_clustering', n_clusters, len(X))
            
            X_clean, _ = self._prepare_data(X, scale=scale)
            
            # Fit K-Means
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X_clean)
            
            # Calculate silhouette score
            silhouette = silhouette_score(X_clean, labels)
            
            # Cluster sizes
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))
            
            return ClusterResults(
                method='kmeans',
                n_clusters=n_clusters,
                labels=labels,
                silhouette_score=silhouette,
                cluster_sizes=cluster_sizes,
                cluster_centers=kmeans.cluster_centers_,
                metadata={
                    'inertia': kmeans.inertia_,
                    'n_features': X_clean.shape[1],
                    'n_samples': len(X_clean)
                }
            )
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('kmeans', str(e))
    
    def hierarchical_clustering(self, X: pd.DataFrame, n_clusters: int = 3,
                               linkage: str = 'ward', scale: bool = True) -> ClusterResults:
        """Perform hierarchical clustering"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('hierarchical', "scikit-learn not available")
            
            if len(X) < n_clusters:
                raise InsufficientDataError('hierarchical_clustering', n_clusters, len(X))
            
            X_clean, _ = self._prepare_data(X, scale=scale)
            
            # Fit hierarchical clustering
            hc = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
            labels = hc.fit_predict(X_clean)
            
            # Calculate silhouette score
            silhouette = silhouette_score(X_clean, labels)
            
            # Cluster sizes
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))
            
            return ClusterResults(
                method='hierarchical',
                n_clusters=n_clusters,
                labels=labels,
                silhouette_score=silhouette,
                cluster_sizes=cluster_sizes,
                cluster_centers=None,
                metadata={
                    'linkage': linkage,
                    'n_features': X_clean.shape[1],
                    'n_samples': len(X_clean)
                }
            )
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('hierarchical', str(e))
    
    def find_optimal_clusters(self, X: pd.DataFrame, max_clusters: int = 10) -> Dict[int, float]:
        """Find optimal number of clusters using silhouette method"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('find_optimal_clusters', "scikit-learn not available")
            
            if len(X) < 2:
                raise InsufficientDataError('find_optimal_clusters', 2, len(X))
            
            X_clean, _ = self._prepare_data(X, scale=True)
            
            silhouette_scores = {}
            for k in range(2, min(max_clusters + 1, len(X_clean))):
                kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                labels = kmeans.fit_predict(X_clean)
                score = silhouette_score(X_clean, labels)
                silhouette_scores[k] = score
            
            return silhouette_scores
        except (InsufficientDataError, ModelTrainingError):
            raise
        except Exception as e:
            raise ModelTrainingError('find_optimal_clusters', str(e))


# ============================================================================
# TIME SERIES FORECASTING
# ============================================================================

class TimeSeriesForecaster:
    """Enhanced time series forecasting with multiple models"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
    
    def _prepare_ts_data(self, df, target_col, time_col):
        """Prepare and validate time series data (≤10 lines)"""
        ts_data = df[[time_col, target_col]].dropna()
        ts_data = ts_data.groupby(time_col)[target_col].mean().reset_index()
        ts_data = ts_data.sort_values(time_col)
        if len(ts_data) < 3:
            raise InsufficientDataError('timeseries_forecast', 3, len(ts_data))
        X = np.asarray(ts_data[time_col].values).reshape(-1, 1)
        y = np.asarray(ts_data[target_col].values)
        return X, y, ts_data
    
    def _fit_polynomial(self, X, y, degree, periods_ahead):
        """Fit polynomial model and forecast (≤10 lines)"""
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        future_years = np.arange(X.max() + 1, X.max() + 1 + periods_ahead).reshape(-1, 1)
        forecasts = model.predict(poly.transform(future_years))
        return model.predict(X_poly), forecasts, r2_score(y, model.predict(X_poly))
    
    def _fit_sma(self, y, periods_ahead, window=3):
        """Fit Simple Moving Average model (≤10 lines)"""
        try:
            window = min(window, len(y))
            sma = pd.Series(y).rolling(window=window).mean()
            last_val = sma.iloc[-1] if not pd.isna(sma.iloc[-1]) else y[-1]
            forecasts = np.full(periods_ahead, last_val)
            fitted = sma.fillna(method='bfill').values
            return fitted, forecasts, r2_score(y, fitted)
        except Exception as e:
            raise TimeSeriesForecastError('sma', str(e))
    
    def _fit_ewma(self, y, periods_ahead, alpha=0.3):
        """Fit Exponential Weighted Moving Average (≤10 lines)"""
        try:
            ewma = pd.Series(y).ewm(alpha=alpha, adjust=False).mean()
            last_val = ewma.iloc[-1]
            forecasts = np.full(periods_ahead, last_val)
            fitted = ewma.values
            return fitted, forecasts, r2_score(y, fitted)
        except Exception as e:
            raise TimeSeriesForecastError('ewma', str(e))
    
    def _fit_wma(self, y, periods_ahead, window=3):
        """Fit Weighted Moving Average (≤10 lines)"""
        try:
            window = min(window, len(y))
            weights = np.arange(1, window + 1)
            wma = pd.Series(y).rolling(window=window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
            fitted = wma.fillna(method='bfill').values
            forecasts = np.full(periods_ahead, wma.iloc[-1] if not pd.isna(wma.iloc[-1]) else y[-1])
            return fitted, forecasts, r2_score(y, fitted)
        except Exception as e:
            raise TimeSeriesForecastError('wma', str(e))
    
    def _calc_confidence_intervals(self, y, fitted, forecasts, confidence=0.95):
        """Calculate confidence intervals for forecasts (≤10 lines)"""
        try:
            residuals = y - fitted
            std_error = np.std(residuals)
            z_score = 1.96 if confidence == 0.95 else 2.576
            margin = z_score * std_error
            return forecasts - margin, forecasts + margin, std_error
        except Exception as e:
            raise ConfidenceIntervalError(str(e))
    
    def _build_model_result(self, name, fitted, forecasts, r2, X, ci_lower, ci_upper):
        """Build result dictionary for a model (≤10 lines)"""
        forecast_dict = dict(zip(
            np.arange(X.max() + 1, X.max() + 1 + len(forecasts)).flatten().tolist(),
            forecasts.tolist()
        ))
        return {
            'r2_score': r2, 'forecasts': forecast_dict,
            'historical_fit': dict(zip(X.flatten().tolist(), fitted.tolist())),
            'ci_lower': ci_lower.tolist(), 'ci_upper': ci_upper.tolist()
        }
    
    def _train_all_models(self, X, y, periods_ahead):
        """Train all forecasting models (≤10 lines)"""
        results = {}
        for degree in [1, 2, 3]:
            fitted, forecasts, r2 = self._fit_polynomial(X, y, degree, periods_ahead)
            ci_lower, ci_upper, _ = self._calc_confidence_intervals(y, fitted, forecasts)
            results[f'polynomial_degree_{degree}'] = self._build_model_result(
                f'poly_{degree}', fitted, forecasts, r2, X, ci_lower, ci_upper)
        return results
    
    def _train_moving_avg_models(self, y, X, periods_ahead):
        """Train moving average models (≤10 lines)"""
        results = {}
        for name, method in [('sma', self._fit_sma), ('ewma', self._fit_ewma), ('wma', self._fit_wma)]:
            try:
                fitted, forecasts, r2 = method(y, periods_ahead)
                ci_lower, ci_upper, _ = self._calc_confidence_intervals(y, fitted, forecasts)
                results[name] = self._build_model_result(name, fitted, forecasts, r2, X, ci_lower, ci_upper)
            except TimeSeriesForecastError:
                continue
        return results
    
    def _select_best_model(self, all_results):
        """Select best model based on R² score (≤10 lines)"""
        best_name, best_r2 = None, -float('inf')
        for name, result in all_results.items():
            if result.get('r2_score', -float('inf')) > best_r2:
                best_r2 = result['r2_score']
                best_name = name
        return best_name, all_results[best_name] if best_name else {}
    
    def _build_forecast_result(self, best_name, best_result, all_results):
        """Build final forecast result dictionary (≤10 lines)"""
        return {'best_model': best_name, 'forecasts': best_result.get('forecasts', {}),
                'r2_score': best_result.get('r2_score', 0), 'all_models': all_results}
        
    def forecast_trend(self, df: pd.DataFrame, target_col: str,
                      time_col: str = 'Census_Year',
                      periods_ahead: int = 3) -> Dict[str, Any]:
        """Forecast future values using multiple models (≤10 lines)"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('timeseries', "scikit-learn not available")
            X, y, ts_data = self._prepare_ts_data(df, target_col, time_col)
            results = {**self._train_all_models(X, y, periods_ahead), 
                      **self._train_moving_avg_models(y, X, periods_ahead)}
            best_name, best_result = self._select_best_model(results)
            return self._build_forecast_result(best_name, best_result, results)
        except (InsufficientDataError, ModelTrainingError, TimeSeriesForecastError):
            raise
        except Exception as e:
            raise ModelTrainingError('timeseries', str(e))


# ============================================================================
# MODEL COMPARISON
# ============================================================================

class ModelComparator:
    """Compare multiple models and select the best"""
    
    @staticmethod
    def compare_regression_models(X: pd.DataFrame, y: pd.Series) -> Dict[str, ModelResults]:
        """Compare multiple regression models"""
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available'}
            
        modeler = RegressionModeler()
        results = {}
        
        for model_type in ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']:
            try:
                result = modeler.train_model(X, y, model_type=model_type)
                results[model_type] = result
            except Exception as e:
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

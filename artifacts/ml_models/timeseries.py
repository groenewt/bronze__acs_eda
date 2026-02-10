import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from .base import SKLEARN_AVAILABLE
from exceptions import InsufficientDataError, ModelTrainingError, TimeSeriesForecastError, ConfidenceIntervalError


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
            fitted = sma.bfill().values
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
            fitted = wma.bfill().values
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

    def _fit_arima(self, y, X, periods_ahead):
        """Fit ARIMA model using statsmodels"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            # Use simple ARIMA(1,1,1) - can be enhanced with auto-order selection
            model = ARIMA(y, order=(1, 1, 1))
            fit = model.fit()
            forecasts = fit.forecast(steps=periods_ahead)
            fitted = fit.fittedvalues
            # ARIMA drops first observation(s) during differencing
            if len(fitted) < len(y):
                fitted = np.concatenate([[y[0]], fitted])
            r2 = r2_score(y, fitted[:len(y)])
            ci_lower, ci_upper, _ = self._calc_confidence_intervals(y, fitted[:len(y)], forecasts)
            return self._build_model_result('arima', fitted[:len(y)], forecasts, r2, X, ci_lower, ci_upper)
        except Exception as e:
            return {'error': f'ARIMA failed: {str(e)}'}

    def _fit_holt_winters(self, y, X, periods_ahead):
        """Fit Holt-Winters exponential smoothing using statsmodels"""
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            # Use additive trend, no seasonality (annual data typically doesn't have seasonality)
            model = ExponentialSmoothing(y, trend='add', seasonal=None)
            fit = model.fit()
            fitted = fit.fittedvalues
            forecasts = fit.forecast(periods_ahead)
            r2 = r2_score(y, fitted)
            ci_lower, ci_upper, _ = self._calc_confidence_intervals(y, fitted, forecasts)
            return self._build_model_result('holt_winters', fitted, forecasts, r2, X, ci_lower, ci_upper)
        except Exception as e:
            return {'error': f'Holt-Winters failed: {str(e)}'}

    def _train_advanced_models(self, y, X, periods_ahead):
        """Train advanced time series models (ARIMA, Holt-Winters)"""
        results = {}
        for name, method in [('arima', self._fit_arima), ('holt_winters', self._fit_holt_winters)]:
            result = method(y, X, periods_ahead)
            if 'error' not in result:
                results[name] = result
        return results

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
        """Forecast future values using multiple models including ARIMA, Holt-Winters"""
        try:
            if not SKLEARN_AVAILABLE:
                raise ModelTrainingError('timeseries', "scikit-learn not available")
            X, y, ts_data = self._prepare_ts_data(df, target_col, time_col)
            results = {**self._train_all_models(X, y, periods_ahead),
                      **self._train_moving_avg_models(y, X, periods_ahead),
                      **self._train_advanced_models(y, X, periods_ahead)}
            best_name, best_result = self._select_best_model(results)
            return self._build_forecast_result(best_name, best_result, results)
        except (InsufficientDataError, ModelTrainingError, TimeSeriesForecastError):
            raise
        except Exception as e:
            raise ModelTrainingError('timeseries', str(e))

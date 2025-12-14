"""Time Series Visualizations"""
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer
from exceptions import PlotCreationError
from logging_config import get_logger

logger = get_logger("visualizations.ml.timeseries")


class TimeSeriesVisualizer(BaseMLVisualizer):
    """Visualizes time series model results"""

    def viz_timeseries(self, result, df, target_col):
        """Generate all time series visualizations (≤10 lines)"""
        self.target_name = target_col
        self.current_target = target_col  # Set for directory path (supervised learning)
        self.ts_method = result.get('model_name', result.get('method', 'polynomial'))
        self._forecast(result, df, target_col)
        self._ts_residuals(result, df, target_col)
        self._ts_trend_decomposition(df, target_col)
        self._ts_accuracy_metrics(result, df, target_col)
        self._ts_confidence_intervals(result, df, target_col)

    def _prep_forecast_data(self, df, col):
        """Prepare aggregated time series data (≤10 lines)"""
        if 'Census_Year' not in df.columns or col not in df.columns:
            return None
        df_agg = df.groupby('Census_Year')[col].mean().reset_index()
        df_agg = df_agg.sort_values('Census_Year')
        return df_agg if len(df_agg) > 0 else None

    def _plot_forecast_lines(self, df_agg, col, forecast_vals, ci_lower=None, ci_upper=None):
        """Plot historical and forecast lines with CI bands (≤10 lines)"""
        # Calculate historical std for uncertainty band
        hist_mean = df_agg[col].mean()
        hist_std = df_agg[col].std()
        hist_upper = df_agg[col] + hist_std
        hist_lower = df_agg[col] - hist_std

        # Plot historical std band (light blue)
        plt.fill_between(df_agg['Census_Year'], hist_lower, hist_upper,
                        alpha=0.15, color='#87CEEB', label='Historical ±1σ')

        # Plot historical data line (EXPLICIT BLUE)
        plt.plot(df_agg['Census_Year'], df_agg[col], marker='o', label='Historical Data',
                linewidth=2.5, color='#1f77b4', markersize=6, markerfacecolor='#1f77b4', markeredgecolor='darkblue')
        logger.debug(f"[VIZ] Forecast values: {forecast_vals}, CI_lower: {ci_lower}, CI_upper: {ci_upper}")

        if forecast_vals and len(forecast_vals) > 0:
            # Get last historical point for seamless connection
            max_yr = df_agg['Census_Year'].max()
            last_val = df_agg[df_agg['Census_Year'] == max_yr][col].iloc[0]

            # Create forecast years and prepend last historical year for connection
            forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
            forecast_yrs_connected = [int(max_yr)] + forecast_yrs
            forecast_vals_connected = [last_val] + list(forecast_vals)

            # Plot forecast connected to last historical point (EXPLICIT ORANGE/RED)
            plt.plot(forecast_yrs_connected, forecast_vals_connected, marker='s',
                    label='Forecast', linewidth=2.5, linestyle='--', color='#ff7f0e',
                    markersize=7, markerfacecolor='#ff7f0e', markeredgecolor='darkorange')

            # Plot forecast CI bands if available (orange/red to contrast with blue historical)
            if ci_lower and ci_upper and len(ci_lower) == len(forecast_vals) and len(ci_upper) == len(forecast_vals):
                ci_lower_connected = [last_val] + list(ci_lower)
                ci_upper_connected = [last_val] + list(ci_upper)
                plt.fill_between(forecast_yrs_connected, ci_lower_connected, ci_upper_connected,
                                alpha=0.25, color='#ff7f0e', label='Forecast 95% CI')
                logger.debug(f"[VIZ] Plotted CI bands: lower={ci_lower_connected}, upper={ci_upper_connected}")
            else:
                logger.debug(f"[VIZ] CI not plotted - ci_lower len: {len(ci_lower) if ci_lower else 0}, ci_upper len: {len(ci_upper) if ci_upper else 0}, forecast len: {len(forecast_vals)}")

    def _finalize_forecast_plot(self, col, model_name=''):
        """Finalize forecast plot (≤10 lines)"""
        plt.xlabel('Year')
        plt.ylabel(f'{col}')
        # Include target name and model name in title
        title = f'Time Series Forecast - {col}'
        if model_name:
            title += f' ({model_name})'
        plt.title(title, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()

    def _forecast(self, r, df, col):
        """Visualize forecast with historical data and CI (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None:
                return
            plt.figure(figsize=(12, 6))
            forecast_vals = r.get('forecast_values', [])
            ci_lower = r.get('ci_lower', [])
            ci_upper = r.get('ci_upper', [])
            model_name = r.get('model_name', r.get('best_model', ''))
            self._plot_forecast_lines(df_agg, col, forecast_vals, ci_lower, ci_upper)
            self._finalize_forecast_plot(col, model_name)
            self._save('forecast.png', 'time_series', self.ts_method)
        except Exception as e:
            logger.warning(f"[VIZ] Time series forecast visualization failed: {e}")

    def _calc_ts_residuals(self, df_sorted, col):
        """Calculate time series residuals (≤10 lines)"""
        window = min(3, len(df_sorted))
        ma = df_sorted[col].rolling(window=window, center=True).mean()
        return df_sorted[col] - ma

    def _plot_residuals_scatter(self, df_agg, residuals, col):
        """Plot residuals scatter (≤10 lines)"""
        plt.scatter(df_agg['Census_Year'], residuals, alpha=0.6, s=50)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Year')
        plt.ylabel('Residuals')
        plt.title(f'Time Series Residuals - {col}', fontweight='bold')
        plt.grid(alpha=0.3)

    def _ts_residuals(self, r, df, col):
        """Visualize time series residuals (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 3:
                return
            residuals = self._calc_ts_residuals(df_agg, col)
            plt.figure(figsize=(12, 6))
            self._plot_residuals_scatter(df_agg, residuals, col)
            self._save('residuals.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_residuals', str(e))

    def _plot_decomp_original(self, ax, df_sorted, col):
        """Plot original series (≤10 lines)"""
        ax.plot(df_sorted['Census_Year'], df_sorted[col], marker='o', linewidth=2)
        ax.set_ylabel(col)
        ax.set_title(f'Original Series - {col}', fontweight='bold')
        ax.grid(alpha=0.3)

    def _plot_decomp_trend(self, ax, df_sorted, col):
        """Plot trend component (≤10 lines)"""
        window = min(3, len(df_sorted))
        trend = df_sorted[col].rolling(window=window, center=True).mean()
        ax.plot(df_sorted['Census_Year'], trend, marker='o', linewidth=2, color='orange')
        ax.set_ylabel('Trend')
        ax.set_title('Trend Component', fontweight='bold')
        ax.grid(alpha=0.3)
        return trend

    def _plot_decomp_residual(self, ax, df_sorted, col, trend):
        """Plot residual component (≤10 lines)"""
        residual = df_sorted[col] - trend
        ax.plot(df_sorted['Census_Year'], residual, marker='o', linewidth=2, color='green')
        ax.axhline(y=0, color='r', linestyle='--', lw=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Residual')
        ax.set_title('Residual Component', fontweight='bold')
        ax.grid(alpha=0.3)

    def _plot_all_decomp(self, axes, df_agg, col):
        """Plot all decomposition components (≤10 lines)"""
        self._plot_decomp_original(axes[0], df_agg, col)
        trend = self._plot_decomp_trend(axes[1], df_agg, col)
        self._plot_decomp_residual(axes[2], df_agg, col, trend)

    def _ts_trend_decomposition(self, df, col):
        """Visualize trend decomposition (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 4:
                return
            fig, axes = plt.subplots(3, 1, figsize=(12, 10))
            self._plot_all_decomp(axes, df_agg, col)
            plt.tight_layout()
            self._save('trend_decomposition.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_trend_decomposition', str(e))

    def _plot_yoy_change(self, ax, df_sorted, col):
        """Plot year-over-year change (≤10 lines)"""
        yoy_change = df_sorted[col].pct_change() * 100
        ax.plot(df_sorted['Census_Year'].iloc[1:], yoy_change.iloc[1:],
                marker='o', linewidth=2, color='purple')
        ax.axhline(y=0, color='r', linestyle='--', lw=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('YoY Change (%)')
        ax.set_title(f'Year-over-Year Change - {col}', fontweight='bold')
        ax.grid(alpha=0.3)

    def _plot_forecast_bars(self, ax, df_sorted, col, forecast_vals):
        """Plot forecast values as bars (≤10 lines)"""
        if len(forecast_vals) == 0:
            return False
        max_yr = df_sorted['Census_Year'].max()
        forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
        ax.bar(forecast_yrs, forecast_vals, alpha=0.7, color='coral', edgecolor='black')
        ax.set_xlabel('Forecast Year')
        ax.set_ylabel(col)
        ax.set_title(f'Forecasted Values - {col}', fontweight='bold')
        ax.grid(alpha=0.3, axis='y')
        return True

    def _ts_accuracy_metrics(self, r, df, col):
        """Visualize forecast accuracy metrics (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 2:
                return
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            self._plot_yoy_change(axes[0], df_agg, col)
            self._plot_forecast_bars(axes[1], df_agg, col, r.get('forecast_values', []))
            plt.tight_layout()
            self._save('accuracy_metrics.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_accuracy_metrics', str(e))

    def _get_ci_data(self, r):
        """Extract confidence interval data from result (≤10 lines)"""
        forecast_vals = r.get('forecast_values', [])
        ci_lower = r.get('ci_lower', [])
        ci_upper = r.get('ci_upper', [])
        if not forecast_vals or not ci_lower or not ci_upper:
            return None, None, None
        return forecast_vals, ci_lower, ci_upper

    def _plot_ci_bands(self, df_agg, col, forecast_vals, ci_lower, ci_upper):
        """Plot confidence interval bands (≤10 lines)"""
        # Plot historical data
        plt.plot(df_agg['Census_Year'], df_agg[col], marker='o', label='Historical', linewidth=2)

        # Get last historical point for connection
        max_yr = df_agg['Census_Year'].max()
        last_val = df_agg[df_agg['Census_Year'] == max_yr][col].iloc[0]

        # Create forecast years and prepend last historical year for connection
        forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
        forecast_yrs_connected = [int(max_yr)] + forecast_yrs
        forecast_vals_connected = [last_val] + list(forecast_vals)
        ci_lower_connected = [last_val] + list(ci_lower)
        ci_upper_connected = [last_val] + list(ci_upper)

        # Plot forecast line connected to last historical point
        plt.plot(forecast_yrs_connected, forecast_vals_connected, marker='s',
                label='Forecast', linewidth=2, linestyle='--', color='red')

        # Fill confidence interval connected to last historical point
        plt.fill_between(forecast_yrs_connected, ci_lower_connected, ci_upper_connected,
                        alpha=0.2, color='red', label='95% CI')

    def _finalize_ci_plot(self, col):
        """Finalize confidence interval plot (≤10 lines)"""
        plt.xlabel('Year')
        plt.ylabel(col)
        plt.title(f'Forecast with Confidence Intervals - {col}', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()

    def _ts_confidence_intervals(self, r, df, col):
        """Visualize forecast with confidence intervals (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            forecast_vals, ci_lower, ci_upper = self._get_ci_data(r)
            if df_agg is None or forecast_vals is None:
                return
            plt.figure(figsize=(12, 6))
            self._plot_ci_bands(df_agg, col, forecast_vals, ci_lower, ci_upper)
            self._finalize_ci_plot(col)
            self._save('confidence_intervals.png', 'time_series', self.ts_method)
        except Exception as e:
            logger.warning(f"[VIZ] Confidence interval visualization failed: {e}")

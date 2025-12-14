"""Outlier detection and year-over-year change visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
from logging_config import get_logger

logger = get_logger("visualization.outlier")

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class YoYChangeVisualizer(BaseVisualizer):
    """Visualizes year-over-year changes and trends"""

    def create_all(self):
        self._apply_housing_sampling()
        self._yoy_change_plot()
        self._growth_rate_heatmap()

    def _yoy_change_plot(self):
        """Create year-over-year percentage change visualization"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_yoy, 'yoy_change')

    def _plot_yoy(self, ax, col: str):
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly_median = numeric_col.groupby(df_filtered['Census_Year']).median().astype(float).sort_index()
        if len(yearly_median) > 1:
            yoy_change = yearly_median.pct_change() * 100
            yoy_change_clean = yoy_change.dropna()
            if len(yoy_change_clean) > 0:
                colors = ['green' if x > 0 else 'red' for x in yoy_change_clean.values]
                ax.bar(yoy_change_clean.index, yoy_change_clean.values, color=colors, alpha=0.7, edgecolor='black')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax.set_title(f'{col} - Year-over-Year % Change', fontweight='bold')
            ax.set_xlabel('Year')
            ax.set_ylabel('% Change')
            ax.grid(alpha=0.3, axis='y')
            ax.tick_params(axis='x', rotation=45)

    def _growth_rate_heatmap(self):
        """Create heatmap of growth rates across variables and years"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return

        # Calculate YoY changes for all key columns
        growth_matrix = []
        years = sorted(self.df['Census_Year'].dropna().unique())

        for col in key_cols:  # key_cols[:8] <<removed
            numeric_col = pd.to_numeric(self.df[col], errors='coerce')
            if self._should_exclude_zeros(col):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly_median = numeric_col.groupby(df_filtered['Census_Year']).median().astype(float).sort_index()
            yoy_change = yearly_median.pct_change() * 100
            growth_matrix.append(yoy_change.values)

        if growth_matrix:
            growth_df = pd.DataFrame(growth_matrix,
                                    index=[c.replace('_', ' ')[:20] for c in key_cols[:len(growth_matrix)]],
                                    columns=[str(int(y)) for y in years])

            # Convert to float to handle pd.NA (NAType) for seaborn compatibility
            growth_df = growth_df.astype(float)

            # Check if dataframe has valid data before plotting
            if growth_df.empty or growth_df.shape[0] == 0 or growth_df.shape[1] == 0:
                logger.verbose("Skipping growth rate heatmap: no valid data")
                return

            plt.figure(figsize=(12, 8))
            sns.heatmap(growth_df, annot=True, fmt='.1f', cmap='RdYlGn',
                       center=0, cbar_kws={'label': '% Change'}, linewidths=0.5)
            plt.title('Year-over-Year Growth Rate Heatmap (%)', fontweight='bold', fontsize=14)
            plt.xlabel('Year')
            plt.ylabel('Variable')
            tight_layout_safe()
            self._save_fig('growth_rate_heatmap.png')

    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization (expanded keywords)"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours', 'Earnings', 'Cost',
                    'Tax', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Person', 'Poverty']
        return [c for c in valuable if any(k in c for k in keywords)][:12]


class OutlierVisualizer(BaseVisualizer):
    """Visualizes outliers and anomalies"""

    def create_all(self):
        self._apply_housing_sampling()
        self._outlier_detection_plot()
        self._temporal_anomalies()

    def _outlier_detection_plot(self):
        """Create visualization of outliers using IQR method"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols:
            return
        self._chunk_plot(key_cols, self._plot_outlier, 'outlier_detection')

    def _plot_outlier(self, ax, col: str):
        data = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        if len(data) > 0:
            Q1, Q3 = data.quantile(0.25), data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound, upper_bound = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            normal = data[(data >= lower_bound) & (data <= upper_bound)]
            ax.scatter(range(len(normal)), sorted(normal.values),
                      alpha=0.5, s=10, color='steelblue', label='Normal')
            if len(outliers) > 0:
                ax.scatter(range(len(normal), len(normal) + len(outliers)),
                          sorted(outliers.values),
                          alpha=0.7, s=30, color='red', marker='x', label='Outliers')
            ax.axhline(y=lower_bound, color='orange', linestyle='--',
                      linewidth=1, label=f'Lower bound: {lower_bound:,.0f}')
            ax.axhline(y=upper_bound, color='orange', linestyle='--',
                      linewidth=1, label=f'Upper bound: {upper_bound:,.0f}')
            ax.set_title(f'{col} - Outlier Detection (IQR Method)', fontweight='bold')
            ax.set_xlabel('Index (sorted)')
            ax.set_ylabel(col)
            ax.legend(fontsize=8, loc='upper left')
            ax.grid(alpha=0.3)
            outlier_pct = len(outliers) / len(data) * 100
            ax.text(0.98, 0.5, f'Outliers: {len(outliers):,}\n({outlier_pct:.1f}%)',
                   transform=ax.transAxes, verticalalignment='center',
                   horizontalalignment='right', bbox=dict(boxstyle='round',
                   facecolor='lightyellow', alpha=0.8), fontsize=9)

    def _temporal_anomalies(self):
        """Detect and visualize temporal anomalies"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_anomaly, 'temporal_anomalies')

    def _plot_anomaly(self, ax, col: str):
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly_stats = numeric_col.groupby(df_filtered['Census_Year']).agg(['median', 'std']).astype(float).sort_index()
        if len(yearly_stats) > 2:
            ma = yearly_stats['median'].rolling(window=3, center=True).mean()
            std_dev = yearly_stats['median'].std()
            anomalies = []
            for year in yearly_stats.index:
                if pd.notna(ma.loc[year]):
                    if abs(yearly_stats.loc[year, 'median'] - ma.loc[year]) > 1.5 * std_dev:
                        anomalies.append(year)
            ax.plot(yearly_stats.index, yearly_stats['median'],
                   marker='o', linewidth=2, label='Actual', color='steelblue')
            ax.plot(ma.index, ma.values, linestyle='--', linewidth=2,
                   label='Moving Avg', color='green', alpha=0.7)
            if anomalies:
                anomaly_vals = [yearly_stats.loc[y, 'median'] for y in anomalies]
                ax.scatter(anomalies, anomaly_vals, color='red', s=100,
                         marker='X', label='Anomalies', zorder=5)
            ax.set_title(f'{col} - Temporal Anomaly Detection', fontweight='bold')
            ax.set_xlabel('Year')
            ax.set_ylabel('Median Value')
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)

    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization (expanded keywords)"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Tax', 'Age', 'Hours',
                    'Earnings', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Person', 'Poverty']
        return [c for c in valuable if any(k in c for k in keywords)][:12]

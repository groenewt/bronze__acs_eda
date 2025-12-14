"""Temporal visualizations for time-series analysis"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from logging_config import get_logger

logger = get_logger("visualization.temporal")

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class TemporalVisualizer(BaseVisualizer):
    """Visualizes temporal trends"""

    def create_all(self):
        self._apply_housing_sampling()
        try:
            self._sample_size_trend()
        except Exception as e:
            logger.warning(f"Sample size trend plot failed: {e}")
        try:
            self._year_distribution()
        except Exception as e:
            logger.warning(f"Year distribution plot failed: {e}")
        try:
            self._temporal_comparison()
        except Exception as e:
            logger.warning(f"Temporal comparison plot failed: {e}")

    def _sample_size_trend(self):
        plt.figure(figsize=(10, 6))
        self._plot_sample_counts()
        tight_layout_safe()
        self._save_fig('sample_size_trend.png')

    def _plot_sample_counts(self):
        logger.verbose(f"_plot_sample_counts: df.shape={self.df.shape}")
        logger.verbose(f"'Census_Year' in columns: {'Census_Year' in self.df.columns}")
        if 'Census_Year' not in self.df.columns:
            logger.warning("Census_Year column missing - skipping plot")
            return
        counts = self.df['Census_Year'].value_counts().sort_index()
        logger.verbose(f"Census_Year counts: {len(counts)} unique years, total records: {counts.sum()}")
        logger.verbose(f"Year range: {counts.index.min() if len(counts) > 0 else 'N/A'} to {counts.index.max() if len(counts) > 0 else 'N/A'}")
        plt.plot(counts.index, counts.values, marker='o', linewidth=2, color='steelblue')
        plt.title('Sample Size Over Time', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Records')
        plt.grid(alpha=0.3)

    def _year_distribution(self):
        logger.verbose(f"_year_distribution: df.shape={self.df.shape}")
        if 'Census_Year' not in self.df.columns:
            logger.warning("Census_Year column missing - skipping plot")
            return
        plt.figure(figsize=(12, 6))
        counts = self.df['Census_Year'].value_counts().sort_index()
        logger.verbose(f"Year distribution: {dict(counts)}")
        plt.bar(counts.index, counts.values, color='steelblue', edgecolor='black')
        plt.title('Records by Census Year', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        tight_layout_safe()
        self._save_fig('year_distribution.png')

    def _temporal_comparison(self):
        logger.verbose(f"_temporal_comparison: df.shape={self.df.shape}")
        numeric_cols = self._get_key_numeric_cols()
        logger.verbose(f"Key numeric columns found: {numeric_cols}")
        if not numeric_cols:
            logger.warning("No key numeric columns found - skipping plot")
            return
        self._chunk_plot(numeric_cols, self._plot_metric_trend, 'temporal_comparison')

    def _get_key_numeric_cols(self) -> List[str]:
        numeric = self.df.select_dtypes(include=[np.number]).columns
        logger.verbose(f"_get_key_numeric_cols: {len(numeric)} numeric columns total")
        logger.verbose(f"Numeric columns: {list(numeric)[:20]}...")  # Show first 20
        # Expanded keywords for better column coverage
        keywords = ['Age', 'Income', 'Poverty', 'Hours', 'Value', 'Rent', 'Wage',
                    'Earnings', 'Security', 'Retirement', 'Travel', 'Week', 'Cost',
                    'Electricity', 'Gas', 'Water', 'Fuel', 'Tax', 'Person']
        # Filter out flag/weight columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        matched = [c for c in valuable if any(k in c for k in keywords)][:12]
        logger.verbose(f"Matched key columns: {matched}")
        return matched

    def _plot_metric_trend(self, ax, col: str):
        logger.verbose(f"_plot_metric_trend for column '{col}'")
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        # Filter zeros if needed
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        non_null = numeric_col.notna().sum()
        logger.verbose(f"Column '{col}': {non_null} non-null values (zeros excluded if needed)")
        if non_null > 0:
            logger.verbose(f"Value range: {numeric_col.min():.2f} to {numeric_col.max():.2f}")
        yearly = numeric_col.groupby(df_filtered['Census_Year']).agg(['mean', 'median']).astype(float)
        yearly.plot(ax=ax, marker='o')
        ax.set_title(f'{col} Over Time', fontweight='bold')
        ax.set_xlabel('Year')
        ax.legend(['Mean', 'Median'])
        ax.grid(alpha=0.3)

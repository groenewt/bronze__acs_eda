"""Correlation visualizations for relationships between variables"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class CorrelationVisualizer(BaseVisualizer):
    """Visualizes correlations and relationships"""

    def create_all(self):
        self._apply_housing_sampling()
        print("[VERBOSE] Creating correlation heatmap...")
        self._correlation_heatmap()
        print("[VERBOSE] Creating scatter matrix...")
        self._scatter_matrix()

    def _correlation_heatmap(self):
        key_cols = self._get_key_columns()
        if len(key_cols) < 2:
            return
        plt.figure(figsize=(12, 10))
        # Filter zeros for each column before correlation
        df_filtered = self.df[key_cols].copy()
        for col in key_cols:
            if self._should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        corr = df_filtered.corr()
        # Convert to float to handle pd.NA (NAType) for seaborn compatibility
        corr = corr.astype(float)
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, square=True, linewidths=1)
        plt.title('Correlation Heatmap - Key Variables', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('correlation_heatmap.png')

    def _get_key_columns(self) -> List[str]:
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Value', 'Rent', 'Age', 'Hours', 'Wage', 'Earnings',
                    'Cost', 'Tax', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Person', 'Poverty']
        return [c for c in valuable if any(k in c for k in keywords)][:10]

    def _scatter_matrix(self):
        key_cols = self._get_key_columns()[:8]
        if len(key_cols) < 2:
            print(f"[VERBOSE] Skipping scatter matrix: insufficient key columns (found {len(key_cols)})")
            return

        # Apply same zero-filtering as heatmap BEFORE dropna()
        df_filtered = self.df[key_cols].copy()
        for col in key_cols:
            if self._should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan

        # Now dropna() removes both NaN and converted zeros
        df_subset = df_filtered.dropna()
        if len(df_subset) == 0:
            print(f"[VERBOSE] Skipping scatter matrix: no valid data after removing NaN/zero values")
            return

        # Check if columns have any variance
        for col in key_cols:
            if df_subset[col].nunique() <= 1:
                print(f"[VERBOSE] Skipping scatter matrix: column '{col}' has no variance")
                return

        print(f"[VERBOSE] Creating scatter matrix with columns: {key_cols}")
        pd.plotting.scatter_matrix(df_subset, figsize=(12, 12),
                                  diagonal='hist', alpha=0.5)
        plt.suptitle('Scatter Matrix - Key Variables', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('scatter_matrix.png')

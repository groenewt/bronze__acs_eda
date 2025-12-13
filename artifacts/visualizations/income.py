"""Income composition and sources visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class IncomeCompositionVisualizer(BaseVisualizer):
    """Visualizes income sources and composition"""

    def create_all(self):
        self._apply_housing_sampling()
        self._income_sources_stacked()
        self._income_by_source()

    def _income_sources_stacked(self):
        income_cols = ['Wage_Income', 'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
                      'Social_Security_Income', 'Retirement_Income', 'Public_Assistance_Income', 'Other_Income']
        available = [c for c in income_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(14, 7))
        # Filter zeros for each income column
        df_filtered = self.df.copy()
        for col in available:
            if self._should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        yearly_income = df_filtered.groupby('Census_Year')[available].mean()
        yearly_income.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
        ax.set_title('Income Sources Over Time (Stacked)', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Average Income ($)')
        ax.legend(title='Income Type', bbox_to_anchor=(1.05, 1), fontsize=9)
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('income_sources_stacked.png')

    def _income_by_source(self):
        income_cols = ['Wage_Income', 'Self_Employment_Income', 'Social_Security_Income',
                      'Retirement_Income', 'Public_Assistance_Income']
        available = [c for c in income_cols if c in self.df.columns]
        if not available:
            return
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        for idx, col in enumerate(available[:6]):
            ax = axes[idx]
            data = self.df[col].dropna()
            if self._should_exclude_zeros(col):
                data = data[data > 0]
            if len(data) > 0:
                ax.hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
                ax.set_title(col.replace('_', ' '), fontweight='bold')
                ax.set_xlabel('Amount ($)')
                ax.set_ylabel('Frequency')
                ax.grid(alpha=0.3, axis='y')
        for idx in range(len(available), 6):
            axes[idx].axis('off')
        tight_layout_safe()
        self._save_fig('income_by_source.png')

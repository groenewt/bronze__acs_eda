"""Distribution comparison visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe
from memory_utils import adaptive_sample
from logging_config import get_logger

logger = get_logger("visualization.distributions")


class DistributionComparisonVisualizer(BaseVisualizer):
    """Compare distributions across different dimensions"""

    def create_all(self):
        # Memory-aware sampling for both HOUSING and POPULATION
        self.df = adaptive_sample(self.df, survey_type=self.survey_type)
        self._temporal_distributions()
        self._density_overlays()
        self._bivariate_kde_plots()

    def _temporal_distributions(self):
        try:
            if 'Census_Year' not in self.df.columns:
                return
            numeric_cols = self._get_key_numeric_cols()[:3]
            if not numeric_cols:
                return
            years = sorted(self.df['Census_Year'].unique())
            if len(years) == 0:
                return

            # Use up to 3 years
            years_to_plot = years[:min(3, len(years))]
            num_cols = len(numeric_cols)

            fig, axes = plt.subplots(1, num_cols, figsize=(15, 5))
            # Handle single subplot case
            if num_cols == 1:
                axes = [axes]

            for idx, col in enumerate(numeric_cols):
                for year in years_to_plot:
                    data = self.df[self.df['Census_Year'] == year][col].dropna()
                    # Filter zeros if needed
                    if self._should_exclude_zeros(col):
                        data = data[data > 0]
                    if len(data) > 10:  # Need enough data for histogram
                        axes[idx].hist(data, alpha=0.5, bins=20, label=str(year))
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
                axes[idx].legend()
                axes[idx].grid(alpha=0.3)

            tight_layout_safe()
            self._save_fig('temporal_distributions')
        except Exception as e:
            logger.warning(f"Temporal distributions failed: {e}")

    def _density_overlays(self):
        try:
            numeric_cols = self._get_key_numeric_cols()[:8]
            if not numeric_cols:
                return

            plt.figure(figsize=(12, 6))
            plotted = False
            for col in numeric_cols:
                data = self.df[col].dropna()
                if self._should_exclude_zeros(col):
                    data = data[data > 0]
                if len(data) > 10:  # Need enough data for density plot
                    try:
                        data.plot(kind='density', alpha=0.6, label=col)
                        plotted = True
                    except Exception:
                        continue

            if plotted:
                plt.xlabel('Value')
                plt.ylabel('Density')
                plt.title('Density Overlays', fontweight='bold')
                plt.legend()
                plt.grid(alpha=0.3)
                tight_layout_safe()
                self._save_fig('density_overlays')
            else:
                plt.close()
        except Exception as e:
            logger.warning(f"Density overlays failed: {e}")

    def _get_key_numeric_cols(self):
        numeric = self.df.select_dtypes(include=[np.number]).columns
        # Filter out flag/weight columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate',
                   'SERIALNO', 'PUMA', 'ST', 'Specified_']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours', 'Earnings', 'Cost',
                    'Tax', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Person', 'Poverty']
        matched = [c for c in valuable if any(k in c for k in keywords)]
        return matched[:15] if matched else valuable[:15]

    def _bivariate_kde_plots(self):
        """Create bivariate KDE plots for key variable pairs"""
        pairs = [
            ('Total_Person_Income', 'Property_Value'),
            ('Total_Person_Income', 'Gross_Rent'),
            ('Total_Person_Income', 'Age'),
        ]

        for col1, col2 in pairs:
            if col1 in self.df.columns and col2 in self.df.columns:
                self._bivariate_kde(col1, col2)

    def _bivariate_kde(self, col1, col2):
        """
        Create bivariate KDE plot showing joint distribution of two variables.

        Args:
            col1: First column name
            col2: Second column name
        """
        try:
            import seaborn as sns

            # Get data and drop NaNs
            data = self.df[[col1, col2]].dropna()

            # Filter zeros for income/property columns if needed
            if self._should_exclude_zeros(col1):
                data = data[data[col1] > 0]
            if self._should_exclude_zeros(col2):
                data = data[data[col2] > 0]

            if len(data) < 100:
                logger.warning(f"Not enough data for bivariate KDE: {col1} vs {col2} ({len(data)} points)")
                return

            # Sample for performance if needed
            if len(data) > 5000:
                data = data.sample(5000, random_state=42)

            plt.figure(figsize=(10, 8))

            # Create KDE plot with contours
            sns.kdeplot(
                data=data,
                x=col1,
                y=col2,
                cmap='Blues',
                fill=True,
                levels=10,
                alpha=0.6
            )

            # Add scatter plot overlay for reference
            if len(data) <= 1000:
                plt.scatter(data[col1], data[col2], alpha=0.1, s=10, color='darkblue')

            plt.xlabel(col1, fontweight='bold')
            plt.ylabel(col2, fontweight='bold')
            plt.title(f'Joint Distribution: {col1} vs {col2}', fontweight='bold', fontsize=14)
            plt.grid(True, alpha=0.3)

            # Format filename
            filename = f'kde_{col1.lower()}_{col2.lower()}.png'
            self._save_fig(filename)

        except Exception as e:
            logger.warning(f"Bivariate KDE failed for {col1} vs {col2}: {e}")

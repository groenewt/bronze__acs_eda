"""Inequality visualizations: Lorenz curves, Gini coefficients, and distributional analysis"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe, auto_log_scale
from logging_config import get_logger

logger = get_logger("visualization.inequality")


class InequalityVisualizer(BaseVisualizer):
    """Visualizes income and wealth inequality patterns"""

    def create_all(self):
        self._apply_housing_sampling()

        # Determine available columns
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else None
        property_col = 'Property_Value' if 'Property_Value' in self.df.columns else None

        # Create visualizations
        try:
            if income_col:
                self._lorenz_curve(income_col)
        except Exception as e:
            logger.warning(f"Lorenz curve (income) failed: {e}")

        try:
            if property_col:
                self._lorenz_curve(property_col)
        except Exception as e:
            logger.warning(f"Lorenz curve (property) failed: {e}")

        try:
            self._gini_trends()
        except Exception as e:
            logger.warning(f"Gini trends failed: {e}")

        try:
            self._gini_by_demographics()
        except Exception as e:
            logger.warning(f"Gini by demographics failed: {e}")

        try:
            self._inequality_heatmaps()
        except Exception as e:
            logger.warning(f"Inequality heatmaps failed: {e}")

        try:
            self._percentile_divergence()
        except Exception as e:
            logger.warning(f"Percentile divergence failed: {e}")

        try:
            self._percentile_gap()
        except Exception as e:
            logger.warning(f"Percentile gap analysis failed: {e}")

    def _calculate_gini(self, values: np.ndarray) -> float:
        """Calculate Gini coefficient from array of values.

        Args:
            values: Array of numeric values (income, property values, etc.)

        Returns:
            Gini coefficient (0 = perfect equality, 1 = perfect inequality)
        """
        # Remove NaN values and filter positive values
        values = values[~np.isnan(values)]
        values = values[values > 0]

        if len(values) < 2:
            return np.nan

        # Sort values
        values = np.sort(values)
        n = len(values)
        cumsum = np.cumsum(values)

        # Calculate Gini coefficient
        gini = (2 * np.sum((np.arange(1, n + 1) * values)) - (n + 1) * cumsum[-1]) / (n * cumsum[-1])
        return gini

    def _lorenz_curve(self, col: str):
        """Create Lorenz curve with Gini coefficient annotation.

        Args:
            col: Column name for which to calculate Lorenz curve
        """
        if col not in self.df.columns:
            return

        # Get data and filter
        data = pd.to_numeric(self.df[col], errors='coerce')

        if self._should_exclude_zeros(col):
            data = data[data > 0]

        data = data.dropna()

        if len(data) < 10:
            logger.warning(f"Insufficient data for Lorenz curve: {col}")
            return

        # Sort values and calculate cumulative proportions
        sorted_values = np.sort(data.values)
        n = len(sorted_values)
        cumsum = np.cumsum(sorted_values)

        # Calculate Lorenz curve coordinates
        x_lorenz = np.linspace(0, 1, n)
        y_lorenz = cumsum / cumsum[-1]

        # Calculate Gini coefficient
        gini = self._calculate_gini(sorted_values)

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot equality line (45-degree line)
        ax.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Perfect Equality', alpha=0.7)

        # Plot Lorenz curve
        ax.plot(x_lorenz, y_lorenz, 'b-', linewidth=2.5, label='Lorenz Curve')

        # Shade area between curves (represents inequality)
        ax.fill_between(x_lorenz, y_lorenz, x_lorenz, alpha=0.3, color='red',
                        label=f'Inequality Area')

        # Add Gini coefficient annotation
        if not np.isnan(gini):
            ax.text(0.6, 0.2, f'Gini Coefficient: {gini:.4f}',
                   fontsize=14, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # Configure axes
        configure_axes(ax,
                      title=f'Lorenz Curve: {col}',
                      xlabel='Cumulative Population Proportion',
                      ylabel='Cumulative Income Proportion',
                      grid=True)

        ax.legend(loc='upper left', fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        tight_layout_safe()
        self._save_fig(f'lorenz_curve_{col}.png')

    def _gini_trends(self):
        """Plot Gini coefficient trends over time for available income/value columns."""
        # Find relevant columns
        gini_cols = []
        if 'Total_Person_Income' in self.df.columns:
            gini_cols.append('Total_Person_Income')
        if 'Property_Value' in self.df.columns:
            gini_cols.append('Property_Value')
        if 'Household_Income' in self.df.columns:
            gini_cols.append('Household_Income')

        if not gini_cols or 'Census_Year' not in self.df.columns:
            return

        fig, ax = plt.subplots(figsize=(12, 7))

        for col in gini_cols:
            # Calculate Gini coefficient by year
            gini_by_year = []
            years = []

            for year in sorted(self.df['Census_Year'].unique()):
                year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col], errors='coerce')

                if self._should_exclude_zeros(col):
                    year_data = year_data[year_data > 0]

                year_data = year_data.dropna()

                if len(year_data) >= 10:
                    gini = self._calculate_gini(year_data.values)
                    if not np.isnan(gini):
                        gini_by_year.append(gini)
                        years.append(year)

            if len(years) > 0:
                ax.plot(years, gini_by_year, marker='o', linewidth=2.5, label=col, markersize=8)

        configure_axes(ax,
                      title='Gini Coefficient Trends Over Time',
                      xlabel='Census Year',
                      ylabel='Gini Coefficient',
                      grid=True)

        ax.legend(loc='best', fontsize=10)
        ax.set_ylim(0, 1)

        tight_layout_safe()
        self._save_fig('gini_trends.png')

    def _gini_by_demographics(self):
        """Calculate and visualize Gini coefficients by demographic groups."""
        if 'Total_Person_Income' not in self.df.columns:
            return

        # Create age groups if not present
        df_work = self.df.copy()
        if 'Age_Group' not in df_work.columns and 'Age' in df_work.columns:
            age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
            age_labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            df_work['Age_Group'] = pd.cut(df_work['Age'], bins=age_bins, labels=age_labels, right=False)

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Gini by Age Group
        if 'Age_Group' in df_work.columns:
            age_gini = []
            age_labels_plot = []

            for age_group in df_work['Age_Group'].dropna().unique():
                group_data = pd.to_numeric(
                    df_work[df_work['Age_Group'] == age_group]['Total_Person_Income'],
                    errors='coerce'
                )

                if self._should_exclude_zeros('Total_Person_Income'):
                    group_data = group_data[group_data > 0]

                group_data = group_data.dropna()

                if len(group_data) >= 10:
                    gini = self._calculate_gini(group_data.values)
                    if not np.isnan(gini):
                        age_gini.append(gini)
                        age_labels_plot.append(str(age_group))

            if age_gini:
                axes[0].bar(range(len(age_labels_plot)), age_gini, color='steelblue', edgecolor='black')
                axes[0].set_xticks(range(len(age_labels_plot)))
                axes[0].set_xticklabels(age_labels_plot, rotation=45, ha='right')
                configure_axes(axes[0],
                              title='Gini Coefficient by Age Group',
                              xlabel='Age Group',
                              ylabel='Gini Coefficient',
                              grid=True)
                axes[0].set_ylim(0, 1)

        # Gini by Education Level
        if 'Educational_Attainment' in df_work.columns:
            edu_gini = []
            edu_labels = []

            for edu_level in df_work['Educational_Attainment'].dropna().unique():
                group_data = pd.to_numeric(
                    df_work[df_work['Educational_Attainment'] == edu_level]['Total_Person_Income'],
                    errors='coerce'
                )

                if self._should_exclude_zeros('Total_Person_Income'):
                    group_data = group_data[group_data > 0]

                group_data = group_data.dropna()

                if len(group_data) >= 10:
                    gini = self._calculate_gini(group_data.values)
                    if not np.isnan(gini):
                        edu_gini.append(gini)
                        edu_labels.append(str(edu_level))

            if edu_gini:
                axes[1].bar(range(len(edu_labels)), edu_gini, color='coral', edgecolor='black')
                axes[1].set_xticks(range(len(edu_labels)))
                axes[1].set_xticklabels(edu_labels, rotation=45, ha='right')
                configure_axes(axes[1],
                              title='Gini Coefficient by Education Level',
                              xlabel='Education Level',
                              ylabel='Gini Coefficient',
                              grid=True)
                axes[1].set_ylim(0, 1)

        tight_layout_safe()
        self._save_fig('gini_by_demographic.png')

    def _inequality_heatmaps(self):
        """Create heatmaps showing median income by age group and education level."""
        if 'Total_Person_Income' not in self.df.columns:
            return

        # Create age groups if not present
        df_work = self.df.copy()
        if 'Age_Group' not in df_work.columns and 'Age' in df_work.columns:
            age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
            age_labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            df_work['Age_Group'] = pd.cut(df_work['Age'], bins=age_bins, labels=age_labels, right=False)

        if 'Age_Group' not in df_work.columns or 'Educational_Attainment' not in df_work.columns:
            return

        # Filter income data
        income_data = pd.to_numeric(df_work['Total_Person_Income'], errors='coerce')
        if self._should_exclude_zeros('Total_Person_Income'):
            df_work = df_work[income_data > 0].copy()
            income_data = income_data[income_data > 0]

        df_work['Total_Person_Income'] = income_data
        df_work = df_work.dropna(subset=['Total_Person_Income', 'Age_Group', 'Educational_Attainment'])

        if len(df_work) < 10:
            return

        # Create cross-tabulation
        pivot_table = df_work.pivot_table(
            values='Total_Person_Income',
            index='Age_Group',
            columns='Educational_Attainment',
            aggfunc='median'
        )

        # Convert to float to handle pd.NA (NAType) for seaborn compatibility
        pivot_table = pivot_table.astype(float)

        if pivot_table.empty:
            return

        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 8))

        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd',
                   cbar_kws={'label': 'Median Income ($)'}, ax=ax, linewidths=0.5)

        configure_axes(ax,
                      title='Median Income by Age Group and Education Level',
                      xlabel='Education Level',
                      ylabel='Age Group',
                      grid=False)

        # Rotate x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        tight_layout_safe()
        self._save_fig('inequality_age_education.png')

    def _percentile_divergence(self):
        """Plot percentile divergence over time to show income/wealth spreading."""
        # Find relevant columns
        value_cols = []
        if 'Total_Person_Income' in self.df.columns:
            value_cols.append('Total_Person_Income')
        if 'Property_Value' in self.df.columns:
            value_cols.append('Property_Value')

        if not value_cols or 'Census_Year' not in self.df.columns:
            return

        for col in value_cols:
            fig, ax = plt.subplots(figsize=(12, 7))

            percentiles = [10, 25, 50, 75, 90]
            percentile_data = {p: [] for p in percentiles}
            years = []

            for year in sorted(self.df['Census_Year'].unique()):
                year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col], errors='coerce')

                if self._should_exclude_zeros(col):
                    year_data = year_data[year_data > 0]

                year_data = year_data.dropna()

                if len(year_data) >= 10:
                    years.append(year)
                    for p in percentiles:
                        percentile_data[p].append(np.percentile(year_data, p))

            if len(years) > 0:
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                for idx, p in enumerate(percentiles):
                    ax.plot(years, percentile_data[p], marker='o', linewidth=2.5,
                           label=f'{p}th Percentile', color=colors[idx], markersize=6)

                configure_axes(ax,
                              title=f'Percentile Divergence: {col}',
                              xlabel='Census Year',
                              ylabel=f'{col} ($)',
                              grid=True)

                ax.legend(loc='best', fontsize=10)

                # Consider log scale if data spans orders of magnitude
                if percentile_data[90]:
                    auto_log_scale(ax, percentile_data[90], axis='y')

                tight_layout_safe()
                self._save_fig(f'percentile_divergence_{col}.png')

    def _percentile_gap(self):
        """Plot 90th-10th percentile gap over time to visualize inequality trends."""
        # Find relevant columns
        value_cols = []
        if 'Total_Person_Income' in self.df.columns:
            value_cols.append('Total_Person_Income')
        if 'Property_Value' in self.df.columns:
            value_cols.append('Property_Value')

        if not value_cols or 'Census_Year' not in self.df.columns:
            return

        fig, ax = plt.subplots(figsize=(12, 7))

        for col in value_cols:
            gaps = []
            years = []

            for year in sorted(self.df['Census_Year'].unique()):
                year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col], errors='coerce')

                if self._should_exclude_zeros(col):
                    year_data = year_data[year_data > 0]

                year_data = year_data.dropna()

                if len(year_data) >= 10:
                    p90 = np.percentile(year_data, 90)
                    p10 = np.percentile(year_data, 10)
                    gap = p90 - p10

                    gaps.append(gap)
                    years.append(year)

            if len(years) > 0:
                ax.plot(years, gaps, marker='o', linewidth=2.5, label=col, markersize=8)

        configure_axes(ax,
                      title='Percentile Gap Analysis (90th - 10th Percentile)',
                      xlabel='Census Year',
                      ylabel='Gap ($)',
                      grid=True)

        ax.legend(loc='best', fontsize=10)

        tight_layout_safe()
        self._save_fig('percentile_gap_analysis.png')

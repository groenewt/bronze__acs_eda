"""Statistical visualizations for distributions and advanced analytics"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer, _DEBUG_LOGGING
from .formatting import configure_axes, tight_layout_safe


class StatisticalVisualizer(BaseVisualizer):
    """Creates statistical distribution visualizations (memory optimized)"""

    def create_all(self):
        self._apply_housing_sampling()
        self._box_plots()
        self._distribution_with_stats()

    def _box_plots(self):
        """Create box plots for key variables showing quartiles and outliers"""
        print(f"[VIZ-VERBOSE] _box_plots: df.shape={self.df.shape}")
        key_cols = self._get_key_numeric_cols()
        print(f"[VIZ-VERBOSE] Key columns for box plots: {key_cols}")
        if not key_cols:
            print("[VIZ-WARNING] No key columns found - skipping box plots")
            return
        self._chunk_plot(key_cols, self._plot_box, 'box_plots')

    def _plot_box(self, ax, col: str):
        data = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        print(f"[VIZ-VERBOSE] Box plot for '{col}': {len(data)} non-null values")
        if len(data) > 0:
            print(f"[VIZ-VERBOSE] Data range: {data.min():.2f} to {data.max():.2f}")
            ax.boxplot(data, vert=True)
            ax.set_title(f'Distribution of {col}', fontweight='bold')
            ax.set_ylabel(col)
            ax.grid(alpha=0.3, axis='y')
            mean_val, median_val = data.mean(), data.median()
            ax.text(0.98, 0.98, f'Mean: {mean_val:,.0f}\nMedian: {median_val:,.0f}',
                   transform=ax.transAxes, verticalalignment='top',
                   horizontalalignment='right', bbox=dict(boxstyle='round',
                   facecolor='wheat', alpha=0.5), fontsize=9)
        else:
            print(f"[VIZ-WARNING] No data for column '{col}' - skipping")

    def _distribution_with_stats(self):
        """Create histograms with mean, median, and std dev overlay"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols:
            return
        self._chunk_plot(key_cols, self._plot_dist_stats, 'distribution_statistics')

    def _plot_dist_stats(self, ax, col: str):
        """Plot histogram with stats overlay (memory optimized, ≤10 lines)"""
        data = self.df[col].dropna()  # Avoid pd.to_numeric copy for numeric cols
        if _DEBUG_LOGGING:
            print(f"[DEBUG] _plot_dist_stats: col='{col}', before_filter={len(data)}")
        if self._should_exclude_zeros(col):
            data = data[data > 0]
            if _DEBUG_LOGGING:
                print(f"[DEBUG]   -> After filter: {len(data)} rows")
        if len(data) > 0:
            ax.hist(data, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
            mean_val, median_val = data.mean(), data.median()
            std_val, skew_val = data.std(), data.skew()
            kurt_val = data.kurtosis()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:,.0f}')
            ax.axvline(median_val, color='green', linestyle='-', linewidth=2, label=f'Median: {median_val:,.0f}')
            ax.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=1.5, alpha=0.7)
            ax.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=1.5, alpha=0.7,
                      label=f'±1 SD: {std_val:,.0f}')
            ax.set_title(f'{col} Distribution', fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.legend(loc='upper right', fontsize=8)
            stats_text = f'Skewness: {skew_val:.2f}\nKurtosis: {kurt_val:.2f}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   verticalalignment='top', bbox=dict(boxstyle='round',
                   facecolor='lightyellow', alpha=0.8), fontsize=8)

    def _get_key_numeric_cols(self) -> List[str]:
        """Get key columns with smart exclusions (expanded keywords)"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Specified_', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        if self.survey_type == "HOUSING":
            # Expanded housing keywords for comprehensive coverage
            keywords = ['Value', 'Rent', 'Income', 'Cost', 'Tax', 'Mortgage', 'Utility',
                        'Electricity', 'Gas', 'Water', 'Fuel', 'Insurance', 'Fee', 'Payment',
                        'Bedroom', 'Room', 'Vehicle', 'Person']
            selected = [c for c in valuable if any(k in c for k in keywords)][:16]
            print(f"[MEMORY] Housing: {len(selected)}/{len(numeric)} columns (excluded flags/binary)")
            return selected
        # Expanded population keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Age', 'Hours', 'Earnings', 'Week', 'Travel',
                    'Security', 'Retirement', 'Employment', 'Dividend', 'Assistance',
                    'Person', 'Poverty']
        return [c for c in valuable if any(k in c for k in keywords)][:16]


class AdvancedVisualizer(BaseVisualizer):
    """Creates advanced statistical visualizations"""

    def create_all(self):
        self._apply_housing_sampling()
        self._violin_plots()
        self._ridge_plots()
        self._radar_chart()
        self._split_violin_plots()
        self._demographic_ridgelines()

    def _violin_plots(self):
        """Create violin plots showing full distribution shape by year"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_violin, 'violin_plots', figsize=(16, 12))

    def _plot_violin(self, ax, col: str):
        data_by_year = []
        years = sorted(self.df['Census_Year'].dropna().unique())
        for year in years[-5:]:
            year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col],
                                     errors='coerce').dropna()
            if self._should_exclude_zeros(col):
                year_data = year_data[year_data > 0]
            if len(year_data) > 10:
                data_by_year.append(year_data)
        if data_by_year:
            parts = ax.violinplot(data_by_year, positions=range(len(data_by_year)),
                                 showmeans=True, showmedians=True)
            ax.set_xticks(range(len(data_by_year)))
            ax.set_xticklabels([str(int(y)) for y in years[-len(data_by_year):]], rotation=45)
            ax.set_title(f'{col} Distribution by Year (Violin Plot)', fontweight='bold')
            ax.set_ylabel(col)
            ax.grid(alpha=0.3, axis='y')

    def _ridge_plots(self):
        """Create ridge plots (joyplots) for temporal density visualization"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return

        col = key_cols[0]  # Use first key column
        years = sorted(self.df['Census_Year'].dropna().unique())[-8:]  # Last 8 years

        fig, ax = plt.subplots(figsize=(14, 10))

        colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

        for idx, year in enumerate(years):
            year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col],
                                     errors='coerce').dropna()
            if self._should_exclude_zeros(col):
                year_data = year_data[year_data > 0]
            if len(year_data) > 30:
                # Calculate density
                density, bins = np.histogram(year_data, bins=50, density=True)
                bin_centers = (bins[:-1] + bins[1:]) / 2

                # Offset each year's distribution vertically
                offset = idx * 0.15
                ax.fill_between(bin_centers, offset, offset + density * 0.1,
                               alpha=0.7, color=colors[idx], label=str(int(year)))
                ax.plot(bin_centers, offset + density * 0.1, color='black',
                       linewidth=0.5, alpha=0.8)

        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel('Year (stacked)', fontsize=12)
        ax.set_title(f'{col} Distribution Over Time (Ridge Plot)',
                    fontweight='bold', fontsize=14)
        ax.legend(loc='upper right', fontsize=9, ncol=2)
        ax.set_yticks([])
        tight_layout_safe()
        self._save_fig('ridge_plot.png')

    def _radar_chart(self):
        """Create radar chart for multi-dimensional comparison across years"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return

        years = sorted(self.df['Census_Year'].dropna().unique())
        if len(years) < 2:
            return

        # Compare first and last year
        compare_years = [years[0], years[-1]]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        angles = np.linspace(0, 2 * np.pi, len(key_cols), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        for year in compare_years:
            values = []
            year_df = self.df[self.df['Census_Year'] == year]

            for col in key_cols:
                col_data = pd.to_numeric(year_df[col], errors='coerce').dropna()
                if len(col_data) > 0:
                    # Normalize to 0-100 scale for comparison
                    all_data = pd.to_numeric(self.df[col], errors='coerce').dropna()
                    if all_data.max() > all_data.min():
                        normalized = (col_data.median() - all_data.min()) / (all_data.max() - all_data.min()) * 100
                        values.append(normalized)
                    else:
                        values.append(0)
                else:
                    values.append(0)

            values += values[:1]  # Complete the circle

            ax.plot(angles, values, 'o-', linewidth=2, label=f'Year {int(year)}')
            ax.fill(angles, values, alpha=0.15)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([col.replace('_', ' ') for col in key_cols], fontsize=9)
        ax.set_ylim(0, 100)
        ax.set_title('Multi-Dimensional Comparison (Radar Chart)',
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)

        tight_layout_safe()
        self._save_fig('radar_chart.png')

    def _split_violin_plots(self):
        """Create split violin plots comparing distributions side-by-side"""
        import seaborn as sns

        # Income by Tenure (Renters vs Owners)
        if 'Tenure' in self.df.columns and 'Total_Person_Income' in self.df.columns:
            data = self.df[['Tenure', 'Total_Person_Income']].dropna()
            data = data[data['Total_Person_Income'] > 0]
            if len(data) > 100:
                # Sample for performance
                if len(data) > 5000:
                    data = data.sample(5000, random_state=42)
                plt.figure(figsize=(10, 6))
                sns.violinplot(data=data, x='Tenure', y='Total_Person_Income',
                              palette='Set2', inner='quartile')
                plt.title('Income Distribution by Housing Tenure', fontweight='bold')
                plt.ylabel('Total Person Income')
                tight_layout_safe()
                self._save_fig('violin_income_by_tenure.png')

        # Costs by Burden Status
        if 'Gross_Rent_Percentage_Income' in self.df.columns:
            data = self.df[['Gross_Rent_Percentage_Income', 'Gross_Rent']].dropna()
            data = data[data['Gross_Rent'] > 0]
            data['Cost_Burdened'] = data['Gross_Rent_Percentage_Income'] > 30
            data['Cost_Burdened'] = data['Cost_Burdened'].map({True: 'Burdened (>30%)', False: 'Not Burdened'})
            if len(data) > 100:
                if len(data) > 5000:
                    data = data.sample(5000, random_state=42)
                plt.figure(figsize=(10, 6))
                sns.violinplot(data=data, x='Cost_Burdened', y='Gross_Rent',
                              palette='RdYlGn_r', inner='quartile')
                plt.title('Rent Distribution by Cost Burden Status', fontweight='bold')
                plt.ylabel('Gross Rent ($)')
                tight_layout_safe()
                self._save_fig('violin_costs_by_burden.png')

    def _demographic_ridgelines(self):
        """Create ridgeline plots showing stacked density distributions by demographic group"""
        import seaborn as sns

        # By Education Level
        if 'Educational_Attainment' in self.df.columns and 'Total_Person_Income' in self.df.columns:
            data = self.df[['Educational_Attainment', 'Total_Person_Income']].dropna()
            data = data[data['Total_Person_Income'] > 0]
            if len(data) > 100:
                if len(data) > 10000:
                    data = data.sample(10000, random_state=42)

                # Get top education categories
                top_cats = data['Educational_Attainment'].value_counts().head(6).index
                data = data[data['Educational_Attainment'].isin(top_cats)]

                plt.figure(figsize=(12, 8))
                # Use FacetGrid for ridgeline effect
                g = sns.FacetGrid(data, row='Educational_Attainment',
                                 hue='Educational_Attainment', aspect=4, height=1.2,
                                 palette='viridis')
                g.map(sns.kdeplot, 'Total_Person_Income', fill=True, alpha=0.7)
                g.set_titles('')
                g.set_xlabels('Income')
                plt.suptitle('Income Distribution by Education Level', fontweight='bold', y=1.02)
                tight_layout_safe()
                self._save_fig('ridgeline_income_by_education.png')

        # By Age Group
        if 'Age' in self.df.columns and 'Total_Person_Income' in self.df.columns:
            data = self.df[['Age', 'Total_Person_Income']].dropna()
            data = data[data['Total_Person_Income'] > 0]
            data['Age_Group'] = pd.cut(data['Age'], bins=[0, 25, 35, 45, 55, 65, 100],
                                       labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
            if len(data) > 100:
                if len(data) > 10000:
                    data = data.sample(10000, random_state=42)
                plt.figure(figsize=(12, 8))
                g = sns.FacetGrid(data, row='Age_Group', hue='Age_Group',
                                 aspect=4, height=1.2, palette='coolwarm')
                g.map(sns.kdeplot, 'Total_Person_Income', fill=True, alpha=0.7)
                g.set_titles('')
                plt.suptitle('Income Distribution by Age Group', fontweight='bold', y=1.02)
                tight_layout_safe()
                self._save_fig('ridgeline_income_by_age.png')

    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization (expanded keywords)"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours', 'Earnings',
                    'Cost', 'Tax', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Person', 'Poverty']
        cols = [c for c in valuable if any(k in c for k in keywords)]
        return cols[:8] if len(cols) >= 8 else cols

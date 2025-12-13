"""Economic visualizations for income, property values, and costs"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe, auto_log_scale


class EconomicVisualizer(BaseVisualizer):
    """Visualizes economic metrics"""

    def create_all(self):
        self._apply_housing_sampling()
        try:
            self._income_distribution()
        except Exception as e:
            print(f"[VIZ-WARNING] Income distribution plot failed: {e}")
        try:
            self._economic_trends()
        except Exception as e:
            print(f"[VIZ-WARNING] Economic trends plot failed: {e}")
        try:
            self._cost_analysis()
        except Exception as e:
            print(f"[VIZ-WARNING] Cost analysis plot failed: {e}")
        try:
            self._price_to_income_trends()
        except Exception as e:
            print(f"[VIZ-WARNING] Price-to-income trends plot failed: {e}")
        try:
            self._affordability_index()
        except Exception as e:
            print(f"[VIZ-WARNING] Affordability index plot failed: {e}")

    def _income_distribution(self):
        income_cols = self._find_income_cols()
        if not income_cols:
            return
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        self._plot_income_hist(axes[0], income_cols[0])
        self._plot_income_by_year(axes[1], income_cols[0])
        tight_layout_safe()
        self._save_fig('income_distribution.png')

    def _find_income_cols(self) -> List[str]:
        return [c for c in self.df.columns if 'Income' in c and
                self.df[c].dtype in [np.float64, np.int64]]

    def _plot_income_hist(self, ax, col: str):
        data = self.df[col].dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        if len(data) > 0:
            ax.hist(data, bins=50, edgecolor='black', alpha=0.7)
            ax.set_title(f'{col} Distribution', fontweight='bold')
            ax.set_xlabel('Income ($)')
            ax.set_ylabel('Frequency')
            auto_log_scale(ax, data, axis='x')  # Apply log scale if data spans orders of magnitude

    def _plot_income_by_year(self, ax, col: str):
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        # Filter zeros if needed
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='green')
        ax.set_title(f'Median {col} Over Time', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Median Income ($)')
        ax.grid(alpha=0.3)

    def _economic_trends(self):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        self._plot_property_values(axes[0, 0])
        self._plot_rents(axes[0, 1])
        self._plot_wages(axes[1, 0])
        self._plot_employment(axes[1, 1])
        tight_layout_safe()
        self._save_fig('economic_trends.png')

    def _plot_property_values(self, ax):
        if 'Property_Value' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Property_Value'], errors='coerce')
            if self._should_exclude_zeros('Property_Value'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='s', color='coral', linewidth=2)
            ax.set_title('Median Property Value', fontweight='bold')
            ax.set_ylabel('Value ($)')
            ax.grid(alpha=0.3)

    def _plot_rents(self, ax):
        if 'Gross_Rent' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Gross_Rent'], errors='coerce')
            if self._should_exclude_zeros('Gross_Rent'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='^', color='purple', linewidth=2)
            ax.set_title('Median Gross Rent', fontweight='bold')
            ax.set_ylabel('Rent ($)')
            ax.grid(alpha=0.3)

    def _plot_wages(self, ax):
        if 'Wage_Income' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Wage_Income'], errors='coerce')
            if self._should_exclude_zeros('Wage_Income'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='o', color='green', linewidth=2)
            ax.set_title('Median Wage Income', fontweight='bold')
            ax.set_ylabel('Wages ($)')
            ax.grid(alpha=0.3)

    def _plot_employment(self, ax):
        if 'Hours_Worked_Per_Week' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Hours_Worked_Per_Week'], errors='coerce')
            if self._should_exclude_zeros('Hours_Worked_Per_Week'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).mean()
            ax.plot(yearly.index, yearly.values, marker='d', color='orange', linewidth=2)
            ax.set_title('Avg Hours Worked Per Week', fontweight='bold')
            ax.set_ylabel('Hours')
            ax.grid(alpha=0.3)

    def _cost_analysis(self):
        cost_cols = self._find_cost_cols()
        if not cost_cols:
            return
        self._chunk_plot(cost_cols, self._plot_cost_trend, 'cost_analysis')

    def _find_cost_cols(self) -> List[str]:
        # Expanded keywords for comprehensive cost coverage
        keywords = ['Cost', 'Tax', 'Fee', 'Payment', 'Mortgage', 'Insurance',
                    'Electricity', 'Gas', 'Water', 'Fuel', 'Utility']
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor']
        cost_cols = [c for c in self.df.columns if any(k in c for k in keywords)]
        return [c for c in cost_cols if not any(p in c for p in exclude)]

    def _plot_cost_trend(self, ax, col: str):
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2)
        ax.set_title(f'{col}', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Cost ($)')
        ax.grid(alpha=0.3)

    def _price_to_income_trends(self):
        """Calculate median Property_Value / median Total_Person_Income by year"""
        if 'Property_Value' not in self.df.columns:
            return
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Household_Income'
        if income_col not in self.df.columns:
            return

        yearly_data = []
        for year in sorted(self.df['Census_Year'].unique()):
            year_df = self.df[self.df['Census_Year'] == year]
            prop_values = year_df['Property_Value'].dropna()
            incomes = year_df[income_col].dropna()
            prop_values = prop_values[prop_values > 0]
            incomes = incomes[incomes > 0]
            if len(prop_values) > 0 and len(incomes) > 0:
                median_ratio = prop_values.median() / incomes.median()
                # Calculate percentiles for confidence bands
                p25 = prop_values.quantile(0.25) / incomes.quantile(0.75)  # Conservative estimate
                p75 = prop_values.quantile(0.75) / incomes.quantile(0.25)  # Optimistic estimate
                yearly_data.append({
                    'year': year,
                    'ratio': median_ratio,
                    'p25': p25,
                    'p75': p75
                })

        if not yearly_data:
            return

        df_plot = pd.DataFrame(yearly_data)
        plt.figure(figsize=(10, 6))
        plt.plot(df_plot['year'], df_plot['ratio'], marker='o', linewidth=2, color='darkred', label='Median Ratio')
        plt.fill_between(df_plot['year'], df_plot['p25'], df_plot['p75'], alpha=0.3, color='red', label='25th-75th Percentile')
        plt.xlabel('Year')
        plt.ylabel('Property Value / Income Ratio')
        plt.title('Housing Affordability: Price-to-Income Ratio', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('price_to_income_trends.png')

    def _affordability_index(self):
        """Composite housing affordability index over time"""
        # Components: rent burden, owner cost burden, price-to-income ratio
        components_needed = {
            'rent': 'Gross_Rent_Percentage_Income',
            'owner': 'Owner_Costs_Percentage_Income',
            'property': 'Property_Value'
        }

        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Household_Income'

        if income_col not in self.df.columns:
            return

        # Check if we have at least 2 components
        available_components = sum([col in self.df.columns for col in components_needed.values()])
        if available_components < 2:
            return

        yearly_index = []
        for year in sorted(self.df['Census_Year'].unique()):
            year_df = self.df[self.df['Census_Year'] == year]
            index_components = []

            # Rent burden component (normalized, 30% = index 100)
            if 'Gross_Rent_Percentage_Income' in self.df.columns:
                rent_burden = year_df['Gross_Rent_Percentage_Income'].dropna()
                rent_burden = rent_burden[(rent_burden > 0) & (rent_burden < 100)]
                if len(rent_burden) > 0:
                    rent_index = (rent_burden.median() / 30) * 100
                    index_components.append(rent_index)

            # Owner cost burden component (normalized, 30% = index 100)
            if 'Owner_Costs_Percentage_Income' in self.df.columns:
                owner_burden = year_df['Owner_Costs_Percentage_Income'].dropna()
                owner_burden = owner_burden[(owner_burden > 0) & (owner_burden < 100)]
                if len(owner_burden) > 0:
                    owner_index = (owner_burden.median() / 30) * 100
                    index_components.append(owner_index)

            # Price-to-income component (normalized, ratio of 3.0 = index 100)
            if 'Property_Value' in self.df.columns:
                prop_values = year_df['Property_Value'].dropna()
                incomes = year_df[income_col].dropna()
                prop_values = prop_values[prop_values > 0]
                incomes = incomes[incomes > 0]
                if len(prop_values) > 0 and len(incomes) > 0:
                    price_income_ratio = prop_values.median() / incomes.median()
                    price_index = (price_income_ratio / 3.0) * 100
                    index_components.append(price_index)

            if index_components:
                composite_index = np.mean(index_components)
                yearly_index.append({'year': year, 'index': composite_index})

        if not yearly_index:
            return

        df_index = pd.DataFrame(yearly_index)
        plt.figure(figsize=(10, 6))
        plt.plot(df_index['year'], df_index['index'], marker='s', linewidth=2, color='darkblue')
        plt.axhline(100, color='orange', linestyle='--', linewidth=2, label='Baseline (100 = affordable)')
        plt.xlabel('Year')
        plt.ylabel('Affordability Index')
        plt.title('Composite Housing Affordability Index\n(Higher = Less Affordable)', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('affordability_index.png')

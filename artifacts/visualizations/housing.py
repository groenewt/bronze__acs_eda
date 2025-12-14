"""Housing characteristics, composition, and cost burden visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe, auto_log_scale
from logging_config import get_logger

logger = get_logger("visualization.housing")


class HousingCharacteristicsVisualizer(BaseVisualizer):
    """Visualizes housing unit characteristics"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating housing characteristics visualizations...")
        self._bedrooms_rooms_distribution()
        self._building_type_trends()
        self._year_built_distribution()
        self._vehicles_available()

    def _bedrooms_rooms_distribution(self):
        has_bed = 'Number_of_Bedrooms' in self.df.columns
        has_rooms = 'Number_of_Rooms' in self.df.columns
        if not (has_bed or has_rooms):
            logger.verbose("Skipping bedrooms/rooms distribution: missing Number_of_Bedrooms and Number_of_Rooms columns")
            return
        logger.verbose("Creating bedrooms/rooms distribution visualization...")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        if has_bed:
            bed_counts = self.df['Number_of_Bedrooms'].value_counts().sort_index()
            axes[0].bar(bed_counts.index, bed_counts.values, color='coral', edgecolor='black')
            axes[0].set_title('Number of Bedrooms', fontweight='bold', fontsize=12)
            axes[0].set_xlabel('Bedrooms')
            axes[0].set_ylabel('Count')
            axes[0].grid(alpha=0.3, axis='y')
        if has_rooms:
            room_counts = self.df['Number_of_Rooms'].value_counts().sort_index()
            axes[1].bar(room_counts.index, room_counts.values, color='teal', edgecolor='black')
            axes[1].set_title('Total Number of Rooms', fontweight='bold', fontsize=12)
            axes[1].set_xlabel('Rooms')
            axes[1].set_ylabel('Count')
            axes[1].grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('bedrooms_rooms_distribution.png')

    def _building_type_trends(self):
        if 'Building_Type' not in self.df.columns or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping building type trends: missing Building_Type or Census_Year columns")
            return
        logger.verbose("Creating building type trends visualization...")
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(self.df['Census_Year'], self.df['Building_Type'], normalize='index') * 100
        pivot.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Building Type Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend(title='Type', bbox_to_anchor=(1.05, 1))
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('building_type_trends.png')

    def _year_built_distribution(self):
        if 'Year_Structure_Built' not in self.df.columns:
            logger.verbose("Skipping year built distribution: missing Year_Structure_Built column")
            return
        logger.verbose("Creating year built distribution visualization...")
        plt.figure(figsize=(12, 6))
        years = self.df['Year_Structure_Built'].dropna()
        plt.hist(years, bins=30, color='steelblue', edgecolor='black')
        plt.title('Year Structure Built Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('year_built_distribution.png')

    def _vehicles_available(self):
        if 'Vehicles_Available' not in self.df.columns:
            logger.verbose("Skipping vehicles available: missing Vehicles_Available column")
            return
        logger.verbose("Creating vehicles available visualization...")
        plt.figure(figsize=(10, 6))
        veh_counts = self.df['Vehicles_Available'].value_counts().sort_index()
        plt.bar(veh_counts.index, veh_counts.values, color='darkgreen', edgecolor='black')
        plt.title('Vehicles Available per Household', fontweight='bold', fontsize=14)
        plt.xlabel('Number of Vehicles')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('vehicles_available.png')


class HouseholdCompositionVisualizer(BaseVisualizer):
    """Visualizes household composition and family structure"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating household composition visualizations...")
        self._family_type_distribution()
        self._household_size()
        self._children_presence()
        self._multigenerational_trends()
        self._age_composition()
        self._snap_participation()
        self._workers_distribution()
        self._household_diversity()

    def _family_type_distribution(self):
        if 'Household_Family_Type' not in self.df.columns:
            logger.verbose("Skipping family type distribution: missing Household_Family_Type column")
            return
        logger.verbose("Creating family type distribution visualization...")
        plt.figure(figsize=(10, 6))
        fam_counts = self.df['Household_Family_Type'].value_counts()
        plt.pie(fam_counts.values, labels=fam_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Household Family Type Distribution', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('family_type_distribution.png')

    def _household_size(self):
        if 'Number_of_Persons' not in self.df.columns:
            logger.verbose("Skipping household size: missing Number_of_Persons column")
            return
        logger.verbose("Creating household size visualization...")
        plt.figure(figsize=(10, 6))
        size_counts = self.df['Number_of_Persons'].value_counts().sort_index()
        plt.bar(size_counts.index, size_counts.values, color='purple', edgecolor='black')
        plt.title('Household Size Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Number of Persons')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('household_size.png')

    def _children_presence(self):
        child_cols = ['Household_Own_Children_Present', 'Household_Related_Children_Present']
        available = [c for c in child_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping children presence: missing child columns or Census_Year column")
            return
        logger.verbose("Creating children presence visualization...")
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in available:
            yearly = self.df.groupby('Census_Year')[col].mean() * 100
            ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, label=col.replace('_', ' '))
        ax.set_title('Children Presence in Households Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend()
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('children_presence.png')

    def _multigenerational_trends(self):
        if 'Multigenerational_Household' not in self.df.columns or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping multigenerational trends: missing Multigenerational_Household or Census_Year columns")
            return
        logger.verbose("Creating multigenerational trends visualization...")
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Multigenerational_Household'].mean() * 100
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='darkred')
        ax.set_title('Multigenerational Households Trend', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('multigenerational_trends.png')

    def _age_composition(self):
        """Household age composition - persons under 18, 60+, 65+"""
        age_cols = [
            ('Persons_Under_18', 'Under 18'),
            ('Persons_60_And_Over', '60 and Over'),
            ('Persons_65_And_Over', '65 and Over'),
        ]
        available = [(col, label) for col, label in age_cols if col in self.df.columns]
        if not available:
            logger.verbose("Skipping age composition: no age composition columns available")
            return
        logger.verbose("Creating household age composition visualization...")

        fig, axes = plt.subplots(1, len(available), figsize=(5 * len(available), 6))
        if len(available) == 1:
            axes = [axes]

        for idx, (col, label) in enumerate(available):
            ax = axes[idx]
            counts = self.df[col].value_counts().sort_index()
            ax.bar(counts.index, counts.values, color='steelblue', edgecolor='black')
            ax.set_title(f'Persons {label} in Household', fontweight='bold', fontsize=12)
            ax.set_xlabel('Count per Household')
            ax.set_ylabel('Number of Households')
            ax.grid(alpha=0.3, axis='y')

        tight_layout_safe()
        self._save_fig('household_age_composition.png')

    def _snap_participation(self):
        """Food Stamp/SNAP participation trends"""
        col = 'Food_Stamp_SNAP'
        if col not in self.df.columns or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping SNAP participation: missing Food_Stamp_SNAP or Census_Year columns")
            return
        logger.verbose("Creating SNAP participation visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        # FS: 1 = received SNAP, 2 = did not receive
        yearly = self.df.groupby('Census_Year').apply(
            lambda x: (x[col] == 1).sum() / len(x) * 100 if len(x) > 0 else 0
        )
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='#e67e22', markersize=8)
        ax.fill_between(yearly.index, yearly.values, alpha=0.3, color='#e67e22')
        ax.set_title('SNAP/Food Stamp Participation Rate Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Participation Rate (%)')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('snap_participation.png')

    def _workers_distribution(self):
        """Workers in family distribution"""
        col = 'Workers_In_Family'
        if col not in self.df.columns:
            logger.verbose("Skipping workers distribution: missing Workers_In_Family column")
            return
        logger.verbose("Creating workers distribution visualization...")

        plt.figure(figsize=(10, 6))
        worker_counts = self.df[col].value_counts().sort_index()
        colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(worker_counts)))
        plt.bar(worker_counts.index, worker_counts.values, color=colors, edgecolor='black')
        plt.title('Number of Workers in Family', fontweight='bold', fontsize=14)
        plt.xlabel('Number of Workers')
        plt.ylabel('Count of Households')
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('workers_in_family.png')

    def _household_diversity(self):
        """Same-sex couples and unmarried partners trends"""
        cols_map = [
            ('Same_Sex_Married_Couple', 'Same-Sex Married'),
            ('Unmarried_Partner_Household', 'Unmarried Partners'),
        ]
        available = [(col, label) for col, label in cols_map if col in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping household diversity: missing diversity columns or Census_Year column")
            return
        logger.verbose("Creating household diversity visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['#9b59b6', '#3498db']
        for idx, (col, label) in enumerate(available):
            yearly = self.df.groupby('Census_Year').apply(
                lambda x: (x[col] == 1).sum() / len(x) * 100 if len(x) > 0 else 0
            )
            ax.plot(yearly.index, yearly.values, marker='o', linewidth=2,
                    color=colors[idx % len(colors)], label=label, markersize=8)

        ax.set_title('Household Diversity Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage of Households (%)')
        ax.legend()
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('household_diversity_trends.png')


class CostBurdenVisualizer(BaseVisualizer):
    """Visualizes housing cost burden and affordability"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating cost burden visualizations...")
        self._rent_burden()
        self._owner_cost_burden()
        self._utility_costs_comparison()
        self._affordability_ecdf()
        self._burden_concentration()
        self._burden_by_demographic()

    def _rent_burden(self):
        if 'Gross_Rent_Percentage_Income' not in self.df.columns:
            logger.verbose("Skipping rent burden: missing Gross_Rent_Percentage_Income column")
            return
        logger.verbose("Creating rent burden visualization...")
        plt.figure(figsize=(12, 6))
        burden = self.df['Gross_Rent_Percentage_Income'].dropna()
        plt.hist(burden[burden < 100], bins=30, color='coral', edgecolor='black')
        plt.axvline(30, color='red', linestyle='--', linewidth=2, label='30% Threshold')
        plt.title('Gross Rent as Percentage of Income', fontweight='bold', fontsize=14)
        plt.xlabel('Percentage (%)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('rent_burden.png')

    def _owner_cost_burden(self):
        if 'Owner_Costs_Percentage_Income' not in self.df.columns:
            logger.verbose("Skipping owner cost burden: missing Owner_Costs_Percentage_Income column")
            return
        logger.verbose("Creating owner cost burden visualization...")
        plt.figure(figsize=(12, 6))
        burden = self.df['Owner_Costs_Percentage_Income'].dropna()
        plt.hist(burden[burden < 100], bins=30, color='steelblue', edgecolor='black')
        plt.axvline(30, color='red', linestyle='--', linewidth=2, label='30% Threshold')
        plt.title('Owner Costs as Percentage of Income', fontweight='bold', fontsize=14)
        plt.xlabel('Percentage (%)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('owner_cost_burden.png')

    def _utility_costs_comparison(self):
        util_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly', 'Fuel_Cost_Monthly', 'Water_Cost_Yearly']
        available = [c for c in util_cols if c in self.df.columns]
        if not available:
            logger.verbose("Skipping utility costs comparison: no utility cost columns available")
            return
        logger.verbose("Creating utility costs comparison visualization...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        for idx, col in enumerate(available[:8]):
            ax = axes[idx]
            data = self.df[col].dropna()
            if self._should_exclude_zeros(col):
                data = data[data > 0]
            if len(data) > 0:
                data_filtered = data[data < data.quantile(0.95)]
                ax.hist(data_filtered, bins=30, color='teal', edgecolor='black', alpha=0.7)
                ax.set_title(col.replace('_', ' '), fontweight='bold')
                ax.set_xlabel('Cost ($)')
                ax.set_ylabel('Frequency')
                ax.grid(alpha=0.3, axis='y')
                auto_log_scale(ax, data_filtered, axis='x')  # Log scale for wide cost ranges
        for idx in range(len(available), 4):
            axes[idx].axis('off')
        tight_layout_safe()
        self._save_fig('utility_costs_comparison.png')

    def _affordability_ecdf(self):
        """Empirical Cumulative Distribution Function of rent-to-income ratio"""
        col = 'Gross_Rent_Percentage_Income'
        if col not in self.df.columns:
            logger.verbose("Skipping affordability ECDF: missing Gross_Rent_Percentage_Income column")
            return
        logger.verbose("Creating affordability ECDF visualization...")
        data = self.df[col].dropna()
        data = data[(data > 0) & (data < 100)]  # Valid range
        if len(data) < 100:
            logger.verbose("Skipping affordability ECDF: insufficient data points")
            return

        # Calculate ECDF
        sorted_data = np.sort(data)
        ecdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_data, ecdf, linewidth=2, color='steelblue')
        plt.axvline(30, color='orange', linestyle='--', label='30% Threshold')
        plt.axvline(50, color='red', linestyle='--', label='50% Severe Burden')
        plt.xlabel('Rent as % of Income')
        plt.ylabel('Cumulative Proportion')
        plt.title('Housing Affordability: Cumulative Distribution', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('affordability_ecdf.png')

    def _burden_concentration(self):
        """Show how housing burden concentrates by income quintile"""
        col = 'Gross_Rent_Percentage_Income'
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Household_Income'

        if col not in self.df.columns or income_col not in self.df.columns:
            logger.verbose("Skipping burden concentration: missing Gross_Rent_Percentage_Income or income column")
            return
        logger.verbose("Creating burden concentration visualization...")

        # Filter valid data
        df_valid = self.df[[income_col, col]].dropna()
        df_valid = df_valid[(df_valid[col] > 0) & (df_valid[col] < 100)]
        df_valid = df_valid[df_valid[income_col] > 0]

        if len(df_valid) < 100:
            logger.verbose("Skipping burden concentration: insufficient data points")
            return

        # Create income quintiles
        df_valid['income_quintile'] = pd.qcut(df_valid[income_col], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])

        # Sort by income and calculate cumulative burden
        df_sorted = df_valid.sort_values(income_col).reset_index(drop=True)
        df_sorted['cumulative_pop'] = np.arange(1, len(df_sorted) + 1) / len(df_sorted)
        df_sorted['cumulative_burden'] = df_sorted[col].cumsum() / df_sorted[col].sum()

        plt.figure(figsize=(10, 6))
        plt.plot(df_sorted['cumulative_pop'], df_sorted['cumulative_burden'], linewidth=2, color='darkred')
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Equality')
        plt.xlabel('Cumulative Population (sorted by income)')
        plt.ylabel('Cumulative Cost Burden')
        plt.title('Housing Burden Concentration Curve', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('burden_concentration.png')

    def _burden_by_demographic(self):
        """Show % cost-burdened by demographic group"""
        col = 'Gross_Rent_Percentage_Income'
        if col not in self.df.columns:
            logger.verbose("Skipping burden by demographic: missing Gross_Rent_Percentage_Income column")
            return
        logger.verbose("Creating burden by demographic visualization...")

        # Create cost burden indicator (>30%)
        df_analysis = self.df.copy()
        df_analysis['cost_burdened'] = (df_analysis[col] > 30).astype(float)

        demographic_cols = []

        # Check for Age
        if 'Age' in df_analysis.columns:
            df_analysis['Age_Group'] = pd.cut(df_analysis['Age'],
                                               bins=[0, 25, 35, 50, 65, 100],
                                               labels=['<25', '25-35', '35-50', '50-65', '65+'])
            demographic_cols.append('Age_Group')

        # Check for Family Type
        if 'Household_Family_Type' in df_analysis.columns:
            demographic_cols.append('Household_Family_Type')

        # Check for Tenure
        if 'Tenure' in df_analysis.columns:
            demographic_cols.append('Tenure')

        if not demographic_cols:
            logger.verbose("Skipping burden by demographic: no demographic columns available")
            return

        # Calculate burden rates by demographic
        fig, axes = plt.subplots(len(demographic_cols), 1,
                                 figsize=(12, 5 * len(demographic_cols)))

        if len(demographic_cols) == 1:
            axes = [axes]

        for idx, demo_col in enumerate(demographic_cols):
            burden_rates = df_analysis.groupby(demo_col)['cost_burdened'].mean() * 100
            burden_rates = burden_rates.dropna().sort_values(ascending=False)

            axes[idx].barh(range(len(burden_rates)), burden_rates.values, color='coral', edgecolor='black')
            axes[idx].set_yticks(range(len(burden_rates)))
            axes[idx].set_yticklabels(burden_rates.index)
            axes[idx].set_xlabel('% Cost Burdened (>30% of income)')
            axes[idx].set_title(f'Cost Burden by {demo_col.replace("_", " ")}', fontweight='bold')
            axes[idx].axvline(30, color='red', linestyle='--', alpha=0.5)
            axes[idx].grid(alpha=0.3, axis='x')

        tight_layout_safe()
        self._save_fig('burden_by_demographic.png')

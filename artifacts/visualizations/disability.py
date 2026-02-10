"""Disability status and type visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe
from logging_config import get_logger

logger = get_logger("visualization.disability")


class DisabilityVisualizer(BaseVisualizer):
    """Visualizes disability prevalence, types, and demographic patterns"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating disability visualizations...")
        self._disability_prevalence()
        self._disability_types()
        self._disability_by_age()
        self._disability_trends()
        self._multiple_disabilities()
        self._disability_employment()
        self._disability_income_gap()
        self._disability_by_education()

    def _disability_prevalence(self):
        """Overall disability prevalence pie chart"""
        col = 'Disability_Status'
        if col not in self.df.columns:
            logger.verbose("Skipping disability prevalence: missing Disability_Status column")
            return
        logger.verbose("Creating disability prevalence visualization...")

        plt.figure(figsize=(10, 8))
        # DIS: 1 = has disability, 2 = no disability
        dis_counts = self.df[col].value_counts()
        labels = ['Has Disability (1)', 'No Disability (2)'] if len(dis_counts) == 2 else dis_counts.index
        colors = ['#e74c3c', '#2ecc71'] if len(dis_counts) == 2 else None
        plt.pie(dis_counts.values, labels=labels, autopct='%1.1f%%',
                startangle=90, colors=colors, explode=[0.02] * len(dis_counts))
        plt.title('Disability Status in Population', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('disability_prevalence.png')

    def _disability_types(self):
        """Bar chart showing prevalence of different disability types"""
        dis_cols = [
            ('Hearing_Difficulty', 'Hearing'),
            ('Vision_Difficulty', 'Vision'),
            ('Cognitive_Difficulty', 'Cognitive'),
            ('Ambulatory_Difficulty', 'Ambulatory'),
            ('Self_Care_Difficulty', 'Self-Care'),
            ('Independent_Living_Difficulty', 'Independent Living'),
        ]
        available = [(col, label) for col, label in dis_cols if col in self.df.columns]
        if not available:
            logger.verbose("Skipping disability types: no disability type columns available")
            return
        logger.verbose("Creating disability types visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        # Calculate percentage with each disability type (value == 1 means has difficulty)
        dis_pcts = []
        labels = []
        for col, label in available:
            pct = self._calc_binary_rate(self.df, col, true_value=1)
            dis_pcts.append(pct)
            labels.append(label)

        colors = plt.cm.Reds(np.linspace(0.3, 0.8, len(labels)))
        bars = ax.barh(labels, dis_pcts, color=colors, edgecolor='black')
        ax.set_xlabel('Percentage of Population (%)')
        ax.set_title('Disability Type Prevalence', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='x')

        # Add percentage labels
        for i, (pct, label) in enumerate(zip(dis_pcts, labels)):
            ax.text(pct + 0.1, i, f'{pct:.2f}%', va='center', fontsize=10)

        tight_layout_safe()
        self._save_fig('disability_types.png')

    def _disability_by_age(self):
        """Disability rate by age group"""
        col = 'Disability_Status'
        if col not in self.df.columns or 'Age' not in self.df.columns:
            logger.verbose("Skipping disability by age: missing Disability_Status or Age columns")
            return
        logger.verbose("Creating disability by age visualization...")

        df_analysis = self.df.copy()
        age_bins = [0, 18, 30, 45, 60, 75, 100]
        age_labels = ['0-17', '18-29', '30-44', '45-59', '60-74', '75+']
        df_analysis['Age_Group'] = pd.cut(df_analysis['Age'], bins=age_bins, labels=age_labels)

        fig, ax = plt.subplots(figsize=(12, 6))
        # Calculate disability rate by age group (DIS == 1 means has disability)
        dis_by_age = self._calc_rate_by_group(df_analysis, 'Age_Group', col, true_value=1)
        colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(dis_by_age)))
        ax.bar(dis_by_age.index, dis_by_age.values, color=colors, edgecolor='black')
        ax.set_title('Disability Rate by Age Group', fontweight='bold', fontsize=14)
        ax.set_xlabel('Age Group')
        ax.set_ylabel('Disability Rate (%)')
        ax.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('disability_by_age.png')

    def _disability_trends(self):
        """Disability rate over time"""
        col = 'Disability_Status'
        if col not in self.df.columns or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping disability trends: missing Disability_Status or Census_Year columns")
            return
        logger.verbose("Creating disability trends visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self._calc_rate_by_group(self.df, 'Census_Year', col, true_value=1)
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='#e74c3c', markersize=8)
        ax.fill_between(yearly.index, yearly.values, alpha=0.3, color='#e74c3c')
        ax.set_title('Disability Rate Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Disability Rate (%)')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('disability_trends.png')

    def _multiple_disabilities(self):
        """Heatmap showing co-occurrence of disability types"""
        dis_cols = [
            'Hearing_Difficulty', 'Vision_Difficulty', 'Cognitive_Difficulty',
            'Ambulatory_Difficulty', 'Self_Care_Difficulty', 'Independent_Living_Difficulty'
        ]
        available = [c for c in dis_cols if c in self.df.columns]
        if len(available) < 2:
            logger.verbose(f"Skipping multiple disabilities: insufficient columns (found {len(available)})")
            return
        logger.verbose("Creating multiple disabilities co-occurrence visualization...")

        # Create binary matrix (1 = has disability)
        df_binary = self.df[available].copy()
        for col in available:
            df_binary[col] = self._to_binary(df_binary[col], true_value=1)

        # Calculate correlation matrix
        corr_matrix = df_binary.corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr_matrix, cmap='Reds', aspect='auto', vmin=0, vmax=1)
        plt.colorbar(im, ax=ax, label='Correlation')

        # Labels
        labels = [c.replace('_Difficulty', '').replace('_', ' ') for c in available]
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_yticklabels(labels)

        # Add correlation values
        for i in range(len(available)):
            for j in range(len(available)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha='center', va='center', color='black', fontsize=9)

        ax.set_title('Disability Type Co-occurrence', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('multiple_disabilities.png')

    def _disability_employment(self):
        """Employment status by disability status"""
        dis_col = 'Disability_Status'
        emp_col = 'Employment_Status_Recode'

        if dis_col not in self.df.columns or emp_col not in self.df.columns:
            logger.verbose("Skipping disability employment: missing Disability_Status or Employment_Status_Recode columns")
            return
        logger.verbose("Creating disability employment visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        # Compare employment distribution for disabled vs non-disabled
        disabled = self._safe_value_counts(self.df[self.df[dis_col] == 1][emp_col], dropna=True)
        disabled = disabled / disabled.sum() * 100
        not_disabled = self._safe_value_counts(self.df[self.df[dis_col] == 2][emp_col], dropna=True)
        not_disabled = not_disabled / not_disabled.sum() * 100

        x = np.arange(min(len(disabled), 6))
        width = 0.35
        codes = disabled.index[:6]

        ax.bar(x - width/2, disabled.reindex(codes).fillna(0).values, width,
               label='With Disability', color='#e74c3c')
        ax.bar(x + width/2, not_disabled.reindex(codes).fillna(0).values, width,
               label='No Disability', color='#2ecc71')

        ax.set_title('Employment Status by Disability Status', fontweight='bold', fontsize=14)
        ax.set_xlabel('Employment Status Code')
        ax.set_ylabel('Percentage (%)')
        ax.set_xticks(x)
        ax.set_xticklabels(codes)
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('disability_employment.png')

    def _disability_income_gap(self):
        """Compare income distributions between disabled and non-disabled"""
        dis_col = 'Disability_Status'
        income_col = 'Total_Person_Income'

        if dis_col not in self.df.columns or income_col not in self.df.columns:
            logger.verbose("Skipping disability income gap: missing Disability_Status or Total_Person_Income columns")
            return
        logger.verbose("Creating disability income gap visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))

        # Filter positive incomes for each group
        disabled = self.df[self.df[dis_col] == 1][income_col].dropna()
        not_disabled = self.df[self.df[dis_col] == 2][income_col].dropna()

        disabled = disabled[disabled > 0]
        not_disabled = not_disabled[not_disabled > 0]

        if len(disabled) < 10 or len(not_disabled) < 10:
            logger.verbose("Skipping disability income gap: insufficient data points")
            plt.close()
            return

        # Calculate medians for annotation
        med_disabled = disabled.median()
        med_not_disabled = not_disabled.median()

        # Limit x-axis to 95th percentile for visibility
        x_max = max(disabled.quantile(0.95), not_disabled.quantile(0.95))

        ax.hist([disabled, not_disabled], bins=50,
                label=[f'With Disability (median: ${med_disabled:,.0f})',
                       f'No Disability (median: ${med_not_disabled:,.0f})'],
                alpha=0.7, color=['#e74c3c', '#2ecc71'])
        ax.set_xlabel('Total Person Income ($)')
        ax.set_ylabel('Frequency')
        ax.set_title('Income Distribution by Disability Status', fontweight='bold', fontsize=14)
        ax.legend()
        ax.set_xlim(0, x_max)
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('disability_income_gap.png')

    def _disability_by_education(self):
        """Disability rate by educational attainment"""
        dis_col = 'Disability_Status'
        edu_col = 'Educational_Attainment'

        if dis_col not in self.df.columns or edu_col not in self.df.columns:
            logger.verbose("Skipping disability by education: missing Disability_Status or Educational_Attainment columns")
            return
        logger.verbose("Creating disability by education visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))

        # Calculate disability rate by education level
        dis_by_edu = self._calc_rate_by_group(self.df, edu_col, dis_col, true_value=1)

        # Filter to top 10 education levels by count (dropna to avoid NA in index)
        top_edu = self._safe_value_counts(self.df[edu_col], dropna=True).head(10).index
        dis_by_edu = dis_by_edu[dis_by_edu.index.isin(top_edu)].sort_values()

        if len(dis_by_edu) == 0:
            logger.verbose("Skipping disability by education: no valid education data")
            plt.close()
            return

        colors = plt.cm.Reds(np.linspace(0.3, 0.8, len(dis_by_edu)))
        ax.barh(range(len(dis_by_edu)), dis_by_edu.values, color=colors, edgecolor='black')
        ax.set_yticks(range(len(dis_by_edu)))
        ax.set_yticklabels([f'Code {self._safe_int(x, default=0)}' if pd.notna(x) else 'Unknown' for x in dis_by_edu.index])
        ax.set_xlabel('Disability Rate (%)')
        ax.set_title('Disability Rate by Educational Attainment', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='x')
        tight_layout_safe()
        self._save_fig('disability_by_education.png')

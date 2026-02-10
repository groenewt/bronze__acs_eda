"""Health Insurance coverage visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe
from logging_config import get_logger

logger = get_logger("visualization.health_insurance")


class HealthInsuranceVisualizer(BaseVisualizer):
    """Visualizes health insurance coverage patterns and trends"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating health insurance visualizations...")
        self._coverage_overview()
        self._insurance_type_breakdown()
        self._uninsured_trends()
        self._coverage_by_age()
        self._public_vs_private()
        self._coverage_by_employment()
        self._coverage_by_income_quartile()

    def _coverage_overview(self):
        """Overall health insurance coverage pie chart"""
        col = 'Health_Insurance_Coverage'
        if col not in self.df.columns:
            logger.verbose("Skipping coverage overview: missing Health_Insurance_Coverage column")
            return
        logger.verbose("Creating health insurance coverage overview...")

        plt.figure(figsize=(10, 8))
        coverage_counts = self._safe_value_counts(self.df[col])
        labels = ['Covered (1)', 'Not Covered (2)'] if len(coverage_counts) == 2 else coverage_counts.index
        colors = ['#2ecc71', '#e74c3c'] if len(coverage_counts) == 2 else None
        plt.pie(coverage_counts.values, labels=labels, autopct='%1.1f%%',
                startangle=90, colors=colors, explode=[0.02] * len(coverage_counts))
        plt.title('Health Insurance Coverage Overview', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('health_coverage_overview.png')

    def _insurance_type_breakdown(self):
        """Stacked bar of different insurance types"""
        ins_cols = [
            ('Health_Insurance_Employer', 'Employer'),
            ('Health_Insurance_Direct', 'Direct Purchase'),
            ('Health_Insurance_Medicare', 'Medicare'),
            ('Health_Insurance_Medicaid', 'Medicaid'),
            ('Health_Insurance_Tricare', 'Tricare'),
            ('Health_Insurance_VA', 'VA'),
            ('Health_Insurance_IHS', 'IHS'),
        ]
        available = [(col, label) for col, label in ins_cols if col in self.df.columns]
        if not available:
            logger.verbose("Skipping insurance type breakdown: no insurance type columns available")
            return
        logger.verbose("Creating insurance type breakdown visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        # Calculate percentage with each type of insurance (value == 1 means has coverage)
        coverage_pcts = []
        labels = []
        for col, label in available:
            pct = self._calc_binary_rate(self.df, col, true_value=1)
            coverage_pcts.append(pct)
            labels.append(label)

        colors = plt.cm.Set2(np.linspace(0, 1, len(labels)))
        ax.barh(labels, coverage_pcts, color=colors, edgecolor='black')
        ax.set_xlabel('Percentage of Population (%)')
        ax.set_title('Health Insurance Coverage by Type', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='x')

        # Add percentage labels
        for i, (pct, label) in enumerate(zip(coverage_pcts, labels)):
            ax.text(pct + 0.5, i, f'{pct:.1f}%', va='center', fontsize=10)

        tight_layout_safe()
        self._save_fig('insurance_type_breakdown.png')

    def _uninsured_trends(self):
        """Uninsured rate over time"""
        col = 'Health_Insurance_Coverage'
        if col not in self.df.columns or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping uninsured trends: missing Health_Insurance_Coverage or Census_Year columns")
            return
        logger.verbose("Creating uninsured trends visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        # HICOV: 1 = covered, 2 = not covered
        yearly = self._calc_rate_by_group(self.df, 'Census_Year', col, true_value=2)
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='#e74c3c', markersize=8)
        ax.fill_between(yearly.index, yearly.values, alpha=0.3, color='#e74c3c')
        ax.set_title('Uninsured Rate Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Uninsured Rate (%)')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('uninsured_trends.png')

    def _coverage_by_age(self):
        """Health insurance coverage by age group"""
        col = 'Health_Insurance_Coverage'
        if col not in self.df.columns or 'Age' not in self.df.columns:
            logger.verbose("Skipping coverage by age: missing Health_Insurance_Coverage or Age columns")
            return
        logger.verbose("Creating coverage by age visualization...")

        df_analysis = self.df.copy()
        age_bins = [0, 18, 26, 35, 45, 55, 65, 100]
        age_labels = ['0-17', '18-25', '26-34', '35-44', '45-54', '55-64', '65+']
        df_analysis['Age_Group'] = pd.cut(df_analysis['Age'], bins=age_bins, labels=age_labels)

        fig, ax = plt.subplots(figsize=(12, 6))
        # Calculate uninsured rate by age group
        uninsured_by_age = self._calc_rate_by_group(df_analysis, 'Age_Group', col, true_value=2)
        colors = ['#e74c3c' if pct > 10 else '#2ecc71' for pct in uninsured_by_age.values]
        ax.bar(uninsured_by_age.index, uninsured_by_age.values, color=colors, edgecolor='black')
        ax.axhline(y=10, color='orange', linestyle='--', label='10% Threshold')
        ax.set_title('Uninsured Rate by Age Group', fontweight='bold', fontsize=14)
        ax.set_xlabel('Age Group')
        ax.set_ylabel('Uninsured Rate (%)')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('coverage_by_age.png')

    def _public_vs_private(self):
        """Compare public vs private health insurance trends"""
        pub_col = 'Public_Health_Insurance'
        priv_col = 'Private_Health_Insurance'

        if pub_col not in self.df.columns or priv_col not in self.df.columns:
            logger.verbose("Skipping public vs private: missing Public_Health_Insurance or Private_Health_Insurance columns")
            return
        if 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping public vs private: missing Census_Year column")
            return
        logger.verbose("Creating public vs private insurance visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))
        yearly_pub = self._calc_rate_by_group(self.df, 'Census_Year', pub_col, true_value=1)
        yearly_priv = self._calc_rate_by_group(self.df, 'Census_Year', priv_col, true_value=1)

        ax.plot(yearly_pub.index, yearly_pub.values, marker='o', linewidth=2,
                color='#3498db', label='Public Insurance', markersize=8)
        ax.plot(yearly_priv.index, yearly_priv.values, marker='s', linewidth=2,
                color='#9b59b6', label='Private Insurance', markersize=8)
        ax.set_title('Public vs Private Health Insurance Coverage', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Coverage Rate (%)')
        ax.legend()
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('public_vs_private_insurance.png')

    def _coverage_by_employment(self):
        """Health insurance coverage by employment status"""
        cov_col = 'Health_Insurance_Coverage'
        emp_col = 'Employment_Status_Recode'

        if cov_col not in self.df.columns or emp_col not in self.df.columns:
            logger.verbose("Skipping coverage by employment: missing Health_Insurance_Coverage or Employment_Status_Recode columns")
            return
        logger.verbose("Creating coverage by employment visualization...")

        fig, ax = plt.subplots(figsize=(12, 6))

        # Calculate uninsured rate by employment status
        uninsured_by_emp = self._calc_rate_by_group(self.df, emp_col, cov_col, true_value=2)

        # Filter to top 6 employment categories by population size (dropna to avoid NA in index)
        top_emp = self._safe_value_counts(self.df[emp_col]).head(6).index
        uninsured_by_emp = uninsured_by_emp[uninsured_by_emp.index.isin(top_emp)]

        if len(uninsured_by_emp) == 0:
            logger.verbose("Skipping coverage by employment: no valid employment data")
            plt.close()
            return

        colors = ['#e74c3c' if pct > 15 else '#f39c12' if pct > 10 else '#2ecc71'
                  for pct in uninsured_by_emp.values]
        ax.bar(range(len(uninsured_by_emp)), uninsured_by_emp.values,
               color=colors, edgecolor='black')
        ax.set_xticks(range(len(uninsured_by_emp)))
        ax.set_xticklabels([f'Code {int(x)}' if pd.notna(x) else 'Unknown' for x in uninsured_by_emp.index])
        ax.set_ylabel('Uninsured Rate (%)')
        ax.set_xlabel('Employment Status Code')
        ax.set_title('Uninsured Rate by Employment Status', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('coverage_by_employment.png')

    def _coverage_by_income_quartile(self):
        """Health insurance coverage by income quartile"""
        cov_col = 'Health_Insurance_Coverage'
        income_col = 'Total_Person_Income'

        if cov_col not in self.df.columns or income_col not in self.df.columns:
            logger.verbose("Skipping coverage by income quartile: missing Health_Insurance_Coverage or Total_Person_Income columns")
            return
        logger.verbose("Creating coverage by income quartile visualization...")

        # Filter to positive incomes (handle NA values first)
        df_analysis = self.df[self.df[income_col].notna() & (self.df[income_col] > 0)].copy()
        if len(df_analysis) < 100:
            logger.verbose("Skipping coverage by income quartile: insufficient data points")
            return

        # Create income quartiles
        try:
            df_analysis['Income_Quartile'] = pd.qcut(
                df_analysis[income_col], 4,
                labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)']
            )
        except ValueError:
            # Handle case where quantiles can't be computed
            logger.verbose("Skipping coverage by income quartile: unable to compute quartiles")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        # Calculate uninsured rate by quartile
        uninsured_by_quartile = self._calc_rate_by_group(df_analysis, 'Income_Quartile', cov_col, true_value=2)

        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 4))
        ax.bar(uninsured_by_quartile.index, uninsured_by_quartile.values,
               color=colors, edgecolor='black')
        ax.set_ylabel('Uninsured Rate (%)')
        ax.set_xlabel('Income Quartile')
        ax.set_title('Uninsured Rate by Income Quartile', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='y')

        # Add value labels on bars
        for i, pct in enumerate(uninsured_by_quartile.values):
            ax.text(i, pct + 0.5, f'{pct:.1f}%', ha='center', fontsize=10)

        tight_layout_safe()
        self._save_fig('coverage_by_income_quartile.png')

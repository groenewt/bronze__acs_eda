"""Occupation and Industry visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe, subplots_with_spacing
from logging_config import get_logger

logger = get_logger("visualization.occupation_industry")


class OccupationIndustryVisualizer(BaseVisualizer):
    """Visualizes occupation and industry distributions and trends"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating occupation and industry visualizations...")
        self._industry_sector_distribution()
        self._occupation_skill_distribution()
        self._industry_income_relationship()
        self._industry_trends()
        self._occupation_by_sex()
        self._industry_wage_premium()
        self._occupation_education_matrix()

    def _industry_sector_distribution(self):
        """Show industry sector distribution with counts and percentages for ALL available columns"""
        # Find all Industry_Sector columns
        sector_cols = [c for c in self.df.columns if c.startswith('Industry_Sector')]
        if not sector_cols:
            logger.verbose("Skipping industry sector distribution: no Industry_Sector columns found")
            return

        for col in sector_cols:
            suffix = col.replace('Industry_Sector_', '').replace('Industry_Sector', 'All')
            logger.verbose(f"Creating industry sector distribution for {col}...")

            sector_counts = self._safe_value_counts(self.df[col])
            if len(sector_counts) == 0:
                continue

            total = sector_counts.sum()
            sector_pcts = (sector_counts / total * 100).round(1)

            fig, axes = subplots_with_spacing(1, 2, figsize=(16, 8), wspace=0.4)
            colors = plt.cm.Set3(np.linspace(0, 1, len(sector_counts)))

            # Left: Counts
            axes[0].barh(range(len(sector_counts)), sector_counts.values, color=colors, edgecolor='black')
            axes[0].set_yticks(range(len(sector_counts)))
            axes[0].set_yticklabels(sector_counts.index, fontsize=10)
            configure_axes(axes[0], title=f'Industry Sectors by Count ({suffix})', xlabel='Count')
            for i, v in enumerate(sector_counts.values):
                axes[0].text(v + max(sector_counts.values) * 0.01, i, f'{v:,}', va='center', fontsize=9)

            # Right: Percentages
            axes[1].barh(range(len(sector_pcts)), sector_pcts.values, color=colors, edgecolor='black')
            axes[1].set_yticks(range(len(sector_pcts)))
            axes[1].set_yticklabels(sector_pcts.index, fontsize=10)
            configure_axes(axes[1], title=f'Industry Sectors by Percentage ({suffix})', xlabel='Percentage (%)')
            for i, v in enumerate(sector_pcts.values):
                axes[1].text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)

            fig.suptitle(f'Industry Sector Distribution ({suffix})', fontweight='bold', fontsize=14, y=1.02)
            tight_layout_safe()
            self._save_fig(f'industry_sector_distribution_{suffix}.png')

    def _occupation_skill_distribution(self):
        """Show occupation skill level distribution for ALL available columns"""
        # Find all Occupation_Skill_Level columns
        skill_cols = [c for c in self.df.columns if c.startswith('Occupation_Skill_Level')]
        if not skill_cols:
            logger.verbose("Skipping occupation skill distribution: no Occupation_Skill_Level columns found")
            return

        skill_order = ['High', 'Medium', 'Low', 'Unknown']
        skill_colors = {'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c', 'Unknown': '#95a5a6'}

        for col in skill_cols:
            suffix = col.replace('Occupation_Skill_Level_', '').replace('Occupation_Skill_Level', 'All')
            logger.verbose(f"Creating occupation skill distribution for {col}...")

            skill_counts = self._safe_value_counts(self.df[col])
            if len(skill_counts) == 0:
                continue

            skill_counts = skill_counts.reindex([s for s in skill_order if s in skill_counts.index])
            total = skill_counts.sum()
            skill_pcts = (skill_counts / total * 100).round(1)

            fig, axes = subplots_with_spacing(1, 2, figsize=(14, 6), wspace=0.4)
            colors = [skill_colors.get(s, '#3498db') for s in skill_counts.index]

            # Left: Counts
            axes[0].barh(range(len(skill_counts)), skill_counts.values, color=colors, edgecolor='black')
            axes[0].set_yticks(range(len(skill_counts)))
            axes[0].set_yticklabels(skill_counts.index, fontsize=11)
            configure_axes(axes[0], title=f'Skill Levels by Count ({suffix})', xlabel='Count')
            for i, v in enumerate(skill_counts.values):
                axes[0].text(v + max(skill_counts.values) * 0.01, i, f'{v:,}', va='center', fontsize=10)

            # Right: Percentages
            axes[1].barh(range(len(skill_pcts)), skill_pcts.values, color=colors, edgecolor='black')
            axes[1].set_yticks(range(len(skill_pcts)))
            axes[1].set_yticklabels(skill_pcts.index, fontsize=11)
            configure_axes(axes[1], title=f'Skill Levels by Percentage ({suffix})', xlabel='Percentage (%)')
            for i, v in enumerate(skill_pcts.values):
                axes[1].text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)

            fig.suptitle(f'Occupation Skill Level Distribution ({suffix})', fontweight='bold', fontsize=14, y=1.02)
            tight_layout_safe()
            self._save_fig(f'occupation_skill_distribution_{suffix}.png')

    def _industry_income_relationship(self):
        """Box plot of income by industry (top 10 industries)"""
        industry_cols = ['Industry_Code_2007', 'Industry_Code_2002', 'INDP']
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Wage_Income'

        industry_col = next((c for c in industry_cols if c in self.df.columns), None)
        if industry_col is None or income_col not in self.df.columns:
            logger.verbose("Skipping industry income relationship: missing required columns")
            return
        logger.verbose("Creating industry income relationship box plot...")

        # Get top 10 industries (dropna to avoid NA in index)
        top_industries = self._safe_value_counts(self.df[industry_col]).head(10).index.tolist()
        if len(top_industries) == 0:
            return

        df_filtered = self.df[self.df[industry_col].isin(top_industries)].copy()

        # Filter zero/negative incomes
        if self._should_exclude_zeros(income_col):
            df_filtered = df_filtered[df_filtered[income_col] > 0]

        if len(df_filtered) < 100:
            return

        plt.figure(figsize=(14, 8))
        df_filtered.boxplot(column=income_col, by=industry_col, figsize=(14, 8))
        plt.suptitle('')
        plt.title('Income Distribution by Top 10 Industries', fontweight='bold', fontsize=14)
        plt.xlabel('Industry Code')
        plt.ylabel('Income ($)')
        plt.xticks(rotation=45)
        tight_layout_safe()
        self._save_fig('industry_income_relationship.png')

    def _industry_trends(self):
        """Show industry distribution changes over time"""
        industry_cols = ['Industry_Code_2007', 'Industry_Code_2002', 'INDP']
        industry_col = next((c for c in industry_cols if c in self.df.columns), None)

        if industry_col is None or 'Census_Year' not in self.df.columns:
            logger.verbose("Skipping industry trends: missing required columns")
            return
        logger.verbose("Creating industry trends over time...")

        # Get top 5 industries (dropna to avoid NA in index)
        top_industries = self._safe_value_counts(self.df[industry_col]).head(5).index.tolist()
        if len(top_industries) == 0:
            return

        df_top = self.df[self.df[industry_col].isin(top_industries)].copy()
        if len(df_top) == 0:
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(df_top['Census_Year'], df_top[industry_col], normalize='index') * 100
        pivot.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Top 5 Industries Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage of Workers')
        ax.legend(title='Industry Code', bbox_to_anchor=(1.05, 1))
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('industry_trends.png')

    def _occupation_by_sex(self):
        """Show occupation distribution by sex"""
        occ_cols = ['Occupation_Code_2010', 'Occupation_Code_2002', 'OCCP']
        occ_col = next((c for c in occ_cols if c in self.df.columns), None)

        if occ_col is None or 'Sex' not in self.df.columns:
            logger.verbose("Skipping occupation by sex: missing required columns")
            return
        logger.verbose("Creating occupation by sex distribution...")

        # Get top 8 occupations (dropna to avoid NA in index)
        top_occs = self._safe_value_counts(self.df[occ_col]).head(8).index.tolist()
        if len(top_occs) == 0:
            return

        df_top = self.df[self.df[occ_col].isin(top_occs)].copy()
        if len(df_top) == 0:
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(df_top[occ_col], df_top['Sex'], normalize='index') * 100
        pivot.plot(kind='barh', ax=ax, stacked=True, color=['steelblue', 'coral'])
        ax.set_title('Top 8 Occupations by Sex Distribution', fontweight='bold', fontsize=14)
        ax.set_xlabel('Percentage')
        ax.set_ylabel('Occupation Code')
        ax.legend(['Male (1)', 'Female (2)'], title='Sex')
        ax.grid(alpha=0.3, axis='x')
        tight_layout_safe()
        self._save_fig('occupation_by_sex.png')

    def _industry_wage_premium(self):
        """Calculate and visualize wage premium/discount by industry relative to overall median"""
        industry_cols = ['Industry_Code_2007', 'Industry_Code_2002', 'Industry_Code', 'INDP']
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Wage_Income'

        industry_col = next((c for c in industry_cols if c in self.df.columns), None)
        if industry_col is None or income_col not in self.df.columns:
            logger.verbose("Skipping industry wage premium: missing required columns")
            return
        logger.verbose("Creating industry wage premium analysis...")

        # Filter to positive incomes
        df_analysis = self.df[self.df[income_col] > 0].copy()
        if len(df_analysis) < 100:
            return

        # Calculate overall median
        overall_median = df_analysis[income_col].median()

        # Get top 15 industries by count (dropna to avoid NA in index)
        top_industries = self._safe_value_counts(df_analysis[industry_col]).head(15).index.tolist()
        if len(top_industries) == 0:
            return

        df_top = df_analysis[df_analysis[industry_col].isin(top_industries)]
        if len(df_top) == 0:
            return

        # Calculate median by industry and premium
        industry_medians = df_top.groupby(industry_col)[income_col].median()
        premiums = ((industry_medians - overall_median) / overall_median * 100).sort_values()

        fig, ax = plt.subplots(figsize=(12, 8))

        colors = ['#e74c3c' if p < 0 else '#2ecc71' for p in premiums.values]
        bars = ax.barh(range(len(premiums)), premiums.values, color=colors, edgecolor='black')

        ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
        ax.set_yticks(range(len(premiums)))
        ax.set_yticklabels([f'Industry {int(x)}' if pd.notna(x) else 'Unknown' for x in premiums.index], fontsize=9)
        ax.set_xlabel('Wage Premium/Discount (%)')
        ax.set_title(f'Industry Wage Premium/Discount (vs Overall Median: ${overall_median:,.0f})',
                     fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='x')

        # Add percentage labels
        for i, pct in enumerate(premiums.values):
            offset = 2 if pct >= 0 else -2
            ha = 'left' if pct >= 0 else 'right'
            ax.text(pct + offset, i, f'{pct:+.1f}%', va='center', ha=ha, fontsize=9)

        tight_layout_safe()
        self._save_fig('industry_wage_premium.png')

    def _occupation_education_matrix(self):
        """Heatmap showing occupation distribution by educational attainment"""
        occ_cols = ['Occupation_Code_2010', 'Occupation_Code_2002', 'Occupation_Code', 'OCCP']
        occ_col = next((c for c in occ_cols if c in self.df.columns), None)
        edu_col = 'Educational_Attainment'

        if occ_col is None or edu_col not in self.df.columns:
            logger.verbose("Skipping occupation education matrix: missing required columns")
            return
        logger.verbose("Creating occupation-education matrix heatmap...")

        # Get top 10 occupations and top 8 education levels (dropna to avoid NA in index)
        top_occs = self._safe_value_counts(self.df[occ_col]).head(10).index.tolist()
        top_edu = self._safe_value_counts(self.df[edu_col]).head(8).index.tolist()

        if len(top_occs) == 0 or len(top_edu) == 0:
            return

        df_filtered = self.df[
            (self.df[occ_col].isin(top_occs)) &
            (self.df[edu_col].isin(top_edu))
        ].copy()

        if len(df_filtered) < 100:
            return

        # Create cross-tabulation (normalized by column - education)
        crosstab = pd.crosstab(df_filtered[occ_col], df_filtered[edu_col], normalize='columns') * 100

        fig, ax = plt.subplots(figsize=(12, 10))
        im = ax.imshow(crosstab.values, cmap='YlGnBu', aspect='auto')
        plt.colorbar(im, ax=ax, label='Percentage within Education Level (%)')

        # Labels
        ax.set_xticks(range(len(crosstab.columns)))
        ax.set_yticks(range(len(crosstab.index)))
        ax.set_xticklabels([f'Edu {int(x)}' if pd.notna(x) else 'Unknown' for x in crosstab.columns], rotation=45, ha='right')
        ax.set_yticklabels([f'Occ {int(x)}' if pd.notna(x) else 'Unknown' for x in crosstab.index])

        ax.set_xlabel('Educational Attainment Code')
        ax.set_ylabel('Occupation Code')
        ax.set_title('Occupation Distribution by Educational Attainment', fontweight='bold', fontsize=14)

        # Add percentage values in cells
        for i in range(len(crosstab.index)):
            for j in range(len(crosstab.columns)):
                val = crosstab.iloc[i, j]
                color = 'white' if val > 15 else 'black'
                ax.text(j, i, f'{val:.1f}', ha='center', va='center', color=color, fontsize=8)

        tight_layout_safe()
        self._save_fig('occupation_education_matrix.png')

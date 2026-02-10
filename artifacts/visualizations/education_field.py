"""Field of Degree and Education visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from logging_config import get_logger
from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe

logger = get_logger("visualization.education_field")


class EducationFieldVisualizer(BaseVisualizer):
    """Visualizes field of degree distributions and STEM patterns"""

    # Field of degree code mappings (top categories)
    FOD_CATEGORIES = {
        1100: 'Agriculture',
        1301: 'Environmental Science',
        1401: 'Architecture',
        1501: 'Area/Ethnic Studies',
        2001: 'Communications',
        2100: 'Computer Science',
        2400: 'Education',
        2500: 'Engineering',
        2600: 'Linguistics',
        2900: 'Family Sciences',
        3200: 'Biology',
        3301: 'Math/Statistics',
        3600: 'Interdisciplinary',
        3700: 'Fitness/Recreation',
        3800: 'Philosophy',
        4000: 'Physical Sciences',
        4100: 'Psychology',
        4800: 'Theology',
        5000: 'Visual Arts',
        5200: 'Business',
        5400: 'History',
        5500: 'Social Sciences',
        6000: 'Medical/Health',
        6100: 'Nursing',
    }

    def create_all(self):
        self._apply_housing_sampling()
        self._field_distribution()
        self._stem_trends()
        self._field_by_sex()
        self._field_income_relationship()
        self._stem_income_premium()
        self._field_trends_over_time()

    def _field_distribution(self):
        """Top 20 fields of degree by count"""
        col = 'FOD1P' if 'FOD1P' in self.df.columns else None
        if col is None:
            return

        plt.figure(figsize=(12, 10))
        fod_counts = self.df[col].dropna().value_counts().head(20)

        # Try to map codes to names
        labels = []
        for code in self._iter_codes_safe(fod_counts.index):
            # Round to nearest category
            category = int(code // 100) * 100
            label = self.FOD_CATEGORIES.get(category, f'Code {code}')
            labels.append(f'{label} ({code})')

        plt.barh(range(len(fod_counts)), fod_counts.values, color='steelblue', edgecolor='black')
        plt.yticks(range(len(fod_counts)), labels, fontsize=9)
        plt.xlabel('Count')
        plt.ylabel('Field of Degree')
        plt.title('Top 20 Fields of Degree', fontweight='bold', fontsize=14)
        plt.grid(alpha=0.3, axis='x')
        tight_layout_safe()
        self._save_fig('field_of_degree_distribution.png')

    def _stem_trends(self):
        """STEM field trends over time"""
        # SCIENGP: 1 = Science/Engineering field, 2 = Science/Engineering related, other = non-STEM
        col = 'SCIENGP' if 'SCIENGP' in self.df.columns else None
        if col is None or 'Census_Year' not in self.df.columns:
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        yearly_stem = self.df.groupby('Census_Year').apply(
            lambda x: (x[col] == 1).sum() / len(x[x[col].notna()]) * 100 if len(x[x[col].notna()]) > 0 else 0
        )
        yearly_stem_related = self.df.groupby('Census_Year').apply(
            lambda x: (x[col] == 2).sum() / len(x[x[col].notna()]) * 100 if len(x[x[col].notna()]) > 0 else 0
        )

        ax.plot(yearly_stem.index, yearly_stem.values, marker='o', linewidth=2,
                color='#3498db', label='STEM Field', markersize=8)
        ax.plot(yearly_stem_related.index, yearly_stem_related.values, marker='s', linewidth=2,
                color='#2ecc71', label='STEM-Related Field', markersize=8)

        ax.set_title('STEM Degree Holders Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage of Degree Holders (%)')
        ax.legend()
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('stem_trends.png')

    def _field_by_sex(self):
        """Field of degree distribution by sex"""
        col = 'FOD1P' if 'FOD1P' in self.df.columns else None
        if col is None or 'Sex' not in self.df.columns:
            return

        # Get top 10 fields (dropna to avoid NA in index)
        top_fields = self.df[col].dropna().value_counts().head(10).index.tolist()
        df_top = self.df[self.df[col].isin(top_fields)].copy()

        fig, ax = plt.subplots(figsize=(12, 8))
        pivot = pd.crosstab(df_top[col], df_top['Sex'], normalize='index') * 100

        # Map field codes to names (guard against NA)
        labels = []
        for code in pivot.index:
            # Use _iter_codes_safe pattern - check if NA first
            if pd.notna(code):
                category = int(code // 100) * 100
                label = self.FOD_CATEGORIES.get(category, f'Code {code}')
                labels.append(label[:20])  # Truncate long names
            else:
                labels.append('Unknown'[:20])

        pivot.index = labels
        pivot.plot(kind='barh', ax=ax, stacked=True, color=['steelblue', 'coral'])
        ax.set_title('Top 10 Fields of Degree by Sex', fontweight='bold', fontsize=14)
        ax.set_xlabel('Percentage')
        ax.set_ylabel('Field of Degree')
        ax.legend(['Male (1)', 'Female (2)'], title='Sex')
        ax.grid(alpha=0.3, axis='x')
        tight_layout_safe()
        self._save_fig('field_by_sex.png')

    def _field_income_relationship(self):
        """Income by field of degree"""
        col = 'FOD1P' if 'FOD1P' in self.df.columns else None
        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Wage_Income'

        if col is None or income_col not in self.df.columns:
            return

        # Get top 10 fields (dropna to avoid NA in index)
        top_fields = self.df[col].dropna().value_counts().head(10).index.tolist()
        df_top = self.df[self.df[col].isin(top_fields)].copy()

        # Filter zero incomes
        if self._should_exclude_zeros(income_col):
            df_top = df_top[df_top[income_col] > 0]

        if len(df_top) < 100:
            return

        fig, ax = plt.subplots(figsize=(14, 8))
        # Calculate median income by field
        median_incomes = df_top.groupby(col)[income_col].median().sort_values(ascending=True)

        # Map codes to names (guard against NA)
        labels = []
        for code in median_incomes.index:
            # Use _iter_codes_safe pattern - check if NA first
            if pd.notna(code):
                category = int(code // 100) * 100
                label = self.FOD_CATEGORIES.get(category, f'Code {code}')
                labels.append(label[:25])
            else:
                labels.append('Unknown'[:25])

        ax.barh(range(len(median_incomes)), median_incomes.values, color='teal', edgecolor='black')
        ax.set_yticks(range(len(median_incomes)))
        ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel('Median Income ($)')
        ax.set_title('Median Income by Field of Degree (Top 10 Fields)', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3, axis='x')

        # Add income labels
        for i, inc in enumerate(median_incomes.values):
            if pd.notna(inc):
                ax.text(inc + 1000, i, f'${inc:,.0f}', va='center', fontsize=9)
            else:
                logger.warning(f"NA median income for field index {i} - skipping label")

        tight_layout_safe()
        self._save_fig('field_income_relationship.png')

    def _stem_income_premium(self):
        """Compare income distributions between STEM and non-STEM degree holders"""
        # SCIENGP: 1 = Science/Engineering, 2 = Science/Engineering related, other = non-STEM
        stem_col = 'SCIENGP' if 'SCIENGP' in self.df.columns else 'Science_Engineering_Field'
        if stem_col not in self.df.columns:
            return

        income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Wage_Income'
        if income_col not in self.df.columns:
            return

        # Filter to positive incomes only (NA in SCIENGP means non-S&E field = Non-STEM)
        df_analysis = self.df[self.df[income_col] > 0].copy()
        if len(df_analysis) < 100:
            return

        # Create STEM category (1=STEM, 2=STEM-Related, NA/other=Non-STEM)
        def classify_stem(x):
            if pd.notna(x) and x == 1:
                return 'STEM'
            elif pd.notna(x) and x == 2:
                return 'STEM-Related'
            return 'Non-STEM'

        df_analysis['STEM_Category'] = df_analysis[stem_col].apply(classify_stem)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: Box plots by STEM category
        categories = ['STEM', 'STEM-Related', 'Non-STEM']
        data_by_cat = {cat: df_analysis[df_analysis['STEM_Category'] == cat][income_col] for cat in categories}

        # Calculate medians with NA handling
        medians = {}
        for cat, data in data_by_cat.items():
            med = data.median()
            if pd.notna(med) and med > 0:
                medians[cat] = float(med)
            else:
                logger.warning(f"Invalid median for {cat} (NA or <=0) - category excluded from analysis")

        # Need at least Non-STEM baseline and one other category
        if 'Non-STEM' not in medians or len(medians) < 2:
            logger.warning("Insufficient valid medians for STEM premium analysis")
            plt.close(fig)
            return

        # Build ordered lists for plotting
        valid_categories = [cat for cat in categories if cat in medians]
        data_list = [data_by_cat[cat] for cat in valid_categories]
        median_list = [medians[cat] for cat in valid_categories]

        bp = axes[0].boxplot(data_list, labels=valid_categories, patch_artist=True)
        colors = {'STEM': '#3498db', 'STEM-Related': '#2ecc71', 'Non-STEM': '#95a5a6'}
        for i, cat in enumerate(valid_categories):
            bp['boxes'][i].set_facecolor(colors[cat])

        axes[0].set_ylabel('Income ($)')
        axes[0].set_title('Income Distribution by STEM Status', fontweight='bold', fontsize=12)
        axes[0].grid(alpha=0.3, axis='y')

        # Add median annotations
        for i, cat in enumerate(valid_categories):
            med = medians[cat]
            axes[0].annotate(f'${med:,.0f}', xy=(i+1, med), xytext=(5, 5),
                            textcoords='offset points', fontsize=9)

        # Right: Premium calculation bar chart
        non_stem_median = medians['Non-STEM']
        premiums = [(medians[cat] - non_stem_median) / non_stem_median * 100 for cat in valid_categories]

        bar_colors = [colors[cat] for cat in valid_categories]
        axes[1].bar(valid_categories, premiums, color=bar_colors, edgecolor='black')
        axes[1].axhline(y=0, color='black', linestyle='-', linewidth=1)
        axes[1].set_ylabel('Income Premium vs Non-STEM (%)')
        axes[1].set_title('STEM Income Premium', fontweight='bold', fontsize=12)
        axes[1].grid(alpha=0.3, axis='y')

        # Add percentage labels
        for i, pct in enumerate(premiums):
            va = 'bottom' if pct >= 0 else 'top'
            axes[1].text(i, pct, f'{pct:+.1f}%', ha='center', va=va, fontsize=10)

        tight_layout_safe()
        self._save_fig('stem_income_premium.png')

    def _field_trends_over_time(self):
        """Show trends in top fields of degree over time"""
        col = 'FOD1P' if 'FOD1P' in self.df.columns else 'Field_Of_Degree_1'
        if col not in self.df.columns or 'Census_Year' not in self.df.columns:
            return

        # Get top 8 fields overall (dropna to avoid NA in index)
        top_fields = self.df[col].dropna().value_counts().head(8).index.tolist()
        df_top = self.df[self.df[col].isin(top_fields)].copy()

        if len(df_top) < 100:
            return

        fig, ax = plt.subplots(figsize=(14, 8))

        # Calculate percentage within each year
        yearly_pcts = pd.crosstab(df_top['Census_Year'], df_top[col], normalize='index') * 100

        # Map field codes to names for legend (guard against NA)
        for field_code in self._iter_codes_safe(yearly_pcts.columns):
            # Safe to use int() now since _iter_codes_safe filters out NA
            category = int(field_code // 100) * 100
            label = self.FOD_CATEGORIES.get(category, f'Code {field_code}')
            ax.plot(yearly_pcts.index, yearly_pcts[field_code].values,
                   marker='o', linewidth=2, label=label[:20], markersize=6)

        ax.set_title('Top Fields of Degree Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage of Degree Holders (%)')
        ax.legend(title='Field of Degree', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('field_trends_over_time.png')

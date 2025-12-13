"""Demographics and race/ethnicity visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class DemographicsVisualizer(BaseVisualizer):
    """Visualizes demographic distributions and trends"""

    def create_all(self):
        self._apply_housing_sampling()
        self._age_pyramid()
        self._education_distribution()
        self._marital_status_trends()
        self._citizenship_patterns()

    def _age_pyramid(self):
        if 'Age' not in self.df.columns or 'Sex' not in self.df.columns:
            return
        # Get 3 most recent years if Census_Year available
        if 'Census_Year' in self.df.columns:
            recent_years = sorted(self.df['Census_Year'].dropna().unique())[-3:]
            fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
            self._plot_pyramids_by_year(axes, recent_years)
        else:
            # Fallback to single pyramid if no year data
            fig, ax = plt.subplots(figsize=(10, 8))
            self._plot_single_pyramid(ax, self.df, 'All Years')
        tight_layout_safe()
        self._save_fig('age_pyramid.png')

    def _plot_pyramids_by_year(self, axes, years):
        """Plot age pyramids for multiple years (≤10 lines)"""
        age_bins = [0, 18, 30, 45, 60, 75, 100]
        labels = ['0-17', '18-29', '30-44', '45-59', '60-74', '75+']
        for idx, year in enumerate(years):
            df_year = self.df[self.df['Census_Year'] == year]
            self._plot_single_pyramid(axes[idx], df_year, str(int(year)), labels, age_bins)
            if idx == 0:
                axes[idx].set_ylabel('Age Group', fontweight='bold')

    def _plot_single_pyramid(self, ax, df, title, labels=None, age_bins=None):
        """Plot single age pyramid (≤10 lines)"""
        if labels is None:
            labels = ['0-17', '18-29', '30-44', '45-59', '60-74', '75+']
        if age_bins is None:
            age_bins = [0, 18, 30, 45, 60, 75, 100]
        df_clean = df[df['Age'].notna() & df['Sex'].notna()].copy()
        df_clean['Age_Group'] = pd.cut(df_clean['Age'], bins=age_bins, labels=labels)
        male = df_clean[df_clean['Sex'] == 1].groupby('Age_Group').size()
        female = df_clean[df_clean['Sex'] == 2].groupby('Age_Group').size()
        y_pos = np.arange(len(labels))
        ax.barh(y_pos, -male.reindex(labels, fill_value=0), color='steelblue', label='Male')
        ax.barh(y_pos, female.reindex(labels, fill_value=0), color='coral', label='Female')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Population Count', fontweight='bold')
        ax.set_title(f'Age Pyramid - {title}', fontweight='bold', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3, axis='x')
        ax.axvline(0, color='black', linewidth=0.8)

    def _education_distribution(self):
        if 'Educational_Attainment' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        edu_counts = self.df['Educational_Attainment'].value_counts().sort_index()
        plt.bar(edu_counts.index, edu_counts.values, color='teal', edgecolor='black')
        plt.title('Educational Attainment Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Education Level Code')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('education_distribution.png')

    def _marital_status_trends(self):
        if 'Marital_Status' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(self.df['Census_Year'], self.df['Marital_Status'], normalize='index') * 100
        pivot.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Marital Status Trends Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend(title='Status', bbox_to_anchor=(1.05, 1))
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('marital_status_trends.png')

    def _citizenship_patterns(self):
        if 'Citizenship_Status' not in self.df.columns:
            return
        plt.figure(figsize=(10, 6))
        cit_counts = self.df['Citizenship_Status'].value_counts()
        plt.pie(cit_counts.values, labels=cit_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Citizenship Status Distribution', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('citizenship_distribution.png')


class RaceEthnicityVisualizer(BaseVisualizer):
    """Visualizes race and ethnicity distributions"""

    def create_all(self):
        self._apply_housing_sampling()
        self._race_distribution()
        self._hispanic_origin_trends()
        self._diversity_trends()

    def _race_distribution(self):
        race_cols = ['Race_White', 'Race_Black', 'Race_Asian',
                    'Race_American_Indian_Alaska_Native', 'Race_Native_Hawaiian_Pacific_Islander']
        available = [c for c in race_cols if c in self.df.columns]
        if not available:
            return
        fig, ax = plt.subplots(figsize=(10, 6))
        race_counts = {col.replace('Race_', ''): self.df[col].sum() for col in available}
        ax.bar(race_counts.keys(), race_counts.values(), color='skyblue', edgecolor='black')
        ax.set_title('Race Distribution', fontweight='bold', fontsize=14)
        ax.set_xlabel('Race')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        ax.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('race_distribution.png')

    def _hispanic_origin_trends(self):
        if 'Hispanic_Origin' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Hispanic_Origin'].apply(lambda x: (x > 1).sum())
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='orange')
        ax.set_title('Hispanic/Latino Population Trend', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Count')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('hispanic_origin_trends.png')

    def _diversity_trends(self):
        if 'Number_Of_Races' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Number_Of_Races'].mean()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='purple')
        ax.set_title('Average Number of Races per Person', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Avg Number of Races')
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('diversity_trends.png')

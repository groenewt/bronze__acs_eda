"""Multi-variable interactions and enhanced feature visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from exceptions import PlotCreationError

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe
from memory_utils import adaptive_sample
from logging_config import get_logger

logger = get_logger("visualization.interactions")


class MultiVariableVisualizer(BaseVisualizer):
    """Visualizations for multi-variable interactions"""

    def create_all(self):
        # Memory-aware sampling for both HOUSING and POPULATION
        self.df = adaptive_sample(self.df, survey_type=self.survey_type)
        self._pairwise_interactions()
        self._three_way_interactions()

    def _pairwise_interactions(self):
        try:
            numeric_cols = self._get_key_numeric_cols()
            if len(numeric_cols) < 2:
                return
            # Create more diverse pairs for better coverage
            pairs = []
            for i in range(min(6, len(numeric_cols))):
                for j in range(i+1, min(i+3, len(numeric_cols))):
                    if len(pairs) < 6:
                        pairs.append((numeric_cols[i], numeric_cols[j]))

            if not pairs:
                return

            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            axes = axes.flatten()
            for idx, (col1, col2) in enumerate(pairs):
                data1 = self.df[col1].dropna()
                data2 = self.df[col2].dropna()
                if len(data1) > 0 and len(data2) > 0:
                    # Align data
                    common_idx = data1.index.intersection(data2.index)
                    axes[idx].scatter(data1[common_idx], data2[common_idx],
                                    alpha=0.3, s=5)
                    axes[idx].set_xlabel(col1)
                    axes[idx].set_ylabel(col2)
                    axes[idx].set_title(f'{col1} vs {col2}')
            # Hide unused subplots
            for idx in range(len(pairs), 6):
                axes[idx].axis('off')
            tight_layout_safe()
            self._save_fig('pairwise_interactions')
        except Exception as e:
            logger.warning(f"Pairwise interactions failed: {e}")

    def _three_way_interactions(self):
        try:
            numeric_cols = self._get_key_numeric_cols()[:5]
            if len(numeric_cols) < 3:
                return
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.df[numeric_cols[0]], self.df[numeric_cols[1]],
                      self.df[numeric_cols[2]], alpha=0.3, s=5)
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            ax.set_zlabel(numeric_cols[2])
            self._save_fig('three_way_interaction')
        except Exception as e:
            raise PlotCreationError('three_way_interaction', str(e))

    def _get_key_numeric_cols(self):
        numeric = self.df.select_dtypes(include=[np.number]).columns
        # Filter out flag/weight columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Adjustment_Factor', 'Weight_Replicate',
                   'SERIALNO', 'PUMA', 'ST', 'Specified_']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        # Expanded keywords for comprehensive coverage
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours', 'Earnings', 'Cost',
                    'Tax', 'Security', 'Retirement', 'Travel', 'Week',
                    'Electricity', 'Gas', 'Water', 'Poverty']
        matched = [c for c in valuable if any(k in c for k in keywords)]
        return matched[:15] if matched else valuable[:15]


class EnhancedFeatureInteractionVisualizer(BaseVisualizer):
    """Enhanced feature interactions and ratio analysis"""

    def create_all(self):
        # Memory-aware sampling for both HOUSING and POPULATION
        self.df = adaptive_sample(self.df, survey_type=self.survey_type)
        self._feature_ratios()
        self._quadrant_analysis()
        self._quintile_analysis()

    def _feature_ratios(self):
        try:
            pairs = [('Total_Person_Income', 'Hours_Worked_Per_Week'),
                    ('Property_Value', 'Household_Income'),
                    ('Gross_Rent', 'Household_Income')]
            for num, denom in pairs:
                if num in self.df.columns and denom in self.df.columns:
                    data = self.df[[num, denom]].dropna()
                    data = data[(data[denom] > 0) & (data[num] > 0)]
                    if len(data) > 10:
                        data['ratio'] = data[num] / data[denom]
                        plt.figure(figsize=(10, 6))
                        plt.hist(data['ratio'], bins=30, alpha=0.7, edgecolor='black')
                        plt.xlabel(f'{num} / {denom}')
                        plt.ylabel('Frequency')
                        plt.title(f'Ratio: {num}/{denom}', fontweight='bold')
                        self._save_fig(f'ratio_{num}_{denom}')
        except Exception as e:
            raise PlotCreationError('feature_ratios', str(e))

    def _quadrant_analysis(self):
        try:
            pairs = [('Age', 'Total_Person_Income'),
                    ('Property_Value', 'Gross_Rent'),
                    ('Hours_Worked_Per_Week', 'Wage_Income')]
            for x_col, y_col in pairs:
                if x_col in self.df.columns and y_col in self.df.columns:
                    data = self.df[[x_col, y_col]].dropna()
                    # Apply zero filtering like distributions.py
                    if self._should_exclude_zeros(x_col):
                        data = data[data[x_col] > 0]
                    if self._should_exclude_zeros(y_col):
                        data = data[data[y_col] > 0]
                    if len(data) > 10:
                        x_med = data[x_col].median()
                        y_med = data[y_col].median()
                        plt.figure(figsize=(10, 8))
                        plt.scatter(data[x_col], data[y_col], alpha=0.4, s=10)
                        plt.axvline(x_med, color='red', linestyle='--', alpha=0.7)
                        plt.axhline(y_med, color='red', linestyle='--', alpha=0.7)
                        plt.xlabel(x_col)
                        plt.ylabel(y_col)
                        plt.title(f'Quadrant: {x_col} vs {y_col}', fontweight='bold')
                        self._save_fig(f'quadrant_{x_col}_{y_col}')
        except Exception as e:
            raise PlotCreationError('quadrant_analysis', str(e))

    def _quintile_analysis(self):
        """Create quintile-based housing cost analysis"""
        try:
            import seaborn as sns
            income_col = 'Total_Person_Income' if 'Total_Person_Income' in self.df.columns else 'Household_Income'
            cost_col = 'Gross_Rent'
            burden_col = 'Gross_Rent_Percentage_Income'

            if income_col not in self.df.columns:
                return

            data = self.df[[income_col, cost_col, burden_col]].dropna() if cost_col in self.df.columns else None
            if data is None or len(data) < 100:
                return

            data = data[(data[income_col] > 0) & (data[cost_col] > 0)]
            data['Income_Quintile'] = pd.qcut(data[income_col], q=5, labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4', 'Q5 (Highest)'])

            # Scatter with regression by quintile
            if len(data) > 5000:
                plot_data = data.sample(5000, random_state=42)
            else:
                plot_data = data

            plt.figure(figsize=(12, 8))
            sns.scatterplot(data=plot_data, x=income_col, y=cost_col, hue='Income_Quintile',
                           alpha=0.5, palette='viridis')
            plt.title('Housing Costs by Income Quintile', fontweight='bold')
            plt.legend(title='Income Quintile', bbox_to_anchor=(1.02, 1))
            tight_layout_safe()
            self._save_fig('quintile_housing_scatter.png')

            # Burden rates by quintile
            burden_rates = data.groupby('Income_Quintile').apply(
                lambda x: (x[burden_col] > 30).mean() * 100
            )
            plt.figure(figsize=(10, 6))
            burden_rates.plot(kind='bar', color='coral', edgecolor='black')
            plt.axhline(30, color='red', linestyle='--', label='30% National Avg')
            plt.title('Housing Cost Burden Rate by Income Quintile', fontweight='bold')
            plt.xlabel('Income Quintile')
            plt.ylabel('% Cost Burdened (>30% Income)')
            plt.xticks(rotation=0)
            plt.legend()
            plt.grid(alpha=0.3, axis='y')
            tight_layout_safe()
            self._save_fig('quintile_burden_rates.png')
        except Exception as e:
            raise PlotCreationError('quintile_analysis', str(e))

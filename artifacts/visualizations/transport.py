"""Transportation and commute pattern visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class TransportationVisualizer(BaseVisualizer):
    """Visualizes commute and transportation patterns"""

    def create_all(self):
        self._apply_housing_sampling()
        self._travel_time_distribution()
        self._transportation_mode()
        self._commute_trends()

    def _travel_time_distribution(self):
        if 'Travel_Time_To_Work_Minutes' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        travel = self.df['Travel_Time_To_Work_Minutes'].dropna()
        if self._should_exclude_zeros('Travel_Time_To_Work_Minutes'):
            travel = travel[travel > 0]
        plt.hist(travel[travel < 120], bins=30, color='skyblue', edgecolor='black')
        plt.title('Travel Time to Work Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Minutes')
        plt.ylabel('Frequency')
        plt.axvline(travel.median(), color='red', linestyle='--', label=f'Median: {travel.median():.0f} min')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        tight_layout_safe()
        self._save_fig('travel_time_distribution.png')

    def _transportation_mode(self):
        if 'Transportation_To_Work' not in self.df.columns:
            return
        plt.figure(figsize=(10, 8))
        mode_counts = self.df['Transportation_To_Work'].value_counts()
        plt.barh(range(len(mode_counts)), mode_counts.values, color='teal')
        plt.yticks(range(len(mode_counts)), mode_counts.index)
        plt.title('Transportation Mode to Work', fontweight='bold', fontsize=14)
        plt.xlabel('Count')
        plt.grid(alpha=0.3, axis='x')
        tight_layout_safe()
        self._save_fig('transportation_mode.png')

    def _commute_trends(self):
        if 'Travel_Time_To_Work_Minutes' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        col = 'Travel_Time_To_Work_Minutes'
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            df_filtered[col] = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = df_filtered.groupby('Census_Year')[col].agg(['mean', 'median']).astype(float)
        yearly.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Commute Time Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Minutes')
        ax.legend(['Mean', 'Median'])
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('commute_trends.png')

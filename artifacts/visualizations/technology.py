"""Technology adoption visualizations"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

from .base import BaseVisualizer
from .formatting import configure_axes, tight_layout_safe


class TechnologyAdoptionVisualizer(BaseVisualizer):
    """Visualizes technology adoption trends"""

    def create_all(self):
        self._apply_housing_sampling()
        self._technology_adoption_trends()
        self._device_ownership()

    def _technology_adoption_trends(self):
        tech_cols = ['Smartphone', 'Tablet_Computer', 'Satellite_Internet']
        available = [c for c in tech_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in available:
            yearly = self.df.groupby('Census_Year')[col].mean() * 100
            ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, label=col.replace('_', ' '))
        ax.set_title('Technology Adoption Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Adoption Rate (%)')
        ax.legend()
        ax.grid(alpha=0.3)
        tight_layout_safe()
        self._save_fig('technology_adoption_trends.png')

    def _device_ownership(self):
        tech_cols = ['Smartphone', 'Tablet_Computer']
        available = [c for c in tech_cols if c in self.df.columns]
        if not available:
            return
        fig, axes = plt.subplots(1, len(available), figsize=(12, 5))
        if len(available) == 1:
            axes = [axes]
        for idx, col in enumerate(available):
            counts = self.df[col].value_counts()
            axes[idx].pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90)
            axes[idx].set_title(col.replace('_', ' '), fontweight='bold')
        tight_layout_safe()
        self._save_fig('device_ownership.png')

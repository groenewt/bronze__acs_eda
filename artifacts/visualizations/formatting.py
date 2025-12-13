"""Formatting utilities for visualizations"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional

FIGURE_SIZES = {
    'small': (8, 6),
    'medium': (10, 6),
    'large': (12, 8),
    'wide': (14, 6),
    'grid_2x2': (12, 10),
}

def configure_axes(ax, title=None, xlabel=None, ylabel=None, rotation=0, grid=True):
    """Standard axis configuration"""
    if title:
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if rotation:
        ax.tick_params(axis='x', rotation=rotation)
        for label in ax.get_xticklabels():
            label.set_ha('right')
    if grid:
        ax.grid(alpha=0.3, linestyle='--')

def format_pie_chart(ax, sizes, labels, title=None, max_slices=8):
    """Pie chart with legend instead of inline labels to prevent overlap"""
    sizes = np.array(sizes)
    if len(sizes) > max_slices:
        sorted_idx = np.argsort(sizes)[::-1]
        top_idx = sorted_idx[:max_slices-1]
        other_sum = sizes[sorted_idx[max_slices-1:]].sum()
        sizes = np.append(sizes[top_idx], other_sum)
        labels = [labels[i] for i in top_idx] + ['Other']

    def autopct(pct):
        return f'{pct:.1f}%' if pct > 5 else ''

    wedges, _, autotexts = ax.pie(sizes, labels=None, autopct=autopct, startangle=90, pctdistance=0.75)
    ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    if title:
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    return wedges

def tight_layout_safe(fig=None, pad=1.5):
    """Safe tight_layout with error handling"""
    try:
        (fig or plt.gcf()).tight_layout(pad=pad)
    except Exception:
        pass

def smart_legend(ax, loc='best', fontsize=9, max_items=10):
    """Legend with item limit"""
    handles, labels = ax.get_legend_handles_labels()
    if len(labels) > max_items:
        handles, labels = handles[:max_items], labels[:max_items]
    if handles:
        ax.legend(handles, labels, loc=loc, fontsize=fontsize, framealpha=0.9)

def subplots_with_spacing(nrows, ncols, figsize=None, hspace=0.35, wspace=0.3):
    """Subplots with proper spacing"""
    if figsize is None:
        figsize = (5*ncols, 4*nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    return fig, axes

def auto_log_scale(ax, data, axis='y', threshold_ratio=100):
    """Apply log scale if data spans more than threshold_ratio orders of magnitude.

    Args:
        ax: matplotlib axes object
        data: array-like data to check range
        axis: 'x' or 'y' axis to apply log scale
        threshold_ratio: min ratio of max/min to trigger log scale (default 100)
    """
    data = np.asarray(data)
    data_positive = data[data > 0]
    if len(data_positive) < 2:
        return False

    ratio = data_positive.max() / data_positive.min()
    if ratio > threshold_ratio:
        if axis == 'y':
            ax.set_yscale('log')
        else:
            ax.set_xscale('log')
        return True
    return False

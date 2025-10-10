#!/usr/bin/env python3
"""Debug script to trace data sizes through visualization pipeline"""

import sys
import pandas as pd
import numpy as np
from config import Config
from loader import DataLoader

def format_size(rows, cols):
    cells = rows * cols
    mb = (cells * 8) / (1024 * 1024)  # Assume 8 bytes per cell
    return f"{rows:,} rows × {cols} cols = {cells:,} cells (~{mb:.1f}MB)"

def main():
    # Setup
    config = Config()
    config.states = ["01"]
    config.surveys = ["housing"]
    config.scopes = ["1-year"]

    print("="*70)
    print("MEMORY DEBUG: Tracing data shapes through pipeline")
    print("="*70)

    # Load data
    loader = DataLoader(config)
    df = loader.load_data()
    print(f"\n[1] After load_data(): {format_size(len(df), len(df.columns))}")

    # Feature engineering (simulated)
    print(f"[2] After feature engineering: {format_size(len(df), len(df.columns))}")

    # StatisticalVisualizer sampling logic
    total_cells = len(df) * len(df.columns)
    target_cells = 10_000_000
    sample_rows = min(len(df), int(target_cells / len(df.columns)))

    print(f"\n[3] StatisticalVisualizer sampling:")
    print(f"    Original: {format_size(len(df), len(df.columns))}")
    print(f"    Target cells: {target_cells:,}")
    print(f"    Sample rows: {sample_rows:,}")

    df_sampled = df.sample(n=sample_rows, random_state=42) if len(df) > sample_rows else df
    print(f"    Sampled: {format_size(len(df_sampled), len(df_sampled.columns))}")

    # Column selection
    numeric = df_sampled.select_dtypes(include=[np.number]).columns
    exclude = ['Flag_', '_is_zero', '_is_missing', 'Specified_',
               'Adjustment_Factor', 'Weight_Replicate']
    valuable = [c for c in numeric if not any(p in c for p in exclude)]
    keywords = ['Value', 'Rent', 'Income', 'Cost', 'Tax', 'Mortgage', 'Utility']
    selected = [c for c in valuable if any(k in c for k in keywords)][:12]

    print(f"\n[4] Column selection:")
    print(f"    Total numeric: {len(numeric)}")
    print(f"    After exclusions: {len(valuable)}")
    print(f"    Housing keywords matched: {len(selected)}")
    print(f"    Selected columns: {selected}")

    # Final histogram data
    df_viz = df_sampled[selected]
    print(f"\n[5] Final visualization data: {format_size(len(df_viz), len(df_viz.columns))}")

    # Memory estimate for histogram creation (50 bins per column)
    bins = 50
    hist_memory = len(df_viz) * len(df_viz.columns) * bins * 8 / (1024 * 1024)
    print(f"\n[6] Estimated histogram memory (50 bins): ~{hist_memory:.1f}MB")

    # Aggressive sampling for housing
    aggressive_target = 1_000_000  # 1M cells (10x less)
    aggressive_rows = min(len(df), int(aggressive_target / len(df.columns)))
    df_aggressive = df.sample(n=aggressive_rows, random_state=42)
    df_aggressive_viz = df_aggressive[selected]

    print(f"\n[7] AGGRESSIVE SAMPLING (1M cells target):")
    print(f"    Sampled dataset: {format_size(len(df_aggressive), len(df_aggressive.columns))}")
    print(f"    Final viz data: {format_size(len(df_aggressive_viz), len(df_aggressive_viz.columns))}")
    aggressive_hist = len(df_aggressive_viz) * len(df_aggressive_viz.columns) * bins * 8 / (1024 * 1024)
    print(f"    Histogram memory: ~{aggressive_hist:.1f}MB")

    print("\n" + "="*70)
    print("COMPARISON:")
    print(f"  Current approach: {format_size(len(df_viz), len(df_viz.columns))}")
    print(f"  Aggressive approach: {format_size(len(df_aggressive_viz), len(df_aggressive_viz.columns))}")
    print(f"  Reduction: {len(df_viz) / len(df_aggressive_viz):.1f}x fewer rows")
    print("="*70)

if __name__ == "__main__":
    main()

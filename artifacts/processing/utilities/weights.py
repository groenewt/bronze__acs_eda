import pandas as pd
import numpy as np
from typing import Dict


def get_weight_column(survey_type: str) -> str:
    """Get appropriate weight column name for survey type."""
    if survey_type == 'population':
        return 'Person_Weight'
    elif survey_type == 'housing':
        return 'Housing_Unit_Weight'
    return 'Person_Weight'  # Default


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted mean."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    return float(np.average(values[mask], weights=weights[mask]))


def weighted_std(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted standard deviation."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    avg = np.average(v, weights=w)
    variance = np.average((v - avg) ** 2, weights=w)
    return float(np.sqrt(variance))


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted median (50th percentile)."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    sorted_idx = np.argsort(v)
    v_sorted, w_sorted = v[sorted_idx], w[sorted_idx]
    cumsum = np.cumsum(w_sorted)
    cutoff = cumsum[-1] / 2.0
    return float(v_sorted[np.searchsorted(cumsum, cutoff)])


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    """Calculate weighted quantile."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    sorted_idx = np.argsort(v)
    v_sorted, w_sorted = v[sorted_idx], w[sorted_idx]
    cumsum = np.cumsum(w_sorted)
    cutoff = cumsum[-1] * q
    return float(v_sorted[np.searchsorted(cumsum, cutoff)])


def weighted_correlation(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted Pearson correlation coefficient."""
    mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(weights) | (weights <= 0))
    if mask.sum() < 3:
        return np.nan
    x_m, y_m, w = x[mask], y[mask], weights[mask]
    x_mean = np.average(x_m, weights=w)
    y_mean = np.average(y_m, weights=w)
    cov = np.average((x_m - x_mean) * (y_m - y_mean), weights=w)
    x_std = np.sqrt(np.average((x_m - x_mean) ** 2, weights=w))
    y_std = np.sqrt(np.average((y_m - y_mean) ** 2, weights=w))
    if x_std == 0 or y_std == 0:
        return np.nan
    return float(cov / (x_std * y_std))


def calc_weighted_stats_by_year(df: pd.DataFrame, col: str, weight_col: str) -> Dict[int, Dict]:
    """
    Calculate weighted statistics PER YEAR.

    ACS weights are calibrated to each survey year's population totals,
    so weights must be applied within each year, not across years.
    """
    # Import here to avoid circular dependency
    from .zero_exclusion import should_exclude_zeros

    if col not in df.columns or weight_col not in df.columns:
        return {}
    if 'Census_Year' not in df.columns:
        return {}

    results = {}
    numeric_col = pd.to_numeric(df[col], errors='coerce')
    numeric_weight = pd.to_numeric(df[weight_col], errors='coerce')

    # Filter zeros for economic columns
    if should_exclude_zeros(col):
        valid_mask = (numeric_col > 0) & numeric_col.notna() & numeric_weight.notna() & (numeric_weight > 0)
    else:
        valid_mask = numeric_col.notna() & numeric_weight.notna() & (numeric_weight > 0)

    df_valid = df[valid_mask].copy()
    df_valid['_val'] = numeric_col[valid_mask].values
    df_valid['_wgt'] = numeric_weight[valid_mask].values

    for year, group in df_valid.groupby('Census_Year'):
        v = group['_val'].values
        w = group['_wgt'].values
        if len(v) < 10:
            continue
        results[int(year)] = {
            'weighted_mean': weighted_mean(v, w),
            'weighted_median': weighted_median(v, w),
            'weighted_std': weighted_std(v, w),
            'weighted_q25': weighted_quantile(v, w, 0.25),
            'weighted_q75': weighted_quantile(v, w, 0.75),
            'unweighted_mean': float(np.mean(v)),
            'unweighted_median': float(np.median(v)),
            'n_obs': len(v),
            'sum_weights': float(np.sum(w))
        }

    return results

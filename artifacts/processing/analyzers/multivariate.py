"""
Multivariate analysis and hypothesis testing for Census ACS data
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any, Optional, Tuple
import warnings
# Suppress sklearn.utils.parallel warning (Python 3.13 compatibility)
warnings.filterwarnings('ignore', message='.*sklearn.utils.parallel.*')

# Optional sklearn imports with fallback
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

from ..base import BaseAnalyzer
from logging_config import get_logger


# ============================================================================
# MULTIVARIATE OUTLIER DETECTOR
# ============================================================================

class MultivariateOutlierDetector:
    """Multivariate outlier detection using multiple algorithms"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        from logging_config import get_logger
        self.logger = get_logger("processing.outlier_detector")

    def analyze(self, focus_vars: Optional[List[str]] = None,
                methods: List[str] = ['isolation_forest', 'mahalanobis']) -> Dict[str, Any]:
        """Detect outliers using multiple multivariate methods"""
        self.logger.debug(f"Detecting outliers with methods: {methods}")

        # Prepare data
        if focus_vars:
            available = [v for v in focus_vars if v in self.df.columns]
            df = self.df[available].select_dtypes(include=[np.number]).dropna()
        else:
            df = self.df.select_dtypes(include=[np.number]).dropna()

        if len(df) < 10 or df.shape[1] < 2:
            return {'error': 'Insufficient data for multivariate outlier detection'}

        results = {}

        if 'isolation_forest' in methods:
            results['isolation_forest'] = self._isolation_forest(df)

        if 'mahalanobis' in methods:
            results['mahalanobis'] = self._mahalanobis_distance(df)

        if 'lof' in methods:
            results['lof'] = self._local_outlier_factor(df)

        # Ensemble results
        results['ensemble'] = self._ensemble_outliers(results, len(df))
        return results

    def _isolation_forest(self, df: pd.DataFrame, contamination: float = 0.1) -> Dict:
        """Isolation Forest outlier detection"""
        try:
            from sklearn.ensemble import IsolationForest

            X = df.values
            clf = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
            predictions = clf.fit_predict(X)

            outlier_mask = predictions == -1
            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],  # Limit for memory
                'method': 'Isolation Forest',
                'contamination': contamination
            }
        except ImportError:
            return {'error': 'sklearn not available'}
        except Exception as e:
            self.logger.warning(f"Isolation Forest failed: {e}")
            return {'error': str(e)}

    def _mahalanobis_distance(self, df: pd.DataFrame, threshold: float = 3.0) -> Dict:
        """Mahalanobis distance outlier detection"""
        try:
            from scipy import stats

            X = df.values
            mean = np.mean(X, axis=0)
            cov = np.cov(X.T)

            # Handle singular covariance matrix
            try:
                cov_inv = np.linalg.inv(cov)
            except np.linalg.LinAlgError:
                cov_inv = np.linalg.pinv(cov)

            # Vectorized Mahalanobis distance calculation
            # d(x) = sqrt((x - mean).T @ cov_inv @ (x - mean))
            diff = X - mean  # Shape: (n_samples, n_features)
            # Compute (diff @ cov_inv) * diff for each row, then sum across features
            distances = np.sqrt(np.sum((diff @ cov_inv) * diff, axis=1))

            # Chi-squared threshold for multivariate outliers
            chi2_threshold = stats.chi2.ppf(0.975, df=X.shape[1])
            outlier_mask = distances > chi2_threshold

            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],
                'method': 'Mahalanobis Distance',
                'threshold': float(chi2_threshold),
                'mean_distance': float(np.mean(distances)),
                'max_distance': float(np.max(distances))
            }
        except Exception as e:
            self.logger.warning(f"Mahalanobis distance failed: {e}")
            return {'error': str(e)}

    def _local_outlier_factor(self, df: pd.DataFrame, n_neighbors: int = 20) -> Dict:
        """Local Outlier Factor detection"""
        try:
            from sklearn.neighbors import LocalOutlierFactor

            X = df.values
            clf = LocalOutlierFactor(n_neighbors=min(n_neighbors, len(X) - 1))
            predictions = clf.fit_predict(X)

            outlier_mask = predictions == -1
            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],
                'method': 'Local Outlier Factor',
                'n_neighbors': n_neighbors
            }
        except ImportError:
            return {'error': 'sklearn not available'}
        except Exception as e:
            self.logger.warning(f"LOF failed: {e}")
            return {'error': str(e)}

    def _ensemble_outliers(self, results: Dict, n_samples: int) -> Dict:
        """Combine multiple methods for robust outlier identification"""
        all_indices = set()
        method_counts = {}

        for method, result in results.items():
            if method == 'ensemble' or 'error' in result:
                continue
            indices = result.get('outlier_indices', [])
            for idx in indices:
                all_indices.add(idx)
                method_counts[idx] = method_counts.get(idx, 0) + 1

        # Points flagged by multiple methods are more likely outliers
        consensus_outliers = [idx for idx, count in method_counts.items() if count >= 2]

        return {
            'all_flagged': len(all_indices),
            'consensus_outliers': len(consensus_outliers),
            'consensus_percentage': float(len(consensus_outliers) / n_samples * 100) if n_samples > 0 else 0,
            'consensus_indices': consensus_outliers[:100]
        }


# ============================================================================
# HYPOTHESIS TESTING ANALYZER
# ============================================================================

class HypothesisTestingAnalyzer:
    """Statistical hypothesis testing with multiple comparison corrections"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        from logging_config import get_logger
        self.logger = get_logger("processing.hypothesis_testing")

    def test_group_differences(self, value_col: str, group_col: str,
                               correction: str = 'bonferroni') -> Dict[str, Any]:
        """Test differences between groups with correction for multiple comparisons"""
        self.logger.debug(f"Testing group differences: {value_col} by {group_col}")

        if value_col not in self.df.columns or group_col not in self.df.columns:
            return {'error': 'Columns not found'}

        try:
            from scipy import stats

            # Get groups
            groups = self.df.groupby(group_col)[value_col].apply(
                lambda x: x.dropna().tolist()
            ).to_dict()

            if len(groups) < 2:
                return {'error': 'Need at least 2 groups for comparison'}

            # Perform pairwise tests
            group_names = list(groups.keys())
            p_values = []
            comparisons = []

            for i in range(len(group_names)):
                for j in range(i + 1, len(group_names)):
                    g1, g2 = groups[group_names[i]], groups[group_names[j]]
                    if len(g1) > 1 and len(g2) > 1:
                        _, p_val = stats.mannwhitneyu(g1, g2, alternative='two-sided')
                        p_values.append(p_val)
                        comparisons.append((group_names[i], group_names[j]))

            # Apply correction
            if correction == 'bonferroni':
                corrected = self._bonferroni_correction(p_values)
            elif correction == 'fdr' or correction == 'bh':
                corrected = self._fdr_correction(p_values)
            elif correction == 'holm':
                corrected = self._holm_bonferroni(p_values)
            else:
                corrected = [(p, p < 0.05) for p in p_values]

            results = []
            for (g1, g2), (adj_p, significant) in zip(comparisons, corrected):
                results.append({
                    'group1': str(g1), 'group2': str(g2),
                    'adjusted_p': float(adj_p),
                    'significant': bool(significant)
                })

            return {
                'comparisons': results,
                'correction_method': correction,
                'n_comparisons': len(comparisons),
                'n_significant': sum(1 for _, sig in corrected if sig)
            }
        except Exception as e:
            self.logger.warning(f"Group difference test failed: {e}")
            return {'error': str(e)}

    def _bonferroni_correction(self, p_values: List[float],
                                alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Bonferroni correction - conservative"""
        n = len(p_values)
        return [(min(p * n, 1.0), p * n < alpha) for p in p_values]

    def _holm_bonferroni(self, p_values: List[float],
                         alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Holm-Bonferroni step-down procedure"""
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        adjusted = [0.0] * n
        significant = [False] * n

        for rank, idx in enumerate(sorted_indices):
            adj_p = min(p_values[idx] * (n - rank), 1.0)
            adjusted[idx] = adj_p
            significant[idx] = adj_p < alpha

        return list(zip(adjusted, significant))

    def _fdr_correction(self, p_values: List[float],
                        alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Benjamini-Hochberg FDR correction"""
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        adjusted = [0.0] * n

        # Calculate adjusted p-values
        prev_adj = 1.0
        for rank in range(n - 1, -1, -1):
            idx = sorted_indices[rank]
            adj_p = min(p_values[idx] * n / (rank + 1), prev_adj)
            adjusted[idx] = adj_p
            prev_adj = adj_p

        return [(adj, adj < alpha) for adj in adjusted]

    def normality_tests(self, cols: List[str]) -> Dict[str, Dict]:
        """Test normality with Shapiro-Wilk and other tests"""
        from ..utilities import should_exclude_zeros

        results = {}
        try:
            from scipy import stats

            for col in cols:
                if col not in self.df.columns:
                    continue

                series = pd.to_numeric(self.df[col], errors='coerce').dropna()
                if should_exclude_zeros(col):
                    series = series[series > 0]

                if len(series) < 8:
                    results[col] = {'error': 'Insufficient data'}
                    continue

                # Limit sample size for Shapiro-Wilk
                sample = series.sample(n=min(5000, len(series)), random_state=42)

                try:
                    shapiro_stat, shapiro_p = stats.shapiro(sample)
                    results[col] = {
                        'shapiro_statistic': float(shapiro_stat),
                        'shapiro_p_value': float(shapiro_p),
                        'is_normal': shapiro_p > 0.05,
                        'n_samples': len(sample)
                    }
                except Exception:
                    results[col] = {'error': 'Test failed'}

            return results
        except ImportError:
            return {'error': 'scipy not available'}

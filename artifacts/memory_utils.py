"""
Memory Monitoring Utilities for Census ACS EDA
Provides memory tracking, context managers, and cleanup utilities
"""
import gc
import os
import functools
from contextlib import contextmanager
from typing import Optional, Callable, Any
from datetime import datetime

import pandas as pd
import numpy as np

# Try importing psutil for memory monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Try importing matplotlib for figure management
try:
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False

from logging_config import get_logger

logger = get_logger("memory")


class MemoryMonitor:
    """Singleton memory monitor with logging capabilities"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.process = psutil.Process(os.getpid()) if PSUTIL_AVAILABLE else None
        self.log_file = None
        self.threshold_mb = 500  # Log when memory changes by 500MB
        self.last_memory_mb = 0
        self._initialized = True
        self._checkpoints: dict = {}

    def get_memory_mb(self) -> float:
        """Get current memory usage in MB"""
        if not PSUTIL_AVAILABLE:
            return 0.0
        return self.process.memory_info().rss / (1024 * 1024)

    def get_available_memory_mb(self) -> float:
        """Get available system memory in MB"""
        if not PSUTIL_AVAILABLE:
            return float('inf')
        return psutil.virtual_memory().available / (1024 * 1024)

    def log_memory(self, phase: str, force: bool = False) -> float:
        """Log memory usage with phase identifier"""
        current_mb = self.get_memory_mb()
        delta = current_mb - self.last_memory_mb

        if force or abs(delta) > self.threshold_mb:
            msg = f"{phase}: {current_mb:.1f}MB (delta: {delta:+.1f}MB)"
            logger.info(msg)

            if self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write(msg + '\n')

            self.last_memory_mb = current_mb

        return current_mb

    def set_checkpoint(self, name: str):
        """Set a memory checkpoint for later comparison"""
        self._checkpoints[name] = self.get_memory_mb()
        logger.debug(f"Checkpoint '{name}': {self._checkpoints[name]:.1f}MB")

    def get_delta_from_checkpoint(self, name: str) -> float:
        """Get memory delta from a named checkpoint"""
        if name not in self._checkpoints:
            return 0.0
        return self.get_memory_mb() - self._checkpoints[name]

    def clear_checkpoint(self, name: str):
        """Clear a specific checkpoint"""
        self._checkpoints.pop(name, None)

    def set_log_file(self, path: str):
        """Set file for memory logging"""
        self.log_file = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def set_threshold(self, threshold_mb: float):
        """Set the memory change threshold for logging"""
        self.threshold_mb = threshold_mb

    def collect_garbage(self, generations: int = 2) -> int:
        """Force garbage collection and return objects collected"""
        collected = gc.collect(generations)
        logger.debug(f"GC collected {collected} objects")
        return collected


# Global singleton instance
_monitor: Optional[MemoryMonitor] = None


def get_memory_monitor() -> MemoryMonitor:
    """Get or create the global memory monitor"""
    global _monitor
    if _monitor is None:
        _monitor = MemoryMonitor()
    return _monitor


def memory_tracked(phase: str = None):
    """Decorator to track memory before/after function execution"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor = get_memory_monitor()
            func_phase = phase or func.__name__

            monitor.log_memory(f"{func_phase}:START", force=True)
            try:
                result = func(*args, **kwargs)
                gc.collect()
                monitor.log_memory(f"{func_phase}:END", force=True)
                return result
            except Exception as e:
                monitor.log_memory(f"{func_phase}:ERROR", force=True)
                raise
        return wrapper
    return decorator


def log_dataframe_memory(df: pd.DataFrame, name: str = "DataFrame") -> float:
    """Log memory usage of a DataFrame"""
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    logger.info(f"{name}: {len(df):,} rows x {len(df.columns)} cols = {memory_mb:.1f}MB")
    return memory_mb


def get_dataframe_memory_mb(df: pd.DataFrame) -> float:
    """Get memory usage of a DataFrame in MB"""
    return df.memory_usage(deep=True).sum() / (1024 * 1024)


@contextmanager
def managed_figure(figsize: tuple = (10, 6), dpi: int = 150):
    """Context manager for matplotlib figures with guaranteed cleanup"""
    if not MPL_AVAILABLE:
        yield None
        return

    fig = None
    try:
        fig = plt.figure(figsize=figsize, dpi=dpi)
        yield fig
    finally:
        if fig is not None:
            plt.close(fig)
        gc.collect()


@contextmanager
def managed_dataframe(df: pd.DataFrame, sample_size: Optional[int] = None,
                      random_state: int = 42):
    """Context manager for DataFrame operations with memory cleanup"""
    working_df = None
    try:
        if sample_size and len(df) > sample_size:
            working_df = df.sample(n=sample_size, random_state=random_state)
            logger.debug(f"Sampled DataFrame: {len(df):,} -> {sample_size:,} rows")
        else:
            working_df = df
        yield working_df
    finally:
        if working_df is not None and working_df is not df:
            del working_df
        gc.collect()


@contextmanager
def memory_phase(phase_name: str, cleanup: bool = True):
    """Context manager for tracking memory phases"""
    monitor = get_memory_monitor()
    monitor.log_memory(f"{phase_name}:ENTER", force=True)
    try:
        yield monitor
    finally:
        if cleanup:
            gc.collect()
        monitor.log_memory(f"{phase_name}:EXIT", force=True)


def clear_matplotlib_cache():
    """Clear matplotlib caches to free memory"""
    if not MPL_AVAILABLE:
        return

    plt.close('all')

    # Clear font cache
    try:
        import matplotlib.font_manager as fm
        if hasattr(fm, '_font_manager'):
            fm._font_manager = None
        if hasattr(fm, 'fontManager'):
            fm.fontManager = None
    except Exception:
        pass

    gc.collect()
    logger.debug("Cleared matplotlib caches")


def clear_seaborn_cache():
    """Clear seaborn caches to free memory"""
    try:
        import seaborn as sns
        sns.reset_defaults()
        gc.collect()
        logger.debug("Reset seaborn defaults")
    except ImportError:
        pass


def clear_tensorflow_session():
    """Clear TensorFlow/Keras session to free memory"""
    try:
        import tensorflow as tf
        tf.keras.backend.clear_session()
        gc.collect()
        logger.debug("Cleared TensorFlow session")
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"Failed to clear TensorFlow session: {e}")


def clear_all_caches():
    """Clear all known caches to free memory"""
    # Clear visualization caches
    clear_matplotlib_cache()
    clear_seaborn_cache()

    # Clear TensorFlow session
    clear_tensorflow_session()

    # Clear visualizer cache if available
    try:
        from visualizations import clear_viz_cache
        clear_viz_cache()
    except ImportError:
        pass
    except Exception:
        pass

    # Force garbage collection
    gc.collect()
    logger.info("Cleared all caches")


def get_optimal_sample_size(df: pd.DataFrame, target_memory_mb: float = 1000,
                            min_rows: int = 1000, max_rows: int = 100000) -> int:
    """Calculate optimal sample size based on target memory usage"""
    if len(df) == 0:
        return 0

    # Estimate memory per row
    current_memory = get_dataframe_memory_mb(df)
    memory_per_row = current_memory / len(df)

    # Calculate target rows
    if memory_per_row > 0:
        target_rows = int(target_memory_mb / memory_per_row)
    else:
        target_rows = max_rows

    # Clamp to bounds
    target_rows = max(min_rows, min(target_rows, max_rows, len(df)))

    logger.debug(f"Optimal sample: {target_rows:,} rows for {target_memory_mb}MB target")
    return target_rows


def adaptive_sample(df: pd.DataFrame, survey_type: str = "population",
                    random_state: int = 42,
                    force_max_rows: Optional[int] = None) -> pd.DataFrame:
    """
    Adaptively sample DataFrame based on available memory and survey type.

    Args:
        df: Input DataFrame
        survey_type: "population" or "housing"
        random_state: Random seed for reproducibility
        force_max_rows: If set, forces sampling to this size regardless of memory
                       (use for ML tuning where parallel workers multiply memory)
    """
    monitor = get_memory_monitor()
    available_mb = monitor.get_available_memory_mb()

    # Force sampling if explicitly requested (e.g., for GridSearchCV)
    if force_max_rows is not None and len(df) > force_max_rows:
        logger.info(f"[FORCED] Sampling: {len(df):,} -> {force_max_rows:,} rows")
        return df.sample(n=force_max_rows, random_state=random_state)

    # Skip sampling entirely if 16GB+ available
    if available_mb >= 16000:
        logger.debug(f"Skipping sampling: {available_mb:.0f}MB available (>16GB)")
        return df

    # Determine target based on available memory and survey type
    if survey_type.lower() == "housing":
        # Housing surveys tend to have more columns and need more aggressive sampling
        if available_mb < 4000:
            target_rows = 5000
        elif available_mb < 8000:
            target_rows = 10000
        else:
            target_rows = 20000
    else:
        # Population surveys can handle larger samples
        if available_mb < 4000:
            target_rows = 10000
        elif available_mb < 8000:
            target_rows = 25000
        else:
            target_rows = 50000

    if len(df) > target_rows:
        logger.info(f"Adaptive sampling: {len(df):,} -> {target_rows:,} rows "
                   f"(available: {available_mb:.0f}MB)")
        return df.sample(n=target_rows, random_state=random_state)

    return df


def get_available_memory_gb() -> float:
    """Get available system memory in GB (standalone helper)."""
    monitor = get_memory_monitor()
    return monitor.get_available_memory_mb() / 1024


class MemoryGuard:
    """Context manager that raises if memory usage exceeds threshold"""

    def __init__(self, max_memory_mb: float = 8000, action: str = "warn"):
        """
        Args:
            max_memory_mb: Maximum memory usage allowed
            action: "warn" to log warning, "raise" to raise MemoryError
        """
        self.max_memory_mb = max_memory_mb
        self.action = action
        self.monitor = get_memory_monitor()

    def __enter__(self):
        self.start_memory = self.monitor.get_memory_mb()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_memory = self.monitor.get_memory_mb()
        if current_memory > self.max_memory_mb:
            msg = f"Memory usage ({current_memory:.1f}MB) exceeded threshold ({self.max_memory_mb}MB)"
            if self.action == "raise":
                raise MemoryError(msg)
            else:
                logger.warning(msg)
        return False

    def check(self):
        """Manually check memory usage"""
        current_memory = self.monitor.get_memory_mb()
        if current_memory > self.max_memory_mb:
            msg = f"Memory usage ({current_memory:.1f}MB) exceeded threshold ({self.max_memory_mb}MB)"
            if self.action == "raise":
                raise MemoryError(msg)
            else:
                logger.warning(msg)
                return False
        return True


def get_safe_sample_size_quadratic(n_samples: int, n_features: int = 10,
                                    max_memory_gb: float = 4.0) -> int:
    """
    Calculate safe sample size for O(n²) algorithms like hierarchical clustering.

    Memory needed: n² * 8 bytes (float64 distance matrix)

    Following pattern from processing/analyzers/multivariate.py:311 which samples
    before expensive operations.

    Args:
        n_samples: Current number of samples
        n_features: Number of features (unused but kept for API consistency)
        max_memory_gb: Maximum memory to use for distance matrix (default 4GB)

    Returns:
        Safe sample size that won't exceed memory limit
    """
    # Distance matrix is n x n x 8 bytes (float64)
    max_bytes = max_memory_gb * 1024 * 1024 * 1024
    max_n = int(np.sqrt(max_bytes / 8))

    # Cap at reasonable limit: 15k samples = ~1.8GB distance matrix
    safe_n = min(n_samples, max_n, 15000)

    if safe_n < n_samples:
        original_memory_gb = (n_samples ** 2 * 8) / (1024 ** 3)
        logger.info(f"[MEMORY] O(n²) safe sample: {n_samples:,} -> {safe_n:,} "
                   f"(distance matrix would be {original_memory_gb:.1f}GB)")

    return safe_n


def get_safe_shap_sample_size(n_samples: int, n_features: int = 10,
                               n_estimators: int = 100,
                               max_memory_gb: float = 2.0,
                               balanced: bool = True) -> int:
    """
    Calculate safe sample size for SHAP TreeExplainer.

    SHAP TreeExplainer memory: O(n_samples * n_features * n_estimators)
    For balanced mode, caps at 1000 samples for good statistical properties.

    Args:
        n_samples: Current number of samples
        n_features: Number of features
        n_estimators: Number of trees in ensemble
        max_memory_gb: Maximum memory budget for SHAP computation
        balanced: If True, use balanced defaults (1000 samples)

    Returns:
        Safe sample size for SHAP computation
    """
    if balanced:
        # Balanced mode: 1000 samples gives good feature importance estimates
        safe_n = min(n_samples, 1000)
    else:
        # Memory-based calculation
        # Each SHAP value is float64 (8 bytes), need n_samples * n_features
        max_bytes = max_memory_gb * 1024 * 1024 * 1024
        bytes_per_sample = n_features * 8 * 2  # SHAP values + computation overhead
        safe_n = min(n_samples, int(max_bytes / bytes_per_sample), 2000)

    if safe_n < n_samples:
        logger.info(f"[SHAP] Safe sample size: {n_samples:,} -> {safe_n:,}")

    return max(safe_n, 100)  # Minimum 100 for statistical validity


def get_ml_tuning_sample_limit(n_samples: int, n_combinations: int = 24,
                                n_cv_folds: int = 5,
                                n_jobs: int = -1) -> int:
    """
    Calculate safe sample size for GridSearchCV hyperparameter tuning.

    GridSearchCV with n_jobs=-1 spawns parallel workers, each holding data copies.
    This causes OOM even when available memory appears sufficient.

    Pattern follows get_safe_sample_size_quadratic() and get_safe_shap_sample_size().

    Args:
        n_samples: Current number of samples
        n_combinations: Number of parameter combinations in grid
        n_cv_folds: Number of cross-validation folds
        n_jobs: Number of parallel jobs (-1 = all cores)

    Returns:
        Safe maximum sample size for tuning
    """
    total_fits = n_combinations * n_cv_folds

    # Adaptive limits based on grid complexity
    if total_fits > 100:
        safe_n = 25_000   # Very complex grid
    elif total_fits > 50:
        safe_n = 50_000   # Complex grid (RF/GB with 24 combos × 5 folds)
    elif total_fits > 20:
        safe_n = 100_000  # Medium grid
    else:
        safe_n = 200_000  # Simple grid (ridge/lasso)

    if safe_n < n_samples:
        logger.info(f"[ML-TUNE] Limiting samples: {n_samples:,} -> {safe_n:,} "
                   f"({total_fits} total fits from {n_combinations} combos × {n_cv_folds} folds)")

    return min(n_samples, safe_n)

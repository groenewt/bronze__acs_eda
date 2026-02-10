"""
Machine Learning Models Package for Census Data Analysis
Provides comprehensive predictive modeling, clustering, and evaluation capabilities
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

from .base import (
    BaseMLModel,
    ModelResults,
    ClusterResults,
    SKLEARN_AVAILABLE,
    SHAP_AVAILABLE
)

from .feature_groups import (
    FEATURE_GROUPS,
    get_domain_features,
    get_all_domain_features
)

# Import model classes with graceful fallback for not-yet-implemented modules
__all__ = [
    # Base classes and data structures
    'BaseMLModel',
    'ModelResults',
    'ClusterResults',
    'SKLEARN_AVAILABLE',
    'SHAP_AVAILABLE',

    # Feature groups
    'FEATURE_GROUPS',
    'get_domain_features',
    'get_all_domain_features',
]

try:
    from .regression import RegressionModeler
    __all__.append('RegressionModeler')
except ImportError:
    pass

try:
    from .classification import ClassificationModeler
    __all__.append('ClassificationModeler')
except ImportError:
    pass

try:
    from .clustering import ClusteringModeler
    __all__.append('ClusteringModeler')
except ImportError:
    pass

try:
    from .timeseries import TimeSeriesForecaster
    __all__.append('TimeSeriesForecaster')
except ImportError:
    pass

try:
    from .comparison import ModelComparator
    __all__.append('ModelComparator')
except ImportError:
    pass

try:
    from .explainability import ModelExplainer
    __all__.append('ModelExplainer')
except ImportError:
    pass

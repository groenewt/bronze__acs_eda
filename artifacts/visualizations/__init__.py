"""Visualizations package for ACS EDA

This package provides a comprehensive suite of visualizations for exploring
American Community Survey (ACS) data. It includes:

- Temporal analysis (trends over time)
- Economic metrics (income, property values, costs)
- Correlations and relationships
- Statistical distributions
- Outlier detection and anomaly analysis
- Demographics (age, education, citizenship)
- Housing characteristics and affordability
- Transportation patterns
- Income composition
- Technology adoption
- Multi-variable interactions
- Machine learning visualizations

The main entry point is the `Visualizer` class which orchestrates all
visualization types.
"""

from .base import BaseVisualizer, clear_viz_cache, enable_debug_logging
from .formatting import (
    configure_axes,
    format_pie_chart,
    tight_layout_safe,
    smart_legend,
    subplots_with_spacing,
    FIGURE_SIZES
)
from .orchestrator import Visualizer
from .temporal import TemporalVisualizer
from .economic import EconomicVisualizer
from .correlation import CorrelationVisualizer
from .statistical import StatisticalVisualizer, AdvancedVisualizer
from .outlier import YoYChangeVisualizer, OutlierVisualizer
from .demographics import DemographicsVisualizer, RaceEthnicityVisualizer
from .housing import (
    HousingCharacteristicsVisualizer,
    HouseholdCompositionVisualizer,
    CostBurdenVisualizer
)
from .transport import TransportationVisualizer
from .income import IncomeCompositionVisualizer
from .technology import TechnologyAdoptionVisualizer
from .interactions import MultiVariableVisualizer, EnhancedFeatureInteractionVisualizer
from .distributions import DistributionComparisonVisualizer
from .ml import MLVisualizer

# Conditional imports for new visualizers
try:
    from .inequality import InequalityVisualizer
    _has_inequality = True
except ImportError:
    _has_inequality = False

try:
    from .occupation_industry import OccupationIndustryVisualizer
    _has_occupation = True
except ImportError:
    _has_occupation = False

try:
    from .health_insurance import HealthInsuranceVisualizer
    _has_health_insurance = True
except ImportError:
    _has_health_insurance = False

try:
    from .disability import DisabilityVisualizer
    _has_disability = True
except ImportError:
    _has_disability = False

try:
    from .education_field import EducationFieldVisualizer
    _has_education_field = True
except ImportError:
    _has_education_field = False

__all__ = [
    # Main orchestrator
    'Visualizer',

    # Base classes and utilities
    'BaseVisualizer',
    'clear_viz_cache',
    'enable_debug_logging',

    # Formatting utilities
    'configure_axes',
    'format_pie_chart',
    'tight_layout_safe',
    'smart_legend',
    'subplots_with_spacing',
    'FIGURE_SIZES',

    # Temporal analysis
    'TemporalVisualizer',

    # Economic visualizers
    'EconomicVisualizer',

    # Correlation and relationships
    'CorrelationVisualizer',

    # Statistical visualizers
    'StatisticalVisualizer',
    'AdvancedVisualizer',

    # Outlier and anomaly detection
    'YoYChangeVisualizer',
    'OutlierVisualizer',

    # Demographics
    'DemographicsVisualizer',
    'RaceEthnicityVisualizer',

    # Housing
    'HousingCharacteristicsVisualizer',
    'HouseholdCompositionVisualizer',
    'CostBurdenVisualizer',

    # Transportation
    'TransportationVisualizer',

    # Income
    'IncomeCompositionVisualizer',

    # Technology
    'TechnologyAdoptionVisualizer',

    # Interactions
    'MultiVariableVisualizer',
    'EnhancedFeatureInteractionVisualizer',

    # Distributions
    'DistributionComparisonVisualizer',

    # Machine Learning
    'MLVisualizer',
]

# Conditionally add new visualizers to __all__
if _has_inequality:
    __all__.append('InequalityVisualizer')

if _has_occupation:
    __all__.append('OccupationIndustryVisualizer')

if _has_health_insurance:
    __all__.append('HealthInsuranceVisualizer')

if _has_disability:
    __all__.append('DisabilityVisualizer')

if _has_education_field:
    __all__.append('EducationFieldVisualizer')

"""
Report Sections Module
Individual section generators for each analysis type.
"""

from .overview import OverviewSection
from .temporal import TemporalSection
from .economic import EconomicSection
from .statistics import StatisticsSection
from .correlation import CorrelationSection
from .cross_variable import CrossVariableSection
from .outlier import OutlierSection
from .anomaly import AnomalySection
from .trend import TrendSection
from .feature_eng import FeatureEngineeringSection
from .ml_models import MLModelsSection
from .deep_learning import DeepLearningSection
from .disability import DisabilitySection
from .health_insurance import HealthInsuranceSection
from .occupation_industry import OccupationIndustrySection
from .education_field import EducationFieldSection
from .llm_insights import (
    LLMDataQualitySection,
    LLMPolicyRecommendationsSection,
    LLMTemporalInsightsSection,
    LLMEconomicInsightsSection,
    LLMCorrelationInsightsSection,
    LLMStatisticalInsightsSection,
    LLMOutlierInsightsSection,
    LLMAnomalyInsightsSection,
    LLMTrendInsightsSection,
    LLMDeepLearningInsightsSection,
    LLMDisabilityInsightsSection,
    LLMHealthInsuranceInsightsSection,
    LLMOccupationIndustryInsightsSection,
    LLMEducationFieldInsightsSection
)

__all__ = [
    'OverviewSection',
    'TemporalSection',
    'EconomicSection',
    'StatisticsSection',
    'CorrelationSection',
    'CrossVariableSection',
    'OutlierSection',
    'AnomalySection',
    'TrendSection',
    'FeatureEngineeringSection',
    'MLModelsSection',
    'DeepLearningSection',
    'DisabilitySection',
    'HealthInsuranceSection',
    'OccupationIndustrySection',
    'EducationFieldSection',
    'LLMDataQualitySection',
    'LLMPolicyRecommendationsSection',
    'LLMTemporalInsightsSection',
    'LLMEconomicInsightsSection',
    'LLMCorrelationInsightsSection',
    'LLMStatisticalInsightsSection',
    'LLMOutlierInsightsSection',
    'LLMAnomalyInsightsSection',
    'LLMTrendInsightsSection',
    'LLMDeepLearningInsightsSection',
    'LLMDisabilityInsightsSection',
    'LLMHealthInsuranceInsightsSection',
    'LLMOccupationIndustryInsightsSection',
    'LLMEducationFieldInsightsSection'
]

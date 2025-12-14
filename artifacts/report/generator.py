"""
Report Generator - Main orchestrator for report generation.
"""

from typing import Dict, List, Tuple, Any

from config import Config, ProcessingStats
from report.toc import TableOfContentsSection
from report.sections import (
    OverviewSection,
    TemporalSection,
    EconomicSection,
    StatisticsSection,
    CorrelationSection,
    CrossVariableSection,
    OutlierSection,
    AnomalySection,
    TrendSection,
    FeatureEngineeringSection,
    MLModelsSection,
    DeepLearningSection,
    DisabilitySection,
    HealthInsuranceSection,
    OccupationIndustrySection,
    EducationFieldSection,
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


class ReportGenerator:
    """Main report generator coordinating all sections."""

    def __init__(self, config: Config):
        self.config = config
        self._init_sections()

    def _init_sections(self):
        """Initialize all section generators."""
        self.sections = {
            'toc': TableOfContentsSection(self.config),
            'overview': OverviewSection(self.config),
            'temporal': TemporalSection(self.config),
            'economic': EconomicSection(self.config),
            'statistics': StatisticsSection(self.config),
            'correlation': CorrelationSection(self.config),
            'cross_var': CrossVariableSection(self.config),
            'outlier': OutlierSection(self.config),
            'anomaly': AnomalySection(self.config),
            'trend': TrendSection(self.config),
            'feature_eng': FeatureEngineeringSection(self.config),
            'ml': MLModelsSection(self.config),
            'dl': DeepLearningSection(self.config),
            'disability': DisabilitySection(self.config),
            'health_insurance': HealthInsuranceSection(self.config),
            'occupation_industry': OccupationIndustrySection(self.config),
            'education_field': EducationFieldSection(self.config),
            'llm_data_quality': LLMDataQualitySection(self.config),
            'llm_policy': LLMPolicyRecommendationsSection(self.config),
            'llm_temporal': LLMTemporalInsightsSection(self.config),
            'llm_economic': LLMEconomicInsightsSection(self.config),
            'llm_correlation': LLMCorrelationInsightsSection(self.config),
            'llm_statistical': LLMStatisticalInsightsSection(self.config),
            'llm_outlier': LLMOutlierInsightsSection(self.config),
            'llm_anomaly': LLMAnomalyInsightsSection(self.config),
            'llm_trend': LLMTrendInsightsSection(self.config),
            'llm_deep_learning': LLMDeepLearningInsightsSection(self.config),
            'llm_disability': LLMDisabilityInsightsSection(self.config),
            'llm_health_insurance': LLMHealthInsuranceInsightsSection(self.config),
            'llm_occupation_industry': LLMOccupationIndustryInsightsSection(self.config),
            'llm_education_field': LLMEducationFieldInsightsSection(self.config)
        }

    def generate(self, stats: ProcessingStats, temporal: Dict,
                 llm_results: Dict, economic: Dict = None,
                 correlations: Dict = None, statistics: Dict = None,
                 outliers: Dict = None, anomalies: Dict = None,
                 trends: Dict = None, feature_eng: Dict = None,
                 ml_results: Dict = None, cross_var: Dict = None,
                 dl_results: Dict = None) -> str:
        """
        Generate all report sections.

        Args:
            stats: Processing statistics
            temporal: Temporal analysis data
            llm_results: LLM-generated insights
            economic: Economic analysis data
            correlations: Correlation analysis data
            statistics: Statistical analysis data
            outliers: Outlier detection data
            anomalies: Anomaly detection data
            trends: Trend analysis data
            feature_eng: Feature engineering data
            ml_results: ML model results
            cross_var: Cross-variable analysis data
            dl_results: Deep learning results

        Returns:
            Summary string of generated sections
        """
        results = []
        section_metadata = []  # List of tuples: (display_name, filename)

        # Generate core sections
        results.extend(self._gen_overview(stats))
        section_metadata.append(("Overview", self.sections['overview'].get_filename()))

        if temporal and not temporal.get('skipped'):
            results.extend(self._gen_temporal(temporal))
            section_metadata.append(("Temporal Analysis", self.sections['temporal'].get_filename()))

        if economic and not economic.get('skipped'):
            results.extend(self._gen_economic(economic))
            section_metadata.append(("Economic Analysis", self.sections['economic'].get_filename()))

        if statistics and not statistics.get('skipped'):
            results.extend(self._gen_statistics(statistics))
            section_metadata.append(("Statistical Analysis", self.sections['statistics'].get_filename()))

        if correlations and not correlations.get('skipped'):
            results.extend(self._gen_correlation(correlations))
            section_metadata.append(("Correlation Analysis", self.sections['correlation'].get_filename()))

        if cross_var and not cross_var.get('skipped'):
            results.extend(self._gen_cross_var(cross_var))
            section_metadata.append(("Cross-Variable Analysis", self.sections['cross_var'].get_filename()))

        if outliers and not outliers.get('skipped'):
            results.extend(self._gen_outlier(outliers))
            section_metadata.append(("Outlier Detection", self.sections['outlier'].get_filename()))

        if anomalies and not anomalies.get('skipped'):
            results.extend(self._gen_anomaly(anomalies))
            section_metadata.append(("Anomaly Detection", self.sections['anomaly'].get_filename()))

        if trends and not trends.get('skipped'):
            results.extend(self._gen_trend(trends))
            section_metadata.append(("Trend Analysis", self.sections['trend'].get_filename()))

        if feature_eng and not feature_eng.get('skipped'):
            results.extend(self._gen_feature_eng(feature_eng))
            section_metadata.append(("Feature Engineering", self.sections['feature_eng'].get_filename()))

        if ml_results and not ml_results.get('skipped'):
            results.extend(self._gen_ml(ml_results))
            section_metadata.append(("ML Models", self.sections['ml'].get_filename()))

        if dl_results and not dl_results.get('skipped'):
            results.extend(self._gen_dl(dl_results))
            section_metadata.append(("Deep Learning Models", self.sections['dl'].get_filename()))

        # Generate LLM subsections
        llm_sections = self._gen_llm_sections(llm_results, section_metadata)
        results.extend(llm_sections)

        # Generate and save TOC (last but appears first in output)
        results.extend(self._gen_toc(section_metadata))

        return f"Generated {len(results)} report sections"

    def _gen_overview(self, stats: ProcessingStats) -> List[str]:
        """Generate overview section."""
        try:
            data = {'stats': stats}
            content = self.sections['overview'].generate(data)
            path = self.sections['overview'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Overview section failed: {e}")
            return []

    def _gen_temporal(self, temporal: Dict) -> List[str]:
        """Generate temporal section."""
        try:
            content = self.sections['temporal'].generate(temporal)
            path = self.sections['temporal'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Temporal section failed: {e}")
            return []

    def _gen_economic(self, economic: Dict) -> List[str]:
        """Generate economic section."""
        try:
            content = self.sections['economic'].generate(economic)
            path = self.sections['economic'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Economic section failed: {e}")
            return []

    def _gen_statistics(self, statistics: Dict) -> List[str]:
        """Generate statistics section."""
        try:
            content = self.sections['statistics'].generate(statistics)
            path = self.sections['statistics'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Statistics section failed: {e}")
            return []

    def _gen_correlation(self, correlations: Dict) -> List[str]:
        """Generate correlation section."""
        try:
            content = self.sections['correlation'].generate(correlations)
            path = self.sections['correlation'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Correlation section failed: {e}")
            return []

    def _gen_cross_var(self, cross_var: Dict) -> List[str]:
        """Generate cross-variable section."""
        try:
            content = self.sections['cross_var'].generate(cross_var)
            path = self.sections['cross_var'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Cross-variable section failed: {e}")
            return []

    def _gen_outlier(self, outliers: Dict) -> List[str]:
        """Generate outlier section."""
        try:
            content = self.sections['outlier'].generate(outliers)
            path = self.sections['outlier'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Outlier section failed: {e}")
            return []

    def _gen_anomaly(self, anomalies: Dict) -> List[str]:
        """Generate anomaly section."""
        try:
            content = self.sections['anomaly'].generate(anomalies)
            path = self.sections['anomaly'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Anomaly section failed: {e}")
            return []

    def _gen_trend(self, trends: Dict) -> List[str]:
        """Generate trend section."""
        try:
            content = self.sections['trend'].generate(trends)
            path = self.sections['trend'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Trend section failed: {e}")
            return []

    def _gen_feature_eng(self, feature_eng: Dict) -> List[str]:
        """Generate feature engineering section."""
        try:
            content = self.sections['feature_eng'].generate(feature_eng)
            path = self.sections['feature_eng'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Feature engineering section failed: {e}")
            return []

    def _gen_ml(self, ml_results: Dict) -> List[str]:
        """Generate ML section."""
        try:
            content = self.sections['ml'].generate(ml_results)
            path = self.sections['ml'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] ML section failed: {e}")
            return []

    def _gen_dl(self, dl_results: Dict) -> List[str]:
        """Generate deep learning section."""
        try:
            content = self.sections['dl'].generate(dl_results)
            path = self.sections['dl'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Deep Learning section failed: {e}")
            return []

    def _gen_llm_sections(self, llm_results: Dict, section_metadata: List[Tuple[str, str]]) -> List[str]:
        """Generate all LLM subsections as separate files."""
        results = []

        # Define LLM subsections with their keys and display names
        llm_subsections = [
            ('llm_data_quality', 'LLM: Data Quality'),
            ('llm_policy', 'LLM: Policy Recommendations'),
            ('llm_temporal', 'LLM: Temporal Insights'),
            ('llm_economic', 'LLM: Economic Insights'),
            ('llm_correlation', 'LLM: Correlation Insights'),
            ('llm_statistical', 'LLM: Statistical Insights'),
            ('llm_outlier', 'LLM: Outlier Insights'),
            ('llm_anomaly', 'LLM: Anomaly Insights'),
            ('llm_trend', 'LLM: Trend Insights'),
            ('llm_deep_learning', 'LLM: Deep Learning Insights'),
            ('llm_disability', 'LLM: Disability Insights'),
            ('llm_health_insurance', 'LLM: Health Insurance Insights'),
            ('llm_occupation_industry', 'LLM: Occupation/Industry Insights'),
            ('llm_education_field', 'LLM: Education Field Insights')
        ]

        for section_key, display_name in llm_subsections:
            try:
                content = self.sections[section_key].generate(llm_results)
                # Only save and add to TOC if content is not None (i.e., data exists)
                if content is not None:
                    path = self.sections[section_key].save(content)
                    results.append(path)
                    filename = self.sections[section_key].get_filename()
                    section_metadata.append((display_name, filename))
            except Exception as e:
                print(f"[WARNING] {display_name} section failed: {e}")

        return results

    def _gen_toc(self, section_metadata: List[Tuple[str, str]]) -> List[str]:
        """Generate table of contents."""
        try:
            data = {'sections': section_metadata}
            content = self.sections['toc'].generate(data)
            path = self.sections['toc'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] TOC generation failed: {e}")
            return []

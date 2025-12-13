"""
LLM Insights Sections - AI-generated analysis and recommendations.
"""

from typing import Dict, Any

from report.base import BaseReportSection


class BaseLLMSection(BaseReportSection):
    """Base class for LLM insight sections."""

    def _format_llm_header(self, title: str) -> str:
        """Format LLM section header with model info."""
        return self.md.h1(
            f"model: {self.config.llm_model}, Engine: {self.config.llm_engine}, "
            f"GPU: {self.config.llm_gpu} -- AI-Generated Insights: {title}"
        )


class LLMDataQualitySection(BaseLLMSection):
    """LLM Data Quality Assessment section."""

    def get_filename(self) -> str:
        return "12_llm_data_quality.md"

    def generate(self, data: Dict) -> str:
        quality = data.get('data_quality', '')
        content = [self._format_llm_header("Data Quality")]

        if quality and quality != 'N/A':
            content.append(quality)
        else:
            content.append("_No data quality assessment available._")

        return "\n".join(content) + "\n"


class LLMPolicyRecommendationsSection(BaseLLMSection):
    """LLM Policy Recommendations section."""

    def get_filename(self) -> str:
        return "13_llm_policy_recommendations.md"

    def generate(self, data: Dict) -> str:
        recs = data.get('recommendations', '') or data.get('policy_recommendations', '')
        content = [self._format_llm_header("Policy Recommendations")]

        if recs and recs != 'N/A':
            content.append(recs)
        else:
            content.append("_No policy recommendations available._")

        return "\n".join(content) + "\n"


class LLMTemporalInsightsSection(BaseLLMSection):
    """LLM Temporal Analysis Insights section."""

    def get_filename(self) -> str:
        return "14_llm_temporal_insights.md"

    def generate(self, data: Dict) -> str:
        insights = data.get('temporal_insights', '')
        if not insights or insights == 'N/A':
            return None

        content = [self._format_llm_header("Temporal Analysis")]
        content.append(insights)

        return "\n".join(content) + "\n"


class LLMEconomicInsightsSection(BaseLLMSection):
    """LLM Economic Analysis Insights section."""

    def get_filename(self) -> str:
        return "15_llm_economic_insights.md"

    def generate(self, data: Dict) -> str:
        analysis = data.get('economic_analysis', '')
        if not analysis or analysis == 'N/A':
            return None

        content = [self._format_llm_header("Economic Analysis")]
        content.append(analysis)

        return "\n".join(content) + "\n"


class LLMCorrelationInsightsSection(BaseLLMSection):
    """LLM Correlation Insights section."""

    def get_filename(self) -> str:
        return "16_llm_correlation_insights.md"

    def generate(self, data: Dict) -> str:
        insights = data.get('correlation_insights', '')
        if not insights or insights == 'N/A':
            return None

        content = [self._format_llm_header("Correlation Analysis")]
        content.append(insights)

        return "\n".join(content) + "\n"


class LLMStatisticalInsightsSection(BaseLLMSection):
    """LLM Statistical Analysis Insights section."""

    def get_filename(self) -> str:
        return "17_llm_statistical_insights.md"

    def generate(self, data: Dict) -> str:
        analysis = data.get('statistical_analysis', '')
        if not analysis or analysis == 'N/A':
            return None

        content = [self._format_llm_header("Statistical Analysis")]
        content.append(analysis)

        return "\n".join(content) + "\n"


class LLMOutlierInsightsSection(BaseLLMSection):
    """LLM Outlier Analysis Insights section."""

    def get_filename(self) -> str:
        return "18_llm_outlier_insights.md"

    def generate(self, data: Dict) -> str:
        analysis = data.get('outlier_analysis', '')
        if not analysis or analysis == 'N/A':
            return None

        content = [self._format_llm_header("Outlier Analysis")]
        content.append(analysis)

        return "\n".join(content) + "\n"


class LLMAnomalyInsightsSection(BaseLLMSection):
    """LLM Anomaly Detection Insights section."""

    def get_filename(self) -> str:
        return "19_llm_anomaly_insights.md"

    def generate(self, data: Dict) -> str:
        detection = data.get('anomaly_detection', '')
        if not detection or detection == 'N/A':
            return None

        content = [self._format_llm_header("Anomaly Detection")]
        content.append(detection)

        return "\n".join(content) + "\n"


class LLMTrendInsightsSection(BaseLLMSection):
    """LLM Trend Analysis Insights section."""

    def get_filename(self) -> str:
        return "20_llm_trend_insights.md"

    def generate(self, data: Dict) -> str:
        analysis = data.get('trend_analysis', '')
        if not analysis or analysis == 'N/A':
            return None

        content = [self._format_llm_header("Trend Analysis")]
        content.append(analysis)

        return "\n".join(content) + "\n"


class LLMDeepLearningInsightsSection(BaseLLMSection):
    """LLM Deep Learning Analysis Insights section."""

    def get_filename(self) -> str:
        return "21_llm_deep_learning_insights.md"

    def generate(self, data: Dict) -> str:
        insights = data.get('deep_learning_insights', '')
        if not insights or insights == 'N/A':
            return None

        content = [self._format_llm_header("Deep Learning Analysis")]
        content.append(insights)

        return "\n".join(content) + "\n"

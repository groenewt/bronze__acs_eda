import os
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

from config import Config, ProcessingStats
from exceptions import ReportError, ReportGenerationError, ReportSaveError
from visual_registry import get_registry


class MarkdownFormatter:
    """Utility for MD formatting"""
    
    @staticmethod
    def h1(text: str) -> str:
        return f"# {text}\n"
    
    @staticmethod
    def h2(text: str) -> str:
        return f"## {text}\n"
    
    @staticmethod
    def h3(text: str) -> str:
        return f"### {text}\n"
    
    @staticmethod
    def bold(text: str) -> str:
        return f"**{text}**"
    
    @staticmethod
    def italic(text: str) -> str:
        return f"*{text}*"
    
    @staticmethod
    def code_block(text: str, lang: str = "") -> str:
        return f"```{lang}\n{text}\n```\n"
    
    @staticmethod
    def bullet(text: str) -> str:
        return f"- {text}\n"
    
    @staticmethod
    def link(text: str, url: str) -> str:
        return f"[{text}]({url})"
    
    @staticmethod
    def horizontal_rule() -> str:
        return "---\n"
    
    @staticmethod
    def table_row(cells: List[str]) -> str:
        return f"| {' | '.join(cells)} |\n"
    
    @staticmethod
    def table_separator(num_cols: int) -> str:
        return f"| {' | '.join(['---'] * num_cols)} |\n"


class BaseReportSection(ABC):
    """Abstract base for report sections"""
    
    def __init__(self, config: Config):
        self.config = config
        self.md = MarkdownFormatter()
    
    @abstractmethod
    def generate(self, data: Any) -> str:
        """Generate section content"""
        pass
    
    @abstractmethod
    def get_filename(self) -> str:
        """Get section filename"""
        pass
    
    def save(self, content: str) -> str:
        """Save section to file"""
        try:
            filepath = self._get_filepath()
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception as e:
            raise ReportSaveError(filepath, str(e))
    
    def _get_filepath(self) -> str:
        return os.path.join(self.config.output_dir, self.get_filename())
    
    def _link_images(self, image_dir: str, pattern: str = "*.png") -> List[str]:
        """Find and create markdown links for images (recursively in subdirectories)"""
        import glob
        fig_path = os.path.join(self.config.figure_dir, image_dir)
        # Use ** for recursive search in subdirectories
        imgs = glob.glob(os.path.join(fig_path, "**", pattern), recursive=True)
        # Also include images in the immediate directory
        imgs.extend(glob.glob(os.path.join(fig_path, pattern)))
        links = []
        for img in sorted(set(imgs)):
            # Use relative path from report location (figures/...)
            # Report is saved in output_dir, figures are in output_dir/figures/
            rel_path = os.path.relpath(img, self.config.output_dir)
            name = os.path.basename(img).replace('_', ' ').replace('.png', '')
            # Include subdirectory name in the image caption for context
            subdir = os.path.basename(os.path.dirname(img))
            if subdir and subdir != os.path.basename(fig_path):
                name = f"{subdir} - {name}"
            links.append(f"![{name}]({rel_path})")
        return links
    
    def _embed_image(self, rel_path: str, alt_text: str = "") -> str:
        """Create markdown image embed"""
        return f"![{alt_text}]({rel_path})"

    def _link_from_registry(self, **filters) -> List[str]:
        """Get visualization links from registry (≤10 lines)"""
        try:
            registry = get_registry()
            registry.set_output_dir(self.config.output_dir)
            visuals = registry.query(**filters)
            return registry.to_markdown_links(visuals)
        except Exception as e:
            print(f"[WARNING] Registry query failed: {e}")
            return []


class OverviewSection(BaseReportSection):
    """Overview and metadata section"""
    
    def get_filename(self) -> str:
        return "01_overview.md"
    
    def generate(self, data: Dict) -> str:
        stats = data.get('stats')
        content = []
        content.append(self._header())
        content.append(self._metadata())
        content.append(self._stats(stats))
        return "\n".join(content)
    
    def _header(self) -> str:
        title = f"Census ACS Analysis Report - {self.config.get_state_name()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.md.h1(title) + f"\n{self.md.italic(f'Generated: {timestamp}')}\n"
    
    def _metadata(self) -> str:
        lines = [self.md.h2("Dataset Information")]
        lines.append(self.md.bullet(f"State: {self.config.get_state_name()}"))
        lines.append(self.md.bullet(f"Survey Type: {self.config.survey_type}"))
        lines.append(self.md.bullet(f"Survey Scope: {self.config.survey_scope}"))
        return "\n".join(lines) + "\n"
    
    def _stats(self, stats: ProcessingStats) -> str:
        lines = [self.md.h2("Processing Statistics")]
        lines.append(self.md.bullet(f"Files Found: {stats.files_found}"))
        lines.append(self.md.bullet(f"Files Loaded: {stats.files_loaded}"))
        lines.append(self.md.bullet(f"Total Rows: {stats.total_rows:,}"))
        lines.append(self.md.bullet(f"Columns Found: {stats.columns_found}"))
        return "\n".join(lines) + "\n"


class TemporalSection(BaseReportSection):
    """Temporal analysis section"""
    
    def get_filename(self) -> str:
        return "02_temporal_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Temporal Analysis")]
        content.append(self._year_distribution(data))
        content.append(self._trends(data))
        content.append(self._growth_rates(data))
        content.append(self._visualizations())
        return "\n".join(content)
    
    def _year_distribution(self, data: Dict) -> str:
        dist = data.get('year_distribution', {})
        lines = [self.md.h2("Year Distribution")]
        if dist:
            for year, count in sorted(dist.items()):
                lines.append(self.md.bullet(f"{year}: {count:,} records"))
        else:
            lines.append("No year distribution data available.")
        return "\n".join(lines) + "\n"
    
    def _trends(self, data: Dict) -> str:
        trends = data.get('trends', {})
        lines = [self.md.h2("Temporal Trends")]
        if trends:
            for var, trend in list(trends.items()):
                lines.append(self.md.bullet(f"{var}: {trend}"))
        else:
            lines.append("No trend data available.")
        return "\n".join(lines) + "\n"
    
    def _growth_rates(self, data: Dict) -> str:
        growth = data.get('growth_rates', {})
        lines = [self.md.h2("Growth Rates")]
        if growth:
            for var, rate in list(growth.items()):
                lines.append(self.md.bullet(f"{var}: {rate:.2%}"))
        else:
            lines.append("No growth rate data available.")
        return "\n".join(lines) + "\n"
    
    def _visualizations(self) -> str:
        lines = [self.md.h2("Visualizations")]
        img_links = self._link_images("")
        temporal_imgs = [link for link in img_links if 'temporal' in link.lower() 
                        or 'year' in link.lower() or 'yoy' in link.lower()]
        if temporal_imgs:
            for link in temporal_imgs:
                lines.append(link)
        else:
            lines.append("No temporal visualizations available.")
        return "\n".join(lines) + "\n"


class EconomicSection(BaseReportSection):
    """Economic analysis section"""
    
    def get_filename(self) -> str:
        return "03_economic_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Economic Analysis")]
        if 'housing' in data:
            content.append(self._housing(data['housing']))
        if 'population' in data:
            content.append(self._population(data['population']))
        content.append(self._visualizations())
        return "\n".join(content)
    
    def _housing(self, housing: Dict) -> str:
        lines = [self.md.h2("Housing Economics")]
        has_data = False
        
        # Process all housing data sections
        for section_key, section_data in housing.items():
            if not section_data:
                continue
            # Convert key to readable title
            section_title = section_key.replace('_', ' ').title()
            lines.append(self.md.h3(section_title))
            
            if isinstance(section_data, dict):
                for k, v in section_data.items():
                    # Handle nested dicts (e.g., time series data)
                    if isinstance(v, dict):
                        if v:  # Only if dict has data
                            lines.append(self.md.bullet(f"{k}: {len(v)} data points"))
                            has_data = True
                    # Handle numeric values
                    elif isinstance(v, (int, float)) and v != 0:
                        lines.append(self.md.bullet(f"{k}: ${v:,.0f}"))
                        has_data = True
        
        if not has_data:
            lines.append("No housing economics data available.")
        return "\n".join(lines) + "\n"
    
    def _population(self, pop: Dict) -> str:
        lines = [self.md.h2("Population Economics")]
        has_data = False
        
        # Process all population data sections
        for section_key, section_data in pop.items():
            if not section_data:
                continue
            # Convert key to readable title
            section_title = section_key.replace('_', ' ').title()
            lines.append(self.md.h3(section_title))
            
            if isinstance(section_data, dict):
                for k, v in section_data.items():
                    # Handle nested dicts (e.g., time series data)
                    if isinstance(v, dict):
                        if v:  # Only if dict has data
                            lines.append(self.md.bullet(f"{k}: {len(v)} data points"))
                            has_data = True
                    # Handle numeric values
                    elif isinstance(v, (int, float)) and v != 0:
                        lines.append(self.md.bullet(f"{k}: ${v:,.0f}"))
                        has_data = True
        
        if not has_data:
            lines.append("No population economics data available.")
        return "\n".join(lines) + "\n"
    
    def _visualizations(self) -> str:
        lines = [self.md.h2("Visualizations")]
        img_links = self._link_images("")
        econ_imgs = [link for link in img_links if any(term in link.lower() 
                    for term in ['economic', 'income', 'property', 'rent', 'wage'])]
        if econ_imgs:
            for link in econ_imgs:
                lines.append(link)
        else:
            lines.append("No economic visualizations available.")
        return "\n".join(lines) + "\n"


class StatisticsSection(BaseReportSection):
    """Statistical analysis section"""
    
    def get_filename(self) -> str:
        return "04_statistical_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Statistical Analysis")]
        content.append(self._summary_stats(data))
        content.append(self._distributions(data))
        content.append(self._variance_analysis(data))
        content.append(self._visualizations())
        return "\n".join(content)
    
    def _summary_stats(self, data: Dict) -> str:
        summary = data.get('summary_statistics', {})
        lines = [self.md.h2("Summary Statistics")]
        if summary:
            for var, stats in list(summary.items()):
                lines.append(self.md.h3(var))
                if isinstance(stats, dict):
                    for key in ['mean', 'median', 'std', 'min', 'max']:
                        val = stats.get(key, 0)
                        if val != 0:
                            lines.append(self.md.bullet(f"{key.title()}: {val:,.2f}"))
        else:
            lines.append("No summary statistics available.")
        return "\n".join(lines) + "\n"
    
    def _distributions(self, data: Dict) -> str:
        dist = data.get('distribution_analysis', {})
        lines = [self.md.h2("Distribution Analysis")]
        skewed = dist.get('skewed_distributions', [])
        if skewed:
            for var in skewed:
                lines.append(self.md.bullet(f"{var}: Skewed distribution"))
        else:
            lines.append("No distribution analysis available.")
        return "\n".join(lines) + "\n"
    
    def _variance_analysis(self, data: Dict) -> str:
        variance = data.get('high_variance_vars', [])
        lines = [self.md.h2("High Variance Variables")]
        if variance:
            for var in variance:
                lines.append(self.md.bullet(var))
        else:
            lines.append("No variance analysis available.")
        return "\n".join(lines) + "\n"
    
    def _visualizations(self) -> str:
        lines = [self.md.h2("Visualizations")]
        img_links = self._link_images("")
        stat_imgs = [link for link in img_links if any(term in link.lower() 
                    for term in ['box', 'distribution', 'violin', 'statistical', 'histogram'])]
        if stat_imgs:
            for link in stat_imgs:
                lines.append(link)
        else:
            lines.append("No statistical visualizations available.")
        return "\n".join(lines) + "\n"


class CorrelationSection(BaseReportSection):
    """Correlation analysis section"""
    
    def get_filename(self) -> str:
        return "05_correlation_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Correlation Analysis")]
        content.append(self._strong_correlations(data))
        content.append(self._correlation_matrix(data))
        content.append(self._visualizations())
        return "\n".join(content)
    
    def _strong_correlations(self, data: Dict) -> str:
        strong = data.get('strong_correlations', [])
        lines = [self.md.h2("Strong Correlations")]
        if strong:
            for corr in strong:
                try:
                    var1, var2, val = corr[0], corr[1], corr[2]
                    lines.append(self.md.bullet(f"{var1} ↔ {var2}: {val:.3f}"))
                except (IndexError, TypeError):
                    continue
        else:
            lines.append("No strong correlations found.")
        return "\n".join(lines) + "\n"
    
    def _correlation_matrix(self, data: Dict) -> str:
        lines = [self.md.h2("Correlation Matrix")]
        lines.append("See correlation heatmap in figures directory.\n")
        return "\n".join(lines)
    
    def _visualizations(self) -> str:
        lines = [self.md.h2("Visualizations")]
        img_links = self._link_images("")
        corr_imgs = [link for link in img_links if any(term in link.lower() 
                    for term in ['correlation', 'heatmap', 'scatter'])]
        if corr_imgs:
            for link in corr_imgs:
                lines.append(link)
        else:
            lines.append("No correlation visualizations available.")
        return "\n".join(lines) + "\n"


class CrossVariableSection(BaseReportSection):
    """Cross-variable analysis section"""
    
    def get_filename(self) -> str:
        return "06_cross_variable_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Cross-Variable Analysis")]
        content.append(self._interactions(data))
        content.append(self._ratios(data))
        return "\n".join(content)
    
    def _interactions(self, data: Dict) -> str:
        interactions = data.get('interactions', {})
        lines = [self.md.h2("Variable Interactions")]
        for group, analysis in list(interactions.items()):
            lines.append(self.md.h3(group))
            lines.append(self.md.bullet(f"Correlation: {analysis.get('correlation', 0):.3f}"))
        return "\n".join(lines) + "\n"
    
    def _ratios(self, data: Dict) -> str:
        ratios = data.get('ratios', {})
        lines = [self.md.h2("Key Ratios")]
        for ratio_name, stats in list(ratios.items()):
            lines.append(self.md.bullet(f"{ratio_name}: {stats.get('mean', 0):.2f}"))
        return "\n".join(lines) + "\n"


class OutlierSection(BaseReportSection):
    """Outlier detection section"""
    
    def get_filename(self) -> str:
        return "07_outlier_detection.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Outlier Detection")]
        content.append(self._outlier_summary(data))
        content.append(self._high_outlier_vars(data))
        return "\n".join(content)
    
    def _outlier_summary(self, data: Dict) -> str:
        summary = data.get('outlier_summary', {})
        lines = [self.md.h2("Outlier Summary")]
        for var, info in list(summary.items()):
            count = info.get('count', 0)
            pct = info.get('percentage', 0)
            lines.append(self.md.bullet(f"{var}: {count} ({pct:.1f}%)"))
        return "\n".join(lines) + "\n"
    
    def _high_outlier_vars(self, data: Dict) -> str:
        high = data.get('high_outlier_vars', [])
        lines = [self.md.h2("Variables with High Outlier Rate")]
        for var in high:
            lines.append(self.md.bullet(var))
        return "\n".join(lines) + "\n"


class AnomalySection(BaseReportSection):
    """Anomaly detection section"""
    
    def get_filename(self) -> str:
        return "08_anomaly_detection.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Anomaly Detection")]
        content.append(self._temporal_anomalies(data))
        content.append(self._anomaly_stats(data))
        return "\n".join(content)
    
    def _temporal_anomalies(self, data: Dict) -> str:
        anomalies = data.get('anomaly_summary', {})
        lines = [self.md.h2("Temporal Anomalies")]
        for var, info in list(anomalies.items()):
            count = info.get('total_anomalies', 0)
            lines.append(self.md.bullet(f"{var}: {count} anomalies detected"))
        return "\n".join(lines) + "\n"
    
    def _anomaly_stats(self, data: Dict) -> str:
        total = data.get('total_anomalies', 0)
        lines = [self.md.h2("Overall Statistics")]
        lines.append(self.md.bullet(f"Total Anomalies: {total}"))
        return "\n".join(lines) + "\n"


class TrendSection(BaseReportSection):
    """Trend analysis section"""
    
    def get_filename(self) -> str:
        return "09_trend_analysis.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Trend Analysis")]
        content.append(self._trend_summary(data))
        content.append(self._strong_trends(data))
        content.append(self._trend_categories(data))
        return "\n".join(content)
    
    def _trend_summary(self, data: Dict) -> str:
        summary = data.get('trend_summary', {})
        lines = [self.md.h2("Trend Summary")]
        for var, info in list(summary.items()):
            slope = info.get('slope', 0)
            lines.append(self.md.bullet(f"{var}: slope={slope:.4f}"))
        return "\n".join(lines) + "\n"
    
    def _strong_trends(self, data: Dict) -> str:
        strong = data.get('strong_trends', [])
        lines = [self.md.h2("Strong Trends")]
        for var in strong:
            lines.append(self.md.bullet(var))
        return "\n".join(lines) + "\n"
    
    def _trend_categories(self, data: Dict) -> str:
        cats = data.get('trend_categories', {})
        lines = [self.md.h2("Trend Categories")]
        lines.append(self.md.bullet(f"Growing: {cats.get('growing', 0)}"))
        lines.append(self.md.bullet(f"Declining: {cats.get('declining', 0)}"))
        lines.append(self.md.bullet(f"Stable: {cats.get('stable', 0)}"))
        return "\n".join(lines) + "\n"


class FeatureEngineeringSection(BaseReportSection):
    """Feature engineering section"""
    
    def get_filename(self) -> str:
        return "10_feature_engineering.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Feature Engineering")]
        content.append(self._created_features(data))
        content.append(self._transformations(data))
        return "\n".join(content)
    
    def _created_features(self, data: Dict) -> str:
        features = data.get('features_created', [])
        lines = [self.md.h2("Created Features")]
        for feat in features:
            lines.append(self.md.bullet(feat))
        return "\n".join(lines) + "\n"
    
    def _transformations(self, data: Dict) -> str:
        transforms = data.get('transformations', [])
        lines = [self.md.h2("Applied Transformations")]
        for trans in transforms:
            lines.append(self.md.bullet(trans))
        return "\n".join(lines) + "\n"


class MLModelsSection(BaseReportSection):
    """Machine learning models section"""
    
    def get_filename(self) -> str:
        return "11_ml_models.md"
    
    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Machine Learning Models")]
        if 'regression' in data and data['regression']:
            content.append(self._regression(data['regression']))
        if 'clustering' in data and data['clustering']:
            content.append(self._clustering(data['clustering']))
        if 'timeseries' in data and data['timeseries']:
            content.append(self._timeseries(data['timeseries']))
        if 'time_series' in data and data['time_series']:
            content.append(self._timeseries(data['time_series']))
        content.append(self._model_comparison())
        if not any(k in data for k in ['regression', 'clustering', 'timeseries','time_series']):
            content.append("No ML models were trained for this dataset.")
        return "\n".join(content)
    
    def _regression(self, reg: Dict) -> str:
        """Generate regression section with registry-based linking (≤10 lines)"""
        lines = [self.md.h2("Regression Models")]
        lines.extend(self._regression_metrics(reg))
        lines.append("\n" + self.md.h3("Visualizations"))
        img_links = self._link_from_registry(visual_type='regression') or self._link_images("ml/regression")
        lines.extend(img_links if img_links else ["No regression visualizations available."])
        return "\n".join(lines) + "\n"

    def _regression_metrics(self, reg: Dict) -> List[str]:
        """Format regression metrics (≤10 lines)"""
        lines = [self.md.h3(f"Target Variable: {self.md.bold(reg.get('target', 'N/A'))}")]
        lines.append(self.md.bullet(f"Best Model: {reg.get('best_model', 'N/A')}"))
        lines.append(self.md.bullet(f"R² Score: {reg.get('test_score', 0):.4f}"))
        lines.append(self.md.bullet(f"RMSE: {reg.get('rmse', 0):.2f}"))
        lines.append(self.md.bullet(f"MAE: {reg.get('mae', 0):.2f}"))
        if 'feature_importance' in reg:
            lines.append(self.md.h3("Top Features"))
            lines.extend([self.md.bullet(f"{f}: {i:.4f}") for f, i in list(reg.get('feature_importance', {}).items())])
        return lines
    
    def _clustering(self, clust: Dict) -> str:
        """Generate clustering section with registry (≤10 lines)"""
        lines = [self.md.h2("Clustering Analysis")]
        lines.append(self.md.bullet(f"Method: {clust.get('method', 'N/A')}"))
        lines.append(self.md.bullet(f"Clusters: {clust.get('n_clusters', 0)}"))
        lines.append(self.md.bullet(f"Silhouette Score: {clust.get('silhouette', 0):.4f}"))
        if 'cluster_sizes' in clust:
            lines.append(self.md.h3("Cluster Sizes"))
            for i, size in enumerate(clust.get('cluster_sizes', [])):
                lines.append(self.md.bullet(f"Cluster {i}: {size} samples"))
        lines.append("\n" + self.md.h3("Visualizations"))
        img_links = self._link_from_registry(visual_type='clustering') or self._link_images("ml/clustering")
        lines.extend(img_links if img_links else ["No clustering visualizations available."])
        return "\n".join(lines) + "\n"
    
    def _timeseries(self, ts: Dict) -> str:
        """Generate time series section with registry (≤10 lines)"""
        lines = [self.md.h2("Time Series Forecasting")]
        lines.append(self.md.h3(f"Target Variable: {self.md.bold(ts.get('target', 'N/A'))}"))
        lines.append(self.md.bullet(f"Method: {ts.get('method', 'N/A')}"))
        lines.append(self.md.bullet(f"Periods Ahead: {ts.get('periods', 0)}"))
        forecast_vals = ts.get('forecast_values', [])
        if forecast_vals:
            lines.append(self.md.h3("Forecasted Values"))
            for i, val in enumerate(forecast_vals, 1):
                lines.append(self.md.bullet(f"Period {i}: {val:.2f}"))
        lines.append("\n" + self.md.h3("Visualizations"))
        img_links = self._link_from_registry(visual_type='time_series') or self._link_images("ml/time_series")
        lines.extend(img_links if img_links else ["No time series visualizations available."])
        return "\n".join(lines) + "\n"
    
    def _model_comparison(self) -> str:
        lines = [self.md.h2("Model Comparison")]
        img_links = self._link_images("ml/model_comparison")
        if img_links:
            for link in img_links:
                lines.append(link)
        else:
            lines.append("No model comparison visualizations available.")
        return "\n".join(lines) + "\n"


class LLMDataQualitySection(BaseReportSection):
    """LLM Data Quality Assessment section"""
    
    def get_filename(self) -> str:
        return "12_llm_data_quality.md"
    
    def generate(self, data: Dict) -> str:
        quality = data.get('data_quality', '')
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Data Quality")]
        if quality and quality != 'N/A':
      	    content.append(quality)
            #content.append(self.md.code_block(quality, "bash"))
        else:
            content.append("No assessment available.")
        return "\n".join(content) + "\n"


class LLMPolicyRecommendationsSection(BaseReportSection):
    """LLM Policy Recommendations section"""
    
    def get_filename(self) -> str:
        return "13_llm_policy_recommendations.md"
    
    def generate(self, data: Dict) -> str:
        recs = data.get('recommendations', '') or data.get('policy_recommendations', '')
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Policy Recommendations")]
        if recs and recs != 'N/A':
            content.append(recs)
        else:
            content.append("No recommendations available.")
        return "\n".join(content) + "\n"


class LLMTemporalInsightsSection(BaseReportSection):
    """LLM Temporal Analysis Insights section"""
    
    def get_filename(self) -> str:
        return "14_llm_temporal_insights.md"
    
    def generate(self, data: Dict) -> str:
        insights = data.get('temporal_insights', '')
        if not insights or insights == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Temporal Analysis")]
        content.append(insights)
      #content.append(self.md.code_block(insights, "bash"))
        return "\n".join(content) + "\n"


class LLMEconomicInsightsSection(BaseReportSection):
    """LLM Economic Analysis Insights section"""
    
    def get_filename(self) -> str:
        return "15_llm_economic_insights.md"
    
    def generate(self, data: Dict) -> str:
        analysis = data.get('economic_analysis', '')
        if not analysis or analysis == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Economic Analysis")]
        content.append(analysis)
#content.append(self.md.code_block(analysis, "bash"))
        return "\n".join(content) + "\n"


class LLMCorrelationInsightsSection(BaseReportSection):
    """LLM Correlation Insights section"""
    
    def get_filename(self) -> str:
        return "16_llm_correlation_insights.md"
    
    def generate(self, data: Dict) -> str:
        insights = data.get('correlation_insights', '')
        if not insights or insights == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Correlation Analysis")]
        content.append(insights)
      #content.append(self.md.code_block(insights, "bash"))
        return "\n".join(content) + "\n"


class LLMStatisticalInsightsSection(BaseReportSection):
    """LLM Statistical Analysis Insights section"""
    
    def get_filename(self) -> str:
        return "17_llm_statistical_insights.md"
    
    def generate(self, data: Dict) -> str:
        analysis = data.get('statistical_analysis', '')
        if not analysis or analysis == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Statistical Analysis")]
        content.append(analysis)
#content.append(self.md.code_block(analysis, "bash"))
        return "\n".join(content) + "\n"


class LLMOutlierInsightsSection(BaseReportSection):
    """LLM Outlier Analysis Insights section"""
    
    def get_filename(self) -> str:
        return "18_llm_outlier_insights.md"
    
    def generate(self, data: Dict) -> str:
        analysis = data.get('outlier_analysis', '')
        if not analysis or analysis == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Outlier Analysis")]
        content.append(analysis)
#content.append(self.md.code_block(analysis, "bash"))
        return "\n".join(content) + "\n"


class LLMAnomalyInsightsSection(BaseReportSection):
    """LLM Anomaly Detection Insights section"""
    
    def get_filename(self) -> str:
        return "19_llm_anomaly_insights.md"
    
    def generate(self, data: Dict) -> str:
        detection = data.get('anomaly_detection', '')
        if not detection or detection == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Anomaly Detection")]
        content.append(detection)
        return "\n".join(content) + "\n"


class LLMTrendInsightsSection(BaseReportSection):
    """LLM Trend Analysis Insights section"""
    
    def get_filename(self) -> str:
        return "20_llm_trend_insights.md"
    
    def generate(self, data: Dict) -> str:
        analysis = data.get('trend_analysis', '')
        if not analysis or analysis == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Trend Analysis")]
        content.append(analysis)
#content.append(self.md.code_block(analysis, "bash"))
        return "\n".join(content) + "\n"


class LLMDeepLearningInsightsSection(BaseReportSection):
    """LLM Deep Learning Analysis Insights section"""

    def get_filename(self) -> str:
        return "21_llm_deep_learning_insights.md"

    def generate(self, data: Dict) -> str:
        insights = data.get('deep_learning_insights', '')
        if not insights or insights == 'N/A':
            return None
        content = [self.md.h1("model: microsoft/phi-4-mini-reasoning Q8_0,Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Deep Learning Analysis")]
        content.append(insights)
        return "\n".join(content) + "\n"


class DeepLearningSection(BaseReportSection):
    """Deep learning models section"""

    def get_filename(self) -> str:
        return "11b_deep_learning_models.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Deep Learning Models (TensorFlow CPU)")]
        if not data or not isinstance(data, dict) or len(data) == 0:
            content.append("No deep learning models were trained for this dataset.")
            return "\n".join(content)
        content.append(self._dl_summary(data))
        content.append(self._dl_tasks(data))
        content.append(self._visualizations())
        return "\n".join(content)

    def _dl_summary(self, data: Dict) -> str:
        lines = [self.md.h2("Deep Learning Summary")]
        lines.append(self.md.bullet(f"Total Tasks: {len(data)}"))
        lines.append(self.md.bullet(f"Tasks: {', '.join(data.keys())}"))
        return "\n".join(lines) + "\n"

    def _dl_tasks(self, data: Dict) -> str:
        lines = []
        for task_name, dl_result in data.items():
            lines.append(self._format_task(task_name, dl_result))
        return "\n".join(lines)

    def _format_task(self, task_name: str, dl_result) -> str:
        lines = [self.md.h2(f"Task: {task_name.replace('_', ' ').title()}")]
        lines.append(self._task_details(dl_result))
        lines.append(self._task_metrics(dl_result))
        return "\n".join(lines) + "\n"

    def _task_details(self, dl_result) -> str:
        lines = [self.md.h3("Model Details")]
        lines.append(self.md.bullet(f"Model Type: {dl_result.model_type}"))
        lines.append(self.md.bullet(f"Task Type: {dl_result.task_type}"))
        targets = ', '.join(dl_result.targets)
        lines.append(self.md.bullet(f"Target Variables: {targets}"))
        layers = dl_result.architecture.get('layers', 'N/A')
        params = dl_result.architecture.get('params', 'N/A')
        lines.append(self.md.bullet(f"Architecture: {layers} layers, {params:,} parameters"))
        features = dl_result.metadata.get('features', [])
        lines.append(self.md.bullet(f"Input Features: {len(features)} features"))
        epochs_trained = len(dl_result.history.get('loss', []))
        lines.append(self.md.bullet(f"Training Epochs: {epochs_trained}"))
        return "\n".join(lines) + "\n"

    def _task_metrics(self, dl_result) -> str:
        lines = [self.md.h3("Performance Metrics")]
        lines.append(self.md.bullet(f"Training Loss: {dl_result.train_loss:.4f}"))
        lines.append(self.md.bullet(f"Validation Loss: {dl_result.val_loss:.4f}"))
        overfitting_gap = dl_result.val_loss - dl_result.train_loss
        risk_level = 'HIGH RISK' if overfitting_gap > 0.5 else 'MODERATE' if overfitting_gap > 0.2 else 'LOW'
        lines.append(self.md.bullet(f"Overfitting Risk: {risk_level} (gap: {overfitting_gap:.4f})"))
        for metric_name, metric_val in dl_result.test_metrics.items():
            lines.append(self.md.bullet(f"{metric_name.upper()}: {metric_val:.4f}"))
        return "\n".join(lines) + "\n"

    def _visualizations(self) -> str:
        """Generate DL visualizations section with registry (≤10 lines)"""
        lines = [self.md.h2("Visualizations")]
        img_links = self._link_from_registry(visual_type='deep_learning') or self._link_images("ml/deep_learning")
        lines.extend(img_links if img_links else ["No deep learning visualizations available."])
        return "\n".join(lines) + "\n"


class TableOfContentsSection(BaseReportSection):
    """Table of contents for all reports"""
    
    def get_filename(self) -> str:
        return "00_table_of_contents.md"
    
    def generate(self, data: Dict) -> str:
        sections = data.get('sections', [])
        content = [self.md.h1("Table of Contents")]
        content.append(self._toc_list(sections))
        content.append(self._figures_link())
        return "\n".join(content)
    
    def _toc_list(self, sections: List[Tuple[str, str]]) -> str:
        """Generate TOC list from section metadata tuples (display_name, filename)"""
        lines = [self.md.h2("Report Sections")]
        for i, (display_name, filename) in enumerate(sections, 1):
            lines.append(f"{i}. {self.md.link(display_name, filename)}")
        return "\n".join(lines) + "\n"
    
    def _figures_link(self) -> str:
        lines = [self.md.h2("Visualizations")]
        lines.append(self.md.bullet("See the `figures/` directory for all charts and plots"))
        return "\n".join(lines) + "\n"


class ReportGenerator:
    """Main report generator coordinating all sections"""
    
    def __init__(self, config: Config):
        self.config = config
        self._init_sections()
    
    def _init_sections(self):
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
            'llm_data_quality': LLMDataQualitySection(self.config),
            'llm_policy': LLMPolicyRecommendationsSection(self.config),
            'llm_temporal': LLMTemporalInsightsSection(self.config),
            'llm_economic': LLMEconomicInsightsSection(self.config),
            'llm_correlation': LLMCorrelationInsightsSection(self.config),
            'llm_statistical': LLMStatisticalInsightsSection(self.config),
            'llm_outlier': LLMOutlierInsightsSection(self.config),
            'llm_anomaly': LLMAnomalyInsightsSection(self.config),
            'llm_trend': LLMTrendInsightsSection(self.config),
            'llm_deep_learning': LLMDeepLearningInsightsSection(self.config)
        }
    
    def generate(self, stats: ProcessingStats, temporal: Dict,
                llm_results: Dict, economic: Dict = None,
                correlations: Dict = None, statistics: Dict = None,
                outliers: Dict = None, anomalies: Dict = None,
                trends: Dict = None, feature_eng: Dict = None,
                ml_results: Dict = None, cross_var: Dict = None,
                dl_results: Dict = None) -> str:
        
        results = []
        section_metadata = []  # List of tuples: (display_name, filename)
        
        # Generate TOC last but save first
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

        # Generate individual LLM subsections
        llm_sections = self._gen_llm_sections(llm_results, section_metadata)
        results.extend(llm_sections)
        
        # Generate and save TOC
        results.extend(self._gen_toc(section_metadata))
        
        return f"Generated {len(results)} report sections"
    
    def _gen_overview(self, stats: ProcessingStats) -> List[str]:
        try:
            data = {'stats': stats}
            content = self.sections['overview'].generate(data)
            path = self.sections['overview'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Overview section failed: {e}")
            return []
    
    def _gen_temporal(self, temporal: Dict) -> List[str]:
        try:
            content = self.sections['temporal'].generate(temporal)
            path = self.sections['temporal'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Temporal section failed: {e}")
            return []
    
    def _gen_economic(self, economic: Dict) -> List[str]:
        try:
            content = self.sections['economic'].generate(economic)
            path = self.sections['economic'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Economic section failed: {e}")
            return []
    
    def _gen_statistics(self, statistics: Dict) -> List[str]:
        try:
            content = self.sections['statistics'].generate(statistics)
            path = self.sections['statistics'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Statistics section failed: {e}")
            return []
    
    def _gen_correlation(self, correlations: Dict) -> List[str]:
        try:
            content = self.sections['correlation'].generate(correlations)
            path = self.sections['correlation'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Correlation section failed: {e}")
            return []
    
    def _gen_cross_var(self, cross_var: Dict) -> List[str]:
        try:
            content = self.sections['cross_var'].generate(cross_var)
            path = self.sections['cross_var'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Cross-variable section failed: {e}")
            return []
    
    def _gen_outlier(self, outliers: Dict) -> List[str]:
        try:
            content = self.sections['outlier'].generate(outliers)
            path = self.sections['outlier'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Outlier section failed: {e}")
            return []
    
    def _gen_anomaly(self, anomalies: Dict) -> List[str]:
        try:
            content = self.sections['anomaly'].generate(anomalies)
            path = self.sections['anomaly'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Anomaly section failed: {e}")
            return []
    
    def _gen_trend(self, trends: Dict) -> List[str]:
        try:
            content = self.sections['trend'].generate(trends)
            path = self.sections['trend'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Trend section failed: {e}")
            return []
    
    def _gen_feature_eng(self, feature_eng: Dict) -> List[str]:
        try:
            content = self.sections['feature_eng'].generate(feature_eng)
            path = self.sections['feature_eng'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Feature engineering section failed: {e}")
            return []
    
    def _gen_ml(self, ml_results: Dict) -> List[str]:
        try:
            content = self.sections['ml'].generate(ml_results)
            path = self.sections['ml'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] ML section failed: {e}")
            return []

    def _gen_dl(self, dl_results: Dict) -> List[str]:
        try:
            content = self.sections['dl'].generate(dl_results)
            path = self.sections['dl'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] Deep Learning section failed: {e}")
            return []

    def _gen_llm_sections(self, llm_results: Dict, section_metadata: List[Tuple[str, str]]) -> List[str]:
        """Generate all LLM subsections as separate files"""
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
            ('llm_deep_learning', 'LLM: Deep Learning Insights')
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
        try:
            data = {'sections': section_metadata}
            content = self.sections['toc'].generate(data)
            path = self.sections['toc'].save(content)
            return [path]
        except Exception as e:
            print(f"[WARNING] TOC generation failed: {e}")
            return []

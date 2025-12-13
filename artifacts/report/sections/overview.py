"""
Overview Section - Enhanced dataset overview and metadata reporting.
"""

from typing import Dict, Any
from datetime import datetime

from report.base import BaseReportSection, MarkdownFormatter
from config import Config, ProcessingStats


class OverviewSection(BaseReportSection):
    """Overview and metadata section with enhanced verbosity."""

    def get_filename(self) -> str:
        return "01_overview.md"

    def generate(self, data: Dict) -> str:
        stats = data.get('stats')
        content = []
        content.append(self._header())
        content.append(self._metadata())
        content.append(self._processing_stats(stats))
        content.append(self._data_quality_summary(data))
        content.append(self._column_breakdown(data))
        content.append(self._year_range(data))
        content.append(self._key_highlights(data))
        return "\n".join(filter(None, content))

    def _header(self) -> str:
        """Generate report header with title and timestamp."""
        title = f"Census ACS Analysis Report - {self.config.get_state_name()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            self.md.h1(title),
            f"{self.md.italic(f'Generated: {timestamp}')}",
            "",
            self.md.blockquote(
                f"Comprehensive analysis of American Community Survey (ACS) data "
                f"for {self.config.get_state_name()} - {self.config.survey_type} survey, "
                f"{self.config.survey_scope} estimates."
            ),
            ""
        ]
        return "\n".join(lines)

    def _metadata(self) -> str:
        """Generate dataset metadata section."""
        lines = [self.md.h2("Dataset Information")]

        # Create metadata table
        headers = ["Property", "Value"]
        rows = [
            ["State", self.config.get_state_name()],
            ["Survey Type", self.config.survey_type.title()],
            ["Survey Scope", self.config.survey_scope],
            ["Output Directory", f"`{self.config.output_dir}`"],
        ]
        lines.append(self.md.table(headers, rows))
        return "\n".join(lines)

    def _processing_stats(self, stats: ProcessingStats) -> str:
        """Generate processing statistics with enhanced detail."""
        lines = [self.md.h2("Processing Statistics")]

        if not stats:
            lines.append("_No processing statistics available._")
            return "\n".join(lines)

        # Create stats table
        headers = ["Metric", "Value", "Description"]
        rows = [
            ["Files Found", f"{stats.files_found:,}", "Total ACS data files discovered"],
            ["Files Loaded", f"{stats.files_loaded:,}", "Files successfully loaded into memory"],
            ["Total Records", f"{stats.total_rows:,}", "Total observations in dataset"],
            ["Total Columns", f"{stats.columns_found:,}", "Number of variables/features"],
        ]
        lines.append(self.md.table(headers, rows))

        # Add load success rate
        if stats.files_found > 0:
            success_rate = (stats.files_loaded / stats.files_found) * 100
            lines.append("")
            lines.append(self.md.metric("Load Success Rate", success_rate, "%", 1))

        # Estimate memory usage (rough estimate: ~8 bytes per cell for numeric data)
        estimated_memory_mb = (stats.total_rows * stats.columns_found * 8) / (1024 * 1024)
        lines.append(self.md.metric("Estimated Memory", estimated_memory_mb, "MB", 1))

        return "\n".join(lines)

    def _data_quality_summary(self, data: Dict) -> str:
        """Generate data quality summary section."""
        lines = [self.md.h2("Data Quality Summary")]

        quality = data.get('data_quality', {})
        if not quality:
            # Generate basic quality metrics from stats
            stats = data.get('stats')
            if stats:
                lines.append(self.md.bullet(f"Total Records: {stats.total_rows:,}"))
                lines.append(self.md.bullet(f"Total Variables: {stats.columns_found}"))
                lines.append("")
                lines.append(self.md.interpretation(
                    "Detailed data quality metrics will be available in the Statistical Analysis section."
                ))
            else:
                lines.append("_Data quality metrics not available._")
            return "\n".join(lines)

        # If quality data is available, show detailed metrics
        complete_records = quality.get('complete_records', 0)
        total_records = quality.get('total_records', 1)
        missing_pct = quality.get('missing_percentage', 0)

        headers = ["Quality Metric", "Value", "Percentage"]
        rows = [
            ["Complete Records", f"{complete_records:,}", f"{(complete_records/total_records)*100:.1f}%"],
            ["Records with Missing Data", f"{total_records - complete_records:,}",
             f"{((total_records - complete_records)/total_records)*100:.1f}%"],
            ["Total Missing Values", f"{quality.get('total_missing', 0):,}", f"{missing_pct:.1f}%"],
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _column_breakdown(self, data: Dict) -> str:
        """Generate column type breakdown."""
        lines = [self.md.h2("Variable Types")]

        column_info = data.get('column_info', {})
        if not column_info:
            stats = data.get('stats')
            if stats:
                lines.append(self.md.bullet(f"Total Variables: {stats.columns_found}"))
                lines.append("")
                lines.append(self.md.interpretation(
                    "Variable type breakdown available in schema documentation."
                ))
            return "\n".join(lines)

        headers = ["Variable Type", "Count", "Percentage"]
        total = sum(column_info.values()) or 1
        rows = [
            [vtype, f"{count:,}", f"{(count/total)*100:.1f}%"]
            for vtype, count in column_info.items()
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _year_range(self, data: Dict) -> str:
        """Generate year range information."""
        lines = [self.md.h2("Temporal Coverage")]

        year_info = data.get('year_info', {})
        year_dist = data.get('year_distribution', {})

        if year_dist:
            years = sorted(year_dist.keys())
            if years:
                min_year = min(years)
                max_year = max(years)
                total_years = len(years)

                lines.append(self.md.metric("Year Range", f"{min_year} - {max_year}"))
                lines.append(self.md.metric("Total Years", total_years))
                lines.append(self.md.metric("Records per Year (avg)",
                                           sum(year_dist.values()) / len(year_dist)))
                lines.append("")

                # Show year distribution summary
                if len(years) <= 10:
                    lines.append(self.md.h3("Records by Year"))
                    headers = ["Year", "Records", "% of Total"]
                    total_records = sum(year_dist.values())
                    rows = [
                        [str(year), f"{count:,}", f"{(count/total_records)*100:.1f}%"]
                        for year, count in sorted(year_dist.items())
                    ]
                    lines.append(self.md.table(headers, rows))
        elif year_info:
            lines.append(self.md.metric("Year Range",
                                       f"{year_info.get('min', 'N/A')} - {year_info.get('max', 'N/A')}"))
        else:
            lines.append("_Temporal coverage information not available._")

        return "\n".join(lines)

    def _key_highlights(self, data: Dict) -> str:
        """Generate key highlights/executive summary."""
        lines = [self.md.h2("Key Highlights")]

        highlights = data.get('highlights', [])
        stats = data.get('stats')

        if highlights:
            for highlight in highlights:
                lines.append(self.md.bullet(highlight))
        elif stats:
            # Generate automatic highlights
            lines.append(self.md.bullet(
                f"Dataset contains {stats.total_rows:,} records across {stats.columns_found} variables"
            ))
            if stats.files_loaded > 1:
                lines.append(self.md.bullet(
                    f"Data consolidated from {stats.files_loaded} source files"
                ))
            lines.append(self.md.bullet(
                f"Survey type: {self.config.survey_type.title()} ({self.config.survey_scope} estimates)"
            ))
            lines.append("")
            lines.append(self.md.interpretation(
                "For detailed analysis, see the Statistical Analysis and Economic Analysis sections."
            ))
        else:
            lines.append("_Key highlights will be generated after full analysis._")

        return "\n".join(lines)

"""
Table of Contents Section - Master index for all report sections.
"""

from typing import Dict, List, Tuple, Any

from report.base import BaseReportSection


class TableOfContentsSection(BaseReportSection):
    """Table of contents section with navigation links."""

    def get_filename(self) -> str:
        return "00_table_of_contents.md"

    def generate(self, data: Dict) -> str:
        sections = data.get('sections', [])
        content = [self.md.h1("Table of Contents")]

        content.append(self.md.blockquote(
            "Master index for the Census ACS Analysis Report. "
            "Click on any section to navigate directly to that analysis."
        ))
        content.append("")

        content.append(self._toc_list(sections))
        content.append(self._figures_link())
        content.append(self._report_metadata())

        return "\n".join(filter(None, content))

    def _toc_list(self, sections: List[Tuple[str, str]]) -> str:
        """Generate TOC list from section metadata tuples (display_name, filename)."""
        lines = [self.md.h2("Report Sections")]

        if not sections:
            lines.append("_No sections available._")
            return "\n".join(lines)

        # Group sections by category
        analysis_sections = []
        llm_sections = []

        for display_name, filename in sections:
            if 'LLM' in display_name or 'llm' in filename:
                llm_sections.append((display_name, filename))
            else:
                analysis_sections.append((display_name, filename))

        # Core analysis sections
        if analysis_sections:
            lines.append(self.md.h3("Core Analysis"))
            for i, (display_name, filename) in enumerate(analysis_sections, 1):
                lines.append(f"{i}. {self.md.link(display_name, filename)}")
            lines.append("")

        # LLM insight sections
        if llm_sections:
            lines.append(self.md.h3("AI-Generated Insights"))
            for i, (display_name, filename) in enumerate(llm_sections, len(analysis_sections) + 1):
                # Clean up display name
                clean_name = display_name.replace('LLM: ', '')
                lines.append(f"{i}. {self.md.link(clean_name, filename)}")
            lines.append("")

        return "\n".join(lines)

    def _figures_link(self) -> str:
        """Generate figures directory link."""
        lines = [self.md.h2("Visualizations")]
        lines.append(self.md.bullet(
            f"All charts and plots are available in the {self.md.link('figures/', 'figures/')} directory"
        ))
        lines.append("")

        # Subdirectories
        lines.append(self.md.h3("Figure Subdirectories"))
        subdirs = [
            ("Statistical Analysis", "figures/"),
            ("ML: Clustering", "figures/ml/clustering/"),
            ("ML: Regression", "figures/ml/regression/"),
            ("ML: Time Series", "figures/ml/time_series/"),
            ("Deep Learning", "figures/ml/deep_learning/"),
        ]
        for name, path in subdirs:
            lines.append(self.md.bullet(f"{self.md.link(name, path)}"))

        return "\n".join(lines) + "\n"

    def _report_metadata(self) -> str:
        """Generate report metadata section."""
        lines = [self.md.h2("Report Information")]

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        headers = ["Property", "Value"]
        rows = [
            ["State", self.config.get_state_name()],
            ["Survey Type", self.config.survey_type],
            ["Survey Scope", self.config.survey_scope],
            ["Generated", timestamp],
            ["Output Directory", f"`{self.config.output_dir}`"],
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines) + "\n"

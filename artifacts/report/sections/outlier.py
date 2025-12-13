"""
Outlier Detection Section - Statistical outlier analysis and reporting.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class OutlierSection(BaseReportSection):
    """Outlier detection section with comprehensive outlier analysis."""

    def get_filename(self) -> str:
        return "07_outlier_detection.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Outlier Detection")]

        # Add section description
        content.append(self.md.blockquote(
            "Statistical outlier detection using IQR (Interquartile Range) method. "
            "Outliers are values falling outside Q1 - 1.5×IQR or Q3 + 1.5×IQR bounds."
        ))
        content.append("")

        content.append(self._detection_method(data))
        content.append(self._outlier_summary(data))
        content.append(self._high_outlier_vars(data))
        content.append(self._outlier_details(data))
        content.append(self._impact_assessment(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _detection_method(self, data: Dict) -> str:
        """Document the outlier detection methodology."""
        lines = [self.md.h2("Detection Methodology")]

        method = data.get('method', 'IQR')

        headers = ["Parameter", "Value", "Description"]
        rows = [
            ["Method", method, "Outlier detection algorithm"],
            ["Lower Bound", "Q1 - 1.5 × IQR", "Values below are outliers"],
            ["Upper Bound", "Q3 + 1.5 × IQR", "Values above are outliers"],
            ["IQR Definition", "Q3 - Q1", "Interquartile Range"],
        ]
        lines.append(self.md.table(headers, rows))

        lines.append("")
        lines.append(self.md.note(
            "The IQR method is robust to extreme values and works well for "
            "approximately symmetric distributions."
        ))

        return "\n".join(lines)

    def _outlier_summary(self, data: Dict) -> str:
        """Generate outlier summary section."""
        summary = data.get('outlier_summary', {})
        lines = [self.md.h2("Outlier Summary")]

        if not summary:
            lines.append("_No outlier summary available._")
            return "\n".join(lines)

        # Calculate totals
        total_outliers = sum(info.get('count', 0) for info in summary.values() if isinstance(info, dict))
        vars_with_outliers = len([v for v, info in summary.items()
                                  if isinstance(info, dict) and info.get('count', 0) > 0])

        lines.append(self.md.h3("Overview"))
        lines.append(self.md.metric("Variables Analyzed", len(summary)))
        lines.append(self.md.metric("Variables with Outliers", vars_with_outliers))
        lines.append(self.md.metric("Total Outliers Detected", total_outliers))
        lines.append("")

        # Detailed table
        lines.append(self.md.h3("Outliers by Variable"))

        headers = ["Variable", "Count", "Percentage", "Severity"]
        rows = []

        # Sort by count descending
        sorted_vars = sorted(
            [(var, info) for var, info in summary.items() if isinstance(info, dict)],
            key=lambda x: x[1].get('count', 0),
            reverse=True
        )

        for var, info in sorted_vars[:20]:  # Top 20
            count = info.get('count', 0)
            pct = info.get('percentage', 0)

            # Determine severity
            if pct > 10:
                severity = "High"
            elif pct > 5:
                severity = "Moderate"
            elif pct > 1:
                severity = "Low"
            else:
                severity = "Minimal"

            if count > 0:
                rows.append([var, f"{count:,}", f"{pct:.2f}%", severity])

        if rows:
            lines.append(self.md.table(headers, rows))
        else:
            lines.append("_No outliers detected in the dataset._")

        return "\n".join(lines)

    def _high_outlier_vars(self, data: Dict) -> str:
        """Generate high outlier rate variables section."""
        high = data.get('high_outlier_vars', [])
        summary = data.get('outlier_summary', {})

        if not high and not summary:
            return ""

        lines = [self.md.h2("High Outlier Rate Variables")]

        # Identify high outlier rate variables from summary if not provided
        if not high and summary:
            high = [var for var, info in summary.items()
                    if isinstance(info, dict) and info.get('percentage', 0) > 5]

        if high:
            lines.append(self.md.blockquote(
                "Variables with outlier rate > 5% may indicate data quality issues, "
                "non-normal distributions, or genuinely extreme values."
            ))
            lines.append("")

            for var in high[:15]:
                info = summary.get(var, {})
                if isinstance(info, dict):
                    pct = info.get('percentage', 0)
                    count = info.get('count', 0)
                    lines.append(self.md.bullet(f"**{var}**: {count:,} outliers ({pct:.2f}%)"))
                else:
                    lines.append(self.md.bullet(f"**{var}**"))

            lines.append("")
            lines.append(self.md.interpretation(
                "Consider investigating these variables for data entry errors, "
                "applying transformations, or using robust statistical methods."
            ))
        else:
            lines.append("_No variables with high outlier rates (> 5%) detected._")

        return "\n".join(lines)

    def _outlier_details(self, data: Dict) -> str:
        """Generate detailed outlier information with bounds."""
        details = data.get('outlier_details', data.get('outlier_bounds', {}))
        summary = data.get('outlier_summary', {})

        if not details:
            return ""

        lines = [self.md.h2("Outlier Bounds")]

        headers = ["Variable", "Lower Bound", "Upper Bound", "Min Outlier", "Max Outlier"]
        rows = []

        for var, bounds in list(details.items())[:15]:
            if isinstance(bounds, dict):
                lower = bounds.get('lower_bound', bounds.get('lower', None))
                upper = bounds.get('upper_bound', bounds.get('upper', None))
                min_out = bounds.get('min_outlier', None)
                max_out = bounds.get('max_outlier', None)

                lower_str = f"{lower:,.2f}" if lower is not None else "—"
                upper_str = f"{upper:,.2f}" if upper is not None else "—"
                min_str = f"{min_out:,.2f}" if min_out is not None else "—"
                max_str = f"{max_out:,.2f}" if max_out is not None else "—"

                rows.append([var, lower_str, upper_str, min_str, max_str])

        if rows:
            lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _impact_assessment(self, data: Dict) -> str:
        """Generate outlier impact assessment."""
        summary = data.get('outlier_summary', {})

        if not summary:
            return ""

        lines = [self.md.h2("Impact Assessment")]

        # Calculate impact metrics
        total_vars = len(summary)
        vars_with_outliers = sum(1 for info in summary.values()
                                 if isinstance(info, dict) and info.get('count', 0) > 0)
        high_rate_vars = sum(1 for info in summary.values()
                             if isinstance(info, dict) and info.get('percentage', 0) > 5)

        affected_pct = (vars_with_outliers / total_vars) * 100 if total_vars > 0 else 0

        lines.append(self.md.h3("Data Quality Impact"))

        headers = ["Impact Metric", "Value", "Assessment"]
        rows = [
            ["Variables Affected", f"{vars_with_outliers}/{total_vars}", f"{affected_pct:.1f}%"],
            ["High Risk Variables", str(high_rate_vars), "Outlier rate > 5%"],
        ]
        lines.append(self.md.table(headers, rows))

        lines.append("")

        # Recommendations
        lines.append(self.md.h3("Recommendations"))

        if high_rate_vars > 0:
            lines.append(self.md.bullet(
                "Investigate high outlier rate variables for data quality issues"
            ))
            lines.append(self.md.bullet(
                "Consider log transformation for highly skewed variables"
            ))
            lines.append(self.md.bullet(
                "Use robust statistics (median, IQR) instead of mean/std for affected variables"
            ))
        else:
            lines.append(self.md.bullet(
                "Outlier rates are within acceptable ranges"
            ))
            lines.append(self.md.bullet(
                "Standard statistical methods should perform well"
            ))

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        outlier_imgs = [link for link in img_links if any(term in link.lower()
                       for term in ['outlier', 'box'])]

        if outlier_imgs:
            for link in outlier_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No outlier visualizations available._")

        return "\n".join(lines)

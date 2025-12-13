"""
Anomaly Detection Section - Temporal anomaly analysis and reporting.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class AnomalySection(BaseReportSection):
    """Anomaly detection section with temporal anomaly analysis."""

    def get_filename(self) -> str:
        return "08_anomaly_detection.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Anomaly Detection")]

        # Add section description
        content.append(self.md.blockquote(
            "Detection of unusual patterns and anomalies in temporal data, "
            "identifying values that deviate significantly from expected trends."
        ))
        content.append("")

        content.append(self._detection_method(data))
        content.append(self._temporal_anomalies(data))
        content.append(self._anomaly_stats(data))
        content.append(self._anomaly_severity(data))
        content.append(self._temporal_patterns(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _detection_method(self, data: Dict) -> str:
        """Document the anomaly detection methodology."""
        lines = [self.md.h2("Detection Methodology")]

        method = data.get('method', 'Z-Score / Moving Average Deviation')

        headers = ["Parameter", "Description"]
        rows = [
            ["Method", method],
            ["Baseline", "Moving average or trend line"],
            ["Threshold", "Values exceeding 2-3 standard deviations"],
            ["Scope", "Year-over-year and within-year patterns"],
        ]
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _temporal_anomalies(self, data: Dict) -> str:
        """Generate temporal anomalies section."""
        anomalies = data.get('anomaly_summary', {})
        lines = [self.md.h2("Temporal Anomalies by Variable")]

        if not anomalies:
            lines.append("_No temporal anomalies detected._")
            return "\n".join(lines)

        headers = ["Variable", "Total Anomalies", "Anomaly Rate", "Severity"]
        rows = []

        # Sort by anomaly count
        sorted_anomalies = sorted(
            [(var, info) for var, info in anomalies.items() if isinstance(info, dict)],
            key=lambda x: x[1].get('total_anomalies', 0),
            reverse=True
        )

        for var, info in sorted_anomalies[:20]:
            count = info.get('total_anomalies', info.get('count', 0))
            rate = info.get('anomaly_rate', info.get('percentage', 0))

            # Determine severity
            if rate > 10:
                severity = "Critical"
            elif rate > 5:
                severity = "High"
            elif rate > 2:
                severity = "Moderate"
            else:
                severity = "Low"

            if count > 0:
                rows.append([var, f"{count:,}", f"{rate:.2f}%", severity])

        if rows:
            lines.append(self.md.table(headers, rows))
        else:
            lines.append("_No anomalies detected in the dataset._")

        return "\n".join(lines)

    def _anomaly_stats(self, data: Dict) -> str:
        """Generate overall anomaly statistics."""
        total = data.get('total_anomalies', 0)
        anomalies = data.get('anomaly_summary', {})

        lines = [self.md.h2("Overall Statistics")]

        # Calculate additional metrics
        vars_with_anomalies = sum(1 for info in anomalies.values()
                                  if isinstance(info, dict) and info.get('total_anomalies', 0) > 0)

        headers = ["Statistic", "Value"]
        rows = [
            ["Total Anomalies Detected", f"{total:,}"],
            ["Variables with Anomalies", str(vars_with_anomalies)],
            ["Variables Analyzed", str(len(anomalies))],
        ]

        if len(anomalies) > 0:
            avg_anomalies = total / len(anomalies)
            rows.append(["Average Anomalies per Variable", f"{avg_anomalies:.2f}"])

        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _anomaly_severity(self, data: Dict) -> str:
        """Generate anomaly severity breakdown."""
        anomalies = data.get('anomaly_summary', {})
        severity_data = data.get('severity_breakdown', {})

        if not anomalies and not severity_data:
            return ""

        lines = [self.md.h2("Anomaly Severity Analysis")]

        if severity_data:
            headers = ["Severity Level", "Count", "Description"]
            rows = []
            for level, count in severity_data.items():
                desc = {
                    'critical': 'Requires immediate investigation',
                    'high': 'Significant deviation from expected',
                    'moderate': 'Notable but not critical',
                    'low': 'Minor deviation'
                }.get(level.lower(), '—')
                rows.append([level.title(), f"{count:,}", desc])
            lines.append(self.md.table(headers, rows))
        else:
            # Calculate from anomaly summary
            critical = sum(1 for info in anomalies.values()
                          if isinstance(info, dict) and info.get('anomaly_rate', 0) > 10)
            high = sum(1 for info in anomalies.values()
                      if isinstance(info, dict) and 5 < info.get('anomaly_rate', 0) <= 10)
            moderate = sum(1 for info in anomalies.values()
                          if isinstance(info, dict) and 2 < info.get('anomaly_rate', 0) <= 5)
            low = sum(1 for info in anomalies.values()
                     if isinstance(info, dict) and 0 < info.get('anomaly_rate', 0) <= 2)

            headers = ["Severity Level", "Variables", "Threshold"]
            rows = [
                ["Critical", str(critical), "> 10% anomaly rate"],
                ["High", str(high), "5-10% anomaly rate"],
                ["Moderate", str(moderate), "2-5% anomaly rate"],
                ["Low", str(low), "0-2% anomaly rate"],
            ]
            lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _temporal_patterns(self, data: Dict) -> str:
        """Generate temporal pattern analysis."""
        patterns = data.get('temporal_patterns', data.get('patterns_by_year', {}))

        if not patterns:
            return ""

        lines = [self.md.h2("Temporal Patterns")]

        if isinstance(patterns, dict):
            lines.append(self.md.h3("Anomalies by Time Period"))

            headers = ["Period", "Anomaly Count", "Notable Variables"]
            rows = []

            for period, info in sorted(patterns.items()):
                if isinstance(info, dict):
                    count = info.get('count', 0)
                    top_vars = info.get('top_variables', [])
                    vars_str = ", ".join(top_vars[:3]) if top_vars else "—"
                    rows.append([str(period), f"{count:,}", vars_str])
                elif isinstance(info, (int, float)):
                    rows.append([str(period), f"{info:,}", "—"])

            if rows:
                lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        anomaly_imgs = [link for link in img_links if any(term in link.lower()
                       for term in ['anomaly', 'anomalies'])]

        if anomaly_imgs:
            for link in anomaly_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No anomaly visualizations available._")

        return "\n".join(lines)

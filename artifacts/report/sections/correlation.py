"""
Correlation Analysis Section - Variable relationships and correlation patterns.
"""

from typing import Dict, List, Any, Tuple

from report.base import BaseReportSection


class CorrelationSection(BaseReportSection):
    """Correlation analysis section with detailed relationship reporting."""

    def get_filename(self) -> str:
        return "05_correlation_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Correlation Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Analysis of linear relationships between variables. Correlation coefficients "
            "range from -1 (perfect negative) to +1 (perfect positive). Values near 0 indicate weak/no relationship."
        ))
        content.append("")

        content.append(self._correlation_summary(data))
        content.append(self._strong_correlations(data))
        content.append(self._moderate_correlations(data))
        content.append(self._weighted_correlations(data))
        content.append(self._correlation_interpretation(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _correlation_summary(self, data: Dict) -> str:
        """Generate correlation summary statistics."""
        strong = data.get('strong_correlations', [])
        lines = [self.md.h2("Correlation Summary")]

        if not strong:
            lines.append("_No strong correlations detected in the dataset._")
            return "\n".join(lines)

        # Count by direction
        positive = [c for c in strong if len(c) >= 3 and c[2] > 0]
        negative = [c for c in strong if len(c) >= 3 and c[2] < 0]

        # Strength categories
        very_strong = [c for c in strong if len(c) >= 3 and abs(c[2]) >= 0.8]
        strong_corr = [c for c in strong if len(c) >= 3 and 0.6 <= abs(c[2]) < 0.8]
        moderate = [c for c in strong if len(c) >= 3 and 0.4 <= abs(c[2]) < 0.6]

        headers = ["Category", "Count", "Description"]
        rows = [
            ["Very Strong (|r| ≥ 0.8)", len(very_strong), "Nearly deterministic relationship"],
            ["Strong (0.6 ≤ |r| < 0.8)", len(strong_corr), "Strong linear relationship"],
            ["Moderate (0.4 ≤ |r| < 0.6)", len(moderate), "Moderate linear relationship"],
            ["Positive Correlations", len(positive), "Variables move together"],
            ["Negative Correlations", len(negative), "Variables move inversely"],
        ]
        lines.append(self.md.table(headers, rows))
        lines.append("")

        lines.append(self.md.metric("Total Significant Correlations", len(strong)))

        return "\n".join(lines)

    def _strong_correlations(self, data: Dict) -> str:
        """Generate strong correlations section."""
        strong = data.get('strong_correlations', [])
        lines = [self.md.h2("Strong Correlations")]

        if not strong:
            lines.append("_No strong correlations found (|r| ≥ 0.6)._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "Strong correlations (|r| ≥ 0.6) indicate significant linear relationships "
            "that may be important for modeling and interpretation."
        ))
        lines.append("")

        # Filter and sort strong correlations
        filtered = []
        for corr in strong:
            try:
                if len(corr) >= 3 and abs(corr[2]) >= 0.6:
                    filtered.append((corr[0], corr[1], corr[2]))
            except (IndexError, TypeError):
                continue

        if not filtered:
            lines.append("_No correlations with |r| ≥ 0.6 found._")
            return "\n".join(lines)

        # Sort by absolute value
        filtered.sort(key=lambda x: abs(x[2]), reverse=True)

        headers = ["Variable 1", "Variable 2", "Correlation", "Strength", "Direction"]
        rows = []
        for var1, var2, val in filtered[:25]:  # Top 25
            if abs(val) >= 0.8:
                strength = "Very Strong"
            elif abs(val) >= 0.6:
                strength = "Strong"
            else:
                strength = "Moderate"

            direction = "Positive" if val > 0 else "Negative"
            arrow = "→" if val > 0 else "↔"

            rows.append([var1, var2, f"{val:.3f}", strength, direction])

        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _moderate_correlations(self, data: Dict) -> str:
        """Generate moderate correlations section."""
        strong = data.get('strong_correlations', [])

        # Filter for moderate correlations
        moderate = []
        for corr in strong:
            try:
                if len(corr) >= 3 and 0.3 <= abs(corr[2]) < 0.6:
                    moderate.append((corr[0], corr[1], corr[2]))
            except (IndexError, TypeError):
                continue

        if not moderate:
            return ""

        lines = [self.md.h2("Moderate Correlations")]
        lines.append(self.md.blockquote(
            "Moderate correlations (0.3 ≤ |r| < 0.6) suggest meaningful but not dominant relationships."
        ))
        lines.append("")

        # Sort by absolute value
        moderate.sort(key=lambda x: abs(x[2]), reverse=True)

        headers = ["Variable 1", "Variable 2", "Correlation", "Direction"]
        rows = []
        for var1, var2, val in moderate[:20]:  # Top 20
            direction = "Positive" if val > 0 else "Negative"
            rows.append([var1, var2, f"{val:.3f}", direction])

        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _weighted_correlations(self, data: Dict) -> str:
        """Generate weighted correlations section."""
        weighted_corrs = data.get('weighted_correlations', {})
        if not weighted_corrs:
            return ""

        lines = [self.md.h2("Weighted Correlations (ACS Sample Weights)")]
        lines.append(self.md.blockquote(
            "Correlations computed using ACS sample weights to account for survey design. "
            "These provide population-representative estimates."
        ))
        lines.append("")

        # Process aggregated weighted correlations
        aggregated = weighted_corrs.get('aggregated', {})
        if aggregated:
            # Sort by absolute correlation value
            sorted_corrs = sorted(
                aggregated.items(),
                key=lambda x: abs(x[1].get('avg_weighted_corr', 0)) if isinstance(x[1], dict) else 0,
                reverse=True
            )[:15]  # Top 15

            headers = ["Variable Pair", "Weighted Corr", "Years", "Consistency"]
            rows = []
            for pair, stats in sorted_corrs:
                if not isinstance(stats, dict):
                    continue
                try:
                    var1, var2 = pair.split('__')
                    wcorr = stats.get('avg_weighted_corr', 0)
                    n_years = stats.get('n_years', 0)
                    std = stats.get('std_weighted_corr', 0)

                    # Assess consistency across years
                    if std < 0.05:
                        consistency = "Very Stable"
                    elif std < 0.1:
                        consistency = "Stable"
                    else:
                        consistency = "Variable"

                    rows.append([f"{var1} ↔ {var2}", f"{wcorr:.3f}", str(n_years), consistency])
                except (ValueError, AttributeError):
                    continue

            if rows:
                lines.append(self.md.table(headers, rows))

        # By-year breakdown if available
        by_year = weighted_corrs.get('by_year', {})
        if by_year and len(by_year) <= 5:
            lines.append("")
            lines.append(self.md.h3("Year-by-Year Weighted Correlations"))

            for year, year_corrs in sorted(by_year.items()):
                if isinstance(year_corrs, dict):
                    lines.append(self.md.h4(f"Year {year}"))
                    top_corrs = sorted(
                        year_corrs.items(),
                        key=lambda x: abs(x[1]) if isinstance(x[1], (int, float)) else 0,
                        reverse=True
                    )[:5]
                    for pair, val in top_corrs:
                        lines.append(self.md.bullet(f"{pair}: {val:.3f}"))
                    lines.append("")

        return "\n".join(lines)

    def _correlation_interpretation(self, data: Dict) -> str:
        """Generate correlation interpretation guide."""
        lines = [self.md.h2("Correlation Interpretation Guide")]

        headers = ["Range", "Interpretation", "Implications"]
        rows = [
            ["0.8 to 1.0", "Very Strong Positive", "Variables strongly increase together"],
            ["0.6 to 0.8", "Strong Positive", "Clear positive relationship"],
            ["0.4 to 0.6", "Moderate Positive", "Noticeable positive trend"],
            ["0.2 to 0.4", "Weak Positive", "Slight positive tendency"],
            ["-0.2 to 0.2", "Negligible", "No meaningful linear relationship"],
            ["-0.4 to -0.2", "Weak Negative", "Slight negative tendency"],
            ["-0.6 to -0.4", "Moderate Negative", "Noticeable negative trend"],
            ["-0.8 to -0.6", "Strong Negative", "Clear negative relationship"],
            ["-1.0 to -0.8", "Very Strong Negative", "Variables strongly move inversely"],
        ]
        lines.append(self.md.table(headers, rows))

        lines.append("")
        lines.append(self.md.note(
            "Correlation does not imply causation. Strong correlations may be due to "
            "confounding variables, spurious relationships, or shared underlying factors."
        ))

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        corr_imgs = [link for link in img_links if any(term in link.lower()
                    for term in ['correlation', 'heatmap', 'scatter', 'pair'])]

        if corr_imgs:
            for link in corr_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_See correlation heatmap in figures directory._")

        return "\n".join(lines)

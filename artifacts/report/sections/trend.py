"""
Trend Analysis Section - Long-term trend identification and analysis.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class TrendSection(BaseReportSection):
    """Trend analysis section with comprehensive trend reporting."""

    def get_filename(self) -> str:
        return "09_trend_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Trend Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Analysis of long-term trends in key variables, including trend direction, "
            "strength, and statistical significance."
        ))
        content.append("")

        content.append(self._trend_summary(data))
        content.append(self._strong_trends(data))
        content.append(self._trend_categories(data))
        content.append(self._trend_details(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _trend_summary(self, data: Dict) -> str:
        """Generate trend summary section."""
        summary = data.get('trend_summary', {})
        lines = [self.md.h2("Trend Summary")]

        if not summary:
            lines.append("_No trend summary available._")
            return "\n".join(lines)

        # Sort by absolute slope
        sorted_trends = sorted(
            [(var, info) for var, info in summary.items() if isinstance(info, dict)],
            key=lambda x: abs(x[1].get('slope', 0)),
            reverse=True
        )

        headers = ["Variable", "Slope", "Direction", "R²", "Significance"]
        rows = []

        for var, info in sorted_trends[:20]:
            slope = info.get('slope', 0)
            r2 = info.get('r2', info.get('r_squared', None))
            p_value = info.get('p_value', info.get('pvalue', None))

            # Determine direction
            if slope > 0.01:
                direction = "Increasing"
            elif slope < -0.01:
                direction = "Decreasing"
            else:
                direction = "Stable"

            # Format values
            slope_str = f"{slope:.4f}"
            r2_str = f"{r2:.4f}" if r2 is not None else "—"

            # Significance assessment
            if p_value is not None:
                if p_value < 0.01:
                    sig = "***"
                elif p_value < 0.05:
                    sig = "**"
                elif p_value < 0.1:
                    sig = "*"
                else:
                    sig = "NS"
            else:
                sig = "—"

            rows.append([var, slope_str, direction, r2_str, sig])

        if rows:
            lines.append(self.md.table(headers, rows))
            lines.append("")
            lines.append(self.md.note(
                "Significance: *** p<0.01, ** p<0.05, * p<0.1, NS: Not Significant"
            ))

        return "\n".join(lines)

    def _strong_trends(self, data: Dict) -> str:
        """Generate strong trends section."""
        strong = data.get('strong_trends', [])
        summary = data.get('trend_summary', {})

        lines = [self.md.h2("Strong Trends")]

        # Identify strong trends if not provided
        if not strong and summary:
            strong = [var for var, info in summary.items()
                     if isinstance(info, dict) and abs(info.get('slope', 0)) > 0.05]

        if strong:
            lines.append(self.md.blockquote(
                "Variables showing significant long-term trends that may require attention "
                "or represent important patterns in the data."
            ))
            lines.append("")

            for var in strong[:15]:
                info = summary.get(var, {})
                if isinstance(info, dict):
                    slope = info.get('slope', 0)
                    direction = "increasing" if slope > 0 else "decreasing"
                    lines.append(self.md.bullet(
                        f"**{var}**: {direction} trend (slope: {slope:.4f})"
                    ))
                else:
                    lines.append(self.md.bullet(f"**{var}**"))
        else:
            lines.append("_No strong trends identified._")

        return "\n".join(lines)

    def _trend_categories(self, data: Dict) -> str:
        """Generate trend categories summary."""
        cats = data.get('trend_categories', {})
        summary = data.get('trend_summary', {})

        lines = [self.md.h2("Trend Categories")]

        # Calculate from summary if not provided
        if not cats and summary:
            growing = sum(1 for info in summary.values()
                         if isinstance(info, dict) and info.get('slope', 0) > 0.01)
            declining = sum(1 for info in summary.values()
                           if isinstance(info, dict) and info.get('slope', 0) < -0.01)
            stable = len(summary) - growing - declining
            cats = {'growing': growing, 'declining': declining, 'stable': stable}

        if cats:
            total = sum(cats.values()) or 1

            headers = ["Category", "Count", "Percentage", "Description"]
            rows = [
                ["Growing", str(cats.get('growing', 0)),
                 f"{(cats.get('growing', 0)/total)*100:.1f}%", "Upward trend"],
                ["Declining", str(cats.get('declining', 0)),
                 f"{(cats.get('declining', 0)/total)*100:.1f}%", "Downward trend"],
                ["Stable", str(cats.get('stable', 0)),
                 f"{(cats.get('stable', 0)/total)*100:.1f}%", "No significant trend"],
            ]
            lines.append(self.md.table(headers, rows))

            # Interpretation
            dominant = max(cats.items(), key=lambda x: x[1])[0]
            lines.append("")
            lines.append(self.md.interpretation(
                f"The majority of variables show {dominant} trends, suggesting "
                f"{'overall growth' if dominant == 'growing' else 'overall decline' if dominant == 'declining' else 'stability'} in the data."
            ))
        else:
            lines.append("_Trend category data not available._")

        return "\n".join(lines)

    def _trend_details(self, data: Dict) -> str:
        """Generate detailed trend information."""
        summary = data.get('trend_summary', {})

        if not summary:
            return ""

        lines = [self.md.h2("Trend Equations")]

        lines.append(self.md.blockquote(
            "Linear trend equations of the form: y = slope × year + intercept"
        ))
        lines.append("")

        # Show top trends with full equations
        sorted_trends = sorted(
            [(var, info) for var, info in summary.items()
             if isinstance(info, dict) and info.get('slope') is not None],
            key=lambda x: abs(x[1].get('slope', 0)),
            reverse=True
        )[:10]

        for var, info in sorted_trends:
            slope = info.get('slope', 0)
            intercept = info.get('intercept', 0)
            r2 = info.get('r2', info.get('r_squared', None))

            lines.append(self.md.h4(var))

            # Trend equation
            sign = "+" if intercept >= 0 else "-"
            equation = f"y = {slope:.4f} × year {sign} {abs(intercept):.2f}"
            lines.append(f"**Equation**: `{equation}`")
            lines.append("")

            if r2 is not None:
                lines.append(self.md.bullet(f"**R²**: {r2:.4f} ({self._interpret_r2(r2)})"))

            # Annual change interpretation
            if slope != 0:
                direction = "increase" if slope > 0 else "decrease"
                lines.append(self.md.bullet(
                    f"**Annual Change**: {abs(slope):.4f} unit {direction} per year"
                ))

            lines.append("")

        return "\n".join(lines)

    def _interpret_r2(self, r2: float) -> str:
        """Interpret R² for trend fit."""
        if r2 >= 0.9:
            return "very strong trend"
        elif r2 >= 0.7:
            return "strong trend"
        elif r2 >= 0.5:
            return "moderate trend"
        elif r2 >= 0.3:
            return "weak trend"
        else:
            return "no clear trend"

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        trend_imgs = [link for link in img_links if any(term in link.lower()
                     for term in ['trend', 'growth', 'yoy'])]

        if trend_imgs:
            for link in trend_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No trend visualizations available._")

        return "\n".join(lines)

"""
Temporal Analysis Section - Year-over-year trends and temporal patterns.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class TemporalSection(BaseReportSection):
    """Temporal analysis section with enhanced trend reporting."""

    def get_filename(self) -> str:
        return "02_temporal_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Temporal Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Analysis of data patterns and trends over time, including year-over-year changes "
            "and growth rate calculations."
        ))
        content.append("")

        content.append(self._year_distribution(data))
        content.append(self._sample_size_analysis(data))
        content.append(self._trends(data))
        content.append(self._growth_rates(data))
        content.append(self._year_over_year_changes(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _year_distribution(self, data: Dict) -> str:
        """Generate year distribution section with table format."""
        dist = data.get('year_distribution', {})
        lines = [self.md.h2("Year Distribution")]

        if not dist:
            lines.append("_No year distribution data available._")
            return "\n".join(lines)

        # Summary statistics
        years = sorted(dist.keys())
        total_records = sum(dist.values())
        avg_per_year = total_records / len(dist) if dist else 0

        lines.append(self.md.h3("Summary"))
        lines.append(self.md.metric("Total Years", len(years)))
        lines.append(self.md.metric("Year Range", f"{min(years)} - {max(years)}"))
        lines.append(self.md.metric("Total Records", total_records))
        lines.append(self.md.metric("Average Records/Year", avg_per_year, precision=0))
        lines.append("")

        # Distribution table
        lines.append(self.md.h3("Records by Year"))
        headers = ["Year", "Records", "% of Total", "Deviation from Avg"]
        rows = []
        for year, count in sorted(dist.items()):
            pct = (count / total_records) * 100 if total_records > 0 else 0
            deviation = ((count - avg_per_year) / avg_per_year) * 100 if avg_per_year > 0 else 0
            deviation_str = f"+{deviation:.1f}%" if deviation > 0 else f"{deviation:.1f}%"
            rows.append([str(year), f"{count:,}", f"{pct:.1f}%", deviation_str])

        lines.append(self.md.table(headers, rows))

        # Interpretation
        if len(years) >= 2:
            first_count = dist[min(years)]
            last_count = dist[max(years)]
            change = ((last_count - first_count) / first_count) * 100 if first_count > 0 else 0
            direction = "increased" if change > 0 else "decreased"
            lines.append(self.md.interpretation(
                f"Sample size {direction} by {abs(change):.1f}% from {min(years)} to {max(years)}."
            ))

        return "\n".join(lines)

    def _sample_size_analysis(self, data: Dict) -> str:
        """Analyze sample size consistency across years."""
        dist = data.get('year_distribution', {})
        if not dist or len(dist) < 2:
            return ""

        lines = [self.md.h2("Sample Size Consistency")]

        counts = list(dist.values())
        avg = sum(counts) / len(counts)
        variance = sum((c - avg) ** 2 for c in counts) / len(counts)
        std_dev = variance ** 0.5
        cv = (std_dev / avg) * 100 if avg > 0 else 0

        # Coefficient of variation assessment
        if cv < 10:
            consistency = "highly consistent"
            assessment = "Sample sizes are stable across years."
        elif cv < 25:
            consistency = "moderately consistent"
            assessment = "Some variation in sample sizes, but within acceptable range."
        else:
            consistency = "variable"
            assessment = "Significant variation in sample sizes may affect year-over-year comparisons."

        lines.append(self.md.metric("Standard Deviation", std_dev, "records", 0))
        lines.append(self.md.metric("Coefficient of Variation", cv, "%", 1))
        lines.append(self.md.metric("Consistency Rating", consistency))
        lines.append("")
        lines.append(self.md.interpretation(assessment))

        return "\n".join(lines)

    def _trends(self, data: Dict) -> str:
        """Generate temporal trends section with direction indicators."""
        trends = data.get('trends', {})
        lines = [self.md.h2("Temporal Trends")]

        if not trends:
            lines.append("_No trend data available._")
            return "\n".join(lines)

        # Group trends by direction
        increasing = []
        decreasing = []
        stable = []

        for var, trend in trends.items():
            trend_str = str(trend).lower()
            if 'increas' in trend_str or 'up' in trend_str or 'grow' in trend_str:
                increasing.append((var, trend))
            elif 'decreas' in trend_str or 'down' in trend_str or 'declin' in trend_str:
                decreasing.append((var, trend))
            else:
                stable.append((var, trend))

        # Summary
        lines.append(self.md.h3("Trend Summary"))
        headers = ["Direction", "Count", "Percentage"]
        total = len(trends)
        rows = [
            ["Increasing", len(increasing), f"{(len(increasing)/total)*100:.1f}%"],
            ["Decreasing", len(decreasing), f"{(len(decreasing)/total)*100:.1f}%"],
            ["Stable/Other", len(stable), f"{(len(stable)/total)*100:.1f}%"],
        ]
        lines.append(self.md.table(headers, rows))
        lines.append("")

        # Detailed trends
        if increasing:
            lines.append(self.md.h3("Increasing Trends"))
            for var, trend in increasing[:10]:  # Limit to top 10
                lines.append(self.md.bullet(f"**{var}**: {trend}"))
            lines.append("")

        if decreasing:
            lines.append(self.md.h3("Decreasing Trends"))
            for var, trend in decreasing[:10]:
                lines.append(self.md.bullet(f"**{var}**: {trend}"))
            lines.append("")

        return "\n".join(lines)

    def _growth_rates(self, data: Dict) -> str:
        """Generate growth rates section with detailed analysis."""
        growth = data.get('growth_rates', {})
        lines = [self.md.h2("Growth Rates")]

        if not growth:
            lines.append("_No growth rate data available._")
            return "\n".join(lines)

        # Sort by absolute growth rate
        sorted_growth = sorted(growth.items(), key=lambda x: abs(x[1]), reverse=True)

        # Summary statistics
        rates = list(growth.values())
        avg_rate = sum(rates) / len(rates) if rates else 0
        positive_count = sum(1 for r in rates if r > 0)
        negative_count = sum(1 for r in rates if r < 0)

        lines.append(self.md.h3("Growth Rate Summary"))
        lines.append(self.md.metric("Average Growth Rate", avg_rate * 100, "%", 2))
        lines.append(self.md.metric("Variables with Positive Growth", positive_count))
        lines.append(self.md.metric("Variables with Negative Growth", negative_count))
        lines.append("")

        # Top growth rates table
        lines.append(self.md.h3("Top Growth Rates"))
        headers = ["Variable", "Growth Rate", "Direction"]
        rows = []
        for var, rate in sorted_growth[:15]:
            direction = "Increasing" if rate > 0 else "Decreasing" if rate < 0 else "Stable"
            rows.append([var, f"{rate:.2%}", direction])
        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _year_over_year_changes(self, data: Dict) -> str:
        """Generate year-over-year change analysis."""
        yoy = data.get('yoy_changes', {})
        if not yoy:
            return ""

        lines = [self.md.h2("Year-over-Year Changes")]

        for var, changes in list(yoy.items())[:5]:  # Top 5 variables
            lines.append(self.md.h3(var))
            if isinstance(changes, dict):
                headers = ["Period", "Change", "% Change"]
                rows = []
                for period, change_data in sorted(changes.items()):
                    if isinstance(change_data, dict):
                        abs_change = change_data.get('absolute', 0)
                        pct_change = change_data.get('percentage', 0)
                        rows.append([str(period), f"{abs_change:,.2f}", f"{pct_change:.2f}%"])
                if rows:
                    lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        temporal_imgs = [link for link in img_links if any(term in link.lower()
                        for term in ['temporal', 'year', 'yoy', 'trend', 'growth', 'sample_size'])]

        if temporal_imgs:
            for link in temporal_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No temporal visualizations available._")

        return "\n".join(lines)

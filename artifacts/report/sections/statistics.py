"""
Statistical Analysis Section - Comprehensive descriptive statistics and distributions.
"""

from typing import Dict, List, Any, Optional

from report.base import BaseReportSection


class StatisticsSection(BaseReportSection):
    """Statistical analysis section with enhanced metrics and interpretations."""

    def get_filename(self) -> str:
        return "04_statistical_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Statistical Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Comprehensive descriptive statistics including central tendency, dispersion, "
            "distribution characteristics, and weighted statistics using ACS sample weights."
        ))
        content.append("")

        content.append(self._summary_stats(data))
        content.append(self._distributions(data))
        content.append(self._variance_analysis(data))
        content.append(self._percentile_analysis(data))
        content.append(self._missing_data_analysis(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _summary_stats(self, data: Dict) -> str:
        """Generate comprehensive summary statistics section."""
        summary = data.get('summary_statistics', {})
        lines = [self.md.h2("Summary Statistics")]

        if not summary:
            lines.append("_No summary statistics available._")
            return "\n".join(lines)

        # Count variables by type
        numeric_count = len(summary)
        lines.append(self.md.metric("Variables Analyzed", numeric_count))
        lines.append("")

        # Process each variable
        for var, stats in list(summary.items()):
            if not isinstance(stats, dict):
                continue

            lines.append(self.md.h3(var))

            # Create comprehensive stats table
            headers = ["Statistic", "Unweighted", "Weighted (ACS)"]
            rows = []

            # Extract values with defaults
            mean = stats.get('mean', stats.get('Mean', None))
            median = stats.get('median', stats.get('Median', None))
            std = stats.get('std_dev', stats.get('std', stats.get('Std Dev', None)))
            min_val = stats.get('min', stats.get('Min', None))
            max_val = stats.get('max', stats.get('Max', None))
            weighted_mean = stats.get('weighted_mean_avg', stats.get('weighted_mean', None))
            weighted_median = stats.get('weighted_median_avg', stats.get('weighted_median', None))

            # Additional statistics
            skewness = stats.get('skewness', stats.get('skew', None))
            kurtosis = stats.get('kurtosis', stats.get('kurt', None))
            p25 = stats.get('25%', stats.get('p25', stats.get('percentile_25', None)))
            p75 = stats.get('75%', stats.get('p75', stats.get('percentile_75', None)))
            count = stats.get('count', stats.get('n', None))
            missing = stats.get('missing', stats.get('null_count', None))

            # Build rows
            if mean is not None:
                w_mean = f"{weighted_mean:,.2f}" if weighted_mean is not None else "N/A"
                rows.append(["Mean", f"{mean:,.2f}", w_mean])

            if median is not None:
                w_median = f"{weighted_median:,.2f}" if weighted_median is not None else "N/A"
                rows.append(["Median", f"{median:,.2f}", w_median])

            if std is not None:
                rows.append(["Std Deviation", f"{std:,.2f}", "—"])

            if min_val is not None:
                rows.append(["Minimum", f"{min_val:,.2f}", "—"])

            if max_val is not None:
                rows.append(["Maximum", f"{max_val:,.2f}", "—"])

            if p25 is not None and p75 is not None:
                iqr = p75 - p25
                rows.append(["25th Percentile", f"{p25:,.2f}", "—"])
                rows.append(["75th Percentile", f"{p75:,.2f}", "—"])
                rows.append(["IQR", f"{iqr:,.2f}", "—"])

            if count is not None:
                rows.append(["Count", f"{int(count):,}", "—"])

            if rows:
                lines.append(self.md.table(headers, rows))

            # Distribution shape interpretation
            shape_notes = []
            if skewness is not None:
                if skewness > 1:
                    shape_notes.append(f"highly right-skewed (skewness: {skewness:.2f})")
                elif skewness > 0.5:
                    shape_notes.append(f"moderately right-skewed (skewness: {skewness:.2f})")
                elif skewness < -1:
                    shape_notes.append(f"highly left-skewed (skewness: {skewness:.2f})")
                elif skewness < -0.5:
                    shape_notes.append(f"moderately left-skewed (skewness: {skewness:.2f})")
                else:
                    shape_notes.append(f"approximately symmetric (skewness: {skewness:.2f})")

            if kurtosis is not None:
                if kurtosis > 3:
                    shape_notes.append(f"heavy-tailed/leptokurtic (kurtosis: {kurtosis:.2f})")
                elif kurtosis < 3:
                    shape_notes.append(f"light-tailed/platykurtic (kurtosis: {kurtosis:.2f})")

            if shape_notes:
                lines.append(self.md.interpretation("Distribution is " + ", ".join(shape_notes) + "."))

            # Coefficient of variation
            if mean is not None and std is not None and mean != 0:
                cv = (std / abs(mean)) * 100
                if cv > 100:
                    cv_interp = "very high variability"
                elif cv > 50:
                    cv_interp = "high variability"
                elif cv > 25:
                    cv_interp = "moderate variability"
                else:
                    cv_interp = "low variability"
                lines.append(self.md.metric("Coefficient of Variation", cv, f"% ({cv_interp})", 1))

            # Per-year weighted breakdown (if available and not too many years)
            weighted_by_year = stats.get('weighted_by_year', {})
            if weighted_by_year and 2 <= len(weighted_by_year) <= 8:
                lines.append("")
                lines.append(self.md.h4("Weighted Statistics by Year"))
                year_headers = ["Year", "Weighted Mean", "Weighted Median"]
                year_rows = []
                for year, year_stats in sorted(weighted_by_year.items()):
                    if isinstance(year_stats, dict):
                        w_mean = year_stats.get('weighted_mean', 0)
                        w_med = year_stats.get('weighted_median', 0)
                        year_rows.append([str(year), f"{w_mean:,.2f}", f"{w_med:,.2f}"])
                if year_rows:
                    lines.append(self.md.table(year_headers, year_rows))

            lines.append("")

        return "\n".join(lines)

    def _distributions(self, data: Dict) -> str:
        """Generate distribution analysis section."""
        dist = data.get('distribution_analysis', {})
        summary = data.get('summary_statistics', {})
        lines = [self.md.h2("Distribution Analysis")]

        # Extract skewness info from summary stats if distribution_analysis is empty
        skewed_vars = []
        for var, stats in summary.items():
            if isinstance(stats, dict):
                skewness = stats.get('skewness', stats.get('skew', None))
                if skewness is not None and abs(skewness) > 0.5:
                    direction = "right" if skewness > 0 else "left"
                    skewed_vars.append((var, skewness, direction))

        skewed_from_dist = dist.get('skewed_distributions', [])

        if skewed_vars:
            lines.append(self.md.h3("Skewed Distributions"))
            lines.append(self.md.blockquote(
                "Variables with skewness > |0.5| indicate non-normal distributions. "
                "Consider log transformations for highly skewed variables in modeling."
            ))
            lines.append("")

            # Sort by absolute skewness
            skewed_vars.sort(key=lambda x: abs(x[1]), reverse=True)

            headers = ["Variable", "Skewness", "Direction", "Severity"]
            rows = []
            for var, skew, direction in skewed_vars[:20]:  # Top 20
                if abs(skew) > 1:
                    severity = "High"
                else:
                    severity = "Moderate"
                rows.append([var, f"{skew:.3f}", f"{direction.title()}-skewed", severity])

            lines.append(self.md.table(headers, rows))

            # Summary
            lines.append("")
            lines.append(self.md.metric("Total Skewed Variables", len(skewed_vars)))
            right_count = sum(1 for _, _, d in skewed_vars if d == "right")
            left_count = len(skewed_vars) - right_count
            lines.append(self.md.metric("Right-skewed", right_count))
            lines.append(self.md.metric("Left-skewed", left_count))

        elif skewed_from_dist:
            lines.append(self.md.h3("Skewed Distributions"))
            for var in skewed_from_dist:
                lines.append(self.md.bullet(f"**{var}**: Non-normal distribution detected"))
        else:
            # Generate from summary stats if available
            if summary:
                lines.append("_Distribution analysis metrics extracted from summary statistics above._")
                lines.append("")
                lines.append(self.md.interpretation(
                    "See individual variable statistics for skewness and kurtosis values."
                ))
            else:
                lines.append("_No distribution analysis available._")

        return "\n".join(lines)

    def _variance_analysis(self, data: Dict) -> str:
        """Generate variance analysis section with CV rankings."""
        high_var = data.get('high_variance_vars', [])
        summary = data.get('summary_statistics', {})
        lines = [self.md.h2("Variance Analysis")]

        # Calculate CV for all variables
        cv_data = []
        for var, stats in summary.items():
            if isinstance(stats, dict):
                mean = stats.get('mean', stats.get('Mean', None))
                std = stats.get('std_dev', stats.get('std', stats.get('Std Dev', None)))
                if mean is not None and std is not None and mean != 0:
                    cv = (std / abs(mean)) * 100
                    cv_data.append((var, cv, std, mean))

        if cv_data:
            # Sort by CV descending
            cv_data.sort(key=lambda x: x[1], reverse=True)

            lines.append(self.md.h3("Coefficient of Variation Ranking"))
            lines.append(self.md.blockquote(
                "CV (Coefficient of Variation) = (Std Dev / Mean) × 100%. "
                "Higher CV indicates greater relative variability."
            ))
            lines.append("")

            headers = ["Variable", "CV (%)", "Std Dev", "Mean", "Variability"]
            rows = []
            for var, cv, std, mean in cv_data[:20]:  # Top 20
                if cv > 100:
                    variability = "Very High"
                elif cv > 50:
                    variability = "High"
                elif cv > 25:
                    variability = "Moderate"
                else:
                    variability = "Low"
                rows.append([var, f"{cv:.1f}%", f"{std:,.2f}", f"{mean:,.2f}", variability])

            lines.append(self.md.table(headers, rows))

            # Summary statistics
            lines.append("")
            cvs = [cv for _, cv, _, _ in cv_data]
            lines.append(self.md.metric("Average CV", sum(cvs) / len(cvs), "%", 1))
            lines.append(self.md.metric("High Variance Variables (CV > 50%)",
                                       sum(1 for cv in cvs if cv > 50)))

        elif high_var:
            lines.append(self.md.h3("High Variance Variables"))
            for var in high_var:
                lines.append(self.md.bullet(f"**{var}**"))
        else:
            lines.append("_Variance analysis computed from summary statistics above._")

        return "\n".join(lines)

    def _percentile_analysis(self, data: Dict) -> str:
        """Generate percentile analysis section."""
        summary = data.get('summary_statistics', {})

        # Check if we have percentile data
        has_percentiles = False
        for var, stats in summary.items():
            if isinstance(stats, dict):
                if any(k in stats for k in ['25%', 'p25', 'percentile_25', '75%', 'p75', 'percentile_75']):
                    has_percentiles = True
                    break

        if not has_percentiles:
            return ""

        lines = [self.md.h2("Percentile Analysis")]
        lines.append(self.md.blockquote(
            "Percentiles show data distribution boundaries. "
            "The IQR (75th - 25th percentile) indicates the spread of the middle 50% of data."
        ))
        lines.append("")

        headers = ["Variable", "25th %ile", "Median", "75th %ile", "IQR"]
        rows = []

        for var, stats in list(summary.items())[:15]:  # Limit to 15 vars
            if not isinstance(stats, dict):
                continue

            p25 = stats.get('25%', stats.get('p25', stats.get('percentile_25', None)))
            median = stats.get('median', stats.get('Median', stats.get('50%', None)))
            p75 = stats.get('75%', stats.get('p75', stats.get('percentile_75', None)))

            if p25 is not None and p75 is not None:
                iqr = p75 - p25
                med_str = f"{median:,.2f}" if median is not None else "N/A"
                rows.append([var, f"{p25:,.2f}", med_str, f"{p75:,.2f}", f"{iqr:,.2f}"])

        if rows:
            lines.append(self.md.table(headers, rows))
        else:
            lines.append("_Percentile data not available for variables._")

        return "\n".join(lines)

    def _missing_data_analysis(self, data: Dict) -> str:
        """Generate missing data analysis section."""
        summary = data.get('summary_statistics', {})
        missing_info = data.get('missing_data', {})

        # Try to extract missing info from summary
        missing_vars = []
        for var, stats in summary.items():
            if isinstance(stats, dict):
                missing = stats.get('missing', stats.get('null_count', stats.get('na_count', None)))
                count = stats.get('count', stats.get('n', None))
                if missing is not None and count is not None and missing > 0:
                    pct = (missing / (count + missing)) * 100
                    missing_vars.append((var, missing, pct))

        if not missing_vars and not missing_info:
            return ""

        lines = [self.md.h2("Missing Data Analysis")]

        if missing_vars:
            # Sort by missing count
            missing_vars.sort(key=lambda x: x[1], reverse=True)

            headers = ["Variable", "Missing Count", "Missing %"]
            rows = [(var, f"{count:,}", f"{pct:.1f}%") for var, count, pct in missing_vars[:15]]
            lines.append(self.md.table(headers, rows))

            total_missing = sum(m for _, m, _ in missing_vars)
            lines.append("")
            lines.append(self.md.metric("Total Missing Values", total_missing))
            lines.append(self.md.metric("Variables with Missing Data", len(missing_vars)))

        elif missing_info:
            for var, info in list(missing_info.items())[:15]:
                if isinstance(info, dict):
                    count = info.get('count', 0)
                    pct = info.get('percentage', 0)
                    lines.append(self.md.bullet(f"**{var}**: {count:,} missing ({pct:.1f}%)"))

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        stat_imgs = [link for link in img_links if any(term in link.lower()
                    for term in ['box', 'distribution', 'violin', 'statistical',
                                'histogram', 'density', 'feature_distributions'])]

        if stat_imgs:
            for link in stat_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No statistical visualizations available._")

        return "\n".join(lines)

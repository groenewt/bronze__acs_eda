"""
Disability Analysis Section - Disability prevalence, types, and socioeconomic impacts.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class DisabilitySection(BaseReportSection):
    """Disability analysis section with prevalence, types, and impact metrics."""

    def get_filename(self) -> str:
        return "06a_disability_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Disability Analysis")]

        content.append(self.md.blockquote(
            "Analysis of disability prevalence, types, and socioeconomic impacts including "
            "employment gaps and income disparities for individuals with disabilities."
        ))
        content.append("")

        content.append(self._prevalence(data))
        content.append(self._disability_types(data))
        content.append(self._employment_gap(data))
        content.append(self._income_gap(data))
        content.append(self._age_patterns(data))
        content.append(self._trends(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _prevalence(self, data: Dict) -> str:
        """Generate disability prevalence overview."""
        lines = [self.md.h2("Disability Prevalence")]

        prevalence = self._safe_get(data, 'prevalence', default={})

        if not prevalence:
            lines.append("_No disability prevalence data available._")
            return "\n".join(lines)

        overall_rate = prevalence.get('overall_rate')
        total_count = prevalence.get('count')
        total_pop = prevalence.get('total_population')

        if overall_rate is not None:
            lines.append(self.md.metric("Overall Disability Rate", overall_rate, "%", 1))
        if total_count is not None:
            lines.append(self.md.metric("Population with Disability", total_count, "", 0))
        if total_pop is not None:
            lines.append(self.md.metric("Total Population Analyzed", total_pop, "", 0))

        if overall_rate and overall_rate > 15:
            lines.append(self.md.interpretation(
                f"Disability rate of {overall_rate:.1f}% is above the national average (~12-13%), "
                "suggesting an older population or higher prevalence of health challenges."
            ))
        elif overall_rate and overall_rate < 10:
            lines.append(self.md.interpretation(
                f"Disability rate of {overall_rate:.1f}% is below the national average, "
                "which may reflect a younger population demographic."
            ))

        lines.append("")
        return "\n".join(lines)

    def _disability_types(self, data: Dict) -> str:
        """Generate disability type breakdown."""
        lines = [self.md.h2("Disability Type Breakdown")]

        types = self._safe_get(data, 'disability_types', default={})

        if not types:
            lines.append("_No disability type data available._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "ACS tracks six disability types: hearing, vision, cognitive, ambulatory, "
            "self-care, and independent living difficulties."
        ))
        lines.append("")

        headers = ["Disability Type", "Prevalence (%)"]
        rows = []
        for dis_type, rate in sorted(types.items(), key=lambda x: x[1], reverse=True):
            type_name = dis_type.replace('_', ' ').replace('Difficulty', '').strip()
            rows.append([type_name, f"{rate:.2f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify most common
            most_common = max(types.items(), key=lambda x: x[1])
            lines.append(self.md.interpretation(
                f"{most_common[0].replace('_', ' ')} is the most prevalent disability type at {most_common[1]:.2f}%."
            ))

        lines.append("")
        return "\n".join(lines)

    def _employment_gap(self, data: Dict) -> str:
        """Generate employment gap analysis."""
        lines = [self.md.h2("Employment Gap Analysis")]

        employment = self._safe_get(data, 'employment_gap', default={})

        if not employment:
            lines.append("_No employment gap data available._")
            return "\n".join(lines)

        disabled_rate = employment.get('disabled_employment_rate')
        non_disabled_rate = employment.get('non_disabled_employment_rate')
        gap = employment.get('employment_gap')

        headers = ["Group", "Employment Rate"]
        rows = []
        if disabled_rate is not None:
            rows.append(["With Disability", f"{disabled_rate:.1f}%"])
        if non_disabled_rate is not None:
            rows.append(["Without Disability", f"{non_disabled_rate:.1f}%"])
        if gap is not None:
            rows.append(["**Gap**", f"**{gap:.1f} pp**"])

        if rows:
            lines.append(self.md.table(headers, rows))

        if gap and gap > 30:
            lines.append(self.md.interpretation(
                f"A {gap:.1f} percentage point employment gap indicates significant barriers "
                "for individuals with disabilities in accessing employment opportunities."
            ))

        lines.append("")
        return "\n".join(lines)

    def _income_gap(self, data: Dict) -> str:
        """Generate income disparity analysis."""
        lines = [self.md.h2("Income Disparity")]

        income = self._safe_get(data, 'income_gap', default={})

        if not income:
            lines.append("_No income gap data available._")
            return "\n".join(lines)

        disabled_income = income.get('disabled_median_income')
        non_disabled_income = income.get('non_disabled_median_income')
        gap_pct = income.get('income_gap_percent')

        headers = ["Group", "Median Income"]
        rows = []
        if disabled_income is not None:
            rows.append(["With Disability", f"${disabled_income:,.0f}"])
        if non_disabled_income is not None:
            rows.append(["Without Disability", f"${non_disabled_income:,.0f}"])
        if gap_pct is not None:
            rows.append(["**Gap**", f"**{gap_pct:.1f}%**"])

        if rows:
            lines.append(self.md.table(headers, rows))

        if gap_pct and gap_pct > 20:
            lines.append(self.md.interpretation(
                f"Individuals with disabilities earn {gap_pct:.1f}% less than their non-disabled counterparts, "
                "highlighting significant economic disparities."
            ))

        lines.append("")
        return "\n".join(lines)

    def _age_patterns(self, data: Dict) -> str:
        """Generate disability by age analysis."""
        lines = [self.md.h2("Disability by Age Group")]

        by_age = self._safe_get(data, 'by_age', default={})

        if not by_age:
            return ""

        headers = ["Age Group", "Disability Rate"]
        rows = [[age, f"{rate:.1f}%"] for age, rate in by_age.items()]

        if rows:
            lines.append(self.md.table(headers, rows))
            lines.append(self.md.interpretation(
                "Disability rates typically increase with age, with the highest rates among "
                "individuals 65 and older due to age-related health conditions."
            ))

        lines.append("")
        return "\n".join(lines)

    def _trends(self, data: Dict) -> str:
        """Generate temporal trends section."""
        lines = [self.md.h2("Temporal Trends")]

        trends = self._safe_get(data, 'trends', default={})

        if not trends:
            return ""

        headers = ["Year", "Disability Rate"]
        rows = [[str(year), f"{rate:.2f}%"] for year, rate in sorted(trends.items())]

        if rows:
            lines.append(self.md.table(headers, rows))

        lines.append("")
        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        disability_imgs = [link for link in img_links if any(term in link.lower()
                          for term in ['disability', 'hearing', 'vision', 'cognitive',
                                       'ambulatory', 'self_care', 'independent'])]

        if disability_imgs:
            for link in disability_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No disability visualizations available._")

        return "\n".join(lines)

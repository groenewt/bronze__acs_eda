"""
Health Insurance Analysis Section - Coverage rates, insurance types, and gaps.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class HealthInsuranceSection(BaseReportSection):
    """Health insurance coverage analysis section."""

    def get_filename(self) -> str:
        return "06b_health_insurance_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Health Insurance Analysis")]

        content.append(self.md.blockquote(
            "Analysis of health insurance coverage patterns including coverage rates, "
            "insurance types, uninsured demographics, and temporal trends."
        ))
        content.append("")

        content.append(self._coverage_overview(data))
        content.append(self._insurance_types(data))
        content.append(self._uninsured_demographics(data))
        content.append(self._public_vs_private(data))
        content.append(self._trends(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _coverage_overview(self, data: Dict) -> str:
        """Generate coverage overview section."""
        lines = [self.md.h2("Coverage Overview")]

        coverage = self._safe_get(data, 'coverage', default={})

        if not coverage:
            lines.append("_No coverage data available._")
            return "\n".join(lines)

        insured_rate = coverage.get('insured_rate')
        uninsured_rate = coverage.get('uninsured_rate')
        uninsured_count = coverage.get('uninsured_count')
        total_pop = coverage.get('total_population')

        if insured_rate is not None:
            lines.append(self.md.metric("Insured Rate", insured_rate, "%", 1))
        if uninsured_rate is not None:
            lines.append(self.md.metric("Uninsured Rate", uninsured_rate, "%", 1))
        if uninsured_count is not None:
            lines.append(self.md.metric("Uninsured Population", uninsured_count, "", 0))
        if total_pop is not None:
            lines.append(self.md.metric("Total Population Analyzed", total_pop, "", 0))

        if uninsured_rate:
            if uninsured_rate > 10:
                lines.append(self.md.interpretation(
                    f"Uninsured rate of {uninsured_rate:.1f}% is concerning and above the national "
                    "average, indicating gaps in healthcare access."
                ))
            elif uninsured_rate < 5:
                lines.append(self.md.interpretation(
                    f"Uninsured rate of {uninsured_rate:.1f}% indicates strong healthcare coverage, "
                    "likely reflecting state expansion policies or strong employer coverage."
                ))

        lines.append("")
        return "\n".join(lines)

    def _insurance_types(self, data: Dict) -> str:
        """Generate insurance type breakdown."""
        lines = [self.md.h2("Insurance Type Breakdown")]

        types = self._safe_get(data, 'insurance_types', default={})

        if not types:
            lines.append("_No insurance type data available._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "ACS tracks multiple insurance types. Individuals may have more than one type of coverage."
        ))
        lines.append("")

        headers = ["Insurance Type", "Coverage Rate"]
        rows = []

        type_labels = {
            'employer': 'Employer-Sponsored',
            'direct': 'Direct Purchase',
            'medicare': 'Medicare',
            'medicaid': 'Medicaid',
            'military': 'VA/Military',
            'tricare': 'TRICARE',
            'va': 'VA Health Care',
            'ihs': 'Indian Health Service'
        }

        for key, rate in sorted(types.items(), key=lambda x: x[1], reverse=True):
            label = type_labels.get(key.lower(), key.replace('_', ' ').title())
            if rate is not None:
                rows.append([label, f"{rate:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify dominant type
            if types:
                top_type = max(types.items(), key=lambda x: x[1] if x[1] else 0)
                label = type_labels.get(top_type[0].lower(), top_type[0])
                lines.append(self.md.interpretation(
                    f"{label} is the most common source of coverage at {top_type[1]:.1f}%."
                ))

        lines.append("")
        return "\n".join(lines)

    def _uninsured_demographics(self, data: Dict) -> str:
        """Generate uninsured demographics breakdown."""
        lines = [self.md.h2("Uninsured Population Demographics")]

        demographics = self._safe_get(data, 'demographic_breakdown', default={})

        if not demographics:
            return ""

        # By age
        by_age = demographics.get('by_age', {})
        if by_age:
            lines.append(self.md.h3("By Age Group"))
            headers = ["Age Group", "Uninsured Rate"]
            rows = [[age, f"{rate:.1f}%"] for age, rate in by_age.items()]
            if rows:
                lines.append(self.md.table(headers, rows))
            lines.append("")

        # By income
        by_income = demographics.get('by_income', {})
        if by_income:
            lines.append(self.md.h3("By Income Level"))
            headers = ["Income Level", "Uninsured Rate"]
            rows = [[level, f"{rate:.1f}%"] for level, rate in by_income.items()]
            if rows:
                lines.append(self.md.table(headers, rows))
            lines.append("")

        # By employment
        by_employment = demographics.get('by_employment', {})
        if by_employment:
            lines.append(self.md.h3("By Employment Status"))
            headers = ["Employment Status", "Uninsured Rate"]
            rows = [[status, f"{rate:.1f}%"] for status, rate in by_employment.items()]
            if rows:
                lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    def _public_vs_private(self, data: Dict) -> str:
        """Generate public vs private insurance comparison."""
        lines = [self.md.h2("Public vs Private Insurance")]

        public_rate = self._safe_get(data, 'public_rate')
        private_rate = self._safe_get(data, 'private_rate')

        if public_rate is None and private_rate is None:
            return ""

        headers = ["Insurance Category", "Coverage Rate"]
        rows = []
        if public_rate is not None:
            rows.append(["Public Insurance", f"{public_rate:.1f}%"])
        if private_rate is not None:
            rows.append(["Private Insurance", f"{private_rate:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            if public_rate and private_rate:
                if public_rate > private_rate:
                    lines.append(self.md.interpretation(
                        "Public insurance covers more of the population than private insurance, "
                        "suggesting a significant role for government healthcare programs."
                    ))
                else:
                    lines.append(self.md.interpretation(
                        "Private insurance is the dominant coverage type, reflecting a strong "
                        "employer-sponsored insurance market."
                    ))

        lines.append("")
        return "\n".join(lines)

    def _trends(self, data: Dict) -> str:
        """Generate temporal trends section."""
        lines = [self.md.h2("Coverage Trends Over Time")]

        trends = self._safe_get(data, 'trends', default={})

        if not trends:
            return ""

        headers = ["Year", "Uninsured Rate"]
        rows = [[str(year), f"{rate:.1f}%"] for year, rate in sorted(trends.items())]

        if rows:
            lines.append(self.md.table(headers, rows))

            # Calculate trend direction
            years = sorted(trends.keys())
            if len(years) >= 2:
                first_rate = trends[years[0]]
                last_rate = trends[years[-1]]
                change = last_rate - first_rate
                direction = "decreased" if change < 0 else "increased"
                lines.append(self.md.interpretation(
                    f"Uninsured rate has {direction} by {abs(change):.1f} percentage points "
                    f"from {years[0]} to {years[-1]}."
                ))

        lines.append("")
        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        insurance_imgs = [link for link in img_links if any(term in link.lower()
                         for term in ['insurance', 'coverage', 'uninsured', 'health',
                                      'medicare', 'medicaid'])]

        if insurance_imgs:
            for link in insurance_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No health insurance visualizations available._")

        return "\n".join(lines)

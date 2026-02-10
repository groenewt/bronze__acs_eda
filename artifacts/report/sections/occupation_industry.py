"""
Occupation and Industry Analysis Section - Employment patterns, wage analysis, workforce composition.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class OccupationIndustrySection(BaseReportSection):
    """Occupation and industry analysis section."""

    def get_filename(self) -> str:
        return "06c_occupation_industry_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Occupation & Industry Analysis")]

        content.append(self.md.blockquote(
            "Analysis of workforce composition including top industries, occupations, "
            "wage premiums, and demographic patterns in employment."
        ))
        content.append("")

        content.append(self._top_industries(data))
        content.append(self._top_occupations(data))
        content.append(self._wage_premium(data))
        content.append(self._demographic_patterns(data))
        content.append(self._industry_trends(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _top_industries(self, data: Dict) -> str:
        """Generate top industries section."""
        lines = [self.md.h2("Top Industries by Employment")]

        industries = self._safe_get(data, 'top_industries', default={})

        if not industries:
            lines.append("_No industry data available._")
            return "\n".join(lines)

        headers = ["Industry", "Employment Share"]
        rows = []
        for industry, info in list(industries.items())[:15]:
            if isinstance(info, dict):
                pct = info.get('percentage', 0)
            else:
                pct = info
            industry_name = str(industry).replace('_', ' ')
            rows.append([industry_name, f"{pct:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify concentration
            total_top5 = sum(
                (info.get('percentage', 0) if isinstance(info, dict) else info)
                for info in list(industries.values())[:5]
            )
            if total_top5 > 50:
                lines.append(self.md.interpretation(
                    f"The top 5 industries account for {total_top5:.1f}% of employment, "
                    "indicating economic concentration in a few sectors."
                ))

        lines.append("")
        return "\n".join(lines)

    def _top_occupations(self, data: Dict) -> str:
        """Generate top occupations section."""
        lines = [self.md.h2("Top Occupations by Employment")]

        occupations = self._safe_get(data, 'top_occupations', default={})

        if not occupations:
            lines.append("_No occupation data available._")
            return "\n".join(lines)

        headers = ["Occupation", "Employment Share"]
        rows = []
        for occupation, info in list(occupations.items())[:15]:
            if isinstance(info, dict):
                pct = info.get('percentage', 0)
            else:
                pct = info
            occ_name = str(occupation).replace('_', ' ')
            rows.append([occ_name, f"{pct:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

        lines.append("")
        return "\n".join(lines)

    def _wage_premium(self, data: Dict) -> str:
        """Generate wage premium analysis."""
        lines = [self.md.h2("Industry Wage Premium/Discount")]

        wage_premium = self._safe_get(data, 'wage_premium', default={})

        if not wage_premium:
            return ""

        lines.append(self.md.blockquote(
            "Wage premium shows how median income in each industry compares to the overall median. "
            "Positive values indicate above-average wages; negative values indicate below-average."
        ))
        lines.append("")

        # Sort by premium (highest to lowest)
        sorted_premiums = sorted(wage_premium.items(), key=lambda x: x[1], reverse=True)

        headers = ["Industry", "Wage Premium/Discount"]
        rows = []
        for industry, premium in sorted_premiums[:15]:
            sign = "+" if premium > 0 else ""
            industry_name = str(industry).replace('_', ' ')
            rows.append([industry_name, f"{sign}{premium:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify extremes
            highest = sorted_premiums[0]
            lowest = sorted_premiums[-1]
            lines.append(self.md.interpretation(
                f"Highest wage premium: {highest[0]} (+{highest[1]:.1f}%). "
                f"Lowest wages: {lowest[0]} ({lowest[1]:.1f}%)."
            ))

        lines.append("")
        return "\n".join(lines)

    def _demographic_patterns(self, data: Dict) -> str:
        """Generate demographic patterns section."""
        lines = [self.md.h2("Demographic Patterns")]

        demographics = self._safe_get(data, 'demographic_patterns', default={})

        if not demographics:
            return ""

        # By sex
        by_sex = demographics.get('by_sex', {})
        if by_sex:
            lines.append(self.md.h3("Occupational Distribution by Sex"))
            headers = ["Occupation", "Male %", "Female %"]
            rows = []
            for occ, sex_data in list(by_sex.items())[:10]:
                male_pct = sex_data.get('male', 50)
                female_pct = 100 - male_pct
                rows.append([str(occ), f"{male_pct:.0f}%", f"{female_pct:.0f}%"])

            if rows:
                lines.append(self.md.table(headers, rows))
                lines.append(self.md.interpretation(
                    "Significant differences in male/female representation across occupations "
                    "indicate occupational segregation patterns."
                ))
            lines.append("")

        # By education
        by_education = demographics.get('by_education', {})
        if by_education:
            lines.append(self.md.h3("Education-Occupation Alignment"))
            headers = ["Education Level", "Top Occupation"]
            rows = [[str(edu), str(occ)] for edu, occ in list(by_education.items())[:8]]
            if rows:
                lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    def _industry_trends(self, data: Dict) -> str:
        """Generate industry trends section."""
        lines = [self.md.h2("Industry Employment Trends")]

        trends = self._safe_get(data, 'industry_trends', default={})

        if not trends:
            return ""

        headers = ["Industry", "Trend", "Change"]
        rows = []
        for industry, trend_data in list(trends.items())[:10]:
            if isinstance(trend_data, dict):
                direction = trend_data.get('direction', 'stable')
                change = trend_data.get('change', 0)
                rows.append([
                    str(industry),
                    direction.upper(),
                    f"{'+' if change > 0 else ''}{change:.1f}%"
                ])

        if rows:
            lines.append(self.md.table(headers, rows))

        lines.append("")
        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        occ_ind_imgs = [link for link in img_links if any(term in link.lower()
                       for term in ['occupation', 'industry', 'wage', 'employment',
                                    'job', 'worker', 'sector'])]

        if occ_ind_imgs:
            for link in occ_ind_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No occupation/industry visualizations available._")

        return "\n".join(lines)

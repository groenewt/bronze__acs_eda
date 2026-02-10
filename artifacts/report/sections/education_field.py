"""
Education Field Analysis Section - Field of degree patterns, STEM analysis, income relationships.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class EducationFieldSection(BaseReportSection):
    """Education field of degree analysis section."""

    def get_filename(self) -> str:
        return "06d_education_field_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Education Field Analysis")]

        content.append(self.md.blockquote(
            "Analysis of field of degree patterns including STEM representation, "
            "income by field, and demographic patterns in higher education."
        ))
        content.append("")

        content.append(self._stem_analysis(data))
        content.append(self._top_fields(data))
        content.append(self._income_by_field(data))
        content.append(self._demographic_patterns(data))
        content.append(self._field_trends(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _stem_analysis(self, data: Dict) -> str:
        """Generate STEM analysis section."""
        lines = [self.md.h2("STEM Degree Analysis")]

        stem = self._safe_get(data, 'stem_analysis', default={})

        if not stem:
            lines.append("_No STEM analysis data available._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "STEM fields include Science, Technology, Engineering, and Mathematics. "
            "STEM-related fields include health sciences and technical fields with strong STEM foundations."
        ))
        lines.append("")

        stem_rate = stem.get('stem_rate')
        stem_related_rate = stem.get('stem_related_rate')
        non_stem_rate = stem.get('non_stem_rate')
        income_premium = stem.get('income_premium')

        headers = ["Category", "Percentage"]
        rows = []
        if stem_rate is not None:
            rows.append(["STEM Fields", f"{stem_rate:.1f}%"])
        if stem_related_rate is not None:
            rows.append(["STEM-Related Fields", f"{stem_related_rate:.1f}%"])
        if non_stem_rate is not None:
            rows.append(["Non-STEM Fields", f"{non_stem_rate:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

        if income_premium is not None:
            lines.append("")
            lines.append(self.md.metric("STEM Income Premium", income_premium, "%", 1))
            if income_premium > 20:
                lines.append(self.md.interpretation(
                    f"STEM degree holders earn {income_premium:.1f}% more than non-STEM graduates, "
                    "reflecting strong labor market demand for technical skills."
                ))

        lines.append("")
        return "\n".join(lines)

    def _top_fields(self, data: Dict) -> str:
        """Generate top fields of degree section."""
        lines = [self.md.h2("Top Fields of Degree")]

        fields = self._safe_get(data, 'top_fields', default={})

        if not fields:
            lines.append("_No field of degree data available._")
            return "\n".join(lines)

        headers = ["Field of Degree", "Percentage"]
        rows = []
        for field, info in list(fields.items())[:15]:
            if isinstance(info, dict):
                pct = info.get('percentage', 0)
            else:
                pct = info
            field_name = str(field).replace('_', ' ')
            rows.append([field_name, f"{pct:.1f}%"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify dominant field
            top_field = list(fields.items())[0]
            field_name = str(top_field[0]).replace('_', ' ')
            pct = top_field[1].get('percentage', 0) if isinstance(top_field[1], dict) else top_field[1]
            lines.append(self.md.interpretation(
                f"{field_name} is the most common field of degree at {pct:.1f}%."
            ))

        lines.append("")
        return "\n".join(lines)

    def _income_by_field(self, data: Dict) -> str:
        """Generate income by field analysis."""
        lines = [self.md.h2("Income by Field of Degree")]

        income = self._safe_get(data, 'income_by_field', default={})

        if not income:
            return ""

        lines.append(self.md.blockquote(
            "Median income varies significantly by field of degree, reflecting labor market "
            "demand, industry placement, and typical career paths for graduates."
        ))
        lines.append("")

        # Sort by income (highest to lowest)
        sorted_income = sorted(income.items(), key=lambda x: x[1], reverse=True)

        headers = ["Field of Degree", "Median Income"]
        rows = []
        for field, inc in sorted_income[:15]:
            field_name = str(field).replace('_', ' ')
            rows.append([field_name, f"${inc:,.0f}"])

        if rows:
            lines.append(self.md.table(headers, rows))

            # Identify extremes
            highest = sorted_income[0]
            lowest = sorted_income[-1]
            gap = highest[1] - lowest[1]
            lines.append(self.md.interpretation(
                f"Highest earning field: {highest[0]} (${highest[1]:,.0f}). "
                f"Lowest: {lowest[0]} (${lowest[1]:,.0f}). "
                f"Gap: ${gap:,.0f}."
            ))

        lines.append("")
        return "\n".join(lines)

    def _demographic_patterns(self, data: Dict) -> str:
        """Generate demographic patterns section."""
        lines = [self.md.h2("Demographic Patterns in Education Fields")]

        demographics = self._safe_get(data, 'demographic_patterns', default={})

        if not demographics:
            return ""

        # STEM by sex
        stem_by_sex = demographics.get('stem_by_sex', {})
        if stem_by_sex:
            lines.append(self.md.h3("STEM Representation by Sex"))
            male_stem = stem_by_sex.get('male', 50)
            female_stem = stem_by_sex.get('female', 50)

            headers = ["Sex", "STEM Rate"]
            rows = [
                ["Male", f"{male_stem:.1f}%"],
                ["Female", f"{female_stem:.1f}%"]
            ]
            lines.append(self.md.table(headers, rows))

            if abs(male_stem - female_stem) > 20:
                lines.append(self.md.interpretation(
                    f"Significant gender gap in STEM fields with {abs(male_stem - female_stem):.1f} "
                    "percentage point difference between male and female representation."
                ))
            lines.append("")

        # Field by age
        by_age = demographics.get('by_age', {})
        if by_age:
            lines.append(self.md.h3("Field Distribution by Age Group"))
            headers = ["Age Group", "Top Field"]
            rows = [[str(age), str(field)] for age, field in list(by_age.items())[:6]]
            if rows:
                lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    def _field_trends(self, data: Dict) -> str:
        """Generate field trends section."""
        lines = [self.md.h2("Field of Degree Trends")]

        trends = self._safe_get(data, 'field_trends', default={})

        if not trends:
            return ""

        headers = ["Field", "Trend"]
        rows = []
        for field, trend_data in list(trends.items())[:10]:
            if isinstance(trend_data, dict):
                direction = trend_data.get('direction', 'stable')
            else:
                direction = str(trend_data)
            rows.append([str(field), direction.upper()])

        if rows:
            lines.append(self.md.table(headers, rows))
            lines.append(self.md.interpretation(
                "Trends in field selection reflect changing labor market demands and "
                "student awareness of career opportunities."
            ))

        lines.append("")
        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        edu_imgs = [link for link in img_links if any(term in link.lower()
                   for term in ['field', 'degree', 'stem', 'education', 'fod',
                                'science', 'engineering', 'major'])]

        if edu_imgs:
            for link in edu_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No education field visualizations available._")

        return "\n".join(lines)

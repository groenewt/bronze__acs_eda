"""
Economic Analysis Section - Housing costs, income, and affordability analysis.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class EconomicSection(BaseReportSection):
    """Economic analysis section with detailed housing and income metrics."""

    def get_filename(self) -> str:
        return "03_economic_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Economic Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Comprehensive analysis of housing economics including property values, "
            "rental markets, utility costs, and affordability metrics."
        ))
        content.append("")

        if 'housing' in data:
            content.append(self._housing(data['housing']))
        if 'population' in data:
            content.append(self._population(data['population']))

        content.append(self._affordability_analysis(data))
        content.append(self._cost_burden_analysis(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _housing(self, housing: Dict) -> str:
        """Generate detailed housing economics section."""
        lines = [self.md.h2("Housing Economics")]

        if not housing:
            lines.append("_No housing economics data available._")
            return "\n".join(lines)

        has_data = False

        # Property Values
        if 'property_values' in housing or any('property' in k.lower() for k in housing.keys()):
            prop_section = self._format_housing_subsection(housing, 'property_values', 'Property Values')
            if prop_section:
                lines.append(prop_section)
                has_data = True

        # Rental Market
        if 'rental_market' in housing or any('rent' in k.lower() for k in housing.keys()):
            rent_section = self._format_housing_subsection(housing, 'rental_market', 'Rental Market')
            if rent_section:
                lines.append(rent_section)
                has_data = True

        # Utility Costs
        if 'utility_costs' in housing or any('utility' in k.lower() or 'cost' in k.lower() for k in housing.keys()):
            util_section = self._format_housing_subsection(housing, 'utility_costs', 'Utility Costs')
            if util_section:
                lines.append(util_section)
                has_data = True

        # Affordability
        if 'affordability' in housing:
            afford_section = self._format_housing_subsection(housing, 'affordability', 'Affordability Metrics')
            if afford_section:
                lines.append(afford_section)
                has_data = True

        # Process all remaining sections
        for section_key, section_data in housing.items():
            if not section_data or section_key in ['property_values', 'rental_market', 'utility_costs', 'affordability']:
                continue

            section_title = section_key.replace('_', ' ').title()
            lines.append(self.md.h3(section_title))

            if isinstance(section_data, dict):
                rows = []
                for k, v in section_data.items():
                    if isinstance(v, dict):
                        if v:
                            lines.append(self.md.bullet(f"**{k}**: {len(v)} data points"))
                            has_data = True
                    elif isinstance(v, (int, float)) and v != 0:
                        if v >= 1000:
                            lines.append(self.md.metric(k, v, "$", 0))
                        else:
                            lines.append(self.md.metric(k, v, "", 2))
                        has_data = True

        if not has_data:
            lines.append("_No housing economics data available._")

        return "\n".join(lines)

    def _format_housing_subsection(self, housing: Dict, key: str, title: str) -> str:
        """Format a housing subsection with detailed metrics."""
        data = housing.get(key, {})
        if not data:
            return ""

        lines = [self.md.h3(title)]

        if isinstance(data, dict):
            # Create a metrics table if there are multiple values
            if len(data) >= 3:
                headers = ["Metric", "Value"]
                rows = []
                for k, v in data.items():
                    if isinstance(v, (int, float)) and v != 0:
                        if v >= 1000:
                            rows.append([k.replace('_', ' ').title(), f"${v:,.0f}"])
                        else:
                            rows.append([k.replace('_', ' ').title(), f"{v:,.2f}"])
                    elif isinstance(v, dict) and v:
                        rows.append([k.replace('_', ' ').title(), f"{len(v)} time periods"])
                if rows:
                    lines.append(self.md.table(headers, rows))
            else:
                for k, v in data.items():
                    if isinstance(v, (int, float)) and v != 0:
                        if v >= 1000:
                            lines.append(self.md.metric(k.replace('_', ' ').title(), v, "$", 0))
                        else:
                            lines.append(self.md.metric(k.replace('_', ' ').title(), v, "", 2))

        lines.append("")
        return "\n".join(lines)

    def _population(self, pop: Dict) -> str:
        """Generate population economics section."""
        lines = [self.md.h2("Population Economics")]

        if not pop:
            lines.append("_No population economics data available._")
            return "\n".join(lines)

        has_data = False

        for section_key, section_data in pop.items():
            if not section_data:
                continue

            section_title = section_key.replace('_', ' ').title()
            lines.append(self.md.h3(section_title))

            if isinstance(section_data, dict):
                for k, v in section_data.items():
                    if isinstance(v, dict):
                        if v:
                            lines.append(self.md.bullet(f"**{k}**: {len(v)} data points"))
                            has_data = True
                    elif isinstance(v, (int, float)) and v != 0:
                        if v >= 1000:
                            lines.append(self.md.metric(k, v, "$", 0))
                        else:
                            lines.append(self.md.metric(k, v, "", 2))
                        has_data = True
            lines.append("")

        if not has_data:
            lines.append("_No population economics data available._")

        return "\n".join(lines)

    def _affordability_analysis(self, data: Dict) -> str:
        """Generate affordability analysis section."""
        housing = data.get('housing', {})
        affordability = housing.get('affordability', {})

        if not affordability and not housing:
            return ""

        lines = [self.md.h2("Affordability Analysis")]

        # Extract affordability metrics
        rent_burden = affordability.get('rent_burden', {})
        owner_burden = affordability.get('owner_burden', {})
        income_to_value = affordability.get('income_to_value_ratio', {})

        if rent_burden:
            lines.append(self.md.h3("Rent Burden Analysis"))
            lines.append(self.md.blockquote(
                "Rent burden is calculated as gross rent as a percentage of household income. "
                "A household is considered 'cost-burdened' if spending more than 30% of income on rent."
            ))
            lines.append("")

            if isinstance(rent_burden, dict):
                headers = ["Metric", "Value"]
                rows = []
                for k, v in rent_burden.items():
                    if isinstance(v, (int, float)):
                        rows.append([k.replace('_', ' ').title(), f"{v:.1f}%"])
                if rows:
                    lines.append(self.md.table(headers, rows))
            lines.append("")

        if owner_burden:
            lines.append(self.md.h3("Owner Cost Burden"))
            lines.append(self.md.blockquote(
                "Owner costs include mortgage payments, property taxes, insurance, and utilities. "
                "Cost burden threshold is 30% of household income."
            ))
            lines.append("")

            if isinstance(owner_burden, dict):
                headers = ["Metric", "Value"]
                rows = []
                for k, v in owner_burden.items():
                    if isinstance(v, (int, float)):
                        rows.append([k.replace('_', ' ').title(), f"{v:.1f}%"])
                if rows:
                    lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines) if len(lines) > 1 else ""

    def _cost_burden_analysis(self, data: Dict) -> str:
        """Generate cost burden threshold analysis."""
        # This can pull from statistics about cost burden variables
        stats = data.get('statistics', {})
        summary = stats.get('summary_statistics', {})

        rent_pct = summary.get('Gross_Rent_Percentage_Income', {})
        owner_pct = summary.get('Owner_Costs_Percentage_Income', {})

        if not rent_pct and not owner_pct:
            return ""

        lines = [self.md.h2("Cost Burden Thresholds")]

        lines.append(self.md.h3("HUD Cost Burden Categories"))
        headers = ["Category", "Definition", "Threshold"]
        rows = [
            ["No Burden", "Affordable housing costs", "< 30% of income"],
            ["Moderate Burden", "Cost-burdened", "30-50% of income"],
            ["Severe Burden", "Severely cost-burdened", "> 50% of income"],
        ]
        lines.append(self.md.table(headers, rows))
        lines.append("")

        if rent_pct:
            mean_rent = rent_pct.get('mean', 0)
            median_rent = rent_pct.get('median', 0)
            lines.append(self.md.h3("Renter Cost Burden"))
            lines.append(self.md.metric("Average Rent-to-Income Ratio", mean_rent, "%", 1))
            lines.append(self.md.metric("Median Rent-to-Income Ratio", median_rent, "%", 1))

            if mean_rent > 30:
                lines.append(self.md.interpretation(
                    f"Average renter households are cost-burdened (spending {mean_rent:.1f}% of income on rent)."
                ))
            lines.append("")

        if owner_pct:
            mean_owner = owner_pct.get('mean', 0)
            median_owner = owner_pct.get('median', 0)
            lines.append(self.md.h3("Owner Cost Burden"))
            lines.append(self.md.metric("Average Owner-Cost-to-Income Ratio", mean_owner, "%", 1))
            lines.append(self.md.metric("Median Owner-Cost-to-Income Ratio", median_owner, "%", 1))
            lines.append("")

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        econ_imgs = [link for link in img_links if any(term in link.lower()
                    for term in ['economic', 'income', 'property', 'rent', 'wage',
                                'cost', 'burden', 'affordability', 'utility'])]

        if econ_imgs:
            for link in econ_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No economic visualizations available._")

        return "\n".join(lines)

"""
Cross-Variable Analysis Section - Variable interactions and derived ratios.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class CrossVariableSection(BaseReportSection):
    """Cross-variable analysis section with interaction analysis."""

    def get_filename(self) -> str:
        return "06_cross_variable_analysis.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Cross-Variable Analysis")]

        # Add section description
        content.append(self.md.blockquote(
            "Analysis of relationships and interactions between multiple variables, "
            "including derived ratios and multi-way interactions."
        ))
        content.append("")

        content.append(self._interactions(data))
        content.append(self._ratios(data))
        content.append(self._conditional_analysis(data))
        content.append(self._visualizations())

        return "\n".join(filter(None, content))

    def _interactions(self, data: Dict) -> str:
        """Generate variable interactions section."""
        interactions = data.get('interactions', {})
        lines = [self.md.h2("Variable Interactions")]

        if not interactions:
            lines.append("_No interaction analysis available._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "Interactions capture how the relationship between two variables "
            "changes across different values of a third variable."
        ))
        lines.append("")

        headers = ["Interaction Group", "Variables", "Correlation", "Strength"]
        rows = []

        for group, analysis in list(interactions.items())[:15]:
            if isinstance(analysis, dict):
                corr = analysis.get('correlation', 0)
                vars_involved = analysis.get('variables', [group])

                # Determine strength
                abs_corr = abs(corr)
                if abs_corr >= 0.7:
                    strength = "Strong"
                elif abs_corr >= 0.4:
                    strength = "Moderate"
                elif abs_corr >= 0.2:
                    strength = "Weak"
                else:
                    strength = "Negligible"

                vars_str = ", ".join(vars_involved) if isinstance(vars_involved, list) else group
                rows.append([group, vars_str, f"{corr:.3f}", strength])

        if rows:
            lines.append(self.md.table(headers, rows))
        else:
            for group, analysis in list(interactions.items())[:10]:
                corr = analysis.get('correlation', 0) if isinstance(analysis, dict) else 0
                lines.append(self.md.bullet(f"**{group}**: correlation = {corr:.3f}"))

        return "\n".join(lines)

    def _ratios(self, data: Dict) -> str:
        """Generate key ratios section."""
        ratios = data.get('ratios', {})
        lines = [self.md.h2("Key Ratios")]

        if not ratios:
            lines.append("_No ratio analysis available._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "Derived ratios that capture important relationships between variables "
            "and enable standardized comparisons."
        ))
        lines.append("")

        headers = ["Ratio", "Mean", "Median", "Std Dev", "Interpretation"]
        rows = []

        # Ratio interpretations
        ratio_interp = {
            'rent_to_income': 'Housing affordability for renters',
            'owner_cost_to_income': 'Housing affordability for owners',
            'rent_to_value': 'Rental yield / investment return',
            'utility_to_income': 'Utility cost burden',
            'property_tax_rate': 'Effective tax burden',
        }

        for ratio_name, stats in list(ratios.items())[:15]:
            if isinstance(stats, dict):
                mean = stats.get('mean', 0)
                median = stats.get('median', None)
                std = stats.get('std', stats.get('std_dev', None))

                mean_str = f"{mean:.4f}"
                median_str = f"{median:.4f}" if median is not None else "—"
                std_str = f"{std:.4f}" if std is not None else "—"

                # Find interpretation
                interp = "—"
                for key, desc in ratio_interp.items():
                    if key in ratio_name.lower():
                        interp = desc
                        break

                rows.append([ratio_name, mean_str, median_str, std_str, interp])

        if rows:
            lines.append(self.md.table(headers, rows))
        else:
            for ratio_name, stats in list(ratios.items())[:10]:
                mean = stats.get('mean', 0) if isinstance(stats, dict) else 0
                lines.append(self.md.bullet(f"**{ratio_name}**: mean = {mean:.4f}"))

        return "\n".join(lines)

    def _conditional_analysis(self, data: Dict) -> str:
        """Generate conditional/segmented analysis."""
        conditional = data.get('conditional_analysis', data.get('segmented_analysis', {}))

        if not conditional:
            return ""

        lines = [self.md.h2("Conditional Analysis")]

        lines.append(self.md.blockquote(
            "Analysis of variable relationships conditioned on specific groups or segments."
        ))
        lines.append("")

        for segment, analysis in list(conditional.items())[:5]:
            lines.append(self.md.h3(segment.replace('_', ' ').title()))

            if isinstance(analysis, dict):
                headers = ["Variable", "Value", "Condition"]
                rows = []
                for var, val in analysis.items():
                    if isinstance(val, (int, float)):
                        rows.append([var, f"{val:.4f}", segment])
                if rows:
                    lines.append(self.md.table(headers, rows))
            lines.append("")

        return "\n".join(lines)

    def _visualizations(self) -> str:
        """Generate visualizations section."""
        lines = [self.md.h2("Visualizations")]

        img_links = self._link_images("")
        cross_imgs = [link for link in img_links if any(term in link.lower()
                     for term in ['interaction', 'ratio', 'pairwise', 'cross', 'three_way'])]

        if cross_imgs:
            for link in cross_imgs:
                lines.append(link)
                lines.append("")
        else:
            lines.append("_No cross-variable visualizations available._")

        return "\n".join(lines)

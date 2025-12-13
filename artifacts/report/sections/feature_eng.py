"""
Feature Engineering Section - Derived features and transformations.
"""

from typing import Dict, List, Any

from report.base import BaseReportSection


class FeatureEngineeringSection(BaseReportSection):
    """Feature engineering section with detailed feature documentation."""

    def get_filename(self) -> str:
        return "10_feature_engineering.md"

    def generate(self, data: Dict) -> str:
        content = [self.md.h1("Feature Engineering")]

        # Add section description
        content.append(self.md.blockquote(
            "Documentation of derived features, transformations, and data preprocessing "
            "steps applied to prepare the dataset for analysis and modeling."
        ))
        content.append("")

        content.append(self._feature_summary(data))
        content.append(self._created_features(data))
        content.append(self._transformations(data))
        content.append(self._feature_statistics(data))
        content.append(self._data_cleaning(data))

        return "\n".join(filter(None, content))

    def _feature_summary(self, data: Dict) -> str:
        """Generate summary statistics for feature engineering."""
        features = data.get('features_created', [])
        transforms = data.get('transformations', [])
        cleaning = data.get('cleaning', {})

        lines = [self.md.h2("Summary")]

        headers = ["Metric", "Value", "Description"]
        rows = [
            ["Features Created", str(len(features)), "New derived variables"],
            ["Transformations Applied", str(len(transforms)), "Data transformations"],
        ]

        if cleaning:
            rows_before = cleaning.get('rows_before', 0)
            rows_after = cleaning.get('rows_after', 0)
            if rows_before > 0:
                retention = (rows_after / rows_before) * 100
                rows.append(["Rows Before Cleaning", f"{rows_before:,}", "Original dataset size"])
                rows.append(["Rows After Cleaning", f"{rows_after:,}", "Final dataset size"])
                rows.append(["Data Retention", f"{retention:.1f}%", "Percentage of data retained"])

        final_shape = data.get('final_shape')
        if final_shape:
            rows.append(["Final Rows", f"{final_shape[0]:,}", "Observations"])
            rows.append(["Final Columns", str(final_shape[1]), "Total variables"])

        lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _created_features(self, data: Dict) -> str:
        """Generate detailed created features section."""
        features = data.get('features_created', [])
        feature_details = data.get('feature_details', {})

        lines = [self.md.h2("Created Features")]

        if not features:
            lines.append("_No derived features were created._")
            return "\n".join(lines)

        lines.append(self.md.blockquote(
            "New variables derived from existing data to capture additional patterns "
            "and relationships."
        ))
        lines.append("")

        # Feature documentation with descriptions
        feature_docs = {
            'Property_Value_is_zero': {
                'description': 'Binary flag indicating zero or missing property value',
                'formula': '1 if Property_Value == 0 else 0',
                'purpose': 'Identify records without valid property valuations'
            },
            'Gross_Rent_is_zero': {
                'description': 'Binary flag indicating zero or missing gross rent',
                'formula': '1 if Gross_Rent == 0 else 0',
                'purpose': 'Identify non-rental or owner-occupied units'
            },
            'Annual_Rent_to_Value_Ratio': {
                'description': 'Ratio of annual rent to property value',
                'formula': '(Gross_Rent × 12) / Property_Value',
                'purpose': 'Assess rental yield and investment potential'
            },
            'Total_Monthly_Utility_Cost': {
                'description': 'Sum of all monthly utility expenses',
                'formula': 'Electricity + Gas + Fuel + Water/12',
                'purpose': 'Aggregate utility burden metric'
            },
            'Property_Tax_Rate': {
                'description': 'Effective property tax rate',
                'formula': 'Property_Taxes_Yearly / Property_Value',
                'purpose': 'Normalized tax burden comparison'
            },
            'Years_Since_Start': {
                'description': 'Years elapsed since first year in dataset',
                'formula': 'Year - min(Year)',
                'purpose': 'Temporal index for trend analysis'
            },
            'Decade': {
                'description': 'Decade grouping of the year',
                'formula': '(Year // 10) × 10',
                'purpose': 'Decadal trend analysis'
            }
        }

        for feat in features:
            lines.append(self.md.h3(feat))

            doc = feature_docs.get(feat, feature_details.get(feat, {}))

            if isinstance(doc, dict) and doc:
                headers = ["Property", "Value"]
                rows = [
                    ["Description", doc.get('description', 'Derived feature')],
                    ["Formula", f"`{doc.get('formula', 'N/A')}`"],
                    ["Purpose", doc.get('purpose', '—')],
                ]
                lines.append(self.md.table(headers, rows))
            else:
                lines.append(self.md.bullet(f"**Type**: Derived feature"))
                lines.append(self.md.bullet(f"**Description**: Engineering feature for analysis"))

            lines.append("")

        return "\n".join(lines)

    def _transformations(self, data: Dict) -> str:
        """Generate detailed transformations section."""
        transforms = data.get('transformations', [])
        transform_details = data.get('transformation_details', {})

        lines = [self.md.h2("Applied Transformations")]

        if not transforms:
            lines.append("_No transformations were applied._")
            return "\n".join(lines)

        # Transformation documentation
        transform_docs = {
            'Flagged zeros in 2 economic columns': {
                'description': 'Created binary flags for zero values in economic variables',
                'columns': 'Property_Value, Gross_Rent',
                'purpose': 'Handle missing/invalid economic data',
                'method': 'Binary encoding (0/1)'
            },
            'Housing cost ratios calculated': {
                'description': 'Computed derived ratios for housing affordability analysis',
                'columns': 'Annual_Rent_to_Value_Ratio, Property_Tax_Rate',
                'purpose': 'Normalize costs for comparison',
                'method': 'Division with zero-handling'
            },
            'Temporal features extracted from year': {
                'description': 'Extracted temporal components for trend analysis',
                'columns': 'Years_Since_Start, Decade',
                'purpose': 'Enable temporal modeling',
                'method': 'Arithmetic transformation'
            }
        }

        for trans in transforms:
            doc = transform_docs.get(trans, transform_details.get(trans, {}))

            if isinstance(doc, dict) and doc:
                lines.append(self.md.h3(trans))

                headers = ["Property", "Value"]
                rows = [
                    ["Description", doc.get('description', trans)],
                    ["Columns Affected", doc.get('columns', '—')],
                    ["Purpose", doc.get('purpose', '—')],
                    ["Method", doc.get('method', '—')],
                ]
                lines.append(self.md.table(headers, rows))
            else:
                lines.append(self.md.bullet(f"**{trans}**"))

            lines.append("")

        return "\n".join(lines)

    def _feature_statistics(self, data: Dict) -> str:
        """Generate statistics for created features."""
        features = data.get('features_created', [])
        feature_stats = data.get('feature_statistics', {})

        if not feature_stats:
            return ""

        lines = [self.md.h2("Feature Statistics")]

        headers = ["Feature", "Mean", "Std Dev", "Min", "Max", "Non-Zero %"]
        rows = []

        for feat in features:
            stats = feature_stats.get(feat, {})
            if isinstance(stats, dict):
                mean = stats.get('mean', None)
                std = stats.get('std', None)
                min_val = stats.get('min', None)
                max_val = stats.get('max', None)
                non_zero = stats.get('non_zero_pct', None)

                mean_str = f"{mean:.4f}" if mean is not None else "—"
                std_str = f"{std:.4f}" if std is not None else "—"
                min_str = f"{min_val:.4f}" if min_val is not None else "—"
                max_str = f"{max_val:.4f}" if max_val is not None else "—"
                nz_str = f"{non_zero:.1f}%" if non_zero is not None else "—"

                rows.append([feat, mean_str, std_str, min_str, max_str, nz_str])

        if rows:
            lines.append(self.md.table(headers, rows))

        return "\n".join(lines)

    def _data_cleaning(self, data: Dict) -> str:
        """Generate data cleaning documentation."""
        cleaning = data.get('cleaning', {})

        if not cleaning:
            return ""

        lines = [self.md.h2("Data Cleaning")]

        # Document cleaning steps
        steps = cleaning.get('steps', [])
        if steps:
            lines.append(self.md.h3("Cleaning Steps Applied"))
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        # Missing value handling
        missing_handling = cleaning.get('missing_handling', {})
        if missing_handling:
            lines.append(self.md.h3("Missing Value Treatment"))

            headers = ["Column", "Method", "Values Affected"]
            rows = []
            for col, treatment in list(missing_handling.items())[:15]:
                if isinstance(treatment, dict):
                    method = treatment.get('method', '—')
                    affected = treatment.get('count', 0)
                    rows.append([col, method, f"{affected:,}"])
            if rows:
                lines.append(self.md.table(headers, rows))

        # Summary
        rows_before = cleaning.get('rows_before', 0)
        rows_after = cleaning.get('rows_after', 0)
        if rows_before > 0 and rows_after > 0:
            removed = rows_before - rows_after
            lines.append("")
            lines.append(self.md.h3("Cleaning Summary"))
            lines.append(self.md.metric("Records Removed", removed))
            lines.append(self.md.percentage("Removal Rate", (removed / rows_before) * 100))

        return "\n".join(lines)

from typing import Dict, List, Tuple, Set
from abc import ABC, abstractmethod


# Era constants
ERA_2007_2011 = '2007-2011'
ERA_2012_2016 = '2012-2016'
ERA_2017_2022 = '2017-2022'
ERA_2023_PLUS = '2023+'

# Era detection indicators
ERA_INDICATORS = {
    ERA_2023_PLUS: {'required': {'ACCESSINET', 'TYPEHUGQ', 'YRBLT'}, 'forbidden': {'ACCESS', 'TYPE', 'YBL'}},
    ERA_2017_2022: {'required': {'ACCESS', 'BROADBND'}, 'forbidden': {'ACCESSINET'}},
    ERA_2012_2016: {'required': {'BDSP', 'ADJHSG'}, 'forbidden': {'ACCESS', 'BROADBND'}},
    ERA_2007_2011: {'required': {'BDS'}, 'forbidden': {'BDSP', 'ADJHSG'}},
}


class SchemaDefinition(ABC):
    """Abstract base for schema definitions"""

    @abstractmethod
    def get_core_columns(self) -> List[Tuple[str, str, str]]:
        """Returns list of (standardized_column_name, dtype, friendly_alias)"""
        pass

    @abstractmethod
    def get_optional_columns(self) -> List[Tuple[str, str, str]]:
        """Returns list of (standardized_column_name, dtype, friendly_alias)"""
        pass

    @abstractmethod
    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Returns mapping from raw column names to standardized names"""
        pass

    def get_all_columns(self) -> List[Tuple[str, str, str]]:
        """Returns all columns (core + optional)"""
        return self.get_core_columns() + self.get_optional_columns()

    def get_dtype_map(self) -> Dict[str, str]:
        """Returns mapping of standardized column names to data types"""
        return {col[0]: col[1] for col in self.get_all_columns()}

    def get_alias_map(self) -> Dict[str, str]:
        """Returns mapping of standardized column names to friendly aliases"""
        return {col[0]: col[2] for col in self.get_all_columns()}

    def get_zero_exclusion_map(self) -> Dict[str, bool]:
        """Returns mapping indicating which columns should exclude zeros (default: False)"""
        # By default, NO columns exclude zeros
        # Subclasses can override to specify exceptions
        return {col[0]: False for col in self.get_all_columns()}

    def should_exclude_zeros(self, column_name: str) -> bool:
        """Check if a specific column should exclude zero values"""
        return self.get_zero_exclusion_map().get(column_name, False)

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """
        Return which columns are available for a given data year.
        Subclasses should override for survey-specific year-based differences.
        """
        return {col[0]: True for col in self.get_all_columns()}

    def detect_era_from_columns(self, columns: Set[str]) -> str:
        """
        Detect which era (2007-2011, 2012-2016, 2017-2022, 2023+) based on column presence.

        Args:
            columns: Set of column names from the dataset

        Returns:
            Era string (ERA_2007_2011, ERA_2012_2016, ERA_2017_2022, or ERA_2023_PLUS)
        """
        # Normalize to uppercase for comparison
        columns_upper = {col.upper() for col in columns}

        # Check eras from newest to oldest
        for era in [ERA_2023_PLUS, ERA_2017_2022, ERA_2012_2016, ERA_2007_2011]:
            indicators = ERA_INDICATORS[era]
            required = indicators['required']
            forbidden = indicators['forbidden']

            # Check if all required columns are present
            has_required = required.issubset(columns_upper)
            # Check if none of the forbidden columns are present
            has_no_forbidden = forbidden.isdisjoint(columns_upper)

            if has_required and has_no_forbidden:
                return era

        # Default to oldest era if no match
        return ERA_2007_2011

    def get_deprecated_columns(self) -> Dict[str, Tuple[int, int]]:
        """
        Return dict of column -> (start_year, end_year) for deprecated columns.

        Returns:
            Dict mapping column name to (start_year, end_year) tuple
        """
        return {
            # Business columns (deprecated after 2016)
            'BUS': (2007, 2016),

            # Technology columns (2017-2022 only)
            'SSMC': (2017, 2022),
            'ACCESS': (2017, 2022),
            'BROADBND': (2017, 2022),

            # Old naming conventions (2007-2011)
            'BDS': (2007, 2011),
            'RMS': (2007, 2011),
            'VAL': (2007, 2011),
            'YBL': (2007, 2011),
            'TYPE': (2007, 2011),

            # Weight columns (lowercase versions deprecated after 2011)
            'wgtp1': (2007, 2011),
            'wgtp2': (2007, 2011),
            'wgtp3': (2007, 2011),
            'wgtp4': (2007, 2011),
            'wgtp5': (2007, 2011),
        }

    def get_renamed_columns(self) -> Dict[str, Dict]:
        """
        Return dict of old_name -> {'new_name': str, 'from_year': int, 'to_year': int}.

        Returns:
            Dict mapping old column names to their new names and year ranges
        """
        return {
            # 2017-2022 -> 2023+ renames
            'ACCESS': {'new_name': 'ACCESSINET', 'from_year': 2017, 'to_year': 2022},
            'TYPE': {'new_name': 'TYPEHUGQ', 'from_year': 2007, 'to_year': 2022},
            'YBL': {'new_name': 'YRBLT', 'from_year': 2007, 'to_year': 2022},

            # 2007-2011 -> 2012+ renames
            'BDS': {'new_name': 'BDSP', 'from_year': 2007, 'to_year': 2011},
            'RMS': {'new_name': 'RMSP', 'from_year': 2007, 'to_year': 2011},
            'VAL': {'new_name': 'VALP', 'from_year': 2007, 'to_year': 2011},

            # Weight columns (lowercase -> uppercase)
            'wgtp1': {'new_name': 'WGTP1', 'from_year': 2007, 'to_year': 2011},
            'wgtp2': {'new_name': 'WGTP2', 'from_year': 2007, 'to_year': 2011},
            'wgtp3': {'new_name': 'WGTP3', 'from_year': 2007, 'to_year': 2011},
            'wgtp4': {'new_name': 'WGTP4', 'from_year': 2007, 'to_year': 2011},
            'wgtp5': {'new_name': 'WGTP5', 'from_year': 2007, 'to_year': 2011},
        }

    def validate_columns_for_year(self, columns: List[str], year: int) -> Dict[str, str]:
        """
        Check if columns are valid for given year.

        Args:
            columns: List of column names to validate
            year: Year to validate against

        Returns:
            Dict of invalid_column -> reason
        """
        invalid = {}
        deprecated = self.get_deprecated_columns()
        renamed = self.get_renamed_columns()

        for col in columns:
            col_upper = col.upper()

            # Check if column is deprecated
            if col_upper in deprecated:
                start_year, end_year = deprecated[col_upper]
                if year < start_year:
                    invalid[col] = f"Column '{col}' not available until {start_year}"
                elif year > end_year:
                    invalid[col] = f"Column '{col}' deprecated after {end_year}"

            # Check if column was renamed
            if col_upper in renamed:
                rename_info = renamed[col_upper]
                from_year = rename_info['from_year']
                to_year = rename_info['to_year']
                new_name = rename_info['new_name']

                if from_year <= year <= to_year:
                    # Column is valid in this range (old name)
                    pass
                elif year > to_year:
                    invalid[col] = f"Column '{col}' renamed to '{new_name}' after {to_year}"

        return invalid

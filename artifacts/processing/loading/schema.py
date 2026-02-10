import pandas as pd
from typing import Dict
from schema import (SchemaDefinition,
                    Population1Year, Population5Year, Housing1Year, Housing5Year)
from exceptions import UnsupportedSurveyTypeError


class SchemaFactory:
    """Factory for schema instantiation"""

    @staticmethod
    def create(survey_type: str, scope: str = '1-Year') -> SchemaDefinition:
        # Case-insensitive normalization: remove hyphens and 'year'/'Year', then strip
        scope_normalized = scope.replace('-', '').lower().replace('year', '').strip()
        schemas = {
            ('population', '1'): Population1Year,
            ('population', '5'): Population5Year,
            ('housing', '1'): Housing1Year,
            ('housing', '5'): Housing5Year
        }
        key = (survey_type.lower(), scope_normalized)
        schema_class = schemas.get(key)
        if not schema_class:
            raise UnsupportedSurveyTypeError(survey_type, list(set(k[0] for k in schemas.keys())))
        return schema_class()


class SchemaApplier:
    """Applies schema to raw data"""

    def __init__(self, schema: SchemaDefinition):
        self.schema = schema
        self.stats = {'found': 0, 'missing': 0}

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_map = self._build_column_map(df)
        raw_to_std = self.schema.get_raw_to_standard_mapping()
        result = pd.DataFrame()

        for std_name, dtype, alias in self.schema.get_all_columns():
            # Find raw column name from mapping, or use std_name if not in mapping
            raw_name = None
            for raw, std in raw_to_std.items():
                if std == std_name:
                    raw_name = raw
                    break
            if raw_name is None:
                raw_name = std_name

            result[alias] = self._process_column(df, cols_map, raw_name, dtype)

        return result

    def _build_column_map(self, df: pd.DataFrame) -> Dict[str, str]:
        return {col.upper(): col for col in df.columns}

    def _process_column(self, df: pd.DataFrame, cols_map: Dict,
                        raw_name: str, dtype: str) -> pd.Series:
        col_upper = raw_name.upper()

        if col_upper in cols_map:
            self.stats['found'] += 1
            return self._cast_column(df[cols_map[col_upper]], dtype)
        else:
            self.stats['missing'] += 1
            return pd.Series([pd.NA] * len(df), index=df.index)

    def _cast_column(self, series: pd.Series, dtype: str) -> pd.Series:
        """Cast column to specified dtype with robust error handling"""
        try:
            dtype_lower = dtype.lower() if dtype else ''
            if 'int' in dtype_lower or 'bigint' in dtype_lower:
                numeric_series = pd.to_numeric(series, errors='coerce')
                return numeric_series.astype('Int64')
            elif 'float' in dtype_lower or 'decimal' in dtype_lower:
                return pd.to_numeric(series, errors='coerce').astype('float64')
            else:
                return series.astype(str)
        except Exception as e:
            dtype_lower = dtype.lower() if dtype else ''
            if 'int' in dtype_lower or 'float' in dtype_lower or 'decimal' in dtype_lower:
                return pd.to_numeric(series, errors='coerce')
            return series

import pandas as pd
import glob
import os
import re
from typing import List, Optional
from config import Config, ProcessingStats, SurveyMetadata
from exceptions import EmptyDataError
from logging_config import get_logger

logger = get_logger("processing.loader")


class FileLoader:
    """Handles CSV file loading with era-specific schema application"""

    def __init__(self, config: Config):
        self.config = config
        self.stats = ProcessingStats()

    def load(self, survey_type: str, scope: str) -> pd.DataFrame:
        """Load and combine CSV files, applying era-specific schema to each file."""
        logger.verbose(f"Searching for {survey_type} files with scope {scope}...")
        files = self._find_files(survey_type, scope)
        logger.verbose(f"Found {len(files)} file(s) to load")

        dfs = []
        for idx, f in enumerate(files, 1):
            logger.verbose(f"Loading file {idx}/{len(files)}: {os.path.basename(f)}")
            df = self._load_file(f, survey_type)
            if df is not None:
                dfs.append(df)
                logger.verbose(f"  -> Loaded {len(df):,} rows, {len(df.columns)} columns")

        logger.verbose(f"Successfully loaded {len(dfs)} dataframe(s)")
        if not dfs:
            raise EmptyDataError(f"{survey_type} ({scope})")

        combined_df = pd.concat(dfs, ignore_index=True)
        if len(combined_df) == 0:
            raise EmptyDataError(f"{survey_type} ({scope})")
        logger.verbose(f"Combined into {len(combined_df):,} total rows, {len(combined_df.columns)} columns")

        # Update stats with combined data info
        self.stats.total_rows = len(combined_df)
        self.stats.columns_found = len(combined_df.columns)

        return combined_df

    def _find_files(self, survey_type: str, scope: str) -> List[str]:
        # Normalize scope for file path: ensure capital Y in "Year"
        if 'year' in scope.lower() and 'Year' not in scope:
            scope = scope.replace('year', 'Year')
        pattern = f"{self.config.folder_base}/{survey_type}/{scope}/{self.config.state_fips}/*/*.csv"
        logger.verbose(f"Pattern: {pattern}")
        files = glob.glob(pattern)
        self.stats.files_found = len(files)
        return files

    def _load_file(self, path: str, survey_type: str) -> Optional[pd.DataFrame]:
        """Load single CSV file and apply era-specific schema."""
        df = pd.read_csv(path, low_memory=False)
        meta = self._extract_metadata(path)
        df = self._add_metadata(df, meta)

        # Apply era-specific schema
        if meta and meta.year:
            from schema import get_schema
            from .schema import SchemaApplier
            schema = get_schema(survey_type, meta.year, meta.survey_scope)
            applier = SchemaApplier(schema)
            df = applier.apply(df)
            logger.verbose(f"  Applied {meta.year} era schema ({schema.__class__.__name__})")

        return df

    def _extract_metadata(self, path: str) -> Optional[SurveyMetadata]:
        pattern = r"/acs/([^/]+)/([^/]+)/(\d{2})/(\d{4})/"
        match = re.search(pattern, path)
        if not match:
            return None
        survey_type = match.group(1)
        survey_scope = match.group(2)
        state_fips = str(match.group(3))
        year = int(match.group(4))
        return SurveyMetadata(survey_type, survey_scope, state_fips, year)

    def _add_metadata(self, df: pd.DataFrame, meta: Optional[SurveyMetadata]) -> pd.DataFrame:
        """Add metadata columns with proper type handling"""
        if meta is None:
            df['year'] = pd.NA
            df['survey_type'] = pd.NA
            df['survey_scope'] = pd.NA
            df['state_fips'] = pd.NA
        else:
            df['year'] = pd.Series([meta.year] * len(df), dtype='Int64')
            df['survey_type'] = meta.survey_type
            df['survey_scope'] = meta.survey_scope
            df['state_fips'] = str(meta.state_fips)

        self.stats.files_loaded += 1
        return df

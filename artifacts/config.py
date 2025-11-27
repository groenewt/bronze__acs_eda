from dataclasses import dataclass, field
from typing import Dict, Optional
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# FIPS MAPPING (States + Territories)
# ============================================================================

FIPS_MAP: Dict[str, str] = {
    "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas",
    "06": "California", "08": "Colorado", "09": "Connecticut", "10": "Delaware",
    "11": "District of Columbia", "12": "Florida", "13": "Georgia", "15": "Hawaii",
    "16": "Idaho", "17": "Illinois", "18": "Indiana", "19": "Iowa",
    "20": "Kansas", "21": "Kentucky", "22": "Louisiana", "23": "Maine",
    "24": "Maryland", "25": "Massachusetts", "26": "Michigan", "27": "Minnesota",
    "28": "Mississippi", "29": "Missouri", "30": "Montana", "31": "Nebraska",
    "32": "Nevada", "33": "New Hampshire", "34": "New Jersey", "35": "New Mexico",
    "36": "New York", "37": "North Carolina", "38": "North Dakota", "39": "Ohio",
    "40": "Oklahoma", "41": "Oregon", "42": "Pennsylvania", "44": "Rhode Island",
    "45": "South Carolina", "46": "South Dakota", "47": "Tennessee", "48": "Texas",
    "49": "Utah", "50": "Vermont", "51": "Virginia", "53": "Washington",
    "54": "West Virginia", "55": "Wisconsin", "56": "Wyoming",
    # Territories
    "72": "Puerto Rico"
    # "60": "American Samoa", "66": "Guam", "69": "Northern Mariana Islands", "78": "U.S. Virgin Islands"
}


# ============================================================================
# CONFIGURATION & DATA CLASSES
# ============================================================================

@dataclass
class Config:
    """Centralized configuration"""
    folder_base: str = "/data/temp/census/raw/acs"
    state_fips: str = "20"  # Default Kansas, can be overridden
    llm_url: str = "http://localhost:1234"
    llm_model: str = "local-model"
    llm_temp: float = 0.7
    llm_max_tokens: int = 24000  # High limit for comprehensive responses
    output_dir: str = "./output"
    figure_dir: str = "./output/figures"
    figure_dpi: int = 150
    survey_type: str = ""
    survey_scope: str = ""
    target_cells: int= 10_000_000     # HOUSING: Sample df before ML/DL to prevent memory explosion
    def set_state(self, state_fips: str):
        """Update state FIPS code and output directories"""
        if state_fips not in FIPS_MAP:
            raise ValueError(f"Invalid FIPS code: {state_fips}")
        self.state_fips = state_fips
        state_name = FIPS_MAP[state_fips].replace(" ", "_")
        self.output_dir = f"./output/{state_name}"
        self.figure_dir = f"{self.output_dir}/figures"
        return self
    
    def set_survey(self, survey_type: str, survey_scope: str):
        """Update survey parameters and reorganize output paths"""
        self.survey_type = survey_type
        self.survey_scope = survey_scope
        state_name = FIPS_MAP[self.state_fips].replace(" ", "_")
        self.output_dir = f"./output/{state_name}/{survey_type}/{survey_scope}"
        self.figure_dir = f"{self.output_dir}/figures"
        return self

    def get_state_name(self) -> str:
        """Return the full state name for the current FIPS code"""
        return FIPS_MAP.get(self.state_fips, "Unknown")

    def list_all_states(self) -> Dict[str, str]:
        """Return all FIPS codes and their corresponding states"""
        return FIPS_MAP


@dataclass
class SurveyMetadata:
    """Survey metadata container"""
    survey_type: str
    survey_scope: str
    state_fips: str
    year: int


@dataclass
class ProcessingStats:
    """Statistics tracker"""
    files_found: int = 0
    files_loaded: int = 0
    files_failed: int = 0
    total_rows: int = 0
    columns_found: int = 0
    columns_missing: int = 0

    def summarize(self) -> str:
        """Generate human-readable summary of stats"""
        return (
            f"Files Found: {self.files_found}, Loaded: {self.files_loaded}, Failed: {self.files_failed}\n"
            f"Rows Processed: {self.total_rows}, Columns Found: {self.columns_found}, Missing: {self.columns_missing}"
        )

"""
Column validation utilities for Census ACS data.

Provides centralized validation of column names and availability across
survey types and data years. Used by deep_learning.py, feature_engineering.py,
and processing.py to ensure column references align with actual CSV data.
"""

from typing import Dict, List, Set, Optional
import pandas as pd


class ColumnValidator:
    """Validates column availability and mappings for Census ACS data."""

    # Master list of standardized column names by survey type
    # Verified against actual CSV data (2012-2023)

    POPULATION_COLUMNS: Set[str] = {
        # Core metadata
        'Census_Year', 'State_FIPS', 'Survey_Type', 'Survey_Scope',
        'Record_Type', 'Serial_Number', 'Person_Number',
        'Public_Use_Microdata_Area', 'State_Code',
        'Income_Adjustment_Factor', 'Person_Weight',

        # Demographics
        'Age', 'Sex', 'Educational_Attainment', 'Marital_Status',
        'Citizenship_Status', 'Class_of_Worker', 'English_Speaking_Ability',
        'Fertility_Status', 'Mobility_Status', 'Military_Service',

        # Work and travel
        'Travel_Time_To_Work_Minutes', 'Vehicle_Occupancy', 'Transportation_To_Work',
        'Hours_Worked_Per_Week', 'Weeks_Worked_Past_Year', 'When_Last_Worked',

        # Income sources
        'Wage_Income', 'Total_Person_Earnings', 'Total_Person_Income',
        'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
        'Retirement_Income', 'Social_Security_Income',
        'Supplemental_Security_Income', 'Public_Assistance_Income', 'Other_Income',

        # Recodes and demographics
        'Employment_Status_Recode', 'Hispanic_Origin', 'Race_Recode',
        'Nativity', 'Poverty_Status', 'Place_Of_Birth', 'Ancestry_Recode',

        # Race detail
        'Race_American_Indian_Alaska_Native', 'Race_Asian', 'Race_Black',
        'Race_Native_Hawaiian_Pacific_Islander', 'Race_Some_Other', 'Race_White',
    }

    HOUSING_COLUMNS: Set[str] = {
        # Core metadata
        'Census_Year', 'State_FIPS', 'Survey_Type', 'Survey_Scope',
        'Serial_Number', 'Census_Division', 'Public_Use_Microdata_Area',
        'Census_Region', 'State_Code',
        'Housing_Adjustment_Factor', 'Income_Adjustment_Factor', 'Housing_Unit_Weight',

        # Physical characteristics
        'Number_of_Persons', 'Housing_Unit_Type', 'Number_of_Bedrooms',
        'Number_of_Rooms', 'Building_Type', 'Year_Structure_Built',

        # Amenities
        'Bathtub_or_Shower', 'Refrigerator', 'Hot_and_Cold_Running_Water',
        'Sink_with_Faucet', 'Stove_or_Range', 'Telephone_Service',

        # Unit status
        'Lot_Acreage', 'Agricultural_Sales', 'Business_On_Property',
        'Tenure', 'Vacancy_Status', 'Property_Value', 'Vehicles_Available',

        # Costs
        'Condo_Fee_Monthly', 'Electricity_Cost_Monthly', 'Fuel_Cost_Monthly',
        'Gas_Cost_Monthly', 'House_Heating_Fuel', 'Insurance_Cost_Yearly',
        'Water_Cost_Yearly', 'Mobile_Home_Costs_Monthly',
        'First_Mortgage_Payment_Monthly', 'Second_Mortgage_Payment_Monthly',
        'Property_Taxes_Yearly', 'Rent_Amount_Monthly', 'Gross_Rent',
        'Gross_Rent_Percentage_Income', 'Selected_Monthly_Owner_Costs',
        'Owner_Costs_Percentage_Income',

        # Household
        'Food_Stamp_SNAP', 'Family_Income', 'Household_Income',
        'Complete_Kitchen_Facilities', 'Complete_Plumbing_Facilities',
        'Multigenerational_Household', 'Response_Mode',

        # Technology (2017+ only)
        'Satellite_Internet', 'Smartphone', 'Tablet_Computer',
        'Internet_Access_Type', 'Broadband_Internet', 'High_Speed_Internet',
    }

    # Columns only available in 2017+ data
    HOUSING_2017_ONLY: Set[str] = {
        'Internet_Access_Type', 'Broadband_Internet', 'Dialup_Internet',
        'High_Speed_Internet', 'Laptop_Desktop_Computer', 'Hot_Water_Heater_Fuel',
        'Other_Internet_Service', 'Computer_Other',
    }

    POPULATION_2017_ONLY: Set[str] = {
        'Census_Division', 'Census_Region',
        'Military_Service_Period_CD', 'Military_Service_Period_FG',
        'Military_Service_Period_HI', 'Military_Service_Period_JK',
    }

    @classmethod
    def validate_targets(cls, targets: List[str], survey_type: str) -> Dict[str, bool]:
        """
        Check if target columns are valid for survey type.

        Args:
            targets: List of target column names
            survey_type: 'population' or 'housing'

        Returns:
            Dict mapping column name to validity (True/False)
        """
        valid_cols = cls.POPULATION_COLUMNS if survey_type == 'population' else cls.HOUSING_COLUMNS
        return {t: t in valid_cols for t in targets}

    @classmethod
    def validate_features(cls, features: List[str], survey_type: str) -> Dict[str, bool]:
        """
        Check if feature columns are valid for survey type.

        Args:
            features: List of feature column names
            survey_type: 'population' or 'housing'

        Returns:
            Dict mapping column name to validity (True/False)
        """
        return cls.validate_targets(features, survey_type)

    @classmethod
    def get_available_features(cls, df: pd.DataFrame,
                               exclude: Optional[List[str]] = None) -> List[str]:
        """
        Get numeric features available in DataFrame.

        Args:
            df: DataFrame to check
            exclude: Columns to exclude (typically targets)

        Returns:
            List of available numeric column names
        """
        numeric = df.select_dtypes(include=['number']).columns.tolist()
        exclude = exclude or []
        return [c for c in numeric if c not in exclude]

    @classmethod
    def get_valid_columns(cls, survey_type: str, year: Optional[int] = None) -> Set[str]:
        """
        Get set of valid column names for survey type and year.

        Args:
            survey_type: 'population' or 'housing'
            year: Optional data year (affects 2017+ columns)

        Returns:
            Set of valid standardized column names
        """
        if survey_type == 'population':
            valid = cls.POPULATION_COLUMNS.copy()
            if year and year < 2017:
                valid -= cls.POPULATION_2017_ONLY
        else:
            valid = cls.HOUSING_COLUMNS.copy()
            if year and year < 2017:
                valid -= cls.HOUSING_2017_ONLY
        return valid

    @classmethod
    def filter_available(cls, df: pd.DataFrame, columns: List[str]) -> List[str]:
        """
        Filter column list to only those available in DataFrame.

        Args:
            df: DataFrame to check
            columns: List of column names to filter

        Returns:
            List of columns that exist in df
        """
        return [c for c in columns if c in df.columns]

    @classmethod
    def report_missing(cls, df: pd.DataFrame, required: List[str],
                       context: str = "validation") -> Dict[str, List[str]]:
        """
        Generate report of missing columns.

        Args:
            df: DataFrame to check
            required: List of required column names
            context: Description for logging

        Returns:
            Dict with 'available' and 'missing' column lists
        """
        available = [c for c in required if c in df.columns]
        missing = [c for c in required if c not in df.columns]
        return {
            'context': context,
            'available': available,
            'missing': missing,
            'available_count': len(available),
            'missing_count': len(missing),
        }


# Convenience functions for direct import
def validate_dl_targets(targets: List[str], survey_type: str) -> bool:
    """Check if all deep learning targets are valid for survey type."""
    validation = ColumnValidator.validate_targets(targets, survey_type)
    return all(validation.values())


def get_survey_columns(survey_type: str, year: int = 2023) -> Set[str]:
    """Get valid columns for survey type and year."""
    return ColumnValidator.get_valid_columns(survey_type, year)

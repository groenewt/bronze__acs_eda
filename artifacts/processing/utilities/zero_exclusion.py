"""Zero exclusion utilities for economic columns"""

from typing import List

# Population survey columns where zero should be excluded
_POP_ZERO_EXCLUDE = [
    # Income columns (schema.py _income_cols)
    'Wage_Income', 'Total_Person_Earnings', 'Total_Person_Income',
    'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
    'Retirement_Income', 'Social_Security_Income', 'Supplemental_Security_Income',
    'Public_Assistance_Income', 'Other_Income',
    # Work/Hours columns (schema.py _work_travel_demographics, _education_work_cols)
    'Travel_Time_To_Work_Minutes', 'Hours_Worked_Per_Week', 'Weeks_Worked_Past_Year',
    # Derived population features
    'Income_Per_Hour', 'Income_Per_Week_Worked', 'Total_Annual_Hours',
]

# Housing survey columns where zero should be excluded
_HOUSING_ZERO_EXCLUDE = [
    # Property values (schema.py _unit_status_cols)
    'Property_Value',
    # Utility costs (schema.py _utility_costs)
    'Condo_Fee_Monthly', 'Electricity_Cost_Monthly', 'Fuel_Cost_Monthly',
    'Gas_Cost_Monthly', 'Insurance_Cost_Yearly', 'Water_Cost_Yearly',
    # Mortgage costs (schema.py _mortgage_costs)
    'Mobile_Home_Costs_Monthly', 'First_Mortgage_Payment_Monthly',
    'Second_Mortgage_Payment_Monthly', 'Property_Taxes_Yearly',
    # Rental costs (schema.py _rental_costs)
    'Rent_Amount_Monthly', 'Gross_Rent', 'Selected_Monthly_Owner_Costs',
    # Household income (schema.py _household_family_cols)
    'Family_Income', 'Household_Income',
    # Derived housing features
    'Total_Monthly_Utility_Cost', 'Property_Tax_Rate', 'Annual_Rent_to_Value_Ratio',
]

# Combined list for backward compatibility
_EXCLUDE_ZERO_RAW = _POP_ZERO_EXCLUDE + _HOUSING_ZERO_EXCLUDE

# NORMALIZE TO UPPERCASE for robust case-insensitive matching
EXCLUDE_ZERO_COLUMNS = {col.upper().strip() for col in _EXCLUDE_ZERO_RAW}
_POP_ZERO_EXCLUDE_SET = {col.upper().strip() for col in _POP_ZERO_EXCLUDE}
_HOUSING_ZERO_EXCLUDE_SET = {col.upper().strip() for col in _HOUSING_ZERO_EXCLUDE}


def get_zero_exclusion_columns(survey_type: str) -> List[str]:
    """Get appropriate zero-exclusion columns for survey type."""
    if survey_type == 'population':
        return _POP_ZERO_EXCLUDE.copy()
    elif survey_type == 'housing':
        return _HOUSING_ZERO_EXCLUDE.copy()
    return _EXCLUDE_ZERO_RAW.copy()


def should_exclude_zeros(col: str, survey_type: str = None) -> bool:
    """
    Check if zeros should be excluded for this column - CASE INSENSITIVE.

    Args:
        col: Column name to check
        survey_type: Optional survey type ('population' or 'housing') for targeted check
    """
    col_upper = col.upper().strip()
    if survey_type == 'population':
        return col_upper in _POP_ZERO_EXCLUDE_SET
    elif survey_type == 'housing':
        return col_upper in _HOUSING_ZERO_EXCLUDE_SET
    return col_upper in EXCLUDE_ZERO_COLUMNS

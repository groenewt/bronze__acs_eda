"""
Feature group definitions for domain-specific analysis
Maps domain names to their associated feature columns
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
from typing import Dict, List


# ============================================================================
# FEATURE GROUPS FOR DOMAIN-SPECIFIC ANALYSIS
# ============================================================================

FEATURE_GROUPS = {
    'disability': [
        'Disability_Status', 'Hearing_Difficulty', 'Vision_Difficulty',
        'Cognitive_Difficulty', 'Ambulatory_Difficulty', 'Self_Care_Difficulty',
        'Independent_Living_Difficulty', 'Disability_Count', 'Disability_Severity',
        'Has_Disability', 'Disability_Employment_Interaction'
    ],
    'health_insurance': [
        'Health_Insurance_Coverage', 'Health_Insurance_Employer',
        'Health_Insurance_Direct', 'Health_Insurance_Medicare',
        'Health_Insurance_Medicaid', 'Health_Insurance_Tricare',
        'Health_Insurance_VA', 'Health_Insurance_IHS',
        'Public_Health_Insurance', 'Private_Health_Insurance',
        'Insurance_Coverage_Count', 'Primary_Insurance_Type',
        'Is_Uninsured', 'Vulnerable_Uninsured', 'Coverage_Comprehensiveness_Score'
    ],
    'occupation_industry': [
        'Industry_Code', 'Industry_Code_2007', 'Industry_Code_2002',
        'Occupation_Code', 'Occupation_Code_2010', 'Occupation_Code_2002',
        'Industry_Sector', 'Occupation_Category', 'Occupation_Skill_Level',
        'Class_Of_Worker', 'Employer_Type'
    ],
    'education_field': [
        'Field_Of_Degree_1', 'Field_Of_Degree_2', 'Science_Engineering_Field',
        'Science_Engineering_Related', 'Is_STEM', 'STEM_Category',
        'Field_Income_Premium', 'FOD1P', 'FOD2P', 'SCIENGP', 'SCIENGRLP'
    ],
    'demographics': [
        'Age', 'Sex', 'Race', 'Hispanic_Origin', 'Marital_Status',
        'Citizenship_Status', 'Nativity', 'Ancestry', 'Place_Of_Birth'
    ],
    'economic': [
        'Total_Person_Income', 'Wage_Income', 'Self_Employment_Income',
        'Interest_Income', 'Social_Security_Income', 'Supplemental_Security_Income',
        'Public_Assistance_Income', 'Retirement_Income', 'Other_Income',
        'Poverty_Status', 'Income_To_Poverty_Ratio', 'SNAP_Received'
    ],
    'education': [
        'Educational_Attainment', 'School_Enrollment', 'Grade_Level_Attending',
        'Undergraduate_Field', 'Graduate_Field'
    ],
    'employment': [
        'Employment_Status', 'Employment_Status_Recode', 'Labor_Force_Status',
        'Weeks_Worked', 'Hours_Worked_Per_Week', 'Work_Experience',
        'Full_Or_Part_Time_Status', 'Multiple_Jobs'
    ],
    'housing': [
        'Housing_Tenure', 'Units_In_Structure', 'Year_Built', 'Year_Moved_In',
        'Vehicles_Available', 'Bedrooms', 'Rooms', 'Kitchen_Facilities',
        'Plumbing_Facilities', 'Telephone_Service', 'Internet_Access'
    ],
    'household_composition': [
        'Household_Size', 'Persons_In_Family', 'Number_Of_Children',
        'Dependency_Ratio', 'High_Dependency_Household', 'SNAP_Eligible_Proxy',
        'Workers_Per_Person_Ratio', 'Grandparent_Living_With_Grandchildren',
        'Relationship_To_Householder'
    ]
}


def get_domain_features(df: pd.DataFrame, domain: str) -> List[str]:
    """
    Get available features for a specific domain that exist in the DataFrame.

    Args:
        df: DataFrame to check for available columns
        domain: Domain name from FEATURE_GROUPS

    Returns:
        List of column names that exist in both FEATURE_GROUPS[domain] and df.columns
    """
    if domain not in FEATURE_GROUPS:
        raise ValueError(f"Unknown domain: {domain}. Available: {list(FEATURE_GROUPS.keys())}")

    domain_features = FEATURE_GROUPS[domain]
    available = [col for col in domain_features if col in df.columns]
    return available


def get_all_domain_features(df: pd.DataFrame, domains: List[str] = None) -> Dict[str, List[str]]:
    """
    Get available features for multiple domains.

    Args:
        df: DataFrame to check for available columns
        domains: List of domain names, or None for all domains

    Returns:
        Dict mapping domain names to lists of available columns
    """
    if domains is None:
        domains = list(FEATURE_GROUPS.keys())

    result = {}
    for domain in domains:
        features = get_domain_features(df, domain)
        if features:  # Only include domains with available features
            result[domain] = features

    return result

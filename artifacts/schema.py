from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# BASE SCHEMA INTERFACE
# ============================================================================

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


# ============================================================================
# PARENT SURVEY CLASSES (WORK WITH STANDARDIZED NAMES ONLY)
# ============================================================================

class PopulationSurvey(SchemaDefinition):
    """
    Parent class for population surveys.
    ALL column references use standardized names (post-renaming).
    Children classes handle raw-to-standard mappings.
    """

    def get_core_columns(self) -> List[Tuple[str, str, str]]:
        """Core columns using standardized names"""
        return [
            ("Census_Year", "INT", "Census_Year"),
            ("State_FIPS", None, "State_FIPS"),
            ("Survey_Type", None, "Survey_Type"),
            ("Survey_Scope", None, "Survey_Scope"),
            ("Record_Type", None, "Record_Type"),
            ("Serial_Number", None, "Serial_Number"),
            ("Person_Number", "INT", "Person_Number"),
            ("Public_Use_Microdata_Area", "INT", "Public_Use_Microdata_Area"),
            ("State_Code", "INT", "State_Code"),
            ("Income_Adjustment_Factor", "DECIMAL(10,6)", "Income_Adjustment_Factor"),
            ("Person_Weight", "INT", "Person_Weight"),
        ]

    def get_optional_columns(self) -> List[Tuple[str, str, str]]:
        """All optional columns using standardized names"""
        return (
                self._person_demographics() +
                self._military_service_periods() +
                self._work_income() +
                self._recode_columns() +
                self._race_columns() +
                self._additional_columns() +
                self._flag_columns() +
                self._weight_replicates() +
                self._industry_occupation_codes()
        )

    # Helper methods returning groups of standardized column names
    def _person_demographics(self) -> List[Tuple[str, str, str]]:
        return self._basic_demographics() + self._work_travel_demographics()
    
    def _basic_demographics(self) -> List[Tuple[str, str, str]]:
        return [
            ('Age', 'INT', 'Age'),
            ('Citizenship_Status', 'INT', 'Citizenship_Status'),
            ('Class_of_Worker', 'INT', 'Class_of_Worker'),
            ('English_Speaking_Ability', 'INT', 'English_Speaking_Ability'),
            ('Fertility_Status', 'INT', 'Fertility_Status'),
            ('Marital_Status', 'INT', 'Marital_Status'),
            ('Mobility_Status', 'INT', 'Mobility_Status'),
            ('Military_Service', 'INT', 'Military_Service'),
        ]
    
    def _work_travel_demographics(self) -> List[Tuple[str, str, str]]:
        return [
            ('Travel_Time_To_Work_Minutes', 'INT', 'Travel_Time_To_Work_Minutes'),
            ('Vehicle_Occupancy', 'INT', 'Vehicle_Occupancy'),
            ('Transportation_To_Work', 'INT', 'Transportation_To_Work'),
            ('Language_Other_Than_English', 'INT', 'Language_Other_Than_English'),
            ('Grandparents_Living_With_Grandchildren', 'INT', 'Grandparents_Living_With_Grandchildren'),
            ('Months_Responsible_For_Grandchildren', 'INT', 'Months_Responsible_For_Grandchildren'),
            ('Grandparents_Responsible_For_Grandchildren', 'INT', 'Grandparents_Responsible_For_Grandchildren'),
            ('Interest_Dividend_Rental_Income', 'BIGINT', 'Interest_Dividend_Rental_Income'),
        ]

    def _military_service_periods(self) -> List[Tuple[str, str, str]]:
        # 2012 format: Individual period columns (1-11)
        periods = [
            (f'Military_Service_Period_{i}', 'INT', f'Military_Service_Period_{i}')
            for i in range(1, 12)
        ]
        # 2017+ format: Combined period columns
        periods.extend([
            ('Military_Service_Period_CD', 'INT', 'Military_Service_Period_CD'),
            ('Military_Service_Period_FG', 'INT', 'Military_Service_Period_FG'),
            ('Military_Service_Period_HI', 'INT', 'Military_Service_Period_HI'),
            ('Military_Service_Period_JK', 'INT', 'Military_Service_Period_JK'),
        ])
        return periods

    def _work_income(self) -> List[Tuple[str, str, str]]:
        return self._work_status_cols() + self._income_cols() + self._education_work_cols()
    
    def _work_status_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Temporary_Absence_From_Work', 'INT', 'Temporary_Absence_From_Work'),
            ('Available_For_Work', 'INT', 'Available_For_Work'),
            ('On_Layoff_From_Work', 'INT', 'On_Layoff_From_Work'),
            ('Looking_For_Work', 'INT', 'Looking_For_Work'),
            ('Informed_Of_Recall', 'INT', 'Informed_Of_Recall'),
        ]
    
    def _income_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Other_Income', 'BIGINT', 'Other_Income'),
            ('Public_Assistance_Income', 'BIGINT', 'Public_Assistance_Income'),
            ('Retirement_Income', 'BIGINT', 'Retirement_Income'),
            ('Self_Employment_Income', 'BIGINT', 'Self_Employment_Income'),
            ('Supplemental_Security_Income', 'BIGINT', 'Supplemental_Security_Income'),
            ('Social_Security_Income', 'BIGINT', 'Social_Security_Income'),
            ('Wage_Income', 'BIGINT', 'Wage_Income'),
        ]
    
    def _education_work_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Relationship_To_Householder', 'INT', 'Relationship_To_Householder'),
            ('School_Enrollment', 'INT', 'School_Enrollment'),
            ('School_Grade_Attending', 'INT', 'School_Grade_Attending'),
            ('Educational_Attainment', 'INT', 'Educational_Attainment'),
            ('Sex', 'INT', 'Sex'),
            ('Hours_Worked_Per_Week', 'INT', 'Hours_Worked_Per_Week'),
            ('When_Last_Worked', 'INT', 'When_Last_Worked'),
            ('Weeks_Worked_Past_Year', 'INT', 'Weeks_Worked_Past_Year'),
            ('Year_Of_Entry', 'INT', 'Year_Of_Entry'),
        ]

    def _recode_columns(self) -> List[Tuple[str, str, str]]:
        return self._ancestry_employment_recodes() + self._location_recodes() + self._person_income_recodes()
    
    def _ancestry_employment_recodes(self) -> List[Tuple[str, str, str]]:
        return [
            ('Ancestry_Recode', 'INT', 'Ancestry_Recode'),
            ('First_Ancestry_Code', 'INT', 'First_Ancestry_Code'),
            ('Second_Ancestry_Code', 'INT', 'Second_Ancestry_Code'),
            ('Decade_Of_Entry', 'INT', 'Decade_Of_Entry'),
            ('Drives_Alone_To_Work', 'INT', 'Drives_Alone_To_Work'),
            ('Employment_Status_Parents', 'INT', 'Employment_Status_Parents'),
            ('Employment_Status_Recode', 'INT', 'Employment_Status_Recode'),
            ('Hispanic_Origin', 'INT', 'Hispanic_Origin'),
        ]
    
    def _location_recodes(self) -> List[Tuple[str, str, str]]:
        return [
            ('Time_Of_Arrival_At_Work', 'INT', 'Time_Of_Arrival_At_Work'),
            ('Time_Of_Departure_For_Work', 'INT', 'Time_Of_Departure_For_Work'),
            ('Language_Spoken_At_Home', 'INT', 'Language_Spoken_At_Home'),
            ('Migration_PUMA', 'INT', 'Migration_PUMA'),
            ('Migration_State_Or_Country', 'INT', 'Migration_State_Or_Country'),
            ('Place_Of_Birth', 'INT', 'Place_Of_Birth'),
            ('Place_Of_Work_PUMA', 'INT', 'Place_Of_Work_PUMA'),
            ('Place_Of_Work_State_Or_Country', 'INT', 'Place_Of_Work_State_Or_Country'),
        ]
    
    def _person_income_recodes(self) -> List[Tuple[str, str, str]]:
        return [
            ('Married_Spouse_Present', 'INT', 'Married_Spouse_Present'),
            ('Nativity', 'INT', 'Nativity'),
            ('Nativity_Of_Parent', 'INT', 'Nativity_Of_Parent'),
            ('Own_Child', 'INT', 'Own_Child'),
            ('Presence_And_Age_Own_Children', 'INT', 'Presence_And_Age_Own_Children'),
            ('Total_Person_Earnings', 'BIGINT', 'Total_Person_Earnings'),
            ('Total_Person_Income', 'BIGINT', 'Total_Person_Income'),
            ('Poverty_Status', 'INT', 'Poverty_Status'),
            ('Quarter_Of_Birth', 'INT', 'Quarter_Of_Birth'),
        ]

    def _race_columns(self) -> List[Tuple[str, str, str]]:
        return self._race_category_cols() + self._race_detail_cols()
    
    def _race_category_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Race_Recode', 'INT', 'Race_Recode'),
            ('Race_Two_Categories', 'INT', 'Race_Two_Categories'),
            ('Race_Three_Categories', 'INT', 'Race_Three_Categories'),
            ('Number_Of_Races', 'INT', 'Number_Of_Races'),
        ]
    
    def _race_detail_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Race_American_Indian_Alaska_Native', 'INT', 'Race_American_Indian_Alaska_Native'),
            ('Race_Asian', 'INT', 'Race_Asian'),
            ('Race_Black', 'INT', 'Race_Black'),
            ('Race_Native_Hawaiian_Pacific_Islander', 'INT', 'Race_Native_Hawaiian_Pacific_Islander'),
            ('Race_Some_Other', 'INT', 'Race_Some_Other'),
            ('Race_White', 'INT', 'Race_White'),
            ('Related_Child', 'INT', 'Related_Child'),
        ]

    def _additional_columns(self) -> List[Tuple[str, str, str]]:
        return [
            ('Subfamily_Number', 'INT', 'Subfamily_Number'),
            ('Subfamily_Relationship', 'INT', 'Subfamily_Relationship'),
            ('Veteran_Period_Of_Service', 'INT', 'Veteran_Period_Of_Service'),
            ('World_Area_Of_Birth', 'INT', 'World_Area_Of_Birth'),
        ]

    def _flag_columns(self) -> List[Tuple[str, str, str]]:
        return self._create_flag_tuples(self._flag_names_list())
    
    def _flag_names_list(self) -> List[str]:
        return self._flag_demographic_names() + self._flag_economic_names() + self._flag_work_names()
    
    def _flag_demographic_names(self) -> List[str]:
        return ['Age', 'Ancestry', 'Citizenship', 'English_Ability', 'Fertility', 
                'Hispanic_Origin', 'Marital_Status', 'Mobility_Status', 'Race', 
                'Sex', 'Education', 'School_Enrollment', 'School_Grade']
    
    def _flag_economic_names(self) -> List[str]:
        return ['Interest_Dividend_Income', 'Other_Income', 'Public_Assistance',
                'Retirement_Income', 'Self_Employment_Income', 'Social_Security_Income',
                'Supplemental_Security_Income', 'Wage_Income']
    
    def _flag_work_names(self) -> List[str]:
        return ['Class_Worker', 'Employment_Status', 'Grandparents_Living_Grandchildren',
                'Months_Responsible_Grandchildren', 'Grandparents_Responsible', 'Industry',
                'Departure_Time_Work', 'Travel_Time_Work', 'Vehicle_Occupancy',
                'Transportation_Work', 'Language_Home', 'Language_Other', 'Migration_State',
                'Military_Periods', 'Military_Service', 'Occupation', 'Place_Birth',
                'Place_Work', 'Relationship', 'Hours_Worked', 'When_Last_Worked',
                'Weeks_Worked', 'Year_Entry']
    
    def _create_flag_tuples(self, flag_names: List[str]) -> List[Tuple[str, str, str]]:
        return [(f'Flag_{name}', 'INT', f'Flag_{name}') for name in flag_names]

    def _weight_replicates(self) -> List[Tuple[str, str, str]]:
        return [(f'Person_Weight_Replicate_{i}', 'INT', f'Person_Weight_Replicate_{i}')
                for i in range(1, 81)]

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for a given data year."""
        availability = {col[0]: True for col in self.get_all_columns()}
        # DIVISION/REGION not in population data before 2017
        if year < 2017:
            availability['Census_Division'] = False
            availability['Census_Region'] = False
            # Combined military codes only in 2017+
            for code in ['Military_Service_Period_CD', 'Military_Service_Period_FG',
                         'Military_Service_Period_HI', 'Military_Service_Period_JK']:
                availability[code] = False
        else:
            # Individual military codes only in 2012 format
            for i in range(1, 12):
                availability[f'Military_Service_Period_{i}'] = False
        return availability

    def _industry_occupation_codes(self) -> List[Tuple[str, str, str]]:
        return [
            ('Industry_Code_2002', 'INT', 'Industry_Code_2002'),
            ('NAICS_Industry_Code_2002', 'STRING', 'NAICS_Industry_Code_2002'),
            ('Occupation_Code_2002', 'INT', 'Occupation_Code_2002'),
            ('Standard_Occupation_Code_2000', 'STRING', 'Standard_Occupation_Code_2000'),
            ('Occupation_Code_2010', 'INT', 'Occupation_Code_2010'),
            ('Standard_Occupation_Code_2010', 'STRING', 'Standard_Occupation_Code_2010'),
            ('Industry_Code_2007', 'INT', 'Industry_Code_2007'),
            ('NAICS_Industry_Code_2007', 'STRING', 'NAICS_Industry_Code_2007'),
        ]


class HousingSurvey(SchemaDefinition):
    """
    Parent class for housing surveys.
    ALL column references use standardized names (post-renaming).
    Children classes handle raw-to-standard mappings.
    """

    def get_core_columns(self) -> List[Tuple[str, str, str]]:
        """Core columns using standardized names"""
        return [
            ("Census_Year", "INT", "Census_Year"),
            ("State_FIPS", None, "State_FIPS"),
            ("Survey_Type", None, "Survey_Type"),
            ("Survey_Scope", None, "Survey_Scope"),
            ("Serial_Number", None, "Serial_Number"),
            ("Census_Division", "INT", "Census_Division"),
            ("Public_Use_Microdata_Area", "INT", "Public_Use_Microdata_Area"),
            ("Census_Region", "INT", "Census_Region"),
            ("State_Code", "INT", "State_Code"),
            ("Housing_Adjustment_Factor", "DECIMAL(10,6)", "Housing_Adjustment_Factor"),
            ("Income_Adjustment_Factor", "DECIMAL(10,6)", "Income_Adjustment_Factor"),
            ("Housing_Unit_Weight", "INT", "Housing_Unit_Weight"),
        ]

    def get_optional_columns(self) -> List[Tuple[str, str, str]]:
        """All optional columns using standardized names"""
        return (
                self._unit_characteristics() +
                self._costs() +
                self._technology() +
                self._household() +
                self._flags() +
                self._weight_replicates()
        )

    # Helper methods returning groups of standardized column names
    def _unit_characteristics(self) -> List[Tuple[str, str, str]]:
        return self._physical_unit_cols() + self._unit_amenities_cols() + self._unit_status_cols()
    
    def _physical_unit_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Number_of_Persons', 'INT', 'Number_of_Persons'),
            ('Housing_Unit_Type', 'INT', 'Housing_Unit_Type'),
            ('Number_of_Bedrooms', 'INT', 'Number_of_Bedrooms'),
            ('Number_of_Rooms', 'INT', 'Number_of_Rooms'),
            ('Building_Type', 'INT', 'Building_Type'),
            ('Year_Structure_Built', 'INT', 'Year_Structure_Built'),
        ]
    
    def _unit_amenities_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Bathtub_or_Shower', 'INT', 'Bathtub_or_Shower'),
            ('Refrigerator', 'INT', 'Refrigerator'),
            ('Hot_and_Cold_Running_Water', 'INT', 'Hot_and_Cold_Running_Water'),
            ('Running_Water', 'INT', 'Running_Water'),
            ('Sink_with_Faucet', 'INT', 'Sink_with_Faucet'),
            ('Stove_or_Range', 'INT', 'Stove_or_Range'),
            ('Telephone_Service', 'INT', 'Telephone_Service'),
        ]
    
    def _unit_status_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Lot_Acreage', 'INT', 'Lot_Acreage'),
            ('Agricultural_Sales', 'INT', 'Agricultural_Sales'),
            ('Business_On_Property', 'INT', 'Business_On_Property'),
            ('Tenure', 'INT', 'Tenure'),
            ('Vacancy_Status', 'INT', 'Vacancy_Status'),
            ('Property_Value', 'BIGINT', 'Property_Value'),
            ('Vehicles_Available', 'INT', 'Vehicles_Available'),
        ]

    def _costs(self) -> List[Tuple[str, str, str]]:
        return self._utility_costs() + self._mortgage_costs() + self._rental_costs()
    
    def _utility_costs(self) -> List[Tuple[str, str, str]]:
        return [
            ('Condo_Fee_Monthly', 'INT', 'Condo_Fee_Monthly'),
            ('Electricity_Cost_Monthly', 'INT', 'Electricity_Cost_Monthly'),
            ('Fuel_Cost_Monthly', 'INT', 'Fuel_Cost_Monthly'),
            ('Gas_Cost_Monthly', 'INT', 'Gas_Cost_Monthly'),
            ('House_Heating_Fuel', 'INT', 'House_Heating_Fuel'),
            ('Insurance_Cost_Yearly', 'INT', 'Insurance_Cost_Yearly'),
            ('Water_Cost_Yearly', 'INT', 'Water_Cost_Yearly'),
        ]
    
    def _mortgage_costs(self) -> List[Tuple[str, str, str]]:
        return [
            ('Mobile_Home_Costs_Monthly', 'INT', 'Mobile_Home_Costs_Monthly'),
            ('First_Mortgage_Includes_Insurance', 'INT', 'First_Mortgage_Includes_Insurance'),
            ('First_Mortgage_Payment_Monthly', 'INT', 'First_Mortgage_Payment_Monthly'),
            ('First_Mortgage_Includes_Taxes', 'INT', 'First_Mortgage_Includes_Taxes'),
            ('First_Mortgage_Status', 'INT', 'First_Mortgage_Status'),
            ('Second_Mortgage_Payment_Monthly', 'INT', 'Second_Mortgage_Payment_Monthly'),
            ('Second_Mortgage_Status', 'INT', 'Second_Mortgage_Status'),
            ('Property_Taxes_Yearly', 'INT', 'Property_Taxes_Yearly'),
        ]
    
    def _rental_costs(self) -> List[Tuple[str, str, str]]:
        return [
            ('Meals_Included_in_Rent', 'INT', 'Meals_Included_in_Rent'),
            ('Rent_Amount_Monthly', 'INT', 'Rent_Amount_Monthly'),
            ('Gross_Rent', 'INT', 'Gross_Rent'),
            ('Gross_Rent_Percentage_Income', 'INT', 'Gross_Rent_Percentage_Income'),
            ('Selected_Monthly_Owner_Costs', 'INT', 'Selected_Monthly_Owner_Costs'),
            ('Owner_Costs_Percentage_Income', 'INT', 'Owner_Costs_Percentage_Income'),
        ]

    def _technology(self) -> List[Tuple[str, str, str]]:
        return [
            ('Satellite_Internet', 'INT', 'Satellite_Internet'),
            ('Smartphone', 'INT', 'Smartphone'),
            ('Tablet_Computer', 'INT', 'Tablet_Computer'),
            # 2017+ technology columns
            ('Internet_Access_Type', 'INT', 'Internet_Access_Type'),
            ('Broadband_Internet', 'INT', 'Broadband_Internet'),
            ('Dialup_Internet', 'INT', 'Dialup_Internet'),
            ('High_Speed_Internet', 'INT', 'High_Speed_Internet'),
            ('Laptop_Desktop_Computer', 'INT', 'Laptop_Desktop_Computer'),
            ('Hot_Water_Heater_Fuel', 'INT', 'Hot_Water_Heater_Fuel'),
            ('Other_Internet_Service', 'INT', 'Other_Internet_Service'),
            ('Computer_Other', 'INT', 'Computer_Other'),
        ]

    def _household(self) -> List[Tuple[str, str, str]]:
        return self._household_family_cols() + self._household_facilities_cols() + self._household_demographics()
    
    def _household_family_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Food_Stamp_SNAP', 'INT', 'Food_Stamp_SNAP'),
            ('Family_Type_Employment_Status', 'INT', 'Family_Type_Employment_Status'),
            ('Family_Income', 'BIGINT', 'Family_Income'),
            ('Family_Presence_Children', 'INT', 'Family_Presence_Children'),
            ('Household_Family_Type', 'INT', 'Household_Family_Type'),
            ('Household_Income', 'BIGINT', 'Household_Income'),
            ('Number_Persons_Family', 'INT', 'Number_Persons_Family'),
            ('Workers_In_Family', 'INT', 'Workers_In_Family'),
            ('Work_Experience_Householder_Spouse', 'INT', 'Work_Experience_Householder_Spouse'),
            ('Work_Status_Householder_Spouse', 'INT', 'Work_Status_Householder_Spouse'),
        ]
    
    def _household_facilities_cols(self) -> List[Tuple[str, str, str]]:
        return [
            ('Complete_Kitchen_Facilities', 'INT', 'Complete_Kitchen_Facilities'),
            ('Complete_Plumbing_Facilities', 'INT', 'Complete_Plumbing_Facilities'),
            ('Plumbing_Facilities_for_Project', 'INT', 'Plumbing_Facilities_for_Project'),
            ('Response_Mode', 'INT', 'Response_Mode'),
            ('Specified_Rent_Unit', 'INT', 'Specified_Rent_Unit'),
            ('Specified_Value_Unit', 'INT', 'Specified_Value_Unit'),
            ('Moved_When', 'INT', 'Moved_When'),
        ]
    
    def _household_demographics(self) -> List[Tuple[str, str, str]]:
        return self._household_language_children() + self._household_composition()
    
    def _household_language_children(self) -> List[Tuple[str, str, str]]:
        return [
            ('Household_Language', 'INT', 'Household_Language'),
            ('Household_Language_Detailed', 'INT', 'Household_Language_Detailed'),
            ('Limited_English_Speaking_Household', 'INT', 'Limited_English_Speaking_Household'),
            ('Household_Grandchildren', 'INT', 'Household_Grandchildren'),
            ('Household_Children_Present', 'INT', 'Household_Children_Present'),
            ('Household_Own_Children_Present', 'INT', 'Household_Own_Children_Present'),
            ('Household_Related_Children_Present', 'INT', 'Household_Related_Children_Present'),
            ('Number_Own_Children', 'INT', 'Number_Own_Children'),
            ('Number_Related_Children', 'INT', 'Number_Related_Children'),
        ]
    
    def _household_composition(self) -> List[Tuple[str, str, str]]:
        return [
            ('Multigenerational_Household', 'INT', 'Multigenerational_Household'),
            ('Grandparent_Grandchildren', 'INT', 'Grandparent_Grandchildren'),
            ('Nonrelative_Present', 'INT', 'Nonrelative_Present'),
            ('Unmarried_Partner_Household', 'INT', 'Unmarried_Partner_Household'),
            ('Subfamilies_Present', 'INT', 'Subfamilies_Present'),
            ('Persons_Under_18', 'INT', 'Persons_Under_18'),
            ('Persons_60_And_Over', 'INT', 'Persons_60_And_Over'),
            ('Persons_65_And_Over', 'INT', 'Persons_65_And_Over'),
            ('Same_Sex_Married_Couple', 'INT', 'Same_Sex_Married_Couple'),
        ]

    def _flags(self) -> List[Tuple[str, str, str]]:
        return self._create_housing_flag_tuples(self._housing_flag_names())
    
    def _housing_flag_names(self) -> List[str]:
        return self._housing_flag_structure() + self._housing_flag_costs() + self._housing_flag_tech()
    
    def _housing_flag_structure(self) -> List[str]:
        return ['Access', 'Lot_Acreage', 'Agricultural_Sales', 'Bathtub', 'Bedrooms', 
                'Building_Type', 'Kitchen', 'Plumbing', 'Plumbing_Project', 'Refrigerator', 
                'Rooms', 'Running_Water', 'Running_Water_Project', 'Sink', 'Stove']
    
    def _housing_flag_costs(self) -> List[str]:
        return ['Condo_Fee', 'Electricity', 'Family_Income', 'Food_Stamp', 'Fuel', 'Gas', 
                'Gross_Rent', 'House_Heating_Fuel', 'Household_Income', 'Insurance', 
                'Mobile_Home', 'First_Mortgage_Insurance', 'First_Mortgage_Payment', 
                'First_Mortgage_Taxes', 'First_Mortgage_Status', 'Meals_Included_Rent', 
                'Rent_Amount', 'Selected_Monthly_Owner_Costs', 'Second_Mortgage_Payment', 
                'Second_Mortgage_Home_Equity', 'Second_Mortgage_Status', 'Property_Taxes', 
                'Property_Value', 'Water_Cost']
    
    def _housing_flag_tech(self) -> List[str]:
        return ['Broadband', 'Computer_Other', 'Dialup', 'High_Speed', 'Hot_Water', 'Laptop', 
                'Moved_When', 'Other_Service', 'Satellite', 'Smartphone', 'Tablet', 'Telephone', 
                'Tenure', 'Vacancy_Status', 'Vehicles', 'Year_Built', 'Business_On_Property']
    
    def _create_housing_flag_tuples(self, flag_names: List[str]) -> List[Tuple[str, str, str]]:
        return [(f'Flag_{name}', 'INT', f'Flag_{name}') for name in flag_names]

    def _weight_replicates(self) -> List[Tuple[str, str, str]]:
        return [(f'Weight_Replicate_{i}', 'INT', f'Weight_Replicate_{i}')
                for i in range(1, 81)]

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for a given data year."""
        availability = {col[0]: True for col in self.get_all_columns()}
        # Technology columns only available in 2017+ data
        if year < 2017:
            tech_2017_cols = ['Internet_Access_Type', 'Broadband_Internet', 'Dialup_Internet',
                              'High_Speed_Internet', 'Laptop_Desktop_Computer', 'Hot_Water_Heater_Fuel',
                              'Other_Internet_Service', 'Computer_Other']
            for col in tech_2017_cols:
                availability[col] = False
        return availability


# ============================================================================
# 1-YEAR SURVEY SCHEMAS
# ============================================================================

class Population1Year(PopulationSurvey):
    """1-year population survey with raw column name mappings"""

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 1-year column names to standardized names"""
        mapping = self._pop_core_mapping()
        mapping.update(self._pop_demo_mapping())
        mapping.update(self._pop_work_income_mapping())
        mapping.update(self._pop_recode_mapping())
        mapping.update(self._pop_race_additional_mapping())
        mapping.update(self._pop_flag_mapping())
        mapping.update(self._pop_weight_mapping())
        return mapping

    def _pop_core_mapping(self) -> Dict[str, str]:
        return {'year': 'Census_Year', 'state_fips': 'State_FIPS', 'survey_type': 'Survey_Type',
                'survey_scope': 'Survey_Scope', 'RT': 'Record_Type', 'SERIALNO': 'Serial_Number',
                'SPORDER': 'Person_Number', 'PUMA': 'Public_Use_Microdata_Area', 'ST': 'State_Code',
                'ADJINC': 'Income_Adjustment_Factor', 'PWGTP': 'Person_Weight'}

    def _pop_demo_mapping(self) -> Dict[str, str]:
        base = {'AGEP': 'Age', 'CIT': 'Citizenship_Status', 'COW': 'Class_of_Worker',
                'ENG': 'English_Speaking_Ability', 'FER': 'Fertility_Status',
                'GCL': 'Grandparents_Living_With_Grandchildren', 'GCM': 'Months_Responsible_For_Grandchildren',
                'GCR': 'Grandparents_Responsible_For_Grandchildren', 'INTP': 'Interest_Dividend_Rental_Income',
                'JWMNP': 'Travel_Time_To_Work_Minutes', 'JWRIP': 'Vehicle_Occupancy', 'JWTR': 'Transportation_To_Work'}
        base.update({'LANX': 'Language_Other_Than_English', 'MAR': 'Marital_Status', 'MIG': 'Mobility_Status',
                     'MIL': 'Military_Service'})
        # 2012 format: individual military service period codes (MLPA through MLPK)
        for i, c in enumerate('ABCDEFGHIJK', 1):
            base[f'MLP{c}'] = f'Military_Service_Period_{i}'
        # 2017+ format: combined military service period codes
        base.update({'MLPCD': 'Military_Service_Period_CD', 'MLPFG': 'Military_Service_Period_FG',
                     'MLPHI': 'Military_Service_Period_HI', 'MLPJK': 'Military_Service_Period_JK'})
        return base

    def _pop_work_income_mapping(self) -> Dict[str, str]:
        return {'NWAB': 'Temporary_Absence_From_Work', 'NWAV': 'Available_For_Work',
                'NWLA': 'On_Layoff_From_Work', 'NWLK': 'Looking_For_Work', 'NWRE': 'Informed_Of_Recall',
                'OIP': 'Other_Income', 'PAP': 'Public_Assistance_Income', 'RELP': 'Relationship_To_Householder',
                'RETP': 'Retirement_Income', 'SCH': 'School_Enrollment', 'SCHG': 'School_Grade_Attending',
                'SCHL': 'Educational_Attainment', 'SEMP': 'Self_Employment_Income', 'SEX': 'Sex',
                'SSIP': 'Supplemental_Security_Income', 'SSP': 'Social_Security_Income', 'WAGP': 'Wage_Income',
                'WKHP': 'Hours_Worked_Per_Week', 'WKL': 'When_Last_Worked', 'WKW': 'Weeks_Worked_Past_Year',
                'YOEP': 'Year_Of_Entry'}

    def _pop_recode_mapping(self) -> Dict[str, str]:
        return {'ANC': 'Ancestry_Recode', 'ANC1P': 'First_Ancestry_Code', 'ANC2P': 'Second_Ancestry_Code',
                'DECADE': 'Decade_Of_Entry', 'DRIVESP': 'Drives_Alone_To_Work', 'ESP': 'Employment_Status_Parents',
                'ESR': 'Employment_Status_Recode', 'HISP': 'Hispanic_Origin', 'JWAP': 'Time_Of_Arrival_At_Work',
                'JWDP': 'Time_Of_Departure_For_Work', 'LANP': 'Language_Spoken_At_Home', 'MIGPUMA': 'Migration_PUMA',
                'MIGSP': 'Migration_State_Or_Country', 'MSP': 'Married_Spouse_Present', 'NATIVITY': 'Nativity',
                'NOP': 'Nativity_Of_Parent', 'OC': 'Own_Child', 'PAOC': 'Presence_And_Age_Own_Children',
                'PERNP': 'Total_Person_Earnings', 'PINCP': 'Total_Person_Income', 'POBP': 'Place_Of_Birth',
                'POVPIP': 'Poverty_Status', 'POWPUMA': 'Place_Of_Work_PUMA', 'POWSP': 'Place_Of_Work_State_Or_Country',
                'QTRBIR': 'Quarter_Of_Birth'}

    def _pop_race_additional_mapping(self) -> Dict[str, str]:
        race = {'RAC1P': 'Race_Recode', 'RAC2P': 'Race_Two_Categories', 'RAC3P': 'Race_Three_Categories',
                'RACAIAN': 'Race_American_Indian_Alaska_Native', 'RACASN': 'Race_Asian', 'RACBLK': 'Race_Black',
                'RACNHPI': 'Race_Native_Hawaiian_Pacific_Islander', 'RACNUM': 'Number_Of_Races',
                'RACSOR': 'Race_Some_Other', 'RACWHT': 'Race_White', 'RC': 'Related_Child'}
        race.update({'SFN': 'Subfamily_Number', 'SFR': 'Subfamily_Relationship', 'VPS': 'Veteran_Period_Of_Service',
                     'WAOB': 'World_Area_Of_Birth', 'indp02': 'Industry_Code_2002', 'naicsp02': 'NAICS_Industry_Code_2002',
                     'occp02': 'Occupation_Code_2002', 'socp00': 'Standard_Occupation_Code_2000',
                     'occp10': 'Occupation_Code_2010', 'socp10': 'Standard_Occupation_Code_2010',
                     'indp07': 'Industry_Code_2007', 'naicsp07': 'NAICS_Industry_Code_2007'})
        return race

    def _pop_flag_mapping(self) -> Dict[str, str]:
        flags = ['FAGEP:Age', 'FANCP:Ancestry', 'FCITP:Citizenship', 'FCOWP:Class_Worker', 'FENGP:English_Ability',
                 'FESRP:Employment_Status', 'FFERP:Fertility', 'FGCLP:Grandparents_Living_Grandchildren',
                 'FGCMP:Months_Responsible_Grandchildren', 'FGCRP:Grandparents_Responsible', 'FHISP:Hispanic_Origin',
                 'FINDP:Industry', 'FINTP:Interest_Dividend_Income', 'FJWDP:Departure_Time_Work',
                 'FJWMNP:Travel_Time_Work', 'FJWRIP:Vehicle_Occupancy', 'FJWTRP:Transportation_Work',
                 'FLANP:Language_Home', 'FLANXP:Language_Other', 'FMARP:Marital_Status', 'FMIGP:Mobility_Status',
                 'FMIGSP:Migration_State', 'FMILPP:Military_Periods', 'FMILSP:Military_Service', 'FOCCP:Occupation',
                 'FOIP:Other_Income', 'FPAP:Public_Assistance', 'FPOBP:Place_Birth', 'FPOWSP:Place_Work',
                 'FRACP:Race', 'FRELP:Relationship', 'FRETP:Retirement_Income', 'FSCHGP:School_Grade',
                 'FSCHLP:Education', 'FSCHP:School_Enrollment', 'FSEMP:Self_Employment_Income', 'FSEXP:Sex',
                 'FSSIP:Supplemental_Security_Income', 'FSSP:Social_Security_Income', 'FWAGP:Wage_Income',
                 'FWKHP:Hours_Worked', 'FWKLP:When_Last_Worked', 'FWKWP:Weeks_Worked', 'FYOEP:Year_Entry']
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in flags}

    def _pop_weight_mapping(self) -> Dict[str, str]:
        return {f'PWGTP{i}': f'Person_Weight_Replicate_{i}' for i in range(1, 81)}


class Housing1Year(HousingSurvey):
    """1-year housing survey with raw column name mappings"""

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 1-year column names to standardized names"""
        mapping = self._h1y_core_mapping()
        mapping.update(self._h1y_unit_mapping())
        mapping.update(self._h1y_cost_tech_mapping())
        mapping.update(self._h1y_household_mapping())
        mapping.update(self._h1y_flag_mapping())
        mapping.update(self._h1y_weight_mapping())
        return mapping

    def _h1y_core_mapping(self) -> Dict[str, str]:
        return {'year': 'Census_Year', 'state_fips': 'State_FIPS', 'survey_type': 'Survey_Type',
                'survey_scope': 'Survey_Scope', 'SERIALNO': 'Serial_Number', 'DIVISION': 'Census_Division',
                'PUMA': 'Public_Use_Microdata_Area', 'REGION': 'Census_Region', 'ST': 'State_Code',
                'ADJHSG': 'Housing_Adjustment_Factor', 'ADJINC': 'Income_Adjustment_Factor',
                'WGTP': 'Housing_Unit_Weight'}

    def _h1y_unit_mapping(self) -> Dict[str, str]:
        return {'NP': 'Number_of_Persons', 'TYPE': 'Housing_Unit_Type', 'ACR': 'Lot_Acreage',
                'AGS': 'Agricultural_Sales', 'BATH': 'Bathtub_or_Shower', 'BDSP': 'Number_of_Bedrooms',
                'BLD': 'Building_Type', 'REFR': 'Refrigerator', 'RMSP': 'Number_of_Rooms',
                'RWAT': 'Hot_and_Cold_Running_Water', 'RWATPR': 'Running_Water', 'SINK': 'Sink_with_Faucet',
                'STOV': 'Stove_or_Range', 'TEL': 'Telephone_Service', 'TEN': 'Tenure', 'VACS': 'Vacancy_Status',
                'VALP': 'Property_Value', 'VEH': 'Vehicles_Available', 'YBL': 'Year_Structure_Built'}

    def _h1y_cost_tech_mapping(self) -> Dict[str, str]:
        costs = {'CONP': 'Condo_Fee_Monthly', 'ELEP': 'Electricity_Cost_Monthly', 'FULP': 'Fuel_Cost_Monthly',
                 'GASP': 'Gas_Cost_Monthly', 'HFL': 'House_Heating_Fuel', 'INSP': 'Insurance_Cost_Yearly',
                 'MHP': 'Mobile_Home_Costs_Monthly', 'MRGI': 'First_Mortgage_Includes_Insurance',
                 'MRGP': 'First_Mortgage_Payment_Monthly', 'MRGT': 'First_Mortgage_Includes_Taxes',
                 'MRGX': 'First_Mortgage_Status', 'RNTM': 'Meals_Included_in_Rent', 'RNTP': 'Rent_Amount_Monthly'}
        costs.update({'SMP': 'Second_Mortgage_Payment_Monthly', 'WATP': 'Water_Cost_Yearly', 'GRNTP': 'Gross_Rent',
                      'GRPIP': 'Gross_Rent_Percentage_Income', 'SMOCP': 'Selected_Monthly_Owner_Costs',
                      'SMX': 'Second_Mortgage_Status', 'TAXP': 'Property_Taxes_Yearly',
                      'OCPIP': 'Owner_Costs_Percentage_Income', 'SATELLITE': 'Satellite_Internet',
                      'SMARTPHONE': 'Smartphone', 'TABLET': 'Tablet_Computer'})
        # 2017+ housing technology columns (not present in 2012 data)
        tech_2017 = {'ACCESS': 'Internet_Access_Type', 'BROADBND': 'Broadband_Internet',
                     'DIALUP': 'Dialup_Internet', 'HISPEED': 'High_Speed_Internet',
                     'LAPTOP': 'Laptop_Desktop_Computer', 'HOTWAT': 'Hot_Water_Heater_Fuel',
                     'OTHSVCEX': 'Other_Internet_Service', 'COMPOTHX': 'Computer_Other'}
        costs.update(tech_2017)
        return costs

    def _h1y_household_mapping(self) -> Dict[str, str]:
        h1 = {'FS': 'Food_Stamp_SNAP', 'FES': 'Family_Type_Employment_Status', 'FINCP': 'Family_Income',
              'FPARC': 'Family_Presence_Children', 'HHL': 'Household_Language', 'HHLANP': 'Household_Language_Detailed',
              'HHT': 'Household_Family_Type', 'HINCP': 'Household_Income', 'HUGCL': 'Household_Grandchildren',
              'HUPAC': 'Household_Children_Present', 'HUPAOC': 'Household_Own_Children_Present'}
        h2 = {'HUPARC': 'Household_Related_Children_Present', 'KIT': 'Complete_Kitchen_Facilities',
              'LNGI': 'Limited_English_Speaking_Household', 'MULTG': 'Multigenerational_Household', 'MV': 'Moved_When',
              'NOC': 'Number_Own_Children', 'NPF': 'Number_Persons_Family', 'NPP': 'Grandparent_Grandchildren',
              'NR': 'Nonrelative_Present', 'NRC': 'Number_Related_Children', 'PARTNER': 'Unmarried_Partner_Household'}
        h3 = {'PLM': 'Complete_Plumbing_Facilities', 'PLMPRP': 'Plumbing_Facilities_for_Project',
              'PSF': 'Subfamilies_Present', 'R18': 'Persons_Under_18', 'R60': 'Persons_60_And_Over',
              'R65': 'Persons_65_And_Over', 'RESMODE': 'Response_Mode', 'SRNT': 'Specified_Rent_Unit',
              'SSMC': 'Same_Sex_Married_Couple', 'SVAL': 'Specified_Value_Unit', 'WIF': 'Workers_In_Family',
              'WKEXREL': 'Work_Experience_Householder_Spouse', 'WORKSTAT': 'Work_Status_Householder_Spouse'}
        h1.update(h2)
        h1.update(h3)
        return h1

    def _h1y_flag_mapping(self) -> Dict[str, str]:
        f1 = ['FACCESSP:Access', 'FACRP:Lot_Acreage', 'FAGSP:Agricultural_Sales', 'FBATHP:Bathtub',
              'FBDSP:Bedrooms', 'FBLDP:Building_Type', 'FBROADBNDP:Broadband', 'FCOMPOTHXP:Computer_Other',
              'FCONP:Condo_Fee', 'FDIALUPP:Dialup', 'FELEP:Electricity', 'FFINCP:Family_Income']
        f2 = ['FFSP:Food_Stamp', 'FFULP:Fuel', 'FGASP:Gas', 'FGRNTP:Gross_Rent', 'FHFLP:House_Heating_Fuel',
              'FHINCP:Household_Income', 'FHISPEEDP:High_Speed', 'FHOTWATP:Hot_Water', 'FINSP:Insurance',
              'FKITP:Kitchen', 'FLAPTOPP:Laptop', 'FMHP:Mobile_Home', 'FMRGIP:First_Mortgage_Insurance']
        f3 = ['FMRGP:First_Mortgage_Payment', 'FMRGTP:First_Mortgage_Taxes', 'FMRGXP:First_Mortgage_Status',
              'FMVP:Moved_When', 'FOTHSVCEXP:Other_Service', 'FPLMP:Plumbing', 'FPLMPRP:Plumbing_Project',
              'FREFRP:Refrigerator', 'FRMSP:Rooms', 'FRNTMP:Meals_Included_Rent', 'FRNTP:Rent_Amount']
        f4 = ['FRWATP:Running_Water', 'FRWATPRP:Running_Water_Project', 'FSATELLITEP:Satellite', 'FSINKP:Sink',
              'FSMARTPHONP:Smartphone', 'FSMOCP:Selected_Monthly_Owner_Costs', 'FSMP:Second_Mortgage_Payment',
              'FSMXHP:Second_Mortgage_Home_Equity', 'FSMXSP:Second_Mortgage_Status', 'FSTOVP:Stove',
              'FTABLETP:Tablet', 'FTAXP:Property_Taxes', 'FTELP:Telephone', 'FTENP:Tenure', 'FVACSP:Vacancy_Status',
              'FVALP:Property_Value', 'FVEHP:Vehicles', 'FWATP:Water_Cost', 'FYBLP:Year_Built']
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in f1 + f2 + f3 + f4}

    def _h1y_weight_mapping(self) -> Dict[str, str]:
        return {f'WGTP{i}': f'Weight_Replicate_{i}' for i in range(1, 81)}


# ============================================================================
# 5-YEAR SURVEY SCHEMAS
# ============================================================================

class Population5Year(PopulationSurvey):
    """5-year population survey with raw column name mappings"""

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """
        Maps raw 5-year column names to standardized names.
        Population data has identical structure between 1-year and 5-year.
        """
        # 5-year population uses the same raw column names as 1-year
        return Population1Year().get_raw_to_standard_mapping()


class Housing5Year(HousingSurvey):
    """5-year housing survey with raw column name mappings"""

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 5-year column names to standardized names"""
        mapping = Housing1Year()._h1y_core_mapping()
        mapping.update(self._h5y_unit_mapping())
        mapping.update(Housing1Year()._h1y_cost_tech_mapping())
        mapping.update(Housing1Year()._h1y_household_mapping())
        mapping.update(self._h5y_flag_mapping())
        mapping.update(Housing1Year()._h1y_weight_mapping())
        return mapping

    def _h5y_unit_mapping(self) -> Dict[str, str]:
        """5-year uses BDS/RMS/VAL instead of BDSP/RMSP/VALP, plus BUS field"""
        return {'NP': 'Number_of_Persons', 'TYPE': 'Housing_Unit_Type', 'ACR': 'Lot_Acreage',
                'AGS': 'Agricultural_Sales', 'BATH': 'Bathtub_or_Shower', 'BDS': 'Number_of_Bedrooms',
                'BLD': 'Building_Type', 'BUS': 'Business_On_Property', 'REFR': 'Refrigerator',
                'RMS': 'Number_of_Rooms', 'RWAT': 'Hot_and_Cold_Running_Water', 'RWATPR': 'Running_Water',
                'SINK': 'Sink_with_Faucet', 'STOV': 'Stove_or_Range', 'TEL': 'Telephone_Service', 'TEN': 'Tenure',
                'VACS': 'Vacancy_Status', 'VAL': 'Property_Value', 'VEH': 'Vehicles_Available',
                'YBL': 'Year_Structure_Built'}

    def _h5y_flag_mapping(self) -> Dict[str, str]:
        """5-year has fewer flags and includes FBUSP"""
        flags = ['FACRP:Lot_Acreage', 'FAGSP:Agricultural_Sales', 'FBDSP:Bedrooms', 'FBLDP:Building_Type',
                 'FBUSP:Business_On_Property', 'FCONP:Condo_Fee', 'FELEP:Electricity', 'FFSP:Food_Stamp',
                 'FFULP:Fuel', 'FGASP:Gas', 'FHFLP:House_Heating_Fuel', 'FINSP:Insurance', 'FKITP:Kitchen',
                 'FMHP:Mobile_Home', 'FMRGIP:First_Mortgage_Insurance', 'FMRGP:First_Mortgage_Payment',
                 'FMRGTP:First_Mortgage_Taxes', 'FMRGXP:First_Mortgage_Status', 'FMVP:Moved_When',
                 'FPLMP:Plumbing', 'FRMSP:Rooms', 'FRNTMP:Meals_Included_Rent', 'FRNTP:Rent_Amount',
                 'FSMP:Second_Mortgage_Payment', 'FSMXHP:Second_Mortgage_Home_Equity', 'FSMXSP:Second_Mortgage_Status',
                 'FTAXP:Property_Taxes', 'FTELP:Telephone', 'FTENP:Tenure', 'FVACSP:Vacancy_Status',
                 'FVALP:Property_Value', 'FVEHP:Vehicles', 'FWATP:Water_Cost', 'FYBLP:Year_Built']
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in flags}


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Default to 1-Year schemas for backward compatibility
PopulationSchema = Population1Year
HousingSchema = Housing1Year
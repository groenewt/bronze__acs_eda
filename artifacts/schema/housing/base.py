from typing import Dict, List, Tuple
from ..base import SchemaDefinition


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

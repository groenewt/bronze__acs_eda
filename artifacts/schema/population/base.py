from typing import Dict, List, Tuple
from ..base import SchemaDefinition


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
                self._disability_columns() +
                self._health_insurance_columns() +
                self._education_field_columns() +
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

    def _disability_columns(self) -> List[Tuple[str, str, str]]:
        """Disability-related columns"""
        return [
            ('Disability_Status', 'INT', 'Disability_Status'),
            ('Self_Care_Difficulty', 'INT', 'Self_Care_Difficulty'),
            ('Hearing_Difficulty', 'INT', 'Hearing_Difficulty'),
            ('Vision_Difficulty', 'INT', 'Vision_Difficulty'),
            ('Independent_Living_Difficulty', 'INT', 'Independent_Living_Difficulty'),
            ('Ambulatory_Difficulty', 'INT', 'Ambulatory_Difficulty'),
            ('VA_Service_Disability_Rating', 'INT', 'VA_Service_Disability_Rating'),
            ('VA_Disability_Rating_Exists', 'INT', 'VA_Disability_Rating_Exists'),
            ('Cognitive_Difficulty', 'INT', 'Cognitive_Difficulty'),
        ]

    def _health_insurance_columns(self) -> List[Tuple[str, str, str]]:
        """Health insurance coverage columns"""
        return [
            ('Health_Insurance_Employer', 'INT', 'Health_Insurance_Employer'),
            ('Health_Insurance_Direct', 'INT', 'Health_Insurance_Direct'),
            ('Health_Insurance_Medicare', 'INT', 'Health_Insurance_Medicare'),
            ('Health_Insurance_Medicaid', 'INT', 'Health_Insurance_Medicaid'),
            ('Health_Insurance_Tricare', 'INT', 'Health_Insurance_Tricare'),
            ('Health_Insurance_VA', 'INT', 'Health_Insurance_VA'),
            ('Health_Insurance_IHS', 'INT', 'Health_Insurance_IHS'),
            ('Health_Insurance_Coverage', 'INT', 'Health_Insurance_Coverage'),
            ('Private_Health_Insurance', 'INT', 'Private_Health_Insurance'),
            ('Public_Health_Insurance', 'INT', 'Public_Health_Insurance'),
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
            # Raw industry/occupation codes (generic, non-year-suffixed)
            ('Industry_Code', 'STRING', 'Industry_Code'),
            ('Occupation_Code', 'STRING', 'Occupation_Code'),
        ]

    def _education_field_columns(self) -> List[Tuple[str, str, str]]:
        """Field of degree and science/engineering columns"""
        return [
            ('Field_Of_Degree_1', 'INT', 'Field_Of_Degree_1'),
            ('Field_Of_Degree_2', 'INT', 'Field_Of_Degree_2'),
            ('Science_Engineering_Field', 'INT', 'Science_Engineering_Field'),
            ('Science_Engineering_Related', 'INT', 'Science_Engineering_Related'),
        ]

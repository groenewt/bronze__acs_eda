from typing import Dict
from ..base import PopulationSurvey


class Population1Year_2012_2016(PopulationSurvey):
    """
    Population survey schema for 2012-2016 era.

    Key characteristics:
    - Uses: DIS, ADJINC, RELP (standardized)
    - Has: ALL disability, health insurance, education field columns
    - Has: MARHD, MARHM, MARHT, MARHW, MARHYP (relationship details)
    - Weights: lowercase pwgtp1-80 (2012), uppercase PWGTP1-80 (2013+)
    - Military: individual codes MLPA-MLPK
    - Has: SSPA
    """

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 2012-2016 column names to standardized names"""
        mapping = self._pop_core_mapping()
        mapping.update(self._pop_demo_mapping())
        mapping.update(self._pop_work_income_mapping())
        mapping.update(self._pop_recode_mapping())
        mapping.update(self._pop_race_additional_mapping())
        mapping.update(self._pop_disability_mapping())
        mapping.update(self._pop_health_insurance_mapping())
        mapping.update(self._pop_education_field_mapping())
        mapping.update(self._pop_relationship_details_mapping())
        mapping.update(self._pop_flag_mapping())
        mapping.update(self._pop_weight_mapping_2012_2016())
        return mapping

    def _pop_core_mapping(self) -> Dict[str, str]:
        """Core columns with standardized naming"""
        return {
            'year': 'Census_Year',
            'state_fips': 'State_FIPS',
            'survey_type': 'Survey_Type',
            'survey_scope': 'Survey_Scope',
            'RT': 'Record_Type',
            'SERIALNO': 'Serial_Number',
            'SPORDER': 'Person_Number',
            'PUMA': 'Public_Use_Microdata_Area',
            'ST': 'State_Code',
            'ADJINC': 'Income_Adjustment_Factor',
            'PWGTP': 'Person_Weight'
        }

    def _pop_demo_mapping(self) -> Dict[str, str]:
        """Demographics with standardized naming"""
        base = {
            'AGEP': 'Age',
            'CIT': 'Citizenship_Status',
            'COW': 'Class_of_Worker',
            'ENG': 'English_Speaking_Ability',
            'FER': 'Fertility_Status',
            'GCL': 'Grandparents_Living_With_Grandchildren',
            'GCM': 'Months_Responsible_For_Grandchildren',
            'GCR': 'Grandparents_Responsible_For_Grandchildren',
            'INTP': 'Interest_Dividend_Rental_Income',
            'JWMNP': 'Travel_Time_To_Work_Minutes',
            'JWRIP': 'Vehicle_Occupancy',
            'JWTR': 'Transportation_To_Work',
            'LANX': 'Language_Other_Than_English',
            'MAR': 'Marital_Status',
            'MIG': 'Mobility_Status',
            'MIL': 'Military_Service'
        }
        # 2012-2016 format: individual military service period codes (MLPA through MLPK)
        for i, c in enumerate('ABCDEFGHIJK', 1):
            base[f'MLP{c}'] = f'Military_Service_Period_{i}'
        return base

    def _pop_work_income_mapping(self) -> Dict[str, str]:
        """Work and income with standardized naming (RELP)"""
        return {
            'NWAB': 'Temporary_Absence_From_Work',
            'NWAV': 'Available_For_Work',
            'NWLA': 'On_Layoff_From_Work',
            'NWLK': 'Looking_For_Work',
            'NWRE': 'Informed_Of_Recall',
            'OIP': 'Other_Income',
            'PAP': 'Public_Assistance_Income',
            'RELP': 'Relationship_To_Householder',
            'RETP': 'Retirement_Income',
            'SCH': 'School_Enrollment',
            'SCHG': 'School_Grade_Attending',
            'SCHL': 'Educational_Attainment',
            'SEMP': 'Self_Employment_Income',
            'SEX': 'Sex',
            'SSIP': 'Supplemental_Security_Income',
            'SSP': 'Social_Security_Income',
            'SSPA': 'Social_Security_Allocated',  # 2012-2016 has SSPA
            'WAGP': 'Wage_Income',
            'WKHP': 'Hours_Worked_Per_Week',
            'WKL': 'When_Last_Worked',
            'WKW': 'Weeks_Worked_Past_Year',
            'YOEP': 'Year_Of_Entry'
        }

    def _pop_recode_mapping(self) -> Dict[str, str]:
        """Recode columns"""
        return {
            'ANC': 'Ancestry_Recode',
            'ANC1P': 'First_Ancestry_Code',
            'ANC2P': 'Second_Ancestry_Code',
            'DECADE': 'Decade_Of_Entry',
            'DRIVESP': 'Drives_Alone_To_Work',
            'ESP': 'Employment_Status_Parents',
            'ESR': 'Employment_Status_Recode',
            'HISP': 'Hispanic_Origin',
            'JWAP': 'Time_Of_Arrival_At_Work',
            'JWDP': 'Time_Of_Departure_For_Work',
            'LANP': 'Language_Spoken_At_Home',
            'MIGPUMA': 'Migration_PUMA',
            'MIGSP': 'Migration_State_Or_Country',
            'MSP': 'Married_Spouse_Present',
            'NATIVITY': 'Nativity',
            'NOP': 'Nativity_Of_Parent',
            'OC': 'Own_Child',
            'PAOC': 'Presence_And_Age_Own_Children',
            'PERNP': 'Total_Person_Earnings',
            'PINCP': 'Total_Person_Income',
            'POBP': 'Place_Of_Birth',
            'POVPIP': 'Poverty_Status',
            'POWPUMA': 'Place_Of_Work_PUMA',
            'POWSP': 'Place_Of_Work_State_Or_Country',
            'QTRBIR': 'Quarter_Of_Birth'
        }

    def _pop_race_additional_mapping(self) -> Dict[str, str]:
        """Race and additional columns"""
        race = {
            'RAC1P': 'Race_Recode',
            'RAC2P': 'Race_Two_Categories',
            'RAC3P': 'Race_Three_Categories',
            'RACAIAN': 'Race_American_Indian_Alaska_Native',
            'RACASN': 'Race_Asian',
            'RACBLK': 'Race_Black',
            'RACNHPI': 'Race_Native_Hawaiian_Pacific_Islander',
            'RACNUM': 'Number_Of_Races',
            'RACSOR': 'Race_Some_Other',
            'RACWHT': 'Race_White',
            'RC': 'Related_Child'
        }
        race.update({
            'SFN': 'Subfamily_Number',
            'SFR': 'Subfamily_Relationship',
            'VPS': 'Veteran_Period_Of_Service',
            'WAOB': 'World_Area_Of_Birth',
            'indp02': 'Industry_Code_2002',
            'naicsp02': 'NAICS_Industry_Code_2002',
            'occp02': 'Occupation_Code_2002',
            'socp00': 'Standard_Occupation_Code_2000',
            'occp10': 'Occupation_Code_2010',
            'socp10': 'Standard_Occupation_Code_2010',
            'indp07': 'Industry_Code_2007',
            'naicsp07': 'NAICS_Industry_Code_2007',
            'INDP': 'Industry_Code',
            'OCCP': 'Occupation_Code'
        })
        return race

    def _pop_disability_mapping(self) -> Dict[str, str]:
        """Disability columns - available in 2012-2016"""
        return {
            'DIS': 'Disability_Status',
            'DDRS': 'Self_Care_Difficulty',
            'DEAR': 'Hearing_Difficulty',
            'DEYE': 'Vision_Difficulty',
            'DOUT': 'Independent_Living_Difficulty',
            'DPHY': 'Ambulatory_Difficulty',
            'DRAT': 'VA_Service_Disability_Rating',
            'DRATX': 'VA_Disability_Rating_Exists',
            'DREM': 'Cognitive_Difficulty',
        }

    def _pop_health_insurance_mapping(self) -> Dict[str, str]:
        """Health insurance columns - available in 2012-2016"""
        return {
            'HINS1': 'Health_Insurance_Employer',
            'HINS2': 'Health_Insurance_Direct',
            'HINS3': 'Health_Insurance_Medicare',
            'HINS4': 'Health_Insurance_Medicaid',
            'HINS5': 'Health_Insurance_Tricare',
            'HINS6': 'Health_Insurance_VA',
            'HINS7': 'Health_Insurance_IHS',
            'HICOV': 'Health_Insurance_Coverage',
            'PRIVCOV': 'Private_Health_Insurance',
            'PUBCOV': 'Public_Health_Insurance',
        }

    def _pop_education_field_mapping(self) -> Dict[str, str]:
        """Education field columns - available in 2012-2016"""
        return {
            'FOD1P': 'Field_Of_Degree_1',
            'FOD2P': 'Field_Of_Degree_2',
            'SCIENGP': 'Science_Engineering_Field',
            'SCIENGRLP': 'Science_Engineering_Related',
        }

    def _pop_relationship_details_mapping(self) -> Dict[str, str]:
        """Relationship detail columns - available in 2012-2016"""
        return {
            'MARHD': 'Marriage_Divorced',
            'MARHM': 'Marriage_Married',
            'MARHT': 'Marriage_Times',
            'MARHW': 'Marriage_Widowed',
            'MARHYP': 'Marriage_Year',
        }

    def _pop_flag_mapping(self) -> Dict[str, str]:
        """Flag columns"""
        flags = [
            'FAGEP:Age', 'FANCP:Ancestry', 'FCITP:Citizenship', 'FCOWP:Class_Worker', 'FENGP:English_Ability',
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
            'FWKHP:Hours_Worked', 'FWKLP:When_Last_Worked', 'FWKWP:Weeks_Worked', 'FYOEP:Year_Entry'
        ]
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in flags}

    def _pop_weight_mapping_2012_2016(self) -> Dict[str, str]:
        """Weight replicates - mixed case in 2012-2016 (lowercase 2012, uppercase 2013+)"""
        mapping = {}
        # Include both lowercase (2012) and uppercase (2013+) versions
        for i in range(1, 81):
            mapping[f'pwgtp{i}'] = f'Person_Weight_Replicate_{i}'  # 2012
            mapping[f'PWGTP{i}'] = f'Person_Weight_Replicate_{i}'  # 2013+
        return mapping

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for 2012-2016 era"""
        availability = {col[0]: True for col in self.get_all_columns()}

        # NO DIVISION/REGION in 2012-2016
        availability['Census_Division'] = False
        availability['Census_Region'] = False

        # 2012-2016 uses individual military codes, NOT combined codes
        for code in ['Military_Service_Period_CD', 'Military_Service_Period_FG',
                     'Military_Service_Period_HI', 'Military_Service_Period_JK']:
            availability[code] = False

        return availability

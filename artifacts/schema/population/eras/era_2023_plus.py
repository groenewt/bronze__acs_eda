from typing import Dict
from ..base import PopulationSurvey


class Population1Year_2023_Plus(PopulationSurvey):
    """
    Population survey schema for 2023+ era.

    Key characteristics:
    - Renames: JWTR→JWTRNS, WKW→WKWN, RELP→RELSHIPP, ST→STATE
    - New: HIMRKS, FHIMRKSP (marketplace), MLPIK
    - Weights: uppercase PWGTP1-80
    - Has: ALL disability, health insurance, education field columns
    - Has: DIVISION, REGION (geography)
    """

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 2023+ column names to standardized names"""
        mapping = self._pop_core_mapping_2023()
        mapping.update(self._pop_demo_mapping_2023())
        mapping.update(self._pop_work_income_mapping_2023())
        mapping.update(self._pop_recode_mapping())
        mapping.update(self._pop_race_additional_mapping())
        mapping.update(self._pop_disability_mapping())
        mapping.update(self._pop_health_insurance_mapping_2023())
        mapping.update(self._pop_education_field_mapping())
        mapping.update(self._pop_geography_mapping())
        mapping.update(self._pop_flag_mapping())
        mapping.update(self._pop_weight_mapping())
        return mapping

    def _pop_core_mapping_2023(self) -> Dict[str, str]:
        """Core columns with 2023+ naming (ST→STATE)"""
        return {
            'year': 'Census_Year',
            'state_fips': 'State_FIPS',
            'survey_type': 'Survey_Type',
            'survey_scope': 'Survey_Scope',
            'RT': 'Record_Type',
            'SERIALNO': 'Serial_Number',
            'SPORDER': 'Person_Number',
            'PUMA': 'Public_Use_Microdata_Area',
            'STATE': 'State_Code',  # 2023+ uses STATE instead of ST
            'ADJINC': 'Income_Adjustment_Factor',
            'PWGTP': 'Person_Weight'
        }

    def _pop_demo_mapping_2023(self) -> Dict[str, str]:
        """Demographics with 2023+ naming (JWTR→JWTRNS)"""
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
            'JWTRNS': 'Transportation_To_Work',  # 2023+ uses JWTRNS instead of JWTR
            'LANX': 'Language_Other_Than_English',
            'MAR': 'Marital_Status',
            'MIG': 'Mobility_Status',
            'MIL': 'Military_Service'
        }
        # 2023+ format: consolidated military service period codes + new MLPIK
        base.update({
            'MLPCD': 'Military_Service_Period_CD',
            'MLPFG': 'Military_Service_Period_FG',
            'MLPHI': 'Military_Service_Period_HI',
            'MLPJK': 'Military_Service_Period_JK',
            'MLPIK': 'Military_Service_Period_IK',  # New in 2023+
        })
        return base

    def _pop_work_income_mapping_2023(self) -> Dict[str, str]:
        """Work and income with 2023+ naming (WKW→WKWN, RELP→RELSHIPP)"""
        return {
            'NWAB': 'Temporary_Absence_From_Work',
            'NWAV': 'Available_For_Work',
            'NWLA': 'On_Layoff_From_Work',
            'NWLK': 'Looking_For_Work',
            'NWRE': 'Informed_Of_Recall',
            'OIP': 'Other_Income',
            'PAP': 'Public_Assistance_Income',
            'RELSHIPP': 'Relationship_To_Householder',  # 2023+ uses RELSHIPP instead of RELP
            'RETP': 'Retirement_Income',
            'SCH': 'School_Enrollment',
            'SCHG': 'School_Grade_Attending',
            'SCHL': 'Educational_Attainment',
            'SEMP': 'Self_Employment_Income',
            'SEX': 'Sex',
            'SSIP': 'Supplemental_Security_Income',
            'SSP': 'Social_Security_Income',
            'WAGP': 'Wage_Income',
            'WKHP': 'Hours_Worked_Per_Week',
            'WKL': 'When_Last_Worked',
            'WKWN': 'Weeks_Worked_Past_Year',  # 2023+ uses WKWN instead of WKW
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
        """Disability columns - available in 2023+"""
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

    def _pop_health_insurance_mapping_2023(self) -> Dict[str, str]:
        """Health insurance columns - available in 2023+ with new marketplace fields"""
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
            'HIMRKS': 'Health_Insurance_Marketplace',  # New in 2023+
        }

    def _pop_education_field_mapping(self) -> Dict[str, str]:
        """Education field columns - available in 2023+"""
        return {
            'FOD1P': 'Field_Of_Degree_1',
            'FOD2P': 'Field_Of_Degree_2',
            'SCIENGP': 'Science_Engineering_Field',
            'SCIENGRLP': 'Science_Engineering_Related',
        }

    def _pop_geography_mapping(self) -> Dict[str, str]:
        """Geography columns - available in 2023+"""
        return {
            'DIVISION': 'Census_Division',
            'REGION': 'Census_Region',
        }

    def _pop_flag_mapping(self) -> Dict[str, str]:
        """Flag columns - including new marketplace flag"""
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
            'FWKHP:Hours_Worked', 'FWKLP:When_Last_Worked', 'FWKWP:Weeks_Worked', 'FYOEP:Year_Entry',
            'FHIMRKSP:Marketplace'  # New in 2023+
        ]
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in flags}

    def _pop_weight_mapping(self) -> Dict[str, str]:
        """Weight replicates - uppercase in 2023+"""
        return {f'PWGTP{i}': f'Person_Weight_Replicate_{i}' for i in range(1, 81)}

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for 2023+ era"""
        availability = {col[0]: True for col in self.get_all_columns()}

        # 2023+ uses consolidated military codes, NOT individual codes
        for i in range(1, 12):
            availability[f'Military_Service_Period_{i}'] = False

        return availability

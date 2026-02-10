from typing import Dict
from ..base import HousingSurvey


class Housing1Year_2007_2011(HousingSurvey):
    """
    1-year housing survey for ACS data years 2007-2011.

    Key characteristics:
    - Uses BDS, RMS, VAL (not BDSP, RMSP, VALP)
    - Has BUS (Business_On_Property)
    - Weights are lowercase: wgtp1-80
    - NO technology columns (ACCESS, BROADBND, etc.)
    - NO adjustment factors (ADJHSG, ADJINC)
    - NO modern appliances (BATH, REFR, SINK, STOV)
    """

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 2007-2011 column names to standardized names"""
        mapping = self._h1y_core_mapping()
        mapping.update(self._h1y_unit_mapping())
        mapping.update(self._h1y_cost_mapping())
        mapping.update(self._h1y_household_mapping())
        mapping.update(self._h1y_flag_mapping())
        mapping.update(self._h1y_weight_mapping())
        return mapping

    def _h1y_core_mapping(self) -> Dict[str, str]:
        return {
            'year': 'Census_Year',
            'state_fips': 'State_FIPS',
            'survey_type': 'Survey_Type',
            'survey_scope': 'Survey_Scope',
            'SERIALNO': 'Serial_Number',
            'DIVISION': 'Census_Division',
            'PUMA': 'Public_Use_Microdata_Area',
            'REGION': 'Census_Region',
            'ST': 'State_Code',
            'WGTP': 'Housing_Unit_Weight',
            # NO ADJHSG, ADJINC in this era
        }

    def _h1y_unit_mapping(self) -> Dict[str, str]:
        return {
            'NP': 'Number_of_Persons',
            'TYPE': 'Housing_Unit_Type',
            'ACR': 'Lot_Acreage',
            'AGS': 'Agricultural_Sales',
            'BDS': 'Number_of_Bedrooms',  # Not BDSP
            'BLD': 'Building_Type',
            'BUS': 'Business_On_Property',  # Has BUS
            'RMS': 'Number_of_Rooms',  # Not RMSP
            'RWAT': 'Hot_and_Cold_Running_Water',
            'RWATPR': 'Running_Water',
            'TEL': 'Telephone_Service',
            'TEN': 'Tenure',
            'VACS': 'Vacancy_Status',
            'VAL': 'Property_Value',  # Not VALP
            'VEH': 'Vehicles_Available',
            'YBL': 'Year_Structure_Built',
            # NO BATH, REFR, SINK, STOV in this era
        }

    def _h1y_cost_mapping(self) -> Dict[str, str]:
        return {
            'CONP': 'Condo_Fee_Monthly',
            'ELEP': 'Electricity_Cost_Monthly',
            'FULP': 'Fuel_Cost_Monthly',
            'GASP': 'Gas_Cost_Monthly',
            'HFL': 'House_Heating_Fuel',
            'INSP': 'Insurance_Cost_Yearly',
            'MHP': 'Mobile_Home_Costs_Monthly',
            'MRGI': 'First_Mortgage_Includes_Insurance',
            'MRGP': 'First_Mortgage_Payment_Monthly',
            'MRGT': 'First_Mortgage_Includes_Taxes',
            'MRGX': 'First_Mortgage_Status',
            'RNTM': 'Meals_Included_in_Rent',
            'RNTP': 'Rent_Amount_Monthly',
            'SMP': 'Second_Mortgage_Payment_Monthly',
            'WATP': 'Water_Cost_Yearly',
            'GRNTP': 'Gross_Rent',
            'GRPIP': 'Gross_Rent_Percentage_Income',
            'SMOCP': 'Selected_Monthly_Owner_Costs',
            'SMX': 'Second_Mortgage_Status',
            'TAXP': 'Property_Taxes_Yearly',
            'OCPIP': 'Owner_Costs_Percentage_Income',
            # NO technology columns in this era
        }

    def _h1y_household_mapping(self) -> Dict[str, str]:
        h1 = {
            'FS': 'Food_Stamp_SNAP',
            'FINCP': 'Family_Income',
            'FPARC': 'Family_Presence_Children',
            'HHL': 'Household_Language',
            'HHLANP': 'Household_Language_Detailed',
            'HHT': 'Household_Family_Type',
            'HINCP': 'Household_Income',
            'HUGCL': 'Household_Grandchildren',
            'HUPAC': 'Household_Children_Present',
            'HUPAOC': 'Household_Own_Children_Present',
            'HUPARC': 'Household_Related_Children_Present',
        }
        h2 = {
            'KIT': 'Complete_Kitchen_Facilities',
            'LNGI': 'Limited_English_Speaking_Household',
            'MULTG': 'Multigenerational_Household',
            'MV': 'Moved_When',
            'NOC': 'Number_Own_Children',
            'NPF': 'Number_Persons_Family',
            'NPP': 'Grandparent_Grandchildren',
            'NR': 'Nonrelative_Present',
            'NRC': 'Number_Related_Children',
            'PARTNER': 'Unmarried_Partner_Household',
        }
        h3 = {
            'PLM': 'Complete_Plumbing_Facilities',
            'PLMPRP': 'Plumbing_Facilities_for_Project',
            'PSF': 'Subfamilies_Present',
            'R18': 'Persons_Under_18',
            'R60': 'Persons_60_And_Over',
            'R65': 'Persons_65_And_Over',
            'RESMODE': 'Response_Mode',
            'SRNT': 'Specified_Rent_Unit',
            'SVAL': 'Specified_Value_Unit',
            'WIF': 'Workers_In_Family',
            'WKEXREL': 'Work_Experience_Householder_Spouse',
            'WORKSTAT': 'Work_Status_Householder_Spouse',
            # NO FES, SSMC in this era
        }
        h1.update(h2)
        h1.update(h3)
        return h1

    def _h1y_flag_mapping(self) -> Dict[str, str]:
        # Flags for columns that exist in this era
        f1 = [
            'FACRP:Lot_Acreage', 'FAGSP:Agricultural_Sales', 'FBDSP:Bedrooms',
            'FBLDP:Building_Type', 'FBUSP:Business_On_Property', 'FCONP:Condo_Fee',
            'FELEP:Electricity', 'FFINCP:Family_Income', 'FFSP:Food_Stamp',
            'FFULP:Fuel', 'FGASP:Gas', 'FGRNTP:Gross_Rent', 'FHFLP:House_Heating_Fuel',
        ]
        f2 = [
            'FHINCP:Household_Income', 'FINSP:Insurance', 'FKITP:Kitchen',
            'FMHP:Mobile_Home', 'FMRGIP:First_Mortgage_Insurance',
            'FMRGP:First_Mortgage_Payment', 'FMRGTP:First_Mortgage_Taxes',
            'FMRGXP:First_Mortgage_Status', 'FMVP:Moved_When', 'FPLMP:Plumbing',
            'FPLMPRP:Plumbing_Project', 'FRMSP:Rooms', 'FRNTMP:Meals_Included_Rent',
        ]
        f3 = [
            'FRNTP:Rent_Amount', 'FRWATP:Running_Water', 'FRWATPRP:Running_Water_Project',
            'FSMOCP:Selected_Monthly_Owner_Costs', 'FSMP:Second_Mortgage_Payment',
            'FSMXHP:Second_Mortgage_Home_Equity', 'FSMXSP:Second_Mortgage_Status',
            'FTAXP:Property_Taxes', 'FTELP:Telephone', 'FTENP:Tenure',
            'FVACSP:Vacancy_Status', 'FVALP:Property_Value', 'FVEHP:Vehicles',
            'FYBLP:Year_Built',
        ]
        # NO technology flags in this era
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in f1 + f2 + f3}

    def _h1y_weight_mapping(self) -> Dict[str, str]:
        # Lowercase weights in this era
        return {f'wgtp{i}': f'Weight_Replicate_{i}' for i in range(1, 81)}

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for the 2007-2011 era."""
        availability = {col[0]: True for col in self.get_all_columns()}

        # NO adjustment factors
        availability['Housing_Adjustment_Factor'] = False
        availability['Income_Adjustment_Factor'] = False

        # NO modern appliances
        availability['Bathtub_or_Shower'] = False
        availability['Refrigerator'] = False
        availability['Sink_with_Faucet'] = False
        availability['Stove_or_Range'] = False

        # NO technology columns
        tech_cols = [
            'Satellite_Internet', 'Smartphone', 'Tablet_Computer',
            'Internet_Access_Type', 'Broadband_Internet', 'Dialup_Internet',
            'High_Speed_Internet', 'Laptop_Desktop_Computer', 'Hot_Water_Heater_Fuel',
            'Other_Internet_Service', 'Computer_Other'
        ]
        for col in tech_cols:
            availability[col] = False

        # NO FES, SSMC
        availability['Family_Type_Employment_Status'] = False
        availability['Same_Sex_Married_Couple'] = False

        return availability

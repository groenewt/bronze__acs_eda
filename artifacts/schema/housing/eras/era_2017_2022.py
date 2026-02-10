from typing import Dict
from ..base import HousingSurvey


class Housing1Year_2017_2022(HousingSurvey):
    """
    1-year housing survey for ACS data years 2017-2022.

    Key characteristics:
    - Uses BDSP, RMSP, VALP (standardized codes)
    - NO BUS field (Business_On_Property removed)
    - Has 21 technology columns (ACCESS, BROADBND, DIALUP, HISPEED, LAPTOP, etc.)
    - Weights: uppercase WGTP1-80
    - Has FES, SSMC
    - Has ADJHSG, ADJINC, BATH, REFR, SINK, STOV
    """

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """Maps raw 2017-2022 column names to standardized names"""
        mapping = self._h1y_core_mapping()
        mapping.update(self._h1y_unit_mapping())
        mapping.update(self._h1y_cost_tech_mapping())
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
            'ADJHSG': 'Housing_Adjustment_Factor',
            'ADJINC': 'Income_Adjustment_Factor',
            'WGTP': 'Housing_Unit_Weight',
        }

    def _h1y_unit_mapping(self) -> Dict[str, str]:
        return {
            'NP': 'Number_of_Persons',
            'TYPE': 'Housing_Unit_Type',
            'ACR': 'Lot_Acreage',
            'AGS': 'Agricultural_Sales',
            'BATH': 'Bathtub_or_Shower',
            'BDSP': 'Number_of_Bedrooms',
            'BLD': 'Building_Type',
            'REFR': 'Refrigerator',
            'RMSP': 'Number_of_Rooms',
            'RWAT': 'Hot_and_Cold_Running_Water',
            'RWATPR': 'Running_Water',
            'SINK': 'Sink_with_Faucet',
            'STOV': 'Stove_or_Range',
            'TEL': 'Telephone_Service',
            'TEN': 'Tenure',
            'VACS': 'Vacancy_Status',
            'VALP': 'Property_Value',
            'VEH': 'Vehicles_Available',
            'YBL': 'Year_Structure_Built',
            # NO BUS in this era
        }

    def _h1y_cost_tech_mapping(self) -> Dict[str, str]:
        costs = {
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
        }

        # Technology columns (new in 2017+)
        tech_2017 = {
            'ACCESS': 'Internet_Access_Type',
            'BROADBND': 'Broadband_Internet',
            'DIALUP': 'Dialup_Internet',
            'HISPEED': 'High_Speed_Internet',
            'LAPTOP': 'Laptop_Desktop_Computer',
            'HOTWAT': 'Hot_Water_Heater_Fuel',
            'OTHSVCEX': 'Other_Internet_Service',
            'COMPOTHX': 'Computer_Other',
            'SATELLITE': 'Satellite_Internet',
            'SMARTPHONE': 'Smartphone',
            'TABLET': 'Tablet_Computer',
        }
        costs.update(tech_2017)
        return costs

    def _h1y_household_mapping(self) -> Dict[str, str]:
        h1 = {
            'FS': 'Food_Stamp_SNAP',
            'FES': 'Family_Type_Employment_Status',  # New in 2017
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
            'SSMC': 'Same_Sex_Married_Couple',  # New in 2017
            'SVAL': 'Specified_Value_Unit',
            'WIF': 'Workers_In_Family',
            'WKEXREL': 'Work_Experience_Householder_Spouse',
            'WORKSTAT': 'Work_Status_Householder_Spouse',
        }
        h1.update(h2)
        h1.update(h3)
        return h1

    def _h1y_flag_mapping(self) -> Dict[str, str]:
        # Flags for columns that exist in this era
        f1 = [
            'FACCESSP:Access', 'FACRP:Lot_Acreage', 'FAGSP:Agricultural_Sales',
            'FBATHP:Bathtub', 'FBDSP:Bedrooms', 'FBLDP:Building_Type',
            'FBROADBNDP:Broadband', 'FCOMPOTHXP:Computer_Other', 'FCONP:Condo_Fee',
            'FDIALUPP:Dialup', 'FELEP:Electricity', 'FFINCP:Family_Income',
        ]
        f2 = [
            'FFSP:Food_Stamp', 'FFULP:Fuel', 'FGASP:Gas', 'FGRNTP:Gross_Rent',
            'FHFLP:House_Heating_Fuel', 'FHINCP:Household_Income',
            'FHISPEEDP:High_Speed', 'FHOTWATP:Hot_Water', 'FINSP:Insurance',
            'FKITP:Kitchen', 'FLAPTOPP:Laptop', 'FMHP:Mobile_Home',
            'FMRGIP:First_Mortgage_Insurance',
        ]
        f3 = [
            'FMRGP:First_Mortgage_Payment', 'FMRGTP:First_Mortgage_Taxes',
            'FMRGXP:First_Mortgage_Status', 'FMVP:Moved_When',
            'FOTHSVCEXP:Other_Service', 'FPLMP:Plumbing', 'FPLMPRP:Plumbing_Project',
            'FREFRP:Refrigerator', 'FRMSP:Rooms', 'FRNTMP:Meals_Included_Rent',
            'FRNTP:Rent_Amount',
        ]
        f4 = [
            'FRWATP:Running_Water', 'FRWATPRP:Running_Water_Project',
            'FSATELLITEP:Satellite', 'FSINKP:Sink', 'FSMARTPHONP:Smartphone',
            'FSMOCP:Selected_Monthly_Owner_Costs', 'FSMP:Second_Mortgage_Payment',
            'FSMXHP:Second_Mortgage_Home_Equity', 'FSMXSP:Second_Mortgage_Status',
            'FSTOVP:Stove', 'FTABLETP:Tablet', 'FTAXP:Property_Taxes',
            'FTELP:Telephone', 'FTENP:Tenure', 'FVACSP:Vacancy_Status',
            'FVALP:Property_Value', 'FVEHP:Vehicles', 'FYBLP:Year_Built',
        ]
        # NO FBUSP in this era
        return {f.split(':')[0]: f'Flag_{f.split(":")[1]}' for f in f1 + f2 + f3 + f4}

    def _h1y_weight_mapping(self) -> Dict[str, str]:
        # Uppercase weights in this era
        return {f'WGTP{i}': f'Weight_Replicate_{i}' for i in range(1, 81)}

    def get_column_availability(self, year: int) -> Dict[str, bool]:
        """Return which columns are available for the 2017-2022 era."""
        availability = {col[0]: True for col in self.get_all_columns()}

        # NO BUS
        availability['Business_On_Property'] = False

        # All technology columns ARE available in this era
        # FES and SSMC ARE available in this era

        return availability

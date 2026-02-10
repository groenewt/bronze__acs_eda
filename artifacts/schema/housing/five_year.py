from typing import Dict
from .base import HousingSurvey
from .one_year import Housing1Year


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

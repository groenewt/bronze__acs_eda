# Feature Engineering

> Documentation of derived features, transformations, and data preprocessing steps applied to prepare the dataset for analysis and modeling.

## Summary

| Metric | Value | Description |
| :--- | :--- | :--- |
| Features Created | 29 | New derived variables |
| Transformations Applied | 10 | Data transformations |
| Rows Before Cleaning | 226,816 | Original dataset size |
| Rows After Cleaning | 226,816 | Final dataset size |
| Data Retention | 100.0% | Percentage of data retained |
| Final Rows | 226,816 | Observations |
| Final Columns | 292 | Total variables |

## Created Features

> New variables derived from existing data to capture additional patterns and relationships.


### Income_Per_Hour

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Income_Per_Week_Worked

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Total_Annual_Hours

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Age_Group

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Years_Since_Start

| Property | Value |
| :--- | :--- |
| Description | Years elapsed since first year in dataset |
| Formula | `Year - min(Year)` |
| Purpose | Temporal index for trend analysis |


### Decade

| Property | Value |
| :--- | :--- |
| Description | Decade grouping of the year |
| Formula | `(Year // 10) × 10` |
| Purpose | Decadal trend analysis |


### Disability_Count

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Disability_Severity

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Has_Multiple_Disabilities

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Has_Disability

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_Employed

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Disability_Employment_Interaction

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Insurance_Coverage_Count

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Private_Insurance_Count

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Public_Insurance_Count

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_Uninsured

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Vulnerable_Uninsured

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Industry_Sector_2007

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Industry_Sector_2002

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Industry_Sector

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_Goods_Producing

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_Service_Sector

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Occupation_Skill_Level_2010

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Occupation_Skill_Level_2002

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Occupation_Skill_Level

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Skill_Level_Numeric

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### STEM_Category

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_STEM

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Is_STEM_Related

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


## Applied Transformations

- **Income ratios derived from work metrics**


- **Age binned into demographic groups**


### Temporal features extracted from year

| Property | Value |
| :--- | :--- |
| Description | Extracted temporal components for trend analysis |
| Columns Affected | Years_Since_Start, Decade |
| Purpose | Enable temporal modeling |
| Method | Arithmetic transformation |


- **Disability count and severity computed**


- **Disability-employment interactions created**


- **Insurance coverage type features created**


- **Uninsured and vulnerability features created**


- **Industry codes mapped to sectors from 3 columns**


- **Occupation skill levels from 3 columns**


- **STEM field categories created**


## Data Cleaning


### Cleaning Summary

- **Records Removed**: 0

- **Removal Rate**: 0.0%

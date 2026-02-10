# Feature Engineering

> Documentation of derived features, transformations, and data preprocessing steps applied to prepare the dataset for analysis and modeling.

## Summary

| Metric | Value | Description |
| :--- | :--- | :--- |
| Features Created | 14 | New derived variables |
| Transformations Applied | 5 | Data transformations |
| Rows Before Cleaning | 1,858,876 | Original dataset size |
| Rows After Cleaning | 1,858,876 | Final dataset size |
| Data Retention | 100.0% | Percentage of data retained |
| Final Rows | 1,858,876 | Observations |
| Final Columns | 254 | Total variables |

## Created Features

> New variables derived from existing data to capture additional patterns and relationships.


### Annual_Rent_to_Value_Ratio

| Property | Value |
| :--- | :--- |
| Description | Ratio of annual rent to property value |
| Formula | `(Gross_Rent × 12) / Property_Value` |
| Purpose | Assess rental yield and investment potential |


### Total_Monthly_Utility_Cost

| Property | Value |
| :--- | :--- |
| Description | Sum of all monthly utility expenses |
| Formula | `Electricity + Gas + Fuel + Water/12` |
| Purpose | Aggregate utility burden metric |


### Property_Tax_Rate

| Property | Value |
| :--- | :--- |
| Description | Effective property tax rate |
| Formula | `Property_Taxes_Yearly / Property_Value` |
| Purpose | Normalized tax burden comparison |


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


### Working_Age_Persons

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Dependency_Ratio

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### High_Dependency_Household

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### FPL_Threshold

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Income_to_FPL_Ratio

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### SNAP_Eligible_Proxy

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### SNAP_Takeup_Gap

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### Workers_Per_Person

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


### No_Worker_Household

- **Type**: Derived feature

- **Description**: Engineering feature for analysis


## Applied Transformations

### Housing cost ratios calculated

| Property | Value |
| :--- | :--- |
| Description | Computed derived ratios for housing affordability analysis |
| Columns Affected | Annual_Rent_to_Value_Ratio, Property_Tax_Rate |
| Purpose | Normalize costs for comparison |
| Method | Division with zero-handling |


### Temporal features extracted from year

| Property | Value |
| :--- | :--- |
| Description | Extracted temporal components for trend analysis |
| Columns Affected | Years_Since_Start, Decade |
| Purpose | Enable temporal modeling |
| Method | Arithmetic transformation |


- **Dependency ratio features created**


- **SNAP eligibility proxy features created**


- **Workers ratio features created**


## Data Cleaning


### Cleaning Summary

- **Records Removed**: 0

- **Removal Rate**: 0.0%

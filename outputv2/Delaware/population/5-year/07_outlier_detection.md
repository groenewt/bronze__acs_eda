# Outlier Detection

> Statistical outlier detection using IQR (Interquartile Range) method. Outliers are values falling outside Q1 - 1.5×IQR or Q3 + 1.5×IQR bounds.

## Detection Methodology

| Parameter | Value | Description |
| :--- | :--- | :--- |
| Method | IQR | Outlier detection algorithm |
| Lower Bound | Q1 - 1.5 × IQR | Values below are outliers |
| Upper Bound | Q3 + 1.5 × IQR | Values above are outliers |
| IQR Definition | Q3 - Q1 | Interquartile Range |



> **Note**: The IQR method is robust to extreme values and works well for approximately symmetric distributions.


## Outlier Summary

_No outlier summary available._
## High Outlier Rate Variables

> Variables with outlier rate > 5% may indicate data quality issues, non-normal distributions, or genuinely extreme values.


- **('Presence_And_Age_Own_Children', 21.75493045575581)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 17.968608436482693)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 16.217829103072045)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.360004298269644)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.370790979251419)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 12.36857359500311)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.94253031869248)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.2000193724829)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.42572544651303)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.10320387570736)**: 0 outliers (0.00%)

- **('Other_Income', 9.928798581600203)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.856639088566391)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.319025427193198)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.15082083328919)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.215278485843381)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

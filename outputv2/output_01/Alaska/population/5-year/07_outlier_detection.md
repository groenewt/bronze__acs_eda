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


- **('Hours_Worked_Per_Week', 17.602630405213628)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 13.489612188365651)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 12.641337677270986)**: 0 outliers (0.00%)

- **('Other_Income', 10.970189025842226)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 9.656277948128274)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.064203591267278)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 7.784951130701419)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 7.37391401558707)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 7.255540689895875)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 7.234572633192794)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 6.945143432310015)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 6.69045143811234)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 6.539063498147438)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 6.461806886418807)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 6.305896256547847)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

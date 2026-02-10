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


- **('Hours_Worked_Per_Week', 32.78257179233272)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 24.663253821297605)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.738139780026295)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.723095877131737)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 11.948655329541054)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.838006230529595)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.408829928748194)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 10.852713178294573)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 10.638447791023168)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.956463160232225)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 9.779668146364065)**: 0 outliers (0.00%)

- **('Other_Income', 9.014118498853627)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.472185889926413)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.330504186070346)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.599565739100623)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

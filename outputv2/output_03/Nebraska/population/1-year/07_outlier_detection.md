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


- **('Total_Annual_Hours', 15.41476394232498)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 13.671679635251287)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.444099780276593)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 11.595303118437528)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.10760564861463)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 10.426012284455135)**: 0 outliers (0.00%)

- **('Other_Income', 9.915170210421946)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 9.466391926043505)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.155172583777816)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 8.749634391216187)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.634445341961012)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.130416838629797)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.4456698776118015)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 7.264194658332429)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.549892853815336)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

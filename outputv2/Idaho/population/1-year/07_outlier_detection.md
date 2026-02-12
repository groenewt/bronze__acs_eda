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


- **('Total_Annual_Hours', 16.228351507376523)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.516311439756416)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 11.190041906599536)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 9.964499984925682)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 9.824110671936758)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 9.691654858452168)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 9.656589374816555)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 9.21430924500614)**: 0 outliers (0.00%)

- **('Other_Income', 9.178593652769134)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 9.043836112032318)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 8.63682956977901)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 8.227185022159244)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.233502538071066)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.845679845275042)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 6.810199282462541)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

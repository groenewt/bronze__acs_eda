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


- **('Hours_Worked_Per_Week', 34.08920561564302)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 24.033396904552795)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.960900153662202)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.002766390027663)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.182996992925553)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.96537753632044)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.89797686897977)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.156476944898102)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.673284523399513)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.332670436660038)**: 0 outliers (0.00%)

- **('Other_Income', 9.403336960464273)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.953697431606301)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.514889251815559)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.966639155553625)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 7.338248767505781)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

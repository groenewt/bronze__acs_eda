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


- **('Presence_And_Age_Own_Children', 23.494673549935566)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 22.861330218598223)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 16.282743032660534)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.42374729080601)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 13.994776051284571)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 13.662087626250214)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 13.042426562254953)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 12.82040889015984)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 12.259970599330666)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 12.000241282088762)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 9.803712552604921)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.76091219971538)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.6016746795007)**: 0 outliers (0.00%)

- **('Other_Income', 8.097375806809845)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 7.382657434967137)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

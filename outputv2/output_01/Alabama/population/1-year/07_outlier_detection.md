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


- **('Hours_Worked_Per_Week', 33.74645077123782)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 23.58467228221208)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.909067775044534)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.285309314881388)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 13.208746503941013)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 12.467045498473075)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 12.340123957890397)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.52112567165333)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.942311904853943)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.569793961884882)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 9.842170597623692)**: 0 outliers (0.00%)

- **('Other_Income', 9.709690492950235)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 9.080548386015487)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.824500563721003)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.63852487533341)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)

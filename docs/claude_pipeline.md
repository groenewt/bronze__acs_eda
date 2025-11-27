# Pipeline Documentation

This document details the complete analysis pipeline, step by step, demonstrating how **Content Augmented Generation (CAG)** bridges statistical metrics and contextual insights.

## Example Dataset: South Carolina Housing (5-Year ACS)

Throughout this document, we use **South Carolina Housing 5-Year** as our running example:

| Attribute | Value |
|-----------|-------|
| **State** | South Carolina (FIPS 45) |
| **Survey** | Housing |
| **Scope** | 5-Year estimates |
| **Years** | 2011-2023 (13 years, no gaps) |
| **Records** | 1,588,240 rows |
| **Columns** | 234 (after feature engineering) |
| **Output** | `output/South_Carolina/housing/5-year/` |
| **Log** | `logs/South Carolina/5-year/housing/` |

---

## Live Execution Trace

What actually happens when you run the pipeline? Here's the real log output:

```
[DL-INFO] TensorFlow 2.18.1 configured for CPU-only mode
[DL-INFO] Using 24 cores
[CONFIG] States: 1, Surveys: ['housing'], Scopes: ['5-year']

======================================================================
[HOUSING] Processing South Carolina (5-year)...
======================================================================
[VERBOSE] Searching for housing files with scope 5-year...
Pattern is:/data/temp/census/raw/acs/housing/5-Year/45/*/*.csv
[VERBOSE] Found 13 file(s) to load
[VERBOSE] Loading file 1/13: ss12hsc.csv
[VERBOSE]   -> Loaded 115,670 rows
...
[VERBOSE] Loading file 13/13: ss11hsc.csv
[VERBOSE]   -> Loaded 113,098 rows
[VERBOSE] Successfully loaded 13 dataframe(s)
[VERBOSE] Combined into 1,588,240 total rows
[INFO] Loaded 1,588,240 records
[CENSUS_YEAR_TRACK] After schema application: 1588240 valid, 13 unique
[VERBOSE] Feature engineering complete: (1588240, 234)
```

---

## Pipeline Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│  1. Data Load   │───▶│  2. Schema Apply │───▶│  3. Feature Eng.   │
│  (FileLoader)   │    │  (SchemaApplier) │    │  (FeatureCreator)  │
└─────────────────┘    └──────────────────┘    └────────────────────┘
                                                         │
         ┌───────────────────────────────────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│  4. Analysis    │───▶│  5. ML Pipeline  │───▶│  6. Deep Learning  │
│  (8 Analyzers)  │    │  (Reg/Clust/TS)  │    │  (TensorFlow CPU)  │
└─────────────────┘    └──────────────────┘    └────────────────────┘
                                                         │
         ┌───────────────────────────────────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│  7. Visualize   │───▶│  8. LLM Analysis │───▶│  9. Report Gen     │
│  (221 figures)  │    │  (CAG Context)   │    │  (22 sections)     │
└─────────────────┘    └──────────────────┘    └────────────────────┘
```

---

## Stage 1: Data Loading

**Source**: `processing.py` → `FileLoader`

The loader reads all CSV files matching the state/survey/scope pattern from the configured data directory and concatenates them into a single DataFrame.

**SC Housing 5-Year Output:**
```
Files Found: 13
Files Loaded: 13
Total Rows: 1,588,240
Columns Found: 227
```

**Output File**: [01_overview.md](../output/South_Carolina/housing/5-year/01_overview.md)

---

## Stage 2: Schema Application

**Source**: `processing.py` → `SchemaFactory`, `SchemaApplier`

Transforms raw ACS variable codes into human-readable column names:

| Raw Code | Transformed Name |
|----------|------------------|
| `VALP` | `Property_Value` |
| `RNTP` | `Gross_Rent` |
| `HINCP` | `Household_Income` |
| `TEN` | `Tenure` |
| `BDSP` | `Number_of_Bedrooms` |
| `RMSP` | `Number_of_Rooms` |
| `YBL` | `Year_Structure_Built` |
| `ELEP` | `Electricity_Cost_Monthly` |

---

## Stage 3: Feature Engineering

**Source**: `feature_engineering.py` → `SmartDataCleaner`, `FeatureCreator`

Creates derived features and handles data quality issues:

- **Income Features**: Brackets, percentiles, flags for zero values
- **Housing Features**: Affordability ratios, cost burden calculations
- **Temporal Features**: Year-based groupings, trend indicators
- **Economic Zero Handling**: Strategy-based (flag vs. impute)

**Output File**: [10_feature_engineering.md](../output/South_Carolina/housing/5-year/10_feature_engineering.md)

---

## Stage 4: Analysis Suite

Eight parallel analyzers process the prepared data:

### 4.1 Temporal Analysis
**Output**: [02_temporal_analysis.md](../output/South_Carolina/housing/5-year/02_temporal_analysis.md)

Year-by-year distributions showing record counts:
- 2011: 113,098 records
- 2023: 128,510 records
- Growth: ~13.6% over 13 years

### 4.2 Economic Analysis
**Output**: [03_economic_analysis.md](../output/South_Carolina/housing/5-year/03_economic_analysis.md)

| Metric | Data Points |
|--------|-------------|
| Median Rent Trend | 13 years |
| Owner Cost Burden | 13 years |
| Renter Cost Burden | 13 years |
| Electricity Cost | 13 years |
| Gas Cost | 13 years |
| Property Taxes | 7 years |

### 4.3 Statistical Analysis
**Output**: [04_statistical_analysis.md](../output/South_Carolina/housing/5-year/04_statistical_analysis.md)

Summary statistics for key variables:

| Variable | Mean | Median | Min | Max |
|----------|------|--------|-----|-----|
| Electricity_Cost_Monthly | $176.46 | $160 | $1 | $2,500 |
| First_Mortgage_Payment | $1,000.22 | $830 | $4 | $6,300 |
| Insurance_Cost_Yearly | $1,066.91 | $800 | $4 | $9,100 |
| Water_Cost_Yearly | $422.80 | $350 | $1 | $3,700 |

### 4.4 Correlation Analysis
**Output**: [05_correlation_analysis.md](../output/South_Carolina/housing/5-year/05_correlation_analysis.md)

Generates correlation heatmap for numeric variables.

### 4.5 Cross-Variable Analysis
**Output**: [06_cross_variable_analysis.md](../output/South_Carolina/housing/5-year/06_cross_variable_analysis.md)

Interaction effects and key ratios between variables.

### 4.6 Outlier Detection
**Output**: [07_outlier_detection.md](../output/South_Carolina/housing/5-year/07_outlier_detection.md)

Variables with highest outlier rates:

| Variable | Outlier Rate |
|----------|--------------|
| Specified_Rent_Unit | 24.6% |
| Mobile_Home_Costs_Monthly | 12.7% |
| Fuel_Cost_Monthly | 11.9% |
| Gas_Cost_Monthly | 10.4% |
| Flag_Property_Taxes | 9.7% |
| Gross_Rent_Percentage_Income | 9.6% |

### 4.7 Anomaly Detection
**Output**: [08_anomaly_detection.md](../output/South_Carolina/housing/5-year/08_anomaly_detection.md)

Temporal anomalies detected: **0** (clean dataset)

### 4.8 Trend Analysis
**Output**: [09_trend_analysis.md](../output/South_Carolina/housing/5-year/09_trend_analysis.md)

Long-term patterns across the 13-year span.

---

## Stage 5: Machine Learning Pipeline

**Source**: `ml_models.py` → `RegressionModeler`, `ClusteringModeler`, `TimeSeriesForecaster`, `ModelComparator`

### 5.1 Regression Models (Supervised)

Five algorithms trained per target variable:
- Linear Regression
- Ridge Regression
- Lasso Regression
- Random Forest
- Gradient Boosting

**Housing Targets**: `Property_Value`, `Gross_Rent`

Each model generates 8 visualizations:
- `predictions_HOUSING.png` - Actual vs Predicted
- `residuals_HOUSING.png` - Residual analysis
- `features_HOUSING.png` - Feature importance
- `cv_scores_HOUSING.png` - Cross-validation scores
- `error_distribution_HOUSING.png` - Error histogram
- `distribution_comparison_HOUSING.png` - Pred vs Actual distributions
- `feature_target_correlation_HOUSING.png` - Correlation with target
- `variance_comparison_HOUSING.png` - Variance analysis

**Figure Path**: `figures/ml/regression/{Target}/{Algorithm}/`

### 5.2 Clustering Models (Unsupervised)

Two algorithms:
- **KMeans** (k=5 clusters)
- **Hierarchical Clustering** (5 clusters)

Each generates 5 visualizations:
- `scatter_HOUSING.png` - 2D cluster visualization
- `silhouette_HOUSING.png` - Silhouette analysis
- `sizes_HOUSING.png` - Cluster size distribution
- `feature_distributions_HOUSING.png` - Features by cluster
- `variance_by_cluster_HOUSING.png` - Within-cluster variance

**Figure Path**: `figures/ml/clustering/{Algorithm}/`

### 5.3 Time Series Forecasting

Six methods for `Gross_Rent` forecasting:
- Simple Moving Average (SMA)
- Weighted Moving Average (WMA)
- Exponential Weighted Moving Average (EWMA)
- Polynomial Degree 1 (Linear)
- Polynomial Degree 2 (Quadratic)
- Polynomial Degree 3 (Cubic)

**Actual Forecasts from SC Housing 5-Year Run:**

```
[ML-TIMESERIES] Training time series for target: Gross_Rent
[DEBUG-TS] Target: Gross_Rent, Forecasts: {2024: 1209.28, 2025: 1321.93, 2026: 1456.48}
```

| Method | 2024 Forecast | 2025 Forecast | 2026 Forecast |
|--------|---------------|---------------|---------------|
| polynomial_degree_3 | $1,209 | $1,322 | $1,456 |
| polynomial_degree_2 | $1,149 | $1,210 | $1,276 |
| polynomial_degree_1 | $1,067 | $1,092 | $1,118 |
| wma | $1,069 | $1,069 | $1,069 |
| sma | $1,042 | $1,042 | $1,042 |
| ewma | $1,000 | $1,000 | $1,000 |

**Note**: `Property_Value` time series failed due to insufficient temporal variation:
```
[WARNING] Time series forecasting failed for Property_Value:
          Insufficient data for timeseries_forecast: need 3, got 1
```

Each generates 5 visualizations:
- `forecast_HOUSING.png` - Future predictions
- `confidence_intervals_HOUSING.png` - Uncertainty bounds
- `residuals_HOUSING.png` - Model residuals
- `accuracy_metrics_HOUSING.png` - Performance metrics
- `trend_decomposition_HOUSING.png` - Trend components

**Figure Path**: `figures/ml/time_series/{Target}/{Method}/`

**Output File**: [11_ml_models.md](../output/South_Carolina/housing/5-year/11_ml_models.md)

---

## Stage 6: Deep Learning Pipeline

**Source**: `deep_learning.py` → `DeepLearningTrainer`

**Configuration**:
- Epochs: 75
- Batch Size: 256
- Framework: TensorFlow (CPU)
- Workers: 1 (no multiprocessing for CPU)

### Housing Survey Tasks (5 Total)

| Task | Model Type | Targets | Layers | Params | R² |
|------|------------|---------|--------|--------|-----|
| property_valuation | HousingValuationModel | Property_Value, Gross_Rent | 7 | 36,994 | -0.09 |
| affordability_analysis | HousingAffordabilityModel | Owner_Costs_%, Gross_Rent_% | 6 | 10,306 | 0.04 |
| **housing_quality** | HousingQualityModel | Year_Built, Bedrooms, Rooms | 6 | 10,371 | **0.96** |
| cost_prediction | HousingDefaultModel | Taxes_Yearly, Insurance_Yearly | 6 | 10,306 | 0.05 |
| occupancy_prediction | HousingDefaultModel | Vacancy_Status, Tenure | 6 | 10,306 | 0.20 |

**Best Performer**: `housing_quality` with R² = 0.9554

Each task generates 9 visualizations:
- `training_history_housing.png` - Loss curves
- `predictions_vs_actual_housing.png` - Scatter plot
- `residual_analysis_housing.png` - Residuals
- `error_distribution_housing.png` - Error histogram
- `architecture_summary_housing.png` - Model diagram
- `{target}_detailed_analysis_housing.png` - Per-target analysis
- `convergence_diagnostics_housing.png` - Training stability
- `error_evolution_housing.png` - Error over epochs

**Dashboard Figures**:
- `learning_curves_comparison_housing.png` - All tasks compared
- `model_comparison_housing.png` - Performance summary

**Figure Path**: `figures/ml/deep_learning/{task_name}/`

**Output File**: [11b_deep_learning_models.md](../output/South_Carolina/housing/5-year/11b_deep_learning_models.md)

---

## Stage 7: Visualization Suite

**Source**: `visualizer.py` → `Visualizer`, `MLVisualizer`, `DLVisualizer`

**Total Figures Generated**: 221 PNG files
- Base visualizations: 50
- ML visualizations: 171

### Memory-Aware Sampling

The pipeline intelligently samples data to prevent OOM errors while preserving statistical validity:

```
[VISUALS] Creating comprehensive visualization suite for HOUSING...
[MEMORY-ORCHESTRATOR] Sampling 1,588,240 → 4,273 rows for all visualizers
[ML-SAMPLE] Housing: 1,588,240 → 42,735 rows (10,000,000 cells / 234 cols)
```

**Sampling Strategy**:
- **Visualizations**: 4,273 rows (keeps rendering fast, preserves distributions)
- **ML Training**: 42,735 rows (target ~10M cells for memory safety)

### 16 Specialized Visualizers

Each visualizer receives the sampled data and focuses on specific aspects:

```
[HOUSING-SAMPLE] TemporalVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] EconomicVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] CorrelationVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] StatisticalVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] AdvancedVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] YoYChangeVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] OutlierVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] DemographicsVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] TransportationVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] IncomeCompositionVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] HousingCharacteristicsVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] HouseholdCompositionVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] TechnologyAdoptionVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] CostBurdenVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] RaceEthnicityVisualizer: 4,273 → 4000 rows
[HOUSING-SAMPLE] MultiVariableVisualizer: 4,273 → 4000 rows
```

### Base Visualizations (50 figures)

| Category | Examples |
|----------|----------|
| Distributions | `income_distribution_HOUSING.png`, `year_distribution_HOUSING.png` |
| Box Plots | `box_plots_1_HOUSING.png`, `box_plots_2_HOUSING.png`, `box_plots_3_HOUSING.png` |
| Violin Plots | `violin_plots_1_HOUSING.png`, `violin_plots_2_HOUSING.png` |
| Correlations | `correlation_heatmap_HOUSING.png`, `growth_rate_heatmap_HOUSING.png` |
| Temporal | `temporal_distributions_HOUSING.png`, `yoy_change_1_HOUSING.png` |
| Housing-Specific | `rent_burden_HOUSING.png`, `owner_cost_burden_HOUSING.png` |
| Outliers | `outlier_detection_1_HOUSING.png`, `outlier_detection_2_HOUSING.png` |
| Anomalies | `temporal_anomalies_1_HOUSING.png`, `temporal_anomalies_2_HOUSING.png` |
| Ratios | `ratio_Gross_Rent_Household_Income_HOUSING.png` |

**Figure Path**: `figures/`

---

## Stage 8: LLM Analysis (Content Augmented Generation)

**Source**: `ml.py` → `LLMClient`, `LLMAnalyzer`

**Model Used**: `microsoft/phi-4-mini-reasoning Q8_0`
**Engine**: ROCm llama.cpp
**Hardware**: AMD RX 9060 XT
**Endpoint**: `http://localhost:1234/v1/chat/completions`

### What is CAG?

Content Augmented Generation combines:
1. **Statistical Results** - All metrics from stages 4-6
2. **State Context** - Economic, demographic, political, historical background
3. **Structured Prompts** - Specific analytical questions

### Live LLM Execution Trace

```
[VERBOSE] Starting LLM analysis with fallback handler...
[VERBOSE] Initializing LLM client and analyzer...
[VERBOSE] Running LLM analysis for state: South Carolina
[VERBOSE] State context loaded: South Carolina
[VERBOSE]   → Running LLM analysis: Temporal Trends
[PROMPT-VERBOSE] User prompt: 726 chars (~181 tokens)
[PROMPT-VERBOSE] Building system prompt...
[PROMPT-VERBOSE] Injecting state context for: South Carolina
[CONTEXT-VERBOSE] Formatted context length: 3989 chars
[CONTEXT-VERBOSE] Estimated tokens: ~997
[PROMPT-VERBOSE] Final system prompt: 8877 chars (~2219 tokens)
[API-VERBOSE] Total request: ~2400 tokens (system: ~2219, user: ~181)
[API-VERBOSE] Sending request to http://localhost:1234/v1/chat/completions
[API-VERBOSE] Received response: 10292 chars
[VERBOSE]   ✓ Temporal Trends analysis complete (10292 chars)
```

### Context Injection Architecture

The system prompt includes **8 context sections** for each state:

```
[CONTEXT-VERBOSE] Full context sections loaded:
  ✓ STATE-SPECIFIC CONTEXT: South Carolina
  ✓ ECONOMIC PROFILE:
  ✓ DEMOGRAPHIC PROFILE:
  ✓ HOUSING MARKET:
  ✓ POLITY:
  ✓ REGIONAL:
  ✓ HISTORICAL:
  ✓ COMPARATIVE:
```

### Token Budget Per Analysis

| Analysis Type | User Prompt | System Prompt | Total Request |
|---------------|-------------|---------------|---------------|
| Temporal Trends | ~181 tokens | ~2,219 tokens | ~2,400 tokens |
| Data Quality | ~302 tokens | ~2,219 tokens | ~2,521 tokens |
| Research Recommendations | ~319 tokens | ~2,219 tokens | ~2,538 tokens |
| Economic Analysis | ~304 tokens | ~2,219 tokens | ~2,523 tokens |
| Correlation Analysis | ~11 tokens | ~2,219 tokens | ~2,230 tokens |
| Statistical Analysis | ~2,381 tokens | ~2,219 tokens | ~4,600 tokens |
| Outlier Detection | ~1,418 tokens | ~2,219 tokens | ~3,637 tokens |
| Anomaly Detection | ~152 tokens | ~2,219 tokens | ~2,371 tokens |
| Trend Analysis | ~1,330 tokens | ~2,219 tokens | ~3,549 tokens |
| Deep Learning Analysis | ~619 tokens | ~2,219 tokens | ~2,838 tokens |

**Total**: 10/10 analyses succeeded, ~100K+ chars of LLM output

### State Context (South Carolina)

The LLM receives comprehensive state-specific context. Here's what gets injected (from actual log):

```
[CONTEXT-VERBOSE] Context preview (first 500 chars):
----------------------------------------------------------------------

STATE-SPECIFIC CONTEXT: South Carolina

ECONOMIC PROFILE:
  Industries: Advanced manufacturing (automotive, aerospace), Tourism and
  hospitality, Agriculture (poultry, cotton, soybeans), Textile and chemical
  manufacturing, Port operations and logistics

  Trends: Strong growth 2011-2019 driven by automotive manufacturing boom
  (BMW expansion, Mercedes, Volvo plants). Port of Charleston expansion.
  Tourism steady growth. Post-pandemic: rapid manufacturing recovery
  2021-2023, supply chain investments
----------------------------------------------------------------------
[CONTEXT-VERBOSE] ... (truncated, 3489 more chars)
```

**Full context structure:**

```json
{
  "state_name": "South Carolina",
  "region": "South",
  "division": "South Atlantic",
  "economic_profile": {
    "key_industries": [
      "Advanced manufacturing (automotive, aerospace)",
      "Tourism and hospitality",
      "Agriculture (poultry, cotton, soybeans)",
      "Port operations and logistics"
    ],
    "gdp_rank": "#26 nationally (~$273B in 2024)",
    "major_employers": ["BMW Manufacturing", "Boeing", "Michelin", "State government"],
    "economic_resilience": "Strong recovery 2011-2019 via manufacturing FDI"
  },
  "housing_context": {
    "market_characteristics": "Generally affordable. Coastal areas expensive. Charleston housing crisis.",
    "affordability_trends": "Affordable 2011-2019. Rapid appreciation 2020-2023.",
    "housing_challenges": ["Coastal appreciation pricing out locals", "Charleston affordability crisis"]
  },
  "political_context": {
    "policy_environment": "Business-friendly: right-to-work, low taxes, light regulation",
    "labor_policy": "Right-to-work state, $7.25 federal minimum wage"
  }
}
```

### LLM Output Sections (10 insight files)

| Section | File | Content |
|---------|------|---------|
| Data Quality | [12_llm_data_quality.md](../output/South_Carolina/housing/5-year/12_llm_data_quality.md) | Completeness, biases, limitations |
| Policy Recommendations | [13_llm_policy_recommendations.md](../output/South_Carolina/housing/5-year/13_llm_policy_recommendations.md) | Research questions, methods, implications |
| Temporal Insights | [14_llm_temporal_insights.md](../output/South_Carolina/housing/5-year/14_llm_temporal_insights.md) | Time-based patterns |
| Economic Insights | [15_llm_economic_insights.md](../output/South_Carolina/housing/5-year/15_llm_economic_insights.md) | Affordability, cost burdens |
| Correlation Insights | [16_llm_correlation_insights.md](../output/South_Carolina/housing/5-year/16_llm_correlation_insights.md) | Variable relationships |
| Statistical Insights | [17_llm_statistical_insights.md](../output/South_Carolina/housing/5-year/17_llm_statistical_insights.md) | Distribution interpretations |
| Outlier Insights | [18_llm_outlier_insights.md](../output/South_Carolina/housing/5-year/18_llm_outlier_insights.md) | Outlier explanations |
| Anomaly Insights | [19_llm_anomaly_insights.md](../output/South_Carolina/housing/5-year/19_llm_anomaly_insights.md) | Anomaly interpretations |
| Trend Insights | [20_llm_trend_insights.md](../output/South_Carolina/housing/5-year/20_llm_trend_insights.md) | Long-term pattern analysis |
| Deep Learning Insights | [21_llm_deep_learning_insights.md](../output/South_Carolina/housing/5-year/21_llm_deep_learning_insights.md) | DL model interpretations |

### Chain-of-Thought Reasoning

LLM outputs include full reasoning chains in `<think>` blocks:

```markdown
# AI-Generated Insights: Temporal Analysis

<think>
Okay, let's tackle this ACS census dataset temporal analysis. First, I need
to understand what the user is asking for. The data spans from 2011 to 2023,
which is 13 years...

Starting with the first question about evaluating data coverage completeness.
Since there are no missing years mentioned, that suggests the dataset has
complete yearly data from 2011 to 2023...

For South Carolina, the dominant sector is manufacturing with plants from BMW,
Mercedes, etc., so maybe a pattern of industrial growth post-recession...
</think>

## Comprehensive Temporal Analysis of the ACS Census Dataset (2011–2023)

### 1. Data Coverage Completeness
- **Observation**: The dataset spans 13 years (2011–2023) with no missing years
- **South Carolina Context**: This completeness allows longitudinal analysis of
  state-specific trends, such as manufacturing growth in the Upstate and tourism
  dynamics in coastal regions...
```

### Example: Economic Analysis Output

From [15_llm_economic_insights.md](../output/South_Carolina/housing/5-year/15_llm_economic_insights.md):

**Key Finding**: Owner cost burden decreased from 24% (2011) to 21% (2023)

**LLM Interpretation**:
> "Homeownership equity growth reduces debt pressure, while renters face slower
> wage gains compared to homeowners... Right-to-work laws might affect labor
> dynamics—limiting unionization which could impact wages."

**Policy Recommendation**:
> "Inclusionary Zoning Laws: Mandate affordable units in high-growth zones
> (Charleston/Upstate) to curb displacement."

---

## Stage 9: Report Generation

**Source**: `report.py` → `ReportGenerator`

Compiles all outputs into the final report structure:

```
output/South_Carolina/housing/5-year/
├── 00_table_of_contents.md      # Navigation index
├── 01_overview.md               # Dataset stats
├── 02_temporal_analysis.md      # Year distributions
├── 03_economic_analysis.md      # Housing economics
├── 04_statistical_analysis.md   # Summary statistics
├── 05_correlation_analysis.md   # Variable correlations
├── 06_cross_variable_analysis.md# Interactions
├── 07_outlier_detection.md      # Outlier rates
├── 08_anomaly_detection.md      # Temporal anomalies
├── 09_trend_analysis.md         # Long-term trends
├── 10_feature_engineering.md    # Created features
├── 11_ml_models.md              # ML results
├── 11b_deep_learning_models.md  # DL results
├── 12_llm_data_quality.md       # LLM: Data quality
├── 13_llm_policy_recommendations.md  # LLM: Policy
├── 14_llm_temporal_insights.md  # LLM: Temporal
├── 15_llm_economic_insights.md  # LLM: Economic
├── 16_llm_correlation_insights.md    # LLM: Correlations
├── 17_llm_statistical_insights.md    # LLM: Statistics
├── 18_llm_outlier_insights.md   # LLM: Outliers
├── 19_llm_anomaly_insights.md   # LLM: Anomalies
├── 20_llm_trend_insights.md     # LLM: Trends
├── 21_llm_deep_learning_insights.md  # LLM: DL
└── figures/                     # 221 visualizations
    ├── *.png                    # 50 base figures
    └── ml/                      # 171 ML/DL figures
        ├── regression/
        ├── clustering/
        ├── time_series/
        ├── deep_learning/
        └── model_comparison/
```

---

## What Makes This "Content Augmented Generation"?

| Traditional Analysis | CAG Enhancement |
|---------------------|-----------------|
| "Property values increased 55%" | "Property values increased 55%, driven by Charleston's tourism boom and BMW/Volvo manufacturing expansion in the Upstate corridor" |
| "Anomaly detected in 2020" | "Anomaly detected in 2020, consistent with COVID-19's differential impact on coastal tourism vs. manufacturing regions" |
| "Owner cost burden: 21%" | "Owner cost burden dropped from 24% to 21%, reflecting equity gains from rapid property appreciation; however, right-to-work policies may limit wage growth offsetting these gains for renters" |
| "Clustering found 5 segments" | "Cluster 3 represents coastal retiree communities with high property values but moderate incomes, reflecting the Hilton Head/Myrtle Beach migration pattern" |

**The LLM connects statistical findings to state-specific context to produce actionable insights.**

---

## Pipeline Completion

When everything succeeds, you see:

```
[VERBOSE] LLM analysis suite complete: 10/10 analyses succeeded
[VERBOSE] LLM analysis completed successfully
[REPORT] Generated: report_South_Carolina_housing_20251010_130731.txt
[SUCCESS] HOUSING (5-year) pipeline complete for South Carolina!

======================================================================
[COMPLETE] All processing finished!
======================================================================
```

---

## Running the Pipeline

```bash
# Single state, single survey
uv run main.py --states "South Carolina" --surveys housing --scopes 5-Year

# Full run (all states, all surveys, all scopes)
uv run main.py --all-states --all-scopes

# Check CLI options
uv run main.py --help
```

### Log Location

Logs are written to: `logs/{State}/{Scope}/{Survey}/`

Example: `logs/South Carolina/5-year/housing/5-year_housing_25_10_09_2027.log`

The log contains:
- Data loading progress
- Memory sampling decisions
- ML/DL training progress
- LLM prompt/response details
- All warnings and errors

---

## Appendix: Full State Context Schema

See [pipeline.md](./pipeline.md) for the complete South Carolina context JSON used in CAG prompts.

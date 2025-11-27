# Census ACS Exploratory Data Analysis (by State)
Early exploration using Context Augmented Generation (CAG) to bridge the gap between statistical metrics and lived reality


**Educational Use Disclaimer**

*EDUCATIONAL AND RESEARCH PURPOSES ONLY*: ***This repository and its contents are provided solely for educational, academic research, and learning purposes. The data, scripts, analyses, and any outputs are intended to demonstrate data analysis techniques and Census data exploration methods. Users are responsible for ensuring their use of Census data complies with all applicable terms of service, usage restrictions, and legal requirements. This project is not affiliated with, endorsed by, or representative of the U.S. Census Bureau. Always refer to official Census Bureau sources for authoritative data and interpretations.***


**Data Accuracy & No Warranty**

*NO WARRANTY*: ***This repository is provided "as is" without warranty of any kind, express or implied. The authors make no guarantees regarding the accuracy, completeness, or reliability of any data, scripts, or analyses. Users assume all responsibility for verifying data accuracy and appropriateness for their intended use. Census data contains sampling and non-sampling errors - always consult official documentation and use appropriate statistical methods.***
This repository contains Exploratory Data Analysis (EDA) for Census ACS organized by State/Survey-Type/Survey-Scope
- **State**: 50 US States plus District of Columbia, Puerto Rico
- **Survey-Type**: housing, population
- **Survey-Scope**: 1-Year, 5-Year

***Data Availability Note***: Only 2007–2024 ACS data is evaluated
##  So What? 
### REVISITING UPDATE  
AI is fascinating as it provides the unique ability as it provides I/O for combinations of structured, unstructured, and multidimensional data into a shared output — an output that is only possible with a Large Language model. What does this mean? In most econometric models, you get amazing insights, understanding, and ability to quantify XYZ. Integration of LLM's adds elements of sentiment analysis, 'emotion', and interpretation that do not exist in traditional econometric models. With this, new insights are provided that can potentially bridge the infamous 'Economic Model' from the 'Reality' gap. Traditional econometrics give us the skeleton; LLMs add the nervous system. Now, we finally see the full organism.

**The Result**: We can finally explain why GDP says "growth" while people feel "recession"
**The Vision**: Democratizing economic analysis so policymakers see what people feel, not just what models measure.
 
#### Example Insight

Ohio 2023: Traditional metrics show +55% income growth.
LLM analysis reveals: Underlying anxiety about gig economy instability.
Result: Policy recommendations that address actual, not statistical, problems.

```markdown
This isn't just about better economic analysis.
It's about who controls the tools to understand our world.

Today: You need millions to analyze economies at scale.
Tomorrow: You need $400 and this framework.

Today: "Truth" comes from centralized models you can't inspect.
Tomorrow: Truth comes from local models you control.

This is computational democracy in action.
The revolution will be locally computed.
```

## Highlights
### LLM Powered Analysis
Large Language Model Integration (LLM) to help with large scale data analytics (Exploratory Data Analysis, Data Visualization, Data Modeling, etc.)
**Optimized Responses**: Generating at runtime an extended unique context providing additional instructions, background knowledge, and contextual information.
### Deep Exploration Patterns
Large quantity of repeated analysis, processing, visualization, and modeling patterns across a plethora of states/survey-types/survey-scopes.
### Next Steps
0) Blueprints for the next steps are generated for distinct topics/subjects; this comes as a result of diverse analysis, processing, visualization, and modeling patterns, in tandem with LLM interpretation.
1) Making the Silver Layer: The cleaned, organized, coalescing of data from multiple sources into Iceberg Tables—addressing observed data quality issues from bronze while 'starting to unify' data across multiple sources ([Apache Iceberg](https://github.com/apache/iceberg))
2) Making the Gold Layer: A certified, analytics-ready Gold Medallion layer — curated, de-duplicated, and tensor-ready slices of vast diversity of economic data that power repeatable modeling, visualizations, and decisioning. ([Icechunk](https://github.com/earth-mover/icechunk))


## Documents
1) [Quick Start](./docs/quick_start.md)
2) [Pipeline Example](./docs/pipeline.md) : Breaking down the pipeline with an example and explaining Context Augmented Generation  
3) [Claude Pipeline CAG](./docs/claude_pipeline.md): How CAG extends beyond just the pipeline. I had Claude Opus 4.5 (claude-opus-4-5-20251101) mirror me putting (2) together but instructed Agent to utilize the log output (*NOTE*: I truncated the epochs from the log to allow Agent to fully 'read' the log) to create/refine the pipeline example
4) [Hardware Recommendations](./docs/hardware.md) : Showcasing miscellaneous examples of hardware 'to make this happen'
5) [General Usage](./docs/general_usage.md): General Usage


## Appendix
### Privacy & Confidentiality
**PROTECT PRIVACY**: While ACS PUMAS data is anonymized and disclosure-protected by the Census Bureau, users must:
- Never attempt to re-identify individuals or households in the data
- Handle data responsibly and ethically
- Comply with all data use agreements and privacy regulations
- Be aware that combining datasets may create re-identification risks



### Ethical Server Use
**RESPECTFUL DATA COLLECTION**: When using the download scripts:
- Implement reasonable rate limiting (wait times included in scripts)
- Cache data locally and avoid redundant downloads
- Do not overwhelm Census Bureau servers
- Use during off-peak hours when possible
- The scripts include `--wait=2 --random-wait` to be respectful of server resources




import pandas as pd
import requests
from typing import Dict, List, Tuple, Optional, Any
from config import Config
import warnings
import json
from pathlib import Path
from exceptions import (LLMConnectionError, LLMTimeoutError, LLMResponseError,
                        LLMParsingError, InsufficientDataError)
from logging_config import get_logger

logger = get_logger("ml")

warnings.filterwarnings('ignore')


# ============================================================================
# STATE CONTEXT LOADER
# ============================================================================

class StateContextLoader:
    """Loads and manages state-specific historical/political/economic context"""

    def __init__(self, context_file: str = "state_context.json"):
        # If relative path, make it relative to this file's directory
        if not Path(context_file).is_absolute():
            context_file = Path(__file__).parent / context_file
        self.context_file = Path(context_file)
        self.state_contexts = self._load_contexts()

    def _load_contexts(self) -> Dict:
        """Load state context from JSON file"""
        if self.context_file.exists():
            with open(self.context_file, 'r') as f:
                return json.load(f)
        return {}

    def get_state_context(self, state: str) -> Dict:
        """Get context for specific state - handles both FIPS codes and state names"""
        # First, try direct lookup (for FIPS codes like "DE", "AL")
        if state.upper() in self.state_contexts:
            return self.state_contexts[state.upper()]

        # If not found, try to map state name to FIPS code
        state_to_fips = self._get_state_name_to_fips_map()
        fips_code = state_to_fips.get(state.upper())
        if fips_code:
            return self.state_contexts.get(fips_code, {})

        return {}

    def _get_state_name_to_fips_map(self) -> Dict[str, str]:
        """Build reverse map from state names to FIPS codes"""
        name_to_fips = {}
        for fips_code, context in self.state_contexts.items():
            if isinstance(context, dict) and 'state_name' in context:
                state_name = context['state_name'].upper()
                name_to_fips[state_name] = fips_code
        return name_to_fips

    def format_state_context(self, state: str) -> str:
        """Format state context for prompt injection - FULL integration"""
        context = self.get_state_context(state)
        if not context:
            logger.warning(f"[CONTEXT] No context available for state: {state}")
            return f"STATE: {state} (No additional context available)"

        logger.debug(f"[CONTEXT] Loading context for state: {state}")
        sections = [f"\nSTATE-SPECIFIC CONTEXT: {state}"]
        sections.append(self._format_economic(context))
        sections.append(self._format_demographic(context))
        sections.append(self._format_housing(context))
        sections.append(self._format_political(context))
        sections.append(self._format_regional(context))
        sections.append(self._format_historical(context))
        sections.append(self._format_comparative(context))
        formatted = "\n".join([s for s in sections if s])
        self._log_formatted_context(formatted)
        return formatted

    def _log_formatted_context(self, formatted: str):
        """Log the formatted context for validation"""
        logger.debug(f"[CONTEXT] Formatted context length: {len(formatted)} chars")
        logger.debug(f"[CONTEXT] Estimated tokens: ~{len(formatted) // 4}")
        logger.debug("[CONTEXT] Context preview:")
        logger.debug("-" * 70)
        logger.debug(formatted)
        logger.debug("-" * 70)
        logger.debug("[CONTEXT] Full context sections loaded:")
        for line in formatted.split('\n'):
            if line.strip() and ':' in line and not line.startswith('  '):
                logger.debug(f"[CONTEXT]   ✓ {line.strip()}")

    def _format_economic(self, context: Dict) -> str:
        econ = context.get('economic_profile', {})
        if not econ:
            return ""
        lines = ["\nECONOMIC PROFILE:"]
        if econ.get('key_industries'):
            lines.append(f"  Industries: {', '.join(econ['key_industries'])}")
        if econ.get('economic_trends'):
            lines.append(f"  Trends: {econ['economic_trends']}")
        if econ.get('income_characteristics'):
            lines.append(f"  Income: {econ['income_characteristics']}")
        if econ.get('employment_sectors', {}).get('dominant'):
            lines.append(f"  Dominant Sector: {econ['employment_sectors']['dominant']}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_demographic(self, context: Dict) -> str:
        demo = context.get('demographic_profile', {})
        if not demo:
            return ""
        lines = ["\nDEMOGRAPHIC PROFILE:"]
        if demo.get('population_trends'):
            lines.append(f"  Trends: {demo['population_trends']}")
        if demo.get('migration_patterns'):
            lines.append(f"  Migration: {demo['migration_patterns']}")
        if demo.get('education_levels'):
            lines.append(f"  Education: {demo['education_levels']}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_housing(self, context: Dict) -> str:
        housing = context.get('housing_context', {})
        if not housing:
            return ""
        lines = ["\nHOUSING MARKET:"]
        if housing.get('market_characteristics'):
            lines.append(f"  Market: {housing['market_characteristics']}")
        if housing.get('affordability_trends'):
            lines.append(f"  Affordability: {housing['affordability_trends']}")
        if housing.get('housing_challenges'):
            lines.append(f"  Challenges: {', '.join(housing['housing_challenges'])}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_political(self, context: Dict) -> str:
        pol = context.get('political_context', {})
        if not pol:
            return ""
        lines = ["\nPOLITY:"]
        if pol.get('policy_environment'):
            lines.append(f"  Policy: {pol['policy_environment']}")
        if pol.get('housing_policy'):
            lines.append(f"  Housing: {pol['housing_policy']}")
        if pol.get('labor_policy'):
            lines.append(f"  Labor: {pol['labor_policy']}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_regional(self, context: Dict) -> str:
        reg = context.get('regional_characteristics', {})
        if not reg:
            return ""
        lines = ["\nREGIONAL:"]
        if reg.get('geography'):
            lines.append(f"  Geography: {reg['geography']}")
        if reg.get('urban_rural_mix'):
            lines.append(f"  Urban/Rural: {reg['urban_rural_mix']}")
        if reg.get('infrastructure'):
            lines.append(f"  Infrastructure: {reg['infrastructure']}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_historical(self, context: Dict) -> str:
        hist = context.get('historical_context', {})
        if not hist:
            return ""
        lines = ["\nHISTORICAL:"]
        if hist.get('major_events'):
            lines.append(f"  Events: {'; '.join(hist['major_events'])}")
        if hist.get('economic_shocks'):
            lines.append(f"  Shocks: {hist['economic_shocks']}")
        if hist.get('industry_transitions'):
            lines.append(f"  Transitions: {hist['industry_transitions']}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_comparative(self, context: Dict) -> str:
        comp = context.get('comparative_context', {})
        if not comp:
            return ""
        lines = ["\nCOMPARATIVE:"]
        if comp.get('national_benchmarks'):
            lines.append(f"  Benchmarks: {comp['national_benchmarks']}")
        if comp.get('peer_states'):
            lines.append(f"  Peer States: {', '.join(comp['peer_states'])}")
        if comp.get('unique_factors'):
            lines.append(f"  Unique: {comp['unique_factors']}")
        return "\n".join(lines) if len(lines) > 1 else ""


# ============================================================================
# LLM CLIENT (Optimized for LM Server)
# ============================================================================

class LLMClient:
    """Handles LLM API calls - optimized for Meta-Llama-3.1-8B-Instruct"""

    def __init__(self, config: Config, state_context_loader: Optional[StateContextLoader] = None):
        self.config = config
        self.state_context_loader = state_context_loader or StateContextLoader()
        self.current_state = None

        # LM Server optimized settings for 8B quantized model
        self.max_context = 50000  # Leave buffer for extended context
        self.chunk_size = 20000  # Optimal chunk for extended context

    def set_state(self, state: str):
        """Set current state for context injection"""
        self.current_state = state

    def analyze(self, prompt: str, analysis_type: str = "general") -> Optional[str]:
        logger.info(f"[LLM] Running analysis: {analysis_type}")

        # Log user prompt details
        user_tokens = self._estimate_tokens(prompt)
        logger.debug(f"[LLM] User prompt: {len(prompt)} chars (~{user_tokens} tokens)")

        # Check if prompt needs chunking
        if user_tokens > self.chunk_size:
            logger.warning(f"[LLM] Large prompt detected, using chunked approach")
            response = self._analyze_chunked(prompt, analysis_type)
        else:
            response = self._call_api(prompt)

        if response:
            logger.info(f"[LLM] {analysis_type} analysis complete ({len(response)} chars)")
            return response
        logger.warning(f"[LLM] {analysis_type} analysis failed (LLM unavailable or timed out)")
        return None

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars for English)"""
        return len(text) // 4

    def _analyze_chunked(self, prompt: str, analysis_type: str) -> Optional[str]:
        """Handle large prompts by chunking (for edge cases)"""
        # For now, truncate - can implement proper chunking if needed
       # truncated = prompt[:self.chunk_size * 4]  # Convert back to chars
       # print(f"[VERBOSE]   ⚠ Truncating prompt to fit context window")
        return self._call_api(truncated)

    def _call_api(self, prompt: str) -> Optional[str]:
        try:
            payload = self._build_payload(prompt)

            # Log total token count
            system_tokens = self._estimate_tokens(payload['messages'][0]['content'])
            user_tokens = self._estimate_tokens(payload['messages'][1]['content'])
            total_tokens = system_tokens + user_tokens
            logger.debug(f"[API] Total request: ~{total_tokens} tokens (system: ~{system_tokens}, user: ~{user_tokens})")

            if total_tokens > self.max_context:
                logger.warning(f"[API] Request exceeds max context ({total_tokens} > {self.max_context})")

            logger.debug(f"[API] Sending request to {self.config.llm_url}/v1/chat/completions")
            response = requests.post(
                f"{self.config.llm_url}/v1/chat/completions",  # Explicit endpoint
                json=payload,
                timeout=1200  # Significantly increased for larger/slower model
            )
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
            logger.debug(f"[API] Received response: {len(result)} chars")
            return result
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[API] Connection failed: LM Studio not running on {self.config.llm_url}")
            return None
        except requests.exceptions.Timeout:
            logger.error(f"[API] Request timeout (>1200s)")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"[API] HTTP error: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"[API] Malformed response: {e}")
            return None
        except Exception as e:
            logger.error(f"[API] Unexpected error: {e}")
            return None

    def _build_payload(self, prompt: str) -> Dict:
        """Build optimized payload for Meta-Llama-3.1-8B-Instruct"""

        # Build system prompt with state context if available
        system_prompt = self._build_system_prompt()

        # Optimized parameters for 8B quantized model
        return {
            "model": self.config.llm_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.config.llm_temp,
            "max_tokens": self.config.llm_max_tokens,
            # Additional parameters optimized for Llama 3.1
            "top_p": 0.9,  # Nucleus sampling for better coherence
            "frequency_penalty": 0.1,  # Reduce repetition
            "presence_penalty": 0.1,  # Encourage topic diversity
            "stop": ["</analysis>", "\n\nUser:", "\n\nHuman:"]  # Clean stops
        }

    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with state context"""
        logger.debug("[PROMPT] Building system prompt...")

        base_prompt = """You are an expert census data analyst with deep expertise in socioeconomic research, policy analysis, and state-level comparative economics. You have access to comprehensive state-specific context and must use it extensively in your analysis.

DATA CONTEXT:
You are analyzing aggregated state-level data derived from U.S. Census Bureau Public Use Microdata Areas (PUMAs). PUMAs are non-overlapping statistical geographic areas that divide each state into regions typically containing about 100,000 residents. They enable the release of Public Use Microdata Sample (PUMS) data from the American Community Survey (ACS) while protecting respondent privacy.

The data comes from ACS 1-year estimates (for larger populations, offering more current but less precise data) and 5-year estimates (for smaller areas, providing more reliable averages over time). Key metrics include:
- Population demographics: Age distribution, sex, race/ethnicity, household size, migration patterns
- Housing characteristics: Occupancy rates, tenure (owner vs. renter), structure type, housing value/rent, year built
- Economic indicators: Median household income, poverty rates, employment status, industry/occupation, commuting patterns
- Other social metrics: Education attainment, health insurance coverage, disability status, family structure

CRITICAL TEMPORAL FOCUS:
Focus on data from 2007-2023. Briefly mention impact of any  MISSINGS YEARS but do not factor into remainder of your analysis. The COVID-19 pandemic caused significant disruptions in data collection (lower response rates, sampling biases) and economic anomalies (lockdowns, unemployment spikes, supply chain failures), making it unreliable for trend analysis or comparisons.

NATIONAL ECONOMIC CONTEXT (2011-2023, excluding 2020):
- 2011-2019 (Post-Great Recession Recovery): Steady GDP growth (~2.2% annually), unemployment fell from 9% to under 4%, strong job gains in services/healthcare/technology. Challenges included slower wage growth for lower-income groups, rising income inequality, regional disparities (urban vs. rural), and housing affordability issues in high-demand areas.
- 2021-2023: Post-pandemic recovery with varying patterns across sectors and regions. Monitor for pandemic impacts on employment, housing markets, remote work trends, and income distribution shifts.

REASONING REQUIREMENTS:
You are a reasoning model. For each analysis:
1. **THINK STEP-BY-STEP**: Break down complex patterns into logical components
2. **ESTABLISH CAUSALITY**: Identify cause-and-effect relationships between state context and observed data patterns
3. **REASON FROM FIRST PRINCIPLES**: Connect specific state characteristics (industries, policies, geography) to economic/demographic outcomes
4. **COMPARATIVE REASONING**: Systematically compare this state to peer states and national benchmarks
5. **SYNTHESIZE EVIDENCE**: Integrate multiple data sources with contextual knowledge for comprehensive insights"""

        # Inject state-specific context if available
        if self.current_state and self.state_context_loader:
            logger.debug(f"[PROMPT] Injecting state context for: {self.current_state}")
            state_context = self.state_context_loader.format_state_context(self.current_state)
            base_prompt += f"\n\n{state_context}"
            logger.debug(f"[PROMPT] State context injected ({len(state_context)} chars)")
        else:
            logger.debug("[PROMPT] No state context to inject")

        base_prompt += """

MANDATORY CONTEXT INTEGRATION:
**YOU MUST ACTIVELY USE THE STATE-SPECIFIC CONTEXT PROVIDED ABOVE**

For EVERY analysis, you must:
1. **CITE SPECIFIC STATE CONTEXT**: Explicitly reference industries, policies, events, demographics, or characteristics from the state context
2. **EXPLAIN CONNECTIONS**: Show how observed data patterns relate to state's economic profile, political environment, historical events, or geographic characteristics
3. **LEVERAGE COMPARATIVE DATA**: Reference peer states and national benchmarks provided in context
4. **CONTEXTUALIZE TRENDS**: Explain whether trends are expected/unexpected given state-specific factors
5. **INFORM RECOMMENDATIONS**: Tailor policy suggestions to state's political environment, regulatory stance, and economic structure

RESPONSE FORMAT & LENGTH:
- **MINIMUM 500 WORDS, TARGET 800+ words** per analysis (you have 50k token context - use it!)
- Structure with clear markdown headers (##, ###)
- Use numbered lists for key findings (at least 5-7 points)
- Include a "State Context Integration" section showing explicit connections
- Provide detailed, specific insights with quantitative support
- Include comprehensive policy recommendations (3-5 actionable items)
- Add "Evidence Synthesis" section connecting multiple data points

REASONING APPROACH:
1. **Initial Observations**: State what you see in the data
2. **Contextual Interpretation**: Explain WHY based on state context
3. **Causal Analysis**: Identify likely drivers (economic, political, demographic)
4. **Comparative Positioning**: Where does this state stand relative to peers?
5. **Forward-Looking Implications**: What does this mean for future trends?
6. **Actionable Insights**: What should policymakers/researchers do?

CRITICAL: Generic analysis without state context citations is UNACCEPTABLE. Every paragraph should demonstrate awareness of state-specific factors. Show your reasoning process."""

        prompt_len = len(base_prompt)
        token_estimate = prompt_len // 4
        logger.debug(f"[PROMPT] Final system prompt: {prompt_len} chars (~{token_estimate} tokens)")
        if token_estimate > 3000:
            logger.warning(f"[PROMPT] System prompt is large ({token_estimate} tokens), may reduce user prompt space")

        return base_prompt


# ============================================================================
# LLM ANALYZER (Enhanced with State Context)
# ============================================================================

class LLMAnalyzer:
    """Orchestrates LLM analysis with state-specific context"""

    def __init__(self, client: LLMClient):
        self.client = client

    def run_analysis(self, df: pd.DataFrame, temporal: Dict,
                     state: Optional[str] = None,
                     economic: Dict = None, correlations: Dict = None,
                     statistics: Dict = None, outliers: Dict = None,
                     anomalies: Dict = None, trends: Dict = None,
                     deep_learning: Dict = None,
                     feature_engineering: Dict = None,
                     disability: Dict = None,
                     health_insurance: Dict = None,
                     occupation_industry: Dict = None,
                     education_field: Dict = None) -> Dict[str, str]:
        logger.info("[LLM] Starting LLM analysis suite...")

        # Set state context
        if state:
            self.client.set_state(state)
            logger.info(f"[LLM] State context loaded: {state}")

        results = {}

        # Core analyses (always run)
        results['temporal_insights'] = self._temporal_prompt(temporal)
        results['data_quality'] = self._quality_prompt(df)
        results['recommendations'] = self._recommendations_prompt(df, temporal, feature_engineering)

        # Optional analyses (run if data available)
        if economic:
            results['economic_analysis'] = self._economic_prompt(economic)
        if correlations:
            results['correlation_insights'] = self._correlation_prompt(correlations)
        if statistics:
            results['statistical_analysis'] = self._statistics_prompt(statistics)
        if outliers:
            results['outlier_analysis'] = self._outlier_prompt(outliers)
        if anomalies:
            results['anomaly_detection'] = self._anomaly_prompt(anomalies)
        if trends:
            results['trend_analysis'] = self._trend_prompt(trends)
        if deep_learning:
            results['deep_learning_insights'] = self._deep_learning_prompt(deep_learning)
        if feature_engineering and feature_engineering.get('features_created'):
            results['feature_engineering_insights'] = self._feature_engineering_prompt(feature_engineering)

        # New domain-specific analyses
        if disability:
            results['disability_analysis'] = self._disability_prompt(disability)
        if health_insurance:
            results['health_insurance_analysis'] = self._health_insurance_prompt(health_insurance)
        if occupation_industry:
            results['occupation_industry_analysis'] = self._occupation_industry_prompt(occupation_industry)
        if education_field:
            results['education_field_analysis'] = self._education_field_prompt(education_field)

        completed = sum(1 for v in results.values() if v)
        logger.info(f"[LLM] LLM analysis suite complete: {completed}/{len(results)} analyses succeeded")
        return results

    def _temporal_prompt(self, temporal: Dict) -> str:
        """Generate comprehensive temporal analysis prompt"""
        patterns = temporal.get('temporal_patterns', {})
        growth = temporal.get('growth_rates', {})

        sections = ["Analyze the temporal characteristics of this ACS census dataset:\n"]

        sections.append("TEMPORAL COVERAGE:")
        sections.append(f"Years Covered: {patterns.get('years_covered', 'N/A')}")
        sections.append(f"Year Range: {patterns.get('year_range', 'N/A')}")
        sections.append(f"Missing Years: {patterns.get('missing_years', 'None') or 'None'}")
        sections.append(f"Data Span: {patterns.get('year_span', 'N/A')} years\n")

        sections.append("SAMPLE SIZE TRENDS:")
        sections.append(f"Sample Growth Rate: {growth.get('sample_growth', 'N/A')}%")
        avg_records = growth.get('avg_records_per_year', 'N/A')
        avg_records_str = f"{avg_records:,.0f}" if isinstance(avg_records, (int, float)) else str(avg_records)
        sections.append(f"Records per Year: {avg_records_str} (average)")
        if growth.get('min_year'):
            sections.append(f"Smallest Sample: {growth.get('min_year')} ({growth.get('min_records', 0):,} records)")
        if growth.get('max_year'):
            sections.append(f"Largest Sample: {growth.get('max_year')} ({growth.get('max_records', 0):,} records)")

        sections.append("\n\nPROVIDE COMPREHENSIVE TEMPORAL ANALYSIS:")
        sections.append("1. Evaluate data coverage completeness - are there concerning gaps or missing years?")
        sections.append("2. Analyze sample size trends - is growth consistent or are there anomalies?")
        sections.append("3. Assess data reliability across years - which periods have strongest/weakest coverage?")
        sections.append("4. Identify 3 key temporal patterns and their research implications")
        sections.append("5. What cautions should researchers take when analyzing trends across these years?")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Temporal Trends")

    def _quality_prompt(self, df: pd.DataFrame) -> str:
        """Generate comprehensive data quality assessment prompt"""
        missing_pct = (df.isna().sum() / len(df) * 100)
        top_missing = missing_pct.nlargest(10)
        overall_missing = missing_pct.mean()
        complete_vars = (missing_pct == 0).sum()

        sections = ["Assess the data quality of this ACS census dataset:\n"]

        sections.append("DATASET DIMENSIONS:")
        sections.append(f"Total Records: {len(df):,}")
        sections.append(f"Total Variables: {len(df.columns)}")
        sections.append(f"Complete Variables (0% missing): {complete_vars}/{len(df.columns)}\n")

        sections.append("MISSING DATA ANALYSIS:")
        sections.append(f"Overall Missing Rate: {overall_missing:.2f}%")
        sections.append(f"\nTop 10 Variables with Missing Data:")
        for var, pct in top_missing.items():
            sections.append(f"  - {var}: {pct:.1f}% missing")

        # Data types summary
        numeric_cols = len(df.select_dtypes(include=['number']).columns)
        object_cols = len(df.select_dtypes(include=['object']).columns)
        sections.append(f"\nDATA TYPES:")
        sections.append(f"Numeric Variables: {numeric_cols}")
        sections.append(f"Categorical Variables: {object_cols}")

        sections.append("\n\nPROVIDE COMPREHENSIVE QUALITY ASSESSMENT:")
        sections.append("1. Evaluate overall data completeness - is this dataset suitable for robust analysis?")
        sections.append("2. Identify critical variables with concerning missing rates - what are the implications?")
        sections.append("3. Assess whether missing patterns suggest systematic issues or random gaps")
        sections.append("4. What imputation strategies would be appropriate for key variables?")
        sections.append("5. Provide 3 specific recommendations for improving data quality or handling missing values")
        sections.append("6. Which analyses would be compromised by current missing data patterns?")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Data Quality")

    def _recommendations_prompt(self, df: pd.DataFrame, temporal: Dict,
                                 feature_engineering: Dict = None) -> str:
        """Generate comprehensive research recommendations prompt"""
        patterns = temporal.get('temporal_patterns', {})

        # Identify key variable categories
        numeric_vars = df.select_dtypes(include=['number']).columns.tolist()
        income_vars = [v for v in numeric_vars if 'Income' in v or 'Wage' in v]
        housing_vars = [v for v in numeric_vars if 'Value' in v or 'Rent' in v or 'Bedroom' in v]
        demographic_vars = [v for v in df.columns if 'Age' in v or 'Sex' in v or 'Race' in v]

        sections = ["Develop research recommendations for this ACS census dataset:\n"]

        sections.append("DATASET CHARACTERISTICS:")
        sections.append(f"Sample Size: {len(df):,} records")
        sections.append(f"Temporal Coverage: {patterns.get('years_covered', 'N/A')} years")
        sections.append(f"Year Range: {patterns.get('year_range', 'N/A')}")
        sections.append(f"Total Variables: {len(df.columns)}\n")

        sections.append("KEY VARIABLE CATEGORIES:")
        if income_vars:
            sections.append(f"Economic/Income: {', '.join(income_vars)}")
        if housing_vars:
            sections.append(f"Housing: {', '.join(housing_vars)}")
        if demographic_vars:
            sections.append(f"Demographics: {', '.join(demographic_vars)}")

        # Include engineered features if available
        if feature_engineering:
            features = feature_engineering.get('features_created', [])
            if features:
                sections.append(f"Engineered Features: {', '.join(features)}")
        sections.append("")

        sections.append("PROVIDE STRATEGIC RESEARCH RECOMMENDATIONS:")
        sections.append("1. Identify 3 high-impact research questions this dataset can answer")
        sections.append("2. For each question, specify:")
        sections.append("   - Key variables to analyze")
        sections.append("   - Appropriate analytical methods")
        sections.append("   - Expected policy implications")
        sections.append("3. What longitudinal analyses are enabled by the temporal coverage?")
        sections.append("4. Which cross-sectional comparisons would yield valuable insights?")
        sections.append("5. Recommend 3 specific visualizations that would best communicate findings")
        sections.append("6. Identify any methodological challenges or limitations researchers should address")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Research Recommendations")

    def _feature_engineering_prompt(self, feature_engineering: Dict) -> str:
        """Generate feature engineering analysis prompt"""
        features = feature_engineering.get('features_created', [])
        transforms = feature_engineering.get('transformations', [])
        cleaning = feature_engineering.get('cleaning', {})

        sections = ["Analyze the feature engineering applied to this ACS census dataset:\n"]

        sections.append("ENGINEERED FEATURES:")
        if features:
            for feat in features:
                sections.append(f"  - {feat}")
        else:
            sections.append("  No derived features were created.")
        sections.append("")

        sections.append("TRANSFORMATIONS APPLIED:")
        if transforms:
            for trans in transforms:
                sections.append(f"  - {trans}")
        else:
            sections.append("  No transformations were applied.")
        sections.append("")

        if cleaning:
            rows_before = cleaning.get('rows_before', 0)
            rows_after = cleaning.get('rows_after', 0)
            sections.append("DATA CLEANING IMPACT:")
            sections.append(f"  Records processed: {rows_before:,} → {rows_after:,}")
            sections.append("")

        sections.append("PROVIDE FEATURE ENGINEERING ANALYSIS:")
        sections.append("1. Evaluate the appropriateness of each engineered feature")
        sections.append("2. How do these features enhance analytical capability?")
        sections.append("3. What additional features could be derived from the raw data?")
        sections.append("4. Are there any potential issues with the transformations applied?")
        sections.append("5. Recommend feature engineering improvements for future analyses")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Feature Engineering")

    def _economic_prompt(self, economic: Dict) -> str:
        """Generate comprehensive economic analysis prompt"""
        housing = economic.get('housing', {})
        population = economic.get('population', {})
        prompt = self._build_economic_prompt(housing, population)
        return self.client.analyze(prompt, "Economic Analysis")

    def _build_economic_prompt(self, housing: Dict, population: Dict) -> str:
        """Build detailed economic analysis prompt"""
        sections = ["Analyze socioeconomic trends in this census data:\n"]

        # Housing economics
        if housing:
            sections.append("HOUSING MARKET INDICATORS:")
            sections.append(self._format_housing_data(housing))
            sections.append("")

        # Population economics
        if population:
            sections.append("INCOME & EMPLOYMENT INDICATORS:")
            sections.append(self._format_population_data(population))
            sections.append("")

        sections.append("PROVIDE COMPREHENSIVE ECONOMIC ANALYSIS:")
        sections.append("1. Identify the 3 most significant economic trends and their trajectory")
        sections.append("2. Assess affordability and cost burden patterns - what populations are most affected?")
        sections.append("3. Evaluate income distribution and employment trends - signs of inequality or improvement?")
        sections.append("4. Analyze housing market dynamics - are property values and rents moving in tandem?")
        sections.append("5. What policy interventions are suggested by these economic patterns?")
        sections.append("6. Compare trends to national/regional benchmarks - is this area outperforming or lagging?")
        sections.append("7. Identify 3 actionable recommendations for policymakers based on these economic indicators")

        return "\n".join(sections)

    def _format_housing_data(self, housing: Dict) -> str:
        props = housing.get('property_values', {})
        rental = housing.get('rental_market', {})
        afford = housing.get('affordability', {})
        return f"""HOUSING ECONOMICS:
- Property Values: {self._format_trend(props.get('median_value_trend', {}))}
- Rental Market: {self._format_trend(rental.get('median_rent_trend', {}))}
- Owner Cost Burden: {self._format_trend(afford.get('owner_cost_burden', {}))}
- Renter Cost Burden: {self._format_trend(afford.get('renter_cost_burden', {}))}"""

    def _format_population_data(self, population: Dict) -> str:
        income = population.get('income', {})
        employ = population.get('employment', {})
        wages = population.get('wages', {})
        return f"""POPULATION ECONOMICS:
- Median Income: {self._format_trend(income.get('median_person_income', {}))}
- Median Wages: {self._format_trend(wages.get('median_wage_trend', {}))}
- Avg Hours Worked: {self._format_trend(employ.get('avg_hours_worked', {}))}"""

    def _format_trend(self, trend_data: Dict, limit: int = 3) -> str:
        if not trend_data:
            return "N/A"
        items = list(trend_data.items())
        return ", ".join([f"{k}: {v:.0f}" for k, v in items if v])

    def _correlation_prompt(self, correlations: Dict) -> str:
        """Generate comprehensive correlation analysis prompt"""
        strong = correlations.get('strong_correlations', [])
        prompt = self._build_correlation_prompt(strong, correlations)
        return self.client.analyze(prompt, "Correlation Analysis")

    def _build_correlation_prompt(self, strong_corr: List, correlations: Dict) -> str:
        """Build detailed correlation analysis prompt"""
        if not strong_corr:
            return "No strong correlations detected in the dataset."

        sections = ["Analyze correlation patterns in this census dataset:\n"]

        sections.append(f"STRONG CORRELATIONS DETECTED (|r| > 0.7): {len(strong_corr)} pairs\n")

        # Positive correlations
        positive = [c for c in strong_corr if c[2] > 0]
        if positive:
            sections.append("STRONG POSITIVE CORRELATIONS:")
            for var1, var2, r in positive:
                sections.append(f"  - {var1} <-> {var2}: r = {r:.3f}")
            sections.append("")

        # Negative correlations
        negative = [c for c in strong_corr if c[2] < 0]
        if negative:
            sections.append("STRONG NEGATIVE CORRELATIONS:")
            for var1, var2, r in negative:
                sections.append(f"  - {var1} <-> {var2}: r = {r:.3f}")
            sections.append("")

        sections.append("PROVIDE COMPREHENSIVE CORRELATION INTERPRETATION:")
        sections.append("1. Explain the top 3 strongest correlations - what do they reveal about relationships?")
        sections.append("2. Identify which correlations are expected vs. surprising - why?")
        sections.append("3. Distinguish between likely causal relationships vs. spurious correlations")
        sections.append("4. What do negative correlations suggest about trade-offs or inverse relationships?")
        sections.append("5. Which correlations have important policy implications?")
        sections.append("6. Recommend 3 follow-up analyses to explore these relationships further")
        sections.append("7. Identify any missing correlations that would be expected but aren't present")

        return "\n".join(sections)

    def _statistics_prompt(self, statistics: Dict) -> str:
        """Generate comprehensive statistical analysis prompt"""
        summary_stats = statistics.get('summary_statistics', {})
        overall = statistics.get('overall_metrics', {})
        dist_analysis = statistics.get('distribution_analysis', {})

        prompt = self._build_statistics_prompt(summary_stats, overall, dist_analysis)
        return self.client.analyze(prompt, "Statistical Analysis")

    def _build_statistics_prompt(self, summary_stats: Dict, overall: Dict,
                                 dist_analysis: Dict) -> str:
        """Build detailed statistical prompt with robust metrics"""
        sections = ["Analyze the following comprehensive statistical summary of census data:\n"]

        # Overall metrics
        sections.append("DATASET OVERVIEW:")
        sections.append(f"Total Variables Analyzed: {overall.get('total_variables', 'N/A')}")
        sections.append(f"Total Observations: {overall.get('total_observations', 'N/A'):,}")
        sections.append(f"Average Missing Rate: {overall.get('avg_missing_rate', 0):.2f}%\n")

        # High variance variables
        high_var = overall.get('highly_variable_vars', [])
        if high_var:
            sections.append("HIGH VARIABILITY VARIABLES (CV > 100%):")
            for var, cv in high_var:
                sections.append(f"  - {var}: CV = {cv:.1f}%")
            sections.append("")

        # Distribution characteristics
        if dist_analysis:
            sections.append("DISTRIBUTION CHARACTERISTICS:")
            if dist_analysis.get('normal_distributions'):
                sections.append(f"  Normal: {', '.join(dist_analysis['normal_distributions'])}")
            if dist_analysis.get('skewed_right'):
                sections.append(f"  Right-Skewed: {', '.join(dist_analysis['skewed_right'])}")
            if dist_analysis.get('skewed_left'):
                sections.append(f"  Left-Skewed: {', '.join(dist_analysis['skewed_left'])}")
            if dist_analysis.get('heavy_tailed'):
                sections.append(f"  Heavy-Tailed: {', '.join(dist_analysis['heavy_tailed'])}")
            sections.append("")

        # Detailed statistics for key variables (top 5)
        sections.append("DETAILED SUMMARY STATISTICS (Top 5 Variables):")
        for idx, (var_name, stats) in enumerate(list(summary_stats.items()), 1):
            if 'error' in stats:
                continue

            sections.append(f"\n{idx}. {var_name}:")
            sections.append(f"   Count: {stats.get('count', 'N/A'):,}")
            sections.append(f"   Mean: {stats.get('mean', 0):,.2f}")
            sections.append(f"   Median: {stats.get('median', 0):,.2f}")
            sections.append(f"   Std Dev: {stats.get('std_dev', 0):,.2f}")
            sections.append(f"   Variance: {stats.get('variance', 0):,.2f}")
            sections.append(f"   Skewness: {stats.get('skewness', 0):.3f}")
            sections.append(f"   Kurtosis: {stats.get('kurtosis', 0):.3f}")
            sections.append(f"   Range: [{stats.get('min', 0):,.0f} to {stats.get('max', 0):,.0f}]")
            sections.append(f"   IQR: [{stats.get('q25', 0):,.0f} to {stats.get('q75', 0):,.0f}]")

        sections.append("\n\nPROVIDE A ROBUST ANALYSIS:")
        sections.append("1. Interpret the MEAN vs MEDIAN for each variable - what does the difference suggest?")
        sections.append(
            "2. Explain the SKEWNESS values - are distributions symmetric or skewed? What are the implications?")
        sections.append("3. Interpret KURTOSIS - are there heavy tails or outliers in the distributions?")
        sections.append("4. Discuss VARIANCE/STD DEV - which variables show high dispersion and why?")
        sections.append("5. Provide 3 key insights about the overall data characteristics and quality.")

        return "\n".join(sections)

    def _outlier_prompt(self, outliers: Dict) -> str:
        """Generate outlier analysis prompt"""
        outlier_stats = outliers.get('outlier_statistics', {})
        high_outlier_vars = outliers.get('high_outlier_vars', [])
        outlier_counts = outliers.get('outlier_counts', {})

        sections = ["Analyze outlier patterns in this census dataset:\n"]

        # Overall outlier statistics
        sections.append("OVERALL OUTLIER STATISTICS:")
        sections.append(f"Average Outlier Percentage: {outlier_stats.get('avg_outlier_percentage', 0):.2f}%")
        sections.append(f"Maximum Outlier Percentage: {outlier_stats.get('max_outlier_percentage', 0):.2f}%")
        sections.append(
            f"Variables with Outliers: {outlier_stats.get('vars_with_outliers', 0)}/{outlier_stats.get('total_vars_analyzed', 0)}\n")

        # High outlier variables
        if high_outlier_vars:
            sections.append("VARIABLES WITH HIGH OUTLIER RATES (>5%):")
            for var, pct in high_outlier_vars:
                sections.append(f"  - {var}: {pct:.1f}% outliers")
            sections.append("")

        # Detailed outlier info for top 3 variables
        sections.append("DETAILED OUTLIER ANALYSIS (Top 3 Variables):")
        for idx, (var, data) in enumerate(list(outlier_counts.items()), 1):
            if 'error' in data:
                continue
            sections.append(f"\n{idx}. {var}:")
            sections.append(f"   Total Observations: {data.get('total_count', 0):,}")
            sections.append(
                f"   Outliers Detected: {data.get('outlier_count', 0):,} ({data.get('outlier_percentage', 0):.1f}%)")
            sections.append(f"   IQR Bounds: [{data.get('lower_bound', 0):,.0f}, {data.get('upper_bound', 0):,.0f}]")
            if data.get('max_outlier'):
                sections.append(
                    f"   Outlier Range: [{data.get('min_outlier', 0):,.0f}, {data.get('max_outlier', 0):,.0f}]")

        sections.append("\n\nPROVIDE COMPREHENSIVE INTERPRETATION:")
        sections.append("1. What do the outlier patterns suggest about data quality and extreme values?")
        sections.append("2. Which variables have unexpectedly high outlier rates and why might this be?")
        sections.append("3. Are the outliers likely data errors or legitimate extreme observations? Explain.")
        sections.append("4. What implications do these outliers have for statistical analysis and policy decisions?")
        sections.append("5. Recommend 3 specific actions for handling or investigating these outliers.")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Outlier Detection")

    def _anomaly_prompt(self, anomalies: Dict) -> str:
        """Generate anomaly detection prompt"""
        anomaly_years = anomalies.get('anomaly_years', {})
        total_anomalies = anomalies.get('total_anomalies', 0)

        sections = ["Analyze temporal anomalies detected in census data:\n"]

        sections.append(f"TOTAL ANOMALIES DETECTED: {total_anomalies}\n")

        # List anomalies by variable
        if anomaly_years:
            sections.append("ANOMALIES BY VARIABLE:")
            for var, var_anomalies in list(anomaly_years.items()):
                anomaly_list = var_anomalies.get('anomaly_years', [])
                if anomaly_list:
                    sections.append(f"\n{var}:")
                    for anom in anomaly_list:
                        sections.append(
                            f"  - Year {anom['year']}: Value={anom['value']:,.0f}, Expected={anom['expected']:,.0f}, Deviation={anom['deviation']:,.0f}")
        else:
            sections.append("No significant temporal anomalies detected.")

        sections.append("\n\nPROVIDE IN-DEPTH ANALYSIS:")
        sections.append("1. What historical events or policy changes might explain these temporal anomalies?")
        sections.append("2. Are the anomalies concentrated in specific years? What was happening during those periods?")
        sections.append("3. Which variables show the most unusual temporal patterns and why?")
        sections.append("4. Could these anomalies represent data collection issues or genuine socioeconomic shifts?")
        sections.append("5. What are the implications for trend analysis and forecasting?")
        sections.append("6. Provide 3 recommendations for further investigation of these anomalies.")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Anomaly Detection")

    def _trend_prompt(self, trends: Dict) -> str:
        """Generate trend analysis prompt"""
        trend_analysis = trends.get('trend_analysis', {})
        strong_trends = trends.get('strong_trends', [])
        trend_directions = trends.get('trend_directions', {})

        sections = ["Analyze long-term trends in census data:\n"]

        # Strong trends
        if strong_trends:
            sections.append("STRONG TRENDS DETECTED (R² > 0.7):")
            for var, r2, direction in strong_trends:
                sections.append(f"  - {var}: {direction.upper()} (R² = {r2:.3f})")
            sections.append("")

        # Trend categorization
        sections.append("TREND CATEGORIZATION:")
        if trend_directions.get('strong_increasing'):
            sections.append(f"  Strong Increasing: {', '.join(trend_directions['strong_increasing'])}")
        if trend_directions.get('strong_decreasing'):
            sections.append(f"  Strong Decreasing: {', '.join(trend_directions['strong_decreasing'])}")
        if trend_directions.get('moderate_increasing'):
            sections.append(f"  Moderate Increasing: {', '.join(trend_directions['moderate_increasing'])}")
        if trend_directions.get('moderate_decreasing'):
            sections.append(f"  Moderate Decreasing: {', '.join(trend_directions['moderate_decreasing'])}")
        if trend_directions.get('weak_or_flat'):
            sections.append(f"  Weak/Flat: {', '.join(trend_directions['weak_or_flat'])}")
        sections.append("")

        # Detailed trend analysis for top variables
        sections.append("DETAILED TREND METRICS (Top 5 Variables):")
        for idx, (var, data) in enumerate(list(trend_analysis.items()), 1):
            if 'error' in data:
                continue
            sections.append(f"\n{idx}. {var}:")
            sections.append(f"   Direction: {data.get('direction', 'N/A').upper()}")
            sections.append(f"   Trend Strength: {data.get('trend_strength', 'N/A').upper()}")
            sections.append(f"   R-squared: {data.get('r_squared', 0):.3f}")
            sections.append(f"   Overall % Change: {data.get('percent_change', 0):+.1f}%")
            sections.append(f"   Years Analyzed: {data.get('years_analyzed', 0)}")

        sections.append("\n\nPROVIDE COMPREHENSIVE TREND INTERPRETATION:")
        sections.append("1. What are the most significant trends and what do they reveal about socioeconomic changes?")
        sections.append("2. Are increasing and decreasing trends balanced, or is there a dominant pattern?")
        sections.append("3. Which trends are most likely to continue vs. reverse? Explain your reasoning.")
        sections.append("4. What policy interventions might be suggested by these trend patterns?")
        sections.append("5. How do these trends compare to national/regional economic patterns?")
        sections.append("6. Identify 3 variables where trend reversal would have major societal impact.")
        sections.append("7. Provide 3 forecasting insights based on these trend analyses.")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Trend Analysis")

    def _deep_learning_prompt(self, deep_learning: Dict) -> str:
        """Generate comprehensive deep learning analysis prompt"""
        sections = ["Analyze deep learning model performance and insights:\n"]
        sections.append("DEEP LEARNING MODELS TRAINED:")
        sections.append(self._format_dl_tasks(deep_learning))
        sections.append("\nMODEL PERFORMANCE METRICS:")
        sections.append(self._format_dl_metrics(deep_learning))
        sections.append("\nPROVIDE COMPREHENSIVE DEEP LEARNING INSIGHTS:")
        sections.append("1. Compare neural network performance to traditional ML - advantages/limitations?")
        sections.append("2. Which target predictions show strongest performance and why?")
        sections.append("3. Analyze overfitting risk - validation vs training loss gaps")
        sections.append("4. Interpret R² scores - which relationships are well-captured by neural nets?")
        sections.append("5. Recommend architectural improvements or alternative approaches")
        sections.append("6. Discuss computational efficiency vs accuracy tradeoffs")
        sections.append("7. Identify 3 actionable insights from deep learning results")
        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Deep Learning Analysis")

    def _format_dl_tasks(self, dl_results: Dict) -> str:
        """Format deep learning task summary with architecture (≤10 lines)"""
        lines = []
        for task_name, result in dl_results.items():
            targets = ", ".join(result.targets)
            #if len(result.targets) > 3:
            #    targets += f" (+{len(result.targets)-3} more)"
            lines.append(f"  - {task_name}: {result.model_type} ({result.task_type})")
            lines.append(f"    Targets: {targets}")
            lines.append(f"    Architecture: {result.architecture.get('layers', 'N/A')} layers, "
                        f"{result.architecture.get('params', 'N/A'):,} parameters")
            features = result.metadata.get('features', [])
            lines.append(f"    Features Used: {len(features)} features")
        return "\n".join(lines)

    def _format_dl_metrics(self, dl_results: Dict) -> str:
        """Format deep learning metrics with convergence analysis (≤10 lines)"""
        lines = []
        for task_name, result in dl_results.items():
            lines.append(f"\n{task_name.upper()}:")
            for metric, value in result.test_metrics.items():
                lines.append(f"  {metric.upper()}: {value:.4f}")
            lines.append(f"  Train Loss: {result.train_loss:.4f}")
            lines.append(f"  Val Loss: {result.val_loss:.4f}")
            overfitting_gap = result.val_loss - result.train_loss
            lines.append(f"  Overfit Gap: {overfitting_gap:.4f} "
                        f"({'HIGH RISK' if overfitting_gap > 0.5 else 'LOW'})")
            epochs_trained = len(result.history.get('loss', []))
            lines.append(f"  Epochs Trained: {epochs_trained}")
        return "\n".join(lines)

    def _disability_prompt(self, disability: Dict) -> str:
        """Generate comprehensive disability analysis prompt"""
        prevalence = disability.get('prevalence', {})
        types = disability.get('disability_types', {})
        employment = disability.get('employment_gap', {})
        income = disability.get('income_gap', {})
        trends = disability.get('trends', {})

        sections = ["Analyze disability patterns and socioeconomic impacts in this census data:\n"]

        # Overall prevalence
        sections.append("DISABILITY PREVALENCE:")
        sections.append(f"Overall Disability Rate: {prevalence.get('overall_rate', 'N/A')}%")
        sections.append(f"Population with Disability: {prevalence.get('count', 'N/A'):,}")
        sections.append("")

        # Disability types
        if types:
            sections.append("DISABILITY TYPE BREAKDOWN:")
            for dis_type, rate in types.items():
                sections.append(f"  - {dis_type}: {rate:.2f}%")
            sections.append("")

        # Employment gaps
        if employment:
            sections.append("EMPLOYMENT GAP ANALYSIS:")
            sections.append(f"Employment Rate (Disabled): {employment.get('disabled_employment_rate', 'N/A')}%")
            sections.append(f"Employment Rate (Non-Disabled): {employment.get('non_disabled_employment_rate', 'N/A')}%")
            sections.append(f"Employment Gap: {employment.get('employment_gap', 'N/A')} percentage points")
            sections.append("")

        # Income gaps
        if income:
            sections.append("INCOME DISPARITY:")
            sections.append(f"Median Income (Disabled): ${income.get('disabled_median_income', 0):,.0f}")
            sections.append(f"Median Income (Non-Disabled): ${income.get('non_disabled_median_income', 0):,.0f}")
            sections.append(f"Income Gap: {income.get('income_gap_percent', 0):.1f}%")
            sections.append("")

        # Trends
        if trends:
            sections.append("TEMPORAL TRENDS:")
            for year, rate in list(trends.items())[:5]:
                sections.append(f"  - {year}: {rate:.2f}%")
            sections.append("")

        sections.append("PROVIDE COMPREHENSIVE DISABILITY ANALYSIS:")
        sections.append("1. Analyze disability prevalence patterns - are rates consistent with national averages?")
        sections.append("2. Identify which disability types are most prevalent and potential underlying causes")
        sections.append("3. Assess employment barriers for disabled individuals - what factors contribute to the gap?")
        sections.append("4. Evaluate income disparities - how does disability impact economic well-being?")
        sections.append("5. Connect disability patterns to state-specific factors (industries, healthcare access, policies)")
        sections.append("6. Identify vulnerable subpopulations (e.g., disabled elderly, working-age disabled)")
        sections.append("7. Recommend 3-5 policy interventions to improve disability employment and income outcomes")
        sections.append("8. Discuss accessibility, accommodation, and support service implications")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Disability Analysis")

    def _health_insurance_prompt(self, health_insurance: Dict) -> str:
        """Generate comprehensive health insurance analysis prompt"""
        coverage = health_insurance.get('coverage', {})
        insurance_types = health_insurance.get('insurance_types', {})
        uninsured = health_insurance.get('uninsured', {})
        demographics = health_insurance.get('demographic_breakdown', {})
        trends = health_insurance.get('trends', {})

        sections = ["Analyze health insurance coverage patterns in this census data:\n"]

        # Overall coverage
        sections.append("OVERALL COVERAGE:")
        sections.append(f"Insured Rate: {coverage.get('insured_rate', 'N/A')}%")
        sections.append(f"Uninsured Rate: {coverage.get('uninsured_rate', 'N/A')}%")
        sections.append(f"Uninsured Count: {coverage.get('uninsured_count', 'N/A'):,}")
        sections.append("")

        # Insurance types
        if insurance_types:
            sections.append("INSURANCE TYPE BREAKDOWN:")
            sections.append(f"  - Employer-Sponsored: {insurance_types.get('employer', 'N/A')}%")
            sections.append(f"  - Direct Purchase: {insurance_types.get('direct', 'N/A')}%")
            sections.append(f"  - Medicare: {insurance_types.get('medicare', 'N/A')}%")
            sections.append(f"  - Medicaid: {insurance_types.get('medicaid', 'N/A')}%")
            sections.append(f"  - VA/Military: {insurance_types.get('military', 'N/A')}%")
            sections.append("")

        # Uninsured demographics
        if demographics:
            sections.append("UNINSURED BY DEMOGRAPHICS:")
            if demographics.get('by_age'):
                sections.append("  By Age Group:")
                for age_group, rate in demographics['by_age'].items():
                    sections.append(f"    - {age_group}: {rate:.1f}% uninsured")
            if demographics.get('by_income'):
                sections.append("  By Income Level:")
                for income_level, rate in demographics['by_income'].items():
                    sections.append(f"    - {income_level}: {rate:.1f}% uninsured")
            if demographics.get('by_employment'):
                sections.append("  By Employment Status:")
                for emp_status, rate in demographics['by_employment'].items():
                    sections.append(f"    - {emp_status}: {rate:.1f}% uninsured")
            sections.append("")

        # Trends
        if trends:
            sections.append("COVERAGE TRENDS:")
            for year, rate in list(trends.items()):
                sections.append(f"  - {year}: {rate:.1f}% uninsured")
            sections.append("")

        sections.append("PROVIDE COMPREHENSIVE HEALTH INSURANCE ANALYSIS:")
        sections.append("1. Evaluate overall coverage adequacy - how does this compare to national/state benchmarks?")
        sections.append("2. Analyze the insurance type mix - is there over-reliance on particular coverage sources?")
        sections.append("3. Identify the most vulnerable uninsured populations and contributing factors")
        sections.append("4. Assess geographic and demographic disparities in coverage")
        sections.append("5. Connect coverage patterns to state policies (Medicaid expansion, ACA marketplace, etc.)")
        sections.append("6. Analyze public vs. private insurance trends and implications")
        sections.append("7. Recommend 3-5 policy interventions to expand coverage and reduce disparities")
        sections.append("8. Discuss healthcare access implications for uninsured populations")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Health Insurance Analysis")

    def _occupation_industry_prompt(self, occupation_industry: Dict) -> str:
        """Generate comprehensive occupation and industry analysis prompt"""
        industries = occupation_industry.get('top_industries', {})
        occupations = occupation_industry.get('top_occupations', {})
        wage_premium = occupation_industry.get('wage_premium', {})
        trends = occupation_industry.get('industry_trends', {})
        demographics = occupation_industry.get('demographic_patterns', {})

        sections = ["Analyze occupation and industry patterns in this census data:\n"]

        # Top industries
        if industries:
            sections.append("TOP INDUSTRIES BY EMPLOYMENT:")
            for industry, data in list(industries.items()):
                pct = data.get('percentage', 0) if isinstance(data, dict) else data
                sections.append(f"  - {industry}: {pct:.1f}%")
            sections.append("")

        # Top occupations
        if occupations:
            sections.append("TOP OCCUPATIONS BY COUNT:")
            for occupation, data in list(occupations.items()):
                pct = data.get('percentage', 0) if isinstance(data, dict) else data
                sections.append(f"  - {occupation}: {pct:.1f}%")
            sections.append("")

        # Wage premiums
        if wage_premium:
            sections.append("WAGE PREMIUM/DISCOUNT BY INDUSTRY:")
            for industry, premium in sorted(wage_premium.items(), key=lambda x: x[1], reverse=True)[:10]:
                sign = "+" if premium > 0 else ""
                sections.append(f"  - {industry}: {sign}{premium:.1f}%")
            sections.append("")

        # Industry trends
        if trends:
            sections.append("INDUSTRY EMPLOYMENT TRENDS:")
            for industry, trend_data in list(trends.items()):
                if isinstance(trend_data, dict):
                    direction = trend_data.get('direction', 'stable')
                    change = trend_data.get('change', 0)
                    sections.append(f"  - {industry}: {direction.upper()} ({change:+.1f}%)")
            sections.append("")

        # Demographics
        if demographics:
            if demographics.get('by_sex'):
                sections.append("OCCUPATIONAL SEX DISTRIBUTION:")
                for occ, sex_data in list(demographics['by_sex'].items()):
                    male_pct = sex_data.get('male', 50)
                    sections.append(f"  - {occ}: {male_pct:.0f}% male / {100-male_pct:.0f}% female")
                sections.append("")

        sections.append("PROVIDE COMPREHENSIVE OCCUPATION/INDUSTRY ANALYSIS:")
        sections.append("1. Characterize the economic base - what industries drive employment?")
        sections.append("2. Identify high-wage vs. low-wage industry patterns and implications")
        sections.append("3. Analyze occupational segregation by sex/demographics - what patterns emerge?")
        sections.append("4. Assess industry diversification - is the economy vulnerable to sector-specific shocks?")
        sections.append("5. Connect industry patterns to state-specific factors (resources, location, policies)")
        sections.append("6. Evaluate emerging vs. declining industries and workforce implications")
        sections.append("7. Analyze skill requirements and education-occupation alignment")
        sections.append("8. Recommend 3-5 workforce development and economic policy priorities")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Occupation/Industry Analysis")

    def _education_field_prompt(self, education_field: Dict) -> str:
        """Generate comprehensive education field analysis prompt"""
        stem = education_field.get('stem_analysis', {})
        top_fields = education_field.get('top_fields', {})
        income_by_field = education_field.get('income_by_field', {})
        trends = education_field.get('field_trends', {})
        demographics = education_field.get('demographic_patterns', {})

        sections = ["Analyze field of degree patterns in this census data:\n"]

        # STEM analysis
        if stem:
            sections.append("STEM DEGREE ANALYSIS:")
            sections.append(f"STEM Degree Rate: {stem.get('stem_rate', 'N/A')}%")
            sections.append(f"STEM-Related Rate: {stem.get('stem_related_rate', 'N/A')}%")
            sections.append(f"Non-STEM Rate: {stem.get('non_stem_rate', 'N/A')}%")
            sections.append(f"STEM Income Premium: {stem.get('income_premium', 'N/A')}%")
            sections.append("")

        # Top fields
        if top_fields:
            sections.append("TOP FIELDS OF DEGREE:")
            for field, data in list(top_fields.items()):
                pct = data.get('percentage', 0) if isinstance(data, dict) else data
                sections.append(f"  - {field}: {pct:.1f}%")
            sections.append("")

        # Income by field
        if income_by_field:
            sections.append("MEDIAN INCOME BY FIELD:")
            sorted_fields = sorted(income_by_field.items(), key=lambda x: x[1], reverse=True)
            for field, income in sorted_fields:
                sections.append(f"  - {field}: ${income:,.0f}")
            sections.append("")

        # Field trends
        if trends:
            sections.append("FIELD OF DEGREE TRENDS:")
            for field, trend_data in list(trends.items()):
                if isinstance(trend_data, dict):
                    direction = trend_data.get('direction', 'stable')
                    sections.append(f"  - {field}: {direction.upper()}")
            sections.append("")

        # Demographics
        if demographics:
            if demographics.get('stem_by_sex'):
                sections.append("STEM BY SEX:")
                male_stem = demographics['stem_by_sex'].get('male', 50)
                sections.append(f"  - Male STEM rate: {male_stem:.1f}%")
                sections.append(f"  - Female STEM rate: {100-male_stem:.1f}%")
                sections.append("")

        sections.append("PROVIDE COMPREHENSIVE EDUCATION FIELD ANALYSIS:")
        sections.append("1. Evaluate STEM representation - how does this compare to state/national workforce needs?")
        sections.append("2. Analyze the STEM income premium - is it justified by productivity/demand differences?")
        sections.append("3. Identify gender disparities in field selection and their economic implications")
        sections.append("4. Assess alignment between degree fields and local industry demands")
        sections.append("5. Connect education patterns to state economic development strategies")
        sections.append("6. Evaluate trends in field selection - which fields are growing/declining?")
        sections.append("7. Analyze the role of higher education in workforce development")
        sections.append("8. Recommend 3-5 education and workforce policy interventions")

        prompt = "\n".join(sections)
        return self.client.analyze(prompt, "Education Field Analysis")
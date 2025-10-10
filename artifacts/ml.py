import pandas as pd
import requests
from typing import Dict, List, Tuple, Optional, Any
from config import Config
import warnings
import json
from pathlib import Path
from exceptions import (LLMConnectionError, LLMTimeoutError, LLMResponseError,
                        LLMParsingError, InsufficientDataError)

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
            print(f"[CONTEXT-WARN] No context available for state: {state}")
            return f"STATE: {state} (No additional context available)"

        print(f"[CONTEXT-VERBOSE] Loading context for state: {state}")
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
        print(f"[CONTEXT-VERBOSE] Formatted context length: {len(formatted)} chars")
        print(f"[CONTEXT-VERBOSE] Estimated tokens: ~{len(formatted) // 4}")
        print("[CONTEXT-VERBOSE] Context preview (first 500 chars):")
        print("-" * 70)
        print(formatted[:500])
        print("-" * 70)
        if len(formatted) > 500:
            print(f"[CONTEXT-VERBOSE] ... (truncated, {len(formatted) - 500} more chars)")
        print("[CONTEXT-VERBOSE] Full context sections loaded:")
        for line in formatted.split('\n'):
            if line.strip() and ':' in line and not line.startswith('  '):
                print(f"[CONTEXT-VERBOSE]   ✓ {line.strip()}")

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
        print(f"[VERBOSE]   → Running LLM analysis: {analysis_type}")

        # Log user prompt details
        user_tokens = self._estimate_tokens(prompt)
        print(f"[PROMPT-VERBOSE] User prompt: {len(prompt)} chars (~{user_tokens} tokens)")

        # Check if prompt needs chunking
        if user_tokens > self.chunk_size:
            print(f"[VERBOSE]   ⚠ Large prompt detected, using chunked approach")
            response = self._analyze_chunked(prompt, analysis_type)
        else:
            response = self._call_api(prompt)

        if response:
            print(f"[VERBOSE]   ✓ {analysis_type} analysis complete ({len(response)} chars)")
            return response
        print(f"[VERBOSE]   ✗ {analysis_type} analysis failed (LLM unavailable or timed out)")
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
            print(f"[API-VERBOSE] Total request: ~{total_tokens} tokens (system: ~{system_tokens}, user: ~{user_tokens})")

            if total_tokens > self.max_context:
                print(f"[API-WARN] Request exceeds max context ({total_tokens} > {self.max_context})")

            print(f"[API-VERBOSE] Sending request to {self.config.llm_url}/v1/chat/completions")
            response = requests.post(
                f"{self.config.llm_url}/v1/chat/completions",  # Explicit endpoint
                json=payload,
                timeout=1200  # Significantly increased for larger/slower model
            )
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
            print(f"[API-VERBOSE] Received response: {len(result)} chars")
            return result
        except requests.exceptions.ConnectionError as e:
            print(f"[API-ERROR] Connection failed: LM Studio not running on {self.config.llm_url}")
            return None
        except requests.exceptions.Timeout:
            print(f"[API-ERROR] Request timeout (>1200s)")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"[API-ERROR] HTTP error: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"[API-ERROR] Malformed response: {e}")
            return None
        except Exception as e:
            print(f"[API-ERROR] Unexpected error: {e}")
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
        print("[PROMPT-VERBOSE] Building system prompt...")

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
            print(f"[PROMPT-VERBOSE] Injecting state context for: {self.current_state}")
            state_context = self.state_context_loader.format_state_context(self.current_state)
            base_prompt += f"\n\n{state_context}"
            print(f"[PROMPT-VERBOSE] State context injected ({len(state_context)} chars)")
        else:
            print("[PROMPT-VERBOSE] No state context to inject")

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
        print(f"[PROMPT-VERBOSE] Final system prompt: {prompt_len} chars (~{token_estimate} tokens)")
        if token_estimate > 3000:
            print(f"[PROMPT-WARN] System prompt is large ({token_estimate} tokens), may reduce user prompt space")

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
                     deep_learning: Dict = None) -> Dict[str, str]:
        print("[VERBOSE] Starting LLM analysis suite...")

        # Set state context
        if state:
            self.client.set_state(state)
            print(f"[VERBOSE] State context loaded: {state}")

        results = {}

        # Core analyses (always run)
        results['temporal_insights'] = self._temporal_prompt(temporal)
        results['data_quality'] = self._quality_prompt(df)
        results['recommendations'] = self._recommendations_prompt(df, temporal)

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

        completed = sum(1 for v in results.values() if v)
        print(f"[VERBOSE] LLM analysis suite complete: {completed}/{len(results)} analyses succeeded")
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

    def _recommendations_prompt(self, df: pd.DataFrame, temporal: Dict) -> str:
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
            targets = ", ".join(result.targets[:3])
            if len(result.targets) > 3:
                targets += f" (+{len(result.targets)-3} more)"
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
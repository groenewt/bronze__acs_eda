# Usage Guidelines & Best Practices

## Before You Begin

### Prerequisites
- [ ] Read the [ACS_OVERVIEW.md](ACS_OVERVIEW.md) to understand the data
- [ ] Review [LICENSE.md](LICENSE.md) for licensing information
- [ ] Ensure you have sufficient disk space (compressed: ~XXX GB, uncompressed: ~XXX GB)
- [ ] Verify you have required tools installed: `bash`, `curl`, `wget`, `unzip`
- [ ] Check Census Bureau server status and planned maintenance

### Required Reading
1. **ACS PUMS Documentation**: https://www.census.gov/programs-surveys/acs/technical-documentation/pums.html
2. **Data Dictionaries**: Year-specific documentation for variable definitions
3. **Accuracy Statement**: Understand margins of error and data quality

## Using the Download Script

### Initial Configuration
Before running the script, review and modify these settings:

```bash
# Set your base directory
BASE_DOWNLOAD_DIR="/data/temp/census"  # Adjust to your needs

# Set your year range
YEAR_START=2007  # Earliest year you need
YEAR_END=2024    # Latest year you need

# Select states (remove states you don't need)
declare -A STATES_TO_GET=(
    ["29"]="MO"  # Missouri
    # ... add only the states you need
)
```

### Best Practices for Downloads

#### 1. Start Small
```bash
# Test with a single state and year first
YEAR_START=2023
YEAR_END=2023
# Keep only one state in STATES_TO_GET array
```

#### 2. Download During Off-Peak Hours
- **Best time**: Evenings/weekends in U.S. Eastern Time
- **Avoid**: Business hours (9 AM - 5 PM ET) when possible
- **Check**: Census Bureau maintenance schedules

#### 3. Monitor Progress
```bash
# Create a log file
./download_script.sh 2>&1 | tee download_$(date +%Y%m%d_%H%M%S).log
```

#### 4. Handle Interruptions
The script includes:
- Skip logic for already-downloaded files
- Retry mechanisms (`--tries=5`)
- Wait periods (`--wait=2 --random-wait`)

If interrupted, simply re-run the script - it will resume where it left off.

#### 5. Verify Downloads
```bash
# Check for corrupted zip files
find "${BASE_DOWNLOAD_DIR}/zips" -name "*.zip" -exec zip -T {} \; 2>&1 | grep -i error

# Count expected vs. actual files
# Expected per state/year: 4 files (2 survey types × 2 scopes)
```

### Server Etiquette

**DO:**
- ✅ Use the built-in wait times and random delays
- ✅ Download complete datasets once and cache locally
- ✅ Spread large downloads over multiple days if possible
- ✅ Use official Census Bureau APIs when available
- ✅ Report issues to Census Bureau if servers seem down

**DON'T:**
- ❌ Remove wait times from the script
- ❌ Run multiple parallel download processes
- ❌ Re-download files unnecessarily
- ❌ Ignore rate limits or throttling responses
- ❌ Use the script for commercial scraping operations

## Working with the Data

### File Organization
The script creates this structure:
```
/data/temp/census/
├── zips/
│   └── acs/
│       ├── housing/
│       │   ├── 1-Year/
│       │   │   └── [FIPS]/
│       │   │       └── [YEAR]/
│       │   │           └── csv_h[state].zip
│       │   └── 5-Year/
│       └── population/
│           ├── 1-Year/
│           └── 5-Year/
└── raw/
    └── acs/
        └── [extracted files]
```

### Data Processing Pipeline

#### Step 1: Extraction (Included in Script)
The script automatically extracts zip files to the `raw/` directory.

#### Step 2: Data Validation
```bash
# Verify extracted files
find "${BASE_RAW_DIR}" -name "*.csv" -exec wc -l {} \; | awk '{sum+=$1} END {print "Total rows:", sum}'

# Check for empty files
find "${BASE_RAW_DIR}" -name "*.csv" -size 0
```

#### Step 3: Quality Checks
Before analysis:
1. **Check headers**: Verify column names match data dictionary
2. **Spot check data**: Review sample records for anomalies
3. **Validate weights**: Ensure weight variables are present and non-zero
4. **Check for updates**: Compare with Census Bureau errata

### Analysis Best Practices

#### Always Use Weights
```python
# Example: Python/Pandas
import pandas as pd

# Read data
df = pd.read_csv('psam_pMO.csv')

# For population estimates, use PWGTP (person weight)
total_population = df['PWGTP'].sum()

# For housing estimates, use WGTP (housing weight)
# Read housing file
hdf = pd.read_csv('psam_hMO.csv')
total_housing_units = hdf['WGTP'].sum()
```

#### Calculate Standard Errors
```python
# Use replicate weights (PWGTP1-PWGTP80) for variance estimation
# Implement Successive Difference Replication (SDR) method
# See ACS PUMS documentation for formulas
```

#### Report Margins of Error
Always include margins of error (MOE) in your results:
- For estimates at 90% confidence level
- Following Census Bureau calculation methods
- Using appropriate standard error formulas

## Common Issues & Solutions

### Issue: "No such file or directory"
**Solution**: Check file paths and ensure extraction completed successfully.

### Issue: Out of Disk Space
**Solution**: 
- Delete zip files after extraction
- Process states in batches
- Use compressed file formats for analysis

### Issue: Different Column Names Across Years
**Solution**: 
- Use year-specific data dictionaries
- Create crosswalk/mapping for consistent variable names
- Document any harmonization steps

### Issue: Missing Values
**Solution**:
- Understand Census Bureau coding (e.g., -1, 0, NA)
- Check data dictionary for special codes
- Use appropriate imputation methods if needed

### Issue: Slow Processing
**Solution**:
- Use columnar formats (Parquet, Feather)
- Implement chunked reading
- Consider distributed computing (Spark, Dask)
- Filter to needed columns early

## Data Security & Privacy

### Storage
- Store data on secure systems
- Implement appropriate access controls
- Back up important derived datasets
- Document data lineage

### Sharing
- Share aggregated results, not microdata
- Apply cell suppression rules (Census Bureau guidelines)
- Never share potentially re-identifiable combinations
- Use secure transfer methods

### Disposal
- Securely delete data when no longer needed
- Follow institutional data retention policies
- Clear temporary files and caches

## Getting Help

### Documentation Resources
1. Census Bureau technical documentation
2. ACS PUMS User Guide
3. Data dictionary for your specific year
4. Census Bureau YouTube channel

### Support Channels
- **ACS Questions**: acso.users.support@census.gov
- **Technical Issues**: Census Bureau contact page
- **Community**: Census Data Users Google Group, Stack Overflow

### Repository Maintainer
[Add your contact information or contribution guidelines]

## Contributing

If you find issues or have improvements:
1. Document the problem/enhancement clearly
2. Test your changes thoroughly
3. Update documentation as needed
4. Follow ethical data practices

---

**Remember**: The goal is to produce high-quality, reproducible research while respecting data providers and protecting individual privacy.

**Last Updated**: October 2025
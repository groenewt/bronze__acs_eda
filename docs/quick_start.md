# Quick Start Guide

These scripts are oriented around a Unix machine. If on Windows, ENSURE ALL PATHS are adjusted to use "C:/***PATHNAME***" 

## Setting up AI

Link to LM Studio: [Website](https://lmstudio.ai/)
*** RECOMMENDATION FOR VULKAN FOR GPU ***
*** If using AMD and package manager does not have ROCm, see [TheRock](https://github.com/ROCm/TheRock)

## Downloading the data

1) Download script
```shell
#!/bin/env bash
#^Shebangs with bin/env bash vs bin/bash < improved compatibility bc it uses the env bash, not the default system bash (Mac, for example would 'call' an older bash version with less cool features) 
################################################################################################
################################################################################################
# Base configuration
BASE_DOWNLOAD_DIR="/data/temp/census" 
BASE_CENSUS_URL="https://www2.census.gov" #FTP BASE
BASE_ZIP_DIR="${BASE_DOWNLOAD_DIR}/zips"
BASE_RAW_DIR="${BASE_DOWNLOAD_DIR}/raw"
mkdir -p "$BASE_DOWNLOAD_DIR"/{zips,raw}
#BASE_TIGER_URL="${BASE_CENSUS_URL}/geo/tiger/TIGER" #All over the place pre 2008, New 'Schemas' by decade (consistent folder convention post-2010)
ACS_URL="${BASE_CENSUS_URL}/programs-surveys/acs/data/pums" # ACS GOES TO 1996-2024 
YEAR_START=2007
YEAR_END=2024
################################################################################################
################################################################################################
## STATE TO GET - associative array
declare -A STATES_TO_GET=(
    ["29"]="MO"  # Missouri (FIPS 29)
    ["20"]="KS"  # Kansas (FIPS 20)
    ["01"]="AL"  # Alabama (FIPS 01)
    ["02"]="AK"  # Alaska (FIPS 02)
    ["04"]="AZ"  # Arizona (FIPS 04)
    ["05"]="AR"  # Arkansas (FIPS 05)
    ["06"]="CA"  # California (FIPS 06)
    ["08"]="CO"  # Colorado (FIPS 08)
    ["09"]="CT"  # Connecticut (FIPS 09)
    ["10"]="DE"  # Delaware (FIPS 10)
    ["11"]="DC"  # District of Columbia (FIPS 11)
    ["12"]="FL"  # Florida (FIPS 12)
    ["13"]="GA"  # Georgia (FIPS 13)
    ["15"]="HI"  # Hawaii (FIPS 15)
    ["16"]="ID"  # Idaho (FIPS 16)
    ["17"]="IL"  # Illinois (FIPS 17)
    ["18"]="IN"  # Indiana (FIPS 18)
    ["19"]="IA"  # Iowa (FIPS 19)
    ["21"]="KY"  # Kentucky (FIPS 21)
    ["22"]="LA"  # Louisiana (FIPS 22)
    ["23"]="ME"  # Maine (FIPS 23)
    ["24"]="MD"  # Maryland (FIPS 24)
    ["25"]="MA"  # Massachusetts (FIPS 25)
    ["26"]="MI"  # Michigan (FIPS 26)
    ["27"]="MN"  # Minnesota (FIPS 27)
    ["28"]="MS"  # Mississippi (FIPS 28)
    ["30"]="MT"  # Montana (FIPS 30)
    ["31"]="NE"  # Nebraska (FIPS 31)
    ["32"]="NV"  # Nevada (FIPS 32)
    ["33"]="NH"  # New Hampshire (FIPS 33)
    ["34"]="NJ"  # New Jersey (FIPS 34)
    ["35"]="NM"  # New Mexico (FIPS 35)
    ["36"]="NY"  # New York (FIPS 36)
    ["37"]="NC"  # North Carolina (FIPS 37)
    ["38"]="ND"  # North Dakota (FIPS 38)
    ["39"]="OH"  # Ohio (FIPS 39)
    ["40"]="OK"  # Oklahoma (FIPS 40)
    ["41"]="OR"  # Oregon (FIPS 41)
    ["42"]="PA"  # Pennsylvania (FIPS 42)
    ["44"]="RI"  # Rhode Island (FIPS 44)
    ["45"]="SC"  # South Carolina (FIPS 45)
    ["46"]="SD"  # South Dakota (FIPS 46)
    ["47"]="TN"  # Tennessee (FIPS 47)
    ["48"]="TX"  # Texas (FIPS 48)
    ["49"]="UT"  # Utah (FIPS 49)
    ["50"]="VT"  # Vermont (FIPS 50)
    ["51"]="VA"  # Virginia (FIPS 51)
    ["53"]="WA"  # Washington (FIPS 53)
    ["54"]="WV"  # West Virginia (FIPS 54)
    ["55"]="WI"  # Wisconsin (FIPS 55)
    ["56"]="WY"  # Wyoming (FIPS 56)
    ["60"]="AS"  # American Samoa (FIPS 60)
    ["64"]="FM"  # Federated States of Micronesia (FIPS 64)
    ["66"]="GU"  # Guam (FIPS 66)
    ["68"]="MH"  # Marshall Islands (FIPS 68)
    ["69"]="MP"  # Northern Mariana Islands (FIPS 69)
    ["70"]="PW"  # Palau (FIPS 70)
    ["72"]="PR"  # Puerto Rico (FIPS 72)
)
# Function to download ACS data
func_get_acs() {
    local yr_to_get="${1}"
    local st_fips="${2}"
    local st_abbr="${3}"
    local ACS_SURVEY_LENGTH=("1-Year" "5-Year")
    declare -A ACS_SURVEY_TYPES=(
        ["housing"]="h"
        ["population"]="p"
    )
    for curr_survey in "${ACS_SURVEY_LENGTH[@]}"; do
        for survey_name in "${!ACS_SURVEY_TYPES[@]}"; do
            local survey_code="${ACS_SURVEY_TYPES[$survey_name]}"
            local st_abbr_lower=$(echo "$st_abbr" | tr '[:upper:]' '[:lower:]')
            local target_dir="${BASE_DOWNLOAD_DIR}/zips/acs/${survey_name}/${curr_survey}/${st_fips}/${yr_to_get}"
            mkdir -p "$target_dir"
            echo "  Downloading ACS ${curr_survey} ${survey_name} data for ${st_abbr}..."
            curl -s "${ACS_URL}/${yr_to_get}/${curr_survey}/" | \
                grep -o 'href="[^"]*\.zip"' | \
                sed 's/href="//; s/"//' | \
                grep "^csv_${survey_code}${st_abbr_lower}\.zip" | \
                while read -r filename; do
                    # Skip if already downloaded
                    if [[ -f "${target_dir}/${filename}" ]]; then
                        echo "    Skipping existing file: ${filename}"
                        continue
                    fi
                    wget \
                        --quiet \
                        --wait=2 \
                        --random-wait \
                        --tries=5 \
                        --user-agent="Mozilla/5.0 (compatible; research download)" \
                        -P "$target_dir" \
                        "${ACS_URL}/${yr_to_get}/${curr_survey}/${filename}"
                    if [[ -f "${target_dir}/${filename}" ]]; then
                        local size=$(du -h "${target_dir}/${filename}" | cut -f1)
                        echo "    Downloaded: ${filename} (${size}) -> ${target_dir}"
                    fi
                done
        done
    done
}
####MAIN EXECUTION BLOCK
echo "----------------------------------------"
echo "Starting Census data download..."
echo "Years: ${YEAR_START} to ${YEAR_END}"
echo "States: ${!STATES_TO_GET[@]}"
echo "Base directory: ${BASE_DOWNLOAD_DIR}"
echo "----------------------------------------"
# Loop over years
for yr in $(seq "${YEAR_START}" "${YEAR_END}"); do
    echo "Getting data for ${yr}"
    # Loop over states
    for state_fips in "${!STATES_TO_GET[@]}"; do
        state_abbr="${STATES_TO_GET[$state_fips]}"
        echo "  Processing state ${state_abbr} (FIPS ${state_fips})"
        # Download ACS data
        echo "  === ACS Data ==="
        func_get_acs "$yr" "$state_fips" "$state_abbr"
        # Download TIGER data
        echo "  === TIGER Data ==="
     #   func_get_tiger "$yr" "$state_fips"
        echo "  Completed ${state_abbr} for year ${yr}"
        echo "  ----------------------------------------"
    done
done
echo "Download complete!"
echo "Data stored in: ${BASE_DOWNLOAD_DIR}"
find "${BASE_DOWNLOAD_DIR}" -name "*.zip" -type f | wc -l | \
    xargs -I {} echo "Total files downloaded: {}"
du -sh "${BASE_DOWNLOAD_DIR}" | \
    awk '{print "Total size: " $1}'
### EXTRACTION
# Find all zip files and unzip them to processed directory
echo "=== unzipping data (zip -> raw) ==="
find "${BASE_ZIP_DIR}" -name "*.zip" -type f | while read zipfile; do
    extractpath=$(dirname "$zipfile" | sed 's/\/zips/\/raw/')
    mkdir -p "$extractpath"
    unzip -q -o "$zipfile" -d "$extractpath"
    echo "Extracted: $(basename "$zipfile")"
done
echo "=== Finished unzipping data (raw ready for Sparky!) ==="
echo "=== Summary Statistics ==="
# Total ZIP size
zip_size=$(du -sb "${BASE_ZIP_DIR}" | awk '{print $1}')
# Total RAW size
raw_size=$(du -sb "${BASE_RAW_DIR}" | awk '{print $1}')
#Convert to human-readable sizes
zip_h=$(du -sh "${BASE_ZIP_DIR}" | awk '{print $1}')
raw_h=$(du -sh "${BASE_RAW_DIR}" | awk '{print $1}')
tot_dir_size=$(du -sh "${BASE_DOWNLOAD_DIR}" | awk '{print $1}')
#Percentage expansion (avoid div0)
if [ "$zip_size" -gt 0 ]; then
    pct=$(awk -v z=$zip_size -v r=$raw_size 'BEGIN {printf "%.2f", (r/z - 1) * 100}')
else
    pct="N/A"
fi
echo "=========================="
echo "Current Total size : ${tot_dir_size}"
echo "ZIP total size 	: $zip_h"
echo "RAW total size	: $raw_h"
echo "Expansion      	: ${pct} %"
echo "=========================="
```


## Getting the Code Ready

1) Git cloning but sparse checkout artifacts (Unless you want to download all the components!)
```shell
BASE_REPO_NAME="bronze__acs_eda"
BASE_GIT_URL="https://github.com/groenewt/${BASE_REPO_NAME}.git"
git clone --filter=blob:none --sparse $BASE_GIT_URL
cd $BASE_REPO_NAME
#This way we only get the code in artifacts, not the 'unnecessary parts'  
git sparse-checkout set artifacts
```

2) Setup Python Environment and adjusting the Configuration
```bash
cd artifacts 
# install/setup venv based on dependencies
# Note: The base dependencies are pandas, seaborn, scikit-learn, requests, and tensorflow
#(***If you know what you are doing, please adjust as needed)
uv sync 
```
```python 
### IN config.py
#SO as is, the script configuration is 'designed' for linux system with default.
# There is more to customize, but if you know you 'what to customize' you will find the appropriate fields around here as well
@dataclass
class Config:
    """Centralized configuration"""
    # KEY NOTES: BASE_DOWNLOAD_DIR from that earlier download script HAS TO GET UPDATED In config.py << ENSURE MATCHES
    folder_base: str = "/data/temp/census/raw/acs"
    #... 
    # KEY NOTES: LM Studio 'serve'
    llm_url: str = "http://localhost:1234"
    #KEY NOTES: CHANGE TO DESIRED MODEL 
    llm_model: str = "local-model"
```

3) Run the code
```shell
#For just one state
#This Example will showcase the running for Kansas (State FIPS 20), for the housing survey
STATES_TO_RUN="Kansas" 
uv run main.py --states $STATES_TO_RUN --surveys housing --scopes 5-Year
```
```shell
#Full Blast (ALL STATES, ALL SCOPES, ALL YEARS, ALL SURVEYS)
# No need for --survey housing,population  bc by default runs both unless specific is stated
uv run main.py --all-states --all-scopes
```
```shell
#Obligatory call --help for full overview of cli options
uv run main.py --help 
```


## Appendix
### Privacy & Confidentiality
**PROTECT PRIVACY**: While ACS PUMS data is anonymized and disclosure-protected by the Census Bureau, users must:
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


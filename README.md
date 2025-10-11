# Census ACS Exploratory Data Analysis (by State)

**Educational Use Disclaimer**

*EDUCATIONAL AND RESEARCH PURPOSES ONLY*: ***This repository and its contents are provided solely for educational, academic research, and learning purposes. The data, scripts, analyses, and any outputs are intended to demonstrate data analysis techniques and Census data exploration methods. Users are responsible for ensuring their use of Census data complies with all applicable terms of service, usage restrictions, and legal requirements. This project is not affiliated with, endorsed by, or representative of the U.S. Census Bureau. Always refer to official Census Bureau sources for authoritative data and interpretations.***


**Data Accuracy & No Warranty**

*NO WARRANTY*: ***This repository is provided "as is" without warranty of any kind, express or implied. The authors make no guarantees regarding the accuracy, completeness, or reliability of any data, scripts, or analyses. Users assume all responsibility for verifying data accuracy and appropriateness for their intended use. Census data contains sampling and non-sampling errors - always consult official documentation and use appropriate statistical methods.***
This repository contains Exploratory Data Analysis (EDA) for Census ACS organized by State/Survey-Type/Survey-Scope
- **State**: 50 US States + District of Columbia, Puerto Rico
- **Survey-Type**: housing, population
- **Survey-Scope**: 1-Year, 5-Year

***Data Availability Note***: Only 2007-2023 ACS data is evaluated
##  So What? 
**Test of LLM usage during EDA Stages**
1) Ability to interpret and provide recommendations for employed statistical methods/models 
2) Interpretation, based on combinding provided context - *and whatever else model has been trainied on prior*, to help inform "What we are seeing" as well as "What is expected" 
3) Missing Data handling- how does an LLM react when told to analyze Anomalies when none have been provided? *Preliminary Investigation has yieled fascinating results wherein Model 'reasons' where they would have expected anomalies and why and how it potentially relates to data quality/normalization/etc
**Designed Limitations**
1) *Brute full spectrum*: Designed to be 'full spectrum', this EDA creates various models (unsupervised, supervised) for various configurations (some non-sense, limited in scope, not adhering to best statistical/economic practices)
2) *CPU Training for Deep Learning*: While not signficant for end viewer, this limitation is a result of limited machine  
**Next Run**
1) *Improving Model Context*: provided LLM Context should have been more in depth into data source (PUMA microdata) and illict/reference in reasoning 
2) *Personal Oversight*: Full disclosure, I definitely overlooked 'Currency' (Nominal, Real, +++) and as such any currency values should be treated as nominal

## Highlights
### LLM Powered Analysis
Large Languge Model Integration (LLM) to assist with large scale data analytics (Exploratory Data Analysis, Data Visualization, Data Modeling, etc.)
**Optimized Responses**: Generating at runtime an extended unique context providing additional instructions, background knowledge, and contextual information.
### Deep Exploration Patterns
Large quantity of repeated analysis,processing, visualization, and modeling patterns across a plethora of states/survey-types/survey-scopes.
### Next Steps
Blueprints for next steps generated for distinct topics/subjects; this comes as a result of diverse  analysis,processing, visualization, and modeling patterns, in tandem with LLM intepretation.



## Hardware Quickstart 
Base Recommendation for local LLM Hardware: 


1. **OS**                   : $    0.00 : Debian 13 Trixie
2. **Framework**            : $ 1699.00 : [Framework Desktop Mainboard AMD Ryzen AI MAX 300 128 GB LPDDR5x-8000 memory](https://frame.work/products/framework-desktop-mainboard-amd-ryzen-ai-max-300-series?v=FRAFMK0002)
3. **Case**                 : $  109.99 : [Fractal Design Node 304](https://www.newegg.com/fractal-design-mini-itx-tower-node-304-aluminum-steel-computer-case-black-fd-ca-node-304-bl/p/N82E16811352027)
4. **Power Supply**         : $  124.99 : [CORSAIR RMe Series RM1200e ATX Power Supply – Fully Modular – ATX 3.1 – 80 PLUS Gold – Cybenetics Platinum – Low-Noise – 1200 Watts](https://www.newegg.com/rme-atx-3-0-compatible-atx-3-1-compatible-1200-w-80-plus-gold-certified-power-supplies-corsair-rm1200e/p/N82E16817139315?Item=N82E16817139315&cm_sp=product-_-from-price-options)
5. **CPU Fan**              : $   31.90 : [Noctua NF-A12x25 HS-PWM 120mm](https://frame.work/products/desktop-noctua-cpu-fan?v=FRAMBX0002)
6. **NVMe (Slot 1)**        : $  399.99 : [WD_BLACK 8TB SN850X NVMe Internal Gaming Solid State Drive with Heatsink](https://www.amazon.com/WD_BLACK-SN850X-Internal-Gaming-Heatsink/dp/B0D9WTM2TH/ref=sr_1_2_sspa?crid=19538HBDFKJJ5&dib=eyJ2IjoiMSJ9.ydUUsp-J3DcI7tj41OTg3ZicITCffXsMBWPfPriDGbgqvPtvar_0grj_sR3Ial8AKyyK-nXsqpbH0msDXVFSbedIExEgIDSxt9Z8SckCDCCSM1I3eOoPY_k818Y6L8GB6RER1xPkA5NWtBe8YKEgMzhG6Ga6hVJp9kxgedN9uhKRdSF5cubi8CFF8NPNI03Xu6nbmVrz9Jv4F6r251C3a-plHcGt2IXM0-5W-Dv0cRU.Xrlr7sovlGh7-NKRwLutup86O4HpC961jGkrsHjcVdE&dib_tag=se&keywords=SAMSUNG%2B9100%2BPRO%2B4TB&qid=1760139413&sprefix=samsung%2B9100%2Bpro%2B4tb%2Caps%2C166&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)  
7. **NVMe (Slot 2)**        : $  399.99 : [WD_BLACK 8TB SN850X NVMe Internal Gaming Solid State Drive with Heatsink](https://www.amazon.com/WD_BLACK-SN850X-Internal-Gaming-Heatsink/dp/B0D9WTM2TH/ref=sr_1_2_sspa?crid=19538HBDFKJJ5&dib=eyJ2IjoiMSJ9.ydUUsp-J3DcI7tj41OTg3ZicITCffXsMBWPfPriDGbgqvPtvar_0grj_sR3Ial8AKyyK-nXsqpbH0msDXVFSbedIExEgIDSxt9Z8SckCDCCSM1I3eOoPY_k818Y6L8GB6RER1xPkA5NWtBe8YKEgMzhG6Ga6hVJp9kxgedN9uhKRdSF5cubi8CFF8NPNI03Xu6nbmVrz9Jv4F6r251C3a-plHcGt2IXM0-5W-Dv0cRU.Xrlr7sovlGh7-NKRwLutup86O4HpC961jGkrsHjcVdE&dib_tag=se&keywords=SAMSUNG%2B9100%2BPRO%2B4TB&qid=1760139413&sprefix=samsung%2B9100%2Bpro%2B4tb%2Caps%2C166&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)  
8. **NVMe Heatsink**        : $   29.99 : M.2 2280 Heatsink / Thermal Pad — recommended for sustained loads
9. **NVMe Mount / Screws**  : $    6.50 : M.2 standoff & screw kit
10. **Cables / Adapters**   : $   24.99 : 24-pin ATX extension, SATA cables, USB adapters
11. **UPS**                 : $  119.99 : 600–900 VA UPS, pure sine wave
#### ADDITIONAL STORAGE
12. **PCIe SATA Controller**            : $   45.99 : [RIITOP 6-Port PCIe 3.0 x4 SATA Controller](https://www.amazon.com/RIITOP-Controller-Expansion-Desktop-Support/dp/B0BYN3XVP3) — ASM1166 chipset
13. **6x Seagate IronWolf Pro 28TB**    : $ 2879.94 : [Seagate IronWolf Pro 28TB Enterprise NAS](https://www.amazon.com/Seagate-IronWolf-Internal-Hard-Drive/dp/B0FFBPK8T7/) — 6 drives @ $479.99 each
14. **SATA Cables (6-pack)**            : $   14.99 : 18-24" right-angle SATA III cables
15. **SATA Power Splitters**            : $   12.99 : SATA power Y-splitters for PSU
### HARDWARE SUMMARY

**CPU/APU**: AMD Ryzen AI MAX 300 Series (Framework Desktop Mainboard)  

**CPU Main**: 16-core/32-thread + 3.0GHz base clock (*Up to 5.1GHz max boost*)

**Additional CPU**: 64MB L3 Cache , Processor power level: 120W sustained, 140W boost power

**NPU**: 32 Tiles, Up to 50 TOPS

**Integrated Graphics**: Radeon™ 8060S (*Up to 2.9GHz, 40 Compute Units, 32MB MALL Cache*)

**Total LPDDR5x Memory**: 128GB @ 8000 MT/s  

**Total NVMe Storage**: 16TB (2× 8TB M.2 slots maxed)  

**Total HDD Storage**: 168TB (6× 28TB Seagate IronWolf Pro)  

**Power Supply**: 1200W Corsair RM1200e (80 PLUS Gold, ATX 3.1, Fully Modular)  

**Case**: Fractal Design Node 304 (Mini-ITX, High Airflow)  

**Storage Controller**: RIITOP 6-Port PCIe 3.0 x4 SATA (ASM1166 chipset)  

**Backup Power**: 600-900VA UPS (Pure Sine Wave)  

**Operating System**: Debian 13 Trixie  

**Grand Total Storage**: **184TB**  
### Estimated Total Cost: **$6,501.24**

### Key Features
- 16TB ultra-fast NVMe for OS, applications, and hot data
- 168TB high-capacity HDD array for bulk storage  
- Fully modular 1200W PSU for future expansion  
- Mini-ITX compact form factor with high airflow design  
- UPS included for power protection  
- Expandable SATA storage with dedicated PCIe controller  
- 128GB unified memory for AI/compute workloads


### IMPORTANT COMPATIBILITY NOTES
* **Framework Desktop mainboard I/O**: 2× M.2 2280 NVMe slots (PCIe 4.0 x4 each), 1× PCIe 4.0 x4 expansion slot, **ZERO SATA ports**. No support for 2.5" or 3.5" SATA/HDD drives on the mainboard itself.
* **PCIe Gen5 limitation**: The Framework Desktop M.2 slots operate at PCIe Gen4 speeds max. The Samsung 9100 PRO (Gen5 drive) will work but fall back to Gen4 bandwidth (~7,500 MB/s real-world vs advertised 14,800 MB/s).
* **Power connectors**: Framework Desktop mainboard expects standard 24-pin ATX + 8-pin EPS when used in a conventional Mini-ITX case with ATX PSU.
* **Case compatibility**: Framework Desktop uses standard Mini-ITX form factor; compatible with any Mini-ITX case and ATX PSU.
* **SATA expansion option**: To add SATA support, you would need a PCIe 4.0 x4 SATA controller card in the single expansion slot (sacrifices the PCIe slot for SATA ports).

### OTHER AWESOME HARDWARE:
**Fast New Generation NVMe** : $  999.99 : [SAMSUNG 9100 PRO 8TB PCIe 5.0 x4 M.2 2280, up to 14,800 MB/s — MZ-VAP8T0B/AM](https://www.samsung.com/us/memory-storage/nvme-ssd/9100-pro-nvme-ssd-sku-mz-vap8t0b-am/)
- Compatible with motherboard but runs at PCIe 4.0 speeds

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

1) Download script
```shell
#!/bin/env bash
################################################################################################
# Base configuration
BASE_DOWNLOAD_DIR="/data/temp/census"
mkdir -p "$BASE_DOWNLOAD_DIR"/{zips,raw}
BASE_CENSUS_URL="https://www2.census.gov" #FTP BASE
#BASE_TIGER_URL="${BASE_CENSUS_URL}/geo/tiger/TIGER" #All over the place pre 2008, New 'Schemas' by decade (consistent folder convention post-2010)
ACS_URL="${BASE_CENSUS_URL}/programs-surveys/acs/data/pums" # ACS GOES TO 1996-2023
YEAR_START=2007
YEAR_END=2024
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
BASE_DOWNLOAD_DIR="/data/temp/census"

### combined across Zeppelin paragraphs  
### EXTRACTION
BASE_ZIP_DIR="${BASE_DOWNLOAD_DIR}/zips"
BASE_RAW_DIR="${BASE_DOWNLOAD_DIR}/raw"
echo "=== unzipping data (zip -> raw) ==="
# Find all zip files and unzip them to processed directory
find "${BASE_ZIP_DIR}" -name "*.zip" -type f | while read zipfile; do
    # Replace /zips with /processed in the path
    extractpath=$(dirname "$zipfile" | sed 's/\/zips/\/raw/')
    # Create directory if it doesn't exist
    mkdir -p "$extractpath"
    # Unzip the file
    unzip -q "$zipfile" -d "$extractpath"
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
echo "Current Total size : ${tot_dir_siz}"
echo "ZIP total size 	: $zip_h"
echo "RAW total size	: $raw_h"
echo "Expansion      	: ${pct} %"
echo "=========================="
```



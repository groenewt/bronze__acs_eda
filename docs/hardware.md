# Hardware 
## Budget & Alternative Hardware Options

The "Base Recommendation" above is optimized for running large local LLMs (70B+ parameters). However, the EDA pipeline itself is much lighter - it includes `gc.collect()` calls and can run on modest hardware. Here are tiered alternatives:

### Tier 1: "Just Run the Pipeline" (~$300-450)
**For**: EDA, ML models, visualizations - skip local LLM or use cloud/API

| Option | Price | Specs | Notes |
|--------|-------|-------|-------|
| Kamrui Hyper H2 | ~$420 | i9-11900H, 32GB DDR4, 1TB | Cheapest 32GB option |
| Bosgame P3 | ~$440 | Ryzen 7 7840HS, 32GB DDR5, 1TB | Better CPU generation |
| Geekom AX8 Max | ~$470 | Ryzen 7 8745HS, 32GB DDR5, 1TB | Best value, often on sale |

### Tier 2: "Run Small Local LLMs" (~$600-800)
**For**: Full pipeline + 7B-13B quantized models via LM Studio

| Option | Price | Specs | Notes |
|--------|-------|-------|-------|
| Mac Mini M4 | $599-799 | M4 chip, 16-32GB unified | Excellent memory bandwidth for inference |
| Beelink SER8 | ~$600 | Ryzen 7 8745HS, 32GB DDR5 | RAM upgradeable to 64GB later |
| Refurb Dell Precision 5820 | ~$500-700 | Xeon, 64GB ECC | eBay/Dell Outlet; add GPU later |

### Tier 3: "Serious Local LLM" (~$900-1200)
**For**: 14B+ parameter models, heavier workloads

| Option | Price | Specs | Notes |
|--------|-------|-------|-------|
| Beelink SER9 Pro | ~$999 | Ryzen AI 9 370, 32GB LPDDR5x | 24GB allocatable VRAM, 50 TOPS NPU |
| Refurb HP Z4 G4 + GPU | ~$1000-1200 | Xeon W, 64-128GB + RTX 3060 | Workstation + ~$250 GPU |

### Refurbished Workstation Tips
- **Dell Precision 5820/7820** and **HP Z4/Z6 G4** are excellent value on eBay/Dell Outlet
- Look for Xeon W-series with 64GB+ ECC RAM
- Add a used RTX 3060/3070/3080 (~$200-350) for GPU inference
- Higher power draw but expandable and repairable

### What Can Run Where?
| Hardware Tier | Census EDA Pipeline | 7B Models | 13B Models | 70B+ Models |
|---------------|---------------------|-----------|-------------|-------------|
| Tier 1 (32GB) | ✓ Full | ✓ Slow | ⚠ Quantized | ✗ |
| Tier 2 (32-64GB) | ✓ Full | ✓ Good | ✓ Quantized | ⚠ Very slow |
| Tier 3 (64GB+) | ✓ Full | ✓ Fast | ✓ Good | ⚠ Quantized only |
| Base Rec (128GB) | ✓ Full | ✓ Fast | ✓ Fast | ✓ Quantized |

### Sources
- [Beelink SER9 LLM Benchmarks](https://www.bee-link.com/blogs/all/ser9-performance-comparison-in-local-deployment-of-deepseek-r1-llm)
- [Local LLM Hardware Guide 2025](https://introl.com/blog/local-llm-hardware-pricing-guide-2025)
- [Budget Mini PCs 2025](https://www.gizmochina.com/2025/11/13/best-budget-friendly-mini-pcs-you-can-buy-in-2025/)


##  A Built Out Machine  
This details a custom build that captures 'how I wish I would've built my machine'. This seeks to facilitate big data operations while offering sufficient memory/capabilities for said operations/Local LLMs

Base Recommendation for local LLM Hardware: 
1. **OS**                   : $    0.00 : Debian 13 Trixie
2. **Framework**            : $ 1699.00 : [Framework Desktop Mainboard AMD Ryzen AI MAX 300 128 GB LPDDR5x-8000 memory](https://frame.work/products/framework-desktop-mainboard-amd-ryzen-ai-max-300-series?v=FRAFMK0002)
3. **Case**                 : $  109.99 : [Fractal Design Node 304](https://www.newegg.com/fractal-design-mini-itx-tower-node-304-aluminum-steel-computer-case-black-fd-ca-node-304-bl/p/N82E16811352027)
4. **Power Supply**         : $  199.99 : [CORSAIR RMe Series RM1200e ATX Power Supply – Fully Modular – ATX 3.1 – 80 PLUS Gold – Cybenetics Platinum – Low-Noise – 1200 Watts](https://www.newegg.com/rme-atx-3-0-compatible-atx-3-1-compatible-1200-w-80-plus-gold-certified-power-supplies-corsair-rm1200e/p/N82E16817139315?Item=N82E16817139315&cm_sp=product-_-from-price-options)
5. **CPU Fan**              : $   39.00 : [Noctua NF-A12x25 HS-PWM 120mm](https://frame.work/products/desktop-noctua-cpu-fan?v=FRAMBX0002)
6. **NVMe (Slot 1)**        : $  639.99 : [WD_BLACK 8TB SN850X NVMe Internal Gaming Solid State Drive with Heatsink](https://www.amazon.com/WD_BLACK-SN850X-Internal-Gaming-Heatsink/dp/B0D9WTM2TH/ref=sr_1_2_sspa?crid=19538HBDFKJJ5&dib=eyJ2IjoiMSJ9.ydUUsp-J3DcI7tj41OTg3ZicITCffXsMBWPfPriDGbgqvPtvar_0grj_sR3Ial8AKyyK-nXsqpbH0msDXVFSbedIExEgIDSxt9Z8SckCDCCSM1I3eOoPY_k818Y6L8GB6RER1xPkA5NWtBe8YKEgMzhG6Ga6hVJp9kxgedN9uhKRdSF5cubi8CFF8NPNI03Xu6nbmVrz9Jv4F6r251C3a-plHcGt2IXM0-5W-Dv0cRU.Xrlr7sovlGh7-NKRwLutup86O4HpC961jGkrsHjcVdE&dib_tag=se&keywords=SAMSUNG%2B9100%2BPRO%2B4TB&qid=1760139413&sprefix=samsung%2B9100%2Bpro%2B4tb%2Caps%2C166&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)  
7. **NVMe (Slot 2)**        : $  639.99 : [WD_BLACK 8TB SN850X NVMe Internal Gaming Solid State Drive with Heatsink](https://www.amazon.com/WD_BLACK-SN850X-Internal-Gaming-Heatsink/dp/B0D9WTM2TH/ref=sr_1_2_sspa?crid=19538HBDFKJJ5&dib=eyJ2IjoiMSJ9.ydUUsp-J3DcI7tj41OTg3ZicITCffXsMBWPfPriDGbgqvPtvar_0grj_sR3Ial8AKyyK-nXsqpbH0msDXVFSbedIExEgIDSxt9Z8SckCDCCSM1I3eOoPY_k818Y6L8GB6RER1xPkA5NWtBe8YKEgMzhG6Ga6hVJp9kxgedN9uhKRdSF5cubi8CFF8NPNI03Xu6nbmVrz9Jv4F6r251C3a-plHcGt2IXM0-5W-Dv0cRU.Xrlr7sovlGh7-NKRwLutup86O4HpC961jGkrsHjcVdE&dib_tag=se&keywords=SAMSUNG%2B9100%2BPRO%2B4TB&qid=1760139413&sprefix=samsung%2B9100%2Bpro%2B4tb%2Caps%2C166&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)  
8. **NVMe Heatsink**        : $   29.99 : M.2 2280 Heatsink / Thermal Pad — recommended for sustained loads
9. **NVMe Mount / Screws**  : $    6.50 : M.2 standoff & screw kit
10. **Cables / Adapters**   : $   24.99 : 24-pin ATX extension, SATA cables, USB adapters
11. **UPS**                 : $  119.99 : 600–900 VA UPS, pure sine wave
#### ADDITIONAL STORAGE
12. **PCIe SATA Controller**            : $   41.59 : [RIITOP 6-Port PCIe 3.0 x4 SATA Controller](https://www.amazon.com/Ports-RIITOP-Expansion-Controller-Adapter/dp/B09C4G57PW/ref=sr_1_3?dib=eyJ2IjoiMSJ9.jRI1W7UIRHS1PfwpKHZ1LgwXhLbW9gJcNZni4uJLahw5mWggxrOT3jvrRkaKBWS4LwSP2kbbn4Ki9PUi7nZhoOrtsN9JHbrjymjPt-b73hi7gDU5bwe0Wziex82pHxiCdXI0vyqBAGqHN2-qW7csCmSp1JhIqd2iyPEgr_g5UiAx7fs5hEPqLLtZo4Kf5O-Iy79s6-ySSlJVGd3Rtfp4h3MLoIdc0iUqrDxCfjaBq3k.zTFVDteZP4k2eUGQt25eA9jJG-37eSS2YJNDu4TagC4&dib_tag=se&keywords=RIITOP+6-Port+PCIe+3.0+x4+SATA+Controller&qid=1760143101&sr=8-3)
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

### Estimated Total Cost Basic: **$3579.01** 
- This Option does not include the additional 192 TB of HDD storage
### Estimated Total Cost      : **$6458.95**
- This Option does include the additional 192 TB of HDD storage

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

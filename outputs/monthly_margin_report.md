# Monthly Hosting Margin Report
Period analyzed: **February 2026** (vs January 2026)

## 1. Executive Summary
- Overall annualized gross margin was **93.6%** on **$361,504,958** revenue and **$23,122,076** cost; this is **-0.45 pts MoM**.
- Margin pressure remains concentrated: top 5 sub-70% accounts represent **29.7%** of total excess cost (target gap), equal to **$1,553,519** annualized.
- Total opportunity to bring all sub-70% material accounts to 70% margin is **$5,232,647** annualized.
- MoM, revenue changed **$-4,707,989** and cost changed **$1,331,706**; cost growth outpaced revenue growth on a target-margin basis by **$2,744,103**.
- **655** material accounts show 2+ consecutive months of worsening margin into February 2026; largest current target-gap exposures are listed in Risks.

## 2. KPI Table
| KPI | Value |
|---|---:|
| Total annualized revenue | $361,504,958 |
| Total annualized cost | $23,122,076 |
| Gross margin % | 93.6% |
| MoM revenue change | $-4,707,989 |
| MoM cost change | $1,331,706 |
| MoM gross margin % change | -0.45 pts |
| YTD average gross margin % (2026) | 93.8% |

## 3. Top Issues (Top 10 by Excess Cost vs 70% Target)
| Account | Annualized Revenue | Annualized Cost | Gross Margin % | Excess Cost vs 70% Target |
|---|---:|---:|---:|---:|
| Numeral | $547,160 | $631,221 | -15.4% | $467,073 |
| Virgo Facilities | $299,328 | $490,726 | -63.9% | $400,928 |
| Notion Labs, Inc. | $384,610 | $403,535 | -4.9% | $288,152 |
| Shutterstock Inc. | $249,880 | $281,184 | -12.5% | $206,220 |
| Metronome | $240,936 | $263,427 | -9.3% | $191,146 |
| (Unmapped Account) | $0 | $188,363 | 0.0% | $188,363 |
| Modern_AI_LLC | $133,889 | $194,238 | -45.1% | $154,071 |
| YPrime | $121,302 | $174,235 | -43.6% | $137,844 |
| U.S. Venture, Inc. | $72,028 | $120,213 | -66.9% | $98,605 |
| Krazybee Services Private Limited | $0 | $91,836 | 0.0% | $91,836 |

## 4. Drivers
- **Revenue/price effect:** gross revenue movement was **$-4,707,989** annualized ($26,067,102 increases offset by $-30,775,091 decreases).
- **Cost increases:** total cost movement was **$1,331,706** annualized ($4,074,417 increases offset by $-2,742,711 decreases).
- **Usage/volume + mix signal:** implied margin pressure from cost relative to 70% target rose by **$2,744,103** MoM.
- **Concentration:** top 10 accounts are **42.5%** of total excess cost; pressure is concentrated, not broad-based.
- Largest account-level movers by target-gap impact (MoM):
  - Beazley: revenue $-0, cost $-798,800, target-gap impact ~$-798,800.
  - Notion Labs, Inc.: revenue $-33, cost $281,044, target-gap impact ~$281,054.
  - Numeral: revenue $-28, cost $253,955, target-gap impact ~$253,963.
  - Carilion Services: revenue $-699,630, cost $-24,510, target-gap impact ~$185,379.
  - Pacific International Lines Pte Ltd: revenue $545,014, cost $0, target-gap impact ~$-163,504.

## 5. Segmentation
### By cloud provider proxy (PBF flag; dataset does not include explicit cloud-provider field)
| Provider Segment | Revenue | Cost | Gross Margin % |
|---|---:|---:|---:|
| Non-PBF | $320,589,069 | $19,005,313 | 94.1% |
| PBF | $16,510,137 | $2,873,093 | 82.6% |

### By customer tier (Simplified Platform Tier)
| Tier | Revenue | Cost | Gross Margin % |
|---|---:|---:|---:|
| Unspecified | $109,388,694 | $9,240,271 | 91.6% |
| Standard | $83,073,750 | $4,384,188 | 94.7% |
| Enterprise | $81,393,731 | $5,367,961 | 93.4% |
| BCF | $62,737,033 | $2,708,073 | 95.7% |
| Starter | $423,198 | $14,552 | 96.6% |
| Freemium | $82,800 | $163,362 | -97.3% |

### By revenue band
| Revenue Band | Revenue | Cost | Gross Margin % |
|---|---:|---:|---:|
| $50k-$250k | $175,176,721 | $10,566,214 | 94.0% |
| $250k-$1M | $96,881,242 | $6,195,479 | 93.6% |
| <$50k | $51,405,199 | $4,346,632 | 91.5% |
| >$1M | $13,636,044 | $770,082 | 94.4% |

## 6. Opportunities
- Total annualized margin improvement if all material sub-70% accounts are lifted to 70%: **$5,232,647**.
- Top actionable levers:
  - **Pricing correction:** target accounts where realized margin is deeply negative and revenue base can support repricing.
  - **Infrastructure optimization:** reduce compute/runtime load for high-cost accounts (especially where cost/revenue ratio has widened MoM).
  - **Usage management:** enforce workload guardrails and sync/runtime limits on accounts with disproportionate donkey runtime or connection footprint.
  - **Customer migration / hosting changes:** evaluate migration paths for structurally unprofitable hosting patterns (e.g., repeatedly negative-margin configurations).

## 7. Risks
- Accounts with 2+ consecutive months of worsening gross margin (latest three observations):
| Account | Gross Margin Trend (oldest→latest) | Current Excess Cost vs 70% |
|---|---:|---:|
| Numeral | 42.0% → 31.1% → -15.4% | $467,073 |
| Virgo Facilities | -34.7% → -48.0% → -63.9% | $400,928 |
| Notion Labs, Inc. | 75.8% → 68.2% → -4.9% | $288,152 |
| Shutterstock Inc. | 36.0% → 35.6% → -12.5% | $206,220 |
| Metronome | 8.9% → -6.2% → -9.3% | $191,146 |
| YPrime | 0.8% → -7.1% → -43.6% | $137,844 |
| Krazybee Services Private Limited | 62.5% → 43.7% → 13.7% | $91,836 |
| Jaris, Inc. | 35.8% → 30.7% → 7.4% | $84,358 |
| Autodesk, Inc. | 68.5% → 66.4% → 55.6% | $82,529 |
| Karbon | 79.7% → 71.9% → 5.4% | $71,204 |
- Concentration risk: top 5 accounts contribute **29.7%** of total excess cost.
- Data quality / attribution caveat: explicit cloud provider dimension is absent in source files, so provider segmentation is shown via PBF flag proxy only.

## 8. Final Output
### Top 5 Priority Accounts
1. **Numeral** — excess cost $467,073, GM -15.4%.
1. **Virgo Facilities** — excess cost $400,928, GM -63.9%.
1. **Notion Labs, Inc.** — excess cost $288,152, GM -4.9%.
1. **Shutterstock Inc.** — excess cost $206,220, GM -12.5%.
1. **Metronome** — excess cost $191,146, GM -9.3%.

### Recommended Next Actions
1. Launch pricing review for top-5 priority accounts within current quarter and set floor margin guardrails at renewal.
2. Run infra cost deep-dives on the top 10 accounts by excess cost and assign optimization owners with 30/60-day targets.
3. Apply usage controls for high-runtime / high-connection outliers and monitor weekly cost-to-revenue drift.
4. Define migration plans for structurally negative-margin configurations and track realized savings.

### Estimated Financial Impact
- Full uplift to 70% across all material sub-70% accounts: **$5,232,647 annualized**.
- Near-term focus on top 5 accounts captures **$1,553,519 annualized** (29.7% of total opportunity).

## Top 20 Material Named Accounts by Margin Impact
### Summary Metrics (Top Panel)
- Total margin impact across top 20 material named accounts: **$-1,128,137**.
- Worst single account: **Virgo Facilities** ($-191,398).
- Count of accounts with cost but zero revenue: **4**.
- Highest cost per sync hour: **Capella Space** at **$438.61/hr**.

### Dollar Impact Chart Data (Worst to Best)
| Rank | Account | Margin $ |
|---:|---|---:|
| 1 | Virgo Facilities | $-191,398 |
| 2 | Krazybee Services Private Limited | $-91,836 |
| 3 | Numeral | $-84,061 |
| 4 | Mara_Care_AG | $-79,098 |
| 5 | OPTIMIND Inc.株式会社オプティマインド | $-76,330 |
| 6 | Rhombus AI | $-69,032 |
| 7 | Modern_AI_LLC | $-60,349 |
| 8 | Capella Space | $-60,209 |
| 9 | YPrime | $-52,933 |
| 10 | FivetranAnalytics | $-52,667 |
| 11 | U.S. Venture, Inc. | $-48,185 |
| 12 | PT_Mata_Gunung_Altazor | $-41,735 |
| 13 | Firehouse_Technology | $-39,327 |
| 14 | Shutterstock Inc. | $-31,304 |
| 15 | Gilion | $-30,710 |
| 16 | Circular | $-28,143 |
| 17 | Cifra_Labs | $-24,972 |
| 18 | Irvine Company - BCF Account | $-23,642 |
| 19 | Metronome | $-22,491 |
| 20 | NISSIN FOODS HOLDINGS CO., LTD. | $-19,714 |

### Account-Level Breakdown Table
| Account | Customer Tier | Annualized Revenue | Annualized Cost | Margin $ | Margin % | Runtime (hrs) | Cost / Runtime hr | Key Drivers |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Virgo Facilities | Unspecified | $299,328 | $490,726 | $-191,398 | -63.9% | 11,425.3 | $42.95 | DLW cost, low scale |
| Krazybee Services Private Limited | Unspecified | $0 | $91,836 | $-91,836 | 0.0% | 3,536.3 | $25.97 | no revenue, connection |
| Numeral | Unspecified | $547,160 | $631,221 | $-84,061 | -15.4% | 52,643.9 | $11.99 | DLW cost, low scale |
| Mara_Care_AG | Enterprise | $753 | $79,851 | $-79,098 | -10511.1% | 467.5 | $170.80 | connection, low scale |
| OPTIMIND Inc.株式会社オプティマインド | Enterprise | $3,042 | $79,372 | $-76,330 | -2509.2% | 7,803.2 | $10.17 | connection, low scale |
| Rhombus AI | Freemium | $0 | $69,032 | $-69,032 | 0.0% | 2,176.1 | $31.72 | no revenue, DLW cost |
| Modern_AI_LLC | Standard | $133,889 | $194,238 | $-60,349 | -45.1% | 54,869.6 | $3.54 | DLW cost, low scale |
| Capella Space | BCF | $13,039 | $73,248 | $-60,209 | -461.7% | 167.0 | $438.61 | connection, low scale |
| YPrime | Unspecified | $121,302 | $174,235 | $-52,933 | -43.6% | 26,046.6 | $6.69 | connection, low scale |
| FivetranAnalytics | BCF | $0 | $52,667 | $-52,667 | 0.0% | 7,360.1 | $7.16 | no revenue, connection |
| U.S. Venture, Inc. | BCF | $72,028 | $120,213 | $-48,185 | -66.9% | 590.1 | $203.70 | DLW cost, low scale |
| PT_Mata_Gunung_Altazor | Enterprise | $388 | $42,124 | $-41,735 | -10751.0% | 355.1 | $118.63 | DLW cost, low scale |
| Firehouse_Technology | Enterprise | $4,607 | $43,934 | $-39,327 | -853.6% | 11,394.3 | $3.86 | DLW cost, low scale |
| Shutterstock Inc. | Unspecified | $249,880 | $281,184 | $-31,304 | -12.5% | 8,750.5 | $32.13 | DLW cost, low scale |
| Gilion | Standard | $18,556 | $49,266 | $-30,710 | -165.5% | 9,879.0 | $4.99 | connection, low scale |
| Circular | Enterprise | $12,734 | $40,877 | $-28,143 | -221.0% | 4,576.2 | $8.93 | connection, low scale |
| Cifra_Labs | Enterprise | $535 | $25,507 | $-24,972 | -4668.0% | 2,319.5 | $11.00 | DLW cost, low scale |
| Irvine Company - BCF Account | BCF | $22,445 | $46,087 | $-23,642 | -105.3% | 1,745.2 | $26.41 | connection, low scale |
| Metronome | BCF | $240,936 | $263,427 | $-22,491 | -9.3% | 1,993.6 | $132.14 | DLW cost, low scale |
| NISSIN FOODS HOLDINGS CO., LTD. | Unspecified | $0 | $19,714 | $-19,714 | 0.0% | 218.0 | $90.44 | no revenue, connection |

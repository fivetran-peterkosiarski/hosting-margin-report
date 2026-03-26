Perform a monthly FP&A analysis of customer hosting margin for the most recently completed month.

Use only materially significant accounts by default. Define material as:
- annualized revenue > 20000, or
- annualized cost > 1000

Rank issues by absolute dollar impact, not just gross margin %.

Define:
excess_cost_70 = max(0, annualized_cost - 0.30 * annualized_revenue)

Output format:

1. Executive Summary
- Summarize the 3 to 5 most important takeaways
- Focus on material changes and financially meaningful issues only

2. KPI Table
- Total annualized revenue
- Total annualized cost
- Gross margin %
- MoM change in revenue, cost, and gross margin %
- YTD average gross margin %

3. Top Issues
- Rank the top 10 accounts by margin dollar loss relative to a 70% target margin
- For each account, show:
  - account name
  - annualized revenue
  - annualized cost
  - gross margin %
  - excess cost vs 70% target

4. Drivers
- Explain the main drivers of monthly margin change
- Break down changes into:
  - revenue / price
  - usage / volume
  - cost increases
  - customer or product mix
- Call out whether issues are broad-based or concentrated

5. Segmentation
- Show gross margin by:
  - cloud provider
  - customer tier
  - revenue band

6. Opportunities
- Estimate total annualized margin improvement opportunity if all sub-70% margin accounts were brought to 70%
- Identify top actionable levers:
  - pricing correction
  - infrastructure optimization
  - usage management
  - customer migration / hosting changes

7. Risks
- Flag accounts with worsening margin for 2+ consecutive months
- Flag concentration risk where a small number of accounts drive a large share of margin loss
- Flag known attribution or data quality issues that may affect interpretation

8. Final Output
- top 5 priority accounts
- recommended next actions
- estimated financial impact

Write the final report to outputs/monthly_margin_report.md.
If code is needed, create or update scripts in this repo and run them.

In addition to the standard FP&A analysis, produce a structured "Top Accounts by Margin Impact" section with the following format:

1. Summary Metrics (Top Panel)
- Total margin impact across top 20 material named accounts (sum of margin $)
- Worst single account (by margin $)
- Count of accounts with cost but zero revenue
- Highest cost per sync hour (if runtime available)

2. Top Accounts Selection
- Identify the top 20 material accounts ranked by absolute margin dollar loss (not %)
- Exclude immaterial accounts unless they have zero revenue with non-trivial cost

3. Dollar Impact Chart Data
- Output a ranked list of accounts with margin $ (negative values)
- Format for visualization (account name + margin $)
- Sort from worst to best

4. Account-Level Breakdown Table
For each of the top 20 accounts, output:
- Account name
- Customer tier
- Annualized revenue
- Annualized cost
- Margin $ (revenue - cost)
- Margin %
- Runtime (if available)
- Cost per runtime unit (e.g., $/sync hr)
- Key drivers (categorize into: DLW cost, connection cost, low scale, no revenue, etc.)

5. Driver Classification
Classify each account into 1–2 primary drivers using rules:
- "DLW cost" if compute-heavy cost dominates
- "connection" if connection count / overhead dominates
- "low scale" if revenue is very low relative to cost
- "no revenue" if revenue = 0

6. Output Format
- Present the top accounts table in a clean, tabular format
- Include a short labeled section header:
  "Top 20 Material Named Accounts by Margin Impact"
- Keep narrative minimal; prioritize structured output

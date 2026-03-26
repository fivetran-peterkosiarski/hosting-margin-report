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
import csv
import glob
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

DATA_GLOB = os.path.join("data", "*.csv")
OUTPUT_MD = os.path.join("outputs", "monthly_margin_report.md")
OUTPUT_CSV = os.path.join("outputs", "top20_margin_impact.csv")

MONTH_MAP = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def parse_period_from_filename(path: str) -> datetime:
    name = os.path.basename(path)
    m = re.search(r"for\s*\xa0?([A-Za-z]{3})\s+(\d{4})", name)
    if not m:
        m = re.search(r"for\s+([A-Za-z]{3})\s+(\d{4})", name)
    if not m:
        raise ValueError(f"Cannot parse month/year from {name}")

    mon = MONTH_MAP[m.group(1).lower()]
    year = int(m.group(2))
    return datetime(year, mon, 1)


def clean_account_name(name: str) -> str:
    cleaned = (name or "").strip()
    return cleaned if cleaned else "(Unmapped Account)"


def to_float(value) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def fmt_dollar(value: float) -> str:
    return f"${value:,.0f}"


def fmt_pct(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def fmt_runtime_hours(value: float) -> str:
    if value >= 1000:
        return f"{value / 1000:.1f}K"
    return f"{value:,.1f}"


def fmt_cost_per_sync_hour(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def load_month(path: str) -> List[Dict]:
    by_account: Dict[str, Dict] = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            account = clean_account_name(row.get("Salesforce Account Name", ""))
            item = by_account.setdefault(
                account,
                {
                    "account_name": account,
                    "tier": (row.get("Simplified Platform Tier") or "").strip() or "Unspecified",
                    "revenue": 0.0,
                    "cost": 0.0,
                    "dlw_cost": 0.0,
                    "connection_cost": 0.0,
                    "runtime_hours": 0.0,
                },
            )

            item["revenue"] += to_float(row.get("Annualized Revenue"))
            item["cost"] += to_float(row.get("Account Annualized Cost"))
            item["dlw_cost"] += to_float(row.get("Account DLW Cost"))
            item["connection_cost"] += to_float(row.get("Account Connections Cost"))
            item["runtime_hours"] += to_float(row.get("Total Donkey Runtime (hrs)"))

            if item["tier"] == "Unspecified":
                maybe_tier = (row.get("Simplified Platform Tier") or "").strip()
                if maybe_tier:
                    item["tier"] = maybe_tier

    rows = list(by_account.values())
    for row in rows:
        revenue = row["revenue"]
        cost = row["cost"]
        margin_dollar = revenue - cost
        row["margin_dollar"] = margin_dollar
        row["margin_pct"] = (margin_dollar / revenue) if revenue > 0 else None
        row["excess_cost_70"] = max(0.0, cost - 0.30 * revenue)
        row["cost_per_sync_hour"] = (cost / row["runtime_hours"]) if row["runtime_hours"] > 0 else None

    return rows


def is_material(row: Dict) -> bool:
    return (
        row["revenue"] >= 20000
        or row["cost"] >= 1000
        or row["margin_dollar"] <= -25000
    )


def classify_drivers(row: Dict) -> str:
    tags: List[str] = []
    revenue = row["revenue"]
    cost = row["cost"]
    dlw_cost = row["dlw_cost"]
    conn_cost = row["connection_cost"]
    runtime = row["runtime_hours"]
    cphr = row["cost_per_sync_hour"]
    margin = row["margin_dollar"]

    if revenue == 0 and cost > 0:
        tags.append("no revenue")

    if cost > 0 and (dlw_cost / cost >= 0.50 or dlw_cost >= 50000):
        tags.append("DLW cost")

    if cost > 0 and (conn_cost / cost >= 0.50 or (conn_cost >= 15000 and revenue < 100000)):
        tags.append("connection")

    if margin < 0 and revenue < 50000:
        tags.append("low scale")

    if runtime >= 1000 and cphr is not None and cphr >= 25:
        tags.append("high runtime")

    if not tags:
        if margin < 0:
            tags.append("low scale")
        else:
            tags.append("mixed")

    return ", ".join(tags[:2])


def get_period_files() -> List[Tuple[datetime, str]]:
    files = glob.glob(DATA_GLOB)
    if not files:
        raise SystemExit("No data files found in ./data")
    return sorted(((parse_period_from_filename(f), f) for f in files), key=lambda x: x[0])


def find_account(rows: List[Dict], account_name: str) -> Optional[Dict]:
    for row in rows:
        if row["account_name"] == account_name:
            return row
    return None


def main() -> None:
    period_files = get_period_files()
    if len(period_files) < 2:
        raise SystemExit("Need at least two monthly files for MoM comparisons")

    latest_period, latest_path = period_files[-1]
    prior_period, prior_path = period_files[-2]

    latest_rows = load_month(latest_path)
    prior_rows = load_month(prior_path)

    named_material = [
        r for r in latest_rows if r["account_name"] != "(Unmapped Account)" and is_material(r)
    ]
    top20_named = sorted(named_material, key=lambda r: r["margin_dollar"])[:20]

    unmapped_material_negative = [
        r
        for r in latest_rows
        if r["account_name"] == "(Unmapped Account)"
        and is_material(r)
        and r["margin_dollar"] < 0
    ]

    total_margin_impact = sum(r["margin_dollar"] for r in top20_named)
    worst_single = min(top20_named, key=lambda r: r["margin_dollar"], default=None)
    zero_revenue_named = sum(1 for r in top20_named if r["revenue"] == 0 and r["cost"] > 0)

    runtime_rows = [r for r in top20_named if r["cost_per_sync_hour"] is not None]
    highest_sync_hr = max(runtime_rows, key=lambda r: r["cost_per_sync_hour"], default=None)

    prior_top20_margin = 0.0
    for row in top20_named:
        prior_row = find_account(prior_rows, row["account_name"])
        if prior_row:
            prior_top20_margin += prior_row["margin_dollar"]
    mom_top20_change = total_margin_impact - prior_top20_margin

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)

    lines: List[str] = []
    lines.append(
        f"# {latest_period.strftime('%b %Y').upper()} — TOP 20 MATERIAL NAMED ACCOUNTS BY MARGIN IMPACT"
    )
    lines.append("")
    lines.append(f"Reporting month: **{latest_period.strftime('%B %Y')}**  ")
    lines.append(f"MoM comparison month: **{prior_period.strftime('%B %Y')}**")
    lines.append("")

    lines.append("## Summary metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Total margin impact | {fmt_dollar(total_margin_impact)} |")
    if worst_single:
        lines.append(
            f"| Worst single account | {worst_single['account_name']} ({fmt_dollar(worst_single['margin_dollar'])}) |"
        )
    else:
        lines.append("| Worst single account | N/A |")
    lines.append(f"| Zero-revenue named | {zero_revenue_named} |")
    if highest_sync_hr:
        lines.append(
            f"| Highest $/sync hr | {highest_sync_hr['account_name']} ({fmt_cost_per_sync_hour(highest_sync_hr['cost_per_sync_hour'])}) |"
        )
    else:
        lines.append("| Highest $/sync hr | N/A |")
    lines.append(f"| Top 20 margin MoM change | {fmt_dollar(mom_top20_change)} |")

    lines.append("")
    lines.append("## Dollar impact by account")
    lines.append("")
    lines.append("| account_name | margin_dollar |")
    lines.append("|---|---:|")
    for row in top20_named:
        lines.append(f"| {row['account_name']} | {fmt_dollar(row['margin_dollar'])} |")

    lines.append("")
    lines.append("## Account-level breakdown")
    lines.append("")
    lines.append(
        "| rank | account name | tier | annualized revenue | annualized cost | margin_dollar | margin_pct | donkey runtime hours | cost per sync hour | key drivers |"
    )
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---|")
    for idx, row in enumerate(top20_named, start=1):
        lines.append(
            "| {rank} | {name} | {tier} | {rev} | {cost} | {margin} | {margin_pct} | {runtime} | {cphr} | {drivers} |".format(
                rank=idx,
                name=row["account_name"],
                tier=row["tier"],
                rev=fmt_dollar(row["revenue"]),
                cost=fmt_dollar(row["cost"]),
                margin=fmt_dollar(row["margin_dollar"]),
                margin_pct=fmt_pct(row["margin_pct"]),
                runtime=fmt_runtime_hours(row["runtime_hours"]),
                cphr=fmt_cost_per_sync_hour(row["cost_per_sync_hour"]),
                drivers=classify_drivers(row),
            )
        )

    if unmapped_material_negative:
        row = unmapped_material_negative[0]
        lines.append("")
        lines.append("## Unmapped account note")
        lines.append(
            f"- Material negative unmapped impact present: {fmt_dollar(row['margin_dollar'])} margin_dollar on {fmt_dollar(row['revenue'])} revenue and {fmt_dollar(row['cost'])} cost."
        )

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["account_name", "margin_dollar"])
        writer.writeheader()
        for row in top20_named:
            writer.writerow(
                {
                    "account_name": row["account_name"],
                    "margin_dollar": f"{row['margin_dollar']:.2f}",
                }
            )

    print(f"Wrote {OUTPUT_MD}")
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Top 20 named accounts: {len(top20_named)}")


if __name__ == "__main__":
    main()

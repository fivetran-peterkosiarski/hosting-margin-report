import csv
import glob
import os
import re
from collections import defaultdict
from datetime import datetime

DATA_GLOB = os.path.join('data', '*.csv')
OUTPUT_PATH = os.path.join('outputs', 'monthly_margin_report.md')

MONTH_MAP = {m: i for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], start=1)}


def parse_period_from_filename(path: str):
    name = os.path.basename(path)
    m = re.search(r'for\s*\xa0?([A-Za-z]{3})\s+(\d{4})', name)
    if not m:
        m = re.search(r'for\s+([A-Za-z]{3})\s+(\d{4})', name)
    if not m:
        raise ValueError(f'Cannot parse month/year from {name}')
    mon = MONTH_MAP[m.group(1)]
    year = int(m.group(2))
    return datetime(year, mon, 1)


def fnum(x):
    return f"${x:,.0f}"


def fpct(x):
    return f"{x*100:.1f}%"


def load_month(path):
    by_account = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                rev = float(r['Annualized Revenue'])
                cost = float(r['Account Annualized Cost'])
            except Exception:
                continue
            account = (r['Salesforce Account Name'] or '').strip() or '(Unmapped Account)'
            item = by_account.setdefault(account, {
                'account': account,
                'tier': (r.get('Simplified Platform Tier') or '').strip() or 'Unspecified',
                'account_type': (r.get('Account Type') or '').strip() or 'Unspecified',
                'is_pbf': (r.get('Is Pbf') or '').strip().lower(),
                'revenue': 0.0,
                'cost': 0.0,
                'connections_cost': 0.0,
                'dlw_cost': 0.0,
                'runtime_hrs': 0.0,
            })
            item['revenue'] += rev
            item['cost'] += cost
            item['connections_cost'] += float(r.get('Account Connections Cost') or 0.0)
            item['dlw_cost'] += float(r.get('Account DLW Cost') or 0.0)
            item['runtime_hrs'] += float(r.get('Total Donkey Runtime (hrs)') or 0.0)
            if item['tier'] == 'Unspecified':
                item['tier'] = (r.get('Simplified Platform Tier') or '').strip() or item['tier']
            if item['is_pbf'] not in ('true', 'false'):
                item['is_pbf'] = (r.get('Is Pbf') or '').strip().lower() or item['is_pbf']
    rows = list(by_account.values())
    for row in rows:
        row['gm'] = (row['revenue'] - row['cost']) / row['revenue'] if row['revenue'] else 0.0
        row['margin_dollar'] = row['revenue'] - row['cost']
        row['cost_per_runtime_hr'] = (row['cost'] / row['runtime_hrs']) if row['runtime_hrs'] > 0 else None
    return rows


def summarize(rows):
    rev = sum(r['revenue'] for r in rows)
    cost = sum(r['cost'] for r in rows)
    gm = (rev - cost)/rev if rev else 0.0
    return rev, cost, gm


def excess_cost_70(row):
    return max(0.0, row['cost'] - 0.30*row['revenue'])


files = sorted(glob.glob(DATA_GLOB))
if not files:
    raise SystemExit('No data files found in data/.')

period_files = sorted(((parse_period_from_filename(p), p) for p in files), key=lambda x: x[0])
periods = [p for p,_ in period_files]
latest_period, latest_file = period_files[-1]
prev_period, prev_file = period_files[-2]

all_months = {dt: load_month(path) for dt, path in period_files}
latest_rows = all_months[latest_period]
prev_rows = all_months[prev_period]

latest_rev, latest_cost, latest_gm = summarize(latest_rows)
prev_rev, prev_cost, prev_gm = summarize(prev_rows)
ytd_months = [dt for dt in periods if dt.year == latest_period.year and dt <= latest_period]
ytd_gms = [summarize(all_months[dt])[2] for dt in ytd_months]
ytd_avg_gm = sum(ytd_gms)/len(ytd_gms)

material_latest = [r for r in latest_rows if r['revenue'] > 20000 or r['cost'] > 1000]

# Top issues by margin dollar loss vs 70% target
issues = []
for r in material_latest:
    ex = excess_cost_70(r)
    if ex > 0:
        rr = dict(r)
        rr['excess'] = ex
        issues.append(rr)
issues.sort(key=lambda x: x['excess'], reverse=True)
top10 = issues[:10]

# Driver decomposition by account-level deltas
prev_map = {r['account']: r for r in prev_rows}
latest_map = {r['account']: r for r in latest_rows}
all_accounts = set(prev_map) | set(latest_map)

delta_rev = 0.0
delta_cost = 0.0
rev_up = rev_down = cost_up = cost_down = 0.0
for a in all_accounts:
    pr = prev_map.get(a, {'revenue':0.0,'cost':0.0})
    lr = latest_map.get(a, {'revenue':0.0,'cost':0.0})
    drev = lr['revenue'] - pr['revenue']
    dcost = lr['cost'] - pr['cost']
    delta_rev += drev
    delta_cost += dcost
    if drev >= 0: rev_up += drev
    else: rev_down += drev
    if dcost >= 0: cost_up += dcost
    else: cost_down += dcost

# Concentration in top issues
total_excess = sum(i['excess'] for i in issues)
top5_excess = sum(i['excess'] for i in issues[:5])
top10_excess = sum(i['excess'] for i in issues[:10])

# Segments

def segment_table(rows, key_fn):
    agg = defaultdict(lambda: {'rev':0.0,'cost':0.0})
    for r in rows:
        k = key_fn(r)
        agg[k]['rev'] += r['revenue']
        agg[k]['cost'] += r['cost']
    out=[]
    for k,v in agg.items():
        gm=(v['rev']-v['cost'])/v['rev'] if v['rev'] else 0.0
        out.append((k,v['rev'],v['cost'],gm))
    out.sort(key=lambda x:x[1], reverse=True)
    return out

provider_segments = segment_table(material_latest, lambda r: 'PBF' if r['is_pbf']=='true' else 'Non-PBF')
tier_segments = segment_table(material_latest, lambda r: r['tier'])

def rev_band(r):
    rev = r['revenue']
    if rev < 50000: return '<$50k'
    if rev < 250000: return '$50k-$250k'
    if rev < 1000000: return '$250k-$1M'
    return '>$1M'

band_segments = segment_table(material_latest, rev_band)

# Risks: worsening margins for 2+ consecutive months (last 3 transitions)
monthly_maps = {dt: {r['account']: r for r in all_months[dt]} for dt in periods}
worsening=[]
for a in set().union(*[set(m.keys()) for m in monthly_maps.values()]):
    gms=[]
    for dt in periods:
        r=monthly_maps[dt].get(a)
        if r and r['revenue']>0:
            gms.append((dt,r['gm']))
    if len(gms) < 3:
        continue
    # check last 3 points strictly decreasing
    last=gms[-3:]
    if last[0][1] > last[1][1] > last[2][1]:
        latest_r = latest_map.get(a)
        if latest_r and (latest_r['revenue']>20000 or latest_r['cost']>1000):
            worsening.append((a,last[0][1],last[1][1],last[2][1],excess_cost_70(latest_r)))
worsening.sort(key=lambda x:x[4], reverse=True)

# monthly change drivers from top movers
movers=[]
for a in all_accounts:
    pr = prev_map.get(a, {'revenue':0.0,'cost':0.0})
    lr = latest_map.get(a, {'revenue':0.0,'cost':0.0})
    impact = abs((lr['cost']-pr['cost']) - 0.30*(lr['revenue']-pr['revenue']))
    movers.append((impact,a,lr['revenue']-pr['revenue'],lr['cost']-pr['cost']))
movers.sort(reverse=True)

lines=[]
lines.append('# Monthly Hosting Margin Report')
lines.append(f"Period analyzed: **{latest_period.strftime('%B %Y')}** (vs {prev_period.strftime('%B %Y')})")
lines.append('')
lines.append('## 1. Executive Summary')
lines.append(f"- Overall annualized gross margin was **{fpct(latest_gm)}** on **{fnum(latest_rev)}** revenue and **{fnum(latest_cost)}** cost; this is **{(latest_gm-prev_gm)*100:+.2f} pts MoM**.")
lines.append(f"- Margin pressure remains concentrated: top 5 sub-70% accounts represent **{fpct(top5_excess/total_excess) if total_excess else '0.0%'}** of total excess cost (target gap), equal to **{fnum(top5_excess)}** annualized.")
lines.append(f"- Total opportunity to bring all sub-70% material accounts to 70% margin is **{fnum(total_excess)}** annualized.")
lines.append(f"- MoM, revenue changed **{fnum(delta_rev)}** and cost changed **{fnum(delta_cost)}**; cost growth outpaced revenue growth on a target-margin basis by **{fnum(delta_cost - 0.30*delta_rev)}**.")
if worsening:
    lines.append(f"- **{len(worsening)}** material accounts show 2+ consecutive months of worsening margin into {latest_period.strftime('%B %Y')}; largest current target-gap exposures are listed in Risks.")

lines.append('')
lines.append('## 2. KPI Table')
lines.append('| KPI | Value |')
lines.append('|---|---:|')
lines.append(f"| Total annualized revenue | {fnum(latest_rev)} |")
lines.append(f"| Total annualized cost | {fnum(latest_cost)} |")
lines.append(f"| Gross margin % | {fpct(latest_gm)} |")
lines.append(f"| MoM revenue change | {fnum(latest_rev-prev_rev)} |")
lines.append(f"| MoM cost change | {fnum(latest_cost-prev_cost)} |")
lines.append(f"| MoM gross margin % change | {(latest_gm-prev_gm)*100:+.2f} pts |")
lines.append(f"| YTD average gross margin % ({latest_period.year}) | {fpct(ytd_avg_gm)} |")

lines.append('')
lines.append('## 3. Top Issues (Top 10 by Excess Cost vs 70% Target)')
lines.append('| Account | Annualized Revenue | Annualized Cost | Gross Margin % | Excess Cost vs 70% Target |')
lines.append('|---|---:|---:|---:|---:|')
for r in top10:
    lines.append(f"| {r['account']} | {fnum(r['revenue'])} | {fnum(r['cost'])} | {fpct(r['gm'])} | {fnum(r['excess'])} |")

lines.append('')
lines.append('## 4. Drivers')
lines.append(f"- **Revenue/price effect:** gross revenue movement was **{fnum(delta_rev)}** annualized ({fnum(rev_up)} increases offset by {fnum(rev_down)} decreases).")
lines.append(f"- **Cost increases:** total cost movement was **{fnum(delta_cost)}** annualized ({fnum(cost_up)} increases offset by {fnum(cost_down)} decreases).")
lines.append(f"- **Usage/volume + mix signal:** implied margin pressure from cost relative to 70% target rose by **{fnum(delta_cost - 0.30*delta_rev)}** MoM.")
lines.append(f"- **Concentration:** top 10 accounts are **{fpct(top10_excess/total_excess) if total_excess else '0.0%'}** of total excess cost; pressure is concentrated, not broad-based.")
lines.append('- Largest account-level movers by target-gap impact (MoM):')
for impact,a,drev,dcost in movers[:5]:
    lines.append(f"  - {a}: revenue {fnum(drev)}, cost {fnum(dcost)}, target-gap impact ~{fnum((dcost - 0.30*drev))}.")

lines.append('')
lines.append('## 5. Segmentation')
lines.append('### By cloud provider proxy (PBF flag; dataset does not include explicit cloud-provider field)')
lines.append('| Provider Segment | Revenue | Cost | Gross Margin % |')
lines.append('|---|---:|---:|---:|')
for k,rev,cost,gm in provider_segments:
    lines.append(f"| {k} | {fnum(rev)} | {fnum(cost)} | {fpct(gm)} |")

lines.append('')
lines.append('### By customer tier (Simplified Platform Tier)')
lines.append('| Tier | Revenue | Cost | Gross Margin % |')
lines.append('|---|---:|---:|---:|')
for k,rev,cost,gm in tier_segments:
    lines.append(f"| {k} | {fnum(rev)} | {fnum(cost)} | {fpct(gm)} |")

lines.append('')
lines.append('### By revenue band')
lines.append('| Revenue Band | Revenue | Cost | Gross Margin % |')
lines.append('|---|---:|---:|---:|')
for k,rev,cost,gm in band_segments:
    lines.append(f"| {k} | {fnum(rev)} | {fnum(cost)} | {fpct(gm)} |")

lines.append('')
lines.append('## 6. Opportunities')
lines.append(f"- Total annualized margin improvement if all material sub-70% accounts are lifted to 70%: **{fnum(total_excess)}**.")
lines.append('- Top actionable levers:')
lines.append('  - **Pricing correction:** target accounts where realized margin is deeply negative and revenue base can support repricing.')
lines.append('  - **Infrastructure optimization:** reduce compute/runtime load for high-cost accounts (especially where cost/revenue ratio has widened MoM).')
lines.append('  - **Usage management:** enforce workload guardrails and sync/runtime limits on accounts with disproportionate donkey runtime or connection footprint.')
lines.append('  - **Customer migration / hosting changes:** evaluate migration paths for structurally unprofitable hosting patterns (e.g., repeatedly negative-margin configurations).')

lines.append('')
lines.append('## 7. Risks')
if worsening:
    lines.append('- Accounts with 2+ consecutive months of worsening gross margin (latest three observations):')
    lines.append('| Account | Gross Margin Trend (oldest→latest) | Current Excess Cost vs 70% |')
    lines.append('|---|---:|---:|')
    for a,g1,g2,g3,ex in worsening[:10]:
        lines.append(f"| {a} | {g1*100:.1f}% → {g2*100:.1f}% → {g3*100:.1f}% | {fnum(ex)} |")
else:
    lines.append('- No material accounts met the 2+ consecutive month worsening threshold.')
lines.append(f"- Concentration risk: top 5 accounts contribute **{fpct(top5_excess/total_excess) if total_excess else '0.0%'}** of total excess cost.")
lines.append('- Data quality / attribution caveat: explicit cloud provider dimension is absent in source files, so provider segmentation is shown via PBF flag proxy only.')

lines.append('')
lines.append('## 8. Final Output')
lines.append('### Top 5 Priority Accounts')
for r in issues[:5]:
    lines.append(f"1. **{r['account']}** — excess cost {fnum(r['excess'])}, GM {fpct(r['gm'])}.")

lines.append('')
lines.append('### Recommended Next Actions')
lines.append('1. Launch pricing review for top-5 priority accounts within current quarter and set floor margin guardrails at renewal.')
lines.append('2. Run infra cost deep-dives on the top 10 accounts by excess cost and assign optimization owners with 30/60-day targets.')
lines.append('3. Apply usage controls for high-runtime / high-connection outliers and monitor weekly cost-to-revenue drift.')
lines.append('4. Define migration plans for structurally negative-margin configurations and track realized savings.')

lines.append('')
lines.append('### Estimated Financial Impact')
lines.append(f"- Full uplift to 70% across all material sub-70% accounts: **{fnum(total_excess)} annualized**.")
lines.append(f"- Near-term focus on top 5 accounts captures **{fnum(top5_excess)} annualized** ({fpct(top5_excess/total_excess) if total_excess else '0.0%'} of total opportunity).")

# Top 20 material named accounts by margin impact
def classify_drivers(row):
    drivers = []
    rev = row['revenue']
    cost = row['cost']
    if rev == 0 and cost > 0:
        drivers.append('no revenue')
    if cost > 0 and row['dlw_cost'] / cost >= 0.60:
        drivers.append('DLW cost')
    if cost > 0 and row['connections_cost'] / cost >= 0.40:
        drivers.append('connection')
    if rev > 0 and (rev < 50000 or rev < cost * 1.2):
        drivers.append('low scale')
    if not drivers:
        drivers.append('mixed')
    # Keep to 1-2 drivers per prompt.
    return ', '.join(drivers[:2])

top20_pool = []
for r in latest_rows:
    is_material = r['revenue'] > 20000 or r['cost'] > 1000
    zero_rev_exception = r['revenue'] == 0 and r['cost'] > 1000
    is_named = r['account'] != '(Unmapped Account)'
    if is_named and (is_material or zero_rev_exception) and r['margin_dollar'] < 0:
        top20_pool.append(r)
top20 = sorted(top20_pool, key=lambda r: abs(r['margin_dollar']), reverse=True)[:20]

top20_total_margin = sum(r['margin_dollar'] for r in top20)
worst_single = min(top20, key=lambda r: r['margin_dollar']) if top20 else None
zero_rev_count = sum(1 for r in top20 if r['revenue'] == 0 and r['cost'] > 0)
with_runtime = [r for r in top20 if r['cost_per_runtime_hr'] is not None]
highest_cost_runtime = max(with_runtime, key=lambda r: r['cost_per_runtime_hr']) if with_runtime else None

lines.append('')
lines.append('## Top 20 Material Named Accounts by Margin Impact')
lines.append('### Summary Metrics (Top Panel)')
lines.append(f"- Total margin impact across top 20 material named accounts: **{fnum(top20_total_margin)}**.")
if worst_single:
    lines.append(f"- Worst single account: **{worst_single['account']}** ({fnum(worst_single['margin_dollar'])}).")
lines.append(f"- Count of accounts with cost but zero revenue: **{zero_rev_count}**.")
if highest_cost_runtime:
    lines.append(f"- Highest cost per sync hour: **{highest_cost_runtime['account']}** at **${highest_cost_runtime['cost_per_runtime_hr']:,.2f}/hr**.")
else:
    lines.append("- Highest cost per sync hour: **N/A** (runtime data unavailable for selected accounts).")

lines.append('')
lines.append('### Dollar Impact Chart Data (Worst to Best)')
lines.append('| Rank | Account | Margin $ |')
lines.append('|---:|---|---:|')
for idx, r in enumerate(sorted(top20, key=lambda x: x['margin_dollar']), start=1):
    lines.append(f"| {idx} | {r['account']} | {fnum(r['margin_dollar'])} |")

lines.append('')
lines.append('### Account-Level Breakdown Table')
lines.append('| Account | Customer Tier | Annualized Revenue | Annualized Cost | Margin $ | Margin % | Runtime (hrs) | Cost / Runtime hr | Key Drivers |')
lines.append('|---|---|---:|---:|---:|---:|---:|---:|---|')
for r in sorted(top20, key=lambda x: x['margin_dollar']):
    runtime = f"{r['runtime_hrs']:,.1f}" if r['runtime_hrs'] else '0.0'
    cphr = f"${r['cost_per_runtime_hr']:,.2f}" if r['cost_per_runtime_hr'] is not None else 'N/A'
    lines.append(
        f"| {r['account']} | {r['tier']} | {fnum(r['revenue'])} | {fnum(r['cost'])} | {fnum(r['margin_dollar'])} | {fpct(r['gm'])} | {runtime} | {cphr} | {classify_drivers(r)} |"
    )

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Wrote {OUTPUT_PATH}')

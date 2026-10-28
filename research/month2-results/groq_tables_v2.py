import csv
import json
import random
import sys
from collections import defaultdict

# v2: same as groq_tables.py (B=5000, seed 20261012, scenario-cluster bootstrap)
# plus a zero-cell rule. When a cell has 0 successes (or all successes), the
# bootstrap interval collapses to a single point, so the bound is widened to
# the exact one-sided 95% bound computed with scenarios as the independent
# units: upper = 1 - 0.05**(1/k), lower = 0.05**(1/k), k = number of scenarios.
B = 5000
SEED = 20261012
OUT = sys.argv[1]
files = sys.argv[2:]

cells = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for path in files:
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            if d.get("record") != "run" or d.get("status") != "ok":
                continue
            kind = d.get("type")
            if kind == "attack":
                hit = d.get("attack_succeeded") is True
            elif kind == "benign":
                hit = d.get("task_completed") is True
            else:
                continue
            fam = str(d.get("family", "")).split("_")[0]
            families = ("ALL", fam) if fam not in ("", "None") else ("ALL",)
            for family in families:
                key = (d["model"], d["suite"], d["config"], family, kind)
                cell = cells[key][d["scenario_id"]]
                cell[0] += 1
                cell[1] += 1 if hit else 0

rng = random.Random(SEED)
rows = []
for key in sorted(cells):
    scen = list(cells[key].values())
    k = len(scen)
    n_runs = sum(s[0] for s in scen)
    succ = sum(s[1] for s in scen)
    rates = []
    for _ in range(B):
        draw = [scen[rng.randrange(len(scen))] for _ in scen]
        total = sum(s[0] for s in draw)
        rates.append(sum(s[1] for s in draw) / total)
    rates.sort()
    lo = rates[int(0.025 * B)]
    hi = rates[int(0.975 * B) - 1]
    note = ""
    if succ == 0:
        lo = 0.0
        hi = max(hi, 1 - 0.05 ** (1.0 / k))
        note = "zero_cell_upper_bound"
    elif succ == n_runs:
        hi = 1.0
        lo = min(lo, 0.05 ** (1.0 / k))
        note = "all_success_lower_bound"
    rows.append(list(key) + [k, n_runs, succ, round(succ / n_runs, 4), round(lo, 4), round(hi, 4), note])

header = ["model", "suite", "config", "family", "kind", "scenarios", "runs", "successes", "rate", "ci_low", "ci_high", "note"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print(" | ".join(header))
for r in rows:
    if r[3] == "ALL":
        print(" | ".join(str(x) for x in r))
print("written", OUT, len(rows), "rows")

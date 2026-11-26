"""Summarise a promptfoo results.json: pass rates per provider and per test,
plus every failed check with the reply that failed it.

Usage: python tools/summarize_promptfoo.py <results.json> [--failures]
"""
import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
show_fail = "--failures" in sys.argv
data = json.load(open(path, encoding="utf-8"))
rows = data["results"]["results"]

per_prov = defaultdict(lambda: [0, 0])
per_test = defaultdict(lambda: defaultdict(lambda: [0, 0]))
fails = []
for r in rows:
    prov = r["provider"].get("label") or r["provider"]["id"]
    desc = r.get("testCase", {}).get("description") or r.get("description", "?")
    ok = bool(r.get("success"))
    per_prov[prov][0] += ok
    per_prov[prov][1] += 1
    per_test[desc][prov][0] += ok
    per_test[desc][prov][1] += 1
    if not ok:
        out = (r.get("response") or {}).get("output") or r.get("error") or ""
        reasons = []
        for c in (r.get("gradingResult") or {}).get("componentResults", []) or []:
            if not c.get("pass"):
                a = c.get("assertion") or {}
                reasons.append(f"{a.get('type')}: {c.get('reason', '')}"[:300])
        fails.append((desc, prov, r.get("vars", {}).get("message", ""), out, reasons))

provs = sorted(per_prov)
print("## Pass rate per provider\n")
for p in provs:
    ok, n = per_prov[p]
    print(f"- {p}: {ok}/{n} ({100 * ok / n:.1f}%)")
print("\n## Per test\n")
print("| Test | " + " | ".join(provs) + " |")
print("|---|" + "---|" * len(provs))
for t in sorted(per_test):
    cells = []
    for p in provs:
        ok, n = per_test[t][p]
        cells.append(f"{ok}/{n}")
    print(f"| {t} | " + " | ".join(cells) + " |")
if show_fail:
    print(f"\n## Failures ({len(fails)})\n")
    for desc, prov, msg, out, reasons in sorted(fails):
        print(f"### {desc} [{prov}]\nPrompt: {msg}\nFailed checks: {reasons}\nReply:\n{out}\n")

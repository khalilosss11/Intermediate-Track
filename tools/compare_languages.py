"""Compare promptfoo results across languages for Quest 2.

Prints pass rates per language for each metric (language, accuracy,
tone_helpfulness), a per-case table, reply length per language, and every
failed check with the reply.

Usage: python tools/compare_languages.py quest-2-languages/results/results.json [--failures]
"""
import json
import statistics
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
rows = json.load(open(sys.argv[1], encoding="utf-8"))["results"]["results"]
LANGS = ["en", "fr", "ar"]

metric = defaultdict(lambda: [0, 0])          # (lang, metric) -> [pass, total]
case = defaultdict(lambda: [0, 0])            # (case, lang) -> [pass, total]
length = defaultdict(list)                    # lang -> word counts
fails = []
for r in rows:
    v = r["vars"]
    lang, cid = v["lang"], v["case"]
    out = (r.get("response") or {}).get("output") or ""
    length[lang].append(len(out.split()))
    case[(cid, lang)][0] += bool(r["success"])
    case[(cid, lang)][1] += 1
    for c in r["gradingResult"]["componentResults"]:
        m = (c.get("assertion") or {}).get("metric") or "other"
        metric[(lang, m)][0] += bool(c["pass"])
        metric[(lang, m)][1] += 1
        if not c["pass"]:
            fails.append((cid, lang, m, c.get("reason", ""), v["message"], out))

print("## Pass rate per language and metric\n")
print("| Metric | " + " | ".join(LANGS) + " |\n|---|" + "---|" * len(LANGS))
for m in ["accuracy", "tone_helpfulness", "language"]:
    cells = []
    for lang in LANGS:
        ok, n = metric[(lang, m)]
        cells.append(f"{ok}/{n} ({100 * ok / n:.0f}%)" if n else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")
print("\n## Average reply length (words)\n")
for lang in LANGS:
    print(f"- {lang}: {statistics.mean(length[lang]):.0f} words (median {statistics.median(length[lang]):.0f})")
print("\n## All checks passed, per case\n")
print("| Case | " + " | ".join(LANGS) + " |\n|---|" + "---|" * len(LANGS))
for cid in sorted({c for c, _ in case}):
    print(f"| {cid} | " + " | ".join(f"{case[(cid, l)][0]}/{case[(cid, l)][1]}" for l in LANGS) + " |")
if "--failures" in sys.argv:
    print(f"\n## Failed checks ({len(fails)})\n")
    for cid, lang, m, reason, msg, out in sorted(fails):
        print(f"### {cid} [{lang}] {m}\nPrompt: {msg}\nGrader: {reason[:400]}\nReply:\n{out}\n")

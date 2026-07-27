#!/usr/bin/env python3
"""Agent QA loop harness (#13): the render -> compare-Rubik -> flag loop that an
agent (a person, me, or Gemma once wired) drives to keep diacritics + spacing
at Google-Fonts-review quality.

It ties the existing tools together and emits ONE structured report:
  1. deterministic placement audit (scripts/audit_diacritics.py, both masters)
  2. Rubik side-by-side render (scripts/compare_diacritics.py)
  3. pointers to the diffenator2 gold-standard views (make review / review-rubik)
  4. an explicit review checklist an agent works down, and a FIX pointer

Placement fixes are deterministic (build_anchors.py); optical/drawing calls are
flagged for a human. Run: python scripts/qa_loop.py  (or: make qa-diacritics)
"""
import subprocess, sys, os, re

PY = ".venv/bin/python"
OUT = "out/qa-report.md"
os.makedirs("out", exist_ok=True)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

lines = ["# Virtua Grotesk — diacritic/spacing QA report", ""]

# 1. deterministic placement audit, both masters
lines.append("## 1. Placement audit (deterministic)")
for m in ("Regular", "Bold"):
    out = run([PY, "scripts/audit_diacritics.py", m])
    total = re.search(r"TOTAL placement problems: (\d+)", out)
    # strip the comb-definition noise from the summary line
    real = [l for l in out.splitlines() if l.startswith(("unanchored", "stale", "ogonek", "unknown"))]
    lines.append(f"- **{m}**: {total.group(1) if total else '?'} flags "
                 f"({'; '.join(real) if real else 'centered accents all correct'})")
lines.append("")

# 2. Rubik side-by-side render
lines.append("## 2. Rubik comparison render")
r = run([PY, "scripts/compare_diacritics.py", "out/diacritics-vs-rubik.png"])
lines.append(f"- `{r.strip().split()[-1] if r.strip() else 'out/diacritics-vs-rubik.png'}` "
             "— Virtua (V) stacked over Rubik (R) for the accented set.")
lines.append("")

# 3. gold-standard views
lines.append("## 3. Gold-standard (what a GF reviewer sees)")
lines.append("- `make review` -> out/review/diffenator2-report.html (Virtua)")
lines.append("- `make review-rubik` -> out/review-rubik/... (Rubik reference)")
lines.append("- Compare the **proofer** pages for centering, spacing, kerning.")
lines.append("")

# 4. review checklist + fix pointer
lines.append("## 4. Agent review checklist")
lines += [
    "- [ ] Audit clean for centered accents (section 1 shows no `stale`/`unanchored`).",
    "- [ ] In the Rubik render, accents match Rubik's centering + optical lean.",
    "- [ ] Ogonek / comma-caron (hand-tuned) still attach cleanly (optical — human call).",
    "- [ ] Flag mark DRAWING issues for the designer (flat tilde, tall circumflex,",
    "      off-8 mark y-coords) — placement is separate from shape.",
    "",
    "**Fix (placement):** `python scripts/build_anchors.py` re-centers every composite",
    "from the anchors; rerun it after any base-glyph edit. Optical/drawing = designer.",
]

report = "\n".join(lines)
open(OUT, "w").write(report + "\n")
print(report)
print(f"\n[written: {OUT}]")

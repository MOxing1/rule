#!/usr/bin/env python3
"""Static validation for this repository's classical Clash rule lists."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

def active_lines(path):
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith(("#", ";"))]

def check_list(path):
    lines = active_lines(path)
    seen = set()
    for line in lines:
        if line in seen:
            ERRORS.append(f"{path.name}: duplicate active rule: {line}")
        seen.add(line)
        if "," not in line:
            ERRORS.append(f"{path.name}: malformed rule: {line}")
    return lines

lists = {name: check_list(ROOT / name) for name in
         ("AI_CN.list", "AI.list", "Copilot.list", "Direct.list", "ProxyLite.list")}

# AI_CN and overseas AI must not overlap.
overlap = set(lists["AI_CN.list"]) & set(lists["AI.list"])
for rule in sorted(overlap):
    ERRORS.append(f"AI_CN.list / AI.list overlap: {rule}")

ini = (ROOT / "rule.ini").read_text(encoding="utf-8")
if "AI_CN.list" not in ini:
    ERRORS.append("rule.ini: AI_CN.list is not referenced")
if "Copilot.list" not in ini:
    ERRORS.append("rule.ini: Copilot.list is not referenced")
if "Bing.list" in ini and "Copilot" in ini:
    ERRORS.append("rule.ini: Copilot still points at Bing.list")
if "claude.ai.com" in "\n".join((ROOT / "AI.list").read_text(encoding="utf-8").splitlines()):
    ERRORS.append("AI.list: invalid claude.ai.com remains")
for line in ini.splitlines():
    if line.startswith("custom_proxy_group="):
        name = line.split("=", 1)[1].split("`", 1)[0]
        if name != name.strip():
            ERRORS.append(f"rule.ini: proxy group has leading/trailing whitespace: {name!r}")

if ERRORS:
    print("RULE VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in ERRORS))
    sys.exit(1)
print("RULE VALIDATION PASSED")
print(f"validated {sum(len(v) for v in lists.values())} active list rules")

#!/usr/bin/env python3
"""Restore latest user-provided chemistry map and enhance ORIGINAL biology 3D school."""
from pathlib import Path
import re

index = Path("index.html")
old = Path("index-before-biology-school-intro.html").read_text(encoding="utf-8")
tail = Path("scripts/latest-map-suffix.htmlpart").read_text(encoding="utf-8")
BASE_PREFIX = 3055219
base = old[:BASE_PREFIX] + tail
assert len(base) == 3143757, f"Latest uploaded map reconstruction changed: {len(base)}"
assert 'id="turkiyeMap"' in base and 'id="startLab"' in base and 'id="languagePicker"' in base
index.write_text(base, encoding="utf-8")
print("Latest uploaded Turkey map restored exactly:", len(base), "characters")

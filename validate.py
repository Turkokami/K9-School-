#!/usr/bin/env python3
"""
K9School site validator. Run AFTER `python3 build.py`, BEFORE every commit/push.
Exits non-zero if anything is broken so CI / pre-push hooks can gate on it.

Checks:
  1. Every JSON-LD <script> block parses as valid JSON.
  2. Every internal /link resolves to a real page or asset.
  3. Reports how many amber [fill-in] placeholders remain (warning, not failure).
"""
import re, json, sys, pathlib

PUB = pathlib.Path(__file__).parent / "public"
if not PUB.exists():
    print("ERROR: public/ not found. Run `python3 build.py` first.")
    sys.exit(2)

html_files = sorted(PUB.glob("*.html"))
errors = []

# 1) JSON-LD
for p in html_files:
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p.read_text(encoding="utf-8"), re.S):
        try:
            json.loads(m)
        except Exception as e:
            errors.append(f"Invalid JSON-LD in {p.name}: {e}")

# 2) internal links
names = {p.name for p in html_files} | {
    "styles.css", "main.js", "sitemap.xml", "robots.txt",
    "favicon.svg", "logo.svg", "og.png", "_redirects",
}
dl = PUB / "downloads"
if dl.exists():
    names |= {"downloads/" + p.name for p in dl.glob("*")}

for p in html_files:
    for href in re.findall(r'href="/([^"#]+?)(?:#[^"]*)?"', p.read_text(encoding="utf-8")):
        if href and not href.startswith(("http", "tel:", "mailto:")) and href not in names:
            errors.append(f"Broken internal link in {p.name}: /{href}")

# 3) placeholder count (informational)
placeholders = sum(len(re.findall(r'<span class="fill">', p.read_text(encoding="utf-8"))) for p in html_files)

print(f"Pages: {len(html_files)} | Placeholders remaining: {placeholders}")

if errors:
    print("\nVALIDATION FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("VALIDATION PASSED - JSON-LD valid, no broken internal links.")

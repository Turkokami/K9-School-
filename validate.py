#!/usr/bin/env python3
"""
K9School verification harness (Keystone Part 9.2). Run AFTER `python build.py`,
BEFORE every commit/push. Exits non-zero on any hard failure so CI / pre-push
hooks can gate on it.

HARD FAILS (exit 1):
  1. Every JSON-LD block parses, and every page's @graph carries the base nodes
     (WebSite, ImageObject, WebPage, BreadcrumbList, LocalBusiness).
  2. Every internal /link resolves to a real page or asset.
  3. Per-page SEO gate: exactly one H1; title present, unique, <=62 chars
     (rendered); meta description 110-165; canonical + og:image present;
     every <img> has alt.
WARNINGS (reported, non-blocking):
  - Word-count auditor (flags thin pages; the 3,000-word M1 floor is reported,
    not enforced, pending the owner decision for this non-local brand).
  - Duplicate-sentence scanner (12+ word sentences on 3+ pages).
  - Missing AEO quick-answer or Speakable hook.
Also reports remaining amber [fill-in] placeholders.
"""
import re, json, sys, pathlib, html as _html
from collections import defaultdict
try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
except Exception:
    pass

def strip_chrome(t):
    """Remove nav/footer/callbar/scripts so word-count & dedup see body content only."""
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<header[^>]*>.*?</header>", " ", t, flags=re.S)
    t = re.sub(r"<footer[^>]*>.*?</footer>", " ", t, flags=re.S)
    t = re.sub(r'<a class="callbar".*?</a>', " ", t, flags=re.S)
    return _html.unescape(re.sub(r"<[^>]+>", " ", t))

PUB = pathlib.Path(__file__).parent / "public"
if not PUB.exists():
    print("ERROR: public/ not found. Run `python build.py` first.")
    sys.exit(2)

html_files = sorted(PUB.glob("*.html"))
indexable = [p for p in html_files if p.name != "404.html"]
errors, warnings = [], []
def read(p): return p.read_text(encoding="utf-8")

BASE_NODES = {"WebSite", "ImageObject", "WebPage", "BreadcrumbList"}

# 1) JSON-LD parse + graph completeness
for p in indexable:
    t = read(p)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not blocks:
        errors.append(f"{p.name}: no JSON-LD block"); continue
    for m in blocks:
        try:
            data = json.loads(m)
        except Exception as e:
            errors.append(f"{p.name}: invalid JSON-LD: {e}"); continue
        graph = data.get("@graph", []) if isinstance(data, dict) else []
        types = set()
        for n in graph:
            tt = n.get("@type")
            types |= set(tt) if isinstance(tt, list) else ({tt} if tt else set())
        missing = BASE_NODES - types
        if missing:
            errors.append(f"{p.name}: schema missing base node(s) {sorted(missing)}")
        if "LocalBusiness" not in types:
            errors.append(f"{p.name}: schema missing LocalBusiness node")
        wp = next((n for n in graph if n.get("@type") == "WebPage"), None)
        if wp is not None and "speakable" not in wp:
            warnings.append(f"{p.name}: WebPage node missing speakable")

# 2) internal links resolve
names = {p.name for p in html_files} | {
    "styles.css", "main.js", "sitemap.xml", "robots.txt",
    "favicon.svg", "logo.svg", "og.png", "_redirects",
}
for sub in ("downloads", "images"):
    d = PUB / sub
    if d.exists():
        names |= {f"{sub}/" + q.name for q in d.glob("*")}
for p in html_files:
    for href in re.findall(r'href="/([^"#]+?)(?:#[^"]*)?"', read(p)):
        if href and not href.startswith(("http", "tel:", "mailto:")) and href not in names:
            errors.append(f"{p.name}: broken internal link /{href}")

# 3) per-page SEO gate
titles = defaultdict(list)
for p in indexable:
    t = read(p)
    h1 = len(re.findall(r'<h1[ >]', t))
    if h1 != 1:
        errors.append(f"{p.name}: {h1} H1 tags (need exactly 1)")
    mt = re.search(r"<title>([^<]*)</title>", t)
    title = _html.unescape(mt.group(1)) if mt else ""
    if not title:
        errors.append(f"{p.name}: missing <title>")
    elif len(title) > 62:
        errors.append(f"{p.name}: title {len(title)} chars (>62): {title}")
    titles[title].append(p.name)
    md = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = _html.unescape(md.group(1)) if md else ""
    if not (110 <= len(desc) <= 165):
        errors.append(f"{p.name}: meta description {len(desc)} chars (need 110-165)")
    if 'rel="canonical"' not in t:
        errors.append(f"{p.name}: missing canonical")
    if 'property="og:image"' not in t:
        errors.append(f"{p.name}: missing og:image")
    for tag in re.findall(r"<img[^>]*>", t):
        if "alt=" not in tag:
            errors.append(f"{p.name}: <img> missing alt")
    if "quick-answer" not in t:
        warnings.append(f"{p.name}: no AEO quick-answer block")
for title, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title {title!r} on {ps}")

# 4) word-count auditor (body only; report; thin = warn)
wc = {p.name: len(strip_chrome(read(p)).split()) for p in indexable}
for name, n in wc.items():
    if n < 400:
        warnings.append(f"{name}: thin body ({n} words)")

# 5) duplicate-sentence scanner (12+ words on 3+ pages, body only)
sent_pages = defaultdict(set)
for p in indexable:
    for s in re.split(r"[.!?]+", strip_chrome(read(p))):
        if len(s.split()) >= 12:
            sent_pages[re.sub(r"\s+", " ", s.strip().lower())].add(p.name)
dupe_sentences = sorted(((len(ps), s) for s, ps in sent_pages.items() if len(ps) >= 3), reverse=True)
for cnt, s in dupe_sentences[:15]:
    warnings.append(f"sentence on {cnt} pages: \"{s[:66]}...\"")

placeholders = sum(len(re.findall(r'<span class="fill">', read(p))) for p in html_files)
print(f"Pages: {len(html_files)} | Placeholders remaining: {placeholders} | "
      f"words/page {min(wc.values())}-{max(wc.values())}")

if warnings:
    print(f"\n{len(warnings)} warning(s) (non-blocking):")
    for w in warnings:
        print("  ~", w)
if errors:
    print(f"\nVALIDATION FAILED ({len(errors)}):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nVALIDATION PASSED - schema graph complete, SEO gate clean, no broken links.")

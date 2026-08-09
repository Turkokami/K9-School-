# -*- coding: utf-8 -*-
"""
K9School.net — Smart Site generator.
Emits a fast, mobile-first static site with a shared design system,
per-page SEO + JSON-LD schema, and segmented lead-capture forms.
Run:  python3 build.py   ->  outputs into ./public
"""
import os, html, pathlib

OUT = pathlib.Path(__file__).parent / "public"
OUT.mkdir(exist_ok=True)

SITE = "https://www.k9school.net"
BIZ = "Latimer School of Operational K9s"
PHONE = "(205) 966-8739"
PHONE_TEL = "+12059668739"
ADDR = "530 Hackney Street, Lincoln, AL 35096"
TAGLINE = "Proven in the Field. Not Just the Yard."
FORM_ACTION = "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"  # FILL-IN

NAV = [
    ("Agencies", "/agencies.html"),
    ("Training", "/training.html"),
    ("Consulting", "/consulting.html"),
    ("Detection Dogs", "/detection-dogs.html"),
    ("The Method", "/method.html"),
    ("Resources", "/resources.html"),
    ("About", "/about.html"),
    ("Contact", "/contact.html"),
]

CSS = r"""
:root{
  /* Brand: Black · Gold · Dark Navy Blue */
  --ink:#0b0d12; --ink2:#0f2444; --panel:#12294a; --steel:#3a4a63; --mute:#5c6b7a;
  --line:#e2e7ec; --paper:#ffffff; --wash:#f5f7f9; --wash2:#eef1f6;
  --amber:#c9a227; --amber-d:#8a6d14; --amber-l:#e4c25e; --green:#2f6f4f; --red:#b23b3b; --blue:#173a66;
  --black:#08090d; --navy:#0a1a33; --navy2:#0f2444; --navy3:#173a66;
  --gold:#c9a227; --gold-l:#e4c25e; --gold-d:#8a6d14;
  --maxw:1140px; --r:12px; --shadow:0 10px 34px rgba(10,26,51,.12);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.62;font-size:17px;background:var(--paper);-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{line-height:1.12;letter-spacing:-.02em;font-weight:800}
h1{font-size:clamp(2.1rem,5vw,3.5rem)}
h2{font-size:clamp(1.6rem,3.4vw,2.4rem)}
h3{font-size:1.22rem}
p{margin:0 0 1rem}
a{color:var(--blue);text-decoration:none}
img{max-width:100%;display:block}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.sec{padding:76px 0}
.sec.tight{padding:52px 0}
.eyebrow{font-size:.74rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--amber-d);margin-bottom:12px}
.lead{font-size:1.2rem;color:var(--steel)}
.center{text-align:center}
.muted{color:var(--mute)}
.mt0{margin-top:0}.mb0{margin-bottom:0}

/* NAV */
header.nav{position:sticky;top:0;z-index:50;background:rgba(8,9,13,.94);backdrop-filter:blur(10px);border-bottom:1px solid rgba(201,162,39,.28)}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:66px;max-width:var(--maxw);margin:0 auto;padding:0 24px}
.brand{display:flex;align-items:center;gap:10px;color:#fff;font-weight:800;letter-spacing:.02em;font-size:1.08rem}
.brand .mark{width:16px;height:16px;background:var(--amber);border-radius:3px;transform:rotate(45deg)}
.brand span{color:var(--amber)}
.nav-links{display:flex;align-items:center;gap:22px}
.nav-links a{color:#cdd8e0;font-size:.92rem;font-weight:600}
.nav-links a:hover{color:#fff}
.nav-cta{background:var(--amber);color:#0d141b!important;padding:9px 16px;border-radius:8px;font-weight:800}
.nav-cta:hover{background:var(--amber-l)}
.burger{display:none;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:6px}
.burger span{width:24px;height:2px;background:#fff;display:block}
.tel{color:#9fb4c4;font-weight:700;font-size:.9rem}

/* BUTTONS */
.btn{display:inline-block;background:var(--amber);color:#0d141b;font-weight:800;padding:14px 26px;border-radius:9px;font-size:1rem;border:0;cursor:pointer;transition:.15s}
.btn:hover{background:var(--amber-l);transform:translateY(-1px)}
.btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)}
.btn.ghost:hover{border-color:#fff;background:rgba(255,255,255,.06)}
.btn.dark{background:var(--ink);color:#fff}
.btn.sm{padding:10px 18px;font-size:.9rem}
.btnrow{display:flex;gap:14px;flex-wrap:wrap}

/* HERO */
.hero{background:radial-gradient(1200px 520px at 72% -12%,#1c3a63 0%,transparent 62%),linear-gradient(158deg,#05070c 0%,#0a1a33 52%,#0f2444 100%);color:#eef2f5;position:relative;overflow:hidden;border-bottom:3px solid var(--gold)}
.hero .wrap{padding-top:84px;padding-bottom:84px;position:relative;z-index:2}
.hero h1{color:#fff;max-width:16ch}
.hero .amb{color:var(--amber)}
.hero p.sub{font-size:1.28rem;color:#c4d2dd;max-width:60ch;margin:20px 0 30px}
.hero .kick{color:var(--amber);font-weight:800;letter-spacing:.16em;text-transform:uppercase;font-size:.8rem;margin-bottom:16px}
.hero-badges{display:flex;gap:22px;flex-wrap:wrap;margin-top:34px;color:#9fb4c4;font-size:.86rem;font-weight:600}
.hero-badges b{color:#fff}
.hero-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:46px;align-items:center}
.hero-media img{width:100%;border-radius:14px;border:1px solid rgba(255,255,255,.16);box-shadow:0 20px 55px rgba(0,0,0,.5);aspect-ratio:4/3;object-fit:cover}
.hero-media .cap{margin-top:10px;color:#9fb4c4;font-size:.82rem;font-weight:600;text-align:center}
@media(max-width:880px){.hero-grid{grid-template-columns:1fr;gap:26px}}

/* STAT BAND */
.statband{background:var(--ink2);color:#eef2f5}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center}
.stat .n{font-size:2.3rem;font-weight:800;color:var(--amber)}
.stat .l{font-size:.82rem;color:#bccbd6;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}

/* CARDS */
.grid{display:grid;gap:22px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:26px;transition:.15s}
.card.hover:hover{box-shadow:var(--shadow);transform:translateY(-2px)}
.card .ic{width:42px;height:42px;border-radius:9px;background:var(--wash2);display:flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:14px}
.card h3{margin-bottom:8px}
.card p{color:var(--mute);font-size:.96rem;margin-bottom:14px}
.card .go{font-weight:800;color:var(--amber-d);font-size:.92rem}
.audience{border-top:4px solid var(--gold)}
.audience.a{border-top-color:var(--navy3)}
.audience.g{border-top-color:var(--gold)}
.audience.m{border-top-color:var(--ink)}
.audience.p{border-top-color:#3a5a8c}

.wash{background:var(--wash)}
.dark{background:var(--ink);color:#eef2f5}
.dark h2,.dark h3{color:#fff}
.dark p{color:#c4d2dd}

/* PROOF / QUOTE */
.quote{border-left:4px solid var(--amber);padding:8px 0 8px 22px;font-size:1.15rem;font-style:italic;color:var(--steel)}
.quote cite{display:block;font-style:normal;font-weight:700;color:var(--ink);margin-top:10px;font-size:.92rem}
.ph{background:repeating-linear-gradient(45deg,#f0f3f6,#f0f3f6 12px,#eaeef2 12px,#eaeef2 24px);border:1px dashed #c3ccd4;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#8494a1;font-size:.82rem;font-weight:700;text-align:center;padding:22px;min-height:150px}
.fill{background:#fff6e6;border:1px solid #e6cf9f;color:#8a6417;padding:2px 7px;border-radius:5px;font-size:.86em;font-weight:700}

/* PHOTOS / GALLERY */
.shot{width:100%;border-radius:var(--r);border:1px solid var(--line);box-shadow:var(--shadow)}
.shot.tall{aspect-ratio:4/5;object-fit:cover}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:8px}
.gallery figure{margin:0;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:var(--ink);box-shadow:var(--shadow)}
.gallery figure img{width:100%;height:200px;object-fit:cover;display:block;transition:transform .35s ease}
.gallery figure:hover img{transform:scale(1.05)}
.gallery figcaption{padding:10px 13px;font-size:.82rem;color:var(--steel);font-weight:600;background:var(--paper)}

/* LIST */
.tick{list-style:none;margin:14px 0}
.tick li{position:relative;padding-left:30px;margin-bottom:10px;color:var(--steel)}
.tick li::before{content:"";position:absolute;left:4px;top:9px;width:9px;height:9px;background:var(--amber);border-radius:2px;transform:rotate(45deg)}

/* FAQ */
.faq details{border-bottom:1px solid var(--line);padding:16px 0}
.faq summary{font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:14px;font-size:1.05rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--amber-d);font-weight:800;font-size:1.4rem;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq details p{margin:12px 0 0;color:var(--mute)}

/* CTA STRIP */
.ctastrip{background:linear-gradient(120deg,#08090d,#0a1a33 55%,#173a66);color:#fff;border-radius:16px;padding:44px;text-align:center;border:1px solid rgba(201,162,39,.35)}
.ctastrip h2{color:#fff}
.ctastrip p{color:#c4d2dd;max-width:56ch;margin:12px auto 24px}

/* FORM */
.form{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:28px;box-shadow:var(--shadow)}
.form label{display:block;font-weight:700;font-size:.86rem;margin:14px 0 6px;color:var(--steel)}
.form input,.form select,.form textarea{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:8px;font-size:1rem;font-family:inherit;background:var(--wash)}
.form input:focus,.form select:focus,.form textarea:focus{outline:2px solid var(--amber);border-color:var(--amber);background:#fff}
.form .btn{width:100%;margin-top:20px}
.pathpick{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:6px}
.pathpick label{display:flex;align-items:center;gap:8px;background:var(--wash);border:1px solid var(--line);border-radius:8px;padding:12px;margin:0;cursor:pointer;font-weight:600;font-size:.9rem}

/* FOOTER */
footer{background:#08090d;color:#9fb0bd;padding:56px 0 30px;font-size:.9rem;border-top:3px solid var(--gold)}
footer h4{color:#fff;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}
footer a{color:#9fb0bd}
footer a:hover{color:#fff}
.footgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:30px;margin-bottom:34px}
.footgrid ul{list-style:none}
.footgrid li{margin-bottom:9px}
.footbrand .brand{margin-bottom:14px}
.copy{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:.82rem;color:#6b7c8a}

.crumb{font-size:.82rem;color:var(--mute);margin-bottom:10px}
.crumb a{color:var(--amber-d);font-weight:600}
.pillrow{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.pill{background:var(--wash2);border:1px solid var(--line);border-radius:20px;padding:5px 12px;font-size:.8rem;font-weight:700;color:var(--steel)}
.split{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;align-items:start}

@media(max-width:900px){
  .g4{grid-template-columns:repeat(2,1fr)}
  .g3{grid-template-columns:1fr}
  .footgrid{grid-template-columns:1fr 1fr}
  .split{grid-template-columns:1fr}
  .stats{grid-template-columns:repeat(2,1fr);gap:26px 8px}
}
@media(max-width:720px){
  .nav-links{position:fixed;inset:66px 0 auto 0;background:#08090d;flex-direction:column;align-items:stretch;gap:0;padding:10px 0;display:none;border-bottom:1px solid rgba(201,162,39,.3)}
  .nav-links.open{display:flex}
  .nav-links a{padding:13px 24px}
  .nav-links .nav-cta{margin:8px 24px;text-align:center}
  .burger{display:flex}
  .tel{display:none}
  .g2{grid-template-columns:1fr}
  .sec{padding:52px 0}
  .ctastrip{padding:30px 22px}
  .pathpick{grid-template-columns:1fr}
}
"""

JS = r"""
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),l=document.querySelector('.nav-links');
  if(b){b.addEventListener('click',function(){l.classList.toggle('open');});}
  // reflect chosen audience in hidden field label if present
  document.querySelectorAll('input[name="inquiry_type"]').forEach(function(r){
    r.addEventListener('change',function(){});
  });
});
"""

def nav_html(active):
    links = ""
    for label, href in NAV:
        cls = "nav-cta" if label == "Contact" else ""
        aria = ' aria-current="page"' if href.endswith(active) else ""
        links += f'<a href="{href}" class="{cls}"{aria}>{label}</a>'
    return f"""<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="/index.html"><span class="mark"></span>K9<span>SCHOOL</span></a>
    <nav class="nav-links">{links}<a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a></nav>
    <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>"""

FOOTER = f"""<footer>
  <div class="wrap">
    <div class="footgrid">
      <div class="footbrand">
        <a class="brand" href="/index.html"><span class="mark"></span>K9<span>SCHOOL</span></a>
        <p>{BIZ}. Operational detection dogs and certified handlers — proven in the field, not just the yard.</p>
        <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br>{ADDR}</p>
      </div>
      <div><h4>Programs</h4><ul>
        <li><a href="/agencies.html">For Agencies</a></li>
        <li><a href="/training.html">Handler &amp; Instructor Training</a></li>
        <li><a href="/consulting.html">Consulting</a></li>
        <li><a href="/detection-dogs.html">Detection Dogs</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="/about.html">About David Latimer</a></li>
        <li><a href="/proof.html">Proof &amp; Results</a></li>
        <li><a href="/certification.html">The LSOC Standard</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul></div>
      <div><h4>Get Started</h4><ul>
        <li><a href="/contact.html">Request a Capability Brief</a></li>
        <li><a href="/training.html#apply">Apply / Enroll</a></li>
        <li><a href="/consulting.html#book">Book an Assessment</a></li>
        <li><a href="/detection-dogs.html#availability">Check Availability</a></li>
      </ul></div>
    </div>
    <div class="copy">
      <span>&copy; 2026 {BIZ}. All rights reserved.</span>
      <span>Lincoln, Alabama &middot; Serving agencies &amp; teams nationwide</span>
    </div>
  </div>
</footer>"""

def page(slug, title, desc, body, schema="", active=None, canonical=None):
    active = active or ("/"+slug)
    canonical = canonical or f"{SITE}/{slug}"
    schema_block = f'<script type="application/ld+json">{schema}</script>' if schema else ""
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og.png">
<meta name="theme-color" content="#0a1a33">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<link rel="stylesheet" href="/styles.css">
{schema_block}
</head>
<body>
{nav_html(active)}
{body}
{FOOTER}
<script src="/main.js"></script>
</body>
</html>"""
    (OUT/slug).write_text(doc, encoding="utf-8")
    print("wrote", slug)

# ---------- shared schema ----------
ORG_SCHEMA = ('{"@context":"https://schema.org","@type":["LocalBusiness","ProfessionalService"],'
  f'"name":"{BIZ}","image":"{SITE}/og.jpg","@id":"{SITE}",'
  f'"url":"{SITE}","telephone":"{PHONE_TEL}","priceRange":"$$$",'
  '"address":{"@type":"PostalAddress","streetAddress":"530 Hackney Street","addressLocality":"Lincoln","addressRegion":"AL","postalCode":"35096","addressCountry":"US"},'
  '"areaServed":"US","founder":{"@type":"Person","name":"David Latimer"},'
  '"description":"Operational detection dog training, handler and instructor certification, program consulting, and placement-ready detection dogs for law enforcement, conservation, and private detection teams.",'
  '"knowsAbout":["detection dog training","narcotics detection","explosives detection","arson accelerant detection","bed bug detection","conservation detection","handler certification","K9 program development"]}')

def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' %
        (_json(q), _json(a)) for q,a in pairs)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items

import json as _j
def _json(s): return _j.dumps(s)

def faq_html(pairs):
    rows = ""
    for q,a in pairs:
        rows += f"<details><summary>{q}</summary><p>{a}</p></details>"
    return f'<div class="faq">{rows}</div>'

# clearly-marked placeholder helper
def fill(txt): return f'<span class="fill">[{txt}]</span>'

def img(name, alt, cls="shot", style="", eager=False):
    st = f' style="{style}"' if style else ""
    ld = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img class="{cls}" src="/images/{name}" alt="{html.escape(alt)}"{ld} decoding="async"{st}>'

def gallery(items):
    figs = "".join(
        f'<figure><img src="/images/{fn}" alt="{html.escape(cap)}" loading="lazy" decoding="async">'
        f'<figcaption>{html.escape(cap)}</figcaption></figure>'
        for fn, cap in items
    )
    return f'<div class="gallery">{figs}</div>'

# Curated field photos for the Proof gallery. Neutral, behavior-first captions —
# no outcome/accuracy claims (see Voice & Ideology Brief). Source images live in
# public/images/ (optimized from David's LSOC library).
FIELD_GALLERY = [
    ("lsoc-95-dog-points-to-odor.jpg", "Working a structure to source odor"),
    ("lsoc-74-freeze-alert.jpg", "Trained final response at source"),
    ("lsoc-5-mal-sitting-and-pointing.jpg", "Sit-and-stare response on a training problem"),
    ("lsoc-94-dog-uses-structure-to-get-to-source.jpg", "Using structure to reach source odor"),
    ("lsoc-75-mal-getting-to-source.jpg", "Detailing a vehicle to source"),
    ("lsoc-78-mal-sniffing-car.jpg", "Vehicle exterior search"),
    ("lsoc-8-dope-find.jpg", "Narcotics detection — vehicle search"),
    ("lsoc-60-contraband-find.jpg", "Contraband detection work"),
    ("lsoc-84-equipment-and-dope.jpg", "Narcotics and paraphernalia — detection work"),
    ("lsoc-121-dope-find-w-team.jpg", "Handler and dog after a find"),
    ("lsoc-67-jinx-and-money.jpg", "Currency detection — Jinx"),
    ("lsoc-46-chappy-and-deke.jpg", "Handler team — Chappy & Deke"),
    ("lsoc-88-cason-and-argo.jpg", "Handler team — Cason & Argo"),
    ("lsoc-96-william-and-zeus.jpg", "Handler team — William & Zeus"),
    ("lsoc-90-summer-and-sonya-win-class.jpg", "Certification day — Summer & Sonya"),
    ("lsoc-127-bedbug-team.jpg", "Bed bug detection team on-site"),
    ("lsoc-114-bedbug-dog-and-handler.jpg", "Bed bug inspection in progress"),
    ("lsoc-52-arson-dog-team.jpg", "Accelerant (arson) detection team"),
    ("lsoc-142-tracking-team-ak.jpg", "Tracking team in the field"),
    ("lsoc-54-tracking-dog-class.jpg", "Tracking class in training"),
    ("lsoc-111-rat-dog.jpg", "Rodent detection dog at work"),
    ("lsoc-112-me-laying-track-in-ak.jpg", "Laying a training track"),
    ("lsoc-119-clas-pic.jpg", "Handler certification class"),
    ("lsoc-32-luna-jump-for-toy.jpg", "Reward drive — the paycheck after the find"),
]

def photostrip(items, heading="The work, as it happens.", eyebrow="From the field", sub="", wash=False):
    subp = f'<p class="lead" style="max-width:64ch">{sub}</p>' if sub else ""
    cls = "sec tight wash" if wash else "sec tight"
    return (f'<section class="{cls}"><div class="wrap">'
            f'<div class="eyebrow">{eyebrow}</div><h2>{heading}</h2>{subp}'
            f'{gallery(items)}</div></section>')

# Per-page photo sets (3–5 each). Neutral, behavior-first captions per the Voice brief.
AGENCIES_PHOTOS = [
    ("lsoc-82-patrol-car.jpg", "K9 unit — marked patrol vehicle"),
    ("lsoc-108-dope-find.jpg", "Narcotics alert at a vehicle"),
    ("lsoc-21-dexter-and-bus-a.jpg", "Interior search — transit vehicle"),
    ("lsoc-141-dog-sniffing-lockers-2.jpg", "Facility search — lockers"),
    ("lsoc-51-two-new-dogs-hit-the-street.jpg", "New teams ready to deploy"),
]
TRAINING_PHOTOS = [
    ("lsoc-14-training-day-a.jpg", "Training day"),
    ("lsoc-106-dog-sniffing-board.jpg", "Foundation work on the scent board"),
    ("lsoc-101-lab-straining-at-leash.jpg", "Building drive on the leash"),
    ("lsoc-99-handler-and-dog-w-toy.jpg", "The reward after the find"),
    ("lsoc-130-scent-board.jpg", "The Scent Board System"),
]
CONSULTING_PHOTOS = [
    ("lsoc-93-handlers.jpg", "Handler cohort"),
    ("lsoc-119-clas-pic.jpg", "Certification class"),
    ("lsoc-53-two-53-new-arson-dog-teams.jpg", "New program teams stood up"),
    ("lsoc-77-training-day-patrol-cars.jpg", "Program training day"),
    ("lsoc-1-female-hndlrs-at-fed-prison.jpg", "Detection teams at a federal facility"),
]
DETECTION_PHOTOS = [
    ("lsoc-68-bedbug-dog-training.jpg", "Bed bug detection training"),
    ("lsoc-80-tracking-team-ak-2.jpg", "Tracking team in the field"),
    ("lsoc-138-dog-sniffing-truck.jpg", "Exterior vehicle search"),
    ("lsoc-122-dog-reaching-for-source.jpg", "Working to source odor"),
    ("lsoc-47-josh-and-aki.jpg", "Handler team — Josh & Aki"),
]
METHOD_PHOTOS = [
    ("lsoc-104-lab-freeze-alert.jpg", "Commitment — a trained final response at source"),
    ("lsoc-105-lab-saeching-for-source.jpg", "The search — before the sit"),
    ("lsoc-107-dog-sniffing-bd-2.jpg", "Detailing a scent board"),
    ("lsoc-109-dog-sniffing-bd-3.jpg", "Reading the change of behavior"),
    ("lsoc-98-bedbug-dog-working-board.jpg", "Working a detection problem"),
]
CERT_PHOTOS = [
    ("lsoc-45-david-and-marley.jpg", "Certified team — David & Marley"),
    ("lsoc-72-seth-and-vixen.jpg", "Certified team — Seth & Vixen"),
    ("lsoc-65-yance-and-friend.jpg", "Handler team on test day"),
    ("lsoc-42-michel-and-bugs.jpg", "Handler team — Michel & Bugs"),
    ("lsoc-90-summer-and-sonya-win-class.jpg", "Certification day — Summer & Sonya"),
]
RESOURCES_PHOTOS = [
    ("lsoc-123-me-and-2-search-dogs.jpg", "David with working dogs"),
    ("lsoc-19-luna-eng-comp-a.jpg", "Detection dog at work"),
    ("lsoc-28-dexter-on-car.jpg", "Vehicle exterior search"),
    ("lsoc-97-ak-team.jpg", "Detection team, Alaska"),
]
CONTACT_PHOTOS = [
    ("lsoc-12-me-tatsa-georgia-and-midnight.jpg", "David and the dogs"),
    ("lsoc-55-annie-and-tulip.jpg", "Handler team — Annie & Tulip"),
    ("lsoc-70-jasmine-and-jeff.jpg", "Handler team — Jasmine & Jeff"),
]
HOME_PHOTOS = [
    ("lsoc-128-bedbug-dog-team-in-br.jpg", "Bed bug detection team on-site"),
    ("lsoc-23-edge-in-bus.jpg", "Interior search — vehicle"),
    ("lsoc-31-edge-on-hay.jpg", "Detection dog — field training"),
    ("lsoc-96-william-and-zeus.jpg", "Handler team — William & Zeus"),
]
ABOUT_PHOTOS = [
    ("lsoc-7-me-na.jpg", "FBI National Academy graduate"),
    ("lsoc-136-me-and-two-search-dogs-2.jpg", "In the field with the dogs"),
    ("lsoc-73-me-and-handler-trng.jpg", "Working with a handler"),
    ("lsoc-100-me-teaching.jpg", "Teaching to the standard"),
]
# Resource-article photo sets (3 each), keyed by slug.
ARTICLE_PHOTOS = {
    "resources-choosing-a-detection-dog.html": [
        ("lsoc-3-beagles.jpg", "Candidate dogs come in many breeds"),
        ("lsoc-5-mal-sitting-and-pointing.jpg", "Evaluating drive and response"),
        ("lsoc-26-jinx-and-dope.jpg", "A finished narcotics dog"),
    ],
    "resources-become-a-k9-handler.html": [
        ("lsoc-92-training-day-patrol-cars.jpg", "Handler training day"),
        ("lsoc-96-william-and-zeus.jpg", "A certified handler team"),
        ("lsoc-13-bedbug-dog-hdlrs-and-dogs.jpg", "Handlers and their dogs"),
    ],
    "resources-starting-a-k9-program.html": [
        ("lsoc-51-two-new-dogs-hit-the-street.jpg", "New teams ready to deploy"),
        ("lsoc-120-training-day-patrol-cars.jpg", "Program training day"),
        ("lsoc-97-ak-team.jpg", "A stood-up detection team"),
    ],
    "resources-narcotics-detection-k9s.html": [
        ("lsoc-26-jinx-and-dope.jpg", "Narcotics dog with a find"),
        ("lsoc-116-dope-find.jpg", "Packaged narcotics located"),
        ("lsoc-69-dope-and-paraphernalia.jpg", "Narcotics and paraphernalia"),
    ],
    "resources-bed-bug-detection-dogs.html": [
        ("lsoc-113-bedbug-dog-on-dog-food-aisle.jpg", "Bed bug search — retail environment"),
        ("lsoc-68-bedbug-dog-training.jpg", "Bed bug detection training"),
        ("lsoc-114-bedbug-dog-and-handler.jpg", "Bed bug inspection in progress"),
    ],
    "resources-explosives-detection-k9.html": [
        ("lsoc-140-dog-sniffing-lockers-independent-work.jpg", "Facility search — high-consequence"),
        ("lsoc-138-dog-sniffing-truck.jpg", "Exterior vehicle search"),
        ("lsoc-82-patrol-car.jpg", "Operational K9 unit"),
    ],
    "resources-five-phases-detector-dog-behavior.html": [
        ("lsoc-95-dog-points-to-odor.jpg", "Detection — working the search"),
        ("lsoc-122-dog-reaching-for-source.jpg", "Commitment — driving to source"),
        ("lsoc-75-mal-getting-to-source.jpg", "Response — at source"),
    ],
    "resources-florida-v-harris-k9-handlers.html": [
        ("lsoc-60-contraband-find.jpg", "Documented recovery"),
        ("lsoc-96-william-and-zeus.jpg", "A court-defensible team"),
        ("lsoc-135-class-pic.jpg", "Certification records matter"),
    ],
    "resources-handler-influence-invisible-leash.html": [
        ("lsoc-103-lab-strains-on-leash.jpg", "Reading leash influence"),
        ("lsoc-102-lab-alerts.jpg", "Handler and dog as one system"),
        ("lsoc-73-me-and-handler-trng.jpg", "Training the human end of the leash"),
    ],
}

# Reusable callout for David's forthcoming book (purchase link added later)
def book_callout():
    return f"""
<div class="card" style="border-left-color:var(--gold);background:var(--wash2)">
  <div class="split" style="gap:22px;align-items:center">
    <div>
      <div class="eyebrow">From the book</div>
      <h3 class="mt0">The method, in David's own words.</h3>
      <p class="muted mb0">David Latimer's forthcoming book distills decades of detector-dog work into a single idea: <i>behavior is evidence</i>. The same principles that shape every dog and handler here are set out in full — from the search before the sit to surviving cross-examination.</p>
    </div>
    <div style="text-align:center">
      <div class="ph" style="min-height:150px;width:120px;margin:0 auto 12px">Cover<br>{fill('book cover image')}</div>
      <span class="btn dark sm" style="opacity:.7;cursor:default">Coming soon</span>
      <p class="muted" style="font-size:.75rem;margin-top:8px">{fill('purchase link — add when ready')}</p>
    </div>
  </div>
</div>"""

def form_fields(inquiry, extra_agency=False, extra_training=False, extra_consulting=False,
                extra_dogs=False, extra_all=False):
    """Segmented lead-capture form body. Posts to a form endpoint (FILL-IN)."""
    path = ""
    if extra_all:
        path = """
  <label>I'm reaching out as</label>
  <div class="pathpick">
    <label><input type="radio" name="inquiry_type" value="Agency" checked> Agency / LE</label>
    <label><input type="radio" name="inquiry_type" value="Handler/Trainer"> Handler / Trainer</label>
    <label><input type="radio" name="inquiry_type" value="Consulting"> Consulting / Program</label>
    <label><input type="radio" name="inquiry_type" value="Detection Dog"> Buying a dog</label>
  </div>"""
    else:
        path = f'<input type="hidden" name="inquiry_type" value="{inquiry}">'

    extra = ""
    if extra_agency:
        extra = """
  <label>Agency / department</label><input name="agency" placeholder="e.g. County Sheriff's Office">
  <label>Detection discipline(s) needed</label><input name="discipline" placeholder="Narcotics, explosives, firearms…">
  <label>Do you need the dog, handler certification, or both?</label>
  <select name="scope"><option>Finished dog</option><option>Handler certification</option><option>Both / full team</option><option>Program development</option></select>"""
    elif extra_training:
        extra = """
  <label>Which program?</label>
  <select name="program"><option>Handler Certification</option><option>Instructor Certification</option><option>Foundation Scent Detection</option><option>Field Deployment Training</option><option>Not sure yet</option></select>
  <label>Your experience level</label>
  <select name="experience"><option>New to detection</option><option>Some experience</option><option>Working handler</option><option>Experienced trainer</option></select>"""
    elif extra_consulting:
        extra = """
  <label>Organization</label><input name="agency" placeholder="Agency / company / org">
  <label>What do you need?</label>
  <select name="engagement"><option>Program development</option><option>Program audit / evaluation</option><option>K9 selection & testing</option><option>Handler / instructor development</option><option>Speaking / seminar</option></select>"""
    elif extra_dogs:
        extra = """
  <label>Discipline</label>
  <select name="discipline"><option>Bed bug</option><option>Arson / accelerant</option><option>Conservation</option><option>Narcotics</option><option>Explosives / firearms</option><option>Other</option></select>
  <label>Working environment</label><input name="environment" placeholder="Where will the dog work?">"""

    return f"""<form action="{FORM_ACTION}" method="POST">
  {path}
  <label>Name</label><input name="name" required placeholder="Full name">
  <label>Email</label><input type="email" name="email" required placeholder="you@example.com">
  <label>Phone</label><input name="phone" placeholder="Best number to reach you">{extra}
  <label>Tell us the mission / what you need</label><textarea name="message" rows="4" placeholder="A few lines on your goal, timeline, and context."></textarea>
  <input type="hidden" name="_subject" value="New {inquiry} inquiry — k9school.net">
  <button class="btn" type="submit">Send it to David</button>
  <p class="muted" style="font-size:.78rem;margin:12px 0 0">We reply personally, usually within {fill('response time')}. No spam, ever.</p>
</form>"""

# ============================================================
# HOME
# ============================================================
home_faq = [
 ("Do you work with departments outside Alabama?",
  f"Yes. We're based in Lincoln, Alabama and support agencies and working teams nationwide. Placement, on-site training, and handler certification are all available beyond the region — {fill('confirm any travel / logistics terms')}."),
 ("Are your dogs and handlers certified to a recognized standard?",
  "Every team is developed and evaluated against the LSOC courtroom-defensible standard — behavioral documentation, blind testing, and handlers who can explain the dog's work — so your records hold up in procurement and in court. See the certification page for details."),
 ("What disciplines do you cover?",
  "Narcotics, explosives, firearms, currency and electronic-storage detection for agencies, plus commercial disciplines including arson/accelerant, bed bug, and conservation detection."),
 ("How fast can we get started?",
  f"Most engagements begin with a short scoping call. Timelines depend on the program and dog availability — {fill('typical lead times to confirm')}."),
]
SELECTOR = r'''
<section class="sec wash" id="finder">
  <style>
    .finder{max-width:820px;margin:28px auto 0}
    .finder-prompt{font-weight:800;font-size:1.15rem;text-align:center;margin-bottom:18px;color:var(--navy)}
    .finder-opts{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .finder-opts button{font-family:inherit;font-size:1rem;font-weight:700;text-align:left;padding:16px 18px;border:1.5px solid var(--line);background:#fff;border-radius:10px;cursor:pointer;color:var(--ink);transition:.15s}
    .finder-opts button:hover{border-color:var(--gold);box-shadow:var(--shadow);transform:translateY(-1px)}
    .finder-r{background:linear-gradient(120deg,#08090d,#0a1a33 60%,#173a66);color:#fff;border:1px solid rgba(201,162,39,.35);border-radius:12px;padding:30px;text-align:center}
    .finder-r h3{color:#fff;font-size:1.35rem;margin-bottom:8px}
    .finder-r p{color:#c4d2dd;max-width:52ch;margin:0 auto 18px}
    .finder-r .again{display:inline-block;margin-top:14px;color:#9fb4c4;font-size:.85rem;font-weight:700;cursor:pointer;background:none;border:0}
    @media(max-width:640px){.finder-opts{grid-template-columns:1fr}}
  </style>
  <div class="wrap">
    <div class="center"><div class="eyebrow">30-second finder</div><h2>Not sure where you fit? Start here.</h2></div>
    <div class="finder">
      <div id="fq">
        <p class="finder-prompt">Which best describes you?</p>
        <div class="finder-opts">
          <button data-k="agency">🛡&#65039; I'm with an agency or law enforcement</button>
          <button data-k="handler">🎓 I want to become a handler or trainer</button>
          <button data-k="program">📋 I'm building or fixing a K9 program</button>
          <button data-k="business">🐕 I need a detection dog for my business/org</button>
        </div>
      </div>
      <div class="finder-r" id="fr" hidden></div>
    </div>
  </div>
  <script>
  (function(){
    var R={
      agency:{h:"Start with a Capability Brief",p:"You need dogs and handlers that hold up in deployment and in court. Send your mission profile and David responds personally with fit, timeline, and options.",l:"Go to the Agencies hub",u:"/agencies.html#brief"},
      handler:{h:"Handler & Instructor Training",p:"Field-first certification that makes you deployable, not just credentialed. Foundation, handler, and instructor tracks.",l:"Explore Training",u:"/training.html#apply"},
      program:{h:"Program Consulting",p:"Stand up a new detection program or fix the one you have. Start with a standards-based assessment of the gaps.",l:"Book an Assessment",u:"/consulting.html#book"},
      business:{h:"Commercial Detection Dogs",p:"A placement-ready dog selected for the environment it will actually work in — bed bug, arson, conservation and more — with handler training included.",l:"Check Availability",u:"/detection-dogs.html#availability"}
    };
    var q=document.getElementById('fq'),r=document.getElementById('fr');
    q.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        var d=R[b.getAttribute('data-k')];
        r.innerHTML='<h3>'+d.h+'</h3><p>'+d.p+'</p><a class="btn" href="'+d.u+'">'+d.l+'</a><br><button class="again" id="fagain">← start over</button>';
        q.hidden=true;r.hidden=false;
        document.getElementById('fagain').addEventListener('click',function(){r.hidden=true;q.hidden=false;});
      });
    });
  })();
  </script>
</section>
'''

home_body = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
     <div class="hero-copy">
      <div class="kick">Operational Detection K9s &middot; Since {fill('year')}</div>
      <h1>Proven in the Field. <span class="amb">Not Just the Yard.</span></h1>
      <p class="sub">Detection dogs and handlers built to hold up where it counts — reliable under pressure, defensible in court, ready for real deployment. Trusted by agencies and working teams nationwide.</p>
      <div class="btnrow">
        <a class="btn" href="/contact.html">Request a Capability Brief</a>
        <a class="btn ghost" href="/training.html">Explore Training</a>
      </div>
      <div class="hero-badges">
        <span><b>LSOC</b> Courtroom-Defensible Standard</span>
        <span><b>Train &middot; Certify &middot; Consult &middot; Place</b></span>
        <span><b>{ADDR}</b></span>
      </div>
     </div>
     <div class="hero-media">
      {img('lsoc-135-class-pic.jpg', 'A full class of K9 officers and their certified detection dogs with patrol vehicles', cls='', eager=True)}
      <div class="cap">Certified K9 teams — officers, handlers, and dogs trained to the LSOC standard.</div>
     </div>
    </div>
  </div>
</section>

<section class="statband sec tight">
  <div class="wrap"><div class="stats">
    <div class="stat"><div class="n">{fill('20+')}</div><div class="l">Years operational experience</div></div>
    <div class="stat"><div class="n">{fill('120+')}</div><div class="l">Teams trained &amp; deployed</div></div>
    <div class="stat"><div class="n">{fill('40+')}</div><div class="l">Agencies &amp; orgs served</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Trained to the LSOC standard</div></div>
  </div></div>
</section>

<section class="sec">
  <div class="wrap center">
    <div class="eyebrow">Find your path</div>
    <h2>One standard. Four ways we work with you.</h2>
    <p class="lead" style="max-width:60ch;margin:14px auto 0">Whether you're deploying a K9 unit, becoming a handler, fixing a program, or buying a working dog — start where you fit.</p>
    <div class="grid g4" style="margin-top:40px;text-align:left">
      <a class="card hover audience a" href="/agencies.html"><div class="ic">🛡️</div><h3>Agencies</h3><p>Finished detection dogs and certified handlers your unit can deploy with confidence.</p><span class="go">For law enforcement →</span></a>
      <a class="card hover audience g" href="/training.html"><div class="ic">🎓</div><h3>Handlers &amp; Trainers</h3><p>Handler and instructor certification that makes you ready on day one — not just credentialed.</p><span class="go">Courses &amp; seminars →</span></a>
      <a class="card hover audience m" href="/consulting.html"><div class="ic">📋</div><h3>Consulting</h3><p>Stand up a new detection program, or fix and audit the one you have.</p><span class="go">Program help →</span></a>
      <a class="card hover audience p" href="/detection-dogs.html"><div class="ic">🐕</div><h3>Detection Dogs</h3><p>Placement-ready dogs for bed bug, arson, conservation, narcotics and more.</p><span class="go">Check availability →</span></a>
    </div>
  </div>
</section>

{SELECTOR}

<section class="sec">
  <div class="wrap split">
    <div>
      <div class="eyebrow">Why K9School</div>
      <h2>The buyers we serve can't afford a team that fails.</h2>
      <p class="lead">A dog in a patrol car or a screening line is a liability decision before it's a training decision. We build teams that stand up to the real test — the deployment, the audit, the courtroom.</p>
      <ul class="tick">
        <li><b>Behavior is evidence.</b> We train the search before the sit — reading the dog, not just rewarding the final response. <a href="/method.html">See the method →</a></li>
        <li><b>Field-first training.</b> Practical readiness for real-world deployment, not controlled-yard performance alone.</li>
        <li><b>The whole team.</b> We train the dog <i>and</i> the human end of the leash, because reliability is a team property.</li>
        <li><b>Courtroom-defensible.</b> Evaluated to the LSOC standard with blind testing and documentation that stands up in court — from a retired chief and FBI National Academy graduate who testifies as an expert.</li>
      </ul>
      <a class="btn dark" href="/about.html">Meet David Latimer</a>
    </div>
    <div>
      {img('lsoc-125-dog-and-toy.jpg', 'Detection dog driving to a training reward — reading the dog through the response')}
      <div class="card" style="margin-top:18px">
        <div class="quote">{fill('Short, specific agency testimonial — the result the dog/handler delivered in the field.')}<cite>— {fill('Name, Title, Agency')}</cite></div>
      </div>
    </div>
  </div>
</section>

{photostrip(HOME_PHOTOS, heading="One standard, many missions.", sub="Narcotics, bed bug, arson, tracking and more — the same field-first approach across every discipline.", wash=True)}

<section class="sec">
  <div class="wrap">
    <div class="center"><div class="eyebrow">Common questions</div><h2>Straight answers</h2></div>
    <div style="max-width:820px;margin:30px auto 0">{faq_html(home_faq)}</div>
  </div>
</section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Tell us what you need to deploy.</h2>
  <p>Send a short brief and David will come back with a straight assessment of fit, timeline, and next steps.</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="/contact.html">Request a Capability Brief</a><a class="btn ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
</div></div></section>
"""
home_schema = "[" + ORG_SCHEMA + "," + faq_schema(home_faq) + "]"
page("index.html", f"{BIZ} — {TAGLINE}",
     "Operational detection dogs and certified handlers for law enforcement, conservation, and private detection teams. Trained, certified, and placed to the LSOC courtroom-defensible standard. Proven in the field, not just the yard.",
     home_body, schema=home_schema, active="/index.html")

# ============================================================
# Reusable hub builder
# ============================================================
def hub(slug, cls, eyebrow, h1, sub, cta_label, cta_href, proof_items, offer_html, faq, seo_title, seo_desc, crumb, photos=None):
    faq_h = faq_html(faq)
    photos_h = photostrip(photos) if photos else ""
    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="crumb"><a href="/index.html">Home</a> / {crumb}</div>
    <div class="kick">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="btnrow"><a class="btn" href="{cta_href}">{cta_label}</a><a class="btn ghost" href="tel:{PHONE_TEL}">Call David: {PHONE}</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="eyebrow">Proof that matters to you</div>
    <h2>Built to remove your risk.</h2>
    <div class="grid g3" style="margin-top:28px">{proof_items}</div>
  </div>
</section>

<section class="sec wash">
  <div class="wrap">{offer_html}</div>
</section>

{photos_h}

<section class="sec">
  <div class="wrap"><div class="center"><div class="eyebrow">Before you decide</div><h2>The questions you're already asking</h2></div>
  <div style="max-width:820px;margin:30px auto 0">{faq_h}</div></div>
</section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>{h1_cta(h1)}</h2>
  <p>{sub}</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="{cta_href}">{cta_label}</a></div>
</div></div></section>
"""
    schema = "[" + ORG_SCHEMA + "," + faq_schema(faq) + "]"
    page(slug, seo_title, seo_desc, body, schema=schema, active="/"+slug)

def h1_cta(h1): return "Ready when you are."

def proof_card(icon, title, body):
    return f'<div class="card"><div class="ic">{icon}</div><h3>{title}</h3><p>{body}</p></div>'

# ---- AGENCIES ----
ag_offer = f"""
<div class="split">
 <div>
  <div class="eyebrow">What you get</div>
  <h2>Finished dogs and certified handlers — deployment-ready.</h2>
  <p class="lead">We deliver detection teams your unit can put to work, with the records to back them.</p>
  <ul class="tick">
   <li>Single- and dual-purpose detection dogs (narcotics, explosives, firearms, currency, ESD).</li>
   <li>Handler certification so the human end of the leash is as reliable as the dog.</li>
   <li>Documented reliability to the LSOC courtroom-defensible standard — training records, blind testing, and behavioral documentation.</li>
   <li>Post-placement support and maintenance training options.</li>
   <li>Program development, audits, and <a href="/consulting.html">expert-witness / litigation support</a> available.</li>
  </ul>
  <div class="pillrow"><span class="pill">Placement from {fill('$ price')}</span><span class="pill">{fill('typical timeline')}</span></div>
  <p style="margin-top:14px"><a class="btn dark sm" href="/downloads/K9School-Agency-Capability-Brief.pdf">⬇ Download the 1-page capability brief (PDF)</a></p>
  <p class="muted" style="font-size:.85rem">Hand it up your chain of command — everything a decision-maker needs on one page.</p>
 </div>
 <div class="form" id="brief">
  <h3 class="mt0">Request a Capability Brief</h3>
  <p class="muted" style="font-size:.9rem">Tell us your mission profile. David responds personally.</p>
  {form_fields("Agency / Law Enforcement", extra_agency=True)}
 </div>
</div>
"""
ag_proof = (proof_card("🎯","Deployment case studies",
              f"Real outcomes from real deployments. {fill('Add 2–3 short case studies with measurable results.')}") +
            proof_card("⚖️","Courtroom-defensible by design",
              "Teams trained for scrutiny, not just success — behavioral documentation, blind testing, and handlers who can explain what the dog actually did. Led by a retired chief and FBI National Academy graduate who testifies as an expert.") +
            proof_card("📜","Documented reliability",
              "Every team evaluated to the LSOC courtroom-defensible standard — the training records and testing history procurement and courts require."))
ag_faq = [
 ("Will these teams hold up to a court challenge?",
  "That's the point. Teams are trained to the LSOC courtroom-defensible standard with documented records and blind testing, so reliability is demonstrable, not just asserted. Our approach is grounded in the governing case law — Harris, Jardines, Caballes, Rodriguez — and in training handlers to separate observation from interpretation on the stand."),
 ("Do you provide expert-witness or case-review support?",
  "Yes. David is a retired chief of police and FBI National Academy graduate who reviews detector-dog cases and testifies as an expert — always on the basis of honest evaluation, never to manufacture a result. See Consulting for litigation support."),
 ("Do you provide the dog, the training, or both?",
  "Both. You can acquire a finished dog, certify your handler with it, or have us develop your whole program end to end."),
 ("What about maintenance after placement?",
  f"We offer maintenance training and support so performance doesn't drift. {fill('Confirm maintenance package terms.')}"),
 ("Can you support federal or multi-agency requirements?",
  f"Yes. {fill('Note any specific approvals/vetting relevant to federal work.')}"),
]
hub("agencies.html","a","For Law Enforcement Agencies",
    "Detection K9s your unit can deploy with confidence.",
    "For procurement leads and K9 supervisors who can't afford a team that fails in the field — dogs and handlers proven in deployment and documented to a defensible standard.",
    "Request a Capability Brief","/agencies.html#brief", ag_proof, ag_offer, ag_faq,
    "Detection Dogs & Handler Certification for Agencies | K9School",
    "Finished detection dogs and certified handlers for law enforcement — narcotics, explosives, firearms and more, documented to the LSOC standard. Request a capability brief.",
    "Agencies", photos=AGENCIES_PHOTOS)

# ---- TRAINING ----
tr_offer = f"""
<div class="eyebrow">Programs</div>
<h2>Become a handler or trainer who's ready on day one.</h2>
<div class="grid g2" style="margin-top:24px">
  <div class="card"><h3>Handler Certification</h3><p class="muted">Build a reliable, court-defensible detection team — dog and handler together.</p><div class="pillrow"><span class="pill">From {fill('$ price')}</span><span class="pill">{fill('duration')}</span><span class="pill">Next cohort: {fill('date')}</span></div><a class="btn sm dark" href="#apply">Apply</a></div>
  <div class="card"><h3>Instructor Certification</h3><p class="muted">Advance from handler to instructor and train teams to standard.</p><div class="pillrow"><span class="pill">From {fill('$ price')}</span><span class="pill">{fill('duration')}</span></div><a class="btn sm dark" href="#apply">Apply</a></div>
  <div class="card"><h3>Foundation Scent Detection</h3><p class="muted">The core detection foundation done right from the start.</p><div class="pillrow"><span class="pill">From {fill('$ price')}</span></div><a class="btn sm dark" href="#apply">Enroll</a></div>
  <div class="card"><h3>Field Deployment Training</h3><p class="muted">Bridge the gap from the yard to real-world environmental searches.</p><div class="pillrow"><span class="pill">{fill('price / inquiry')}</span></div><a class="btn sm dark" href="#apply">Inquire</a></div>
</div>
<div class="card" style="margin-top:24px;background:var(--wash2)">
  <div class="split" style="gap:24px">
   <div><h3 class="mt0">Not ready to enroll yet?</h3><p class="muted mb0">Get the full program catalog &amp; syllabi — curriculum, outcomes, and what each track certifies.</p></div>
   <div style="align-self:center"><a class="btn" href="/downloads/K9School-Program-Catalog.pdf">⬇ Get the catalog (PDF)</a></div>
  </div>
</div>
<div class="form" id="apply" style="margin-top:30px;max-width:720px">
  <h3 class="mt0">Apply / Join the next cohort</h3>
  {form_fields("Handler / Trainer Training", extra_training=True)}
</div>
"""
tr_proof = (proof_card("👁️","Learn to read the dog","We teach the search before the sit — the Five Phases, reading behavior, and the Scent Board System — so you handle the dog you actually have. <a href='/method.html'>The method →</a>") +
            proof_card("✅","Outcomes, not attendance","You leave able to run a reliable, court-defensible team — because we train the human end of the leash, hard.") +
            proof_card("🧭","A real career path","Foundation → handler → instructor. Grow with a standard behind you."))
tr_faq = [
 ("Do I need prior experience?",
  f"No formal experience is required for foundation and handler tracks, though it helps. {fill('State any prerequisites per course.')}"),
 ("Is financing available?",
  f"{fill('Confirm whether financing / payment plans are offered.')}"),
 ("Where does training take place?",
  f"On-site in Lincoln, Alabama, with field components. {fill('Add lodging / travel info and any hybrid/online elements.')}"),
 ("What certification do I earn?",
  "Certification to the LSOC standard, documenting your team's reliability to a recognized benchmark."),
]
hub("training.html","g","Handler &amp; Instructor Training",
    "Ready on day one — not just certified.",
    "Handler certification, instructor certification, and foundation detection training built around field competence and a standard that stands up when it matters.",
    "Apply / Enroll","/training.html#apply", tr_proof, tr_offer, tr_faq,
    "Detection Dog Handler & Instructor Certification Courses | K9School",
    "Handler and instructor certification and foundation scent-detection training. Field-first, outcome-driven, and certified to the LSOC standard. Apply or get the syllabus.",
    "Training", photos=TRAINING_PHOTOS)

# ---- CONSULTING ----
co_offer = f"""
<div class="split">
 <div>
  <div class="eyebrow">Engagements</div>
  <h2>Stand up a program — or fix the one you have.</h2>
  <ul class="tick">
   <li><b>Operational program development.</b> Design a detection program from selection to deployment.</li>
   <li><b>Program audits &amp; evaluation.</b> An honest, standards-based review of where your program leaks reliability.</li>
   <li><b>Expert witness &amp; litigation support.</b> Case review and testimony from a retired chief and FBI National Academy graduate — honest evaluation, for prosecution or defense, never a manufactured result.</li>
   <li><b>K9 selection &amp; testing.</b> Buy the right dog — scent ability, environmental confidence, search drive, stability.</li>
   <li><b>Handler &amp; instructor development.</b> Level up your people to the standard.</li>
   <li><b>Speaking &amp; seminars.</b> Bring operational detection training to your team or event.</li>
  </ul>
  <div class="pillrow"><span class="pill">Custom-quoted</span><span class="pill">Remote or on-site</span></div>
 </div>
 <div class="form" id="book">
  <h3 class="mt0">Book a Program Assessment</h3>
  <p class="muted" style="font-size:.9rem">A focused call to scope your program and its gaps.</p>
  {form_fields("Consulting / Program", extra_consulting=True)}
  <p style="margin-top:14px"><a class="btn dark sm" href="/downloads/K9School-Expert-Witness.pdf">⬇ Expert witness &amp; case review (PDF)</a></p>
 </div>
</div>
"""
co_proof = (proof_card("🔍","Audit methodology","A structured, standards-based evaluation — not opinions. You get a clear picture and a fix-list.") +
            proof_card("📐","The LSOC standard","We assess and build against a defined, courtroom-defensible benchmark, so improvements are measurable.") +
            proof_card("📈","Program outcomes",f"Before-and-after results from programs we've shaped. {fill('Add program case studies.')}"))
co_faq = [
 ("We already have a program — can you just audit it?",
  "Yes. Many engagements start with an audit that produces a prioritized action list you can execute with us or on your own."),
 ("Do you help us pass certification / accreditation?",
  f"We build and evaluate to the LSOC courtroom-defensible standard and prepare teams for defensible certification. {fill('Note any specific accreditations you support.')}"),
 ("Can you review a detector-dog case or testify?",
  "Yes — David reviews cases and testifies as an expert witness. Every review is an honest, objective evaluation of training, records, handler influence, and reliability; the goal is the truth, not a predetermined conclusion for whoever retained him."),
 ("Remote or on-site?",
  "Both, depending on the work — selection testing and hands-on evaluation are typically on-site."),
 ("How is consulting priced?",
  f"Custom-quoted by scope after a short assessment call. {fill('Add day-rate or package ranges if you want them public.')}"),
]
hub("consulting.html","m","Program Consulting",
    "The operator who fixes detection programs.",
    "For agencies and organizations standing up a new detection program or worried theirs won't pass an audit — program development, evaluation, and selection from someone who's done the work.",
    "Book a Program Assessment","/consulting.html#book", co_proof, co_offer, co_faq,
    "K9 Detection Program Development, Audits & Consulting | K9School",
    "Detection program development, standards-based audits, K9 selection and testing, and handler/instructor development. Book a program assessment with David Latimer.",
    "Consulting", photos=CONSULTING_PHOTOS)

# ---- DETECTION DOGS ----
dd_offer = f"""
<div class="eyebrow">Disciplines</div>
<h2>Placement-ready dogs, matched to the job.</h2>
<div class="grid g3" style="margin-top:24px">
  <div class="card"><h3>Bed Bug Detection</h3><p class="muted">For pest control &amp; property managers who stake their name on accuracy.</p></div>
  <div class="card"><h3>Arson / Accelerant</h3><p class="muted">Accelerant detection for fire investigation and insurance work.</p></div>
  <div class="card"><h3>Conservation</h3><p class="muted">Wildlife, invasive species, and environmental detection.</p></div>
  <div class="card"><h3>Narcotics</h3><p class="muted">Reliable narcotics detection for agencies and security teams.</p></div>
  <div class="card"><h3>Explosives / Firearms</h3><p class="muted">High-consequence detection for operational deployment.</p></div>
  <div class="card"><h3>Other / Custom</h3><p class="muted">Allergen and specialty detection. {fill('List any other disciplines.')}</p></div>
</div>
<div class="split" style="margin-top:34px">
 <div>
  <h3>How placement works</h3>
  <ul class="tick">
   <li>Tell us the discipline and environment the dog will work in.</li>
   <li>We match or develop a dog selected for the right drive and temperament.</li>
   <li>Handler training and certification so the team performs from day one.</li>
   <li>Ongoing support to keep reliability high.</li>
  </ul>
 </div>
 <div class="form" id="availability">
  <h3 class="mt0">Check Availability</h3>
  {form_fields("Detection Dog Placement", extra_dogs=True)}
 </div>
</div>
"""
dd_proof = (proof_card("🐾","Selected, not just trained","Dogs chosen for scent ability, environmental confidence, search drive, and operational stability.") +
            proof_card("🧪","Discipline-proven",f"Working dogs placed across narcotics, arson, bed bug and conservation. {fill('Add placement results by discipline.')}") +
            proof_card("🤝","Team, not just a dog","Every placement includes handler development so your people can actually run the dog."))
dd_faq = [
 ("Do you sell green dogs or finished dogs?",
  f"{fill('Clarify what you offer — green, started, or fully finished — and typical price bands.')}"),
 ("Can you train for a discipline not listed?",
  "Often yes — the legacy Kip K9 work spanned narcotics, arson, termite, bed bug, and allergen detection. Ask us."),
 ("What's included with a placement?",
  f"Handler training and certification to the LSOC standard, plus support. {fill('Confirm exactly what each placement includes.')}"),
 ("How much does a detection dog cost?",
  f"It depends on discipline and finish level. {fill('Add price ranges or keep as inquiry.')}"),
]
hub("detection-dogs.html","p","Commercial &amp; Operational Detection Dogs",
    "A working dog your reputation can ride on.",
    "For pest control, restoration, conservation, security, and agencies buying a detection dog — placement-ready teams selected and trained for the environment they'll actually work in.",
    "Check Availability","/detection-dogs.html#availability", dd_proof, dd_offer, dd_faq,
    "Detection Dogs for Sale — Bed Bug, Arson, Narcotics, Conservation | K9School",
    "Placement-ready detection dogs for bed bug, arson/accelerant, conservation, narcotics and explosives detection — selected, trained, and paired with handler certification. Check availability.",
    "Detection Dogs", photos=DETECTION_PHOTOS)

# ============================================================
# PROOF
# ============================================================
proof_body = f"""
<section class="hero"><div class="wrap">
  <div class="crumb"><a href="/index.html">Home</a> / Proof</div>
  <div class="kick">Proof &amp; Results</div>
  <h1>Evidence, not adjectives.</h1>
  <p class="sub">The detection world runs on trust earned in deployment. Here's ours — case studies, references, and certification you can verify.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="eyebrow">Case studies</div>
  <h2>What our teams did in the field.</h2>
  <div class="grid g3" style="margin-top:26px">
   <div class="card"><div class="ph">Case study 1<br>{fill('Situation → what the team did → measurable outcome')}</div></div>
   <div class="card"><div class="ph">Case study 2<br>{fill('Situation → action → outcome')}</div></div>
   <div class="card"><div class="ph">Case study 3<br>{fill('Situation → action → outcome')}</div></div>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="eyebrow">From the field</div>
  <h2>The work, as it happens.</h2>
  <p class="lead" style="max-width:64ch">Detection is behavior you can read — the search before the sit. These are our teams working real problems: alerts, finds, and handlers built to hold up where it counts.</p>
  {gallery(FIELD_GALLERY)}
  <p class="muted" style="font-size:.82rem;margin-top:16px">Photos from LSOC training and deployments.</p>
</div></section>

<section class="sec wash"><div class="wrap">
  <div class="eyebrow">In their words</div>
  <h2>References who run our teams.</h2>
  <div class="grid g2" style="margin-top:26px">
   <div class="card"><div class="quote">{fill('Agency testimonial')}<cite>— {fill('Name, Title, Agency')}</cite></div></div>
   <div class="card"><div class="quote">{fill('Handler / trainer testimonial')}<cite>— {fill('Name, role')}</cite></div></div>
   <div class="card"><div class="quote">{fill('Commercial client testimonial')}<cite>— {fill('Name, Company')}</cite></div></div>
   <div class="card"><div class="quote">{fill('Consulting client testimonial')}<cite>— {fill('Name, Org')}</cite></div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="split">
   <div><div class="eyebrow">Watch</div><h2>See the work.</h2><p class="lead">Training and deployment footage tells the story words can't.</p><p class="muted">{fill('Embed YouTube videos from the existing channel.')}</p></div>
   <div class="ph" style="min-height:240px">Video embed<br>{fill('YouTube embed')}</div>
  </div>
</div></section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Want references for your specific use case?</h2>
  <p>Tell us the mission and we'll connect you with the most relevant proof.</p>
  <a class="btn" href="/contact.html">Request references</a>
</div></div></section>
"""
page("proof.html","Proof & Results — Case Studies & References | K9School",
     "Detection-dog case studies, agency references, client testimonials, and training footage from Latimer School of Operational K9s.",
     proof_body, schema="["+ORG_SCHEMA+"]", active="/proof.html")

# ============================================================
# ABOUT
# ============================================================
about_body = f"""
<section class="hero"><div class="wrap">
  <div class="crumb"><a href="/index.html">Home</a> / About</div>
  <div class="kick">About</div>
  <h1>Operator. Trainer. Expert witness.</h1>
  <p class="sub">K9School is the working home of {BIZ} — David Latimer's operational detection practice in Lincoln, Alabama, built on a career spent in the field and in the courtroom.</p>
</div></section>

<section class="sec"><div class="wrap split">
 <div>
  <div class="eyebrow">David Latimer</div>
  <h2>A lifetime around working dogs.</h2>
  <p class="lead">David Latimer's work with dogs began long before his first detection deployment — it began as a boy, watching his father work a liver-spotted pointer named Sport with nothing but his voice and a quiet kind of respect. That was positive reinforcement before it had a name, and compound behavior before anyone called it that. The lesson stuck: the dog was always communicating; the job was to listen.</p>
  <p>After the military — where he served as an HVAC technician and then a small-arms marksmanship instructor — a chance friendship with a forensic engineer pulled David into the world of fire and explosion investigation. He trained his first accelerant-detection dog in <b>1999</b>, worked hundreds of fire scenes, and helped put arsonists in prison. From there came narcotics, explosives, cadaver, and tracking dogs, and pest-detection dogs beginning around <b>2002</b>.</p>
  <p>He attended the police academy in <b>2003</b> and served as a law enforcement officer for the rest of his career, promoted to <b>Chief of Police in 2007</b> before retiring from full-time law enforcement in <b>2015</b>. Along the way he graduated from the <b>FBI National Academy in Quantico</b> — the highlight of his LE career. Today he trains, certifies, consults, and testifies, and has written extensively on detector-dog behavior and reliability.</p>
  <ul class="tick">
   <li><b>FBI National Academy</b> graduate (Quantico, VA).</li>
   <li>Retired <b>Chief of Police</b>; law enforcement officer since 2003.</li>
   <li>Training detector dogs since <b>1999</b> — arson/accelerant, narcotics, explosives, cadaver, tracking, and pest detection.</li>
   <li>Author and instructor on detector-dog behavior, reliability, and courtroom defensibility.</li>
  </ul>
  <a class="btn dark" href="/method.html">See the method he teaches</a>
 </div>
 <div>{img('lsoc-110-me-teaching.jpg', 'David Latimer instructing in the training room', 'shot tall')}
   <p class="muted" style="font-size:.82rem;margin-top:10px;text-align:center">David Latimer — training the human end of the leash.</p></div>
</div></section>

<section class="sec wash"><div class="wrap split">
  <div>
    <div class="eyebrow">The dog behind the name</div>
    <h2>Kip.</h2>
    <p>One of the finest detector dogs David ever worked was an accelerant-detection dog named Kip — the namesake of the original <b>Kip K9</b> brand. What set Kip apart wasn't drive or flash. It was <i>honesty</i>.</p>
    <p class="muted">Kip worked because he wanted to solve the odor problem. If target odor was there, he found it. If it wasn't, he refused to manufacture an answer just because someone expected one. More than once, people questioned his decisions — and more than once, Kip was right and the assumptions were wrong. That honesty became one of David's greatest teachers, and it's the standard every dog here is built toward.</p>
  </div>
  <div class="card" style="align-self:center">
    <div class="quote" style="font-size:1.18rem">"Kip worked because he wanted to solve the odor problem. He did not seem compelled to manufacture an answer simply because someone expected one."<cite>— David Latimer</cite></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="center"><div class="eyebrow">One operation, several roots</div><h2>K9School, Latimer School of Operational K9s, and Kip K9</h2></div>
  <p class="lead center" style="max-width:72ch;margin:16px auto 24px">K9School.net is now the single home for the work formerly carried under <b>Kip K9</b> and the <b>Latimer School of Operational K9s (LSOC)</b>. Same operator, same standard, one place to find it — with the legacy detection specialties (narcotics, arson, termite, bed bug, allergen) organized under our detection-dog service lines.</p>
  {book_callout()}
</div></section>

{photostrip(ABOUT_PHOTOS, heading="A career in the field — and the classroom.", eyebrow="David Latimer", wash=True)}

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Let's talk about what you need to deploy.</h2>
  <a class="btn" href="/contact.html">Get in touch</a>
</div></div></section>
"""
person_schema = ('{"@context":"https://schema.org","@type":"Person","name":"David Latimer",'
  f'"jobTitle":"Founder, Master Detection Dog Trainer & Expert Witness","worksFor":{{"@type":"Organization","name":"{BIZ}"}},'
  '"alumniOf":"FBI National Academy","hasOccupation":{"@type":"Occupation","name":"Retired Chief of Police"},'
  f'"url":"{SITE}/about.html","knowsAbout":["detector dog behavior","detection dog training","accelerant detection","narcotics detection","K9 program development","handler certification","detector dog courtroom testimony","handler influence","blind and double-blind testing"]}}')
page("about.html","About David Latimer | K9School — Latimer School of Operational K9s",
     "David Latimer and Latimer School of Operational K9s — operational detection dog training built on real field deployment in Lincoln, Alabama.",
     about_body, schema="["+ORG_SCHEMA+","+person_schema+"]", active="/about.html")

# ============================================================
# CERTIFICATION
# ============================================================
cert_faq = [
 ("What is the LSOC courtroom-defensible standard?",
  f"A defined benchmark for evaluating detection-team reliability the way a court would — behavioral documentation, blind and double-blind testing, honest failure records, and handlers who can explain what the dog did. {fill('Describe the standard in detail: what it tests, how it’s scored, who recognizes it.')}"),
 ("How does this relate to the K9 Alliance Certification Standard?",
  f"{fill('The original site referenced a &ldquo;K9 Alliance Certification Standard.&rdquo; Confirm: is that the same as the LSOC standard, a separate third-party certification you use, or a legacy name to retire? We&rsquo;ll align the whole site to your answer.')}"),
 ("Why does the standard matter for agencies?",
  "Documented reliability to a defined standard is defensible in procurement and in court — it turns 'trust us' into evidence a handler can put on the record."),
 ("Can we certify a team we didn't buy from you?",
  f"{fill('Confirm whether you evaluate/certify externally sourced teams.')}"),
]
cert_body = f"""
<section class="hero"><div class="wrap">
  <div class="crumb"><a href="/index.html">Home</a> / Certification</div>
  <div class="kick">The Standard</div>
  <h1>Reliability you can document.</h1>
  <p class="sub">Every dog and handler we build is evaluated against the LSOC courtroom-defensible standard — so your records hold up where it counts.</p>
</div></section>
<section class="sec"><div class="wrap split">
 <div>
  <div class="eyebrow">What it covers</div>
  <h2>A defined benchmark, not a vibe.</h2>
  <p class="lead">The standard evaluates the whole team the way honest scrutiny would — because certification is a benchmark, not the goal.</p>
  <ul class="tick">
   <li>Scent-detection reliability under realistic, field-representative conditions.</li>
   <li>Independent work — blind and double-blind testing to prove the dog reads odor, not the handler.</li>
   <li>Handler communication, control, and the ability to explain the dog's behavior.</li>
   <li>Documented, repeatable evaluation — including honest records of failure.</li>
  </ul>
  <p class="muted">{fill('Add specifics: scoring, pass criteria, re-test cadence, and any recognizing body.')}</p>
 </div>
 <div class="card"><h3 class="mt0">Why it wins deals</h3><p class="muted">Agencies and courts don't reward the best adjectives — they reward the best evidence. A documented standard is that evidence.</p><a class="btn dark sm" href="/contact.html">Certify with us</a></div>
</div></section>
<section class="sec wash"><div class="wrap"><div class="center"><div class="eyebrow">Questions</div><h2>About the standard</h2></div>
<div style="max-width:820px;margin:28px auto 0">{faq_html(cert_faq)}</div></div></section>
{photostrip(CERT_PHOTOS, heading="Teams certified to the standard.")}
"""
page("certification.html","The LSOC Courtroom-Defensible Standard | K9School",
     "The LSOC courtroom-defensible standard — how Latimer School of Operational K9s documents detection-team reliability for defensible, court-ready records.",
     cert_body, schema="["+ORG_SCHEMA+","+faq_schema(cert_faq)+"]", active="/certification.html")

# ============================================================
# CONTACT
# ============================================================
contact_body = f"""
<section class="hero"><div class="wrap">
  <div class="crumb"><a href="/index.html">Home</a> / Contact</div>
  <div class="kick">Contact</div>
  <h1>Tell us what you need to deploy.</h1>
  <p class="sub">Pick your path below. Agencies and consulting inquiries reach David directly; training and placement inquiries route to the right next step.</p>
</div></section>
<section class="sec"><div class="wrap split">
 <div class="form">
  <h3 class="mt0">Start the conversation</h3>
  {form_fields("General", extra_all=True)}
 </div>
 <div>
  <div class="card"><h3 class="mt0">Direct line</h3><p class="muted">Prefer to talk? Call David.</p><p><a class="btn dark" href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
  <div class="card" style="margin-top:18px"><h3 class="mt0">Location</h3><p class="muted">{ADDR}</p><p class="muted">Hours: {fill('business hours')}</p><div class="ph" style="min-height:160px;margin-top:12px">Map embed<br>{fill('Google Map embed')}</div></div>
 </div>
</div></section>
{photostrip(CONTACT_PHOTOS, heading="The people and dogs behind the work.", wash=True)}
"""
page("contact.html","Contact — Request a Capability Brief | K9School",
     "Contact Latimer School of Operational K9s. Request a capability brief, apply for training, book a program assessment, or check detection-dog availability.",
     contact_body, schema="["+ORG_SCHEMA+"]", active="/contact.html")

# ============================================================
# RESOURCES (SEO pillar content + lead magnets)
# ============================================================
def article_schema(title, desc, slug):
    return ('{"@context":"https://schema.org","@type":"Article",'
      f'"headline":{_json(title)},"description":{_json(desc)},'
      f'"author":{{"@type":"Person","name":"David Latimer"}},'
      f'"publisher":{{"@type":"Organization","name":{_json(BIZ)}}},'
      f'"mainEntityOfPage":"{SITE}/{slug}"}}')

def article(slug, kicker, title, desc, intro, sections, cta_head, cta_sub, cta_label, cta_href, faq=None):
    body_sections = ""
    for h, paras in sections:
        body_sections += f"<h2>{h}</h2>"
        for para in paras:
            if para.startswith("UL:"):
                items = para[3:].split("|")
                body_sections += '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
            else:
                body_sections += f"<p>{para}</p>"
    photos_h = photostrip(ARTICLE_PHOTOS[slug], heading="From the field") if slug in ARTICLE_PHOTOS else ""
    faq_block = ""
    schema_extra = ""
    if faq:
        faq_block = f'<h2>Frequently asked</h2><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)}</div>'
        schema_extra = "," + faq_schema(faq)
    body = f"""
<section class="hero"><div class="wrap" style="max-width:820px">
  <div class="crumb"><a href="/index.html">Home</a> / <a href="/resources.html">Resources</a> / Guide</div>
  <div class="kick">{kicker}</div>
  <h1>{title}</h1>
  <p class="sub">{intro}</p>
</div></section>
<section class="sec"><div class="wrap" style="max-width:780px">
  {body_sections}
  {faq_block}
</div></section>
{photos_h}
<section class="sec tight"><div class="wrap" style="max-width:900px"><div class="ctastrip">
  <h2>{cta_head}</h2><p>{cta_sub}</p>
  <a class="btn" href="{cta_href}">{cta_label}</a>
</div></div></section>
"""
    schema = "[" + ORG_SCHEMA + "," + article_schema(title, desc, slug) + schema_extra + "]"
    page(slug, f"{title} | K9School", desc, body, schema=schema, active="/resources.html")

# --- Guide 1: choosing a detection dog ---
article("resources-choosing-a-detection-dog.html",
  "Buyer's Guide",
  "How to Choose a Detection Dog",
  "A practical buyer's guide to selecting a reliable detection dog — the traits, tests, and questions that separate a working dog from an expensive mistake.",
  "A detection dog is a multi-year investment that your operation's results ride on. Whether you're a department, a pest-control company, or a conservation team, the difference between a dog that performs and one that quietly fails comes down to selection. Here's how professionals evaluate a candidate before a dime changes hands.",
  [
   ("Start with the job, not the dog",
    ["Before you look at a single dog, define the work precisely. What odor(s)? What environments — vehicles, luggage, open fields, structures? How many searches a day, in what climate? A dog selected for calm indoor bed-bug work is a poor match for high-tempo vehicle interdiction, and vice versa. The clearer the job profile, the better the match.",
     "Write down your non-negotiables: target odors, environment, daily workload, and who will handle the dog. This profile is what a good vendor will ask you for first — and if they don't ask, that tells you something."]),
   ("The four traits that predict field reliability",
    ["Across disciplines, working-dog professionals evaluate the same core traits:",
     "UL:<b>Scent ability & hunt drive</b> — the genuine desire to search and keep searching when the odor is faint or the environment is distracting.|<b>Environmental confidence</b> — comfort on slick floors, stairs, heights, noise, and novel places. A brilliant nose is useless if the dog shuts down in a real setting.|<b>Search drive & stamina</b> — the persistence to work a full shift without quitting.|<b>Operational stability</b> — a steady temperament under pressure, around people, and in chaos."]),
   ("Green, started, or finished — know what you're buying",
    ["Dogs are sold at different stages, and the right choice depends on your handler's experience and your timeline.",
     "UL:<b>Green</b> dogs show aptitude but aren't trained — cheapest, longest road, needs an experienced trainer.|<b>Started</b> dogs have foundation odor work underway.|<b>Finished</b> dogs are trained to work and can be certified with a handler quickly — highest cost, lowest risk, fastest to deployment.",
     "There's no universally 'right' answer, but be honest about your team's ability to develop a dog. A finished dog paired with handler certification is the lowest-risk path for most agencies and businesses."]),
   ("Insist on evaluation and documentation",
    ["Reputable programs test dogs against a defined standard and hand you the records. Ask to see the selection testing, watch the dog work in an environment like yours, and get written documentation of what was evaluated. For agencies especially, that paper trail is what makes a team defensible in procurement and in court.",
     "If a seller resists letting you see the dog work or can't produce evaluation records, walk away."]),
   ("Buy the team, not just the dog",
    ["Reliability is a property of the dog and the handler together. The best dog in the country will underperform with an undertrained handler. Factor handler training and certification into your decision and your budget from the start — it's not an add-on, it's half the system."]),
  ],
  "Talk through your use case with an operator.",
  "Tell us the job — odor, environment, and workload — and we'll tell you straight what kind of dog fits and what it takes to deploy.",
  "Check availability", "/detection-dogs.html#availability",
  faq=[("How much does a detection dog cost?",
        f"It varies widely by discipline and training stage. {fill('Add your typical price bands or keep as inquiry.')} The cheapest dog is rarely the lowest total cost once training and reliability are accounted for."),
       ("How long until a dog is deployable?",
        f"A finished dog paired with handler certification can deploy quickly; a green dog is a months-long project. {fill('Add typical timelines.')}")])

# --- Guide 2: become a handler ---
article("resources-become-a-k9-handler.html",
  "Career Guide",
  "How to Become a K9 Detection Handler",
  "What it actually takes to become a competent detection-dog handler — the skills, the certification path, and how to choose training that makes you ready for real work.",
  "Becoming a detection handler isn't about collecting a certificate — it's about becoming someone a dog can rely on and an employer can deploy. Here's the honest path, and how to pick training that builds real competence instead of just handing you paper.",
  [
   ("Understand what the job really is",
    ["Handling is reading a dog. The dog does the detecting; your job is to present the search correctly, recognize a change of behavior, avoid cueing false responses, and keep accurate records. That's a learned skill set built on repetition and feedback — which is why the training you choose matters more than the credential you end up with."]),
   ("The typical path",
    ["UL:<b>Foundation</b> — learn scent theory, search patterns, and how to read a dog under a qualified instructor.|<b>Handler certification</b> — become certified as a team with a dog, to a recognized standard.|<b>Field deployment training</b> — bridge from controlled setups to messy real-world environments.|<b>Instructor certification</b> — for those who want to train other teams, the highest rung.",
     "You don't have to start with prior experience, but you do have to commit to reps. Competence comes from time on the leash with good coaching."]),
   ("How to choose a course (five questions)",
    ["UL:Does it certify you to a <b>recognized standard</b>, or just issue its own paper?|Is it <b>field-first</b>, or does it stop at controlled-yard exercises?|Do they train the <b>handler</b>, or mostly the dog?|Can they show you <b>where their graduates are working</b>?|Is the instructor an actual <b>operator</b> with deployment experience?",
     "A program that can answer these confidently is worth far more than the cheapest or fastest option."]),
   ("What competence looks like when you finish",
    ["You should leave able to run a reliable team: present a search cleanly, recognize and reward correctly, troubleshoot common problems, and document your work so it holds up. If a course can't tell you what you'll be able to *do* at the end — only what you'll have attended — keep looking."]),
  ],
  "Ready to train where it's field-first?",
  "See the handler and instructor certification tracks, or get the full syllabus and next cohort dates.",
  "Explore training", "/training.html#apply",
  faq=[("Do I need experience to start?",
        f"No formal experience is required to begin foundation and handler tracks, though it helps. {fill('State prerequisites per course.')}"),
       ("What certification will I earn?",
        "Certification as a team to the LSOC standard, documenting your reliability to a recognized benchmark.")])

# --- Guide 3: starting a program ---
article("resources-starting-a-k9-program.html",
  "Program Guide",
  "Starting (or Fixing) a K9 Detection Program",
  "A field guide for agencies and organizations standing up a detection program — or worried the one they have won't survive an audit.",
  "Standing up a detection program is easy to do badly and expensive to fix later. Whether you're building from scratch or shoring up an existing unit, these are the fundamentals that determine whether your program produces reliable, defensible results.",
  [
   ("Define the mission and the standard first",
    ["Programs drift when nobody wrote down what 'good' means. Before selecting dogs or handlers, define the mission profile and the certification standard you'll hold teams to. That standard becomes the yardstick for selection, training, maintenance, and — critically — the documentation that defends your program under scrutiny."]),
   ("Select for the work, systematically",
    ["Ad-hoc dog buying is where most programs leak reliability. Use a consistent selection process that tests scent ability, environmental confidence, search drive, and stability against your actual mission. Document every selection decision.",
     "The same applies to handlers: pick people who can commit to the reps and the recordkeeping, not just the enthusiasts."]),
   ("Build maintenance and records into day one",
    ["Reliability decays without maintenance training, and undocumented reliability is legally fragile. A real program schedules ongoing training and keeps records that show, on paper, that teams are held to standard. This is the difference between a program that passes an audit and one that panics before one."]),
   ("Get an outside evaluation before you need one",
    ["A structured, standards-based audit from an experienced operator surfaces the gaps while they're cheap to fix — not in a courtroom or a failed certification. Whether you run the fixes yourself or with help, the audit gives you a prioritized, honest picture."]),
   ("Common failure modes to avoid",
    ["UL:Buying dogs before defining the mission.|Training the dog but neglecting the handler.|No maintenance schedule.|Thin or missing documentation.|No recognized certification standard behind the program."]),
  ],
  "Get a straight read on your program.",
  "Book a program assessment — a focused call to scope your program and its gaps, from someone who's built and audited them.",
  "Book an assessment", "/consulting.html#book",
  faq=[("Can you just audit our existing program?",
        "Yes — many engagements start with an audit that produces a prioritized fix-list you can execute with us or on your own."),
       ("Do you help us reach certification?",
        f"We build and evaluate to the LSOC standard and prepare teams for defensible certification. {fill('Note specific accreditations you support.')}")])

# --- Guide 4: narcotics K9s for agencies ---
article("resources-narcotics-detection-k9s.html",
  "Agency Guide",
  "Narcotics Detection K9s: What Agencies Should Know",
  "How agencies should evaluate, deploy, and document narcotics detection K9s — reliability, defensibility, and the mistakes that get cases thrown out.",
  "A narcotics K9 is an evidentiary tool as much as an operational one. Deployed and documented well, it's a force multiplier; documented poorly, it's a liability that can sink a case. Here's what matters when you bring one into your unit.",
  [
   ("Reliability is a legal question, not just a training one",
    ["A narcotics detection alert can establish probable cause — which means your dog's reliability may be scrutinized in court. Courts increasingly look at training records, certification to a recognized standard, and maintenance logs. A dog that performs in the field but has thin documentation is a case waiting to be challenged.",
     "Build the paper trail from day one: certification, ongoing maintenance training, and records of finds and misses."]),
   ("Single-purpose vs. dual-purpose",
    ["Decide whether you need a dedicated narcotics detection dog or a dual-purpose patrol-and-detection dog. Dual-purpose maximizes a handler's utility but adds training and management complexity. The right answer depends on your call volume, staffing, and mission — not on what's cheapest."]),
   ("Selection traits for narcotics work",
    ["UL:Strong, persistent hunt drive in distracting environments (roadside, vehicles, crowds).|Environmental confidence on vehicles, in tight spaces, and around traffic.|A clear, trainable trained final response.|Stable temperament around the public."]),
   ("Handler competence decides field reliability",
    ["The same dog is reliable or unreliable depending on the handler. Cueing, poor search presentation, and sloppy record-keeping are handler failures that look like dog failures. Invest in handler certification and continued development — it's where most real-world reliability is won or lost."]),
  ],
  "Building or upgrading a narcotics K9 capability?",
  "Talk to an operator about the right dog, handler certification, and the documentation that keeps your program defensible.",
  "Request a capability brief","/agencies.html#brief",
  faq=[("Do you certify to a standard courts will respect?",
        "Teams are trained to the LSOC standard with documented records, so reliability is demonstrable rather than asserted."),
       ("Single or dual purpose — which should we get?",
        f"It depends on your call volume and staffing. {fill('Add your guidance / options.')} We'll help you scope it.")])

# --- Guide 5: bed bug dogs for pest control ---
article("resources-bed-bug-detection-dogs.html",
  "Business Guide",
  "Bed Bug Detection Dogs: A Guide for Pest Control Businesses",
  "Why a trained bed bug detection dog can transform a pest-control operation — accuracy, speed, new revenue — and how to choose one that protects your reputation.",
  "For a pest-control business, a bed bug detection dog is a revenue and reputation decision. A reliable dog finds infestations faster and earlier than visual inspection, opens a premium service line, and differentiates you from competitors. An unreliable one does the opposite. Here's how to get it right.",
  [
   ("The business case",
    ["A trained detection dog can inspect a room in minutes with high accuracy, letting you offer canine inspections as a premium service, verify treatments, and win commercial accounts (hotels, property managers) that demand documented thoroughness. The dog often pays for itself through new work and efficiency — but only if it performs consistently."]),
   ("Accuracy depends on training and handling",
    ["A detection dog's real-world accuracy is a product of the dog, the handler, and ongoing maintenance. Beware of any pitch that treats the dog as a plug-and-play gadget. You're buying a team and a routine, not just an animal."]),
   ("What to look for",
    ["UL:A dog selected for calm, methodical indoor work and strong scent drive.|Handler training so your staff can present searches and read the dog correctly.|A clear response you can document for clients.|Ongoing maintenance training to keep accuracy high.|Support from the trainer after placement."]),
   ("Protect your reputation with documentation",
    ["Clients — especially commercial ones — increasingly want proof. Keep records of inspections and maintenance so your canine service is credible and defensible, not just impressive."]),
  ],
  "Add a detection dog to your business the right way.",
  "Tell us your service area and volume, and we'll help you choose a dog and get your handler trained.",
  "Check availability","/detection-dogs.html#availability",
  faq=[("How accurate are bed bug dogs?",
        "Well-trained, well-handled dogs are highly accurate — but accuracy is a property of the whole team and its maintenance routine, which is why handler training and ongoing work matter."),
       ("Do you train our staff to handle the dog?",
        "Yes — every placement includes handler development so your people can actually run the dog and document results.")])

# --- Guide 6: explosives K9 selection ---
article("resources-explosives-detection-k9.html",
  "Operational Guide",
  "Explosives Detection K9s: Selection & Deployment",
  "The high-consequence discipline where reliability is non-negotiable — how explosives detection K9s are selected, trained, and deployed to an operational standard.",
  "Explosives detection is the discipline with the least room for error. Selection, training, and maintenance standards have to be higher because the cost of a miss is catastrophic. This guide covers what separates a truly operational EDD team from one that only looks the part.",
  [
   ("Selection is stricter for a reason",
    ["Explosives detection dogs are selected for the same core traits as any detection dog — hunt drive, environmental confidence, search stamina, stability — but the bar is higher and the temperament requirements stricter, because these dogs work in crowds, transit, and high-pressure environments where a shutdown or a false response has serious consequences."]),
   ("Operational, not just certified",
    ["Certification is a floor, not a ceiling. Operational reliability means the team performs in realistic environments — luggage, vehicles, venues, moving crowds — not just in a controlled certification setup. Field deployment training bridges that gap and should be non-negotiable."]),
   ("Maintenance and documentation",
    ["UL:Scheduled maintenance training to prevent skill decay.|Meticulous records — training, certification, finds.|Regular re-evaluation against a recognized standard.|Handler continuity and development."]),
   ("The handler is half the system",
    ["In explosives work especially, handler reading and search discipline are decisive. A world-class dog with a weak handler is a weak team. Build handler competence deliberately and keep it current."]),
  ],
  "Deploying explosives detection capability?",
  "Talk to an operator about selection, handler certification, and holding the team to an operational standard.",
  "Request a capability brief","/agencies.html#brief",
  faq=[("Is certification enough for explosives work?",
        "Certification is the floor. Operational reliability requires field-realistic training and ongoing maintenance beyond the certification standard."),
       ("Do you provide the dog and train our handler?",
        "Both — and for high-consequence work we strongly recommend the full team approach rather than a dog alone.")])

# --- Guide 7: five phases ---
article("resources-five-phases-detector-dog-behavior.html",
  "Method Guide",
  "The Five Phases of Detector Dog Behavior",
  "The behavioral sequence every detector-dog search moves through — and why naming it changes how handlers observe, document, and testify.",
  "The sit gets all the attention. But by the time a dog performs its trained final response, the important work is already done. Understanding the search as a sequence of phases lets a handler see the investigation as it happens — and describe it accurately later.",
  [
   ("Why phases instead of just “the alert”",
    ["A detector dog doesn't recognize odor at the instant it sits. Recognition happens earlier, and the dog's behavior changes as it works the problem. Breaking the search into phases gives handlers a shared, precise language for what the dog is doing — instead of collapsing an entire investigation into one word: &ldquo;alerted.&rdquo;"]),
   ("The five phases",
    ["UL:<b>Phase 1 — Responds to the command to search.</b> The dog begins working on cue.|<b>Phase 2 — Systematic search, no target odor recognized.</b> The dog covers the area methodically.|<b>Phase 3 — Detection.</b> Target odor becomes meaningful; recognition begins.|<b>Phase 4 — Change of behavior.</b> The observable tell: respiration, head position, body tension, bracketing toward source.|<b>Phase 5 — Trained final response.</b> The dog reports its conclusion. The sit is phase five — not the whole story."]),
   ("Phases 3 and 4 are the investigation",
    ["This is where the dog actually does its work, and it's exactly what most testimony leaves out. A handler who can say what happened in phases 3 and 4 — &ldquo;the dog stopped forward movement, raised its head, turned into the wind, and bracketed the passenger door&rdquo; — is describing evidence. A handler who can only say &ldquo;my dog alerted&rdquo; has skipped the investigation."]),
   ("What it changes for you",
    ["Once you see the phases, you train differently, observe differently, and testify differently. You reward the investigation, not just the final response — and you can explain, step by step, why the dog did what it did."]),
  ],
  "Want handlers trained to read the whole search?",
  "This framework is the backbone of our training. See the full method or talk to us about a course.",
  "Explore the method","/method.html",
  faq=[("Is the trained final response unimportant?",
        "Not at all — it's how the dog reports its conclusion. The point is that it's the end of the sequence, not the entire event. The behavior leading up to it is what makes it meaningful."),
       ("Where does this come from?",
        "It's part of the LSOC approach developed by David Latimer, a retired chief of police and FBI National Academy graduate, and set out in his forthcoming book.")])

# --- Guide 8: Florida v Harris ---
article("resources-florida-v-harris-k9-handlers.html",
  "Legal Guide",
  "What Florida v. Harris Means for K9 Handlers",
  "A plain-language look at the Supreme Court case that shaped how detector-dog reliability is judged — and what it actually requires of handlers and agencies.",
  "Florida v. Harris (2013) is one of the most cited — and most misunderstood — detector-dog cases. Handlers sometimes hear that it means &ldquo;certification proves reliability&rdquo; and stop thinking. It doesn't, and they shouldn't. Here's what it actually means for your work.",
  [
   ("What the Court addressed",
    ["Harris dealt with how a court decides whether a dog's alert established probable cause. The Court rejected rigid checklists in favor of a totality-of-the-circumstances approach — training and certification matter, but so does the defense's ability to challenge them."]),
   ("What it does not do",
    ["It does not make a certificate a magic shield. A defendant can still contest a dog's reliability with evidence about training, records, testing, and handler influence. Certification is a benchmark, not a guarantee — and a thin training file invites exactly the challenge Harris permits."]),
   ("What it asks of you",
    ["UL:Keep genuine training records — including honest documentation of failures.|Test for real reliability with blind and double-blind work, not just pattern-passing.|Be able to explain the dog's behavior, not just assert an alert.|Understand that your credibility on the stand is part of the evidence."]),
   ("The practical takeaway",
    ["Harris rewards teams that can demonstrate reliability and punishes teams that can only claim it. That's the same standard good training aims for anyway: build a dog whose work you can document and defend."]),
  ],
  "Build a program that survives the challenge Harris allows.",
  "We train and document teams for scrutiny, and provide expert review and testimony. Let's talk.",
  "Request a capability brief","/agencies.html#brief",
  faq=[("Does certification alone establish probable cause?",
        "Not automatically. Harris allows the defense to challenge reliability, so documented training, testing, and credible testimony still matter."),
       ("Can you review a case involving a Harris challenge?",
        "Yes — David reviews detector-dog cases and testifies as an expert, on the basis of honest evaluation. See Consulting.")],
  )

# --- Guide 9: handler influence ---
article("resources-handler-influence-invisible-leash.html",
  "Method Guide",
  "The Invisible Leash: Understanding Handler Influence",
  "How handlers unintentionally influence detector dogs — the Clever Hans lesson, the research, and how honest teams train and test to reduce it.",
  "The most powerful force acting on a detector dog often isn't the odor. It's the person holding the leash. Handler influence isn't misconduct — it's usually unconscious — but if you don't understand it, you can't build a dog a court will trust.",
  [
   ("The Clever Hans lesson",
    ["A century ago, a horse called Clever Hans appeared to do arithmetic — until researchers showed he was reading tiny, unconscious cues from the people around him. Detector dogs are at least as sensitive. When a handler expects an alert, the dog can find one, whether or not odor is present."]),
   ("What the research shows",
    ["Studies — including Dr. Lisa Lit's well-known work — have demonstrated that handler beliefs can shape a dog's responses, producing errors that track the handler's expectations rather than the presence of target odor. This isn't an attack on handlers; it's a description of how sensitive these teams are."]),
   ("Four channels of influence",
    ["UL:<b>Physical</b> — leash tension, body position, slowing at a spot.|<b>Visual</b> — a glance, a lean, a change in posture.|<b>Verbal</b> — tone and timing of encouragement.|<b>Emotional</b> — the handler's own anticipation traveling down the leash."]),
   ("How honest teams respond",
    ["You don't eliminate influence by going passive — you manage it and audit for it. Blind training (the handler doesn't know the hide locations) and double-blind testing (no one present does) reveal whether the dog is working odor or reading the handler. &ldquo;Let the dog stop you. You don't stop the dog.&rdquo;"]),
  ],
  "Train and test to prove the dog works the odor — not you.",
  "Reducing and auditing handler influence is built into how we train and evaluate. See the method or get in touch.",
  "Explore the method","/method.html",
  faq=[("Is handler influence the same as cheating?",
        "No. It's almost always unconscious. The problem isn't intent — it's that unmanaged influence undermines reliability. That's why we train to reduce it and test to expose it."),
       ("How do you test for it?",
        "Primarily through blind and double-blind training and evaluation, which remove the handler's knowledge of where odor is — so the dog's work stands on its own.")],
  )

# --- Resources index ---
res_body = f"""
<section class="hero"><div class="wrap">
  <div class="crumb"><a href="/index.html">Home</a> / Resources</div>
  <div class="kick">Resources</div>
  <h1>Field-tested guidance, free to read.</h1>
  <p class="sub">Straight, practical guides on selecting dogs, becoming a handler, and building programs — written from operational experience, not marketing.</p>
</div></section>
<section class="sec"><div class="wrap">
  <div class="grid g3">
    <a class="card hover audience p" href="/resources-choosing-a-detection-dog.html"><div class="ic">🐕</div><h3>How to Choose a Detection Dog</h3><p>The traits, tests, and questions that separate a working dog from an expensive mistake.</p><span class="go">Read the buyer's guide →</span></a>
    <a class="card hover audience g" href="/resources-become-a-k9-handler.html"><div class="ic">🎓</div><h3>How to Become a K9 Handler</h3><p>The real path to competence — and how to choose training that makes you deployable.</p><span class="go">Read the career guide →</span></a>
    <a class="card hover audience a" href="/resources-starting-a-k9-program.html"><div class="ic">📋</div><h3>Starting or Fixing a K9 Program</h3><p>The fundamentals that make a detection program reliable and audit-proof.</p><span class="go">Read the program guide →</span></a>
    <a class="card hover audience a" href="/resources-narcotics-detection-k9s.html"><div class="ic">🛡&#65039;</div><h3>Narcotics Detection K9s for Agencies</h3><p>Reliability, defensibility, and the documentation that keeps cases from getting tossed.</p><span class="go">Read the agency guide →</span></a>
    <a class="card hover audience p" href="/resources-bed-bug-detection-dogs.html"><div class="ic">🐛</div><h3>Bed Bug Dogs for Pest Control</h3><p>The business case, and how to choose a dog that protects your reputation.</p><span class="go">Read the business guide →</span></a>
    <a class="card hover audience a" href="/resources-explosives-detection-k9.html"><div class="ic">💥</div><h3>Explosives Detection K9s</h3><p>The high-consequence discipline where reliability is non-negotiable.</p><span class="go">Read the operational guide →</span></a>
    <a class="card hover audience g" href="/resources-five-phases-detector-dog-behavior.html"><div class="ic">👁️</div><h3>The Five Phases of Detector Dog Behavior</h3><p>The behavioral sequence every search moves through — the heart of the method.</p><span class="go">Read the method guide →</span></a>
    <a class="card hover audience a" href="/resources-florida-v-harris-k9-handlers.html"><div class="ic">⚖️</div><h3>What Florida v. Harris Means for Handlers</h3><p>The Supreme Court case on detector-dog reliability, in plain language.</p><span class="go">Read the legal guide →</span></a>
    <a class="card hover audience m" href="/resources-handler-influence-invisible-leash.html"><div class="ic">🔗</div><h3>The Invisible Leash: Handler Influence</h3><p>How handlers unintentionally shape a dog — and how honest teams test for it.</p><span class="go">Read the method guide →</span></a>
  </div>
</div></section>
{photostrip(RESOURCES_PHOTOS, heading="Guidance grounded in real work.", wash=True)}
<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Have a question these didn't answer?</h2><p>Ask an operator directly.</p>
  <a class="btn" href="/contact.html">Get in touch</a>
</div></div></section>
"""
page("resources.html", "K9 Detection Resources & Guides | K9School",
     "Free, field-tested guides from Latimer School of Operational K9s: choosing a detection dog, becoming a handler, and building a K9 detection program.",
     res_body, schema="["+ORG_SCHEMA+"]", active="/resources.html")

# ============================================================
# THE METHOD (LSOC philosophy — David's framework)
# ============================================================
method_faq = [
 ("What is the difference between an alert and a change of behavior?",
  "A change of behavior is what the dog does when it first recognizes odor — altered respiration, head position, body tension, working the scent. The trained final response (the &ldquo;alert&rdquo; or sit) comes later, after the dog has resolved the problem. The behavior is the investigation; the sit is the dog reporting its conclusion."),
 ("Why does LSOC emphasize blind and double-blind training?",
  "Because reliability is demonstrated, not claimed. If the handler knows where the odor is, the dog can read the handler instead of the odor. Blind and double-blind work audits that out and proves the dog is working independently — which is exactly what a court will ask."),
 ("Is this approach only for law enforcement?",
  "No. The same principles — reading behavior, building independent dogs, honest evaluation, documentation — make any detection dog more reliable, whether it's working narcotics, bed bugs, arson, or conservation."),
]
method_body = f"""
<section class="hero"><div class="wrap" style="max-width:880px">
  <div class="crumb"><a href="/index.html">Home</a> / The Method</div>
  <div class="kick">The LSOC Approach</div>
  <h1>Behavior Is <span class="amb">Evidence.</span></h1>
  <p class="sub">Most of the profession trains the sit, rewards the sit, and testifies about the sit. We train something more important: the search that happens before it — because that is where the dog does its real work.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="quote" style="font-size:1.35rem">"The sit was not the discovery. It was the communication."</div>
  <p class="lead" style="margin-top:16px">A detector dog does not suddenly recognize target odor at the moment it sits. Recognition happened earlier. The dog met odor, and its behavior began to change — respiration, head position, body tension, movement. The trained final response is the <i>end</i> of a conversation that started the moment odor became meaningful. Understanding that conversation is the difference between simply handling a detector dog and learning to read one.</p>
  <p>This is the idea the whole LSOC method is built on: <b>the dog has been talking since the first breath of the search.</b> The handler's job is to learn its language.</p>
</div></section>

<section class="sec wash"><div class="wrap">
  <div class="center"><div class="eyebrow">Framework</div><h2>The Five Phases of Detector Dog Behavior</h2>
  <p class="lead" style="max-width:60ch;margin:12px auto 0">Every search moves through the same sequence. Naming the phases lets a handler observe, document, and testify precisely.</p></div>
  <div class="grid g3" style="margin-top:30px;text-align:left">
    <div class="card"><div class="ic">1</div><h3>Responds to the search command</h3><p>The dog begins working on cue.</p></div>
    <div class="card"><div class="ic">2</div><h3>Systematic search</h3><p>Working the area — no target odor recognized yet.</p></div>
    <div class="card"><div class="ic">3</div><h3>Detection</h3><p>Odor becomes meaningful. Recognition begins.</p></div>
    <div class="card"><div class="ic">4</div><h3>Change of behavior</h3><p>The tell: respiration, head, body, bracketing the source.</p></div>
    <div class="card"><div class="ic">5</div><h3>Trained final response</h3><p>The dog reports its conclusion — the sit is phase five, not the whole story.</p></div>
    <div class="card" style="background:var(--navy);color:#fff;border-color:var(--navy)"><h3 style="color:#fff">Why it matters</h3><p style="color:#c4d2dd">Phases 3 and 4 are the investigation. A handler who can describe them can explain — and defend — exactly what the dog did.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div>
    <div class="eyebrow">Framework</div>
    <h2>The Four Classes of Behavior</h2>
    <p>Not everything a dog does means the same thing. Separating these keeps a handler honest about what the dog is actually telling them.</p>
    <ul class="tick">
      <li><b>Intrinsic</b> — what the dog does by nature.</li>
      <li><b>Trained</b> — what we deliberately taught, including the final response.</li>
      <li><b>Independently learned</b> — what the dog figured out on its own.</li>
      <li><b>Handler-influenced</b> — what the dog did because of us, knowingly or not.</li>
    </ul>
    <p class="muted">That last class is the dangerous one. It's why we train to reduce influence and test to expose it.</p>
  </div>
  <div>
    <div class="eyebrow">Reading the dog</div>
    <h2>Every dog has an accent.</h2>
    <p>Reading behavior is a learned skill, built on knowing your individual dog's baseline and watching for change:</p>
    <ul class="tick">
      <li><b>Respiration</b> — often the first and clearest tell.</li>
      <li><b>Head position</b> — where the dog is placing the problem.</li>
      <li><b>Tail carriage</b> — tension and interest.</li>
      <li><b>Footwork</b> — bracketing, overshooting, source commitment.</li>
    </ul>
    <div class="quote">"Every search is a conversation. The dog is talking. The question is whether the handler understands the language."</div>
  </div>
</div></section>

<section class="sec wash"><div class="wrap">
  <div class="center"><div class="eyebrow">What we build toward</div><h2>Independent dogs, honest answers</h2></div>
  <div class="grid g3" style="margin-top:28px">
    <div class="card"><h3>Teach the dog to say "I don't know"</h3><p class="muted">Blank searches and productive failure teach a dog it doesn't have to manufacture an answer. An honest &ldquo;no odor here&rdquo; is a trained skill.</p></div>
    <div class="card"><h3>Reward the investigation</h3><p class="muted">We never get so focused on the final response that we stop valuing the problem-solving that earned it. Reward is information, not the goal.</p></div>
    <div class="card"><h3>The Invisible Leash</h3><p class="muted">Dogs read us. Physical, visual, verbal, and emotional cues can move a dog. We train to reduce handler influence — and test to expose it.</p></div>
    <div class="card"><h3>The Scent Board System</h3><p class="muted">Our signature tool teaches dogs to <i>think before they alert</i> — discrimination, bracketing, and source commitment, not pattern-guessing.</p></div>
    <div class="card"><h3>Trust, but verify</h3><p class="muted">Reliability is demonstrated, not claimed. Blind and double-blind testing is how we prove the dog works the odor, not the handler.</p></div>
    <div class="card"><h3>Handler, heal thyself</h3><p class="muted">Most &ldquo;dog problems&rdquo; are handler problems. We train the human end of the leash as seriously as the dog.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div>
    <div class="eyebrow">Where it all points</div>
    <h2>Train for the courtroom, not just the yard.</h2>
    <p class="lead">Every exercise is future evidence. The most important trial your dog will ever be part of begins months before anyone files a motion — in how the team was trained, evaluated, and documented.</p>
    <p>David's work is grounded in the case law that governs detector-dog evidence — <i>Harris, Jardines, Caballes, Rodriguez, Place, Edmond</i> — and in the discipline of separating observation from interpretation on the witness stand. Reliability that can't be documented and explained isn't reliability a court can use.</p>
    <div class="quote">"Reliability is not something we claim. It is something we demonstrate."</div>
    <a class="btn dark" href="/agencies.html">How this protects an agency's case</a>
  </div>
  <div class="card" style="align-self:start">
    <h3 class="mt0">The standard behind it</h3>
    <p class="muted">This method is codified as the <b>LSOC courtroom-defensible standard</b> — the benchmark every dog and handler here is trained and evaluated against. {fill('Confirm relationship between the LSOC standard and the "K9 Alliance Certification Standard" referenced on the original site — same thing, or two standards?')}</p>
    <a class="btn sm" href="/certification.html">About the standard</a>
  </div>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="center"><div class="eyebrow">On integrity</div><h2>The point isn't to win. It's to be right.</h2></div>
  <p class="lead center" style="margin-top:14px">David is a strong advocate for properly trained detector dogs — and an equally strong opponent of using them to &ldquo;beat the system.&rdquo; Honest scrutiny doesn't threaten a competent team; it makes it better. The purpose is to catch offenders, protect the innocent, and present evidence that <i>deserves</i> to be trusted.</p>
</div></section>

{photostrip(METHOD_PHOTOS, heading="Reading the dog through the response.", eyebrow="Behavior is evidence", wash=True)}

<section class="sec"><div class="wrap"><div class="center"><div class="eyebrow">Questions</div><h2>About the method</h2></div>
<div style="max-width:820px;margin:28px auto 0">{faq_html(method_faq)}</div></div></section>

<section class="sec tight"><div class="wrap" style="max-width:900px">{book_callout()}</div></section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Want a team trained this way?</h2>
  <p>Whether you're an agency, a handler, or building a program — this is the standard we work to.</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="/contact.html">Start the conversation</a><a class="btn ghost" href="/resources.html">Read the guides</a></div>
</div></div></section>
"""
method_schema = "[" + ORG_SCHEMA + "," + person_schema + "," + faq_schema(method_faq) + "]"
page("method.html", "The Method: Behavior Is Evidence | K9School — David Latimer",
     "The LSOC approach to detector-dog work: the search before the sit, the Five Phases of behavior, building independent dogs, reducing handler influence, and training for the courtroom.",
     method_body, schema=method_schema, active="/method.html")

# ---------- static assets ----------
(OUT/"styles.css").write_text(CSS, encoding="utf-8")
(OUT/"main.js").write_text(JS, encoding="utf-8")

pages = ["index.html","agencies.html","training.html","consulting.html",
         "detection-dogs.html","method.html","resources.html","proof.html","about.html","certification.html","contact.html",
         "resources-choosing-a-detection-dog.html","resources-become-a-k9-handler.html",
         "resources-starting-a-k9-program.html","resources-narcotics-detection-k9s.html",
         "resources-bed-bug-detection-dogs.html","resources-explosives-detection-k9.html",
         "resources-five-phases-detector-dog-behavior.html","resources-florida-v-harris-k9-handlers.html",
         "resources-handler-influence-invisible-leash.html"]
urls = "".join(f'<url><loc>{SITE}/{p}</loc><changefreq>monthly</changefreq></url>' for p in pages)
(OUT/"sitemap.xml").write_text(
  f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
  encoding="utf-8")
(OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

# 404
notfound = """
<section class="hero"><div class="wrap" style="text-align:center">
  <div class="kick">404</div>
  <h1>That trail went cold.</h1>
  <p class="sub" style="margin-left:auto;margin-right:auto">The page you're after isn't here. Let's get you back on scent.</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="/index.html">Back to home</a><a class="btn ghost" href="/contact.html">Contact us</a></div>
</div></section>
"""
page("404.html", "Page Not Found | K9School",
     "The page you're looking for could not be found.", notfound, active="/404.html")

# Netlify-style redirects (301 from legacy domain; SPA-style fallback to 404)
(OUT/"_redirects").write_text(
  "https://kipk9.com/*    https://www.k9school.net/:splat    301!\n"
  "https://www.kipk9.com/*    https://www.k9school.net/:splat    301!\n"
  "/*    /404.html    404\n", encoding="utf-8")

print("done —", len(pages)+1, "pages + assets")

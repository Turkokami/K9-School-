# -*- coding: utf-8 -*-
"""
K9School.net — Smart Site generator.
Emits a fast, mobile-first static site with a shared design system,
per-page SEO + JSON-LD schema, and segmented lead-capture forms.
Run:  python3 build.py   ->  outputs into ./public
"""
import os, html, pathlib, re, json

OUT = pathlib.Path(__file__).parent / "public"
OUT.mkdir(exist_ok=True)

SITE = "https://www.k9school.net"
BIZ = "Latimer School of Operational K9s"
PHONE = "(205) 966-8739"
PHONE_TEL = "+12059668739"
ADDR = "530 Hackney Street, Lincoln, AL 35096"
TAGLINE = "Trained for the field, not just the yard."
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
/* height:auto is load-bearing. Every img carries width/height attributes for CLS;
   without it the attribute height wins and a 1200x1600 photo renders 1600px tall
   and squashed to the column width. */
img{max-width:100%;height:auto;display:block}
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
.hero-media img{width:100%;border-radius:14px;border:1px solid rgba(255,255,255,.16);box-shadow:0 20px 55px rgba(0,0,0,.5);aspect-ratio:4/3;object-fit:cover;object-position:center 28%}
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
.shot{width:100%;height:auto;border-radius:var(--r);border:1px solid var(--line);box-shadow:var(--shadow)}
.shot.tall{aspect-ratio:4/5;object-fit:cover}
/* Portrait shots are capped by height and centred instead of filling the column,
   so a single figure can't run past the fold. Nothing is cropped. Containers that
   crop to a fixed ratio (.gallery, .hero-media, .fig-2) out-specify this. */
.portrait:not(.tall){max-height:600px;margin-left:auto;margin-right:auto}
.shot.portrait:not(.tall){width:auto;max-width:100%}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:8px}
.gallery figure{margin:0;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:var(--ink);box-shadow:var(--shadow)}
.gallery figure img{width:100%;height:210px;object-fit:cover;object-position:center 32%;display:block;transition:transform .35s ease}
.gallery figure:hover img{transform:scale(1.05)}
.gallery figcaption{padding:10px 13px;font-size:.82rem;color:var(--steel);font-weight:600;background:var(--paper)}

/* INLINE CONTENT FIGURES */
.fig{margin:34px auto;max-width:720px;text-align:center}
.fig img,.fig-2 img{border-radius:var(--r);border:1px solid var(--line);box-shadow:var(--shadow);width:100%;height:auto}
.fig figcaption,.fig-2 figcaption{margin-top:8px;font-size:.82rem;color:var(--mute);font-weight:600;text-align:center}
.fig-2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:34px auto;max-width:920px}
.fig-2 figure{margin:0}
.fig-2 img{aspect-ratio:4/5;object-fit:cover;object-position:center 35%}
@media(max-width:680px){.fig-2{grid-template-columns:1fr}}

/* VIDEO FACADE - poster + play button; the YouTube iframe swaps in on click */
.vid-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;margin-top:22px}
.vid{margin:0}
.vid-btn{position:relative;display:block;width:100%;padding:0;border:1px solid var(--line);background:var(--ink);border-radius:var(--r);overflow:hidden;cursor:pointer;box-shadow:var(--shadow)}
.vid-btn img{width:100%;aspect-ratio:16/9;object-fit:cover;object-position:center 35%;display:block;transition:transform .35s ease}
.vid-btn img.portrait{max-height:none;margin:0}
.vid-btn:hover img{transform:scale(1.04)}
.vid-plate{display:flex;align-items:center;justify-content:center;aspect-ratio:16/9;background:linear-gradient(150deg,var(--navy) 0%,var(--black) 100%);padding:20px}
.vid-plate-t{color:#c4d2dd;font-weight:700;font-size:1rem;line-height:1.35;text-align:center}
.vid-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:60px;height:60px;border-radius:50%;background:rgba(201,162,39,.94);box-shadow:0 6px 20px rgba(0,0,0,.45);transition:background .2s ease}
.vid-play::after{content:"";position:absolute;left:56%;top:50%;transform:translate(-50%,-50%);border-style:solid;border-width:11px 0 11px 19px;border-color:transparent transparent transparent var(--black)}
.vid-btn:hover .vid-play{background:var(--gold-l)}
.vid-btn:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.vid-dur{position:absolute;right:9px;bottom:9px;background:rgba(8,9,13,.86);color:#fff;font-size:.75rem;font-weight:700;padding:2px 7px;border-radius:4px;font-variant-numeric:tabular-nums}
.vid figcaption{margin-top:9px;font-size:.84rem;color:var(--mute);line-height:1.45}
.vid figcaption b{color:var(--ink2)}
.vid iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:var(--r);display:block;box-shadow:var(--shadow)}
.vid-more{margin-top:20px;font-size:.86rem;font-weight:700}
.wash .vid figcaption{color:var(--steel)}

/* CASE STUDY (T9) */
.case{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--gold);
      border-radius:var(--r);padding:30px 34px 26px;box-shadow:var(--shadow);max-width:820px;margin:26px auto 0}
.case h3{font-size:1.62rem;margin:6px 0 0;color:var(--ink2);letter-spacing:-.01em}
.case-fig{margin:22px 0 4px}
.case-fig figcaption{margin-top:8px;font-size:.82rem;color:var(--mute);font-weight:600;text-align:center}
.case-body p{margin:14px 0 0}
.case-take{margin-top:22px;padding:14px 18px;background:var(--wash);border-left:3px solid var(--gold);
           border-radius:0 6px 6px 0;font-size:.95rem}
.case-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;
           margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
.case-meta div{font-size:.82rem;line-height:1.5}
.case-meta b{display:block;font-family:'IBM Plex Mono',Consolas,monospace;font-size:.7rem;
             letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-bottom:3px}
.case-meta span{color:var(--ink2);font-weight:600}
@media(max-width:640px){.case{padding:24px 20px 20px}.case h3{font-size:1.35rem}}

/* STICKY MOBILE CLICK-TO-CALL */
.callbar{display:none}
@media(max-width:760px){
 .callbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:60;align-items:center;justify-content:center;gap:8px;background:var(--gold);color:#0a1a33;font-weight:800;font-size:1rem;padding:13px 16px;text-decoration:none;box-shadow:0 -6px 20px rgba(0,0,0,.2)}
 body{padding-bottom:54px}
}

/* AEO QUICK ANSWER */
.qa-sec{padding-top:0}
.quick-answer{max-width:820px;margin:0 auto;background:var(--wash);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:var(--r);padding:20px 24px}
.quick-answer .qa-label{display:inline-block;font-size:.7rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--amber-d);margin-bottom:6px}
.quick-answer p{margin:0;font-size:1.08rem;line-height:1.62;color:var(--ink)}

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
  // Video facade: swap the poster for a real player only when asked. Nothing from
  // youtube.com is requested until this fires, so the page stays light.
  document.addEventListener('click',function(e){
    var b=e.target.closest?e.target.closest('.vid-btn'):null;
    if(!b) return;
    var id=b.getAttribute('data-yt'); if(!id) return;
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
    f.title=b.getAttribute('aria-label')||'Video';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy='strict-origin-when-cross-origin';
    f.setAttribute('allowfullscreen','');
    b.parentNode.replaceChild(f,b);
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
        <p>{BIZ}. Operational detection dogs and certified handlers — trained for the field, not just the yard.</p>
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

def _json(s): return json.dumps(s, ensure_ascii=False)

# ---------- 7-node schema graph (Keystone Part 5.1): built once, per page ----------
SPEAKABLE = '"speakable":{"@type":"SpeakableSpecification","cssSelector":[".quick-answer",".faq"]}'

# ---------- CITED RESEARCH ----------
# Published work the method actually rests on. Cited properly rather than
# paraphrased as "studies show": an answer engine is materially more likely to
# quote a page that sources real research, and a defense attorney is materially
# less likely to dent one.
STUDIES = {
 "lit2011": (
   "Handler beliefs affect scent detection dog outcomes",
   ["Lisa Lit", "Julie B. Schweitzer", "Anita M. Oberbauer"],
   "2011", "Animal Cognition",
   "https://doi.org/10.1007/s10071-010-0373-2"),
}

# slug -> study keys
CITATIONS = {
 "method.html": ["lit2011"],
 "resources-handler-influence-invisible-leash.html": ["lit2011"],
}

def _citation_ids(slug):
    return [f"{SITE}/#study-{k}" for k in CITATIONS.get(slug, [])]

def _citation_nodes(slug):
    out = []
    for k in CITATIONS.get(slug, []):
        name, authors, year, journal, url = STUDIES[k]
        auth = ",".join('{"@type":"Person","name":%s}' % _json(a) for a in authors)
        out.append('{"@type":"ScholarlyArticle","@id":"%s/#study-%s","name":%s,'
                   '"author":[%s],"datePublished":"%s","isPartOf":{"@type":"Periodical","name":%s},"url":"%s"}'
                   % (SITE, k, _json(name), auth, year, _json(journal), url))
    return out

def _website_node():
    return (f'{{"@type":"WebSite","@id":"{SITE}/#website","url":"{SITE}/",'
            f'"name":{_json(BIZ)},"publisher":{{"@id":"{SITE}/#localbusiness"}}}}')

def _logo_node():
    return (f'{{"@type":"ImageObject","@id":"{SITE}/#logo","url":"{SITE}/og.png",'
            f'"contentUrl":"{SITE}/og.png","caption":{_json(BIZ)}}}')

def _localbusiness_node():
    return ('{"@type":["LocalBusiness","ProfessionalService"],'
      f'"@id":"{SITE}/#localbusiness","name":{_json(BIZ)},"url":"{SITE}",'
      f'"logo":{{"@id":"{SITE}/#logo"}},"image":{{"@id":"{SITE}/#logo"}},'
      f'"telephone":"{PHONE_TEL}","priceRange":"$$$",'
      '"address":{"@type":"PostalAddress","streetAddress":"530 Hackney Street","addressLocality":"Lincoln","addressRegion":"AL","postalCode":"35096","addressCountry":"US"},'
      '"areaServed":"US","founder":{"@type":"Person","@id":"'+SITE+'/about.html#david","name":"David Latimer"},'
      '"description":"Operational detection dog training, handler and instructor certification, program consulting, and placement-ready detection dogs for law enforcement, conservation, and private detection teams.",'
      '"knowsAbout":["detection dog training","narcotics detection","explosives detection","arson accelerant detection","bed bug detection","conservation detection","handler certification","K9 program development"]}')

def _webpage_node(canonical, title, desc, cites=()):
    cite = (',"citation":[' + ",".join('{"@id":"%s"}' % c for c in cites) + ']') if cites else ''
    return (f'{{"@type":"WebPage","@id":"{canonical}#webpage","url":"{canonical}",'
            f'"name":{_json(title)},"description":{_json(desc)},'
            f'"isPartOf":{{"@id":"{SITE}/#website"}},"about":{{"@id":"{SITE}/#localbusiness"}},'
            f'"primaryImageOfPage":{{"@id":"{SITE}/#logo"}},'
            f'"breadcrumb":{{"@id":"{canonical}#breadcrumb"}},{SPEAKABLE}{cite}}}')

def _breadcrumb_node(canonical, crumbs):
    items = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"name":{_json(n)},"item":"{u}"}}'
        for i, (n, u) in enumerate(crumbs))
    return f'{{"@type":"BreadcrumbList","@id":"{canonical}#breadcrumb","itemListElement":[{items}]}}'

def service_node(name, desc, url):
    return (f'{{"@type":"Service","name":{_json(name)},"description":{_json(desc)},'
            f'"serviceType":{_json(name)},"provider":{{"@id":"{SITE}/#localbusiness"}},'
            f'"areaServed":"US","url":"{url}"}}')

def page(slug, title, desc, body, nodes=None, active=None, canonical=None, crumbs=None):
    active = active or ("/"+slug)
    canonical = canonical or f"{SITE}/{slug}"
    # breadcrumb (Keystone: mirror the URL taxonomy)
    page_name = re.split(r'\s*[|—]\s*', title)[0].strip()
    if crumbs is None:
        if slug == "index.html":
            crumbs = [("Home", f"{SITE}/")]
        elif slug.startswith("resources-"):
            crumbs = [("Home", f"{SITE}/"), ("Resources", f"{SITE}/resources.html"), (page_name, canonical)]
        else:
            crumbs = [("Home", f"{SITE}/"), (page_name, canonical)]
    graph = [_website_node(), _localbusiness_node(), _logo_node(),
             _webpage_node(canonical, title, desc, _citation_ids(slug)),
             _breadcrumb_node(canonical, crumbs)]
    graph += _citation_nodes(slug)
    graph += [n for n in (nodes or []) if n]
    graph += video_nodes(slug, canonical)
    graph += case_nodes(slug, canonical)
    schema_block = ('<script type="application/ld+json">'
                    '{"@context":"https://schema.org","@graph":[' + ",".join(graph) + ']}</script>')
    # AEO Quick Answer (Keystone Block #1): inject after the hero, hooked for Speakable
    qa = QUICK_ANSWERS.get(slug)
    if qa:
        qblock = ('<section class="sec tight qa-sec"><div class="wrap"><div class="quick-answer" data-speakable="true">'
                  '<span class="qa-label">In short</span><p>' + qa + '</p></div></div></section>')
        i = body.find("</section>")
        body = (body[:i+10] + "\n" + qblock + "\n" + body[i+10:]) if i != -1 else (qblock + body)
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
<a class="callbar" href="tel:{PHONE_TEL}" aria-label="Call David at {PHONE}">📞 Call David — {PHONE}</a>
<script src="/main.js"></script>
</body>
</html>"""
    (OUT/slug).write_text(doc, encoding="utf-8")
    print("wrote", slug)

def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' %
        (_json(q), _json(a)) for q,a in pairs)
    return '{"@type":"FAQPage","mainEntity":[%s]}' % items

def faq_html(pairs):
    rows = ""
    for q,a in pairs:
        rows += f"<details><summary>{q}</summary><p>{a}</p></details>"
    return f'<div class="faq">{rows}</div>'

# clearly-marked placeholder helper
def fill(txt): return f'<span class="fill">[{txt}]</span>'

# AEO Quick Answers (Keystone Block #1) — 40-60 words, answer-first, quotable verbatim.
# page() injects the matching one right after the hero and marks it Speakable.
QUICK_ANSWERS = {
 "index.html": "K9School is the operational detection-dog practice of David Latimer — a retired police chief, FBI National Academy graduate, and detector-dog trainer since 1999. We train, certify, consult on, and place detection dogs and handlers built to perform in the field and hold up in court, to the LSOC courtroom-defensible standard.",
 "agencies.html": "For law enforcement, K9School delivers finished detection dogs and certified handlers built for deployment and documented to a defensible standard. A reliable K9 is a liability decision before a training one, so every team is trained, blind-tested, and recorded to survive the audit, the hearing, and cross-examination.",
 "training.html": "K9School's handler and instructor courses teach you to read the dog, not just reward the sit — running clean searches, recognizing the change of behavior, controlling your own influence, and documenting the work. Foundation, handler, and instructor tracks build real field competence to the LSOC standard, not just a certificate.",
 "consulting.html": "K9School helps agencies and organizations build detection programs from scratch or fix ones that won't survive an audit — selection, testing, handler development, and standards-based evaluation. Guidance comes from David Latimer, a retired police chief and expert witness who has answered for programs under real scrutiny.",
 "detection-dogs.html": "K9School places detection dogs for bed bug, arson, conservation, narcotics, explosives, and firearms work — selected for the environment you actually work in and paired with handler training. You buy a team, not just a dog: a dog matched to the job and a handler trained to read it.",
 "method.html": "The LSOC method treats behavior as evidence: a detector dog is communicating from the first breath of a search, and the handler's job is to read the whole sequence — the Five Phases — not just reward the final sit. Teams are trained honestly, tested blind, and documented to be courtroom-defensible.",
 "certification.html": "The LSOC courtroom-defensible standard evaluates a detection team the way a court would — reliability under field conditions, independent work proven by blind and double-blind testing, a handler who can explain the behavior, and honest documentation including failures. Certification is a defensible benchmark, never a guarantee of perfection.",
 "proof.html": "K9School's credibility rests on verifiable proof, not adjectives — case studies, agency references, certification records, and field footage of teams working real problems. Founder David Latimer is a retired police chief, FBI National Academy graduate, detector-dog trainer since 1999, and expert witness on detection-dog reliability.",
 "about.html": "David Latimer is the operator behind K9School — a retired chief of police, FBI National Academy graduate, and detector-dog trainer since 1999 across arson, narcotics, explosives, cadaver, tracking, and pest detection. He trains, certifies, consults, and testifies as an expert witness, and authored the LSOC method.",
 "contact.html": "Reach K9School to request an agency capability brief, apply for handler or instructor training, book a program assessment, or check detection-dog availability. Agency and consulting inquiries reach David Latimer directly; each form routes by audience so your request goes to the right next step.",
 "resources.html": "K9School's resource library offers free, field-tested guides on choosing a detection dog, becoming a handler, building or fixing a K9 program, and the disciplines we work — narcotics, bed bug, arson, and explosives — plus the method behind courtroom-defensible detection. Written from operational experience, not marketing.",
 "resources-choosing-a-detection-dog.html": "Choosing a detection dog starts with the job, not the dog: define the target odors, environment, and workload first, then evaluate hunt drive, environmental confidence, stamina, and stability. Watch the dog work a cold, realistic problem, insist on a blank-area test, and buy the team — dog plus trained handler.",
 "resources-become-a-k9-handler.html": "Becoming a detection handler means becoming someone a dog can rely on — learning to present a search, read the change of behavior, control your own influence, and document the work. Choose field-first training that certifies to a recognized standard and develops the handler, not just the dog.",
 "resources-starting-a-k9-program.html": "Starting or fixing a K9 program begins by defining the mission and the standard you'll hold teams to, then selecting dogs and handlers systematically and building maintenance and honest records from day one. Blind testing and documentation are what let a program survive an audit or a courtroom challenge.",
 "resources-narcotics-detection-k9s.html": "A narcotics detection K9 is an evidentiary tool as much as an operational one. Reliability is a legal question — courts scrutinize training, certification, and maintenance records — so build the paper trail from day one, test blind to prove the dog works odor and not the handler, and train handlers to describe behavior.",
 "resources-bed-bug-detection-dogs.html": "For pest control, a bed bug detection dog is a revenue and reputation decision: a reliable dog inspects a room in minutes, opens a premium service line, and wins commercial accounts. Accuracy comes from the whole team and its maintenance — and an honest dog that clears a clean room protects your brand.",
 "resources-explosives-detection-k9.html": "Explosives detection is the discipline with the least room for error, so selection, training, and maintenance standards run higher. Operational reliability means the team performs in realistic environments and works independently, proven by blind testing — never a claim of 100% accuracy, which no honest trainer makes.",
 "resources-five-phases-detector-dog-behavior.html": "The Latimer Five-Phase Model describes a detector-dog search as: responds to the search command, systematic search, detection, change of behavior, and trained final response. Phases three and four are the investigation — where the dog actually solves the problem — and naming them lets a handler observe, document, and testify precisely.",
 "resources-florida-v-harris-k9-handlers.html": "Florida v. Harris (2013) holds that a detector dog's reliability is judged by the totality of the circumstances, not a rigid checklist — training and certification matter, but the defense can still challenge them. A certificate is a benchmark, not a magic shield; honest records and blind testing are what hold up.",
 "resources-handler-influence-invisible-leash.html": "The Invisible Leash is unconscious handler influence — the physical, visual, verbal, and emotional cues a dog reads from the person on the leash, as the Clever Hans case and Dr. Lisa Lit's research show. Honest teams don't deny it; they manage it and audit for it with blind and double-blind testing.",
}

# intrinsic dimensions for width/height (prevents CLS); WebP for LCP.
# Produced by optimize_images.py; stdlib json keeps build.py dependency-free.
_DIMS_FILE = pathlib.Path(__file__).parent / "image-dims.json"
_DIMS = json.loads(_DIMS_FILE.read_text(encoding="utf-8")) if _DIMS_FILE.exists() else {}

def img(name, alt, cls="shot", style="", eager=False):
    webp = name.rsplit(".", 1)[0] + ".webp"
    use = webp if webp in _DIMS else name
    wh = _DIMS.get(use) or _DIMS.get(name)
    dim = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    # Most of the library is portrait phone photos. Tag anything taller than a
    # comfortable landscape (h/w > 0.84, so portrait *and* near-square) and let the
    # CSS cap it by height — a 3:4 shot in a 720px column is 960px tall and eats the
    # whole viewport. 4:3 and wider keep the full column width.
    if wh and wh[1] / wh[0] > 0.84:
        cls = (cls + " portrait").strip()
    st = f' style="{style}"' if style else ""
    ld = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img class="{cls}" src="/images/{use}" alt="{html.escape(alt)}"{dim}{ld} decoding="async"{st}>'

def gallery(items):
    figs = "".join(
        f'<figure>{img(fn, cap, cls="")}<figcaption>{html.escape(cap)}</figcaption></figure>'
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

def hero_media(item, eager=True):
    fn, cap = item
    caph = f'<div class="cap">{html.escape(cap)}</div>' if cap else ""
    return f'<div class="hero-media">{img(fn, cap, cls="", eager=eager)}{caph}</div>'

def hero_grid(inner_copy, hero_item):
    """Wrap existing hero copy + a hero image into the two-column grid."""
    if not hero_item:
        return inner_copy
    return f'<div class="hero-grid"><div class="hero-copy">{inner_copy}</div>{hero_media(hero_item)}</div>'

def figure(item):
    fn, cap = item
    return f'<figure class="fig">{img(fn, cap)}<figcaption>{html.escape(cap)}</figcaption></figure>'

def figure2(a, b):
    # cls="" on purpose: the pair is cropped to a shared aspect ratio by `.fig-2 img`
    # so the two columns line up. The `.shot` height cap would fight that.
    return (f'<div class="fig-2">'
            f'<figure>{img(a[0], a[1], cls="")}<figcaption>{html.escape(a[1])}</figcaption></figure>'
            f'<figure>{img(b[0], b[1], cls="")}<figcaption>{html.escape(b[1])}</figcaption></figure></div>')

# Landscape hero image per page (portrait phone photos crop badly in a wide hero).
HERO_PHOTOS = {
    "agencies.html": ("lsoc-82-patrol-car.jpg", "A K9 unit ready for patrol"),
    "training.html": ("lsoc-14-training-day-a.jpg", "Training day in the field"),
    "consulting.html": ("lsoc-119-clas-pic.jpg", "A full class of handler teams"),
    "detection-dogs.html": ("lsoc-125-dog-and-toy.jpg", "A detection dog in drive"),
    "method.html": ("lsoc-95-dog-points-to-odor.jpg", "Working a structure to source"),
    "proof.html": ("lsoc-67-jinx-and-money.jpg", "Currency detection — Jinx on a seizure"),
    "about.html": ("lsoc-12-me-tatsa-georgia-and-midnight.jpg", "David Latimer with his dogs"),
    "certification.html": ("lsoc-97-ak-team.jpg", "A certified detection team"),
    "contact.html": ("lsoc-120-training-day-patrol-cars.jpg", "Teams on a training day"),
    "resources.html": ("lsoc-77-training-day-patrol-cars.jpg", "Field training with working teams"),
}

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
# ---------- VIDEO (David's YouTube channel) ----------
# Facade embeds: a self-hosted poster + play button. The YouTube iframe and its
# ~1MB of player JS load only on click, so the performance gate survives. Upload
# dates and durations are the real values read off the channel - VideoObject
# fields are never guessed. VIDEOS holds all 30 public videos; VIDEO_PAGES decides
# what is placed where and drives BOTH the markup and the schema, so the rendered
# block and the graph cannot drift apart.
YT_CHANNEL = "https://www.youtube.com/@alfirek9"

# id: (display title, upload date, seconds, poster image or None, caption)
VIDEOS = {
 "X4S-qg_rRj4": ("LSOC promotional video", "2026-08-17", 47, "lsoc-124-training-day-patrol-cars.jpg",
   "Who we are and the standard we train to."),
 "9kyLVQTYVgg": ("Bella, days one through seven", "2026-08-17", 302, "lsoc-66-dog-and-mari.jpg",
   "A green dog's first week, start to finish."),
 "G9FgEWuuEIo": ("Zeus, long track in Alaska", "2023-12-03", 202, "lsoc-79-tracking-team-in-ak.jpg",
   "A long track worked in open country."),
 "jegeVYJh5N8": ("Tracking training basics", "2023-11-22", 200, "lsoc-54-tracking-dog-class.jpg",
   "How a tracking problem is laid and then worked."),
 "xouG9aoSAaQ": ("Drug dog opens a car door and gets to source", "2023-11-13", 45, "lsoc-78-mal-sniffing-car.jpg",
   "Independent work. The dog solves the access problem itself."),
 "2m4PP_SM154": ("Zeus on the boxes", "2023-07-14", 60, "lsoc-28-dexter-on-car.jpg",
   "Box work, discrimination and source commitment."),
 "8CnyvXSHqUw": ("Build drive first, then channel it", "2023-07-14", 61, "lsoc-131-wal-mounted-ball-droppers.jpg",
   "Drive is the engine. Watch what it gets aimed at."),
 "G50kgkz4hr4": ("Malinois puppy, first day on odor", "2023-02-03", 61, "lsoc-47-josh-and-aki.jpg",
   "How a detector dog is started on odor."),
 "QBof9goDcUA": ("FSI introduction", "2014-02-16", 127, "lsoc-7-me-na.jpg",
   "An earlier program David built and ran."),
 "OoZAgXv9EPI": ("Handling, good loose leash", "2013-11-24", 69, "lsoc-101-lab-straining-at-leash.jpg",
   "What the leash should be doing, and what it should not."),
 "C1TuYB0zMqM": ("Handling, too much bending", "2013-11-24", 13, "lsoc-103-lab-strains-on-leash.jpg",
   "Handler posture working as an unintended cue."),
 "ChiIklfwuiE": ("Handling, reading a false alert", "2013-11-24", 17, "lsoc-102-lab-alerts.jpg",
   "The response happens. The behavior before it tells you why."),
 "iLyVej-TRqI": ("Handling, minimal direction and teaching source", "2013-11-24", 58, "lsoc-95-dog-points-to-odor.jpg",
   "Letting the dog solve it instead of steering it."),
 "kpm41NdRBmg": ("Handling, how not to teach a dog to go to source", "2013-11-24", 33, "lsoc-122-dog-reaching-for-source.jpg",
   "A common error, shown rather than described."),
 "s2Vmdx5ryQU": ("Handling, do not stop in one place too long", "2013-11-24", 14, "lsoc-105-lab-saeching-for-source.jpg",
   "Pausing at a spot tells the dog something you did not mean to say."),
 "XXgvWsE8MjA": ("Handling, get in and get out", "2013-11-24", 87, "lsoc-104-lab-freeze-alert.jpg",
   "Presenting an area without contaminating it."),
 "XwsecmvVnz4": ("Fire scene training", "2013-11-15", 140, None, "Accelerant work on a training burn."),
 "1hAz4CbobEI": ("Arson dogs", "2013-06-28", 76, "lsoc-52-arson-dog-team.jpg",
   "Accelerant detection, where David started in 1999."),
 "VYtCQ3wnUbM": ("Loretta", "2013-05-27", 96, None, "Training footage."),
 "Z-qdXjkgqME": ("Loretta, part two", "2013-05-27", 136, None, "Training footage."),
 "LT_eGPMY9Go": ("David Latimer describing a search", "2013-03-26", 444, "lsoc-27-me-skeptical.jpg",
   "Seven minutes on how a search should actually be read."),
 "Ai3v9fhGhdU": ("Double blind, narrated", "2013-03-18", 439, "lsoc-130-scent-board.jpg",
   "A blind test run and explained as it happens."),
 "fJxvo_tiPxg": ("Cadaver dog and distractor", "2013-03-13", 357, "lsoc-56-delmetrius-and-yance.jpg",
   "Working target odor against a competing distractor."),
 "HukdZexYIyM": ("Steven Karaduzovic", "2013-02-25", 75, None, "Handler testimonial."),
 "Vri7hMSJBic": ("Steve Yerger, explosives and bed bug detection", "2013-02-24", 88, None, "Seminar testimonial."),
 "UoZzwuJRJRg": ("Nathaniel Levin, one week of K9 training", "2013-02-24", 30, None, "Academy testimonial."),
 "Bx6V542uOP0": ("Devin Reynolds", "2013-02-24", 36, None, "Handler testimonial."),
 "By-pe2vxckQ": ("Rick Chapel, Tennessee", "2013-02-24", 31, None, "Handler testimonial."),
 "uGHDToZpcGM": ("Jonas Wilkey", "2013-02-24", 47, None, "Handler testimonial."),
 "elujMHiMWss": ("Mike Hanna", "2013-02-24", 40, None, "Handler testimonial."),
}

# slug: (eyebrow, heading, sub, [video ids], wash background)
VIDEO_PAGES = {
 "index.html": ("Watch", "See the work.", "", ["X4S-qg_rRj4"], False),
 "agencies.html": ("Watch", "A blind test, run and narrated.",
   "Blind testing is what separates a defensible record from a hopeful one. Here is one, start to finish.",
   ["Ai3v9fhGhdU"], False),
 "training.html": ("Watch", "A green dog's first week.",
   "Days one through seven with Bella, and what actually changes day by day.", ["9kyLVQTYVgg"], False),
 "method.html": ("Watch", "The method, on film.",
   "Behavior is easier to see than to describe. These are David's own training clips.",
   ["LT_eGPMY9Go", "8CnyvXSHqUw", "G50kgkz4hr4"], True),
 "detection-dogs.html": ("Watch", "The disciplines, working.",
   "Narcotics, cadaver, accelerant and tracking. The same field-first approach across every one.",
   ["2m4PP_SM154", "fJxvo_tiPxg", "1hAz4CbobEI", "G9FgEWuuEIo", "jegeVYJh5N8"], True),
 "about.html": ("Watch", "An earlier program.", "", ["QBof9goDcUA"], False),
 "proof.html": ("Watch", "Handlers, in their own words.",
   "Filmed during earlier seminars and academies. Nothing here is scripted.",
   ["HukdZexYIyM", "Vri7hMSJBic", "UoZzwuJRJRg", "Bx6V542uOP0", "By-pe2vxckQ", "uGHDToZpcGM", "elujMHiMWss"], True),
 "resources-five-phases-detector-dog-behavior.html": ("Watch", "The phases, on film.", "",
   ["kpm41NdRBmg", "iLyVej-TRqI"], False),
 "resources-handler-influence-invisible-leash.html": ("Watch", "Handler influence, shown.",
   "Five short clips. In each one you can watch the dog answer something the handler did not mean to say.",
   ["ChiIklfwuiE", "OoZAgXv9EPI", "C1TuYB0zMqM", "s2Vmdx5ryQU", "XXgvWsE8MjA"], False),
 "resources-narcotics-detection-k9s.html": ("Watch", "Independent work on a vehicle.", "",
   ["xouG9aoSAaQ"], False),
}

def _iso_dur(sec):
    m, s2 = divmod(int(sec), 60)
    return "PT%dM%dS" % (m, s2) if m else "PT%dS" % s2

def video(vid):
    title, date, secs, poster, cap = VIDEOS[vid]
    m, s2 = divmod(secs, 60)
    label = html.escape("Play video: " + title)
    if poster:
        media = img(poster, title + " - video still", cls="vid-poster")
    else:
        media = '<span class="vid-plate"><span class="vid-plate-t">%s</span></span>' % html.escape(title)
    return ('<figure class="vid">'
            '<button class="vid-btn" type="button" data-yt="%s" aria-label="%s">'
            '%s<span class="vid-play" aria-hidden="true"></span>'
            '<span class="vid-dur">%d:%02d</span></button>'
            '<figcaption><b>%s</b><br>%s</figcaption></figure>'
            % (vid, label, media, m, s2, html.escape(title), html.escape(cap)))

def video_strip(slug):
    """Render the video block for a page. Empty string when the page has none."""
    v = VIDEO_PAGES.get(slug)
    if not v:
        return ""
    eyebrow, heading, sub, ids, wash = v
    subp = '<p class="lead" style="max-width:64ch">%s</p>' % sub if sub else ""
    note = ""
    if slug == "proof.html":
        # These are real named people filmed under the earlier FSI brand. Do not
        # publish the section until David confirms we may use their names.
        note = ('<p class="lead" style="max-width:64ch">'
                + fill("confirm we may feature these handlers by name") + '</p>')
    grid = "".join(video(i) for i in ids)
    cls = "sec tight wash" if wash else "sec tight"
    return ('<section class="%s"><div class="wrap">'
            '<div class="eyebrow">%s</div><h2>%s</h2>%s%s'
            '<div class="vid-grid">%s</div>'
            '<p class="vid-more"><a href="%s" rel="noopener">More video on the channel</a></p>'
            '</div></section>' % (cls, eyebrow, heading, subp, note, grid, YT_CHANNEL))

def video_nodes(slug, canonical):
    v = VIDEO_PAGES.get(slug)
    if not v:
        return []
    out = []
    for vid in v[3]:
        title, date, secs, poster, cap = VIDEOS[vid]
        thumb = (SITE + "/images/" + poster.rsplit(".", 1)[0] + ".webp") if poster else SITE + "/og.png"
        out.append('{"@type":"VideoObject",'
            '"@id":"%s#video-%s","name":%s,"description":%s,'
            '"uploadDate":"%s","duration":"%s","thumbnailUrl":"%s",'
            '"contentUrl":"https://www.youtube.com/watch?v=%s",'
            '"embedUrl":"https://www.youtube-nocookie.com/embed/%s",'
            '"publisher":{"@id":"%s/#localbusiness"},"isPartOf":{"@id":"%s#webpage"}}'
            % (canonical, vid, _json(title), _json(cap), date, _iso_dur(secs), thumb,
               vid, vid, SITE, canonical))
    return out

# ---------- CASE STUDIES (Keystone T9) ----------
# The highest-trust asset on the site and the one most often missing. Told the way
# David tells them: what happened, then what it changed. Hedges stay in - the value
# of the Tatsa story is that he calls his own explanation a hypothesis rather than
# a finding. Schema is honest CreativeWork: no ratings, no invented dates.
CASE_STUDIES = {
 "lucy-and-the-baby-doll": dict(
   kicker="Case study — explosives",
   title="The box Lucy cleared, and the squad blew up anyway",
   photo=None,
   dog="Lucy",
   discipline="Explosives detection",
   outcome="No explosive odor present. The dog was right; the decision went the other way.",
   body=[
     "After Boomer passed away I started training my wife's Border Collie, Lucy, on explosives. She "
     "took to it almost immediately, and before long we were training regularly with the bomb squad "
     "from a larger department. Those men were professionals who believed training should be as "
     "realistic as possible. Their commander built scenarios that forced the team to think like "
     "investigators rather than technicians — evaluate the evidence, make a decision, solve the "
     "problem under conditions that looked like a real call.",

     "One exercise has stayed with me ever since. A cardboard box had been left at the entrance to a "
     "shopping center before opening, reported by patrol after a bomb threat. The centre was closed, "
     "so the squad had the whole property to work with. They approached the box, elected not to X-ray "
     "it, and decided to deploy Lucy to find out whether explosive odor was present.",

     "I gave her the command to search. The box was the only object in the area, so of course it drew "
     "her. She worked it thoroughly, every side. I watched for the behavior that always came before "
     "her trained final response when she was in odor. It never came. No increase in interest. No "
     "change in breathing. No increased focus. No source commitment. She satisfied her curiosity, "
     "left the box, and carried on searching the area around it. She had run the problem and reached "
     "a conclusion. It just was not the conclusion the humans expected.",

     "After a few minutes I called her back and reported that Lucy found no indication of explosive "
     "odor. For reasons I have never fully understood, the decision was made to proceed as though a "
     "device was inside anyway. A water cannon was brought up, the stand-off distance calculated, the "
     "operators careful and methodical and entirely professional. Then they fired. The box came apart "
     "and a life-sized plastic baby doll bounced across the parking lot.",

     "Nobody said anything for a moment. The exercise had never been about destroying a suspicious "
     "package. It was about making a sound decision on the available evidence. By that standard the "
     "team failed. Lucy did not. She investigated, evaluated, reached a conclusion and moved on. She "
     "never hesitated, never guessed, and never changed her answer because experienced people believed "
     "something different.",

     "That is what <i>Credo Vestri Canis</i> means to me. Trust your dog.",
   ],
   takeaway="A trained dog reporting no odor is information, not the absence of information. If you "
            "only believe the dog when it says yes, you do not actually have a detection capability — "
            "you have a device that confirms what you already thought.",
 ),
 "boomer-and-contamination": dict(
   kicker="Case study — the failure that changed the method",
   title="The bullet Boomer could not find",
   photo=None,
   dog="Boomer",
   discipline="Explosives detection",
   outcome="A public failure that exposed what the dog had actually been trained on",
   body=[
     "Boomer was my first explosives dog and he taught me more than any dog since. One thing he did "
     "looked genuinely impressive: he could find a single round of ammunition, fast. I ran that demo "
     "many times. Pop the magazine out of my Glock, take out a round, toss it into grass or somewhere "
     "it was out of sight, send Boomer, and within a few minutes he would be sitting and pointing his "
     "nose at it. It never failed.",

     "Then one day another officer and I were at a gathering with a lot of other police there. I had "
     "Boomer with me for socialisation. My colleague wanted to show people what the dog could do, so "
     "he popped a round out of <b>his</b> Glock and threw it into a grassy area. I sent Boomer and he "
     "engaged hard, sniffing, working. I had no reason to think he would not be sitting on it within "
     "the minute.",

     "The minutes went by. It became obvious he was not going to find it. That was one of the most "
     "humbling things that has happened to me in this work, and it happened in front of a crowd of "
     "cops.",

     "I thought about it for a long time afterwards, mostly because I never wanted it to happen again. "
     "I knew dogs could find ammunition, so something was wrong, and I suspected the something was me. "
     "It was. Eventually it dawned on me what had actually been going on. Boomer was not finding a "
     "bullet. He was finding an object that carried the odor of my hands. Every round I had ever "
     "thrown had been handled by me first.",

     "That taught me three things I have never let go of. Human odor is enormously strong to a dog. A "
     "dog can tell one person's odor from another's. And a training set-up can quietly teach a dog "
     "something completely different from what you believe you are teaching it, while producing "
     "results that look like success every single time.",
   ],
   takeaway="For months I thought I had a dog that could find ammunition. What I actually had was a "
            "dog that could find me. That is what stimulus control means, and it is why we test for it "
            "rather than assume it.",
 ),
 "tatsa-cleared-vehicle": dict(
   kicker="Case study — narcotics",
   title="The find another dog had already cleared",
   photo=("lsoc-12-me-tatsa-georgia-and-midnight.jpg", "David with Tatsa and the team"),
   dog="Tatsa",
   discipline="Narcotics detection",
   outcome="Crack cocaine, packaged for distribution, behind the driver's seat",
   body=[
     "We were called out to work a vehicle for another agency. When we got there five or six "
     "patrol cars were already on scene. Must be a big deal, I thought. The officer who made the "
     "stop asked me to run Tatsa on the pickup and tell him what we found.",

     "I took her to the grass for a break and we approached from the passenger side. She engaged "
     "and started to work. Coming past the driver's door she stopped hard, changed direction back "
     "toward it, sniffed for a minute, and sat with her nose pointed at the door. I signalled the "
     "alert. The officer opened the door and reached in behind the seat almost immediately: a "
     "plastic bottle of crack rocks, individually wrapped in foil, packaged for distribution.",

     "Then I was told a K9 team had already worked that truck and cleared it. Had I known that "
     "before I came, I probably would not have come.",

     "That one stayed with me. I wanted to know why the other dog did not alert, and I have since "
     "learned there are a lot of possible reasons. But one of the most common is handler influence "
     "— and almost everyone discusses it in one direction only. Handlers are trained not to cue a "
     "dog into a false alert. I think influence can just as easily cause a miss. If a dog has "
     "become handler-dependent and is waiting on a cue it is used to getting, it can find the odor, "
     "never get the cue, and never give the trained final response.",

     "The handler that day was new, and this is a hypothesis on my part, not something I can prove "
     "about that dog. But knowing what I know now it is a reasonable explanation, and it is a large "
     "part of why I built training strategies to reduce handler influence. We have to guard against "
     "influencing a dog into a false alert. We also have to guard against influencing one into a miss.",
   ],
   takeaway="A miss is harder to catch than a false alert. Nobody audits the vehicle you drove away from.",
 ),
}

def case_study(key, flagged=""):
    c = CASE_STUDIES[key]
    paras = "".join(f"<p>{t}</p>" for t in c["body"])
    fig = ""
    if c.get("photo"):
        fn, cap = c["photo"]
        fig = (f'<figure class="case-fig">{img(fn, cap)}'
               f'<figcaption>{html.escape(cap)}</figcaption></figure>')
    meta = "".join(f'<div><b>{k}</b><span>{v}</span></div>'
                   for k, v in (("Dog", c["dog"]), ("Discipline", c["discipline"]), ("Outcome", c["outcome"])))
    return (f'<article class="case" id="{key}">'
            f'<div class="eyebrow">{c["kicker"]}</div><h3>{c["title"]}</h3>'
            f'{fig}'
            f'<div class="case-body">{paras}{flagged}</div>'
            f'<div class="case-take"><b>What it changed:</b> {c["takeaway"]}</div>'
            f'<div class="case-meta">{meta}</div></article>')

def case_nodes(slug, canonical):
    if slug != "proof.html":
        return []
    out = []
    for key, c in CASE_STUDIES.items():
        img_url = ((f'{SITE}/images/' + c["photo"][0].rsplit(".", 1)[0] + ".webp")
                   if c.get("photo") else f'{SITE}/og.png')
        desc = c["body"][0][:200]
        out.append('{"@type":"CreativeWork","@id":"%s#%s","name":%s,"genre":"Case study",'
                   '"inLanguage":"en-US","description":%s,"isPartOf":{"@id":"%s#webpage"},'
                   '"creator":{"@id":"%s/#localbusiness"},"author":{"@id":"%s/about.html#david"},'
                   '"about":{"@type":"Service","name":%s,"provider":{"@id":"%s/#localbusiness"}},'
                   '"image":["%s"]}'
                   % (canonical, key, _json(c["title"]), _json(desc), canonical, SITE, SITE,
                      _json(c["discipline"]), SITE, img_url))
    return out

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
      <h1>Trained for the field, <span class="amb">not just the yard.</span></h1>
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

{video_strip("index.html")}

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
page("index.html", "Operational Detection Dog Training & Placement | K9School",
     "Detection dogs and certified handlers for law enforcement, conservation, and private teams — trained and certified to the LSOC courtroom-defensible standard.",
     home_body, nodes=[faq_schema(home_faq)], active="/index.html")

# ============================================================
# Reusable hub builder
# ============================================================
def hub(slug, cls, eyebrow, h1, sub, cta_label, cta_href, proof_items, offer_html, faq, seo_title, seo_desc, crumb, photos=None, deep=""):
    faq_h = faq_html(faq)
    photos = photos or []
    hero_item = HERO_PHOTOS.get(slug)
    fig_a = figure(photos[0]) if len(photos) >= 1 else ""
    fig_b = figure2(photos[1], photos[2]) if len(photos) >= 3 else ""
    fig_c = figure(photos[3]) if len(photos) >= 4 else ""
    fig_c_sec = f'<section class="sec tight"><div class="wrap">{fig_c}</div></section>' if fig_c else ""
    hero_copy = (f'<div class="crumb"><a href="/index.html">Home</a> / {crumb}</div>'
                 f'<div class="kick">{eyebrow}</div><h1>{h1}</h1><p class="sub">{sub}</p>'
                 f'<div class="btnrow"><a class="btn" href="{cta_href}">{cta_label}</a>'
                 f'<a class="btn ghost" href="tel:{PHONE_TEL}">Call David: {PHONE}</a></div>')
    body = f"""
<section class="hero">
  <div class="wrap">{hero_grid(hero_copy, hero_item)}</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="eyebrow">Proof that matters to you</div>
    <h2>Built to remove your risk.</h2>
    <div class="grid g3" style="margin-top:28px">{proof_items}</div>
    {fig_a}
  </div>
</section>

<section class="sec wash">
  <div class="wrap">{offer_html}
    {fig_b}
  </div>
</section>

{deep}

{video_strip(slug)}

<section class="sec">
  <div class="wrap"><div class="center"><div class="eyebrow">Before you decide</div><h2>The questions you're already asking</h2></div>
  <div style="max-width:820px;margin:30px auto 0">{faq_h}</div></div>
</section>

{fig_c_sec}

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>{h1_cta(h1)}</h2>
  <p>{sub}</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="{cta_href}">{cta_label}</a></div>
</div></div></section>
"""
    svc = service_node(re.sub(r'<[^>]+>', '', h1), re.sub(r'<[^>]+>', '', sub), f"{SITE}/{slug}")
    page(slug, seo_title, seo_desc, body, nodes=[svc, faq_schema(faq)], active="/"+slug)

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
ag_deep = """
<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The real decision</div>
  <h2>A K9 is a liability decision before it's a training decision.</h2>
  <p>When a dog rides in a patrol car, it is not just a tool your unit uses — it is a witness your cases will rest on and a decision your agency will have to defend. Every deployment that dog makes becomes part of a chain that ends, sometimes, in a courtroom, a review board, or a headline. That is the part of the purchase that rarely gets priced. A cheap dog that alerts unreliably, or a handler who cannot explain what the dog actually did, does not save you money. It costs you cases, it costs you credibility, and one bad ruling can taint every deployment that came before it.</p>
  <p>We build for that reality first. The question we help you answer is not "can this dog find the aid in a controlled yard?" Almost any dog can do that. The question is: will this team hold up in the environment you actually work, under the scrutiny you will actually face — the suppression hearing, the internal audit, the cross-examination months after everyone has forgotten the details? If a team cannot survive that, it does not matter how flashy it looks on a demo. We would rather you buy the team that survives it.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">What you're actually buying</div>
  <h2>A finished dog is only half a deployable team.</h2>
  <p>Reliability is a property of the dog and the handler together, so we do not sell a dog and wish you luck. A deployable team is a finished detection dog matched to the work it will really do — single- or dual-purpose, selected for the environment, the tempo, and the odors your mission demands — paired with a handler certified to run it. The best dog in the country underperforms with an undertrained handler, and a sharp handler is grounded without a sound dog. We deliver both ends of the leash, together, evaluated as a unit.</p>
  <p>"Finished" means the dog works the odor problem and reports honestly, including the honest "there is nothing here" that keeps a dog from manufacturing answers under pressure. It means the handler can read the dog through the <a href="/method.html">Five Phases</a> — command, search, detection, change of behavior, response — and can articulate what happened, not just that the dog sat. A handler who can only say "the dog alerted" is a handler who will struggle the first time a defense attorney asks a harder question. We train yours to answer it.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Courtroom-defensible by design</div>
  <h2>The strongest evidence is the paperwork nobody sees at the traffic stop.</h2>
  <p>Months after a deployment, the dog cannot testify and memory gets picked apart. What remains is the record. That is why every team we build is documented the way it would be read aloud in court — training logs, maintenance history, and testing results that include the misses, not just the finds. A training record with no failures in it is not proof of a perfect dog; it is proof of a dishonest logbook, and any competent attorney knows it. Honest documentation of a dog's real error rate is not a weakness to hide. It is the foundation of a reliability a court can actually use.</p>
  <p>We prove that reliability with blind and double-blind testing, so the record shows the dog works the odor and not the handler's expectation. Our approach is grounded in the case law that governs this work — <i>Harris, Jardines, Caballes, Rodriguez, Place, Edmond</i> — and in training handlers to keep observation and interpretation in separate sentences on the stand. See how we build it on <a href="/method.html">The Method</a>, and how we document it against the <a href="/certification.html">LSOC courtroom-defensible standard</a>.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Expert-witness &amp; litigation support</div>
  <h2>When a deployment is challenged, you want the record — and the witness.</h2>
  <p>David Latimer is a retired chief of police and FBI National Academy graduate who reviews detector-dog cases and testifies as an expert. That work is always done on the basis of honest evaluation — the goal is truth, never to manufacture a result or "beat" the other side. For an agency, that matters twice over: it means the teams we build are trained by someone who knows exactly how they will be tested in litigation, and it means that when your program or a specific deployment is challenged, you have access to a reviewer who can speak to reliability, documentation, and defensibility in language a court understands. See <a href="/consulting.html">Consulting</a> for program-level and litigation support.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Single- or dual-purpose</div>
  <h2>Equipped for your mission, maintained after it ships.</h2>
  <p>We place single-purpose detection dogs and dual-purpose dogs across the disciplines agencies actually need — narcotics, explosives, firearms, currency, and electronic-storage detection — selected for the tempo and environment of your unit rather than sold off a one-size shelf. A screening-line dog and an interdiction dog are not the same animal, and matching the dog to the mission is the first place a placement succeeds or fails.</p>
  <p>Placement is the start of the relationship, not the end of it. Reliability drifts without maintenance — handlers pick up habits, dogs test boundaries, and a team that was sharp at delivery can quietly erode over a year of real work. We offer maintenance training and post-placement support so performance stays where it belongs and the documentation stays current. When your program has to answer to a court, an inspector, or a chief, that continuous record is the difference between a team you can stand behind and one you are hoping about.</p>
  <p>The one-page <a href="/downloads/K9School-Agency-Capability-Brief.pdf">capability brief</a> puts the essentials in front of a decision-maker: what we deliver, how it's documented, and why it holds up. Hand it up your chain of command, then start the conversation and we'll scope your mission profile directly.</p>
</div></section>
"""
hub("agencies.html","a","For Law Enforcement Agencies",
    "Detection K9s your unit can deploy with confidence.",
    "For procurement leads and K9 supervisors who can't afford a team that fails in the field — dogs and handlers proven in deployment and documented to a defensible standard.",
    "Request a Capability Brief","/agencies.html#brief", ag_proof, ag_offer, ag_faq,
    "Detection Dogs & Handler Certification for Agencies | K9School",
    "Finished detection dogs and certified handlers for law enforcement — documented to the LSOC courtroom-defensible standard. Request a capability brief.",
    "Agencies", photos=AGENCIES_PHOTOS, deep=ag_deep)

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
tr_deep = """
<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">What we actually teach</div>
  <h2>We don't train the sit. We train you to read the dog.</h2>
  <p>Most handler courses teach a dog to sit at odor and teach a person to reward it. You leave with a certificate and a dog that alerts — and the first time the work gets hard, or a search goes sideways, or an attorney asks what the dog actually did, you discover how little that certificate prepared you for. We teach something more durable and more difficult: how to see. How to read a dog through the <a href="/method.html">Five Phases of behavior</a>, how to know your individual dog's baseline so you catch the change of behavior the instant it happens, and how to tell the difference between a dog working odor and a dog reading you.</p>
  <p>That skill — reading behavior, then explaining it — is what separates a person who owns a detection dog from a handler who can deploy one. It cannot be handed to you on a lanyard. It is built, rep by rep, on real problems, and it is the core of every course we run. The dog is the easy part. The human end of the leash is where reliability is won or lost, and it is where we spend the work.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The path</div>
  <h2>Foundation, handler, instructor — a real career, not a weekend.</h2>
  <p><b>Foundation scent detection</b> builds the core correctly from the start: imprinting on odor, teaching the dog to hunt and to problem-solve, and establishing the honest search habits that everything else stands on. Get the foundation wrong and you spend years patching cracks; get it right and the dog is easy to advance.</p>
  <p><b>Handler certification</b> is where the dog and the person become a team. You learn to run a systematic search, to read your dog's tells, to keep your own influence out of the work, and to document what you did so it holds up later. You leave able to run a reliable, court-defensible team — because we drill the whole sequence, not just the final response.</p>
  <p><b>Instructor certification</b> is for the handler ready to train others and hold a program to standard. It is the difference between doing the work and being able to teach, evaluate, and defend it. A career in this field is a ladder — foundation to handler to instructor — and we built the training so you can climb it with a standard behind you at every rung.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Reduce your own influence</div>
  <h2>The hardest thing to train is the person holding the leash.</h2>
  <p>Every handler leaks. Where you look, how you plant your feet, a change in your breathing near the spot you think the aid is hidden — dogs read all of it, because you are part of the environment they are searching. This is the <a href="/resources-handler-influence-invisible-leash.html">Invisible Leash</a>, and it is not a character flaw; it is physics and biology, documented in the research. We do not pretend you are immune to it. We train you to move the same way whether you know the answer or not, and then we take the answer away from you with blind and double-blind exercises, so you learn — in the safety of training — exactly how your body talks to your dog. Handlers who have felt that in a controlled setting are the ones who can be trusted in an uncontrolled one.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">What you leave with</div>
  <h2>Outcomes, not attendance.</h2>
  <p>A certificate proves you showed up. We care whether you can do the job. When you finish, you should be able to present a search cleanly, read your dog through every phase, keep your influence out of the work, recognize an honest "no odor here," and write a training record that would survive being read aloud in a hearing. That is a higher bar than a passing score on a demo, and it is the bar the work will actually hold you to. If you want the credential without the competence, there are faster places to get it. If you want to be the handler other units call when it matters, start here.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Who this is for</div>
  <h2>New to detection, or fixing a dog you already run.</h2>
  <p>Our courses serve a wide range — officers assigned to a K9 unit for the first time, pest-control and conservation professionals adding a detection capability, working handlers whose dogs have developed problems, and experienced trainers moving toward instructor-level competence. No formal experience is required for the foundation and handler tracks, though a genuine willingness to be coached on your own habits helps more than any résumé. The one thing every student has in common when they leave is that they stopped managing a dog and started reading one.</p>
  <p>Training takes place on-site in Lincoln, Alabama, with real field components rather than yard-only drills, because a dog that only works a clean training room is a dog you have not actually tested. Bring your own dog to build the specific team you'll deploy, or work a program dog to learn the mechanics first. Either way, expect to be the one who gets corrected: most "dog problems" are handler problems, and the fastest way to a reliable team is to fix the end of the leash that talks back.</p>
</div></section>
"""
hub("training.html","g","Handler &amp; Instructor Training",
    "Ready on day one — not just certified.",
    "Handler certification, instructor certification, and foundation detection training built around field competence and a standard that stands up when it matters.",
    "Apply / Enroll","/training.html#apply", tr_proof, tr_offer, tr_faq,
    "K9 Handler & Instructor Certification Courses | K9School",
    "Handler and instructor certification and foundation scent-detection training — field-first, outcome-driven, and certified to the LSOC standard.",
    "Training", photos=TRAINING_PHOTOS, deep=tr_deep)

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
co_deep = """
<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Where programs break</div>
  <h2>Most program failures were built in at the start.</h2>
  <p>When a detection program gets into trouble — a suppression ruling, a failed audit, a unit that quietly stops trusting its own dogs — the cause is almost never the moment it surfaced. It was set months or years earlier: a dog selected for the wrong work, a foundation rushed, a handler certified before they could read their dog, a training record that documents only successes. By the time the problem shows up in a courtroom or an inspection, it has roots. Fixing it means going back to those roots, honestly, and that is uncomfortable work most people avoid until they cannot.</p>
  <p>David has done this from every seat — as a trainer, as a handler, as a chief of police who had to answer for a program, and as an expert witness who has seen exactly how programs come apart under scrutiny. That vantage is the point. He is not auditing your program against a binder of best practices he read once. He is evaluating it against what actually happens when a defense attorney, an inspector general, or a review board goes looking for the weak seam.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Standing one up</div>
  <h2>Build it right the first time — selection to deployment.</h2>
  <p>If you are creating a detection capability from scratch, the decisions you make early are the ones you will live with longest: what odors and environments you are actually equipping for, what kind of dogs fit that work, how handlers will be selected and developed, how you will test and document reliability, and how the whole thing will hold up to the oversight your organization answers to. We help you make those decisions deliberately instead of discovering them the hard way — a program designed backward from the scrutiny it will face, not forward from a catalog of dogs for sale.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Fixing what you have</div>
  <h2>A standards-based assessment finds the gap before an auditor does.</h2>
  <p>If you already have a program and a nagging sense it would not survive a hard look, an honest assessment is cheaper than the ruling that would otherwise teach you the same lesson. We evaluate the real thing: how dogs are selected and maintained, whether handlers can read and articulate their dogs' behavior, whether testing is genuinely blind, and whether the training records would help you or hurt you if they were read aloud in a hearing. You get a straight account of where you stand and a prioritized path to close the gaps — measured against the same <a href="/certification.html">LSOC courtroom-defensible standard</a> the rest of our work is built on.</p>
  <p>And when a program or a case is already being challenged, David provides expert review and testimony grounded in honest evaluation. The goal is never to manufacture a defense or beat the other side; it is to tell the truth about reliability clearly enough that a court can rely on it. That is the same discipline we teach on <a href="/method.html">The Method</a> — it just happens to also be what wins the argument.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Selection, testing &amp; development</div>
  <h2>The pieces of a program, evaluated by someone who's run all of them.</h2>
  <p>Program consulting is rarely one thing. It might be <b>K9 selection and testing</b> — helping you evaluate candidate dogs against the work they will actually do, so you stop buying on a demo and start buying on a defined standard. It might be <b>handler and instructor development</b> — building the human competence a program lives or dies on. It might be a <b>standards-based audit</b> that produces a straight account of where you stand, or the <b>design of a testing regime</b> that is genuinely blind and genuinely documented. And it might be <b>speaking and seminars</b>, bringing this operator-to-operator approach to your team or event. We scope it to what your program actually needs on a focused assessment call, and we quote it honestly.</p>
  <p>What ties all of it together is the vantage point. This is not consulting from a person who read about detection programs. It is evaluation from a retired chief of police, a working detector-dog trainer since 1999, and an expert witness who has watched programs succeed and fail under the only test that ultimately counts — real scrutiny, in the real world, after the fact.</p>
</div></section>
"""
hub("consulting.html","m","Program Consulting",
    "The operator who fixes detection programs.",
    "For agencies and organizations standing up a new detection program or worried theirs won't pass an audit — program development, evaluation, and selection from someone who's done the work.",
    "Book a Program Assessment","/consulting.html#book", co_proof, co_offer, co_faq,
    "K9 Detection Program Development & Audits | K9School",
    "Detection program development, standards-based audits, K9 selection and testing, and handler/instructor development. Book a program assessment with David Latimer.",
    "Consulting", photos=CONSULTING_PHOTOS, deep=co_deep)

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
dd_deep = """
<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Start with the job, not the dog</div>
  <h2>The right dog is defined by the work — before you ever meet it.</h2>
  <p>People shop for a detection dog the way they shop for a truck: they look at the dog first. That is backward. A dog selected for calm, methodical bed-bug work in occupied apartments is a poor match for high-tempo vehicle interdiction, and a hard-charging interdiction dog will wash out of a hotel room in an afternoon. Before we talk about any specific dog, we define the job precisely — the target odors, the environments, the daily workload and climate, and who will handle it. The clearer that profile, the better the match, and the fewer expensive surprises after delivery.</p>
  <p>This is where a placement earns or loses its value. A dog is a multi-year investment your operation's results ride on. Get the selection right and the work is almost easy; get it wrong and no amount of training fully recovers it. So we would rather spend the time up front, ask the uncomfortable questions about how you actually work, and match you to a dog built for it — even when that means telling you the dog you were excited about is wrong for the job.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Green, started, finished</div>
  <h2>Know what stage you're buying — and what your team can develop.</h2>
  <p>Dogs are sold at different stages, and the right choice depends on your handler's experience and your timeline. A <b>green</b> dog shows aptitude but isn't trained — the lowest price and the longest road, and only a good bet if you have an experienced trainer to develop it. A <b>started</b> dog has foundation odor work underway. A <b>finished</b> dog works the odor problem and can be certified with a handler quickly — the highest cost and the lowest risk, fastest to real deployment. There is no universally right answer, but there is a right answer for you, and it depends on an honest look at your team's ability to bring a dog along. For most businesses and agencies, a finished dog paired with handler certification is the lowest total cost once you account for the time and risk of developing one yourself.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Disciplines</div>
  <h2>One approach, many kinds of odor.</h2>
  <p>The principles that make a dog reliable do not change with the target — a bed-bug dog and an accelerant dog are both trained to discriminate, to commit to source, and to tell the truth about what is and isn't there. What changes is the environment and the stakes. We place and support dogs across <b>bed bug</b> detection for pest control and property management, <b>arson / accelerant</b> detection for fire investigation and insurance work, <b>conservation</b> detection for wildlife and invasive species, and <b>narcotics, explosives, and firearms</b> detection for agencies and security teams. The legacy Kip K9 work spanned much of this range, and it all runs on the same method.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">You're buying a team</div>
  <h2>A dog without a trained handler is half a system.</h2>
  <p>The finest dog we could hand you will underperform with an undertrained handler, so we do not treat handler training as an add-on — it is half the system, and we build it into the placement. Whether you are a pest-control company protecting a reputation on every inspection or an agency putting a dog on the street, what you actually need is a <i>team</i> that can work reliably and, when it matters, explain and defend what it did. That is what we deliver: a dog selected for your real work, a handler trained to read it, and the support to keep the team sharp after the sale.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Insist on proof</div>
  <h2>Watch the dog work. Ask for the records. Walk away if you can't.</h2>
  <p>The best protection a buyer has is simple, and it costs nothing: insist on seeing the dog work in an environment like yours, and ask for the documentation of what was evaluated. A reputable program tests dogs against a defined standard and hands you the record. If a seller resists letting you see the dog work, or cannot produce evaluation records, that reluctance is your answer — walk away. A demo in a parking lot the seller controls tells you very little; a dog worked cold in a realistic problem tells you almost everything.</p>
  <p>We hold ourselves to the same rule we would tell you to demand of anyone. Every dog we place is evaluated to the <a href="/certification.html">LSOC courtroom-defensible standard</a>, and the handler is trained to read the <a href="/method.html">behavior behind the response</a> — not just to trust the sit. For a commercial operator, that means a dog whose finds protect your reputation instead of risking it. For an agency, it means a team whose work survives the hearing. Either way, you are buying evidence you can stand behind, which is the only kind worth owning.</p>
</div></section>
"""
hub("detection-dogs.html","p","Commercial &amp; Operational Detection Dogs",
    "A working dog your reputation can ride on.",
    "For pest control, restoration, conservation, security, and agencies buying a detection dog — placement-ready teams selected and trained for the environment they'll actually work in.",
    "Check Availability","/detection-dogs.html#availability", dd_proof, dd_offer, dd_faq,
    "Detection Dogs for Sale — Bed Bug, Arson & More | K9School",
    "Placement-ready detection dogs for bed bug, arson, conservation, narcotics and explosives work — selected, trained, and paired with handler certification.",
    "Detection Dogs", photos=DETECTION_PHOTOS, deep=dd_deep)

# ============================================================
# PROOF
# ============================================================
proof_body = f"""
<section class="hero"><div class="wrap">{hero_grid(
  '<div class="crumb"><a href="/index.html">Home</a> / Proof</div>'
  '<div class="kick">Proof &amp; Results</div>'
  '<h1>Evidence, not adjectives.</h1>'
  "<p class=\"sub\">The detection world runs on trust earned in deployment. Here's ours — case studies, references, and certification you can verify.</p>",
  HERO_PHOTOS['proof.html'])}</div></section>

<section class="sec"><div class="wrap">
  <div class="eyebrow">Case studies</div>
  <h2>What our teams did in the field.</h2>
  <p class="lead" style="max-width:64ch">Told in David's words, including the parts he cannot prove. Where an explanation is a hypothesis, it is labelled as one.</p>
  {case_study("tatsa-cleared-vehicle", flagged='<p class="muted" style="font-size:.86rem">' + fill('confirm we may state that another team had already worked and cleared the vehicle') + ' ' + fill('year, breed, and how long you and Tatsa worked together — and which dog in this photo is Tatsa, or a photo of her on her own') + '</p>')}
  {case_study("lucy-and-the-baby-doll", flagged='<p class="muted" style="font-size:.86rem">' + fill('a photo of Lucy, and confirmation we may describe the squad firing on a box the dog had cleared') + '</p>')}
  {case_study("boomer-and-contamination", flagged='<p class="muted" style="font-size:.86rem">' + fill('a photo of Boomer, and roughly what year this was') + '</p>')}
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

{video_strip("proof.html")}

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Want references for your specific use case?</h2>
  <p>Tell us the mission and we'll connect you with the most relevant proof.</p>
  <a class="btn" href="/contact.html">Request references</a>
</div></div></section>
"""
page("proof.html","Proof & Results — Case Studies & References | K9School",
     "Detection-dog case studies, agency references, client testimonials, and training footage from Latimer School of Operational K9s.",
     proof_body, active="/proof.html")

# ============================================================
# ABOUT
# ============================================================
about_hero = f'''<div class="crumb"><a href="/index.html">Home</a> / About</div>
  <div class="kick">About</div>
  <h1>Operator. Trainer. Expert witness.</h1>
  <p class="sub">K9School is the working home of {BIZ} — David Latimer's operational detection practice in Lincoln, Alabama, built on a career spent in the field and in the courtroom.</p>'''
about_body = f"""
<section class="hero"><div class="wrap">{hero_grid(about_hero, HERO_PHOTOS['about.html'])}</div></section>

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

<section class="sec tight"><div class="wrap">{figure2(("lsoc-136-me-and-two-search-dogs-2.jpg","In the field with the dogs"), ("lsoc-73-me-and-handler-trng.jpg","Working alongside a handler"))}</div></section>
{video_strip("about.html")}

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">It started with Sport</div>
  <h2>The dog was always talking. The job was to listen.</h2>
  <p>Before there was a method, or a badge, or a witness stand, there was a boy watching his father work a liver-spotted pointer named Sport. No electronics, no harsh corrections — just a voice, a read on the dog, and a quiet respect for what the animal already knew how to do. David's father was practicing positive reinforcement before the phrase was fashionable and building compound behavior before anyone had a term for it, and the boy absorbed the lesson that would organize the rest of his life: <b>the dog is always communicating; the handler's only real job is to understand it.</b> Everything on this site is, in one way or another, a footnote to Sport.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Trained for the field</div>
  <h2>Where the phrase came from.</h2>
  <p>Sport was one dog. What came after him was years of watching quail dogs work huge pieces of ground with almost no input from anybody. As we walked, they would wind scent, raise their heads, sample the air, and head toward the origin. Often they would shift into ground tracking, because quail move on the ground until they are flushed — the dog reading the problem and changing method to suit it. When they found the birds they locked up in a motionless point, nose aimed straight at the covey, and held it until we walked past, flushed the birds, and shot a few.</p>
  <p>They did all of that without repeated commands to seek, without a handler pointing or bending over them, without constant direction. The dogs were focused on the odor of quail, and nothing else. David's father was teaching compound behavior and a trained final response long before those were terms anybody used.</p>
  <p>Two things came out of those years. The first is that David never had to be persuaded that a dog's nose was real. He had watched too many of them work all day, finding birds until they were exhausted. In his words: <i>not once do I recall walking up to a pointed bird dog and not finding quail where the dog pointed.</i> He is quick to add the necessary qualification — <b>false alerts are a fact of life in detection work</b>, and the honest response to that is to train to minimize them rather than to make excuses for them. But having seen what a dog is capable of when it is genuinely working odor, he was never going to accept less than that as normal.</p>
  <p>The second is the phrase itself. It came from watching his father start puppies in the yard. A young dog can look perfect in the yard and come apart the first time it is turned loose on a real hunt. It was not that they could not find birds — most of them could. The question was whether they could apply logic to a hunt, use wind scenting and tracking, solve the odor problem, and then point and hold until the hunter flushed the birds. All of those pieces had to arrive at once. You can control a dog in a backyard and make the performance look pretty. Out in the field, where the dog has to take over, is a different story.</p>
  <p>That is where it comes from: <b>trained for the field, not just the yard.</b></p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Fire taught him to prove it</div>
  <h2>Where "reliability you can defend" stopped being a slogan.</h2>
  <p>David's path into detection didn't run through a kennel — it ran through fire. After the military, where he served first as an HVAC technician and then as a small-arms marksmanship instructor, a friendship with a forensic engineer pulled him into the world of fire and explosion investigation. In <b>1999</b> he trained his first accelerant-detection dog, and the work that followed shaped everything about how he thinks. He worked hundreds of fire scenes and helped put arsonists in prison.</p>
  <p>Arson work is unforgiving in a specific way: the dog's indication is only the beginning. What the dog found has to survive a laboratory, a report, and a defense attorney, months or years later. There is no room for a handler who can only say "the dog alerted." From the start, David had to be able to describe exactly what the dog did, document it honestly, and defend it under cross-examination. That is not a marketing posture he adopted later; it is the environment his career was forged in. Courtroom-defensibility is simply the water he learned to swim in.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">One nose, many disciplines</div>
  <h2>From accelerants to narcotics, explosives, cadaver, tracking — and pests.</h2>
  <p>Odor is odor, and the principles that make a dog honest do not change with the target. From accelerant detection, David moved into narcotics, explosives, cadaver, and tracking work, and around <b>2002</b> into pest-detection dogs — the specialty that would eventually anchor the legacy Kip K9 brand. Each discipline has its own environment and stakes, but each is trained on the same foundation: teach the dog to discriminate, to commit to source, and to tell the truth about what is and isn't there. A trainer who understands behavior rather than memorizing a single odor picture can move across all of it, and that breadth is exactly what lets David build programs and place dogs across such different kinds of work today.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The badge and the bench</div>
  <h2>A career spent accountable for the outcome.</h2>
  <p>David attended the police academy in <b>2003</b> and spent the rest of his career in law enforcement, promoted to <b>Chief of Police in 2007</b> before retiring from full-time service in <b>2015</b>. Along the way he graduated from the <b>FBI National Academy</b> at Quantico — the highlight of his law-enforcement career, and a credential that reflects the level at which he was operating. The chief's chair matters to how he teaches: he did not just handle dogs, he was ultimately answerable for a program — for its liability, its documentation, and its performance when someone came looking for a weakness. He has stood where the procurement lead and the K9 supervisor stand, which is why the work here is built backward from the scrutiny an agency actually faces rather than forward from a demo.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Why he writes and testifies</div>
  <h2>An author on behavior — and an expert witness on reliability.</h2>
  <p>Today David trains, certifies, consults, and testifies, and he has written extensively on detector-dog behavior and reliability — a manuscript distilled from decades of doing the work. He testifies as an expert witness on detector-dog reliability, always on the basis of honest evaluation; the goal is the truth of what a dog can and cannot tell you, never manufacturing a result or beating the other side. Writing and testifying are two expressions of the same conviction: this discipline improves when it is explained plainly and held to honest scrutiny, and it suffers when it hides behind bravado. He would rather teach a handler to describe a search precisely than watch another team rest a case on "the dog alerted."</p>
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
  {figure(("lsoc-100-me-teaching.jpg","Teaching handlers to the standard"))}
  {book_callout()}
</div></section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Let's talk about what you need to deploy.</h2>
  <a class="btn" href="/contact.html">Get in touch</a>
</div></div></section>
"""
person_schema = (f'{{"@type":"Person","@id":"{SITE}/about.html#david","name":"David Latimer",'
  f'"jobTitle":"Founder, Master Detection Dog Trainer & Expert Witness","worksFor":{{"@id":"{SITE}/#localbusiness"}},'
  '"alumniOf":"FBI National Academy","hasOccupation":{"@type":"Occupation","name":"Retired Chief of Police"},'
  f'"url":"{SITE}/about.html","knowsAbout":["detector dog behavior","detection dog training","accelerant detection","narcotics detection","K9 program development","handler certification","detector dog courtroom testimony","handler influence","blind and double-blind testing"]}}')
page("about.html","About David Latimer — Founder & Trainer | K9School",
     "David Latimer and Latimer School of Operational K9s — operational detection dog training built on real field deployment in Lincoln, Alabama.",
     about_body, nodes=[person_schema], active="/about.html")

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
cert_hero = ('<div class="crumb"><a href="/index.html">Home</a> / Certification</div>'
  '<div class="kick">The Standard</div>'
  '<h1>Reliability you can document.</h1>'
  '<p class="sub">Every dog and handler we build is evaluated against the LSOC courtroom-defensible standard — so your records hold up where it counts.</p>')
cert_body = f"""
<section class="hero"><div class="wrap">{hero_grid(cert_hero, HERO_PHOTOS['certification.html'])}</div></section>
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

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">What it actually tests</div>
  <h2>Four things, evaluated the way a court would.</h2>
  <p>A certificate is only as good as what it measures. The LSOC standard is built around the four things that determine whether a team's work will hold up, and it evaluates each of them deliberately rather than trusting a single clean demo.</p>
  <p><b>Reliability under field-representative conditions.</b> A dog that only performs in a familiar training room has not been tested; it has been rehearsed. The standard puts the team in conditions that resemble the work — the distractions, the environments, the ambiguity of a real search — because that is where reliability either exists or doesn't.</p>
  <p><b>Independent work, proven by blind and double-blind testing.</b> The single most important question a court will ask is whether the dog was responding to odor or to the handler. The only honest way to answer it is to take the answer away from the handler. Blind and double-blind exercises are therefore not optional flourishes in this standard; they are the core of it, because they are the only thing that separates a reliable dog from a well-cued one.</p>
  <p><b>Handler communication and articulation.</b> We evaluate the human end of the leash as seriously as the dog. Can the handler run a clean search, keep their own influence out of it, read the dog through the <a href="/method.html">Five Phases</a>, and — critically — describe what the dog did in language that survives cross-examination? A team whose handler cannot explain the behavior is not a certified team; it is a liability with a lanyard.</p>
  <p><b>Documented, repeatable evaluation — including failure.</b> The standard requires honest records, and honest records include misses. An evaluation history with no failures in it is not evidence of a perfect team; it is evidence of a dishonest process, and a court knows the difference.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">A benchmark, not a shield</div>
  <h2>Certification is a floor you can defend — not a guarantee.</h2>
  <p>It matters what this standard is <i>not</i>. It is not a promise that a dog will never be wrong, and it is not a magic certificate that ends an argument in court. The Supreme Court itself, in <i>Florida v. Harris</i>, rejected the idea that a certificate is an automatic shield: a defendant can still challenge a team's reliability with evidence about training, records, testing, and handler influence. A standard that pretended otherwise would be selling something. Ours does the opposite — it is designed to produce exactly the documentation and demonstrable reliability that answer those challenges, because it was built by someone who has sat in the witness chair and watched thin programs come apart. The point of certifying to it is not to claim perfection. It is to be able to prove, honestly, that a team's work deserves to be trusted. <a href="/resources-florida-v-harris-k9-handlers.html">Read what Harris means for handlers.</a></p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The record is the certificate</div>
  <h2>Long after the search, the paperwork is what remains.</h2>
  <p>When a deployment is questioned months or years later, no one re-runs the search. What gets examined is the record — the training logs, the testing history, the maintenance documentation. Certifying to a real standard means building and keeping that record honestly, so that it helps you when it is read aloud instead of handing the other side their best exhibit. That is what "courtroom-defensible" means in practice, and it is the through-line from how we <a href="/method.html">train</a> to how we evaluate to how a team performs when it finally matters.</p>
</div></section>

<section class="sec tight"><div class="wrap"><div class="eyebrow center">Teams certified to the standard</div>{figure2(CERT_PHOTOS[0], CERT_PHOTOS[1])}</div></section>
<section class="sec wash"><div class="wrap"><div class="center"><div class="eyebrow">Questions</div><h2>About the standard</h2></div>
{figure(CERT_PHOTOS[2])}
<div style="max-width:820px;margin:28px auto 0">{faq_html(cert_faq)}</div></div></section>
"""
page("certification.html","The LSOC Courtroom-Defensible Standard | K9School",
     "The LSOC courtroom-defensible standard — how Latimer School of Operational K9s documents detection-team reliability for defensible, court-ready records.",
     cert_body, nodes=[faq_schema(cert_faq)], active="/certification.html")

# ============================================================
# CONTACT
# ============================================================
contact_hero = ('<div class="crumb"><a href="/index.html">Home</a> / Contact</div>'
  '<div class="kick">Contact</div>'
  '<h1>Tell us what you need to deploy.</h1>'
  '<p class="sub">Pick your path below. Agencies and consulting inquiries reach David directly; training and placement inquiries route to the right next step.</p>')
contact_body = f"""
<section class="hero"><div class="wrap">{hero_grid(contact_hero, HERO_PHOTOS['contact.html'])}</div></section>
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
<section class="sec tight wash"><div class="wrap"><div class="eyebrow center">The people and dogs behind the work</div>{figure2(CONTACT_PHOTOS[0], CONTACT_PHOTOS[1])}</div></section>
"""
page("contact.html","Contact — Request a Capability Brief | K9School",
     "Contact Latimer School of Operational K9s. Request a capability brief, apply for training, book a program assessment, or check detection-dog availability.",
     contact_body, active="/contact.html")

# ============================================================
# RESOURCES (SEO pillar content + lead magnets)
# ============================================================
def article_schema(title, desc, slug):
    return ('{"@type":"Article",'
      f'"headline":{_json(title)},"description":{_json(desc)},'
      f'"author":{{"@id":"{SITE}/about.html#david"}},'
      f'"publisher":{{"@id":"{SITE}/#localbusiness"}},'
      f'"image":{{"@id":"{SITE}/#logo"}},'
      f'"mainEntityOfPage":{{"@id":"{SITE}/{slug}#webpage"}}}}')

def article(slug, kicker, title, desc, intro, sections, cta_head, cta_sub, cta_label, cta_href, faq=None):
    extra = ARTICLE_PHOTOS.get(slug, [])
    hero_item = extra[0] if extra else None
    inline = extra[1:]
    n = len(sections)
    seam = {}
    for k, ph in enumerate(inline):
        idx = min(n - 1, round((k + 1) * n / (len(inline) + 1)) - 1)
        seam.setdefault(idx, []).append(ph)
    body_sections = ""
    for i, (h, paras) in enumerate(sections):
        body_sections += f"<h2>{h}</h2>"
        for para in paras:
            if para.startswith("UL:"):
                items = para[3:].split("|")
                body_sections += '<ul class="tick">' + "".join(f"<li>{i2}</li>" for i2 in items) + "</ul>"
            else:
                body_sections += f"<p>{para}</p>"
        for ph in seam.get(i, []):
            body_sections += figure(ph)
    faq_block = ""
    schema_extra = ""
    if faq:
        faq_block = f'<h2>Frequently asked</h2><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)}</div>'
        schema_extra = "," + faq_schema(faq)
    hero_copy = (f'<div class="crumb"><a href="/index.html">Home</a> / <a href="/resources.html">Resources</a> / Guide</div>'
                 f'<div class="kick">{kicker}</div><h1>{title}</h1><p class="sub">{intro}</p>')
    body = f"""
<section class="hero"><div class="wrap">
  {hero_grid(hero_copy, hero_item)}
</div></section>
<section class="sec"><div class="wrap" style="max-width:780px">
  {body_sections}
  {faq_block}
</div></section>
{video_strip(slug)}
<section class="sec tight"><div class="wrap" style="max-width:900px"><div class="ctastrip">
  <h2>{cta_head}</h2><p>{cta_sub}</p>
  <a class="btn" href="{cta_href}">{cta_label}</a>
</div></div></section>
"""
    nodes = [article_schema(title, desc, slug)]
    if faq: nodes.append(faq_schema(faq))
    page(slug, f"{title} | K9School", desc, body, nodes=nodes, active="/resources.html")

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
   ("Watch the dog work cold",
    ["A demo the seller controls tells you very little. Of course the dog finds the aid the trainer hid in a room the dog knows — that is a rehearsal, not a test. Insist on watching the dog work a problem it hasn't seen, in an environment like the one you'll deploy it in, with distractions present. Watch how it searches, not just whether it sits: does it work systematically, commit to source, and stay in the game when the odor is faint? A dog that works honestly in an unfamiliar problem is showing you what you're actually buying."]),
   ("The honest-dog test",
    ["Here is a test most buyers never think to run, and it separates a reliable dog from an impressive one: ask to see the dog work a blank area — a search with no target odor at all. A well-trained dog will work it and clear it honestly. A dog that has been taught, however unintentionally, that every search must end in a find will do something revealing instead: it will manufacture an answer, because it believes producing an alert is the job. You want the dog that can say &ldquo;there's nothing here.&rdquo; A dog whose &ldquo;no&rdquo; is honest is a dog whose &ldquo;yes&rdquo; you can trust — and defend."]),
   ("Price versus total cost",
    ["The cheapest dog is almost never the lowest total cost. A green dog with a low sticker price is a months-long project that ties up a handler and carries real risk of washing out; a finished dog costs more up front and deploys fast with far less risk. Think in terms of time-to-deployment and risk, not just purchase price, and factor in handler training and ongoing maintenance. A dog is a multi-year investment your results ride on — buying on sticker price alone is how operations end up paying twice."]),
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
  "What it takes to become a competent detection-dog handler — the skills, the certification path, and how to choose training that makes you deployable.",
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
   ("The skill nobody puts on the flyer: reading behavior",
    ["Most courses will teach you to reward a sit. Few will teach you the skill that actually makes a handler — reading the dog through the whole search, so you can see the change of behavior the instant it happens and know the difference between a dog working odor and a dog working you. That skill can't be handed to you on a lanyard. It's built rep by rep, on real problems, with a coach who can see what you're missing. When you evaluate a course, ask how much time you'll spend learning to observe, not just to handle. See <a href=\"/method.html\">the method</a> we teach for what that looks like."]),
   ("The hardest thing to train is you",
    ["New handlers are surprised to learn that the biggest variable in the team is not the dog — it's them. Where you look, how you move, the tension in the leash, your own anticipation when you think you know where the aid is: the dog reads all of it. This is the <a href=\"/resources-handler-influence-invisible-leash.html\">Invisible Leash</a>, and learning to manage it is a core part of becoming deployable. Good training will make you uncomfortable on purpose, taking the answer away from you with blind exercises so you learn exactly how your body talks to your dog. Be wary of any course where the handler is never the one getting corrected."]),
   ("What competence looks like when you finish",
    ["You should leave able to run a reliable team: present a search cleanly, recognize and reward correctly, troubleshoot common problems, keep your own influence out of the work, recognize an honest &ldquo;no odor here,&rdquo; and document your work so it holds up in a hearing. If a course can't tell you what you'll be able to *do* at the end — only what you'll have attended — keep looking."]),
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
   ("Documentation is the program",
    ["Agencies think of records as paperwork that supports the program. Reverse that. In any hearing or audit that questions a deployment, the record <i>is</i> the program — it is the only thing that survives to be examined months or years later. A program that trains well but documents thinly is a program that will lose arguments it should win. Build the recordkeeping in from day one: training logs, maintenance history, and testing results that honestly include failures. A log with no misses in it does not read as a perfect unit; it reads as a unit that isn't recording honestly, and a competent attorney knows the difference."]),
   ("Blind testing, or it didn't happen",
    ["The fastest way to tell a serious program from a going-through-the-motions one is to ask how it tests. If handlers always know where the aids are hidden, the program cannot answer the single most important challenge it will face — that the dogs are reading their handlers rather than odor. Blind and double-blind testing isn't an advanced nicety; it's the evidence that your teams work independently. Bake it into the training schedule and the certification process, and keep the records, because those records are exactly what turn &ldquo;trust us&rdquo; into something a court can weigh."]),
   ("The view from the chief's chair",
    ["A detection program is a liability decision before it is a capability. Someone in your organization will ultimately answer for it — for its deployments, its documentation, and its performance when a case or an audit puts it under a microscope. Building the program backward from that scrutiny, rather than forward from a demo, is what keeps it from becoming the thing that comes apart at the worst possible moment. That perspective — having sat in the chair that answers for the program — is what an experienced outside evaluation brings to the table."]),
   ("Common failure modes to avoid",
    ["UL:Buying dogs before defining the mission.|Training the dog but neglecting the handler.|No maintenance schedule.|Thin or missing documentation.|Testing that is never truly blind.|No recognized certification standard behind the program."]),
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
   ("The mistakes that get cases thrown out",
    ["The narcotics cases that fall apart tend to fail for the same handful of reasons, and every one of them is preventable. A training file that documents only successes, which reads as dishonest the moment it's examined. Testing that was never blind, leaving no answer to the claim that the dog was cueing off the handler. A handler who overreaches on the stand — testifying that the dog &ldquo;knew&rdquo; there were drugs rather than describing the behavior actually observed. And no fluency with the case law that governs the work, so the handler is caught flat by questions any prepared attorney will ask. The <a href=\"/resources-florida-v-harris-k9-handlers.html\">Florida v. Harris</a> guide covers the legal backdrop; the fix in every case is the same — honest records, genuine blind testing, and testimony bounded to what was seen."]),
   ("Read the dog, don't just call the alert",
    ["A narcotics deployment is stronger when the handler can describe the search, not just announce the outcome. &ldquo;The dog alerted&rdquo; is thin; &ldquo;the dog's respiration changed as it passed the seam of the door, it snapped its head back, bracketed, and gave its trained response at the base of the door&rdquo; is evidence. Training handlers to read the <a href=\"/method.html\">phases of behavior</a> and articulate them is not academic polish — it is what makes a narcotics team's testimony hold up when it matters."]),
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
  "Bed Bug Detection Dogs for Pest Control Businesses",
  "Why a trained bed bug detection dog can transform a pest-control operation — accuracy, speed, new revenue — and how to choose one that protects your reputation.",
  "For a pest-control business, a bed bug detection dog is a revenue and reputation decision. A reliable dog finds infestations faster and earlier than visual inspection, opens a premium service line, and differentiates you from competitors. An unreliable one does the opposite. Here's how to get it right.",
  [
   ("The business case",
    ["A trained detection dog can inspect a room in minutes with high accuracy, letting you offer canine inspections as a premium service, verify treatments, and win commercial accounts (hotels, property managers) that demand documented thoroughness. The dog often pays for itself through new work and efficiency — but only if it performs consistently."]),
   ("Accuracy depends on training and handling",
    ["A detection dog's real-world accuracy is a product of the dog, the handler, and ongoing maintenance. Beware of any pitch that treats the dog as a plug-and-play gadget. You're buying a team and a routine, not just an animal."]),
   ("What to look for",
    ["UL:A dog selected for calm, methodical indoor work and strong scent drive.|Handler training so your staff can present searches and read the dog correctly.|A clear response you can document for clients.|Ongoing maintenance training to keep accuracy high.|Support from the trainer after placement."]),
   ("The reputation math",
    ["For a pest-control business, the dog's reliability is your brand on the line at every inspection. Play out both failure modes. A dog that alerts where there's nothing costs a customer an unnecessary treatment and costs you their trust when the follow-up turns up empty. A dog that misses an infestation costs you a callback, a warranty headache, and a review that follows you around. Reliability isn't an abstract virtue here — it's the difference between a canine service that wins premium commercial accounts and one that quietly bleeds them. That's why the honest dog matters as much in a hotel as it does in a courtroom."]),
   ("The honest dog protects you",
    ["The most valuable trait in a business detection dog is the same one that matters in law enforcement: honesty. A dog that has been taught, even accidentally, that every inspection should end in a find will eventually manufacture one — and a false positive in a client's occupied unit is exactly the kind of mistake that damages a reputation. You want a dog that can work a clean room and clear it confidently. Ask to see it work a space with no bugs; a dog whose &ldquo;all clear&rdquo; is trustworthy is a dog whose &ldquo;found it&rdquo; you can stand behind in front of a paying client."]),
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
   ("Independent work is the whole game",
    ["In a discipline where the cost of error is catastrophic, the last thing you can afford is a dog that's reading its handler instead of odor. That makes blind and double-blind testing more essential here, not less. A team that only trains where the handler knows the hide has no way to prove — to itself or to anyone else — that the dog works the explosive and not the human. Build the testing in, keep the records, and you have a team whose reliability is demonstrated rather than hoped for. That is the only kind of reliability worth deploying against this threat."]),
   ("Why perfection is the wrong promise — even here",
    ["It is tempting, in the highest-consequence discipline, to want a guarantee. Be suspicious of anyone who offers one. No honest trainer will tell you a dog is &ldquo;100% accurate&rdquo; or will &ldquo;never false alert&rdquo; — dogs are living detectors, not instruments, and a program that hides that fact is a program you cannot trust when it counts. What you should demand instead is higher than perfection because it is real: a team selected and trained to the strictest standard, tested honestly under blind conditions, maintained on a schedule, and documented so thoroughly that its reliability can be demonstrated rather than asserted. In explosives work, honesty about a dog's real capabilities isn't a weakness — it's the entire foundation of trusting the dog with the job."]),
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
  "Latimer Five-Phase Model of Detector Dog Behavior",
  "A working model of the behavioral sequence a detector-dog search moves through — and why naming it changes how handlers observe, document, and testify.",
  "The sit gets all the attention. But by the time a dog performs its trained final response, the important work is already done. Understanding the search as a sequence of phases lets a handler see the investigation as it happens — and describe it accurately later.",
  [
   ("Where this model comes from, and what it is not",
    ["This is a working model, and it is worth saying so plainly. Research on detection dogs supports the pieces it is built from: that behavior occurring before the trained response carries usable information, and that dogs measurably change how they move as they localise a source. What no published study has yet done is validate that every search divides into these exact five phases, or that two observers watching the same dog would draw the boundaries in the same place.",
     "So this is the Latimer Five-Phase Model — a framework built in the field over twenty-five years, consistent with the research but not a finding of it. That distinction matters more here than in most training material. A handler who testifies that the dog moved through &ldquo;the five scientifically established phases of canine detection&rdquo; has handed the other side an easy afternoon. A handler who says &ldquo;I use a five-phase framework to describe what I observed, and here is what the dog actually did&rdquo; is describing evidence, and is much harder to move."]),
   ("Why phases instead of just “the alert”",
    ["A detector dog doesn't recognize odor at the instant it sits. Recognition happens earlier, and the dog's behavior changes as it works the problem. Breaking the search into phases gives handlers a shared, precise language for what the dog is doing — instead of collapsing an entire investigation into one word: &ldquo;alerted.&rdquo;"]),
   ("The five phases",
    ["UL:<b>Phase 1 — Responds to the command to search.</b> The dog begins working on cue.|<b>Phase 2 — Systematic search, no target odor recognized.</b> The dog covers the area methodically.|<b>Phase 3 — Detection.</b> Target odor becomes meaningful; recognition begins.|<b>Phase 4 — Change of behavior.</b> The observable tell: respiration, head position, body tension, bracketing toward source.|<b>Phase 5 — Trained final response.</b> The dog reports its conclusion. The sit is phase five — not the whole story."]),
   ("Phases 3 and 4 are the investigation",
    ["This is where the dog actually does its work, and it's exactly what most testimony leaves out. A handler who can say what happened in phases 3 and 4 — &ldquo;the dog stopped forward movement, raised its head, turned into the wind, and bracketed the passenger door&rdquo; — is describing evidence. A handler who can only say &ldquo;my dog alerted&rdquo; has skipped the investigation."]),
   ("A search, phase by phase",
    ["Watch a real search and the sequence stops being abstract. You send the dog — phase one, a clean start line, everything after it on the record. The dog begins working the room methodically, checking seams and corners, using the air — phase two, the honest labor of eliminating negative space, which looks like nothing is happening but is the dog doing exactly its job.",
     "Then it crosses a scent cone and something registers. The first tell is almost always the breath: the open, cooling pant closes into short, rapid sniffs as the dog samples. That is phase three — detection — and it is subtle and fast and the reason most handlers miss the real moment of the find. Now the dog commits: the head drops to a seam or lifts into a current, the tail changes, the footwork tightens into bracketing as the dog works the edges of the odor and drives toward the strongest concentration. That is phase four, the change of behavior, and phases three and four together are where the dog actually solves the problem. The sit that follows is phase five — the dog reporting a conclusion it reached seconds earlier."]),
   ("Reading the change of behavior",
    ["Phase four is the one worth studying, because it is where the evidence lives and because no two dogs perform it the same way. One dog's change of behavior is a dramatic head-snap; another's is a barely perceptible drop in the tail and a shift in cadence. That is why there is no universal checklist — there is only your dog and the baseline you have learned by watching it work clean searches, so you know what normal looks like the instant it stops being normal.",
     "UL:<b>Respiration</b> — the open pant closing into deliberate sampling is often the first and clearest tell.|<b>Head position</b> — where the dog is placing the problem: up into a current, down at a seam, snapping back to a source it overran.|<b>Tail carriage</b> — a change in height, tension, or speed at commitment; for your dog it may be the opposite of the textbook, which is why baseline is everything.|<b>Footwork</b> — bracketing back and forth across the plume, overshooting and correcting, then the hard drive to source."]),
   ("Training to the phases",
    ["Once you see the search as a sequence, you stop drilling the sit and start coaching the whole thing. You reward the investigation — the searching and bracketing and honest problem-solving — instead of getting so fixated on the final response that the dog learns to rush to it. And you build in the honest &ldquo;no odor here,&rdquo; because a dog that believes every search must end in a find will eventually manufacture one. A dog that can clear a blank area confidently is a dog whose alert means something."]),
   ("The phases on the witness stand",
    ["This is where naming the phases pays off in the only room that ultimately counts. On the stand, the strongest thing a handler can do is describe what the dog did and stop there — keep observation and interpretation in separate sentences. &ldquo;The dog's respiration changed, it snapped back to the seam of the trunk, bracketed twice, and sat&rdquo; is an observation a handler can defend. &ldquo;The dog knew there were drugs in the car&rdquo; is an interpretation a good attorney will take apart, because the dog knows odor, not law. A handler who can narrate the phases testifies to behavior — precise, bounded, honest — and that testimony holds up precisely because it does not overreach."]),
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
   ("Totality of the circumstances, in plain terms",
    ["Strip away the legal language and Harris says something a working handler already knows: reliability is judged by looking at everything, not by ticking a single box. A court weighs the whole picture — how the team was trained, whether it was tested honestly, how it performs, and how credibly the handler can account for what the dog did — against whatever the defense can raise to undercut it. Certification is part of that picture and it helps, but it is one factor among several, not a trump card. The practical effect is that the quality and honesty of your program, not the existence of a certificate, is what carries the day.",
     "That cuts both ways, and this is the part handlers miss. Because the standard is flexible, a strong, well-documented team is harder to attack — the totality is on your side. But for a weak team the same flexibility is a door: a thin file, pattern-trained testing, or a handler who overreaches on the stand all become part of the totality too, and they invite exactly the challenge Harris permits."]),
   ("Where teams get into trouble",
    ["The cases that go badly tend to share the same weaknesses, and every one of them is preventable. Training records that show only successes, so the log looks polished but reads as dishonest to anyone who knows dogs. Testing that was never truly blind, so there is no way to answer the claim that the dog was reading the handler. And testimony that overreaches — a handler asserting the dog &ldquo;knew&rdquo; contraband was present instead of describing the behavior they actually observed. Each of these is an unforced error, and each is fixed not by a better certificate but by better habits: honest records, genuine blind and double-blind work, and the discipline to testify to behavior rather than conclusions."]),
   ("What it means if you're buying a team",
    ["For an agency, Harris is really a procurement question in disguise. The dog you buy and the handler you certify will, someday, be the thing your case rests on — and the totality that protects you is built long before the traffic stop, in how the team was trained, tested, and documented. That is why it is worth insisting on teams built for scrutiny from the start, and on a standard that produces the records a court will actually weigh. See how we train for it on <a href=\"/method.html\">The Method</a>, how we document it against the <a href=\"/certification.html\">LSOC courtroom-defensible standard</a>, and how we support agencies on <a href=\"/agencies.html\">the agencies page</a>."]),
   ("The practical takeaway",
    ["Harris rewards teams that can demonstrate reliability and punishes teams that can only claim it. That's the same standard good training aims for anyway: build a dog whose work you can document and defend. If your program is honest, thorough, and well-recorded, Harris is on your side. If it isn't, no certificate will save it — and that is exactly as it should be."]),
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
  "The Invisible Leash: Handler Influence",
  "How handlers unintentionally influence detector dogs — the Clever Hans lesson, the research, and how honest teams train and test to reduce it.",
  "The most powerful force acting on a detector dog often isn't the odor. It's the person holding the leash. Handler influence isn't misconduct — it's usually unconscious — but if you don't understand it, you can't build a dog a court will trust.",
  [
   ("The Clever Hans lesson",
    ["A century ago, a horse called Clever Hans appeared to do arithmetic — until researchers showed he was reading tiny, unconscious cues from the people around him. Detector dogs are at least as sensitive. When a handler expects an alert, the dog can find one, whether or not odor is present."]),
   ("What the research shows",
    ["The clearest demonstration is Lit, Schweitzer and Oberbauer (2011), published in <i>Animal Cognition</i>. Eighteen certified law-enforcement narcotics and explosives teams searched rooms that contained no target odor at all. Handlers were told scent might be present, and in some conditions that paper markers showed where. Across 164 searches the teams produced 225 incorrect alerts, and those alerts clustered at the locations the handlers believed held odor. The handlers' beliefs moved the results more than anything the dogs were reacting to.",
     "Be precise about what that proves, because overstating it is its own trap. It does not mean handlers cue dogs into false alerts every time, and later work has found the size of the effect depends heavily on how strongly the handler believes and how the test is run. Some of the effect is also the handler reading ambiguity as an alert because they expected one — influence running dog-to-handler rather than handler-to-dog. Both directions are the same problem for a court: the record shows an alert that odor did not cause. This isn't an attack on handlers. It's a description of how sensitive these teams are, and why the fix is structural rather than a matter of trying harder."]),
   ("Influence does not only cause false alerts. It causes misses.",
    ["Almost everyone discusses handler influence in one direction: the handler expects odor, the dog reads the expectation, and an alert appears where there is nothing. That is the failure the research documents and the one handlers are trained to avoid. It is only half the problem.",
     "A dog can also be influenced into missing. If a dog has become dependent on its handler — used to a particular cue, a pause, a change of posture before it commits — then a handler who does not produce that cue can leave the dog holding information it never reports. The dog finds the odor and gives you nothing, because the thing it was really waiting on never arrived.",
     "This matters more than it sounds, because of the asymmetry in how the two errors get caught. A false alert is visible: the search happens, nothing is found, everyone in the parking lot knows. A miss is invisible. The vehicle is cleared and driven away and nobody ever learns what was behind the seat. Programs audit the error they can see and stay blind to the one they cannot, which means the miss rate of a handler-dependent team can stay unmeasured for years.",
     'David has written up a deployment that turned on exactly this — a vehicle another team had already worked, and what Tatsa did with it. <a href="/proof.html#tatsa-cleared-vehicle">Read the case study</a>.']),
   ("Four channels of influence",
    ["UL:<b>Physical</b> — leash tension, body position, slowing at a spot.|<b>Visual</b> — a glance, a lean, a change in posture.|<b>Verbal</b> — tone and timing of encouragement.|<b>Emotional</b> — the handler's own anticipation traveling down the leash."]),
   ("Why the dog isn't cheating",
    ["It's worth being precise about what is happening, because the instinct is to blame the dog or the handler, and both are wrong. The dog is doing exactly what it evolved and was trained to do: gather every scrap of available information and act on it. The handler is part of the dog's environment. If the handler's body, voice, and attention are quietly broadcasting where the answer &ldquo;should&rdquo; be, the dog is being a good detective when it factors that in. The failure isn't the dog reading you — it's a training and testing process that let your knowledge into the search in the first place."]),
   ("Two things David has watched happen",
    ["The clearest way to understand handler dependence is to watch it from the outside, which David has done for most of his career. Both of these are his own observations, and neither is an accusation. Nobody in either story was being deceptive. They were handling the way they had been taught to handle, it appeared to work, and so nobody questioned it.",
     "The first was a demonstration. A man had smashed a single termite into a soda-bottle lid and set it in a line with other lids. His dog picked that lid out every time, no matter how often he moved it in the line-up. Most of the people watching were impressed. What David noticed was that the dog looked back at the handler before every choice — and that the handler always knew which lid was the right one. Nobody in the crowd seemed to register that second fact. <i>Clever Hans would have been proud of both of them.</i>",
     "The second was a dog working a fire scene. The handler brought it out of the car and it locked immediately onto his face, waiting for instruction. When the search started he bent at the waist and pointed at the area he wanted sniffed, and he stayed bent over the whole time, pointing at the floor, moving ahead of the dog with the leash held tight and his other hand indicating the next spot. The dog would saunter over slowly, eyes mostly on the handler, mouth open and not really sniffing until it reached the exact place indicated. Often it did not close its mouth and sniff even then. It stared at the handler, waiting for a signal, and sat slowly and tentatively, still staring. The handler would say <i>show me</i> several times and the dog would start bobbing its head up and down. All that head bobbing told you very little about where the odor actually was.",
     "Both dogs looked like they were working. Neither was doing detection in any sense that would survive a hard question. This is not a rare way to handle a dog, and in David's judgement it is a large part of why accelerant dogs came close to being discarded as a tool for fire investigators some years ago."]),
   ("What influence looks like in the real world",
    ["Handler influence is rarely dramatic. It's the half-second of hesitation as you approach the vehicle you searched last week. It's planting your feet a beat longer at the trunk where the aid &ldquo;usually&rdquo; is. It's the small exhale of relief when the dog reaches the right car, or the extra bit of lead you unconsciously give near a spot you suspect. None of it feels like communication to the handler. All of it is audible to the dog. That is why good handlers are trained to present every search the same way — the same pace, the same body, the same neutrality — whether they know the answer or not."]),
   ("How honest teams respond",
    ["You don't eliminate influence by going passive — you manage it and audit for it. Blind training (the handler doesn't know the hide locations) and double-blind testing (no one present does) reveal whether the dog is working odor or reading the handler. &ldquo;Let the dog stop you. You don't stop the dog.&rdquo;"]),
   ("Why this is a courtroom issue, not just a training one",
    ["Handler influence is not an academic curiosity — it is one of the first things a competent defense attorney will raise, precisely because the research is public and the logic is easy for a jury to follow. If your program cannot show that its dogs perform under conditions where the handler did not know the answer, then every alert is open to the argument that the dog was reading the handler. Blind and double-blind records are the answer to that argument. A team that has lived inside that kind of testing can look a court in the eye and say the dog works the odor; a team that has only ever trained where the handler knew the hide is hoping, and hope does not survive cross-examination. This is why reducing and auditing influence is not a nicety in our program — it is the foundation of a reliability you can defend."]),
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
res_hero = ('<div class="crumb"><a href="/index.html">Home</a> / Resources</div>'
  '<div class="kick">Resources</div>'
  '<h1>Field-tested guidance, free to read.</h1>'
  '<p class="sub">Straight, practical guides on selecting dogs, becoming a handler, and building programs — written from operational experience, not marketing.</p>')
res_body = f"""
<section class="hero"><div class="wrap">{hero_grid(res_hero, HERO_PHOTOS['resources.html'])}</div></section>
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
<section class="sec tight wash"><div class="wrap"><div class="eyebrow center">Guidance grounded in real work</div>{figure2(RESOURCES_PHOTOS[0], RESOURCES_PHOTOS[1])}</div></section>
<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Have a question these didn't answer?</h2><p>Ask an operator directly.</p>
  <a class="btn" href="/contact.html">Get in touch</a>
</div></div></section>
"""
page("resources.html", "K9 Detection Resources & Guides | K9School",
     "Free, field-tested guides from Latimer School of Operational K9s: choosing a detection dog, becoming a handler, and building a K9 detection program.",
     res_body, active="/resources.html")

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
method_hero = ('<div class="crumb"><a href="/index.html">Home</a> / The Method</div>'
  '<div class="kick">The LSOC Approach</div>'
  '<h1>Behavior Is <span class="amb">Evidence.</span></h1>'
  '<p class="sub">Most of the profession trains the sit, rewards the sit, and testifies about the sit. We train something more important: the search that happens before it — because that is where the dog does its real work.</p>')
method_body = f"""
<section class="hero"><div class="wrap">{hero_grid(method_hero, HERO_PHOTOS['method.html'])}</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="quote" style="font-size:1.35rem">"The sit was not the discovery. It was the communication."</div>
  <p class="lead" style="margin-top:16px">A detector dog does not suddenly recognize target odor at the moment it sits. Recognition happened earlier. The dog met odor, and its behavior began to change — respiration, head position, body tension, movement. The trained final response is the <i>end</i> of a conversation that started the moment odor became meaningful. Understanding that conversation is the difference between simply handling a detector dog and learning to read one.</p>
  <p>This is the idea the whole LSOC method is built on: <b>the dog has been talking since the first breath of the search.</b> The handler's job is to learn its language.</p>
  <p>Watch a good team work and you will see it. The dog casts across a room, working the low seams where air collects. It passes a doorway, then checks — a half-step of hesitation, a lift of the head into the current coming under the door. The respiration shifts from an open pant to short, closed sniffs. The tail slows and stiffens. The dog turns back into the odor it just crossed, drives to the base of the door, and only then sits. To an untrained eye, the sit was the moment the dog "found it." To a handler who reads behavior, the find happened four seconds earlier, at the doorway, and everything after was the dog closing the distance to a source it had already committed to. The sit was the sentence at the end of the paragraph.</p>
  <p>Most of the profession never learns to read the paragraph. It trains the sit, rewards the sit, records "alert," and testifies to the alert. That works right up until it doesn't — until a defense attorney asks the handler to describe what the dog <i>did</i>, not what it was trained to do, and the handler has nothing to say. The honest answer to "how did you know the dog was in odor?" cannot be "because it sat." It has to be a description of behavior: what changed, when, and how the handler knew the difference between interest and commitment. That description is the whole ballgame, and it is a skill that has to be built deliberately, on purpose, from the first day of training.</p>
  <p>What follows is how we build it. None of it is proprietary magic. It is a way of seeing, a vocabulary for what you see, and a discipline for proving it later. Read it as an operator, because that is who it was written for.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The system</div>
  <h2>The Latimer Detector Dog System</h2>
  <p class="lead">The method has a name because it makes specific, checkable claims. We call the approach <b>Behavior-First Detection</b>: the dog's observable behavior — not the handler's expectation, not the reward history, not the certificate — is the evidence that detection occurred. {fill('confirm the exact protected wording and whether a trademark applies')}</p>
  <p>Everything else follows from that one commitment. If behavior is the evidence, then the handler has to be able to read it, which is why the <a href="/resources-five-phases-detector-dog-behavior.html">Five-Phase Model</a> is taught before anything else. If behavior is the evidence, then the dog has to produce that behavior on its own, which is why independent source commitment matters more to us than a tidy sit. And if behavior is the evidence, then the training has to be run so that the handler's knowledge cannot contaminate it, which is why blind and double-blind work is a standing practice here rather than an annual test.</p>
  <p>The division of labour we teach is narrower than &ldquo;the dog should work independently,&rdquo; and it is the sentence worth remembering: <b>the handler controls the search assignment; odor controls the detection decision.</b> A dog that will not take direction is not an operational dog. A dog whose final response is directed by anything other than odor is not a reliable one. Both halves have to be true at once.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Odor science</div>
  <h2>The dog is smelling vapor, not objects.</h2>
  <p>A detector dog never smells &ldquo;the narcotics&rdquo; or &ldquo;the explosive.&rdquo; It smells volatile compounds coming off a source and moving through air that is doing whatever the building, the weather, and the traffic tell it to do. That sounds academic until it changes a search: it is why source can be six feet from where the odor is strongest, why an inaccessible source produces a dog that will not settle, why residual odor exists at all, and why a handler who does not understand air movement will misread an honest dog.</p>
  <p>Treating odor as a physical thing with physics — rather than a magic power the dog possesses — is what makes the rest of the method teachable. It is also what makes a handler's testimony credible: a witness who can explain why the dog worked a seam thirty inches to the left of the source is a witness who understands the work. {fill('confirm we may name Dr. Larry Myers (Auburn) and describe the collaboration')}</p>
</div></section>

<section class="sec wash"><div class="wrap">
  <div class="center"><div class="eyebrow">Framework</div><h2>The Latimer Five-Phase Model</h2>
  <p class="lead" style="max-width:60ch;margin:12px auto 0">A working model for reading a search, built in the field over twenty-five years. Naming the phases lets a handler observe, document, and testify precisely.</p></div>
  <div class="grid g3" style="margin-top:30px;text-align:left">
    <div class="card"><div class="ic">1</div><h3>Responds to the search command</h3><p>The dog begins working on cue.</p></div>
    <div class="card"><div class="ic">2</div><h3>Systematic search</h3><p>Working the area — no target odor recognized yet.</p></div>
    <div class="card"><div class="ic">3</div><h3>Detection</h3><p>Odor becomes meaningful. Recognition begins.</p></div>
    <div class="card"><div class="ic">4</div><h3>Change of behavior</h3><p>The tell: respiration, head, body, bracketing the source.</p></div>
    <div class="card"><div class="ic">5</div><h3>Trained final response</h3><p>The dog reports its conclusion — the sit is phase five, not the whole story.</p></div>
    <div class="card" style="background:var(--navy);color:#fff;border-color:var(--navy)"><h3 style="color:#fff">Why it matters</h3><p style="color:#c4d2dd">Phases 3 and 4 are the investigation. A handler who can describe them can explain — and defend — exactly what the dog did.</p></div>
  </div>
  <div style="max-width:760px;margin:34px auto 0">
   <p>Naming the phases is not academic. It is the difference between a handler who can testify and one who can only assert. Walk a single search through the sequence and the point becomes obvious.</p>
   <p><b>Phase one — responds to the search command.</b> The work begins on cue, not before. A dog that is "searching" before it is sent is a dog that is freelancing, and a freelancing dog is one a court can argue was cueing on something other than odor. The command is a clean start line: everything after it is on the record.</p>
   <p><b>Phase two — systematic search.</b> The dog covers the area methodically, working air currents, checking seams and corners, moving with intent but without recognition. There is no target odor yet — or none the dog has met. This phase looks like nothing is happening. It is actually the dog doing exactly what it should: eliminating negative space. An honest "there is nothing here" is built in phase two, and it matters as much as a find.</p>
   <p><b>Phase three — detection.</b> Odor becomes meaningful. This is the hinge of the entire search, and it is almost always missed, because it is subtle and it is fast. The dog crosses a scent cone and something registers. You will see it first in the breath — the open, cooling pant closes into rapid, shallow sniffs as the dog samples. This is the moment recognition begins. It is not yet the answer; it is the dog deciding there is a question worth working.</p>
   <p><b>Phase four — change of behavior.</b> Now the dog commits. The head drops or lifts to place the odor. The tail changes — often stiffening, sometimes accelerating. Footwork tightens into bracketing: the dog works back and forth across the edges of the odor plume, narrowing, overshooting, correcting, driving toward the strongest concentration. This is the investigation. Phases three and four are where the dog actually solves the problem, and they are exactly what a handler must be able to describe under oath.</p>
   <p><b>Phase five — trained final response.</b> The sit, the down, the freeze — whatever the dog was taught. It is the dog's report of a conclusion it reached one, two, four seconds earlier. It is real, and it matters, but it is the last line, not the story. A team that only sees phase five is reading the last page of a book and calling it the plot.</p>
   <p>When a handler can narrate a search this way — command, search, detection, change of behavior, response — two things happen. The training gets better, because the handler is coaching the whole sequence instead of drilling a sit. And the testimony gets better, because the handler can answer the only question that ever really matters on the stand: <i>what did the dog do, and how did you know what it meant?</i></p>
  </div>
  {figure2(("lsoc-105-lab-saeching-for-source.jpg","The systematic search — before the sit"), ("lsoc-104-lab-freeze-alert.jpg","Phase five — the trained final response"))}
</div></section>

<section class="sec"><div class="wrap split">
  <div>
    <div class="eyebrow">Framework</div>
    <h2>The Four Classes of Behavior</h2>
    <p>Not everything a dog does means the same thing, and a handler who blurs these together will misread the dog and mislead a court. Separating them keeps you honest about what the dog is actually telling you.</p>
    <ul class="tick">
      <li><b>Intrinsic</b> — what the dog does by nature: the drive to hunt, the way it uses air, the tempo that is simply that animal.</li>
      <li><b>Trained</b> — what we deliberately taught, including the final response and the search pattern.</li>
      <li><b>Independently learned</b> — what the dog figured out on its own, for better or worse. Dogs are relentless pattern-finders. A dog that learns "aids are always on the left rear tire" has learned something we did not teach and do not want.</li>
      <li><b>Handler-influenced</b> — what the dog did because of us, knowingly or not.</li>
    </ul>
    <p>That last class is the dangerous one, and it is dangerous precisely because it is invisible to the person causing it. A handler who slows down at the trunk they searched last week, who tightens the leash near the spot the training aid "should" be, who exhales when the dog reaches the right car, is running a second, silent conversation the dog can hear perfectly. The dog is not cheating. It is doing its job — reading its environment, and the handler is part of the environment. Our answer is not to pretend influence away. It is to train to minimize it and to test in a way that exposes it, so that when the dog commits, we know the commitment came from odor and not from us.</p>
  </div>
  <div>
    <div class="eyebrow">Reading the dog</div>
    <h2>Every dog has an accent.</h2>
    <p>No two dogs say it the same way. One dog's change of behavior is a dramatic head-snap; another's is a barely perceptible drop in the tail and a change in cadence you would miss if you blinked. That is why there is no universal checklist that reads every dog. There is only <i>your</i> dog, and the baseline you have learned by watching it work a hundred clean searches so you know what "normal" looks like the moment it stops being normal.</p>
    <p>Reading behavior is a learned skill, built on that baseline and watching for change:</p>
    <ul class="tick">
      <li><b>Respiration</b> — often the first and clearest tell. The open, thermoregulating pant closes into rapid, deliberate sampling the instant the dog meets odor. Learn to hear it and you are reading detection in real time.</li>
      <li><b>Head position</b> — where the dog is placing the problem: up into a current, down at a seam, snapping back to a source it overran.</li>
      <li><b>Tail carriage</b> — tension, height, and speed. For most dogs it stiffens or changes rhythm at commitment. For yours it may do the opposite; that is why baseline is everything.</li>
      <li><b>Footwork</b> — bracketing back and forth across the plume, overshooting and correcting, then the hard drive to source that says the dog has stopped searching and started answering.</li>
    </ul>
    <p>The discipline that ties it together is simple to say and hard to live: <b>let the dog stop you; you don't stop the dog.</b> The handler who yanks a dog off odor because it "already alerted over there," or who steers a dog toward where the handler expects the aid to be, has replaced the dog's nose with their own assumptions. Our job is to present the search, keep our influence out of it, and then read — carefully, honestly — what the animal tells us.</p>
    <div class="quote">"Every search is a conversation. The dog is talking. The question is whether the handler understands the language."</div>
  </div>
</div>
<div class="wrap">{figure(("lsoc-107-dog-sniffing-bd-2.jpg","Reading the change of behavior on the scent board"))}</div>
</section>

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

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Building independent dogs</div>
  <h2>Teach the dog it is allowed to say "I don't know."</h2>
  <p>The single most valuable thing a detector dog can learn is that a blank area is an acceptable answer. A dog that believes every search must end in a find will eventually manufacture one — because the reward, the handler's body language, and the pattern of training have all taught it that "no odor" is failure. That dog is not lying. It has simply learned the wrong lesson, and it has learned it from us.</p>
  <p>So we build the opposite lesson on purpose. We run <b>blank searches</b> — areas with no target odor — and we reward the dog for working them honestly and clearing them. We use <b>productive failure</b>: problems the dog cannot solve by guessing, only by working, so that quitting on a bad assumption costs nothing and persistence pays. Over hundreds of repetitions the dog internalizes a quiet confidence — it does not have to please us, it has to solve the odor problem, and sometimes the honest solution is "there is nothing here." A dog that can say "I don't know" is a dog whose "yes" means something.</p>
  <p>This is also why we <b>reward the investigation, not just the response.</b> If the only thing that ever earns a paycheck is the sit, the dog learns to rush to the sit. If the searching, the bracketing, the honest problem-solving all get valued, the dog learns to work the problem thoroughly and let the response arrive when it has earned it. Reward is information. We are careful about what we are actually telling the dog every time we deliver it.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The Invisible Leash</div>
  <h2>The dog can hear everything you didn't mean to say.</h2>
  <p>In the early 1900s a horse named Clever Hans appeared to do arithmetic, tapping out answers with his hoof. He was genuinely brilliant — not at math, but at reading the involuntary tension and relief in the people around him, who leaned in as he approached the right number and relaxed when he reached it. He was answering the humans, not the question. Every detector dog is a Clever Hans waiting to happen, and the research bears it out: Dr. Lisa Lit's work showed that handler beliefs about where an aid was hidden measurably changed where dogs alerted — including alerts on locations that held no target odor at all.</p>
  <p>We take that seriously instead of pretending we are immune to it. Handler influence travels down four channels: <b>physical</b> (leash tension, footwork, where you plant yourself), <b>visual</b> (where you look, how you lean, a glance at the "right" spot), <b>verbal</b> (a change in tone, a repeated command, the timing of praise), and <b>emotional</b> (the anticipation the dog can feel coming down the leash). None of these require intent. A handler who knows where the aid is will leak it, every time, unless the training and the testing are built to prevent it.</p>
  <p>The fix is discipline in how we move and rigor in how we test. We teach handlers to present a search the same way whether they know the answer or not, and then we take the answer away from them entirely. <a href="/resources-handler-influence-invisible-leash.html">Read the full breakdown of handler influence and how honest teams test for it →</a></p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The Scent Board System</div>
  <h2>Teach the dog to think before it alerts.</h2>
  <p>Our signature training tool is a deceptively simple one: a board of identical containers, some holding target odor and some holding distractors or nothing at all, arranged so the dog cannot succeed by memorizing a pattern. The Scent Board System trains the three skills that separate a discriminating dog from a guessing one — <b>discrimination</b> (target odor versus the food, the toy, the novel smell that isn't the job), <b>bracketing</b> (working the edges of odor to pin the strongest source), and <b>source commitment</b> (driving to the actual origin instead of responding to a pool of scent nearby).</p>
  <p>Because the layout changes and the answer moves, the dog cannot cheat its way to a reward. It has to actually work the odor, every rep. Over time this builds a dog that pauses at ambiguity instead of blurting an answer — a dog that thinks. That habit, built on a board in a training room, is exactly the habit you want when the same dog is working a real vehicle on a real shift with a real defense attorney waiting months down the road.</p>
</div></section>

<section class="sec wash"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">Trust, but verify</div>
  <h2>Reliability is proven, not asserted.</h2>
  <p>If a handler always knows where the aid is hidden, no amount of good intention makes the results trustworthy — the Invisible Leash sees to that. So we build proof into the training itself with <b>blind</b> and <b>double-blind</b> testing. In a blind test, the handler does not know where the target is. In a double-blind test, no one present knows — not the handler, not the person running the exercise — so there is no one for the dog to read but the odor. A dog that performs under double-blind conditions is a dog demonstrating that it works the problem, not the people.</p>
  <p>This is not a gimmick we run once for a certificate. It is a habit of mind. Every honest evaluation asks the same question a court will: how do you know the dog was responding to odor and not to you? A team that has lived inside blind testing has a real answer. A team that has only ever trained where the handler knew the answer has a hope, and hope does not survive cross-examination.</p>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="eyebrow">The training record</div>
  <h2>The court knows only what you recorded.</h2>
  <p>Months or years after a deployment, no one will remember the search. The dog cannot testify. The handler's memory will be picked apart. What remains is the record — the training logs, the maintenance history, the testing results, the documented failures as well as the finds. If it is thorough and honest, it is the strongest evidence in the room. If it is thin, cherry-picked, or absent, it becomes the defense's best exhibit.</p>
  <p>So we document like it will be read aloud in court, because someday it might be. We record misses and false responses, not just successes, because a training log with no failures in it is not a record of a perfect dog — it is a record of a dishonest logbook, and any competent attorney knows it. Honest documentation of a dog's real error rate is not a weakness to hide. It is the foundation of a reliability a court can actually trust.</p>
</div></section>

<section class="sec wash"><div class="wrap split">
  <div>
    <div class="eyebrow">Where it all points</div>
    <h2>Train for the courtroom, not just the yard.</h2>
    <p class="lead">Every exercise is future evidence. The most important trial your dog will ever be part of begins months before anyone files a motion — in how the team was trained, evaluated, and documented.</p>
    <p>David's work is grounded in the case law that governs detector-dog evidence — <i>Harris, Jardines, Caballes, Rodriguez, Place, Edmond</i> — and in the discipline of separating observation from interpretation on the witness stand. Reliability that can't be documented and explained isn't reliability a court can use.</p>
    <p>On the stand, the most important skill a handler has is the discipline to say what the dog <i>did</i> and stop there — to keep observation and interpretation in separate sentences. "The dog's respiration changed, it snapped its head back to the seam of the trunk, bracketed twice, and sat" is an observation a handler can defend. "The dog knew there were narcotics in the car" is an interpretation that a good attorney will take apart, because the dog knows odor, not law. A handler trained our way testifies to behavior — precise, bounded, honest about the limits of what a dog can tell you — and that testimony holds up precisely because it does not overreach.</p>
    <div class="quote">"Reliability is not something we claim. It is something we demonstrate."</div>
    <a class="btn dark" href="/agencies.html">How this protects an agency's case</a>
  </div>
  <div class="card" style="align-self:start">
    <h3 class="mt0">The standard behind it</h3>
    <p class="muted">This method is codified as the <b>LSOC courtroom-defensible standard</b> — the benchmark every dog and handler here is trained and evaluated against. {fill('Confirm relationship between the LSOC standard and the "K9 Alliance Certification Standard" referenced on the original site — same thing, or two standards?')}</p>
    <a class="btn sm" href="/certification.html">About the standard</a>
  </div>
</div></section>

<section class="sec"><div class="wrap" style="max-width:820px">
  <div class="center"><div class="eyebrow">On integrity</div><h2>The point isn't to win. It's to be right.</h2></div>
  <p class="lead center" style="margin-top:14px">David is a strong advocate for properly trained detector dogs — and an equally strong opponent of using them to &ldquo;beat the system.&rdquo; Honest scrutiny doesn't threaten a competent team; it makes it better. The purpose is to catch offenders, protect the innocent, and present evidence that <i>deserves</i> to be trusted.</p>
  <p style="margin-top:16px">That is why you will never hear a claim of "100% accuracy" or "never a false alert" from this program. Any trainer who tells you that is either selling something or does not understand the animal. Dogs are living detectors, not instruments; they have off days, they meet odor in confusing places, and an honest team accounts for that instead of hiding it. The goal is not a dog that is never wrong. It is a dog whose work is so well trained, so honestly evaluated, and so thoroughly documented that when it is right — which is the overwhelming majority of the time — you can prove it, and when it is wrong, you already knew the rate and disclosed it. That is what courtroom-defensible actually means, and it is a higher standard than perfection, because it is a standard you can keep.</p>
  <p style="margin-top:12px">This is the whole philosophy in one breath: a detector dog is a witness, and a witness's value is its honesty. Train the honesty in, test to keep it, document to prove it, and the reliability takes care of itself.</p>
</div></section>

<section class="sec tight"><div class="wrap"><div class="eyebrow center">The Scent Board System</div>{figure2(("lsoc-109-dog-sniffing-bd-3.jpg","Discrimination and source commitment on the board"), ("lsoc-98-bedbug-dog-working-board.jpg","Working a detection problem"))}</div></section>
{video_strip("method.html")}

<section class="sec"><div class="wrap"><div class="center"><div class="eyebrow">Questions</div><h2>About the method</h2></div>
<div style="max-width:820px;margin:28px auto 0">{faq_html(method_faq)}</div></div></section>

<section class="sec tight"><div class="wrap" style="max-width:900px">{book_callout()}</div></section>

<section class="sec tight"><div class="wrap"><div class="ctastrip">
  <h2>Want a team trained this way?</h2>
  <p>Whether you're an agency, a handler, or building a program — this is the standard we work to.</p>
  <div class="btnrow" style="justify-content:center"><a class="btn" href="/contact.html">Start the conversation</a><a class="btn ghost" href="/resources.html">Read the guides</a></div>
</div></div></section>
"""
page("method.html", "The Method: Behavior Is Evidence | K9School — David Latimer",
     "The LSOC approach to detector-dog work: the search before the sit, the Five Phases of behavior, honest independent dogs, and training for the courtroom.",
     method_body, nodes=[person_schema, faq_schema(method_faq)], active="/method.html")

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

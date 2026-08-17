# K9School.net — Handoff & Operations Guide

> This file doubles as the Claude Code project brief (auto-loaded as `CLAUDE.md`).
> If you are a human, it's your handoff doc too. Read the **Golden Rule** first.

The client is **Latimer School of Operational K9s** (David Latimer), k9school.net —
operational detection-dog training, handler/instructor certification, program
consulting, expert-witness work, and detection-dog placement. This repo is the
website: a fast, dependency-free static site generated from one Python script.

> **Before you build any location pages, read Section 12.** The geo strategy here is
> a deliberate deviation from the portfolio standard, and it is easy to "fix" by
> mistake. Section 12 also records where the site actually lives right now, which is
> not what Section 3 implies.

---

## 0. TL;DR quick start

```bash
python3 build.py        # regenerate the whole site into ./public
python3 validate.py     # must print "VALIDATION PASSED"
# preview locally (styles use absolute /paths, so serve over HTTP, not file://):
cd public && python3 -m http.server 8080   # open http://localhost:8080
```

To ship a change: **edit `build.py`** → `python3 build.py` → `python3 validate.py`
→ commit **both** `build.py` and the regenerated `public/` → push. Vercel deploys.

---

## 1. Golden Rule — `build.py` is the single source of truth

Almost every `.html` file, plus `styles.css`, `main.js`, `sitemap.xml`,
`robots.txt`, `404.html`, and `_redirects`, is **generated** by `build.py`.

**Do NOT hand-edit generated files.** Edit `build.py` (page content lives in
Python strings there) and rebuild. A hand edit to `public/agencies.html` will be
silently overwritten the next time anyone runs the build.

The only files in `public/` that are **not** generated (and must stay committed):
`og.png`, `favicon.svg`, `logo.svg`, and everything in `public/downloads/`.
`build.py` never deletes these — it only writes the generated files alongside them.

---

## 2. Repo layout

```
.
├── build.py                 # THE GENERATOR — edit here, then rebuild
├── validate.py              # JSON-LD + broken-link gate (run before every push)
├── vercel.json              # Vercel build config (buildCommand + outputDirectory)
├── package.json             # `npm run build|validate|preview` shortcuts
├── .gitignore
├── .github/workflows/validate.yml   # CI: build + validate on push/PR
├── README-DEPLOY.md         # deployment notes (Netlify + generic host)
├── FILL-IN.md               # the outstanding [amber placeholder] punch list
├── content/
│   └── email-sequences.md   # drop-in autoresponder / nurture copy (Phase 4)
├── marketing-pdfs/          # brand PDFs (capability brief, catalog, pricing,
│   │                        #   expert-witness, proof-intake kit, VOICE brief)
│   └── K9School_Voice_and_Ideology_Brief.pdf   # READ THIS before writing copy
└── public/                  # THE DEPLOYABLE SITE (generated + static assets)
    ├── index.html, agencies.html, training.html, consulting.html,
    │   detection-dogs.html, method.html, resources.html, proof.html,
    │   about.html, certification.html, contact.html, 404.html
    ├── resources-*.html     # 9 SEO / authority articles
    ├── styles.css, main.js, sitemap.xml, robots.txt, _redirects
    ├── og.png, favicon.svg, logo.svg          # static (not generated)
    └── downloads/*.pdf       # site-linked lead magnets (not generated)
```

Requirements: **Python 3.x only, standard library** (no pip installs, no
`requirements.txt`). Node is not needed to build; `package.json` is just for
convenience scripts and Vercel detection.

---

## 3. Vercel setup (do this once)

The human connects Git; these are the project settings. `vercel.json` already
declares the important ones, so most of this is confirmation.

1. **Import the Git repo** into Vercel → New Project.
2. **Framework Preset:** `Other`.
3. **Root Directory:** repo root (leave default — `build.py` is at the root).
4. **Build Command:** `python3 build.py`  *(already set in vercel.json)*
5. **Output Directory:** `public`  *(already set in vercel.json)*
6. **Install Command:** leave default/empty (there are no dependencies).
7. Deploy. Vercel's build image includes Python 3 — `build.py` uses only the
   standard library, so it runs as-is.

**Auto-deploys after that are automatic:** every push to `main` → Production;
every push to another branch / PR → a Preview URL. Nothing else to wire.

> Fallback if you ever want a zero-build deploy: since `public/` is committed,
> you can instead set Build Command to empty and Output Directory to `public`,
> and Vercel will serve the committed files directly.

### Domains & the kipk9.com redirect
- Add **k9school.net** (and `www`) to the Vercel project; pick one canonical host
  and let Vercel 301 the other.
- Add **kipk9.com** to the project and set it to **Redirect** to
  `https://www.k9school.net` (Vercel Domains → kipk9.com → "Redirect to another
  domain"). This preserves the legacy SEO equity. The `public/_redirects` file is
  a Netlify artifact and is **inert on Vercel** — the domain-level redirect above
  is the real one. (If you need path-level redirects later, add a `redirects`
  array to `vercel.json`.)

---

## 4. Git workflow for auto-pushes

Treat `build.py` as source; keep `public/` in sync in the same commit.

```bash
# 1. make the change in build.py (or content/, or a static asset in public/)
# 2. regenerate + gate
python3 build.py && python3 validate.py   # must pass before committing
# 3. commit BOTH the generator and the regenerated output
git add -A
git commit -m "content: tighten agencies hero; fix training FAQ"
git push
```

Conventions:
- **Never commit if `validate.py` fails.** CI (`.github/workflows/validate.yml`)
  re-runs it on push/PR as a backstop.
- Commit `build.py` and `public/` together so diffs are reviewable and the repo
  stays deployable without a build.
- Prefer small, described commits (`content:`, `seo:`, `fix:`, `build:`).
- `main` is production. Use a branch + PR for anything risky to get a Vercel
  Preview URL before it goes live.

---

## 5. Forms & analytics (wire before public launch)

- **Forms** currently POST to a placeholder: `FORM_ACTION` near the top of
  `build.py` (`https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID`). Create a form
  endpoint (Formspree / Basin / Web3Forms / CRM), set `FORM_ACTION`, rebuild.
  Each form already sends a hidden `inquiry_type` field so leads route by
  audience (Agency / Training / Consulting / Detection Dog).
- **Analytics** aren't installed yet. Add a snippet (GA4 / Plausible / Fathom) by
  editing the `<head>` block in the `page()` function in `build.py` (so it lands
  on every page), then rebuild. For the metric that matters, fire a conversion
  event on form success, segmented by `inquiry_type`.
- **Social image:** `public/og.png` exists and is referenced site-wide. Replace
  it with a real branded image any time (keep the filename or update the meta in
  `page()`).

---

## 6. The FILL-IN system (David's outstanding inputs)

Placeholders render on-page as **amber highlights** and in source as
`<span class="fill">[ ... ]</span>`. `validate.py` prints how many remain;
`FILL-IN.md` lists them grouped by page. To fill one, find the matching
`fill('...')` call in `build.py`, replace it with the real content, rebuild.

Priority order (see `marketing-pdfs/K9School_Proof_Intake_Kit.pdf`, which is the
questionnaire built to collect these): **proof** (case studies, references,
video) → **the four stat numbers + prices** → **photos** → a few confirmations.
David's bio and philosophy are already written in from his book — those are done.

---

## 7. Voice & brand guardrails — do not drift

Before writing or editing any copy, read
**`marketing-pdfs/K9School_Voice_and_Ideology_Brief.pdf`**. It distills David's
book (his actual ideology). The non-negotiables:

- **Behavior is evidence** — "the search before the sit." Reading the dog through
  the **Five Phases**, not just rewarding the sit. This is the site's core idea.
- **Courtroom-defensible / integrity** — the goal is truth, never "beating" the
  defense or the system. **Never** claim "100% accurate" or "never false alerts";
  David explicitly rejects that language.
- **The whole team** — "handler, heal thyself"; train the human end of the leash.
- **Voice:** calm, exact, operator-to-operator. Describe behavior, then meaning.
  No hype or superlatives without proof.
- **Credibility to keep visible:** FBI National Academy graduate, retired Chief
  of Police, detector-dog trainer since 1999, author, expert witness. And
  **Kip** — the honest accelerant dog, namesake of the Kip K9 brand.

### Brand colors (already in `styles.css` via `build.py`)
Black `#08090d` · Gold `#c9a227` · Dark Navy Blue `#0a1a33` (+ `#0f2444` / `#173a66`).

---

## 8. Standard naming — one open decision

The old site said "K9 Alliance Certification Standard"; David's book brands
everything **LSOC**. The site is unified to the **"LSOC courtroom-defensible
standard."** Two on-page notes (Certification page FAQ + The Method page)
explicitly ask David whether "K9 Alliance" is the same thing, a separate
third-party cert he uses, or a legacy name to retire. **Do not remove those
flags until David answers**; then update the wording everywhere in one pass
(search `build.py` for `K9 Alliance`).

---

## 9. The book (future purchase link)

David's manuscript (~73k words) is **not** published here yet. There's a "coming
soon" book callout on The Method and About pages (`book_callout()` in `build.py`)
with a placeholder for the eventual purchase URL. When it's live: set the title,
add a cover image, and turn the callout's button into the buy link — one edit in
`book_callout()`, rebuild.

---

## 10. Backlog (roughly in order)

1. Connect Git + Vercel; confirm build settings (Section 3). First deploy.
2. Set `FORM_ACTION`; test a submission from each of the 4 audience forms.
3. Add analytics + form-success conversion events (Section 5).
4. Configure kipk9.com → k9school.net domain redirect (Section 3).
5. Fill in proof + numbers + prices as David returns the intake kit (Section 6).
6. Replace `og.png` and add real photos/video.
7. Resolve the LSOC vs K9 Alliance naming once David answers (Section 8).
8. Wire the book purchase link when the book goes live (Section 9).

---

## 11. Gotchas / do-not-break

- **Absolute asset paths:** pages link `/styles.css`, `/main.js`. Preview over
  **HTTP** (`python3 -m http.server`), not `file://`, or CSS won't load. On
  Vercel this is correct as-is.
- **Internal links use `.html`** (e.g. `/agencies.html`). Do **not** enable
  Vercel `cleanUrls` — it would 301 `/agencies.html`→`/agencies` and break them.
- **Don't delete** `public/og.png`, `favicon.svg`, `logo.svg`, or
  `public/downloads/*.pdf` — the build won't recreate them.
- **JSON-LD is hand-assembled** in `build.py`. If you touch schema strings, run
  `validate.py` — it will catch malformed JSON.
- Keep `build.py` **standard-library only** so Vercel needs no install step.
- The marketing PDFs are generated by a separate script (`docs_build.py`, kept
  outside this repo). If you need to regenerate them, ask for that script; the
  committed PDFs in `marketing-pdfs/` and `public/downloads/` are the current set.

---

## 12. Standing decisions (2026-08-17)

Recorded so a later session doesn't undo them by following the portfolio standard
literally. Both were settled after auditing this build against Keystone.

### 12.1 Geo strategy — a light regional layer, not a city lattice

**Decision by Kristofer Elling, 2026-08-17. Do not build `/locations/{city}` pages
for this site.**

The portfolio standard's Local dimension assumes a local service business whose
buyers search by town. This one isn't. LSOC sells to agency commanders and program
managers, largely out of state, and the buying decision has nothing to do with which
city the buyer is in. A hundred templated town pages here would be exactly the thin
geo the standard warns against — worse than no geo page at all.

What we build instead, once the Section 4 answers in `INTAKE-KIT-V2.md` (Q37–Q43)
come back:

- **One real facility page.** The Lincoln property in genuine detail — acreage,
  structures, vehicles, what search problems it supports. Written so it could only
  be about this place.
- **A "where teams come from" page**, listing states teams have actually traveled
  from. Real list only. Never a generated state matrix.
- **An on-site / we-travel-to-you page**, covering how training at an agency's own
  facility works, radius and logistics.
- **Alabama and Southeast context** woven into existing pages where it's true —
  terrain, climate, the case types a handler from elsewhere wouldn't expect. Not a
  separate page for it.

That is the whole geo layer. It scores roughly 3 on Local instead of 5, and that is
the accepted trade. The budget the lattice would have consumed goes to the
court-admissibility cluster, the agency-vertical pages, and per-discipline depth,
which is where this business's search demand actually is.

**If you think this site needs city pages, you are about to repeat a decision that
was already made deliberately. Raise it, don't build it.**

### 12.2 Where the site actually lives (supersedes Section 3's assumptions)

- The repo is connected to Vercel (project `k9-school`, org `turkokami-9144s-projects`)
  and auto-deploys `main` to production. That part of Section 3 is done.
- **Production is `k9-school.vercel.app`. It is a staging URL.**
- **`k9school.net` still serves the old GoDaddy Website Builder site** (server
  `DPS/2.0.0`, `img1.wsimg.com` assets, 21 URLs in its sitemap). None of this build
  is public yet.
- `SITE` in `build.py` is `https://www.k9school.net`, so every canonical and every
  schema `@id` already points at the destination domain. That's correct and
  intentional, but it means the schema currently references a host serving different
  HTML. It resolves itself at cutover — don't "fix" it by pointing `SITE` at the
  vercel.app URL.
- David controls the GoDaddy DNS and is ready for the old site to go dark, on our
  timing. **We finish first, then cut.**
- Cutover is blocked on `INTAKE-KIT-V2.md` Section 9, and the 21 legacy URLs each
  need a 301 to their new equivalent. `public/_redirects` is a Netlify artifact and
  is inert on Vercel — the redirect map goes in a `redirects` array in `vercel.json`.
- **Check Q62 before touching DNS.** If David's business email runs through GoDaddy,
  moving nameservers without preserving MX records takes his email down.

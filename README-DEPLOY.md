# K9School.net — Smart Site: Deploy & Launch Guide

This folder is a complete, fast, mobile-first static website for **Latimer School of
Operational K9s** (k9school.net), built to the Phase 0–5 plan. It needs no database,
no build server, and no framework runtime — it's pure HTML/CSS/JS, so it loads fast
and is cheap and secure to host.

```
site/
├─ public/                 ← THE WEBSITE (deploy this folder's contents)
│  ├─ index.html           ← Home
│  ├─ agencies.html        ← Hub: Law enforcement
│  ├─ training.html        ← Hub: Handler / instructor courses
│  ├─ consulting.html      ← Hub: Program development & audits
│  ├─ detection-dogs.html  ← Hub: Commercial / operational dogs
│  ├─ proof.html · about.html · certification.html · contact.html
│  ├─ styles.css · main.js
│  ├─ sitemap.xml · robots.txt
├─ build.py                ← Regenerates all pages from one design system
├─ FILL-IN.md              ← Everything only you/David can supply (59 items)
└─ README-DEPLOY.md        ← This file
```

## The fastest way to go live (pick one)

**Netlify or Cloudflare Pages (recommended, free tier is fine).**
Drag-and-drop the `public/` folder into a new site, or connect a repo. Point the
domain `k9school.net` at it. HTTPS is automatic. Done.

**Any traditional host / cPanel.** Upload the *contents* of `public/` to your web root
(`public_html/`). That's it — there is nothing to compile.

## Two things to wire before launch (Phase 4 smart layer)

1. **Forms.** Every form posts to a placeholder endpoint
   (`FORM_ACTION` in `build.py`, currently `formspree.io/f/REPLACE_WITH_YOUR_FORM_ID`).
   Create a free/low-cost form endpoint (Formspree, Basin, Web3Forms, or your CRM's
   form URL), then either edit `FORM_ACTION` in `build.py` and re-run it, or
   find-and-replace the URL across the `.html` files. Forms already send a labeled
   subject line and an `inquiry_type` field so leads route by audience.

2. **Analytics.** Add your analytics snippet (GA4, Plausible, or Fathom) before
   `</body>`. For richest data, fire a conversion event on each form's success page so
   you can see qualified inquiries **by audience** (Agencies / Training / Consulting /
   Detection Dogs) — that's the Phase 5 metric that matters.

## Redirect map (preserve legacy SEO equity)

`kipk9.com` already 302-redirects to k9school.net. Make these **301 (permanent)** so
ranking equity transfers, and map old paths to the closest new page:

| Legacy | New |
|---|---|
| kipk9.com/ (any path) | https://www.k9school.net/ |
| old narcotics / arson / bed bug / termite pages | /detection-dogs.html |
| old training / course pages | /training.html |
| old about / contact | /about.html · /contact.html |

On Netlify, put this in a `_redirects` file in `public/`:
```
https://kipk9.com/*   https://www.k9school.net/:splat   301!
/*                    /index.html                       404
```
(Adjust per your DNS/host. Keep one canonical host — pick `www` or root, 301 the other.)

## Editing content

- **Small tweaks:** edit the `.html` files directly.
- **Structural / site-wide changes:** edit `build.py` (one shared design system, nav,
  footer, and per-page content) and run `python3 build.py` to regenerate everything
  consistently. This is the "maintainable modern build" from the plan.

## What's already built in (so you don't have to)

- Responsive, mobile-first layout with a working mobile menu.
- Reversal-method page order on every hub: arrival → proof → offer → objections → CTA.
- Segmented lead-capture forms with audience-specific fields.
- JSON-LD schema on every page: `LocalBusiness`/`ProfessionalService`, `Person`
  (David Latimer), `FAQPage`, plus SEO/OpenGraph meta and canonical URLs.
- `sitemap.xml` + `robots.txt` for indexing.
- SEO-oriented titles/descriptions per the Phase 1 cluster plan.

## Launch checklist

- [ ] Fill in the 59 items in `FILL-IN.md` (proof is the priority — it carries the
      agency & consulting pages).
- [ ] Set a real `FORM_ACTION` and test a submission from each hub.
- [ ] Add analytics + form-success conversion events.
- [ ] Add an `og.jpg` (1200×630) social share image to `public/`.
- [ ] Set 301 redirects from kipk9.com and legacy URLs.
- [ ] Choose canonical host (www vs root) and force HTTPS.
- [ ] Submit `sitemap.xml` in Google Search Console; request indexing.
- [ ] QA on a real phone: menu, forms, tap targets, load speed.
- [ ] Go live, then start the 30/60/90-day optimization loop (Phase 5).

#!/usr/bin/env python3
"""
Image optimizer for K9School (run locally, NOT part of the Vercel build).
For every public/images/*.jpg:
  - writes a .webp sibling (quality 82) for smaller, faster LCP
  - records intrinsic width/height
Emits image-dims.json (name -> [w, h]) at the repo root, which build.py reads
(stdlib json only) to stamp width/height on every <img> and prevent layout shift.

Requires Pillow (dev-only dependency). Re-run after adding/replacing images:
    python optimize_images.py
"""
import json, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "public" / "images"
dims = {}
made = 0
for jpg in sorted(IMG.glob("*.jpg")):
    im = Image.open(jpg).convert("RGB")
    dims[jpg.name] = [im.width, im.height]
    webp = jpg.with_suffix(".webp")
    dims[webp.name] = [im.width, im.height]
    im.save(webp, "WEBP", quality=82, method=6)
    made += 1

(ROOT / "image-dims.json").write_text(json.dumps(dims, indent=0), encoding="utf-8")
jpg_bytes = sum(p.stat().st_size for p in IMG.glob("*.jpg"))
webp_bytes = sum(p.stat().st_size for p in IMG.glob("*.webp"))
print(f"Converted {made} images -> WebP")
print(f"JPG total: {jpg_bytes/1e6:.1f} MB  ->  WebP total: {webp_bytes/1e6:.1f} MB")
print(f"Wrote image-dims.json ({len(dims)} entries)")

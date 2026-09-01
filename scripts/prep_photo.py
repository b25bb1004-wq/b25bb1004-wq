#!/usr/bin/env python3
"""Prepare a profile photo for ASCII conversion.

The supplied photo already has a clean light background, so this script
uses grayscale + CLAHE/contrast enhancement. If rembg is installed and
REM_BG=1 is set, it will also attempt background removal.
"""
import os, sys
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py assets/source-photo.jpg")
        raise SystemExit(1)

    src = Path(sys.argv[1])
    out = src.parent / "source-prepped.png"
    img = Image.open(src).convert("RGB")

    if os.getenv("REM_BG") == "1":
        try:
            from rembg import remove
            img = remove(img)
            if img.mode == "RGBA":
                bg = Image.new("RGBA", img.size, "white")
                bg.alpha_composite(img)
                img = bg.convert("RGB")
        except Exception as exc:
            print(f"rembg unavailable/failed ({exc}); continuing without it.")

    gray = ImageOps.grayscale(img)
    gray = ImageEnhance.Contrast(gray).enhance(1.45)
    gray = ImageEnhance.Sharpness(gray).enhance(1.2)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray.save(out)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prepare a profile photo for ASCII conversion.

Real photos with a busy background (a night sky, mountains, trees, distant
lights) don't just need grayscale + contrast: the background's own brightness
variation ends up in the ASCII ramp right alongside the subject, and a flatly
lit face still converts to a dark, unreadable blob. Three steps fix that:

1. Remove the background with rembg, so only the subject remains.
2. Boost local contrast with OpenCV's CLAHE (contrast-limited adaptive
   histogram equalization) — this is what gives a flat face real highlights
   and shadows instead of one flat grey blob.
3. Composite onto pure white so the background maps to the blank end of the
   ASCII ramp (white -> space), rather than carrying speckled noise from
   whatever was behind the subject.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
import cv2

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py assets/source-photo.jpg")
        raise SystemExit(1)

    src = Path(sys.argv[1])
    out = src.parent / "source-prepped.png"
    img = Image.open(src).convert("RGB")

    from rembg import remove
    cutout = remove(img)  # RGBA, background made transparent
    bg = Image.new("RGBA", cutout.size, "white")
    bg.alpha_composite(cutout)
    img = bg.convert("RGB")

    # CLAHE works on a single channel; apply it to luminance (L in Lab) so
    # colour information doesn't skew the contrast curve, then take L as the
    # final greyscale source.
    lab = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)

    gray = Image.fromarray(l, mode="L")
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray.save(out)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
One-time developer utility: the closing-seal artwork sits asymmetrically within
its own source photo (the seal touches the left edge of the frame with ~0px
margin, vs ~51px on the right), which reads as "cropped on the left" once
displayed. Pads the already-processed closing-seal.png with transparent pixels
so the seal is visually centered, without re-running the chroma-key pipeline.
Not part of the Vite build - run manually.
"""
import numpy as np
from PIL import Image
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "src" / "assets" / "images"
TARGET = IMAGES_DIR / "closing-seal.png"

ALPHA_THRESHOLD = 10


def visible_bounds(alpha: np.ndarray) -> tuple[int, int, int, int]:
    cols = np.where(alpha.max(axis=0) > ALPHA_THRESHOLD)[0]
    rows = np.where(alpha.max(axis=1) > ALPHA_THRESHOLD)[0]
    return cols.min(), cols.max(), rows.min(), rows.max()


def main():
    img = Image.open(TARGET).convert("RGBA")
    arr = np.array(img)
    w, h = img.size
    left, right, top, bottom = visible_bounds(arr[:, :, 3])

    left_margin = left
    right_margin = w - 1 - right
    top_margin = top
    bottom_margin = h - 1 - bottom
    print(f"current margins - left:{left_margin} right:{right_margin} top:{top_margin} bottom:{bottom_margin}")

    pad_left = max(0, right_margin - left_margin)
    pad_right = max(0, left_margin - right_margin)
    pad_top = max(0, bottom_margin - top_margin)
    pad_bottom = max(0, top_margin - bottom_margin)
    print(f"padding to add - left:{pad_left} right:{pad_right} top:{pad_top} bottom:{pad_bottom}")

    new_w = w + pad_left + pad_right
    new_h = h + pad_top + pad_bottom
    canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    canvas.paste(img, (pad_left, pad_top))
    canvas.save(TARGET, optimize=True)
    print(f"-> {TARGET.name} resized {w}x{h} -> {new_w}x{new_h}, seal now centered")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
One-time developer utility: split the emblem watermark (a single tall image with
an ornamental band at the top, a mirrored one at the bottom, and a large blank
transparent gap in the middle) into two independently-croppable PNGs so each can
be anchored to the letter card's real top/bottom edges instead of being stretched
via object-fit into a variable-height container.

Finds the true content boundary by scanning the alpha channel row-by-row rather
than guessing a percentage split. Not part of the Vite build - run manually.
"""
import numpy as np
from PIL import Image
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "src" / "assets" / "images"
SOURCE = IMAGES_DIR / "emblem.png"

ALPHA_THRESHOLD = 10  # rows with max alpha at/below this are considered "blank"
PADDING = 30  # extra rows of blank space kept on each crop, for a soft fade


def find_blank_gap(alpha: np.ndarray) -> tuple[int, int]:
    row_max = alpha.max(axis=1)
    is_blank = row_max <= ALPHA_THRESHOLD
    runs = []
    start = None
    for i, blank in enumerate(is_blank):
        if blank and start is None:
            start = i
        elif not blank and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(is_blank) - 1))
    # the gap between the top and bottom ornament is the longest blank run
    runs.sort(key=lambda r: r[1] - r[0], reverse=True)
    return runs[0]


def main():
    img = Image.open(SOURCE).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    h, w = alpha.shape

    gap_start, gap_end = find_blank_gap(alpha)
    print(f"emblem.png: {w}x{h}, blank gap rows {gap_start}-{gap_end}")

    top_end = min(h, gap_start + PADDING)
    bottom_start = max(0, gap_end - PADDING)

    top_crop = img.crop((0, 0, w, top_end))
    bottom_crop = img.crop((0, bottom_start, w, h))

    top_path = IMAGES_DIR / "emblem-top.png"
    bottom_path = IMAGES_DIR / "emblem-bottom.png"
    top_crop.save(top_path, optimize=True)
    bottom_crop.save(bottom_path, optimize=True)

    print(f"-> {top_path.name}  ({top_crop.size[0]}x{top_crop.size[1]})")
    print(f"-> {bottom_path.name}  ({bottom_crop.size[0]}x{bottom_crop.size[1]})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Throwaway verification helper (not committed to the app): composite each
processed PNG over swatches matching the real page/card tones it will sit
against, plus a couple of contrasting tones to expose any residual fringe.
Outputs go to /tmp for visual inspection via the Read tool.
"""
from pathlib import Path
from PIL import Image

IMAGES_DIR = Path(__file__).parent.parent / "src" / "assets" / "images"
OUT_DIR = Path("/private/tmp/claude-501/-Users-yasminhaitham-wedding-invitation/642874d5-c7aa-4180-8805-7175b40b38e7/scratchpad/composites")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SWATCHES = {
    "cream": (0xFD, 0xF9, 0xF4),
    "cream-deep": (0xF5, 0xEC, 0xE3),
    "bg": (0xF7, 0xED, 0xE6),
    "gradient-fefaf6": (0xFE, 0xFA, 0xF6),
    "gradient-f1dad1": (0xF1, 0xDA, 0xD1),
    "contrast-grey": (0x99, 0x99, 0x99),
    "contrast-white": (0xFF, 0xFF, 0xFF),
}

IMAGES = [
    "envelope.png",
    "deco-flower-a.png",
    "deco-flower-b.png",
    "flourish.png",
    "closing-seal.png",
    "emblem.png",
]


def composite_over(fg: Image.Image, color: tuple) -> Image.Image:
    bg = Image.new("RGBA", fg.size, color + (255,))
    return Image.alpha_composite(bg, fg).convert("RGB")


def main():
    for name in IMAGES:
        path = IMAGES_DIR / name
        if not path.exists():
            print(f"SKIP (not found): {path}")
            continue
        fg = Image.open(path).convert("RGBA")

        cols = []
        for swatch_name, color in SWATCHES.items():
            cols.append(composite_over(fg, color))

        # Lay swatches out in a row for one combined contact-sheet image per source
        w, h = cols[0].size
        sheet = Image.new("RGB", (w * len(cols), h), (0, 0, 0))
        for i, im in enumerate(cols):
            sheet.paste(im, (i * w, 0))

        out_path = OUT_DIR / f"{path.stem}-contact-sheet.png"
        sheet.save(out_path)
        print(f"{name} -> {out_path} (order: {', '.join(SWATCHES.keys())})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
One-time developer utility: convert decorative JPEGs (with baked-in photographic
backgrounds) into true-alpha PNGs by chroma-keying against an automatically
sampled background reference, with edge color decontamination.

Not part of the Vite build - run manually, inspect output, then wire the
resulting PNGs into the app. Originals are left untouched.
"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "src" / "assets" / "images"

# Per-file overrides. Default is "let the automatic math decide" (empty dict).
CONFIG = {
    "envelope.jpeg": {},
    "deco-flower-a.jpeg": {},
    "deco-flower-b.jpeg": {},
    "flourish.jpeg": {},
    "closing-seal.jpeg": {},
    # emblem.jpeg has an uneven cream-grey gradient rather than a flat
    # background, so it needs a locally-blurred per-pixel reference instead
    # of one global sampled color.
    "emblem.jpeg": {"mode": "local", "blur_radius_frac": 0.10},
}

PERIMETER_FRAC = 0.03
K1 = 2.5  # low cutoff = K1 * bg_spread
K2 = 4.0  # feather width = K2 * bg_spread (added to low to get high)
MIN_LOW = 6.0
MIN_FEATHER = 8.0


def perimeter_mask(h: int, w: int, frac: float) -> np.ndarray:
    strip = max(4, round(min(h, w) * frac))
    mask = np.zeros((h, w), dtype=bool)
    mask[:strip, :] = True
    mask[-strip:, :] = True
    mask[:, :strip] = True
    mask[:, -strip:] = True
    return mask


def global_bg_color(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return np.median(rgb[mask], axis=0)


def luma_distance(rgb: np.ndarray, ref: np.ndarray) -> np.ndarray:
    diff = rgb.astype(np.float64) - ref.astype(np.float64)
    weights = np.array([0.30, 0.59, 0.11])
    return np.sqrt(np.sum(weights * diff**2, axis=-1))


def smoothstep(x, low, high):
    t = np.clip((x - low) / max(high - low, 1e-6), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def process_image(path: Path, cfg: dict):
    img = Image.open(path).convert("RGB")
    rgb = np.array(img).astype(np.float64)
    h, w, _ = rgb.shape
    mask = perimeter_mask(h, w, PERIMETER_FRAC)

    mode = cfg.get("mode", "global")
    if mode == "local":
        # Local mode keys against a per-pixel blurred version of the image
        # itself (for uneven/gradient backgrounds). bg_spread must then be
        # measured as the perimeter's leftover distance to THIS SAME blurred
        # reference (i.e. background noise after the gradient is accounted
        # for) - not the raw color range of the perimeter, which would
        # conflate the gradient's own span with noise and produce cutoffs
        # so high that nothing (including real foreground detail) ever
        # reaches full opacity.
        blur_radius = cfg.get("blur_radius_frac", 0.10) * min(h, w)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        ref = np.array(blurred).astype(np.float64)
    else:
        bg_color = global_bg_color(rgb, mask)
        ref = np.broadcast_to(bg_color, rgb.shape).astype(np.float64)

    distance = luma_distance(rgb, ref)
    bg_spread = float(np.median(np.abs(distance[mask] - np.median(distance[mask]))))
    low = max(MIN_LOW, K1 * bg_spread)
    high = low + max(MIN_FEATHER, K2 * bg_spread)

    alpha = (smoothstep(distance, low, high) * 255).astype(np.uint8)

    # Clean up: median filter kills speckling in fine detail (stamens,
    # scrollwork), then a small close (min->max) fills pinholes without
    # eroding the silhouette.
    alpha_img = Image.fromarray(alpha, mode="L")
    alpha_img = alpha_img.filter(ImageFilter.MedianFilter(3))
    alpha_img = alpha_img.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    alpha_clean = np.array(alpha_img).astype(np.float64)

    # Edge color decontamination: partially-transparent pixels still carry a
    # blend of foreground + background color. Unmix the background's
    # contribution so translucent edges don't fringe with the old backdrop's
    # tint once composited over a *different* background in the app.
    a = alpha_clean / 255.0
    a_safe = np.clip(a, 0.06, 1.0)[..., None]  # avoid divide-by-near-zero blowups
    decontaminated = (rgb.astype(np.float64) - (1 - a_safe) * ref) / a_safe
    decontaminated = np.clip(decontaminated, 0, 255)

    out = np.dstack([decontaminated, alpha_clean]).astype(np.uint8)
    out_img = Image.fromarray(out, mode="RGBA")

    out_path = path.with_suffix(".png")
    out_img.save(out_path, optimize=True)
    print(
        f"{path.name} -> {out_path.name}  "
        f"(spread={bg_spread:.2f}, low={low:.2f}, high={high:.2f}, mode={mode})"
    )


def main():
    for filename, cfg in CONFIG.items():
        path = IMAGES_DIR / filename
        if not path.exists():
            print(f"SKIP (not found): {path}")
            continue
        process_image(path, cfg)


if __name__ == "__main__":
    main()

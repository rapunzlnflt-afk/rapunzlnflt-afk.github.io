"""Recolour the word "clear" in Shauna's logo.

The wordmark sits in the top band of the artwork: "clear" is the neutral slate
part left of x=340, "track" is the orange part right of it, and the drawn railway
track occupies everything below y=120.

Anti-aliased letter edges in this file are light *opaque* grey pixels rather than
partially transparent ones, so a straight RGB swap would leave pale grey fringes
around every letter. Instead each qualifying pixel keeps its ink coverage as
alpha and takes the new colour flat, which composites cleanly on cream or on
near-black.
"""
import sys
import numpy as np
from PIL import Image

SRC = 'assets/logo.png'
SLATE_LUM = 80.0          # measured mean luminance of the slate letters
WORDMARK_BOTTOM = 120     # rows below this are the drawn track
CLEAR_RIGHT = 340         # "clear" ends at x=326; "track" starts at x=346


def luminance(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def recolour_clear(src, target, out):
    im = Image.open(src).convert('RGBA')
    a = np.array(im).astype(float)
    rgb, alpha = a[..., :3], a[..., 3]

    region = np.zeros(alpha.shape, bool)
    region[:WORDMARK_BOTTOM, :CLEAR_RIGHT] = True

    neutral = (np.abs(rgb[..., 0] - rgb[..., 2]) < 30) & (np.abs(rgb[..., 1] - rgb[..., 2]) < 30)
    lum = luminance(rgb)
    mask = region & neutral & (alpha > 0) & (lum < 210)

    # ink coverage: 0 where the pixel is background-white, 1 at full slate density
    k = np.clip((255.0 - lum) / (255.0 - SLATE_LUM), 0.0, 1.0)

    tgt = np.array([int(target[i:i + 2], 16) for i in (1, 3, 5)], float)
    a[mask, 0], a[mask, 1], a[mask, 2] = tgt
    a[mask, 3] = alpha[mask] * k[mask]

    Image.fromarray(a.round().astype(np.uint8)).save(out)
    return int(mask.sum())


if __name__ == '__main__':
    target, out = sys.argv[1], sys.argv[2]
    print(out, 'recoloured pixels:', recolour_clear(SRC, target, out))

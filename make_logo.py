#!/usr/bin/env python3
"""Turn Shauna's logo JPG into web assets: transparent light + dark variants, favicon.

Background removal is done by flood-filling near-white from the image border, NOT by
matching white globally -- the rails contain genuine white highlights that a global
match would punch holes through.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = '/home/user/workspace/uploaded_attachments/a7a54ba589b44777b08095452bfcd438/cleartrack-gap-closest.jpg'
OUT = '/home/user/workspace/cleartrack-storefront/assets'

im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(np.int16)
h, w, _ = a.shape

# --- 1. background = near-white regions connected to the border ---
near_white = a.min(axis=2) > 238
lbl, n = ndimage.label(near_white)
border = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
border.discard(0)
bg = np.isin(lbl, list(border))
print('background pixels: %.1f%% of image' % (100 * bg.mean()))
interior_white = near_white & ~bg
print('interior highlights preserved: %d px' % interior_white.sum())

# --- 2. alpha with a soft edge: ramp through the antialiased band ---
lum = a.mean(axis=2)
alpha = np.clip((248.0 - lum) / 26.0 * 255.0, 0, 255)   # ramp over lum 222..248
alpha[~bg] = 255                                        # anything not background is solid
alpha[bg & (lum > 248)] = 0
# soften: background pixels adjacent to content keep their ramped value
alpha = np.where(bg, np.clip((248.0 - lum) / 26.0 * 255.0, 0, 255), 255).astype(np.uint8)

rgba = np.dstack([a.astype(np.uint8), alpha])

# --- 3. crop to content ---
ys, xs = np.where(alpha > 8)
pad = 6
y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + 1 + pad)
x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + 1 + pad)
crop = rgba[y0:y1, x0:x1]
print('cropped to %dx%d (from %dx%d)' % (crop.shape[1], crop.shape[0], w, h))

light = Image.fromarray(crop, 'RGBA')
TARGET_W = 720
light = light.resize((TARGET_W, round(TARGET_W * light.height / light.width)), Image.LANCZOS)
light.save(f'{OUT}/logo.png', optimize=True)
print('logo.png       %dx%d' % light.size)

# --- 4. dark-theme variant: lighten only the dark NEUTRAL pixels (the "clear"
#        wordmark and the rail steel). Leave the orange and the brown ties alone. ---
#        Only the wordmark band is touched -- recolouring the track produced pale blue
#        streaks with jagged edges, so the illustration is left exactly as she drew it. ---
d = np.asarray(light).astype(np.int16)
rgb, al = d[..., :3], d[..., 3]
sat = rgb.max(axis=2) - rgb.min(axis=2)
lum2 = rgb.mean(axis=2)

band = np.zeros(al.shape, bool)
band[: int(al.shape[0] * 0.42), :] = True      # wordmark sits in the top ~42%
neutral_dark = band & (sat < 46) & (lum2 < 165) & (al > 8)
print('recoloured for dark theme: %d px (%.1f%% of the mark)'
      % (neutral_dark.sum(), 100 * neutral_dark.sum() / max(1, (al > 8).sum())))

# map to a NEUTRAL grey (equal channels) so no blue cast creeps in
target = np.clip(248 - lum2 * 0.30, 0, 255)    # #484854 -> ~#E1E1E1
out = rgb.copy()
for c in range(3):
    out[..., c] = np.where(neutral_dark, target, rgb[..., c])
Image.fromarray(np.dstack([out.astype(np.uint8), al.astype(np.uint8)]), 'RGBA') \
     .save(f'{OUT}/logo-dark.png', optimize=True)
print('logo-dark.png  saved')

print('favicon is drawn as SVG in make_favicon.py -- the photographic track crop\n'
      'was an illegible smudge at 32px.')

#!/usr/bin/env python3
"""Draw the favicon: a simplified version of the track from Shauna's logo.

The photographic track crop was an unreadable smudge at 32px, so this is a flat,
geometric reduction of the same idea -- two rails converging, three ties -- in her
brand orange. Rasterised with Playwright because cairosvg isn't installed.
"""
import asyncio, os
from playwright.async_api import async_playwright

ORANGE = '#F06C24'
OUT = '/home/user/workspace/cleartrack-storefront/assets'

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Cleartrack Apps">
  <rect width="64" height="64" rx="14" fill="{ORANGE}"/>
  <g fill="none" stroke="#fff" stroke-linecap="round">
    <path d="M14 50 C 22 33, 34 22, 53 17" stroke-width="5.4"/>
    <path d="M31 52 C 36 40, 42 31, 54 25" stroke-width="5.4"/>
    <path d="M16.5 44.5 L 33.5 46.5" stroke-width="4.6"/>
    <path d="M22 35.5 L 37.5 38" stroke-width="4.2"/>
    <path d="M29.5 27.5 L 43 30.5" stroke-width="3.8"/>
  </g>
</svg>'''

open(f'{OUT}/favicon.svg', 'w').write(SVG)
print('favicon.svg written')


async def main():
    """Rasterise once at 512 and downsample. Rendering the SVG straight into a 32px
    viewport silently clipped it to the top-left quadrant, so don't do that."""
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 512, 'height': 512}, device_scale_factor=1)
        await pg.set_content(
            '<body style="margin:0;background:transparent">'
            + SVG.replace('width="64" height="64"', 'width="512" height="512"')
            + '</body>')
        await pg.screenshot(path=f'{OUT}/favicon-512.png', omit_background=True)
        await b.close()

    from PIL import Image
    master = Image.open(f'{OUT}/favicon-512.png').convert('RGBA')
    assert master.size == (512, 512), master.size
    # sanity: the rounded square must fill the frame, not sit in one corner
    a = master.split()[3]
    assert a.getpixel((256, 8)) > 200 and a.getpixel((8, 256)) > 200 \
        and a.getpixel((504, 256)) > 200 and a.getpixel((256, 504)) > 200, \
        'favicon does not fill the frame -- SVG scaling is wrong'
    for size in (32, 64, 180):
        master.resize((size, size), Image.LANCZOS).save(f'{OUT}/favicon-{size}.png', optimize=True)
        print(f'favicon-{size}.png  {os.path.getsize(f"{OUT}/favicon-{size}.png")} bytes')
    print(f'favicon-512.png  {os.path.getsize(f"{OUT}/favicon-512.png")} bytes')

asyncio.run(main())

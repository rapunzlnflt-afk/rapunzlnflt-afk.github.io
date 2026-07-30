#!/usr/bin/env python3
"""Screenshot the header and footer in both themes so the logo can be eyeballed."""
import asyncio
from playwright.async_api import async_playwright

URL = 'file:///home/user/workspace/cleartrack-storefront/index.html'
OUT = '/home/user/workspace/shots'
import os; os.makedirs(OUT, exist_ok=True)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vw, theme in [('desk-light', 1280, 'light'), ('desk-dark', 1280, 'dark'),
                                ('mob-light', 375, 'light'), ('mob-dark', 375, 'dark')]:
            pg = await b.new_page(viewport={'width': vw, 'height': 900}, device_scale_factor=2)
            await pg.goto(URL)
            await pg.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
            await pg.wait_for_timeout(500)
            await pg.locator('header.site-head').screenshot(path=f'{OUT}/head-{name}.png')
            await pg.locator('footer.site-foot').screenshot(path=f'{OUT}/foot-{name}.png')
            # which logo file is actually visible, and how big
            info = await pg.evaluate("""() => [...document.querySelectorAll('.logo-head')].map(i => ({
                src: i.currentSrc.split('/').pop(),
                shown: getComputedStyle(i).display !== 'none',
                w: Math.round(i.getBoundingClientRect().width),
                h: Math.round(i.getBoundingClientRect().height),
                natural: i.naturalWidth + 'x' + i.naturalHeight,
                complete: i.complete
            }))""")
            print(name, info)
            await pg.close()
        await b.close()

asyncio.run(main())

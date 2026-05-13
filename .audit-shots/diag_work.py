"""Re-capture /work/ at desktop without any scrolling, to isolate any rendering issue."""
from playwright.sync_api import sync_playwright
from pathlib import Path

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto("https://opedal.tech/work/", wait_until="networkidle")
    page.wait_for_timeout(800)
    page.screenshot(path=str(OUT / "desktop_work_clean_above_fold.png"), full_page=False)

    # Also probe the nav and h1 positions
    info = page.evaluate("""
      () => {
        const nav = document.querySelector('.site-nav');
        const h1 = document.querySelector('h1');
        const intro = document.querySelector('.section-intro');
        return {
          nav: nav ? {
            top: Math.round(nav.getBoundingClientRect().top),
            bottom: Math.round(nav.getBoundingClientRect().bottom),
            height: Math.round(nav.getBoundingClientRect().height),
            position: getComputedStyle(nav).position,
            zIndex: getComputedStyle(nav).zIndex,
            displayInDOMOrder: Array.from(document.body.children).map(c => c.tagName + '.' + c.className),
          } : null,
          h1: h1 ? {
            text: h1.textContent.trim(),
            top: Math.round(h1.getBoundingClientRect().top),
            bottom: Math.round(h1.getBoundingClientRect().bottom),
            marginBottom: getComputedStyle(h1).marginBottom,
            paddingBottom: getComputedStyle(h1).paddingBottom,
          } : null,
          intro: intro ? {
            text: intro.textContent.trim().slice(0, 80),
            top: Math.round(intro.getBoundingClientRect().top),
            bottom: Math.round(intro.getBoundingClientRect().bottom),
            marginTop: getComputedStyle(intro).marginTop,
          } : null,
          h1IntroOverlap: h1 && intro ? Math.round(h1.getBoundingClientRect().bottom - intro.getBoundingClientRect().top) : null,
        };
      }
    """)
    import json
    print(json.dumps(info, indent=2))
    browser.close()

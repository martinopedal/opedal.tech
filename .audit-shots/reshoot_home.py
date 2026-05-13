"""Re-screenshot live homepage post-portrait-removal + /about/ for re-evaluation."""
from playwright.sync_api import sync_playwright
from pathlib import Path

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    # Bypass CDN cache with a query string
    page.goto("https://opedal.tech/?cb=" + str(__import__('time').time()), wait_until="networkidle")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "v2_desktop_home_full.png"), full_page=True)
    page.screenshot(path=str(OUT / "v2_desktop_home_above_fold.png"), full_page=False)

    info = page.evaluate("""() => {
      const sections = Array.from(document.querySelectorAll('section, header, main > *'));
      const h2s = Array.from(document.querySelectorAll('h2')).map(h => h.textContent.trim());
      const eyebrows = Array.from(document.querySelectorAll('.section-label, .eyebrow')).map(e => e.textContent.trim());
      const aboutSec = document.getElementById('about');
      const aboutInfo = aboutSec ? {
        height: Math.round(aboutSec.getBoundingClientRect().height),
        text: aboutSec.textContent.trim().slice(0, 200),
        innerHTML_head: aboutSec.outerHTML.slice(0, 400),
      } : null;
      return { h2s, eyebrows, aboutInfo };
    }""")
    import json; print(json.dumps(info, indent=2))

    page_m_ctx = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3, is_mobile=True, has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    page_m = page_m_ctx.new_page()
    page_m.goto("https://opedal.tech/?cb2=" + str(__import__('time').time()), wait_until="networkidle")
    page_m.wait_for_timeout(1200)
    page_m.screenshot(path=str(OUT / "v2_mobile_home_full.png"), full_page=True)
    page_m.screenshot(path=str(OUT / "v2_mobile_home_above_fold.png"), full_page=False)

    browser.close()

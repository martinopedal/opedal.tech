"""Capture /about/ live + confirm homepage state."""
from playwright.sync_api import sync_playwright
from pathlib import Path

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

with sync_playwright() as p:
    browser = p.chromium.launch()

    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.goto("https://opedal.tech/about/", wait_until="networkidle")
    page.wait_for_timeout(800)
    page.screenshot(path=str(OUT / "desktop_about_full.png"), full_page=True)
    about_info = page.evaluate("""() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      return {
        title: document.title,
        h1: document.querySelector('h1')?.textContent.trim(),
        images: imgs.map(i => ({ src: i.src, alt: i.alt, w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height) })),
        sectionsCount: document.querySelectorAll('section').length,
        docHeight: document.documentElement.scrollHeight,
      };
    }""")
    print("=== /about/ ===")
    import json; print(json.dumps(about_info, indent=2))

    # Re-confirm: does the homepage STILL have a portrait + About section?
    page.goto("https://opedal.tech/", wait_until="networkidle")
    page.wait_for_timeout(800)
    home_info = page.evaluate("""() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      const aboutSec = document.querySelector('#about, section.about, .about-section');
      return {
        portraitOnHome: imgs.length > 0 ? imgs.map(i => ({ src: i.src, alt: i.alt, w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height) })) : 'no images',
        hasAboutSection: !!aboutSec,
        aboutSectionId: aboutSec?.id || null,
        sectionIds: Array.from(document.querySelectorAll('section, header')).map(s => s.id || s.tagName.toLowerCase() + (s.className ? '.' + s.className : '')),
      };
    }""")
    print("\n=== / (homepage) ===")
    print(json.dumps(home_info, indent=2))

    # Also: does Lovell's About page have the portrait moved into it? Re-take fresh shots.
    ctx_m = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3, is_mobile=True, has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    page_m = ctx_m.new_page()
    page_m.goto("https://opedal.tech/about/", wait_until="networkidle")
    page_m.wait_for_timeout(800)
    page_m.screenshot(path=str(OUT / "mobile_about_full.png"), full_page=True)

    browser.close()

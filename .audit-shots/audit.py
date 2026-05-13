"""Vision audit for opedal.tech — screenshots + gap measurement."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(r"C:\git\opedal.tech\.audit-shots")
OUT.mkdir(exist_ok=True)

DESKTOP = {"width": 1440, "height": 900, "device_scale_factor": 1}
MOBILE = {
    "width": 390,
    "height": 844,
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1"
    ),
}

URLS = {
    "home": "https://opedal.tech/",
    "cv": "https://opedal.tech/cv/",
    "work": "https://opedal.tech/work/",
    "blog": "https://opedal.tech/blog/",
}


def measure_cv_gaps(page):
    """Return rich gap metrics for every consecutive pair of .cv-section blocks."""
    return page.evaluate(
        """
        () => {
          const sections = Array.from(document.querySelectorAll('.cv-section'));
          const data = sections.map((el) => {
            const r = el.getBoundingClientRect();
            const cs = getComputedStyle(el);
            const h2 = el.querySelector('h2');
            return {
              h2: h2 ? h2.textContent.trim() : '(no h2)',
              top: Math.round(r.top + window.scrollY),
              bottom: Math.round(r.bottom + window.scrollY),
              height: Math.round(r.height),
              marginTop: cs.marginTop,
              marginBottom: cs.marginBottom,
              paddingTop: cs.paddingTop,
              paddingBottom: cs.paddingBottom,
              display: cs.display,
              position: cs.position,
            };
          });
          const gaps = [];
          for (let i = 0; i < data.length - 1; i++) {
            gaps.push({
              from: data[i].h2,
              to: data[i + 1].h2,
              gapPx: data[i + 1].top - data[i].bottom,
              fromMarginBottom: data[i].marginBottom,
              toMarginTop: data[i + 1].marginTop,
            });
          }
          // Also measure the container and what sits between sections.
          const container = document.querySelector('.cv-page .container');
          const containerStyle = container ? getComputedStyle(container) : null;
          return {
            sectionCount: sections.length,
            sections: data,
            gaps,
            container: containerStyle ? {
              display: containerStyle.display,
              gap: containerStyle.gap,
              rowGap: containerStyle.rowGap,
              padding: containerStyle.padding,
            } : null,
          };
        }
        """
    )


def cv_dom_between(page, from_h2, to_h2):
    """Walk the DOM between two cv-section elements; report what's in the gap."""
    return page.evaluate(
        """
        ([fromH2, toH2]) => {
          const sections = Array.from(document.querySelectorAll('.cv-section'));
          const fromIdx = sections.findIndex(s => s.querySelector('h2')?.textContent.trim() === fromH2);
          const toIdx = sections.findIndex(s => s.querySelector('h2')?.textContent.trim() === toH2);
          if (fromIdx === -1 || toIdx === -1) return { error: `not found: ${fromH2} / ${toH2}` };
          const from = sections[fromIdx];
          const to = sections[toIdx];
          const between = [];
          let cur = from.nextSibling;
          while (cur && cur !== to) {
            if (cur.nodeType === 1) {
              const r = cur.getBoundingClientRect();
              between.push({
                tag: cur.tagName,
                cls: cur.className,
                outerHTML_head: cur.outerHTML.slice(0, 200),
                heightPx: Math.round(r.height),
              });
            } else if (cur.nodeType === 3) {
              const t = cur.nodeValue.trim();
              if (t) between.push({ text: t.slice(0, 80) });
            }
            cur = cur.nextSibling;
          }
          // Parent of from and to
          return {
            fromParent: from.parentElement?.tagName + '.' + from.parentElement?.className,
            toParent: to.parentElement?.tagName + '.' + to.parentElement?.className,
            sameParent: from.parentElement === to.parentElement,
            between,
            fromLastChildHeight: from.lastElementChild ? Math.round(from.lastElementChild.getBoundingClientRect().height) : null,
            fromLastChildMarginBottom: from.lastElementChild ? getComputedStyle(from.lastElementChild).marginBottom : null,
            toFirstChildMarginTop: to.firstElementChild ? getComputedStyle(to.firstElementChild).marginTop : null,
          };
        }
        """,
        [from_h2, to_h2],
    )


def home_metrics(page):
    """Extract homepage portrait + section info."""
    return page.evaluate(
        """
        () => {
          const imgs = Array.from(document.querySelectorAll('img'));
          const portrait = imgs.find(i =>
            /portrait|martin|opedal|me\\.|profile|headshot/i.test(i.src + ' ' + (i.alt || ''))
          ) || imgs[0];
          const sections = Array.from(document.querySelectorAll('section'));
          return {
            title: document.title,
            portrait: portrait ? {
              src: portrait.src,
              alt: portrait.alt,
              width: portrait.naturalWidth,
              height: portrait.naturalHeight,
              renderedWidth: Math.round(portrait.getBoundingClientRect().width),
              renderedHeight: Math.round(portrait.getBoundingClientRect().height),
              top: Math.round(portrait.getBoundingClientRect().top + window.scrollY),
            } : null,
            allImages: imgs.map(i => ({ src: i.src, alt: i.alt })).slice(0, 10),
            sections: sections.map(s => ({
              id: s.id,
              cls: s.className,
              top: Math.round(s.getBoundingClientRect().top + window.scrollY),
              height: Math.round(s.getBoundingClientRect().height),
            })),
            docHeight: Math.round(document.documentElement.scrollHeight),
            viewportWidth: window.innerWidth,
          };
        }
        """
    )


def color_audit(page):
    """Scan all rendered elements for blue-ish hues (R<G or R<B sharply)."""
    return page.evaluate(
        """
        () => {
          const offenders = [];
          const seen = new Set();
          function parseRgb(s) {
            const m = s.match(/rgba?\\(([^)]+)\\)/);
            if (!m) return null;
            const parts = m[1].split(',').map(x => parseFloat(x.trim()));
            return { r: parts[0], g: parts[1], b: parts[2], a: parts[3] ?? 1 };
          }
          function isBluey(c) {
            if (!c || c.a < 0.1) return false;
            // Skip near-grey (R==G==B within 12)
            const max = Math.max(c.r, c.g, c.b), min = Math.min(c.r, c.g, c.b);
            if (max - min < 15) return false;
            // Skip near-black
            if (max < 30) return false;
            // Bluey: blue dominant
            return c.b > c.r + 25 && c.b > c.g + 10;
          }
          const all = document.querySelectorAll('*');
          for (const el of all) {
            const cs = getComputedStyle(el);
            const props = ['color', 'backgroundColor', 'borderTopColor', 'outlineColor'];
            for (const p of props) {
              const v = cs[p];
              const c = parseRgb(v);
              if (isBluey(c)) {
                const key = el.tagName + '.' + el.className + ':' + p + ':' + v;
                if (!seen.has(key)) {
                  seen.add(key);
                  offenders.push({
                    tag: el.tagName,
                    cls: (el.className || '').toString().slice(0, 80),
                    prop: p,
                    value: v,
                    snippet: (el.outerHTML || '').slice(0, 120),
                  });
                  if (offenders.length > 20) return offenders;
                }
              }
            }
          }
          return offenders;
        }
        """
    )


def a11y_quick(page):
    """Quick a11y sweep: img alt missing, low-contrast warning candidates, focusables."""
    return page.evaluate(
        """
        () => {
          const imgs = Array.from(document.querySelectorAll('img'));
          const missingAlt = imgs.filter(i => !i.hasAttribute('alt')).map(i => i.src);
          const emptyAlt = imgs.filter(i => i.getAttribute('alt') === '').map(i => i.src);
          const links = Array.from(document.querySelectorAll('a'));
          const targetBlankNoRel = links
            .filter(a => a.target === '_blank' && !/noopener/.test(a.rel))
            .map(a => a.href);
          // Tap-target audit (mobile): links/buttons rendered <40x40
          const tapTargets = Array.from(document.querySelectorAll('a, button')).map(el => {
            const r = el.getBoundingClientRect();
            return { text: (el.textContent || '').trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) };
          }).filter(t => t.w > 0 && t.h > 0 && (t.w < 40 || t.h < 40));
          return { missingAlt, emptyAlt, targetBlankNoRel, smallTapTargets: tapTargets.slice(0, 20) };
        }
        """
    )


def shoot(page, label, full=True):
    path = OUT / f"{label}.png"
    page.screenshot(path=str(path), full_page=full)
    return str(path)


results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()

    # --- Desktop pass ---
    ctx = browser.new_context(
        viewport={"width": DESKTOP["width"], "height": DESKTOP["height"]},
        device_scale_factor=DESKTOP["device_scale_factor"],
    )
    page = ctx.new_page()

    for name, url in URLS.items():
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(800)
        # Force lazy-loaded images by scrolling
        page.evaluate(
            "() => new Promise(res => { const step = () => { window.scrollBy(0, 600); if (window.scrollY + window.innerHeight >= document.body.scrollHeight) res(); else setTimeout(step, 80); }; step(); })"
        )
        page.wait_for_timeout(500)
        page.evaluate("() => window.scrollTo(0, 0)")
        page.wait_for_timeout(300)
        results[f"desktop_{name}_full"] = shoot(page, f"desktop_{name}_full", full=True)
        results[f"desktop_{name}_above_fold"] = shoot(page, f"desktop_{name}_above_fold", full=False)

        if name == "cv":
            results["cv_desktop_metrics"] = measure_cv_gaps(page)
            results["cv_desktop_dom_certs_to_speaking"] = cv_dom_between(page, "Certifications", "Speaking")
            results["cv_desktop_dom_speaking_to_oss"] = cv_dom_between(page, "Speaking", "Open Source")
            # Take a focused crop of the certs→speaking→oss band
            try:
                certs = page.locator(".cv-section:has(h2:text('Certifications'))").first
                oss = page.locator(".cv-section:has(h2:text('Open Source'))").first
                certs_box = certs.bounding_box()
                oss_box = oss.bounding_box()
                if certs_box and oss_box:
                    clip_top = max(0, certs_box["y"] - 20)
                    clip_bottom = oss_box["y"] + oss_box["height"] + 20
                    page.evaluate(f"window.scrollTo(0, {clip_top - 80})")
                    page.wait_for_timeout(200)
                    # Re-measure with viewport coords
                    band = page.evaluate(
                        """() => {
                          const sec = Array.from(document.querySelectorAll('.cv-section'));
                          const certs = sec.find(s => s.querySelector('h2')?.textContent.trim() === 'Certifications');
                          const oss = sec.find(s => s.querySelector('h2')?.textContent.trim() === 'Open Source');
                          const cr = certs.getBoundingClientRect();
                          const or_ = oss.getBoundingClientRect();
                          return { x: 0, y: cr.top - 20, width: window.innerWidth, height: (or_.bottom + 20) - (cr.top - 20) };
                        }"""
                    )
                    if band["height"] > 0 and band["height"] < 4000:
                        page.screenshot(
                            path=str(OUT / "desktop_cv_band_certs_to_oss.png"),
                            clip={
                                "x": max(0, band["x"]),
                                "y": max(0, band["y"]),
                                "width": min(1440, band["width"]),
                                "height": band["height"],
                            },
                        )
            except Exception as e:
                results["cv_band_clip_error"] = str(e)

        if name == "home":
            results["home_desktop_metrics"] = home_metrics(page)
            results["home_desktop_blue_audit"] = color_audit(page)
            results["home_desktop_a11y"] = a11y_quick(page)

        if name == "blog":
            results["blog_desktop_blue_audit"] = color_audit(page)

    ctx.close()

    # --- Mobile pass ---
    ctx_m = browser.new_context(
        viewport={"width": MOBILE["width"], "height": MOBILE["height"]},
        device_scale_factor=MOBILE["device_scale_factor"],
        is_mobile=MOBILE["is_mobile"],
        has_touch=MOBILE["has_touch"],
        user_agent=MOBILE["user_agent"],
    )
    page_m = ctx_m.new_page()

    for name, url in URLS.items():
        page_m.goto(url, wait_until="networkidle", timeout=45000)
        page_m.wait_for_timeout(800)
        page_m.evaluate(
            "() => new Promise(res => { const step = () => { window.scrollBy(0, 600); if (window.scrollY + window.innerHeight >= document.body.scrollHeight) res(); else setTimeout(step, 80); }; step(); })"
        )
        page_m.wait_for_timeout(500)
        page_m.evaluate("() => window.scrollTo(0, 0)")
        page_m.wait_for_timeout(300)
        results[f"mobile_{name}_full"] = shoot(page_m, f"mobile_{name}_full", full=True)
        results[f"mobile_{name}_above_fold"] = shoot(page_m, f"mobile_{name}_above_fold", full=False)

        if name == "cv":
            results["cv_mobile_metrics"] = measure_cv_gaps(page_m)
        if name == "home":
            results["home_mobile_metrics"] = home_metrics(page_m)
            results["home_mobile_a11y"] = a11y_quick(page_m)

    ctx_m.close()
    browser.close()

# Write a single JSON report
report_path = OUT / "report.json"
report_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
print(f"Wrote {report_path}")
print(f"Screenshots in {OUT}")

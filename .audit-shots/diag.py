"""Pinpoint the source of the apparent gap — measure inner whitespace of cv-section blocks."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto("https://opedal.tech/cv/", wait_until="networkidle")
    page.wait_for_timeout(800)

    out = page.evaluate(
        """
        () => {
          const targets = ['Certifications', 'Speaking', 'Open Source'];
          const sections = Array.from(document.querySelectorAll('.cv-section'));
          const result = {};
          for (const name of targets) {
            const sec = sections.find(s => s.querySelector('h2')?.textContent.trim() === name);
            if (!sec) { result[name] = { error: 'not found' }; continue; }
            const r = sec.getBoundingClientRect();
            const cs = getComputedStyle(sec);
            // Walk all descendants and find min top + max bottom of any element with non-zero size
            let minTop = Infinity, maxBot = -Infinity;
            let lastVisibleEl = null;
            const desc = sec.querySelectorAll('*');
            for (const el of desc) {
              const rr = el.getBoundingClientRect();
              if (rr.width > 0 && rr.height > 0) {
                if (rr.top < minTop) minTop = rr.top;
                if (rr.bottom > maxBot) {
                  maxBot = rr.bottom;
                  lastVisibleEl = el;
                }
              }
            }
            const children = Array.from(sec.children).map(ch => {
              const rr = ch.getBoundingClientRect();
              const ccs = getComputedStyle(ch);
              return {
                tag: ch.tagName,
                cls: ch.className,
                top: Math.round(rr.top + window.scrollY),
                bottom: Math.round(rr.bottom + window.scrollY),
                height: Math.round(rr.height),
                marginTop: ccs.marginTop,
                marginBottom: ccs.marginBottom,
                paddingTop: ccs.paddingTop,
                paddingBottom: ccs.paddingBottom,
              };
            });
            result[name] = {
              section_top: Math.round(r.top + window.scrollY),
              section_bottom: Math.round(r.bottom + window.scrollY),
              section_height: Math.round(r.height),
              section_paddingTop: cs.paddingTop,
              section_paddingBottom: cs.paddingBottom,
              section_marginBottom: cs.marginBottom,
              first_visible_top: Math.round(minTop + window.scrollY),
              last_visible_bottom: Math.round(maxBot + window.scrollY),
              last_visible_tag: lastVisibleEl ? lastVisibleEl.tagName + '.' + lastVisibleEl.className : null,
              top_inner_whitespace: Math.round(minTop + window.scrollY) - Math.round(r.top + window.scrollY),
              bottom_inner_whitespace: Math.round(r.bottom + window.scrollY) - Math.round(maxBot + window.scrollY),
              children,
            };
          }
          return result;
        }
        """
    )
    print(json.dumps(out, indent=2))

    # Also: capture a tighter band — visible end of certs to visible start of speaking
    band = page.evaluate(
        """
        () => {
          const find = (name) => Array.from(document.querySelectorAll('.cv-section')).find(s => s.querySelector('h2')?.textContent.trim() === name);
          function maxBot(el) {
            let m = -Infinity;
            for (const e of el.querySelectorAll('*')) {
              const r = e.getBoundingClientRect();
              if (r.width > 0 && r.height > 0 && r.bottom > m) m = r.bottom;
            }
            return m;
          }
          function minTop(el) {
            let m = Infinity;
            for (const e of el.querySelectorAll('*')) {
              const r = e.getBoundingClientRect();
              if (r.width > 0 && r.height > 0 && r.top < m) m = r.top;
            }
            return m;
          }
          const certs = find('Certifications');
          const speak = find('Speaking');
          const oss = find('Open Source');
          return {
            certs_visible_bottom: Math.round(maxBot(certs) + window.scrollY),
            speak_visible_top: Math.round(minTop(speak) + window.scrollY),
            speak_visible_bottom: Math.round(maxBot(speak) + window.scrollY),
            oss_visible_top: Math.round(minTop(oss) + window.scrollY),
            cs_gap_visible: Math.round(minTop(speak) + window.scrollY) - Math.round(maxBot(certs) + window.scrollY),
            so_gap_visible: Math.round(minTop(oss) + window.scrollY) - Math.round(maxBot(speak) + window.scrollY),
          };
        }
        """
    )
    print("\nVISIBLE-CONTENT-TO-VISIBLE-CONTENT gaps:")
    print(json.dumps(band, indent=2))

    browser.close()

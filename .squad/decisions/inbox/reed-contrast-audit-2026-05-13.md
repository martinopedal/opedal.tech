# Reed — Live contrast audit

**By:** Reed (Visual Designer)  
**What:** Two surgical token fixes to address "hard to read" user feedback — bump text-dim luminance and flip btn-primary text to dark.  
**Why:** User feedback: colors hard to read. WCAG audit revealed one AA failure (btn-primary white-on-terracotta at 3.12:1) and text-dim hovering just below AAA.

## Pages audited

- **https://martinopedal.github.io/opedal.tech/** — Homepage renders fine for primary text. Hero tagline, section intros, card descriptions, and contact copy all use `--color-text-dim` on either `--color-bg` or `--color-surface`. Visually readable but on the edge—especially on alt-bg sections.
- **https://martinopedal.github.io/opedal.tech/blog/** — Blog hero tagline in text-dim. Blog cards show dates and excerpts in text-dim on surface. Same pattern.
- **https://martinopedal.github.io/opedal.tech/cv/** — CV page heavy with muted body copy (summary, job descriptions, engagement text). All use text-dim. Surface cards dominate.
- **https://martinopedal.github.io/opedal.tech/work/** — Similar pattern to homepage—work row descriptions in text-dim on surface cards.

**Key observation:** The site uses `--color-text-dim` extensively for body copy in cards and sections. On `--color-surface` (alt-bg sections), the current 6.35:1 ratio is AA-compliant but not AAA. User perception of "hard to read" is likely caused by this borderline contrast on the warmer, lighter surface background.

## Failure list (current palette)

| Pair | BG | FG | Ratio | WCAG |
|------|----|----|------:|------|
| text on bg | #14110f | #e8e2d8 | 14.60:1 | ✅ AAA |
| text on surface | #1f1b18 | #e8e2d8 | 13.27:1 | ✅ AAA |
| text-dim on bg | #14110f | #a39d92 | 6.98:1 | ✅ AA (borderline AAA) |
| **text-dim on surface** | #1f1b18 | #a39d92 | 6.35:1 | ✅ AA, ❌ AAA |
| accent on bg | #14110f | #d97757 | 6.02:1 | ✅ AA |
| accent on surface | #1f1b18 | #d97757 | 5.48:1 | ✅ AA |
| accent-hover on bg | #14110f | #e59677 | 8.02:1 | ✅ AAA |
| accent-hover on surface | #1f1b18 | #e59677 | 7.30:1 | ✅ AAA |
| **white on accent (btn-primary)** | #d97757 | #ffffff | 3.12:1 | ❌ **FAIL AA** |

**Critical failures:**
1. `.btn-primary` white text on terracotta fails AA (3.12:1 < 4.5:1) — this is the "View open source" and "Email me" CTA buttons.
2. `--color-text-dim` on `--color-surface` at 6.35:1 is technically AA-passing but sits below AAA, contributing to perceived difficulty.

## Proposed token changes

| Token | Before | After | New ratio on bg | New ratio on surface |
|-------|--------|-------|----------------:|---------------------:|
| `--color-text-dim` | #a39d92 | **#ada79d** | 7.87:1 (AAA ✅) | 7.16:1 (AAA ✅) |
| `.btn-primary { color }` | #ffffff | **#14110f** | n/a | n/a |
| `.btn-primary:hover { color }` | #ffffff | **#14110f** | n/a | n/a |

**Rationale:**
- **`#ada79d`** is the minimum brightness bump that achieves AAA (7:1+) on both bg and surface while preserving the warm taupe character. Visually indistinguishable warmth shift, measurable legibility gain.
- **`#14110f`** (existing `--color-bg`) as btn-primary text flips the button to dark-on-terracotta, achieving 6.02:1 contrast. This maintains the warm Architect Charcoal feel (dark brown on terracotta = classic warm aesthetic) without requiring a new token.

## Implementation notes for Kranz

Update `src/styles/global.css`:

### 1. Token change (line 17)
```css
/* Before */
--color-text-dim:    #a39d92;  /* Muted text */

/* After */
--color-text-dim:    #ada79d;  /* Muted text — AAA on both bg and surface */
```

### 2. Button text color (lines 216-226)
```css
/* Before */
.btn-primary {
  background: var(--accent);
  color: #fff;
  border: 1px solid var(--accent);
}

.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: #fff;
}

/* After */
.btn-primary {
  background: var(--accent);
  color: var(--color-bg);  /* Dark warm text for AA compliance */
  border: 1px solid var(--accent);
}

.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--color-bg);  /* Keep dark on hover too */
}
```

### Summary of CSS changes
- Line 17: `#a39d92` → `#ada79d`
- Line 218: `color: #fff;` → `color: var(--color-bg);`
- Line 225: `color: #fff;` → `color: var(--color-bg);`

## Non-color findings (spot-check)

1. **Section markers (`.section-label`)** — 0.7rem at 600 weight with 0.15em letter-spacing on warm charcoal. Legible but tight. Consider bumping to 0.75rem or 650 weight if user feedback persists.

2. **Prose line-height** — `.prose` at 1.8 line-height is generous and readable. No change needed.

3. **Code blocks** — System mono stack at 0.875rem. JetBrains Mono not yet loaded (per decisions.md, self-hosted woff2 planned). Once added, verify weight 400–500 renders crisply on dark backgrounds.

4. **Button hit-area** — `.btn` padding of `0.65rem 1.4rem` creates adequate 44px+ touch target vertically. Acceptable.

5. **Focus-visible ring** — No explicit `:focus-visible` styles found in global.css. Browsers apply default outline (typically blue). Consider adding `outline: 2px solid var(--accent); outline-offset: 2px;` to `:focus-visible` for better cohesion with the terracotta palette. (Non-blocking for this audit.)

6. **Mobile nav background** — Line 724 uses `rgba(13, 17, 23, 0.98)` (GitHub dark) instead of the Architect Charcoal bg. Minor visual inconsistency on mobile nav dropdown. Consider `rgba(20, 17, 15, 0.98)` to match.

## Verification

After implementation, all text pairs will pass WCAG AA minimum. `--color-text-dim` and `--color-text` will both hit AAA on both background surfaces. The terracotta accent remains recognizably terracotta (no hue shift). The warm Architect Charcoal direction is preserved.

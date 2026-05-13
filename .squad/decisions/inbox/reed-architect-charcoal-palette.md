# Architect Charcoal Palette — Reed verification (2026-05-13)

**By:** Reed (Visual Designer), verifying palette implementation

## Palette specification

| Token               | Hex       | Role                     |
| ------------------- | --------- | ------------------------ |
| `--color-bg`        | `#14110f` | Warm near-black base     |
| `--color-surface`   | `#1f1b18` | Elevated surface         |
| `--color-text`      | `#e8e2d8` | Primary text (warm)      |
| `--color-text-dim`  | `#a39d92` | Secondary/muted text     |
| `--color-border`    | `#2a2520` | Borders                  |
| `--color-accent`    | `#d97757` | Terracotta accent        |
| `--color-accent-hover` | `#e59677` | Lighter terracotta    |

## WCAG AA contrast verification

| Pair                          | Ratio    | Requirement | Pass |
| ----------------------------- | -------- | ----------- | ---- |
| Text `#e8e2d8` on bg `#14110f`   | 14.60:1  | ≥4.5:1      | ✓    |
| Accent `#d97757` on bg `#14110f` | 6.02:1   | ≥3:1 (UI)   | ✓    |
| Text-dim `#a39d92` on bg `#14110f` | 6.98:1 | ≥4.5:1      | ✓    |

All contrast ratios exceed WCAG AA requirements.

## Peer site research

Reviewed:
- **Linear.app**: Cool dark (#0F0F0F), purple/violet accents, high contrast
- **leerob.io**: Minimalist dark, sparse accent use, neutral warm grays

Chosen direction: warm near-black (not cool gray) with terracotta accent. Rationale:
1. Warmth distinguishes from Microsoft/Azure cold blues
2. Matches "datacenters + breweries" tactile identity
3. Terracotta is distinctive without being harsh
4. Senior-architect signal: warm, grounded, organic

## Implementation locations

- `src/styles/global.css` `:root` block (lines 12-37)
- `src/layouts/BaseLayout.astro` `<meta name="theme-color" content="#14110f">`
- `src/styles/global.css` nav background: `rgba(20, 17, 15, 0.92)`

## Legacy compatibility

CSS uses both new `--color-*` tokens and legacy aliases (`--bg`, `--accent`, etc.) for backward compatibility. Future palette swaps: update the 8 `--color-*` variables only.

# Language border colors and section marker scale

**By:** Kranz (PR B redesign session)  
**Date:** 2026-05-13  
**Context:** Adding language-specific colored left borders to repo rows and section marker styling.

## Language border colors added to global.css

Implemented as `.repo-row.lang-{language}` classes with 2px left border colors:

- **terraform**: `#844fba` (purple)
- **python**: `#3fb950` (green)
- **powershell**: `#5391fe` (blue)
- **typescript**: `#3178c6` (blue)
- **javascript**: `#f1e05a` (yellow)
- **go**: `#00add8` (cyan)
- **csharp**: `#178600` (green)
- **all**: `var(--accent)` (GitHub blue)

## Section marker styling

- `.section-label`: mono font, 0.7rem, 0.15em letter-spacing, uppercase, muted color
- `section h2`: 0.75rem padding-bottom, 1px solid border-bottom using `var(--border)`

# Scribe — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal.
- **My role:** silent custodian of `.squad/**`. Orchestration log per spawn, session log per session, decisions inbox merge, cross-agent history updates, archive sweeps when files exceed thresholds.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## File hygiene

- `.gitattributes` declares `merge=union` for `.squad/decisions.md`, `.squad/agents/*/history.md`, `.squad/log/**`, `.squad/orchestration-log/**`. This means concurrent appends from any branch merge cleanly without manual conflict resolution.
- ISO 8601 UTC timestamps in all filenames I create.
- Commit messages via `git commit -F /tmp/scribe-msg.txt` (or the PowerShell equivalent on Windows) — never inline through shell quoting.
- Co-author trailer on every commit.

## Learnings

(append as work progresses)

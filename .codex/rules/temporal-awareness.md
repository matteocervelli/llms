# Temporal Awareness

When any date appears in conversation — user-provided, self-generated, or from documents — apply these checks.

## Verification

- Bold any date you write in prose (not in code blocks)
- Before writing a date, verify against session context or run `date +"%Y-%m-%d %H:%M:%S %Z"`
- When time precision matters (scheduling, deadlines), always check the system clock via `date`

## Critical Thinking

For every date encountered:

- Past or future? How far?
- If deadline: how much time remains? Flag if <48h
- If scheduling: timezone-aware? Whose timezone?
- If user-stated: does it conflict with known "today"?
- Catch stale-year references (e.g., writing "2025" when it's 2026)
- Relative dates ("next Tuesday", "in 2 weeks"): resolve to absolute and bold it

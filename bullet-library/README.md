# Standardized Bullet Library

This folder is a derived working library for resume tailoring.

Canonical source files stay untouched:

- `/Users/chris/2026 Resumes/CANONICAL - Chris Tallent Resume - CTO.docx`
- `/Users/chris/2026 Resumes/CANONICAL - Chris Tallent Resume - Principal Engineer.docx`
- `/Users/chris/2026 Resumes/CANONICAL - 2025 Chris Resume All Bullets.docx`

Use this library to speed up tailoring and copy-fitting in Word without rewriting bullets from scratch.

## Files

- `standardized-bullets.yaml`: curated bullet families with `short`, `medium`, and `long` variants

## Default Workflow

1. Create a new application folder by copying the correct base `.docx`.
2. Start with `medium` bullets by default.
3. If the document runs long, swap from `medium` to `short` before touching Word margins or paragraph spacing.
4. Use `long` only for high-priority roles where the extra context materially improves fit.
5. Keep the canonical `.docx` files unchanged; edit only the copied resume in `Send To/...`.

## Track Guidance

- `cto`: org leadership, product partnership, delivery systems, budgeting, security/compliance, transformation
- `director`: multi-team execution, DevOps, reliability, platform improvements, cross-functional alignment
- `principal`: architecture depth, modernization, AI integration, reliability, developer experience

## Copy-Fit Order

Use the same compression order every time:

1. Tighten the summary.
2. Swap one or two bullets from `medium` to `short`.
3. Trim the core-skills section.
4. Remove the lowest-value page-two bullet.
5. Only then make last-mile formatting changes in Word.

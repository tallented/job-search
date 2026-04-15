# Evidence Library

This folder is the detailed fact store for resume tailoring.

Use it for information that is:
- true and resume-relevant
- richer than a normal resume bullet
- validated through QA / discussion
- likely to be reused across future resumes, cover letters, recruiter screens, and interviews

## Intended Structure

Each role or company should get a dedicated Markdown file containing:
- scope summary
- org structure and reporting context
- architecture ownership
- security/compliance ownership
- stakeholder and customer interaction
- concrete dates, counts, and named systems
- provenance notes such as `validated in chat on YYYY-MM-DD`

## How It Fits With The Existing Resume Assets

- `evidence-library/`
  - detailed fact store and provenance
- `bullet-library/standardized-bullets.yaml`
  - curated resume-ready `short` / `medium` / `long` variants promoted from validated facts
- `CANONICAL - 2025 Chris Resume All Bullets.docx`
  - human-readable bullet bank, not the place for long-form notes or QA transcripts

## Workflow

1. Capture new validated facts here first.
2. Promote the highest-value reusable facts into `standardized-bullets.yaml`.
3. Only add to the canonical all-bullets doc when the fact is worth keeping as a plain resume bullet.
4. Keep dates, counts, org sizes, and named tools exact where known.
5. If a fact is inferred or approximate, say so explicitly.

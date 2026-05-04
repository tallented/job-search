# First Draft Rules

Apply these rules before showing Chris the first draft of any tailored resume.

The goal is that the first review pass should already clear recurring fit, voice, and visual-quality issues.

## 1. Visual QA Must Be Word-Based

Do not rely on Markdown alone for first-draft copy-fit review.

Before presenting a first draft:

1. Open the `.docx` in Word, or inspect a PDF render / graphical snapshot of the actual page layout.
2. Review the summary, core skills, and all bullets for bad line wraps.
3. Fix copy-fit problems by tightening or slightly expanding text before changing layout settings.

Also verify these formatting basics in the actual Word layout:

- heading text should use only a single consistent shade of blue
- body text should be `Calibri` at either `11` or `10.5`
- section headings may be `Calibri 12`
- the name line may be `Calibri 14`
- the horizontal rule below the top heading must remain a single continuous line, not wrap or break

## 2. Single-Word And Jagged-Line Rule

Avoid jagged wrapping in summary lines, core skills rows, and bullets.

- If a single trailing word drops to the next line, either:
  - trim enough words so it returns to the prior line, or
  - add at least `2-3` words so the wrapped line looks intentional.
- If two words spill over and create a visibly jagged line, evaluate whether adding `1-2` more words produces a cleaner wrap.
- Prefer wording fixes over margin, font-size, or paragraph-spacing changes.
- Do not strip out mandate, ownership scope, product/architecture context, stakeholder level, or differentiating AI/security/compliance detail just to eliminate a short final line.
- If a cleanup pass makes a bullet flatter or more generic, restore the stronger `medium` or `long` variant first and solve the wrap with a different wording change.
- After rendering a resume PDF, run the local OCR helper when available:
  - `python3 scripts/check_resume_wraps.py <resume.pdf>`
- Treat OCR flags as a targeted review queue, then confirm the actual rendered page visually before deciding on the final wording fix.
- If Word PDF export is stale or unreliable, fall back to a graphical preview of the actual `.docx` page layout (for example Quick Look thumbnails or Word page screenshots) and do not trust extracted text alone.

## 3. First-Draft Voice Audit

Run an `AI voice vs Chris voice` pass before review.

- Avoid generic hand-waving.
- Avoid overly clever, compressed, or artificial phrasing.
- Avoid consultant-style abstractions when a concrete phrase is available.
- Never use `sits at the intersection of`.
- Summary and Core Skills are the highest-risk sections for AI-sounding language and must be checked first.

Preferred style:

- concrete over abstract
- plainspoken over polished
- specific over clever
- factual scope over vague self-description

## 4. Page-Two Fill Rule

Do not leave a large block of blank space at the bottom of page 2.

- Target no more than `1-2` blank lines at the end of page 2.
- If space remains, add bullets in this order:
  1. bullets that directly strengthen fit for the job req
  2. bullets that strengthen the core narrative for the target lane
  3. bullets that show versatility, breadth, or scale without diluting the role fit
- Added bullets must be real signal, not filler.

Good sources:

- local prior variants
- `bullet-library/standardized-bullets.yaml`
- `evidence-library/`
- stronger adjacent submitted variants

## 5. No Page 3

The first draft should not spill to a third page.

- If page 3 appears, tighten content before changing formatting.
- Preferred order of compression:
  1. summary
  2. core skills rows
  3. swap `medium` bullets to `short`
  4. remove lowest-value page-two bullet
  5. only then consider minor Word layout adjustments

## 6. Team-Scale Number Rule

Avoid using the exact `6 -> 35` scale phrasing by default.

- Prefer wording like:
  - `built out engineering from a small initial team into a four-team organization`
  - `built out the engineering organization into four agile teams`
- Use exact numeric scale only when:
  - the job req explicitly emphasizes org-size thresholds, or
  - the number materially strengthens fit for that specific role.
- Do not lead a current-role section with the org-size bullet unless scale is the main point of the target role.

## 7. Leadership Resume Header Rule

For leadership-track resumes, visible role headers should be factual and not create title friction.

- Do not use `Principal Engineer` in a visible role header on leadership resumes unless it was truly the title or the resume is explicitly targeting a principal role.
- Prefer accurate variants such as:
  - `Chief Technology Officer & Lead Architect`
  - `Fractional CTO & Lead Architect`

## 8. Earlier Roles Dating Rule

When using an `Earlier Roles` section:

- omit dates by default
- keep it compact
- use it to show breadth, not to reopen the full chronology

Also omit graduation years unless there is a specific reason to include them.

## 9. Summary Rule

The summary should be specific and grounded, not evaluative or slogan-like.

- Prefer `Experience spans...`, `Built...`, `Led...`, `Delivered...`
- Avoid vague lines like:
  - `Strong on...`
  - `operator mindset`
  - `practical judgment` when it sounds hand-wavy
  - `responsible AI adoption` if a more concrete phrase is available

If a summary sentence sounds defensible but vague, rewrite it in terms of scope, systems, or outcomes.

## 10. Core Skills Rule

Core Skills rows should be concrete and easy to scan.

- Avoid fuzzy labels like:
  - `Operational Rigor`
  - `CRM-Integrated Workflows`
  - `AI-Assisted SDLC`
- Prefer clearer phrasing like:
  - `Delivery Discipline`
  - `Lead Management Workflows`
  - `AI-Assisted Development`
- Review each row visually in Word so wraps look intentional, not jagged.

## 11. First-Bullet Framing Rule

For current or most relevant roles, the first bullet should usually establish one or more of:

- platform or business scope
- delivery ownership
- architecture ownership
- cross-functional or stakeholder scope

Do not default the first bullet to a team-size fact if a better scope-setting bullet is available.

## 12. Repetition Rule

Read each role section for repeated lead verbs, repeated sentence openings, and obvious word reuse.

- Avoid sequences like `Built ... / Built ... / Built ...` unless there is a strong reason to keep them.
- Vary bullet openings when repetition starts to sound mechanical.
- Check summaries and Core Skills for repeated abstractions or reused filler words.
- Fix repetition with natural phrasing, not thesaurus-driven wording.

## 13. Punctuation Rule

Do not use em dashes in resume copy.

- Treat em dashes as disallowed across all resumes.
- Prefer commas, parentheses, vertical bars, colons, or a regular hyphen depending on context.
- If a date range needs punctuation, use either a regular hyphen or an en dash consistently within that document.
- Check `Earlier Roles`, education lines, and summary sentences specifically, because em dashes tend to creep in there.

## 14. Preferred First-Draft Workflow

Before handing over a first draft:

1. Tailor the top third to the role.
2. Reorder the experience bullets for fit.
3. Run the voice audit.
4. Run the Word/PDF visual wrap audit.
5. Run the OCR wrap checker on the rendered PDF when available and fix flagged jagged lines.
6. Compare the top role bullets against the strongest canonical or prior variant to make sure wrap cleanup did not flatten the story.
7. Fill page-two whitespace with high-signal bullets if needed.
8. Confirm the file is `2` pages, not `3`.
9. Then present it for review.

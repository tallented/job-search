# AGENTS.md (Resume Tailoring Workspace)

This workspace contains Chris Tallent's base resumes and many job-specific variants. The primary recurring task is to tailor a resume for a specific job requisition and company, targeting one of these tracks:

- CTO / Head of Engineering / VP Engineering (exec + org leadership + delivery + security/compliance)
- Engineering Manager / Senior Engineering Manager / Director (team leadership, platform/devex/reliability, execution)
- Principal / Distinguished Engineer (architecture depth, hands-on delivery, distributed systems, AI-integration)

## Source Of Truth Files

Start from these base resumes and bullet banks in the local workspace. Prefer editing copied `.docx` working files and keep the canonical sources unchanged:

- `/Users/chris/2026 Resumes/CANONICAL - Chris Tallent Resume - CTO.docx`
- `/Users/chris/2026 Resumes/CANONICAL - Chris Tallent Resume - Engineering Manager.docx`
- `/Users/chris/2026 Resumes/CANONICAL - Chris Tallent Resume - Principal Engineer.docx`
- `/Users/chris/2026 Resumes/CANONICAL - 2025 Chris Resume All Bullets.docx`

Primary local supporting material:

- `/Users/chris/2026 Resumes/bullet-library/standardized-bullets.yaml` (curated bullet families with `short`, `medium`, and `long` variants)
- `/Users/chris/2026 Resumes/bullet-library/README.md` (copy-fit and usage guidance)
- `/Users/chris/2026 Resumes/evidence-library/` (detailed validated fact store by role/company; use for richer context than normal resume bullets)
- `/Users/chris/2026 Resumes/Send To/` (active company/role-specific working folders)
- `/Users/chris/2026 Resumes/Version - CTO/` and `/Users/chris/2026 Resumes/Version - Engineering/` (local working variants)
- `/Users/chris/2026 Resumes/Submitted/` (submitted/finalized output)
- `/Users/chris/2026 Resumes/Old Versions/`, `/Users/chris/2026 Resumes/prior revisions/`, `/Users/chris/2026 Resumes/ChatGPT/` (legacy local wording and structure variants)

Legacy reference material still exists outside this folder and may be used when helpful, but local workspace copies should be preferred first:

- `/Users/chris/My Drive/Documents/Resume/Chris/2025 Resumes/Send To/`
- `/Users/chris/My Drive/Documents/Resume/Chris/2025 Resumes/Old Versions/`
- `/Users/chris/My Drive/Documents/Resume/Chris/2025 Resumes/prior revisions/`
- `/Users/chris/My Drive/Documents/Resume/Chris/2025 Resumes/ChatGPT/`

## Current Workspace Layout

Use the local `2026 Resumes` folder as the default working tree.

- `Send To/`: active tailoring work by company/role
- `Submitted/`: finalized versions that have already been sent
- `Version - CTO/`, `Version - Engineering/`: reusable local working branches
- `bullet-library/`: normalized bullet variants for copy-fit work
- `searches/`: dated search review queues, watchlists, direct-company sweeps, recruiter target notes, and dispatch-decision matrices
- `_resume_text/`: extracted plaintext cache for fast search
- `_resume_text_archive/`: archived cache snapshots
- `scripts/`: helper scripts for maintenance and cache refresh
- `Old Versions/`, `prior revisions/`, `ChatGPT/`: historical local references

## Resume Header Location

For the resume header location, prefer:

- `Cincinnati Metro Area`

This is the default user-facing location label for the resume header because it is more recognizable than `Fort Thomas, KY` while staying geographically accurate enough for resume use.

Use the actual city/state only where precision matters:

- application forms: `Fort Thomas, KY`
- role history locations: keep the factual company/role location as written

## Earlier Roles Exclusion

Do not use `Tallented Software LLC` as an Earlier Roles item. The experience is older and its useful signals can be shown with more recent, stronger roles such as ACS, Proven Edge, Pitchstone, Glamhive, Lela, Fidelity, or dunnhumby.

## Local Text Cache (For Fast Search)

There is an extracted plaintext cache of the `.docx` files at:

- `/Users/chris/2026 Resumes/_resume_text/`

Use it to quickly search for prior bullets, role-specific phrasing, and metrics across past submissions.

## Wrap-Check Automation

For first-draft visual QA, prefer checking rendered pages instead of relying on extracted text alone.

Available local helper:

- `/Users/chris/2026 Resumes/scripts/check_resume_wraps.py`

Typical workflow:

1. Export the current resume `.docx` to PDF from Word.
2. Run:

```sh
cd "/Users/chris/2026 Resumes"
python3 scripts/check_resume_wraps.py "Send To/<...>/resume.pdf"
```

3. Use the flagged short final lines as a targeted review queue for likely `1-2` word or jagged wraps.
4. Fix wording first, then re-render the PDF and rerun the checker.

Notes:

- The OCR wrap checker is heuristic, not authoritative.
- Always confirm the rendered page visually before accepting or rejecting a suggested fix.
- Prefer trimming or slightly expanding the sentence over layout changes.
- The local helper depends on `pdftoppm` and `tesseract`.
- If Word PDF export is stale, use a graphical preview of the `.docx` itself (for example Quick Look thumbnails or Word screenshots) as the visual source of truth until a fresh PDF render is available.

If you add/modify `.docx` files in this workspace, refresh the local cache:

```sh
cd "/Users/chris/2026 Resumes"
mkdir -p _resume_text
find . -type f -iname "*.docx" ! -name "~$*" -print0 | while IFS= read -r -d '' f; do
  out="_resume_text/${f#./}.txt"
  mkdir -p "$(dirname "$out")"
  /usr/bin/textutil -convert txt -stdout "$f" > "$out"
done
```

## Evidence Library (Detailed Fact Store)

Use the local evidence library for validated facts that are richer than a normal resume bullet:

- `/Users/chris/2026 Resumes/evidence-library/`

Keep detailed scope, reporting structure, architecture ownership, security/compliance ownership, dates, counts, named tools, and provenance notes there.

Workflow:

1. Capture new validated facts in the evidence library first.
2. Promote reusable resume-ready variants into `/Users/chris/2026 Resumes/bullet-library/standardized-bullets.yaml`.
3. Keep `/Users/chris/2026 Resumes/CANONICAL - 2025 Chris Resume All Bullets.docx` as a human-readable bullet bank, not a dumping ground for long-form notes or QA transcripts.
4. If a fact is approximate, mark it clearly in the evidence library before promoting it into resume copy.

## Word-First Resume Construction

Default resume construction should be Word-first, not Markdown-first.

1. Pick the correct canonical Word resume (`CTO`, `Engineering Manager`, or `Principal Engineer`) based on target track.
2. Copy that canonical `.docx` into the target `Send To/<Company - Role>/` folder and use the copied file as the formatting shell.
3. Preserve the canonical Word layout, spacing, heading hierarchy, and overall visual structure unless there is a deliberate formatting reason to change it.
4. Build the content by selecting bullet variants from `/Users/chris/2026 Resumes/bullet-library/standardized-bullets.yaml` and `/Users/chris/2026 Resumes/CANONICAL - 2025 Chris Resume All Bullets.docx`, instead of rewriting from scratch every time.
5. Use `medium` bullets by default. Promote to `long` only when the extra context materially improves fit. Demote to `short` before touching margins, font size, or paragraph spacing.
6. The copied canonical `.docx` is the master document. Do not replace it with a newly generated Word file by default.
7. Use `draft.md` only when a major rewrite is easier to review in text first, then transfer the approved content into the copied Word resume.
8. If automation is used, it should operate on the copied canonical `.docx` in place so margins, fonts, spacing, and pagination stay as close to the canonical file as possible.
9. If line-wrapping issues appear in Word, prefer content tightening (summary, bullet length, core skills) before layout tweaks.

### Core Skills Composition

Treat Core Skills sections as composable source material, not fixed blocks that must be copied wholesale.

- It is acceptable to assemble a new Core Skills block by pulling rows from multiple canonical or prior resume variants.
- It is also acceptable to pull individual skills from different rows when the target requisition calls for a more precise mix.
- Keep the final block coherent, scannable, and ordered to the req rather than preserving the source order.
- Do not pad with broad or generic skills just because they existed in a source block.
- Preserve the Word document structure Chris is using for review. If summary variants or skills variants have been grouped together in the `.docx`, keep those comparison blocks adjacent unless explicitly asked to restructure them.

### Prepared Bullets QA Workflow

Use `/Users/chris/2026 Resumes/CANONICAL - Prepared Bullets.docx` as the reviewed, Word-formatted prepared-bullets source and `/Users/chris/2026 Resumes/CANONICAL - Prepared Bullets.md` as the paired text source when practical.

When Chris flags prepared-bullets line-length or wording issues:

- Do not immediately overwrite the canonical prepared-bullets document unless Chris explicitly asks for source updates.
- First create or update a QA comparison document under `/Users/chris/2026 Resumes/temp/`, using the prepared-bullets `.docx` as the style shell so margins, fonts, and bullet wrapping are meaningful.
- In the QA comparison document, keep the original wording in black and put the current suggested replacement in blue under a `Suggested` label.
- Chris may edit the blue `Suggested` lines in place. Treat those edited blue lines as the current candidate replacements.
- Use additional candidate blocks only when Chris wants to compare multiple alternatives; otherwise avoid clutter.
- For half-line bullets, expand only with high-signal wording. If added words are filler, leave the bullet unchanged or keep the variant only in the QA document.
- For 1-3 word trailing lines, prefer compression unless a materially stronger longer version is available.
- When Chris approves a candidate, promote it back into both `CANONICAL - Prepared Bullets.docx` and `CANONICAL - Prepared Bullets.md` where the matching source entry exists.
- If a bullet is identified as weak, incorrect, or duplicate, remove it from the canonical prepared-bullets source rather than keeping it as a ready variant.
- After modifying prepared-bullets `.docx` files, run structural validation (`unzip -t`), refresh `_resume_text`, and use Quick Look or a targeted render check when possible. Do not use Word automation that closes unrelated documents.

## Resume Edit Change Control

Default to surgical edits unless Chris explicitly asks for a broader rewrite, line-balance pass, or structural consolidation.

### Edit Modes

**Surgical Edit Mode** is the default for requested wording changes.

- Touch only the requested text or the immediate sentence needed to preserve grammar and truth.
- Do not rewrite adjacent bullets, merge bullets, reorder sections, rebalance the whole resume, or change unrelated language.
- Render after the change if the edited text can affect wrapping or pagination.
- If the requested edit creates a line-wrap or page-fill regression, make the smallest local wording adjustment possible or report the tradeoff before broadening scope.

**Line-Balance Mode** applies only when Chris explicitly asks to fix jagged lines, orphan lines, or visual line balance.

- Start from the current rendered PDF as the baseline.
- Fix only the bullets or sections identified as visually problematic unless another regression is directly caused by the fix.
- For each changed bullet, choose the smallest viable action: tighten to one clean line, expand with real signal to a fuller line, or merge with an adjacent bullet only when the combined meaning is natural.
- Do not treat `0` OCR wrap-check flags as sufficient. Visually compare the rendered pages against the baseline.
- The pass fails if it improves a local line ending but makes page-two fill, section density, role fit, or voice worse overall.

**Structural Rewrite / Consolidation Mode** applies only when intentionally reshaping a section or replacing multiple bullets.

- Make a dated backup before editing.
- State the intended bullet deletes, merges, and additions before changing the document when practical.
- Track page budget: if the edit removes several lines, either preserve page fill with equal or stronger signal or explicitly accept the whitespace as a tradeoff.
- Render and compare against the baseline page images before accepting the change.
- If the result is not better overall, revert the structural pass rather than layering more fixes on top.

### Regression Gate

Before accepting any resume iteration:

- Check the extracted text diff or a focused before/after text comparison to confirm the edit scope stayed within the selected mode.
- Render a fresh PDF using the Word helper and verify the PDF text reflects the current `.docx`.
- Visually inspect page images, not just OCR output.
- Confirm page count did not regress and page-two whitespace did not materially increase unless explicitly accepted.
- Confirm no untouched section gained new obvious jagged final lines.
- Confirm the change did not weaken truth, role fit, voice, or the strongest quantified/current-role bullets.

Priority order for tradeoffs:

1. Truth and role fit.
2. No page 3.
3. No major page-two whitespace regression.
4. No obvious jagged or orphan final lines.
5. Chris voice and readability.
6. Minor aesthetic preferences.

## Temporary Files

- Create future temporary, intermediate, render, OCR, and diagnostic files either in the current resume's target folder or under `/Users/chris/2026 Resumes/temp`.
- Avoid `/private/tmp`, `/tmp`, or other external temp folders unless a specific tool requires them and there is no practical workspace-local alternative.
- Prefer clearly named temp files that include the company/role or task context so they can be reviewed and cleaned up safely later.

## Microsoft Word Automation Safety

Multiple resume sessions may be open at once, and Chris may be actively editing a different document in Word. Other Codex sessions may also have Word documents open for different job reqs at the same time.

Hard rules:

- Never run AppleScript or automation that closes every Word document, such as `repeat while (count of documents) > 0`, `close document 1`, or similar bulk-close loops.
- Never quit, force-quit, restart, or otherwise kill Microsoft Word as a cleanup step unless Chris explicitly asks for that.
- Never close a Word document unless it is the specific target document for the current task and the script opened that document itself.
- Never use `saving no` on a document that might have been opened or edited by Chris.
- Treat unexpected, duplicate, untitled, temporary-looking, or "phantom" Word documents as potentially belonging to Chris or another Codex session. Do not close them, discard them, or clean them up from Word. Limit cleanup to files on disk that the current session created and can positively identify.
- Do not assume `active document` is the target document. Identify the target by path or exact file name before exporting, saving, or closing.
- Before opening or rendering a `.docx` after automated revisions, validate the package structure:

```sh
cd "/Users/chris/2026 Resumes"
python3 scripts/validate_docx_package.py "<input.docx>"
```

- If package validation reports `ERROR`, do not open the file in Word; repair from the last known-good `.docx` or compare the modified OOXML first. Warnings are review items, not automatic blockers.
- When exporting PDF from Word, prefer the dedicated helper app wrapper:

```sh
cd "/Users/chris/2026 Resumes"
word-render-helper/render_with_swift_word_helper.sh "<input.docx>" "<output.pdf>" "<stable-slot-name>"
```

- The helper app is `/Users/chris/2026 Resumes/word-render-helper/SwiftResumeWordRenderHelper.app`, which Chris has granted macOS privacy access for Word rendering. It copies the target `.docx` into `/Users/chris/2026 Resumes/temp/word-render-scratch`, exports through Microsoft Word, and copies the PDF back to the requested output path.
- Use a stable, job-specific slot name for each concurrent resume session, for example `coderpad`, `cyara`, or `trueml`. Do not reuse the same slot across parallel sessions. The wrapper uses the slot for both Word scratch filenames and helper control files (`current-job-<slot>.txt` / `current-result-<slot>.txt`).
- The wrapper serializes Word renders with `word-render-helper/render.lock`. Microsoft Word is a single GUI application, so sessions may use distinct slots but should not automate Word simultaneously.
- The wrapper launches a GUI app through macOS Launch Services (`open`). In sandboxed Codex sessions, run the wrapper with escalated/approved GUI-launch permissions. Do not interpret a sandboxed `open` failure as proof that the helper executable is missing.
- Do not rebuild the Swift helper as a routine fix. Rebuild only when the helper source, Info.plist, or bundle structure has intentionally changed, or when Chris explicitly asks for a rebuild. The helper is ad-hoc signed; rebuilding changes its code hash and can trigger macOS privacy prompts again.
- If macOS prompts that `SwiftResumeWordRenderHelper` would like to access data from other apps, stop and report it. The Swift helper should not write into another app's container; repeated prompts likely mean an old helper build or stale render path is still being used.
- If Word shows `Grant File Access` for `/Users/chris/2026 Resumes/temp/word-render-scratch`, Chris may need to select the specific `<slot>.docx` scratch file if the picker does not allow selecting the folder. Do not change render paths; the helper keeps each slot's scratch DOCX path stable and overwrites it in place when possible.
- If the executable check passes but `open` reports `kLSNoExecutableErr`, treat it as Launch Services/sandbox state first. Retry the wrapper with escalation/approved GUI-launch permission. If it still fails after escalation, stop and report the exact error instead of repeatedly rebuilding or falling back to AppleScript.
- Do not use random render-copy filenames to work around grant-access prompts. If the helper or Word blocks, times out, crashes, or triggers a new permission prompt, stop and report that state instead of creating alternate render copies.
- Use `/Users/chris/2026 Resumes/scripts/export_docx_to_pdf.sh` only as a fallback when the helper is unavailable or explicitly inappropriate.
- Keep any remaining Word-opened render copies in either the same target resume folder as the working `.docx` or under `/Users/chris/2026 Resumes/temp`.
- Do not create or open Word render copies in `/private/tmp`, Word's app container, or other external temp folders because macOS privacy controls may repeatedly prompt Chris to Grant Access or approve other-app data access.
- If a non-helper render copy is unavoidable, name it clearly in the target folder or `/Users/chris/2026 Resumes/temp`, export the PDF to the relevant resume folder when possible, and clean up the render copy later only after confirming it was not edited by Chris.
- If Word already has the target document open, leave it open after export.
- If the target document is open with unsaved edits, either export it without closing it or ask Chris before taking any action that could discard changes.

## DOCX XML Edit Safety

Word can report "unreadable content" even when `unzip`, Quick Look, and `textutil` appear to accept a `.docx`. Avoid broad XML rewrites that reserialize whole Word parts and change schema ordering.

- Do not use `xml.etree.ElementTree` to parse and rewrite entire `word/document.xml` or `word/styles.xml` for production resume files.
- Prefer Word's own save/export path, a known-safe helper, or narrow string/minidom edits that preserve original XML ordering.
- For `CANONICAL - Prepared Bullets.docx`, prefer rebuilding from `CANONICAL - Prepared Bullets.md` into the clean prepared-bullets shell rather than surgically editing the existing `.docx` package.
- After any `.docx` package edit, keep a backup, run `unzip -t`, verify `textutil` extraction, and do a graphical render check. If Word later reports unreadable content, restore from backup or rebuild from the paired `.md` source instead of recovering and saving the prompted Word copy.

## First Draft Rules

Before presenting a first draft resume for review, apply:

- `/Users/chris/2026 Resumes/FIRST_DRAFT_RULES.md`

This file defines the mandatory first-pass checks for:

- Word/PDF visual QA
- single-word and jagged-line cleanup
- AI-voice vs Chris-voice cleanup
- page-two whitespace management
- no-page-3 enforcement
- team-scale phrasing defaults
- leadership-header defaults
- earlier-roles dating defaults
- summary / core-skills phrasing discipline

## Resume Language Guardrails

Avoid overusing `workflow` / `workflows` as generic resume filler.

Use `workflow` only when it refers to a real business process, workflow engine, orchestration path, approval flow, or application workflow. If the sentence is really about systems, integrations, controls, agents, tooling, data extraction, operating models, finance rules, or business processes, use the more precise term.

Common replacements:

- `Payment / Credit Workflows` -> `Payment / Credit Processes`, `Payment / Credit Systems`, or `Payment / Credit Rules`
- `Governed AI Workflows` -> `Governed AI Agents`, `Governed AI Tooling`, or `Governed AI Controls`
- `bi-directional workflows` -> `bi-directional integrations`, `data sync`, or `cross-system coordination`
- `AI document workflows` -> `AI document extraction`, `document data extraction`, or `AI-assisted document processing`
- `consumer finance workflows` -> `consumer finance strategies`, `consumer finance processes`, or `consumer lending rules`
- `dealer finance workflows` -> `dealer finance rules`, `dealer finance processes`, or `dealer finance operations`

When editing a resume draft, scan for `workflow` and `workflows` before final review. If there are more than a few uses, rewrite most of them with precise domain language.

## Bullet Variant Workflow

When tailoring from the bullet library:

1. Start with the role-appropriate canonical Word resume.
2. Pull in `medium` bullets for the highest-priority roles and themes first.
3. Reorder bullets to match the job description before rewriting wording.
4. Use `long` bullets sparingly for halo/signature achievements and only where the added detail helps the target role.
5. Use `short` bullets to solve copy-fit and dangling-line problems before making visual formatting changes in Word.
6. Prefer swapping between existing bullet variants over writing new bullets unless the job requires a materially different framing.
7. Keep the bullet families truthful and consistent across tracks; change emphasis and compression, not the underlying facts.

## Default Tailoring Workflow

When given a new job requisition:

1. Locate the closest prior variant in local `Send To/` for the same company or a similar role/seniority. Reuse its tone and any already-targeted bullets. Check legacy external folders only if the local workspace does not already contain a good analogue.
2. Choose the correct base resume (`CTO`, `Engineering Manager`, or `Principal Engineer`) as the backbone, copy that canonical `.docx`, and use the copied Word file as the starting template.
3. Read the job description and extract:
   - Must-have responsibilities (ownership scope, org size, stakeholder level)
   - Must-have technical domains (cloud, platform, security, AI, etc.)
   - Keywords likely used for ATS (platform, reliability, SOC2/ISO, etc.)
4. Apply "Halo first 30 seconds" (see below) and re-author the top 1/3 first:
   - Headline (credible positioning + 2-3 differentiators)
   - Professional Summary (2-4 sentences, specific to the role)
   - Core Skills (assembled from rows or individual skills across variants as needed, reordered to mirror the req; avoid long lists that dilute signal)
5. Experience bullets:
   - Start from bullet-library `medium` variants by default.
   - Promote only a few bullets to `long` when they materially increase fit.
   - Compress from `medium` to `short` before changing Word formatting.
   - Prefer outcome/metric-first bullets (cost, cycle time, uptime, accuracy, retention).
   - Reorder bullets within each role to match the req.
   - Cut anything that does not support the target role; keep to 1-2 pages.
   - Avoid repeating the same technology stack in multiple bullets unless the req calls for it.
6. Consistency checks:
   - Dates/locations consistent across versions.
   - Verb tense consistent (past for past roles; present for current).
   - No unsupported claims (do not invent metrics).
   - Do not let the visible headline or title simply mirror the job requisition unless Chris has held that title or the wording is directly backed by validated experience. Prefer truthful positioning such as `Technology Executive`, `CTO`, `Engineering Executive`, `Product Engineering`, `Platform Engineering`, or `AI Modernization` over an unheld exact target title.
   - Remove role-misaligned details (e.g., too much IC depth for CTO, or too much org narrative for Principal) unless the req explicitly wants that hybrid.
   - Do not use em dashes in resume copy; prefer commas, parentheses, vertical bars, colons, or a regular hyphen.
   - When referring to formal board-level communication, prefer `Board of Directors` over generic `board` unless the sentence intentionally refers to board-level communication as a category.
7. Update the application tracker in the local NocoDB instance at `http://localhost:8085`:
   - Base: `Job Search`
   - Table: `Applications`
   - Add a new record as soon as a tailored resume folder is created.
   - Default pre-submission status is `CREATED`.
   - Fill at least `Company`, `Status`, `Created`, `Title`, the job `Link`, and `Resume Folder`.
   - Preferred creation path: `/Users/chris/2026 Resumes/job-tracker/create-application.sh`
   - Preferred update path for status and follow-up changes: `/Users/chris/2026 Resumes/job-tracker/update-application.sh`
   - `/Users/chris/2026 Resumes/scripts/new_resume.sh` now creates the `Send To/...` folder and also adds the `CREATED` NocoDB row by default unless `SKIP_TRACKER=1`.
   - The archived Excel workbook at `/Users/chris/2026 Resumes/bak/2026 Job Search.xlsx` is legacy import/export only and should not be used as the live tracker.

## Halo vs Horn (First 30 Seconds)

The resume's first "screen" should create a Halo effect (strong competence signal) and avoid early Horn triggers (confusion, clutter, low-signal details).

Reference narrative and components live here:

- `/Users/chris/My Drive/Documents/Resume/Chris/2025 Resumes/Halo Effect.md`

Default Halo anchors to lead with (choose the 2-3 most relevant per role/company):

- Technical co-founder story: Glamhive from wireframes to MVP; won Seattle Angel Conference VII (2015).
- Modernization + execution story: Drive It Now/ACS legacy PHP modernization; Agile; delivered MVP for NADA conference.
- Enterprise rigor: 6 years at Fidelity on 401k tools (scale, compliance, governance).
- Current differentiation: practical AI integration for developer productivity and product strategy (Bedrock/Textract/RAG + AI-assisted modernization).

Practical resume edits that usually increase Halo and reduce Horn:

- Put the strongest quantified outcome or credible signal in the first 2-3 bullets under the current/most relevant role.
- Avoid leading with long tool lists; keep "Core Skills" tight and ordered to the req.
- If the target is leadership, surface org/building-operating-rhythm and delivery-system bullets early; if the target is IC, surface architecture/scale/availability and hands-on bullets early.

## Output Conventions

For each new application, prefer creating a new folder under `Send To/`:

- `Send To/<YYYYMMDD - Company - Target Role>/`

Date-prefix folders by default so new work is clearly separated from older attempts for the same company. Example:

- `Send To/20260330 - Bonzo Inc - CTO/`

If the company name alone is sufficient for clarity, a shorter form is acceptable:

- `Send To/20260330 - Bonzo Inc/`

Store:

- `... job description.txt` (the exact posting text)
- Tailored resume master in `.docx`, named like `Chris Tallent Resume - <Company> - <Role>.docx`
- Optional tightened Word variants when copy-fitting, e.g. `... - Tight.docx`
- Optional exported PDF after the Word version is final
- Optional: a reviewable draft in Markdown for iteration, e.g. `draft.md` (useful when large rewrites are needed)

Folder lifecycle:

- Keep in `Send To/` while the application is in progress, under review, or not yet submitted.
- Before moving a submitted application from `Send To/` to `Submitted/`, clean up transient Word copies. Retain only the final submitted `.docx` for that resume or cover letter; remove local backup, pre-pass, rebuilt, unreadable-repair, and other temporary `.docx` variants unless the user explicitly asks to preserve them.
- Once the application is actually submitted, move the whole folder into `Submitted/`.
- Do not overwrite or reuse an old company folder for a new application cycle; create a new date-prefixed folder instead.
- If there are multiple attempts for the same company over time, the date prefix is the source of truth for recency.

## Application Tracker

Track active and submitted applications in:

- local NocoDB tracker at `http://localhost:8085`
- base: `Job Search`
- table: `Applications`

Also maintain the human-readable priority queue at:

- `/Users/chris/2026 Resumes/Queue.md`

Use NocoDB as the system of record for application status, dates, links, salary, and resume folders. Use `Queue.md` as the current at-a-glance operating queue: what to work next, what is deferred, what is on hold for company-coherence reasons, and what was recently submitted or closed. Update `Queue.md` whenever a search reprioritizes roles, a role is submitted, a role closes, or Chris explicitly defers a role. Each active queue item should include a `Freshness` line when available. Front-load the age signal in bold so it is easy to scan, for example `**Posted 4d ago via LinkedIn**`, `**Crawled 5d ago via NoDesk**`, or `**Posted date n/a**`; then include supporting detail such as `official Ashby page live`, `freshness signals vary`, or `Indeed alert evaluated on YYYY-MM-DD`.

Legacy archive only:

- `/Users/chris/2026 Resumes/bak/2026 Job Search.xlsx`

Populate as much as is known at creation time:

- `Company`
- `Status`
- `Created`
- `Submitted`
- `Last Contact Date`
- `Title`
- `Type`
- `Location`
- `Salary`
- `Next Steps`
- `Listing Source`
- `Ref Number`
- `Link`
- `Resume Folder`
- `Resume Decision`

Status convention:

- `CREATED`: tailored resume folder exists, but not yet submitted
- Update to the later funnel state after submission or recruiter progress

Concurrency rule:

- NocoDB is the writable system of record.
- The archived `.xlsx` workbook is for legacy reference/import only; do not keep it in sync as part of normal resume work.

Helper workflow:

- To create a tracker row directly, use `/Users/chris/2026 Resumes/job-tracker/create-application.sh`.
- To update an existing row, use `/Users/chris/2026 Resumes/job-tracker/update-application.sh`.
- Preferred locator for updates is `Resume Folder`.
- `update-application.sh` also supports row `Id`, or `Company + Title` when that match is unique.
- For status transitions like `SUBMITTED` or `REJECTED`, prefer the updater script over manual SQLite edits.
- Use `Resume Decision` to capture the dispatch strategy, for example `Customize | Canonical EM | strong: prepared; comp clears floor`, `Light customize | Canonical Principal | strong IC fit`, `Canonical CTO direct | acceptable`, or `Hold/skip | stale or below floor`.
- The tracker helpers support this field with `--resume-decision`.

## Role Emphasis Heuristics

- CTO/VP/Head of Eng: org building, execution systems, budgeting, security/compliance, cross-functional leadership, transformation, strategy.
- Engineering Manager / Senior Engineering Manager / Director: team leadership, delivery systems, platform/devex, incident response/SLOs, operational excellence, stakeholder alignment.
- Principal/Distinguished: architecture, distributed systems, hands-on execution, reliability/perf, AI integration, migration/modernization.

Keep the resume "truthful but maximally aligned": same underlying achievements, different ordering and wording depending on the target.

## Opportunity Triage Rubric

Current search is not prestige-only. The priority order is:

1. Income continuity
2. Strong full-time trajectory if possible
3. Fractional / interim as valid bridge income
4. AI-forward positioning where it improves future leverage
5. Remote first, then regional hybrid/travel, then broader relocation only if needed

### Apply Now

Bias toward `Apply Now` when most of these are true:

- Compensation meets the current cash floor or plausibly negotiates to it
- Work model is remote, remote with occasional travel, or in-region hybrid
- Fit is strong or a credible stretch
- Title / scope helps trajectory or at least does not damage it
- Company and role look serious and reasonably well-defined

### Apply If Time

Use `Apply If Time` when:

- Compensation is unclear but might still work
- Fit is stretchy but defensible
- Company is decent but not ideal
- Role is not a perfect trajectory move but could still generate income or interviews
- Tailoring cost is moderate and the company has not already been "burned" with a weak prior application

### Skip

Use `Skip` when any of these are true:

- Compensation is clearly below floor
- Work model is currently unacceptable
- Fit is weak enough that the application is likely noise
- Company / posting looks chaotic, exploitative, or unserious
- Role would push the search into the wrong lane
- Applying would likely burn a company that may have a better-fit role later

### Work Model Rules

Current work model preference order:

- Best: remote
- Good: remote with planned travel (for example monthly)
- Acceptable now: hybrid in Cincinnati metro, Columbus, Dayton, Louisville, Indianapolis, or Cleveland
- Apply-now bias: for strong Cincinnati metro hybrid/on-site roles, apply if compensation and fit are plausible; local in-office friction is acceptable if it supports income continuity.
- Later fallback: broader relocation if the pipeline remains weak

### Fractional Rules

Fractional / interim work is valid and should be positively weighted when:

- The role has real ownership, not just advisory status theater
- Weekly capacity is meaningful enough to matter
- The engagement alone or in combination can contribute materially toward the cash floor
- It strengthens positioning around AI-assisted engineering, agentic coding adoption, architecture, cloud, DevOps, security, or 0→1 platform work

Avoid weak fractional roles that are:

- vague advisor arrangements
- tiny hourly gigs
- low-leverage staff augmentation
- founder therapy disguised as consulting

### AI Positioning Rules

Positive weight should be given to roles where Chris can truthfully sell:

- AI-assisted modernization
- RAG / embeddings / vector search
- document extraction / LLM workflows
- MCP / tool integration
- agentic admin or operational workflows
- AI coding agent adoption for team leverage

### Company History Rule

- If it is a company Chris has not applied to before and the fit is at least a plausible stretch, bias toward applying.
- If it is a company Chris has already applied to, avoid mixed-signal submissions unless the roles are clearly coherent with each other.

### Fast Decision Shortcut

For quick triage, ask:

1. Can this plausibly meet the cash need?
2. Is the work model acceptable right now?
3. Is the fit at least defensible?
4. Does it help trajectory, or at least not hurt it?
5. Is the company / role serious enough to justify the time?

If the answers are mostly yes:

- `Apply Now`

If mixed:

- `Apply If Time`

If mostly no:

- `Skip`

## Recurring Search Playbook

Use this when building the top of the funnel. The goal is to maintain steady opportunity volume without over-tailoring every role before it earns the time.

Primary channel inventory:

- `/Users/chris/2026 Resumes/Search-Sites.md`

### Browser Search Automation

For browser-based job searches, use the dedicated debug-enabled Chrome launcher:

```sh
cd "/Users/chris/2026 Resumes"
scripts/launch_resume_chrome.sh about:blank
```

Use `scripts/launch_resume_chrome.sh --status` to verify the setup. Expected healthy state:

- debug listener is up on port `9224`
- profile is `/tmp/codex-resume-chrome`
- `/Users/chris/Library/Application Support/Google/Chrome/DevToolsActivePort` exists and points to the live browser id
- `chrome-devtools-mcp` can list the `about:blank` page

Do not manually launch normal Chrome or assume port `9222`. The launcher suppresses first-run/default-browser/sign-in prompts for the automation profile, writes the DevTools port file expected by the MCP, and avoids using Chris's normal browser profile. If automation cannot connect, first close the automation Chrome window, rerun the launcher, then check `--status` before trying other browser-control approaches.

### Default Search Cadence

- Daily or near-daily:
  - LinkedIn
    - Use the saved LinkedIn Cincinnati Metro / Remote / Contract / Full-Time searches in `/Users/chris/2026 Resumes/Search-Sites.md` as the manual baseline.
    - Query them through Chrome debugging at a normal user pace; review the newest results first and avoid rapid pagination.
  - Indeed
  - direct company career pages for known target companies
  - Built In
- Two to three times per week:
  - Wellfound
  - YC Work at a Startup
  - Himalayas
- Weekly:
  - Fractional Jobs
  - fraction.al
  - Braintrust
  - Catalant
  - Business Talent Group (BTG)
  - A.Team

### Search Order

1. Submit or finish already-prepared strongest applications first.
2. Search known target companies directly before aggregators.
3. Search remote full-time roles in the preferred lanes:
   - engineering manager
   - senior engineering manager
   - director / senior director of engineering
   - principal / lead / staff-plus platform or AI roles
4. Search regional hybrid/on-site roles in practical commute / relocation metros:
   - Cincinnati Metro / Northern Kentucky
   - Columbus, OH
   - Dayton, OH
   - Louisville, KY
   - Indianapolis, IN
   - Cleveland, OH
5. Search fractional / interim roles and talent networks for bridge income.

### Regional Metro Search Lane

For every comprehensive search, include a dedicated regional lane rather than relying on remote-only results. The goal is to catch income-continuity roles that may not advertise as remote but are acceptable because they are local, commutable, or regionally relocatable.

Search LinkedIn, Indeed, Built In, Google Jobs, and direct company/career pages with these metro filters:

- Cincinnati, OH / Cincinnati Metro / Northern Kentucky / Covington, KY / Florence, KY
- Columbus, OH
- Dayton, OH
- Louisville, KY
- Indianapolis, IN
- Cleveland, OH

Use combinations of:

- `CTO`
- `Chief Technology Officer`
- `VP Engineering`
- `Vice President Engineering`
- `Head of Engineering`
- `Director of Engineering`
- `Senior Director Engineering`
- `Software Engineering Director`
- `Engineering Manager`
- `Platform Engineering`
- `Cloud Engineering`
- `Application Development`
- `Digital Transformation`
- `AI`

Triage regional roles with the same cash-floor rules, but bias upward when:

- The role is Cincinnati metro hybrid/on-site and compensation is plausible.
- The role is within the listed regional metros and offers senior scope, practical income continuity, or a credible bridge into full-time leadership.
- The company is not a prestige target but the role is serious, paid, and aligned enough to generate interviews.

### Preferred Search Themes

Use combinations of:

- `engineering manager`
- `director of engineering`
- `principal engineer`
- `platform`
- `cloud`
- `security`
- `governance`
- `developer platform`
- `AI`
- `applied AI`
- `RAG`
- `agentic`
- `MCP`
- `workflow`
- `remote`
- `fractional CTO`
- `interim engineering leader`

### Output Format For Search Sessions

When running a search session, produce a dated markdown review queue under `/Users/chris/2026 Resumes/searches/` with buckets:

- `Apply Now`
- `Apply If Time`
- `Skip / Probably Not`
- `Activate This Week` for fractional networks or talent platforms

Each item should capture, when available:

- company
- role title
- work model
- compensation or whether it is undisclosed
- one-line fit assessment
- key risk or stretch
- source link

### Review Queue Rules

- Keep broad search notes in a dated markdown queue under `/Users/chris/2026 Resumes/searches/` until a role is selected for action.
- Only create a `Send To/` folder and a `CREATED` tracker row once a role is promoted into active tailoring work.
- It is acceptable to add explicit `PROBABLY NOT` rows to the tracker for notable roles already researched, especially if that avoids re-evaluating the same posting later.

### Company-Coherence Rule

- At a company Chris has not applied to before, a plausible stretch is usually worth consideration.
- At a company Chris has already applied to, prefer one strongest role or a tightly coherent pair.
- Avoid mixed-signal submissions unless there is a clear strategy for them.
- Before promoting another role at a company with recent application history, check `/Users/chris/2026 Resumes/searches/company-application-guardrails.md` for company-specific hold/deprioritization notes.

### Search Expansion Rule

- Until late April 2026, bias toward remote and remote-with-travel.
- As of May 2026, include regional hybrid/on-site searches in every comprehensive search pass, with special attention to Cincinnati metro.
- If the pipeline is still weak in June 2026, emergency fallback rules can be used deliberately rather than accidentally.

## Compensation Scripts (Cash Floor)

Goal: qualify early without oversharing. Keep rationale private. Do not put compensation numbers on the resume.

Working constraints:

- Ideal full-time target is **$290k+ base** or equivalent guaranteed cash.
- Practical W-2 floor is **$265k-$270k base** when benefits are strong enough to offset self-employment costs (health insurance, employer payroll tax share, and retirement benefits).
- Emergency fallback floor is **$240k-$250k base** for full-time W-2 only if the search remains weak into May/June 2026 and the role is otherwise solid on work model, company quality, and trajectory.
- Current self-employment billing baseline is **$24,675/month** (about **$296,100/year**), so avoid dropping materially below that monthly cash profile without an explicit tradeoff decision.
- Current documented self-employment burden includes at least:
  - employer-side Social Security: **$930/month**
  - employer-side Medicare: **$217.50/month**
  - health insurance: **$1,081/month**
  - dental insurance: **$63/month**
- Total documented monthly self-employment burden: **$2,291.50/month** (about **$27,498/year**) before retirement-plan differences.
- Using that burden, a rough W-2 equivalent to the current billing baseline is about **$268,602/year**, which validates the current practical W-2 floor of **$265k-$270k base** when benefits are strong.
- Fractional / interim work is acceptable if one engagement or a combination of engagements can credibly meet the same income need.
- Bonus and equity are upside on top of the base / guaranteed-cash requirement.

### Recruiter Email / LinkedIn Message (Short)

Use when a recruiter asks comp range early or the posting looks ambiguous:

> Thanks for reaching out. Before we invest too much time, I’m targeting roles at **$290k+ base (or equivalent guaranteed cash)**, with bonus/equity on top depending on level and scope. If that aligns, I’d be glad to set up time.

### First Call (Verbal, Neutral)

Use when asked “What are you looking for?”:

> For the right scope, I’m looking for **$290k+ base or equivalent guaranteed cash**. I’m happy to be flexible on bonus and equity on top, depending on the overall package and role expectations.

If pressed on “all-in” first:

> I can talk total comp once we’re aligned on level and scope. The key constraint is **$290k+ base/guaranteed cash**, and then we can structure bonus/equity around that.

### Late-Stage / Offer Negotiation (Firm, Collaborative)

Use after they’ve established fit and level:

> I’m excited about the role and ready to move forward. To accept, I need **$290k+ in base (or guaranteed cash equivalent)**. If there’s flexibility, I’d like to optimize total comp with a sign-on and/or performance bonus and equity on top. How close can we get on base?

If they can’t move base but can move guaranteed cash:

> If base is capped, we can still get to the right cash level with a **guaranteed first-year bonus and/or sign-on**. The main requirement is **$290k+ guaranteed cash in year one**.

### Notes

- “Guaranteed cash” = base + sign-on + guaranteed bonus (not target).
- `Ideal target` and `practical floor` are different:
  - ideal full-time target: `290k+ base`
  - practical W-2 floor: `265k-$270k base` if benefits are strong
- `Emergency fallback floor` is only for late-stage search pressure:
  - `240k-$250k base`
  - use only if the pipeline is still weak in May/June 2026
  - prefer remote, remote-with-travel, or in-region opportunities even in fallback mode
- If a recruiter’s range is clearly below the practical floor, exit quickly and politely unless the search strategy has explicitly shifted into emergency fallback mode.
- Keep delivery calm and matter-of-fact; no justification beyond “market/level/scope alignment.”

## Fractional / Interim Positioning

Use when pursuing fractional CTO / interim engineering leadership as a fallback or bridge (preference remains full-time).

### Resume / LinkedIn Headline Variants

- `Fractional CTO | Interim Engineering Leader | Cloud-Native + AI | 0→1 and Modernization`
- `Fractional CTO (Hands-On) | Delivery Systems, Security/Compliance, Cost + Reliability`

Keep the same achievements and metrics, but tighten bullets around:

- Decision-making scope (strategy + architecture + hiring + operating cadence).
- Fast, concrete outcomes (stabilize delivery, cut spend, ship MVP, unblock teams).

### Inbound Message (Short)

> I’m currently prioritizing full-time CTO/VP Engineering roles, but I’m open to a fractional/interim engagement if the scope is meaningful (decision rights + delivery ownership). If helpful, I can support **[X] days/week** starting **[date]**.

### Screening Call Script

> I prefer full-time, but I’m open to fractional if it’s a real operating role: clear ownership, access to stakeholders, and enough weekly capacity to deliver. What’s the expected time commitment and decision scope?

If they ask about comp for fractional:

> For fractional work I anchor on an annualized equivalent of my full-time target, and we can structure that as a monthly retainer based on **days/week** and scope.

### Engagement Guardrails (Avoid Bad Fractional Deals)

- Confirm decision rights: who owns roadmap priorities, architecture calls, hiring, and budget.
- Define the operating model: meeting cadence, who you manage/mentor, escalation paths.
- Define deliverables: 30/60/90-day outcomes (e.g., roadmap, platform plan, hiring plan, reliability/security posture, modernization plan).
- Ensure time is sufficient: <1 day/week rarely works unless it’s purely advisory.
- If full-time is a possible outcome: set explicit conversion conditions (timeline, level, cash floor).

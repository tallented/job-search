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
   - Headline (title + 2-3 differentiators)
   - Professional Summary (2-4 sentences, specific to the role)
   - Core Skills (reordered to mirror the req; avoid long lists that dilute signal)
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
   - Remove role-misaligned details (e.g., too much IC depth for CTO, or too much org narrative for Principal) unless the req explicitly wants that hybrid.
   - Do not use em dashes in resume copy; prefer commas, parentheses, vertical bars, colons, or a regular hyphen.
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
- Once the application is actually submitted, move the whole folder into `Submitted/`.
- Do not overwrite or reuse an old company folder for a new application cycle; create a new date-prefixed folder instead.
- If there are multiple attempts for the same company over time, the date prefix is the source of truth for recency.

## Application Tracker

Track active and submitted applications in:

- local NocoDB tracker at `http://localhost:8085`
- base: `Job Search`
- table: `Applications`

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
- Acceptable now: hybrid in Cincinnati, Louisville, Indianapolis, Dayton, Columbus, or Cleveland
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
4. Search fractional / interim roles and talent networks for bridge income.
5. Expand into regional hybrid roles when the remote queue is thin.

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

### Search Expansion Rule

- Until late April 2026, bias toward remote and remote-with-travel.
- If the pipeline is still weak in May 2026, expand more aggressively into regional hybrid roles and practical-floor opportunities.
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

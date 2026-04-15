# Job Tracker

This folder runs a local NocoDB instance for job-search tracking.

## Current Local Instance

- URL: `http://localhost:8085`
- base: `Job Search`
- table: `Applications`
- login email: `local-admin@resume-tracker.local`

The current instance is already initialized and the `Submissions` sheet has been imported.

Use this NocoDB base as the main writable tracker going forward. The Excel workbook is now a legacy source/import, not the day-to-day system of record.

## Start

```sh
cd "/Users/chris/2026 Resumes/job-tracker"
./docker.up.sh
```

Open:

- http://localhost:8085

## Create A Tracker Row

Use the helper to create a new `Applications` record in NocoDB:

```sh
cd "/Users/chris/2026 Resumes/job-tracker"
./create-application.sh \
  --company "Acme" \
  --title "CTO" \
  --created 20260415 \
  --status CREATED \
  --type "Full time" \
  --link "https://example.com/jobs/cto" \
  --resume-folder "/Users/chris/2026 Resumes/Send To/20260415 - Acme - CTO"
```

The script writes directly to the local NocoDB SQLite file and prevents duplicate inserts when the same `Resume Folder` is already tracked.

`/Users/chris/2026 Resumes/scripts/new_resume.sh` now uses this helper automatically unless `SKIP_TRACKER=1`.

## Update A Tracker Row

Use the companion helper to update an existing record by row `Id`, `Resume Folder`, or a unique `Company + Title` match:

```sh
cd "/Users/chris/2026 Resumes/job-tracker"
./update-application.sh \
  --resume-folder "/Users/chris/2026 Resumes/Send To/20260415 - Acme - CTO" \
  --status SUBMITTED \
  --submitted today
```

Examples:

```sh
# Mark a row rejected and note the latest touch date automatically.
./update-application.sh \
  --company "Docker" \
  --title "Principal Software Engineer - AI Tools and Security" \
  --status REJECTED \
  --next-steps "Rejected 2026-04-15 - location screen"

# Log recruiter contact without changing status.
./update-application.sh \
  --id 21 \
  --last-contact-date today \
  --next-steps "Recruiter intro call completed; follow up next week"
```

The updater accepts `today` for date fields and can also clear optional fields with repeated `--clear-field ...`.

## Import Current Tracker

The exported `Submissions` sheet is here:

- `import/2026-job-search-submissions.csv`

Recommended import target:

- base: `Job Search`
- table: `Applications`

## Stop

```sh
cd "/Users/chris/2026 Resumes/job-tracker"
./docker.down.sh
```

These scripts are thin wrappers around `docker compose` so you do not need to remember the flags.

## Update The CSV Export

```sh
cd "/Users/chris/2026 Resumes/job-tracker"
python3 export_submissions_sheet.py
```

This reads `../bak/2026 Job Search.xlsx` and exports the archived `Submissions` sheet to CSV.

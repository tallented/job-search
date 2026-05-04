#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path


WORKSPACE = Path("/Users/chris/2026 Resumes")
DB_PATH = WORKSPACE / "job-tracker" / "data" / "noco.db"
TABLE = "nc_g9md___Applications"

CONTACT_STATUSES = {
    "Applied",
    "SUBMITTED",
    "REJECTED",
    "DENIED",
    "ALREADY FILLED",
    "NO LONGER ACCEPTING",
    "INITIAL CONVO",
    "Schedule interview",
}
SUBMISSION_STATUSES = {"Applied", "SUBMITTED"}

CLEARABLE_FIELDS = {
    "submitted": "Submitted",
    "last-contact-date": "Last_Contact_Date",
    "next-steps": "Next_Steps",
    "listing-source": "Listing_Source",
    "ref-number": "Ref_Number",
    "link": "Link",
    "salary": "Salary",
    "location": "Location",
    "type": "Type",
    "resume-folder": "Resume_Folder",
    "resume-decision": "Resume_Decision",
}


def parse_date(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if text.lower() == "today":
        return date.today().isoformat()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value!r}")


def utc_now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S+00:00")


def normalize_resume_folder(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update an existing application row in the local NocoDB tracker."
    )
    parser.add_argument("--db", default=str(DB_PATH))
    parser.add_argument("--id", type=int)
    parser.add_argument("--resume-folder")
    parser.add_argument("--company")
    parser.add_argument("--title")

    parser.add_argument("--status")
    parser.add_argument("--created")
    parser.add_argument("--submitted")
    parser.add_argument("--last-contact-date")
    parser.add_argument("--type")
    parser.add_argument("--location")
    parser.add_argument("--salary")
    parser.add_argument("--next-steps")
    parser.add_argument("--listing-source")
    parser.add_argument("--ref-number")
    parser.add_argument("--link")
    parser.add_argument("--resume-decision")
    parser.add_argument("--set-resume-folder")
    parser.add_argument(
        "--allow-missing-folder",
        action="store_true",
        help="Allow Resume Folder paths that do not exist on disk yet.",
    )
    parser.add_argument(
        "--clear-field",
        action="append",
        choices=sorted(CLEARABLE_FIELDS),
        default=[],
        help="Clear a field instead of setting a value. Repeat as needed.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the proposed row changes without saving them.",
    )
    return parser


def require_locator(args: argparse.Namespace) -> tuple[str, object]:
    locator_count = 0
    locator: tuple[str, object] | None = None

    if args.id is not None:
        locator_count += 1
        locator = ("id", args.id)

    if args.resume_folder:
        locator_count += 1
        locator = ("resume_folder", normalize_resume_folder(args.resume_folder))

    if args.company or args.title:
        if not (args.company and args.title):
            raise SystemExit("Use both --company and --title together when locating by company/title.")
        locator_count += 1
        locator = ("company_title", (args.company.strip(), args.title.strip()))

    if locator_count != 1 or locator is None:
        raise SystemExit(
            "Choose exactly one locator: --id, --resume-folder, or the pair --company and --title."
        )

    return locator


def require_updates(args: argparse.Namespace) -> None:
    update_values = [
        args.status,
        args.created,
        args.submitted,
        args.last_contact_date,
        args.type,
        args.location,
        args.salary,
        args.next_steps,
        args.listing_source,
        args.ref_number,
        args.link,
        args.resume_decision,
        args.set_resume_folder,
    ]
    if not any(value is not None for value in update_values) and not args.clear_field:
        raise SystemExit("Provide at least one field to update.")


def fetch_matching_rows(conn: sqlite3.Connection, locator: tuple[str, object]) -> list[sqlite3.Row]:
    kind, value = locator
    if kind == "id":
        rows = conn.execute(
            f"SELECT * FROM {TABLE} WHERE id = ?",
            (value,),
        ).fetchall()
    elif kind == "resume_folder":
        rows = conn.execute(
            f"SELECT * FROM {TABLE} WHERE Resume_Folder = ?",
            (value,),
        ).fetchall()
    else:
        company, title = value
        rows = conn.execute(
            f"""
            SELECT *
            FROM {TABLE}
            WHERE lower(Company) = lower(?)
              AND lower(Title) = lower(?)
            """,
            (company, title),
        ).fetchall()
    return rows


def conflict_check_resume_folder(
    conn: sqlite3.Connection, target_row_id: int, resume_folder: str
) -> None:
    conflict = conn.execute(
        f"""
        SELECT id, Company, Title, Status
        FROM {TABLE}
        WHERE Resume_Folder = ?
          AND id != ?
        LIMIT 1
        """,
        (resume_folder, target_row_id),
    ).fetchone()
    if conflict is not None:
        raise SystemExit(
            "Resume folder already belongs to another row: "
            f"{conflict['id']} | {conflict['Company']} | {conflict['Title']} | {conflict['Status']}"
        )


def user_to_db_updates(args: argparse.Namespace, current: sqlite3.Row) -> dict[str, object]:
    cleared = {CLEARABLE_FIELDS[name] for name in args.clear_field}
    updates: dict[str, object] = {}

    def ensure_not_cleared(db_field: str, user_flag: str) -> None:
        if db_field in cleared:
            raise SystemExit(f"Cannot use --{user_flag} together with --clear-field {db_field}.")

    if args.status is not None:
        updates["Status"] = args.status.strip()
    if args.created is not None:
        ensure_not_cleared("Created", "created")
        updates["Created"] = parse_date(args.created)
    if args.submitted is not None:
        ensure_not_cleared("Submitted", "submitted")
        updates["Submitted"] = parse_date(args.submitted)
    if args.last_contact_date is not None:
        ensure_not_cleared("Last_Contact_Date", "last-contact-date")
        updates["Last_Contact_Date"] = parse_date(args.last_contact_date)
    if args.type is not None:
        ensure_not_cleared("Type", "type")
        updates["Type"] = args.type.strip() or None
    if args.location is not None:
        ensure_not_cleared("Location", "location")
        updates["Location"] = args.location.strip() or None
    if args.salary is not None:
        ensure_not_cleared("Salary", "salary")
        updates["Salary"] = args.salary.strip() or None
    if args.next_steps is not None:
        ensure_not_cleared("Next_Steps", "next-steps")
        updates["Next_Steps"] = args.next_steps.strip() or None
    if args.listing_source is not None:
        ensure_not_cleared("Listing_Source", "listing-source")
        updates["Listing_Source"] = args.listing_source.strip() or None
    if args.ref_number is not None:
        ensure_not_cleared("Ref_Number", "ref-number")
        updates["Ref_Number"] = args.ref_number.strip() or None
    if args.link is not None:
        ensure_not_cleared("Link", "link")
        updates["Link"] = args.link.strip() or None
    if args.resume_decision is not None:
        ensure_not_cleared("Resume_Decision", "resume-decision")
        updates["Resume_Decision"] = args.resume_decision.strip() or None
    if args.set_resume_folder is not None:
        ensure_not_cleared("Resume_Folder", "set-resume-folder")
        resume_folder = normalize_resume_folder(args.set_resume_folder)
        if resume_folder is None:
            raise SystemExit("--set-resume-folder cannot be blank.")
        if not args.allow_missing_folder and not Path(resume_folder).exists():
            raise FileNotFoundError(
                f"Resume folder does not exist: {resume_folder}\n"
                "Create the folder first or rerun with --allow-missing-folder."
            )
        updates["Resume_Folder"] = resume_folder

    for db_field in cleared:
        updates[db_field] = None

    current_status = current["Status"]
    next_status = updates.get("Status", current_status)
    status_changed = next_status != current_status
    submitted_explicit = "Submitted" in updates
    last_contact_explicit = "Last_Contact_Date" in updates

    if (
        status_changed
        and next_status in SUBMISSION_STATUSES
        and not submitted_explicit
        and not current["Submitted"]
    ):
        updates["Submitted"] = date.today().isoformat()
        submitted_explicit = True

    if not last_contact_explicit and next_status in CONTACT_STATUSES:
        if submitted_explicit and updates.get("Submitted"):
            updates["Last_Contact_Date"] = updates["Submitted"]
        elif status_changed:
            updates["Last_Contact_Date"] = date.today().isoformat()

    return updates


def print_match_conflict(rows: list[sqlite3.Row]) -> None:
    print("Multiple rows matched. Narrow the locator with --id or --resume-folder.")
    for row in rows:
        print(
            f"  {row['id']}: {row['Company']} | {row['Title']} | "
            f"{row['Status']} | {row['Resume_Folder']}"
        )


def main() -> int:
    args = build_parser().parse_args()
    require_updates(args)
    locator = require_locator(args)

    db_path = Path(args.db)
    if not db_path.exists():
        raise FileNotFoundError(f"NocoDB database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        rows = fetch_matching_rows(conn, locator)
        if not rows:
            raise SystemExit("No matching application row found.")
        if len(rows) > 1:
            print_match_conflict(rows)
            raise SystemExit(1)

        current = rows[0]
        updates = user_to_db_updates(args, current)

        if "Resume_Folder" in updates and updates["Resume_Folder"] is not None:
            conflict_check_resume_folder(conn, current["id"], updates["Resume_Folder"])

        changed_fields = {
            key: value
            for key, value in updates.items()
            if current[key] != value
        }

        if not changed_fields:
            print(f"No changes needed for row {current['id']}.")
            return 0

        changed_fields["updated_at"] = utc_now_text()

        if args.dry_run:
            print(f"Dry run for row {current['id']}: {current['Company']} | {current['Title']}")
            for key, value in changed_fields.items():
                print(f"  {key}: {current[key]!r} -> {value!r}")
            return 0

        assignments = ", ".join(f"{column} = ?" for column in changed_fields)
        values = list(changed_fields.values()) + [current["id"]]

        with conn:
            conn.execute(
                f"UPDATE {TABLE} SET {assignments} WHERE id = ?",
                values,
            )
    finally:
        conn.close()

    print(f"Updated NocoDB application row {current['id']}")
    print(f"  Company: {current['Company']}")
    print(f"  Title: {current['Title']}")
    for key, value in changed_fields.items():
        print(f"  {key}: {current[key]!r} -> {value!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path


WORKSPACE = Path("/Users/chris/2026 Resumes")
DB_PATH = WORKSPACE / "job-tracker" / "data" / "noco.db"
TABLE = "nc_g9md___Applications"


@dataclass(frozen=True)
class ExistingRow:
    row_id: int
    company: str | None
    title: str | None
    status: str | None


def parse_date(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
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


def existing_by_resume_folder(conn: sqlite3.Connection, resume_folder: str) -> ExistingRow | None:
    row = conn.execute(
        f"""
        SELECT id, Company, Title, Status
        FROM {TABLE}
        WHERE Resume_Folder = ?
        LIMIT 1
        """,
        (resume_folder,),
    ).fetchone()
    if row is None:
        return None
    return ExistingRow(row_id=row[0], company=row[1], title=row[2], status=row[3])


def next_nc_order(conn: sqlite3.Connection) -> float:
    value = conn.execute(f"SELECT COALESCE(MAX(nc_order), 0) + 1 FROM {TABLE}").fetchone()[0]
    return float(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a new application row in the local NocoDB tracker."
    )
    parser.add_argument("--db", default=str(DB_PATH))
    parser.add_argument("--company", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", default="CREATED")
    parser.add_argument("--created", default=date.today().isoformat())
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
    parser.add_argument("--resume-folder", required=True)
    parser.add_argument(
        "--allow-missing-folder",
        action="store_true",
        help="Allow Resume Folder paths that do not exist on disk yet.",
    )
    parser.add_argument(
        "--skip-if-exists",
        action="store_true",
        help="Return success without inserting if a row with the same Resume Folder already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized row payload without inserting it.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise FileNotFoundError(f"NocoDB database not found: {db_path}")

    resume_folder = normalize_resume_folder(args.resume_folder)
    if resume_folder is None:
        raise ValueError("--resume-folder is required")

    if not args.allow_missing_folder and not Path(resume_folder).exists():
        raise FileNotFoundError(
            f"Resume folder does not exist: {resume_folder}\n"
            "Create the folder first or rerun with --allow-missing-folder."
        )

    created = parse_date(args.created)
    submitted = parse_date(args.submitted)
    last_contact_date = parse_date(args.last_contact_date) or submitted
    timestamp = utc_now_text()

    payload = {
        "created_at": timestamp,
        "updated_at": timestamp,
        "created_by": None,
        "updated_by": None,
        "nc_order": None,  # set after opening the DB
        "Company": args.company.strip(),
        "Status": args.status.strip(),
        "Created": created,
        "Submitted": submitted,
        "Title": args.title.strip(),
        "Type": args.type.strip() if args.type else None,
        "Location": args.location.strip() if args.location else None,
        "Salary": args.salary.strip() if args.salary else None,
        "Next_Steps": args.next_steps.strip() if args.next_steps else None,
        "Listing_Source": args.listing_source.strip() if args.listing_source else None,
        "Ref_Number": args.ref_number.strip() if args.ref_number else None,
        "Link": args.link.strip() if args.link else None,
        "Resume_Decision": args.resume_decision.strip() if args.resume_decision else None,
        "Resume_Folder": resume_folder,
        "Last_Contact_Date": last_contact_date,
    }

    if args.dry_run:
        print("Dry run payload:")
        for key, value in payload.items():
            print(f"  {key}={value}")
        return 0

    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        existing = existing_by_resume_folder(conn, resume_folder)
        if existing is not None:
            message = (
                f"Resume folder already tracked by row {existing.row_id}: "
                f"{existing.company} | {existing.title} | {existing.status}"
            )
            if args.skip_if_exists:
                print(message)
                return 0
            raise SystemExit(message)

        payload["nc_order"] = next_nc_order(conn)

        columns = ", ".join(payload.keys())
        placeholders = ", ".join("?" for _ in payload)
        values = tuple(payload.values())

        with conn:
            cur = conn.execute(
                f"INSERT INTO {TABLE} ({columns}) VALUES ({placeholders})",
                values,
            )
        row_id = cur.lastrowid
    finally:
        conn.close()

    print(f"Created NocoDB application row {row_id}")
    print(f"  Company: {payload['Company']}")
    print(f"  Title: {payload['Title']}")
    print(f"  Status: {payload['Status']}")
    print(f"  Created: {payload['Created']}")
    print(f"  Resume Folder: {payload['Resume_Folder']}")
    if payload["Link"]:
        print(f"  Link: {payload['Link']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

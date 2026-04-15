#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
import re
import subprocess
from pathlib import Path


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)


class HTMLToText(HTMLParser):
    BLOCK_TAGS = {
        "p",
        "div",
        "section",
        "article",
        "header",
        "footer",
        "li",
        "ul",
        "ol",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "pre",
    }

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "br":
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS and tag != "li":
            self.parts.append("\n\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        text = html.unescape("".join(self.parts))
        text = text.replace("\xa0", " ")
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)
        return text.strip()


def html_to_text(value: str) -> str:
    parser = HTMLToText()
    parser.feed(value)
    return parser.text()


def fetch_html(url: str) -> str:
    result = subprocess.run(
        ["curl", "-L", "-A", UA, url],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_placeholder(path: Path) -> dict[str, str]:
    text = path.read_text()
    lines = text.splitlines()
    data: dict[str, str] = {
        "title": lines[0].strip() if lines else path.parent.name,
        "url": "",
        "source_queue": "",
        "lane": "",
        "work_model": "",
        "compensation": "",
        "listing_source": "",
        "fit": "",
        "risk": "",
    }
    fit_lines: list[str] = []
    risk_lines: list[str] = []
    mode = None
    for line in lines[1:]:
        if line.startswith("Source queue: "):
            data["source_queue"] = line.split(": ", 1)[1].strip()
        elif line.startswith("URL: "):
            data["url"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Lane: "):
            data["lane"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Work model: "):
            data["work_model"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Compensation: "):
            data["compensation"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Listing source: "):
            data["listing_source"] = line.split(": ", 1)[1].strip()
        elif line.strip() == "Fit:":
            mode = "fit"
        elif line.strip() == "Risk / stretch:":
            mode = "risk"
        elif mode == "fit":
            fit_lines.append(line.rstrip())
        elif mode == "risk":
            risk_lines.append(line.rstrip())
    data["fit"] = "\n".join([line for line in fit_lines if line.strip()]).strip()
    data["risk"] = "\n".join([line for line in risk_lines if line.strip()]).strip()
    return data


def extract_ashby(path: Path) -> str:
    html_doc = fetch_html(path)
    match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>',
        html_doc,
        flags=re.S,
    )
    if not match:
        raise RuntimeError("Could not find Ashby JobPosting JSON-LD")
    payload = json.loads(match.group(1))
    description_html = payload.get("description", "")
    description_text = html_to_text(description_html)

    parts: list[str] = []
    org = payload.get("hiringOrganization", {})
    company = org.get("name")
    if company:
        parts.append(f"Company: {company}")
    title = payload.get("title")
    if title:
        parts.append(f"Title: {title}")
    employment_type = payload.get("employmentType")
    if employment_type:
        parts.append(f"Employment Type: {employment_type}")
    job_location = payload.get("jobLocation")
    if isinstance(job_location, list):
        locs = []
        for item in job_location:
            addr = item.get("address", {}) if isinstance(item, dict) else {}
            loc = ", ".join(
                [part for part in [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")] if part]
            )
            if loc:
                locs.append(loc)
        if locs:
            parts.append(f"Location: {'; '.join(locs)}")
    elif isinstance(job_location, dict):
        addr = job_location.get("address", {})
        loc = ", ".join(
            [part for part in [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")] if part]
        )
        if loc:
            parts.append(f"Location: {loc}")

    salary = payload.get("baseSalary")
    if isinstance(salary, dict):
        value = salary.get("value", {})
        minimum = value.get("minValue")
        maximum = value.get("maxValue")
        currency = salary.get("currency", "USD")
        unit = value.get("unitText", "")
        if minimum is not None and maximum is not None:
            parts.append(
                f"Compensation: {currency} {minimum:,} - {maximum:,}"
                + (f" per {unit}" if unit else "")
            )

    if parts:
        parts.append("")
    parts.append(description_text)
    return "\n".join(parts).strip()


def write_job_description(path: Path, meta: dict[str, str], full_posting: str, source_note: str) -> None:
    fetched_on = dt.date.today().isoformat()
    body = [
        meta["title"],
        f"Original source URL: {meta['url']}",
        f"Fetched on: {fetched_on}",
        f"Source used for local copy: {source_note}",
    ]
    if meta["source_queue"]:
        body.append(f"Source queue: {meta['source_queue']}")
    if meta["lane"]:
        body.append(f"Lane: {meta['lane']}")
    if meta["work_model"]:
        body.append(f"Work model (queue): {meta['work_model']}")
    if meta["compensation"]:
        body.append(f"Compensation (queue): {meta['compensation']}")
    if meta["listing_source"]:
        body.append(f"Listing source (queue): {meta['listing_source']}")

    body.extend(
        [
            "",
            "--- FULL POSTING ---",
            "",
            full_posting.strip(),
            "",
            "--- LOCAL SUMMARY ---",
            "",
            f"Fit:\n{meta['fit'] or 'Not added yet.'}",
            "",
            f"Risk / stretch:\n{meta['risk'] or 'Not added yet.'}",
            "",
        ]
    )
    path.write_text("\n".join(body))


def refresh_ashby_folder(folder: Path) -> None:
    jd = folder / "job description.txt"
    meta = parse_placeholder(jd)
    full_posting = extract_ashby(meta["url"])
    write_job_description(jd, meta, full_posting, "Original Ashby posting")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="+")
    args = parser.parse_args()
    for raw in args.folder:
        folder = Path(raw)
        refresh_ashby_folder(folder)


if __name__ == "__main__":
    main()

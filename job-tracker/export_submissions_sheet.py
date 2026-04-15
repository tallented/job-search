#!/usr/bin/env python3

import csv
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def column_number(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    value = 0
    for ch in letters:
        value = value * 26 + (ord(ch.upper()) - 64)
    return value


def load_shared_strings(xlsx: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in xlsx.namelist():
        return []

    root = ET.fromstring(xlsx.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.findall("a:si", NS):
        text = "".join(node.text or "" for node in item.iterfind(".//a:t", NS))
        strings.append(text)
    return strings


def submissions_sheet_path(xlsx: zipfile.ZipFile) -> str:
    workbook = ET.fromstring(xlsx.read("xl/workbook.xml"))
    rels = ET.fromstring(xlsx.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}

    for sheet in workbook.find("a:sheets", NS):
        if sheet.attrib["name"] == "Submissions":
            rel_id = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            return "xl/" + rel_map[rel_id]

    raise SystemExit("Could not find the Submissions sheet in the workbook.")


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")

    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iterfind(".//a:t", NS))

    value_node = cell.find("a:v", NS)
    if value_node is None or value_node.text is None:
        return ""

    value = value_node.text
    if cell_type == "s":
        return shared_strings[int(value)]
    return value


def normalize_for_export(column: int, value: str) -> str:
    if not value:
        return value

    if column in (3, 4):
        try:
            serial = float(value)
        except ValueError:
            return value

        date_value = datetime(1899, 12, 30) + timedelta(days=serial)
        return date_value.date().isoformat()

    return value


def export_submissions() -> None:
    root = Path(__file__).resolve().parent
    workbook_path = root.parent / "bak" / "2026 Job Search.xlsx"
    output_dir = root / "import"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "2026-job-search-submissions.csv"

    with zipfile.ZipFile(workbook_path) as xlsx:
        shared_strings = load_shared_strings(xlsx)
        sheet_path = submissions_sheet_path(xlsx)
        sheet = ET.fromstring(xlsx.read(sheet_path))

        rows = []
        max_column = 0
        for row in sheet.findall(".//a:sheetData/a:row", NS):
            values = {}
            for cell in row.findall("a:c", NS):
                col = column_number(cell.attrib["r"])
                values[col] = cell_value(cell, shared_strings)
                max_column = max(max_column, col)
            rows.append(values)

    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        for row in rows:
            writer.writerow(
                [
                    normalize_for_export(col, row.get(col, ""))
                    for col in range(1, max_column + 1)
                ]
            )

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    export_submissions()

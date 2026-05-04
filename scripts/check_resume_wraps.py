#!/usr/bin/env python3
"""Flag likely jagged/orphaned wrapped lines in rendered resume pages.

Workflow:
1. Render a PDF to page PNGs with `pdftoppm`.
2. OCR each page with `tesseract` TSV output.
3. Group words into OCR lines and paragraphs.
4. Flag paragraphs whose final rendered line looks unusually short.

This is heuristic by design. It is meant to reduce review time, not replace
human judgment.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import statistics
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WordBox:
    page: int
    block: int
    paragraph: int
    line: int
    left: int
    top: int
    width: int
    height: int
    conf: float
    text: str


@dataclass
class OcrLine:
    page: int
    block: int
    paragraph: int
    line: int
    left: int
    top: int
    right: int
    bottom: int
    width: int
    word_count: int
    text: str


@dataclass
class FlaggedLine:
    page: int
    reason: str
    ratio: float
    word_count: int
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag likely 1-2 word jagged wrap lines in a resume PDF."
    )
    parser.add_argument("pdf", type=Path, help="Path to a rendered PDF")
    parser.add_argument(
        "--keep-images",
        action="store_true",
        help="Keep rendered page PNGs and print their directory",
    )
    return parser.parse_args()


def require_tool(name: str) -> None:
    if shutil.which(name):
        return
    print(f"Missing required tool: {name}", file=sys.stderr)
    sys.exit(2)


def render_pdf_to_pngs(pdf_path: Path, out_dir: Path) -> list[Path]:
    prefix = out_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", str(pdf_path), str(prefix)],
        check=True,
        capture_output=True,
        text=True,
    )
    pages = sorted(out_dir.glob("page-*.png"))
    if not pages:
        raise RuntimeError(f"No page images rendered from {pdf_path}")
    return pages


def run_tesseract_tsv(image_path: Path) -> list[WordBox]:
    result = subprocess.run(
        ["tesseract", str(image_path), "stdout", "tsv"],
        check=True,
        capture_output=True,
        text=True,
    )
    rows: list[WordBox] = []
    reader = csv.DictReader(result.stdout.splitlines(), delimiter="\t")
    for row in reader:
        text = (row.get("text") or "").strip()
        if not text:
            continue
        if row.get("level") != "5":
            continue
        try:
            conf = float(row["conf"])
        except (TypeError, ValueError):
            conf = -1.0
        if conf >= 0 and conf < 35:
            continue
        rows.append(
            WordBox(
                page=int(row["page_num"]),
                block=int(row["block_num"]),
                paragraph=int(row["par_num"]),
                line=int(row["line_num"]),
                left=int(row["left"]),
                top=int(row["top"]),
                width=int(row["width"]),
                height=int(row["height"]),
                conf=conf,
                text=text,
            )
        )
    return rows


def build_lines(words: list[WordBox]) -> list[OcrLine]:
    grouped: dict[tuple[int, int, int, int], list[WordBox]] = {}
    for word in words:
        key = (word.page, word.block, word.paragraph, word.line)
        grouped.setdefault(key, []).append(word)

    lines: list[OcrLine] = []
    for key, items in grouped.items():
        items.sort(key=lambda w: (w.left, w.top))
        left = min(w.left for w in items)
        top = min(w.top for w in items)
        right = max(w.left + w.width for w in items)
        bottom = max(w.top + w.height for w in items)
        text = " ".join(w.text for w in items)
        lines.append(
            OcrLine(
                page=key[0],
                block=key[1],
                paragraph=key[2],
                line=key[3],
                left=left,
                top=top,
                right=right,
                bottom=bottom,
                width=right - left,
                word_count=len(items),
                text=text,
            )
        )
    lines.sort(key=lambda line: (line.page, line.top, line.left, line.block, line.paragraph, line.line))
    return lines


def looks_like_header(line: OcrLine) -> bool:
    text = line.text.strip()
    if not text:
        return True
    if text.isupper():
        return True
    if "|" in text and line.word_count <= 8:
        return True
    return False


def flag_jagged_lines(lines: list[OcrLine]) -> list[FlaggedLine]:
    grouped: dict[tuple[int, int, int], list[OcrLine]] = {}
    for line in lines:
        grouped.setdefault((line.page, line.block, line.paragraph), []).append(line)

    flagged: list[FlaggedLine] = []
    for (page, _block, _paragraph), paragraph_lines in grouped.items():
        paragraph_lines.sort(key=lambda line: (line.line, line.top, line.left))
        if len(paragraph_lines) < 2:
            continue

        last = paragraph_lines[-1]
        prior = paragraph_lines[:-1]
        if looks_like_header(last):
            continue

        prior_widths = [line.width for line in prior if line.width > 0]
        if not prior_widths:
            continue
        median_width = statistics.median(prior_widths)
        ratio = last.width / median_width if median_width else 1.0

        reason: str | None = None
        if last.word_count <= 2 and ratio < 0.50:
            reason = "1-2 word orphan"
        elif last.word_count == 3 and ratio < 0.35:
            reason = "3-word jagged wrap"
        elif ratio < 0.22:
            reason = "very short final line"

        if reason:
            flagged.append(
                FlaggedLine(
                    page=page,
                    reason=reason,
                    ratio=ratio,
                    word_count=last.word_count,
                    text=last.text,
                )
            )

    flagged.sort(key=lambda item: (item.page, item.reason, item.ratio, item.text))
    return flagged


def main() -> int:
    args = parse_args()
    require_tool("pdftoppm")
    require_tool("tesseract")

    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    if args.keep_images:
        temp_dir = Path(tempfile.mkdtemp(prefix="resume-wrap-check-"))
    else:
        temp_dir_ctx = tempfile.TemporaryDirectory(prefix="resume-wrap-check-")
        temp_dir = Path(temp_dir_ctx.name)

    pages = render_pdf_to_pngs(pdf_path, temp_dir)
    all_words: list[WordBox] = []
    for page in pages:
        all_words.extend(run_tesseract_tsv(page))

    lines = build_lines(all_words)
    flagged = flag_jagged_lines(lines)

    print(f"PDF: {pdf_path}")
    print(f"Pages rendered: {len(pages)}")
    print(f"Flagged lines: {len(flagged)}")
    if args.keep_images:
        print(f"Rendered page images: {temp_dir}")
    print()

    if not flagged:
        print("No likely orphan/jagged wrap lines detected.")
        return 0

    for item in flagged:
        print(
            f"page {item.page} | {item.reason} | words={item.word_count} | "
            f"ratio={item.ratio:.2f} | {item.text}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

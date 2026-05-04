#!/usr/bin/env python3
"""Normalize Word styles so new text stays in Calibri without rewriting the theme."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
import re
import xml.etree.ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"

IGNORABLE_NAMESPACES = {
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16": "http://schemas.microsoft.com/office/word/2018/wordml",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
    "w16sdtdh": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash",
    "w16sdtfl": "http://schemas.microsoft.com/office/word/2024/wordml/sdtformatlock",
    "w16du": "http://schemas.microsoft.com/office/word/2023/wordml/word16du",
}

NS = {"w": W_NS}

ET.register_namespace("w", W_NS)
ET.register_namespace("mc", MC_NS)


def ensure_rfonts(parent: ET.Element) -> ET.Element:
    rfonts = parent.find("w:rFonts", NS)
    if rfonts is None:
        rfonts = ET.SubElement(parent, f"{{{W_NS}}}rFonts")
    return rfonts


def set_calibri_rfonts(rfonts: ET.Element) -> None:
    rfonts.set(f"{{{W_NS}}}ascii", "Calibri")
    rfonts.set(f"{{{W_NS}}}eastAsia", "Calibri")
    rfonts.set(f"{{{W_NS}}}hAnsi", "Calibri")
    rfonts.set(f"{{{W_NS}}}cs", "Calibri")
    for attr in (
        f"{{{W_NS}}}asciiTheme",
        f"{{{W_NS}}}eastAsiaTheme",
        f"{{{W_NS}}}hAnsiTheme",
        f"{{{W_NS}}}cstheme",
    ):
        rfonts.attrib.pop(attr, None)


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"w:{tag}", NS)
    if child is None:
        child = ET.SubElement(parent, f"{{{W_NS}}}{tag}")
    return child


def set_style_color(rpr: ET.Element, color: str) -> None:
    color_el = ensure_child(rpr, "color")
    color_el.set(f"{{{W_NS}}}val", color)
    for attr in (
        f"{{{W_NS}}}themeColor",
        f"{{{W_NS}}}themeShade",
        f"{{{W_NS}}}themeTint",
    ):
        color_el.attrib.pop(attr, None)


def set_style_size(rpr: ET.Element, half_points: str) -> None:
    for tag in ("sz", "szCs"):
        size_el = ensure_child(rpr, tag)
        size_el.set(f"{{{W_NS}}}val", half_points)


def patch_heading_style(root: ET.Element, style_id: str, *, color: str, size: str) -> None:
    style = root.find(f"w:style[@w:styleId='{style_id}']", NS)
    if style is None:
        return

    rpr = style.find("w:rPr", NS)
    if rpr is None:
        rpr = ET.SubElement(style, f"{{{W_NS}}}rPr")

    set_calibri_rfonts(ensure_rfonts(rpr))
    set_style_color(rpr, color)
    set_style_size(rpr, size)


def patch_styles(styles_xml: bytes, *, body_size: str = "22") -> bytes:
    root = ET.fromstring(styles_xml)

    rpr_default = root.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
    if rpr_default is not None:
        set_calibri_rfonts(ensure_rfonts(rpr_default))
        set_style_size(rpr_default, body_size)

    for style_id in ("Normal", "DefaultParagraphFont"):
        style = root.find(f"w:style[@w:styleId='{style_id}']", NS)
        if style is None:
            continue
        rpr = style.find("w:rPr", NS)
        if rpr is None:
            rpr = ET.SubElement(style, f"{{{W_NS}}}rPr")
        set_calibri_rfonts(ensure_rfonts(rpr))
        set_style_size(rpr, body_size)

    patch_heading_style(root, "Heading1", color="4F81BD", size="28")
    patch_heading_style(root, "Heading2", color="4F81BD", size="24")
    patch_heading_style(root, "Heading3", color="4F81BD", size="22")

    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
    xml = ensure_ignorable_namespace_declarations(xml)
    return xml.encode("utf-8")


def ensure_ignorable_namespace_declarations(xml: str) -> str:
    # ElementTree drops unused namespace declarations, but Word still expects the
    # prefixes referenced by mc:Ignorable to be declared on the root element.
    xml = xml.replace(
        'xmlns:ns1="http://schemas.openxmlformats.org/markup-compatibility/2006"',
        f'xmlns:mc="{MC_NS}"',
        1,
    )
    xml = xml.replace("ns1:Ignorable=", "mc:Ignorable=", 1)

    match = re.search(r"<w:styles\b([^>]*)>", xml, flags=re.DOTALL)
    if not match:
        return xml

    root_tag = match.group(0)
    insertions = []
    for prefix, uri in IGNORABLE_NAMESPACES.items():
        decl = f'xmlns:{prefix}="{uri}"'
        if decl not in root_tag:
            insertions.append(decl)

    if not insertions:
        return xml

    replacement = root_tag[:-1] + " " + " ".join(insertions) + ">"
    return xml.replace(root_tag, replacement, 1)


def patch_docx(path: Path, *, body_size: str = "22") -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(path, "r") as src, zipfile.ZipFile(temp_path, "w") as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/styles.xml":
                data = patch_styles(data, body_size=body_size)
            dst.writestr(item, data)
    temp_path.replace(path)


def main(argv: list[str]) -> int:
    body_size = "22"
    paths = argv[1:]

    if len(paths) >= 2 and paths[0] == "--body-half-points":
        body_size = paths[1]
        paths = paths[2:]

    if len(paths) < 1:
        print(
            "Usage: fix_docx_calibri_defaults.py [--body-half-points 22] <docx> [<docx> ...]",
            file=sys.stderr,
        )
        return 1

    for raw_path in paths:
        path = Path(raw_path)
        patch_docx(path, body_size=body_size)
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

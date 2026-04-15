#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape
import shutil
import subprocess
import textwrap
import zipfile
import xml.etree.ElementTree as ET


WORKSPACE = Path("/Users/chris/2026 Resumes")
SEND_TO_DIR = WORKSPACE / "Send To"
TRACKER = WORKSPACE / "bak" / "2026 Job Search.xlsx"
TEMPLATE_DOCX = WORKSPACE / "CANONICAL - Chris Tallent Resume - Principal Engineer.docx"
REVIEW_FILE = WORKSPACE / "Review List - 20260412.md"
TODAY_STAMP = "20260412"

DATE_FORMAT = "mm/dd/yy;@"
XLSX_NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

NS = (
    'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
    'xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" '
    'xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" '
    'xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" '
    'xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" '
    'xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" '
    'xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" '
    'xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" '
    'xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" '
    'xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" '
    'xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:oel="http://schemas.microsoft.com/office/2019/extlst" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
    'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
    'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" '
    'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
    'xmlns:w16du="http://schemas.microsoft.com/office/word/2023/wordml/word16du" '
    'xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" '
    'xmlns:w16sdtfl="http://schemas.microsoft.com/office/word/2024/wordml/sdtformatlock" '
    'xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" '
    'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
    'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
    'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
    'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
    'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh w16sdtfl w16du wp14"'
)

SECT_PR = (
    '<w:sectPr w:rsidR="00565ADA" w:rsidSect="00034616">'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="864" w:right="864" w:bottom="864" w:left="864" w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/>'
    '<w:docGrid w:linePitch="360"/>'
    "</w:sectPr>"
)


@dataclass(frozen=True)
class Experience:
    title: str
    location_dates: str
    bullets: list[str]


@dataclass(frozen=True)
class RoleSpec:
    company: str
    role: str
    folder_name: str
    headline: str
    summary: str
    skills: list[str]
    experiences: list[Experience]
    lane: str
    work_model: str
    compensation: str
    fit: str
    risk: str
    link: str
    source: str
    questions: list[str]
    tracker_type: str = "Full time"
    next_steps: str = "Tailored resume drafted; review and apply"
    ref_number: str = ""


def sanitize_filename(value: str) -> str:
    return value.replace("/", " - ").replace(":", " -")


def p(text: str, style: str | None = None, center: bool = False, italic: bool = False, spacing_before: int | None = None, spacing_after: int | None = None) -> str:
    props: list[str] = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if spacing_before is not None or spacing_after is not None:
        attrs: list[str] = []
        if spacing_before is not None:
            attrs.append(f'w:before="{spacing_before}"')
        if spacing_after is not None:
            attrs.append(f'w:after="{spacing_after}"')
        props.append(f"<w:spacing {' '.join(attrs)}/>")
    if center:
        props.append('<w:jc w:val="center"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else "<w:pPr/>"
    run_props = ""
    if italic:
        run_props = "<w:rPr><w:i/><w:iCs/></w:rPr>"
    return (
        "<w:p>"
        f"{ppr}"
        "<w:r>"
        f"{run_props}"
        f"<w:t>{escape(text)}</w:t>"
        "</w:r>"
        "</w:p>"
    )


def bullet(text: str) -> str:
    return p(text, style="ListBullet")


def page_break() -> str:
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def build_document_xml(spec: RoleSpec) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f"<w:document {NS}>",
        "<w:body>",
        p("CHRIS TALLENT", style="Heading1", center=True, spacing_before=120, spacing_after=40),
        p(spec.headline, center=True, italic=True, spacing_before=40, spacing_after=40),
        p("Cincinnati Metro Area • 859.394.2923 • chris@provenedge.com • linkedin.com/in/tallented", center=True, spacing_before=40, spacing_after=40),
        p("──────────────────────────────────────────────────────────────────────────────────────────────────"),
        p("PROFESSIONAL SUMMARY", style="Heading2", spacing_before=280),
        p(spec.summary),
        p("CORE SKILLS", style="Heading2", spacing_before=280),
    ]
    parts.extend(p(line, spacing_after=120) for line in spec.skills)
    parts.append(p("PROFESSIONAL EXPERIENCE", style="Heading2", spacing_before=280))

    for exp in spec.experiences:
        parts.append(p(exp.title, style="Heading3"))
        parts.append(p(exp.location_dates, spacing_after=40))
        parts.extend(bullet(item) for item in exp.bullets)

    parts.append(p("EDUCATION", style="Heading2", spacing_before=280))
    parts.append(p("Bachelor of Science in Computer Science — University of Kentucky, Lexington, KY"))
    parts.append(SECT_PR)
    parts.append("</w:body></w:document>")
    return "".join(parts)


def build_markdown(spec: RoleSpec) -> str:
    lines = [
        "# CHRIS TALLENT",
        "",
        f"*{spec.headline}*",
        "",
        "Cincinnati Metro Area • 859.394.2923 • chris@provenedge.com • linkedin.com/in/tallented",
        "",
        "──────────────────────────────────────────────────────────────────────────────────────────────────",
        "",
        "## PROFESSIONAL SUMMARY",
        "",
        spec.summary,
        "",
        "## CORE SKILLS",
        "",
    ]
    lines.extend(spec.skills)
    lines.extend(["", "## PROFESSIONAL EXPERIENCE", ""])
    for exp in spec.experiences:
        lines.append(f"### {exp.title}")
        lines.append("")
        lines.append(exp.location_dates)
        lines.append("")
        lines.extend(f"- {item}" for item in exp.bullets)
        lines.append("")
    lines.extend(["## EDUCATION", "", "Bachelor of Science in Computer Science — University of Kentucky, Lexington, KY", ""])
    return "\n".join(lines)


def build_job_description(spec: RoleSpec) -> str:
    return textwrap.dedent(
        f"""\
        {spec.company} - {spec.role}
        Source queue: Review List - 20260412.md
        URL: {spec.link}

        Lane: {spec.lane}
        Work model: {spec.work_model}
        Compensation: {spec.compensation}
        Listing source: {spec.source}

        Fit:
        {spec.fit}

        Risk / stretch:
        {spec.risk}
        """
    )


def build_questions(spec: RoleSpec) -> str:
    lines = [
        f"# {spec.company} - {spec.role}",
        "",
        "Follow-up questions to tighten the resume further if needed:",
        "",
    ]
    lines.extend(f"- {question}" for question in spec.questions)
    lines.append("")
    return "\n".join(lines)


def write_docx(target_docx: Path, document_xml: str) -> None:
    replace_zip_member(target_docx, "word/document.xml", document_xml.encode("utf-8"))


def replace_zip_member(zip_path: Path, member_name: str, data: bytes) -> None:
    temp_path = zip_path.with_suffix(zip_path.suffix + ".tmp")
    with zipfile.ZipFile(zip_path, "r") as src, zipfile.ZipFile(temp_path, "w") as dst:
        for item in src.infolist():
            if item.filename == member_name:
                dst.writestr(item, data)
            else:
                dst.writestr(item, src.read(item.filename))
    temp_path.replace(zip_path)


def refresh_cache(docx_path: Path) -> None:
    rel = docx_path.relative_to(WORKSPACE)
    cache_path = WORKSPACE / "_resume_text" / f"{rel}.txt"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["/usr/bin/textutil", "-convert", "txt", "-stdout", str(docx_path)],
        check=True,
        capture_output=True,
    )
    cache_path.write_bytes(result.stdout)


def parse_shared_strings(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    strings: list[str] = []
    for si in root.findall("main:si", XLSX_NS):
        text_parts = [node.text or "" for node in si.findall(".//main:t", XLSX_NS)]
        strings.append("".join(text_parts))
    return strings


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "s":
        value = cell.findtext("main:v", default="", namespaces=XLSX_NS)
        if not value:
            return ""
        return shared_strings[int(value)]
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//main:t", XLSX_NS))
    return cell.findtext("main:v", default="", namespaces=XLSX_NS)


def excel_serial(value: date) -> int:
    return (value - date(1899, 12, 30)).days


def inline_cell(ref: str, style: int, text: str) -> ET.Element:
    cell = ET.Element("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c", {"r": ref, "s": str(style), "t": "inlineStr"})
    is_node = ET.SubElement(cell, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is")
    t_node = ET.SubElement(is_node, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
    t_node.text = text
    return cell


def numeric_cell(ref: str, style: int, value: int) -> ET.Element:
    cell = ET.Element("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c", {"r": ref, "s": str(style)})
    v_node = ET.SubElement(cell, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
    v_node.text = str(value)
    return cell


def append_tracker_rows(specs: Iterable[RoleSpec]) -> list[str]:
    created_date = datetime.strptime(TODAY_STAMP, "%Y%m%d").date()
    with zipfile.ZipFile(TRACKER, "r") as zf:
        sheet_xml = zf.read("xl/worksheets/sheet1.xml")
        shared_strings_xml = zf.read("xl/sharedStrings.xml")

    shared_strings = parse_shared_strings(shared_strings_xml)
    ET.register_namespace("", XLSX_NS["main"])
    ET.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006")
    ET.register_namespace("x14ac", "http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac")
    ET.register_namespace("xr", "http://schemas.microsoft.com/office/spreadsheetml/2014/revision")
    ET.register_namespace("xr2", "http://schemas.microsoft.com/office/spreadsheetml/2015/revision2")
    ET.register_namespace("xr3", "http://schemas.microsoft.com/office/spreadsheetml/2016/revision3")
    root = ET.fromstring(sheet_xml)
    sheet_data = root.find("main:sheetData", XLSX_NS)
    if sheet_data is None:
        raise RuntimeError("Submissions sheetData not found")

    rows = sheet_data.findall("main:row", XLSX_NS)
    max_row = max(int(row.attrib["r"]) for row in rows)
    existing: set[tuple[str, str]] = set()
    for row in rows[1:]:
        company = ""
        title = ""
        for cell in row.findall("main:c", XLSX_NS):
            ref = cell.attrib.get("r", "")
            if ref.startswith("A"):
                company = cell_text(cell, shared_strings).strip().lower()
            elif ref.startswith("E"):
                title = cell_text(cell, shared_strings).strip().lower()
        if company or title:
            existing.add((company, title))

    appended: list[str] = []
    for spec in specs:
        key = (spec.company.strip().lower(), spec.role.strip().lower())
        if key in existing:
            continue
        max_row += 1
        row = ET.Element(
            "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row",
            {"r": str(max_row), "spans": "1:12", "ht": "17", "{http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac}dyDescent": "0.2"},
        )
        row.append(inline_cell(f"A{max_row}", 3, spec.company))
        row.append(inline_cell(f"B{max_row}", 3, "CREATED"))
        row.append(numeric_cell(f"C{max_row}", 11, excel_serial(created_date)))
        row.append(inline_cell(f"E{max_row}", 3, spec.role))
        row.append(inline_cell(f"F{max_row}", 3, spec.tracker_type))
        row.append(inline_cell(f"G{max_row}", 3, spec.work_model))
        row.append(inline_cell(f"H{max_row}", 3, spec.compensation))
        row.append(inline_cell(f"I{max_row}", 5, spec.next_steps))
        row.append(inline_cell(f"J{max_row}", 3, spec.source))
        if spec.ref_number:
            row.append(inline_cell(f"K{max_row}", 3, spec.ref_number))
        row.append(inline_cell(f"L{max_row}", 3, spec.link))
        sheet_data.append(row)
        existing.add(key)
        appended.append(f"{spec.company} | {spec.role}")

    dimension = root.find("main:dimension", XLSX_NS)
    if dimension is not None:
        dimension.set("ref", f"A1:L{max_row}")

    replace_zip_member(TRACKER, "xl/worksheets/sheet1.xml", ET.tostring(root, encoding="utf-8", xml_declaration=True))
    return appended


def role_questions(*items: str) -> list[str]:
    return list(items)


PITCHSTONE_AI = [
    "Scaled engineering from 6 to roughly 35 across four agile teams, establishing delivery cadence, team structure, and technical ownership.",
    "Architected an AI-enabled, configuration-driven real-estate platform on AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3), exposing secure APIs for document workflows and knowledge-based retrieval.",
    "Built Bedrock knowledge workflows plus Textract / Comprehend-based lease extraction, turning workflow-heavy business problems into governed product capabilities.",
    "Drove AI-assisted engineering with Claude Code for upgrades, test generation, and modernization planning, reducing delivery cycles from 4 months to 3 weeks.",
    "Defined AWS account structure, RBAC, IAM Identity Center permission sets, and access boundaries across five AWS accounts while leading ISO 27001 controls and vulnerability remediation.",
    "Built Docker Compose-based local developer environments with anonymized data refresh, cutting update time from 3+ hours to 45 minutes and improving environment parity.",
    "Partnered with product, UX, and customer stakeholders on roadmap priorities, API design, technical risk, and production operations.",
]

PITCHSTONE_SECURITY = [
    "Architected an AI-enabled, configuration-driven real-estate platform on AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3), exposing secure APIs and governed document workflows.",
    "Defined AWS account structure, RBAC, IAM Identity Center permission sets, and access boundaries across five AWS accounts while leading ISO 27001 controls and vulnerability remediation.",
    "Owned cloud security operations including pen-test coordination, remediation prioritization, and continuous monitoring with Secureframe, Security Hub, GuardDuty, and Inspector.",
    "Built Docker Compose-based developer environments with anonymized data refresh, cutting update time from 3+ hours to 45 minutes and improving release safety.",
    "Restructured CI/CD automation and optimized ECS infrastructure, reducing non-production costs by 35–40% while improving deployment reliability.",
    "Scaled engineering from 6 to roughly 35 across four agile teams, establishing delivery cadence, team structure, and technical ownership.",
]

ACS_CORE = [
    "Modernized a legacy PHP fintech platform into a modern single-page application backed by REST APIs and microservices (AngularJS, Java, Spring MVC, Docker / Kubernetes on AWS), achieving 99.99% uptime with zero-downtime migration from legacy systems.",
    "Implemented CI/CD pipelines with Bitbucket Pipelines and GitHub Actions, shortening deployment cycles from weeks to hours through Kubernetes rolling updates and safer rollback strategies.",
    "Designed a JSON-driven configuration system for financial settings and visual theming, enabling dealer-specific workflows and UI behavior without per-client code forks.",
    "Delivered the NADA 2017 proof-of-concept in two months under a hard business deadline.",
]

PROVEN_EDGE_AI = [
    "Built a reusable multi-platform application scaffold across web, mobile, desktop, API, and AI services, with typed APIs, OIDC auth, RBAC, billing, documents, notifications, and webhooks.",
    "Built Model Context Protocol (MCP)-integrated agent tooling on top of the scaffold and Entity Engine, enabling LLM-driven tools to query structured entity data and perform bounded admin actions through typed APIs.",
    "Implemented generative search over help docs using chunking, embeddings, and a Python vector store, grounding responses in linked source documentation.",
    "Engineered a React / Next.js / Prisma MVP for a legal SaaS platform under tight launch deadlines.",
]

PROVEN_EDGE_PLATFORM = [
    "Built a reusable multi-platform application scaffold across web, mobile, desktop, API, and AI services, with typed APIs, OIDC auth, RBAC, billing, documents, notifications, and webhooks.",
    "Built Model Context Protocol (MCP)-integrated agent tooling on top of the scaffold and Entity Engine, enabling bounded admin actions through typed APIs and structured data access.",
    "Deployed CI/CD pipelines with container orchestration (Docker Compose / ECS) to improve staging-production parity and release confidence.",
    "Modernized a golf-handicapping SaaS platform (Angular, Java, MySQL) for thousands of users, adding automated scoring, cheat evaluation, and multi-source data aggregation.",
]

GLAMHIVE_CORE = [
    "Engineered and launched Glamhive.com on AWS (AngularJS, Java, Spring MVC, MongoDB), integrating external product inventory through a configuration-driven platform.",
    "Designed data model and indexing strategy for real-time search and personalized recommendations via MongoDB aggregation and caching.",
    "Unified web and mobile codebases via Cordova and Ionic, reducing mobile development costs by 70%.",
]

LELA_CORE = [
    "Directed development of a personalized shopping recommendation platform (Java, Spring MVC, MySQL, MongoDB) with multi-retailer integrations.",
    "Refactored core recommendation algorithms into modular Java services, improving maintainability and enabling feature A/B testing.",
    "Improved post-pivot delivery efficiency by 25% through Agile workflows, automated testing, and roadmap alignment.",
]


def exec_experiences(ai: bool = True, security: bool = False) -> list[Experience]:
    pitchstone = PITCHSTONE_SECURITY if security else PITCHSTONE_AI
    proven_edge = PROVEN_EDGE_PLATFORM if security else PROVEN_EDGE_AI
    return [
        Experience("Chief Technology Officer & Principal Engineer | Pitchstone Technology LLC", "Seattle, WA • February 2021 – Present", list(pitchstone)),
        Experience("Chief Technology Officer | Automobile Consumer Services Inc", "Cincinnati, OH • July 2016 – February 2021", list(ACS_CORE)),
        Experience("Fractional CTO & Principal Engineer | Proven Edge LLC", "Fort Thomas, KY • November 2015 – Present", list(proven_edge)),
        Experience("Technical Co-Founder & Chief Technology Officer | Glamhive", "Seattle, WA • November 2013 – November 2015", list(GLAMHIVE_CORE)),
        Experience("Chief Technology Officer | Lela.com", "New York, NY • November 2011 – May 2014", list(LELA_CORE)),
    ]


def management_experiences() -> list[Experience]:
    return [
        Experience("Chief Technology Officer & Principal Engineer | Pitchstone Technology LLC", "Seattle, WA • February 2021 – Present", [
            "Built Docker Compose-based local developer environments with anonymized data refresh, cutting update time from 3+ hours to 45 minutes and improving environment parity.",
            "Defined AWS account structure, RBAC, IAM Identity Center permission sets, and access boundaries across five AWS accounts while leading ISO 27001 controls and vulnerability remediation.",
            "Restructured CI/CD automation and optimized ECS infrastructure, reducing non-production costs by 35–40% while improving deployment reliability.",
            "Architected an AI-enabled, configuration-driven real-estate platform on AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3), exposing secure APIs for document and knowledge workflows.",
            "Partnered with product, UX, and customer stakeholders on roadmap priorities, API design, technical risk, and production operations.",
        ]),
        Experience("Chief Technology Officer | Automobile Consumer Services Inc", "Cincinnati, OH • July 2016 – February 2021", [
            "Modernized a legacy PHP fintech platform into a modern single-page application backed by REST APIs and microservices (AngularJS, Java, Spring MVC, Docker / Kubernetes on AWS), achieving 99.99% uptime with zero-downtime migration.",
            "Implemented CI/CD pipelines with Bitbucket Pipelines and GitHub Actions, shortening deployment cycles from weeks to hours through Kubernetes rolling updates and safer rollback strategies.",
            "Designed a JSON-driven configuration system for dealer-specific workflows and UI behavior without per-client code forks.",
        ]),
        Experience("Fractional CTO & Principal Engineer | Proven Edge LLC", "Fort Thomas, KY • November 2015 – Present", [
            "Built Model Context Protocol (MCP)-integrated agent tooling on top of an internal application scaffold, enabling bounded admin actions through typed APIs.",
            "Deployed CI/CD pipelines with container orchestration (Docker Compose / ECS) to improve staging-production parity and release confidence.",
            "Built a reusable multi-platform application scaffold spanning web, mobile, desktop, API, and AI services with OIDC auth, RBAC, billing, and notifications.",
            "Modernized a golf-handicapping SaaS platform (Angular, Java, MySQL) for thousands of users, adding automated scoring, cheat evaluation, and multi-source data aggregation.",
        ]),
        Experience("Technical Co-Founder & Chief Technology Officer | Glamhive", "Seattle, WA • November 2013 – November 2015", list(GLAMHIVE_CORE)),
        Experience("Chief Technology Officer | Lela.com", "New York, NY • November 2011 – May 2014", list(LELA_CORE)),
    ]


def principal_experiences() -> list[Experience]:
    return [
        Experience("Chief Technology Officer & Principal Engineer | Pitchstone Technology LLC", "Seattle, WA • February 2021 – Present", [
            "Architected an AI-enabled, configuration-driven platform on AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3), exposing secure APIs for document and knowledge workflows.",
            "Built Model Context Protocol (MCP)-adjacent agent tooling and bounded workflow automation patterns that connect LLMs to typed APIs and structured data.",
            "Built AI-assisted modernization workflows with Claude Code for upgrades and unit-test generation, reducing delivery cycles from 4 months to 3 weeks.",
            "Defined AWS account structure, RBAC, IAM Identity Center permission sets, and access boundaries across five AWS accounts while leading ISO 27001 controls.",
            "Built Docker Compose-based developer environments with anonymized data refresh, cutting update time from 3+ hours to 45 minutes.",
        ]),
        Experience("Chief Technology Officer | Automobile Consumer Services Inc", "Cincinnati, OH • July 2016 – February 2021", [
            "Modernized a legacy PHP fintech platform into a modern single-page application backed by REST APIs and microservices (AngularJS, Java, Spring MVC, Docker / Kubernetes on AWS), achieving 99.99% uptime with zero-downtime migration.",
            "Implemented CI/CD pipelines with Bitbucket Pipelines and GitHub Actions, shortening deployment cycles from weeks to hours through Kubernetes rolling updates and safer rollback strategies.",
            "Designed a JSON-driven configuration system for dealer-specific workflows and UI behavior without per-client code forks.",
        ]),
        Experience("Fractional CTO & Principal Engineer | Proven Edge LLC", "Fort Thomas, KY • November 2015 – Present", [
            "Built Model Context Protocol (MCP)-integrated agent tooling on top of an internal multi-platform application scaffold and Entity Engine, enabling LLM-driven tools to query structured entity data and perform bounded admin actions through typed APIs.",
            "Implemented generative search over help docs using chunking, embeddings, and a Python vector store, grounding responses in linked source documentation.",
            "Built a reusable multi-platform application scaffold across web, mobile, desktop, API, and AI services, with typed APIs, OIDC auth, RBAC, billing, documents, notifications, and RAG support.",
            "Engineered a React / Next.js / Prisma MVP for a legal SaaS platform under tight launch deadlines.",
        ]),
        Experience("Technical Co-Founder & Chief Technology Officer | Glamhive", "Seattle, WA • November 2013 – November 2015", list(GLAMHIVE_CORE)),
        Experience("Chief Technology Officer | Lela.com", "New York, NY • November 2011 – May 2014", list(LELA_CORE)),
    ]


ROLE_SPECS: list[RoleSpec] = [
    RoleSpec(
        company="Zapier",
        role="Sr. Director, Engineering - Applied AI",
        folder_name="20260412 - Zapier - Sr. Director, Engineering - Applied AI",
        headline="Senior Director Engineering | Applied AI Platforms & Workflow Systems",
        summary="Engineering leader and hands-on CTO with 20+ years building cloud-native platforms, workflow systems, and AI-enabled products. Proven record scaling teams, modernizing legacy systems, and shipping governed AI capabilities on AWS using Java, Python, and TypeScript. Brings a product-and-platform mindset across developer tooling, secure APIs, document workflows, and cross-functional execution with product, operations, customers, and executives.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "Applied AI: MCP / Agent Tooling • Agentic Workflows • RAG / Knowledge Systems • Document Intelligence",
            "Platform & Governance: Developer Platforms • Secure APIs • RBAC / Auditability • Reliability / Observability",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote",
        compensation="US $373.2K-$559.8K base + equity + bonus",
        fit="Strong overlap on applied AI platform leadership, workflow automation, developer systems, and remote-first scale credibility.",
        risk="Likely wants deeper second-line leadership and larger-org proof than the cleanest bridge roles.",
        link="https://jobs.ashbyhq.com/zapier/de99b0f0-bdb9-4969-a9c5-a5d0bc2722b2/",
        source="Ashby",
        questions=role_questions(
            "Which Pitchstone or Proven Edge examples best show AI workflow adoption beyond a single team or prototype?",
            "Do you have any stronger metrics around internal-tool leverage, developer productivity, or workflow-throughput gains?",
            "What is the clearest example of shaping an AI product with Product and Design peers rather than only engineering delivery?",
            "Is there a stronger story around mentoring managers or principal-level engineers that should be surfaced for director scope?",
        ),
    ),
    RoleSpec(
        company="1Password",
        role="Senior Director Engineering, Identity Security Platform Infrastructure",
        folder_name="20260412 - 1Password - Senior Director Engineering, Identity Security Platform Infrastructure",
        headline="Senior Director Engineering | Identity Security Platforms & Cloud Infrastructure",
        summary="Senior engineering leader and hands-on CTO with 20+ years building secure cloud platforms, access-control systems, and compliance-aware delivery organizations. Experience spans platform modernization, RBAC and identity boundaries, AWS governance, developer tooling, and multi-team execution across Java, Python, and TypeScript. Brings a pragmatic operator’s mindset to security, reliability, cost, and cross-functional alignment.",
        skills=[
            "Leadership: Org Leadership • Manager Development • Cross-Functional Delivery • Technical Strategy",
            "Platform & Security: Identity / Access Controls • Cloud Security • Developer Platforms • Reliability & Incident Response",
            "Governance: Auditability • Compliance-Aware Systems • RBAC / Permission Models • Infrastructure Modernization",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Docker / Kubernetes • Java / Spring • Python • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(security=True),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote US",
        compensation="US $272K-$408K base + equity + incentive eligibility",
        fit="Strong bridge role for platform, identity, security, cloud infrastructure, and larger-org leadership at a recognizable brand.",
        risk="The bar is likely high on prior scale, identity/security depth, and manager-of-managers evidence.",
        link="https://jobs.ashbyhq.com/1password/ff98345b-cc1a-4be9-8fd8-89ed85c7bf89/",
        source="Ashby",
        questions=role_questions(
            "What are the strongest examples of identity, SSO, RBAC, or permission-boundary decisions you personally led?",
            "Do you have any stronger examples of managing through managers or building multiple leadership layers?",
            "Which security/compliance wins can be framed as platform-infrastructure outcomes rather than only audit work?",
            "Is there a better story around infrastructure budgeting, cloud cost controls, or platform reliability targets?",
        ),
    ),
    RoleSpec(
        company="Confluent",
        role="Director of Engineering, Governance",
        folder_name="20260412 - Confluent - Director of Engineering, Governance",
        headline="Director of Engineering | Governance Platforms, Reliability & Applied AI",
        summary="Engineering leader and hands-on CTO with 20+ years building cloud-native platforms, governed workflow systems, and compliance-aware product capabilities. Proven record modernizing legacy systems, scaling delivery teams, and shipping secure APIs and AI-assisted workflows on AWS using Java, Python, and TypeScript. Brings a platform-and-governance mindset across reliability, auditability, developer tooling, and cross-functional execution.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "Governance: Auditability • Access Controls / RBAC • Platform Standards • Reliability / Observability",
            "Applied AI: MCP / Agent Tooling • RAG / Knowledge Systems • Document Intelligence • Workflow Automation",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(security=True),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote U.S.",
        compensation="$322.5K-$387K base + equity",
        fit="Strong match on platform governance, reliability, security/compliance adjacency, and executive-operating narrative.",
        risk="Likely wants deeper manager-of-managers depth than the cleanest bridge roles.",
        link="https://jobs.ashbyhq.com/confluent/2af38283-c25d-4352-9ecb-f56d98af748d",
        source="Ashby",
        questions=role_questions(
            "What governance examples can be framed as platform-enforced standards or guardrails rather than policy work?",
            "Do you have stronger examples of delivery risk management across multiple teams or products?",
            "Which customer-facing or compliance-facing incidents best demonstrate ownership of reliability and governance?",
            "Is there a stronger story around technical strategy reviews, architecture councils, or cross-team standards setting?",
        ),
    ),
    RoleSpec(
        company="1Password",
        role="Director of Engineering - Enterprise Password Manager (EPM)",
        folder_name="20260412 - 1Password - Director of Engineering - Enterprise Password Manager",
        headline="Director of Engineering | Security Product Platforms & Identity Systems",
        summary="Engineering leader and hands-on CTO with 20+ years building secure SaaS platforms, access-controlled systems, and developer-first delivery environments. Experience spans product modernization, RBAC and identity boundaries, cloud governance, and cross-functional execution across Java, Python, and TypeScript. Brings a pragmatic blend of product thinking, platform discipline, and security awareness.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "Security Product Platforms: Identity / Access Controls • Secure APIs • Cloud Security • Reliability / Incident Response",
            "Governance: Auditability • RBAC / Permission Models • Compliance-Aware Delivery • Platform Standards",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Docker / Kubernetes • Java / Spring • Python • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(security=True),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote U.S. / Canada",
        compensation="US $246K-$369K base + equity + incentive eligibility",
        fit="Strong brand plus director scope and credible alignment to security, product, platform, and access-control systems.",
        risk="More product / credential-management focused than broader platform-transformation leadership.",
        link="https://jobs.ashbyhq.com/1password/d6acb733-8988-4a8b-b025-a057144ab12b/",
        source="Ashby",
        questions=role_questions(
            "What are the strongest examples of customer-facing secure product decisions or trust-sensitive workflows you led?",
            "Do you have examples of translating security or compliance constraints into product/platform design choices?",
            "Which role best demonstrates product partnership with design and PM on user-facing security features?",
            "Is there a stronger enterprise-customer or regulated-customer story that should be surfaced here?",
        ),
    ),
    RoleSpec(
        company="Natera",
        role="Vice President of Engineering, UX/Commercial Applications",
        folder_name="20260412 - Natera - Vice President of Engineering, UX-Commercial Applications",
        headline="Vice President Engineering | Product Delivery, Platform Modernization & AI-Enabled Systems",
        summary="Technology executive with 20+ years leading software delivery, platform modernization, and AI-enabled product development across startup and growth environments. Proven record scaling teams, improving delivery systems, modernizing legacy platforms, and aligning engineering execution with business outcomes across Java, Python, TypeScript, and AWS. Brings practical strength in multi-team leadership, delivery governance, reliability, and cross-functional partnership.",
        skills=[
            "Leadership: Org Leadership • Hiring & Team Building • Multi-Team Delivery • Technical Strategy",
            "Execution & Governance: Delivery Systems • Modernization • Reliability • Cross-Functional Operating Rhythm",
            "Applied AI: Workflow Automation • Document Intelligence • AI-Assisted SDLC • MCP / Agent Tooling",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1",
        work_model="Remote U.S.",
        compensation="Undisclosed",
        fit="One of the strongest direct bridge roles surfaced live, with 100+ engineer scope through directors and senior directors plus modernization and AI-enabled delivery themes.",
        risk="Healthcare/commercial-applications domain is less obviously aligned with the preferred software-platform narrative, and compensation still needs validation.",
        link="https://www.linkedin.com/jobs/view/4378135368/",
        source="LinkedIn",
        questions=role_questions(
            "What examples best show leadership through managers or directors, even if the org was smaller?",
            "Do you have stronger stories around executive cadence with revenue, operations, or customer-facing teams?",
            "Which delivery-system changes most clearly improved execution quality, predictability, or business outcomes?",
            "Is there a stronger story around UX-heavy or multi-application product leadership that can offset the healthcare domain gap?",
        ),
    ),
    RoleSpec(
        company="Super.com",
        role="Director of Engineering, Core Experience",
        folder_name="20260412 - Super.com - Director of Engineering, Core Experience",
        headline="Director of Engineering | Product Platforms, Reliability & Delivery Systems",
        summary="Engineering leader and hands-on CTO with 20+ years building cloud-native products, modernizing legacy systems, and improving software delivery across distributed teams. Proven record shipping secure APIs, developer tooling, and AI-enabled workflow capabilities on AWS using Java, Python, and TypeScript. Brings a product-and-platform mindset with strong emphasis on reliability, release quality, and cross-functional execution.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "Product & Platform: Customer Workflows • Secure APIs • Reliability / Observability • Platform Modernization",
            "Applied AI: Workflow Automation • MCP / Agent Tooling • RAG / Knowledge Systems • AI-Assisted SDLC",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote U.S.",
        compensation="US $215K-$316K",
        fit="Recognizable brand, director title, and meaningful consumer-facing scale with solid product and platform overlap.",
        risk="Lower half of the range is below the practical floor, and the role is less clearly governance-heavy than the best bridge roles.",
        link="https://jobs.ashbyhq.com/super.com/ebedcfcc-820e-4a8f-b3d8-891f9a13b96d",
        source="Ashby",
        questions=role_questions(
            "Which examples best demonstrate ownership of customer-critical user journeys or core-product experiences?",
            "Do you have stronger metrics around uptime, performance, or release quality tied to user-facing experiences?",
            "What is the clearest story of partnering with Product and Design to shape a customer-facing roadmap?",
            "Is there a better example of balancing growth features with platform and reliability investments?",
        ),
    ),
    RoleSpec(
        company="Sully.ai",
        role="Head of Engineering, Platform",
        folder_name="20260412 - Sully.ai - Head of Engineering, Platform",
        headline="Head of Engineering | AI Platform, Reliability & Developer Systems",
        summary="Engineering leader and hands-on CTO with 20+ years building cloud-native platforms, workflow-heavy products, and AI-enabled services. Proven record shipping secure APIs, document and knowledge workflows, developer tooling, and modernization programs on AWS using Java, Python, and TypeScript. Brings a strong platform mindset around reliability, observability, delivery systems, and pragmatic AI adoption.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "AI Platform: MCP / Agent Tooling • RAG / Knowledge Systems • Document Intelligence • Workflow Automation",
            "Platform & Reliability: Secure APIs • Developer Platforms • Reliability / Observability • Cost Optimization",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1",
        work_model="Remote U.S.",
        compensation="$300K-$350K base + meaningful equity",
        fit="Strong on AI platform, infrastructure, reliability, and direct platform ownership.",
        risk="May still be closer to startup-scope than true larger-company scale proof.",
        link="https://jobs.ashbyhq.com/sully-ai/056e9f09-ba93-440f-bb3e-d904ffc29d5f?weekdayJdUid=937999",
        source="Ashby",
        questions=role_questions(
            "What platform examples best show you building foundations used by multiple teams or products?",
            "Do you have stronger reliability or latency metrics that can reinforce platform leadership?",
            "Which AI-service decisions most clearly demonstrate production readiness rather than experimentation?",
            "Is there a better story around incident response, on-call maturity, or operational ownership at platform scope?",
        ),
    ),
    RoleSpec(
        company="Socure",
        role="Head of Engineering - Agentic Workflows and Internal Tools",
        folder_name="20260412 - Socure - Head of Engineering - Agentic Workflows and Internal Tools",
        headline="Head of Engineering | Agentic Workflows, Internal Tools & Governance",
        summary="Engineering leader and hands-on CTO with 20+ years building internal platforms, workflow-heavy products, and governed AI-enabled systems. Proven record shipping developer tooling, secure APIs, document intelligence, and automation capabilities on AWS using Java, Python, and TypeScript. Brings a strong operator mindset around reliability, access controls, delivery systems, and bounded AI adoption.",
        skills=[
            "Leadership: Engineering Leadership • Hiring & Team Building • Cross-Functional Delivery • Technical Strategy",
            "Internal Platforms: Developer Tooling • Workflow Automation • Secure APIs • Reliability / Observability",
            "Applied AI: MCP / Agent Tooling • Agentic Workflows • RAG / Knowledge Systems • Document Intelligence",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1",
        work_model="Remote U.S.",
        compensation="$215K-$260K base + equity + bonus",
        fit="Strong alignment to identity/compliance brand, AI and internal-tools positioning, and workflow-system governance.",
        risk="Base is below the practical floor unless the broader package closes the gap.",
        link="https://jobs.ashbyhq.com/socure/15cc89c6-b103-401a-9ec7-2345e69b5e44",
        source="Ashby",
        questions=role_questions(
            "What internal-tool or back-office workflow wins can you quantify beyond engineering-only impact?",
            "Do you have any stronger examples of access controls, auditability, or compliance-aware internal platforms?",
            "Which AI agent or automation examples best show bounded, production-appropriate operational workflows?",
            "Is there a stronger cross-functional story with operations, support, or risk teams that should be surfaced?",
        ),
    ),
    RoleSpec(
        company="A Place for Mom",
        role="Senior Director, Engineering - Senior Living",
        folder_name="20260412 - A Place for Mom - Senior Director, Engineering - Senior Living",
        headline="Senior Director Engineering | Multi-Team Delivery, Reliability & Modernization",
        summary="Senior engineering leader and hands-on CTO with 20+ years improving delivery systems, modernizing legacy platforms, and scaling cloud-native software execution across distributed teams. Proven record building secure APIs, developer tooling, and workflow-heavy product capabilities on AWS using Java, Python, and TypeScript. Brings a pragmatic focus on delivery quality, reliability, and stakeholder alignment.",
        skills=[
            "Leadership: Org Leadership • Hiring & Team Building • Multi-Team Delivery • Technical Strategy",
            "Execution Systems: Delivery Cadence • Modernization • Reliability / Observability • Cross-Functional Partnership",
            "Platform: Secure APIs • Developer Tooling • Workflow Automation • AI-Assisted SDLC",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1",
        work_model="Remote",
        compensation="$215K-$275K base + 30% bonus",
        fit="True senior-director operating role with delivery rigor, multi-team coordination, and stakeholder management.",
        risk="Base alone is below target and the domain is less strategic for long-term positioning.",
        link="https://jobs.ashbyhq.com/a-place-for-mom/21698257-2e73-4349-aba8-4a6cf390d947",
        source="Ashby",
        questions=role_questions(
            "What examples best show managing multiple teams or delivery streams simultaneously?",
            "Do you have stronger stories around service reliability, operational rigor, or stakeholder coordination under pressure?",
            "Which modernization effort best shows business impact beyond technical cleanup?",
            "Is there a stronger narrative around people development or leadership-system building that should be surfaced?",
        ),
    ),
    RoleSpec(
        company="Protege",
        role="VP, Engineering",
        folder_name="20260412 - Protege - VP, Engineering",
        headline="Vice President Engineering | AI Platforms, Delivery Systems & Org Scale",
        summary="Technology executive with 20+ years leading software delivery, platform modernization, and AI-enabled product development across startup and growth environments. Proven record scaling teams, improving delivery systems, and shipping secure workflow capabilities on AWS using Java, Python, and TypeScript. Brings a practical mix of technical depth, organizational leadership, and cross-functional execution.",
        skills=[
            "Leadership: Org Leadership • Hiring & Team Building • Multi-Team Delivery • Technical Strategy",
            "Applied AI: MCP / Agent Tooling • Workflow Automation • RAG / Knowledge Systems • AI-Assisted SDLC",
            "Platform & Governance: Secure APIs • Developer Platforms • Reliability / Observability • Access Controls / RBAC",
            "Technical: AWS (Bedrock, Textract, Comprehend, RDS/Aurora, ECS, Lambda, S3) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(),
        lane="Lane 1",
        work_model="Remote",
        compensation="Not surfaced",
        fit="AI-forward VP title with direct leadership scope and credible product/platform overlap.",
        risk="May be too close to another early-stage executive title rather than the scale jump the strategy is trying to force.",
        link="https://jobs.ashbyhq.com/protege/4b3b5324-3050-46c6-b400-be4b9f05dc24",
        source="Ashby",
        questions=role_questions(
            "What is the strongest evidence that you can position yourself as a growth-stage operator rather than another early-stage CTO?",
            "Do you have clearer examples of budgeting, headcount planning, or organization design that belong on a VP resume?",
            "Which AI-platform stories feel most credible as shipped systems rather than experiments?",
            "Is there a stronger business-outcome narrative tied to platform strategy, margin, or revenue support?",
        ),
    ),
    RoleSpec(
        company="Vanta",
        role="Senior Director, Corporate Engineering",
        folder_name="20260412 - Vanta - Senior Director, Corporate Engineering",
        headline="Senior Director Engineering | Corporate Platforms, Governance & Internal Systems",
        summary="Senior engineering leader and hands-on CTO with 20+ years building secure internal platforms, governance-aware delivery systems, and cloud-native developer tooling. Experience spans access controls, auditability, platform modernization, and cross-functional operations across Java, Python, TypeScript, and AWS. Brings a practical operator’s mindset around reliability, security, delivery systems, and remote-first execution.",
        skills=[
            "Leadership: Org Leadership • Manager Development • Cross-Functional Delivery • Technical Strategy",
            "Corporate Platforms: Internal Systems • Access Controls / RBAC • Governance • Reliability / Incident Response",
            "Developer Enablement: Developer Tooling • Workflow Automation • Platform Modernization • AI-Assisted SDLC",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Docker / Kubernetes • Java / Spring • Python • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(security=True),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote U.S.",
        compensation="Undisclosed",
        fit="Strong brand, senior-director title, and serious operating scope across internal systems, governance, remote workforce support, and compliance-aware platform strategy.",
        risk="Closer to corporate engineering / internal systems than product engineering, so it helps executive-operating credibility more than product-platform narrative.",
        link="https://www.linkedin.com/jobs/view/4323422584/",
        source="LinkedIn",
        questions=role_questions(
            "What internal-platform or enterprise-systems examples best map to corporate engineering scope?",
            "Do you have stronger stories around employee tooling, access governance, or operational enablement outside the core product?",
            "Which compliance or audit efforts can be framed as scalable platform capability rather than one-off project work?",
            "Is there a stronger example of partnering with IT, security, finance, or people-ops stakeholders?",
        ),
    ),
    RoleSpec(
        company="GE HealthCare",
        role="Senior Director - Cloud Infrastructure & Platform Engineering",
        folder_name="20260412 - GE HealthCare - Senior Director - Cloud Infrastructure & Platform Engineering",
        headline="Senior Director Engineering | Cloud Platform, Governance & Reliability",
        summary="Senior engineering leader and hands-on CTO with 20+ years building cloud-native platforms, improving delivery systems, and governing secure infrastructure at scale. Experience spans AWS platform architecture, reliability, access boundaries, cost optimization, and compliance-aware modernization across Java, Python, and TypeScript environments. Brings a pragmatic focus on platform standards, delivery quality, and multi-stakeholder execution.",
        skills=[
            "Leadership: Org Leadership • Manager Development • Cross-Functional Delivery • Technical Strategy",
            "Cloud Platform: AWS Architecture • Reliability / Observability • Platform Standards • Cost Optimization",
            "Governance: Access Controls / RBAC • Auditability • Compliance-Aware Delivery • Infrastructure Modernization",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Docker / Kubernetes • Java / Spring • Python • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=exec_experiences(security=True),
        lane="Lane 1 + Lane 2 overlap",
        work_model="Remote",
        compensation="$188K-$282K base + performance incentive and possible LTI",
        fit="Real enterprise-scale bridge role with budget ownership, FinOps, compliance, platform governance, and multi-business-unit cloud strategy.",
        risk="Base is below the ideal range and only brushes the practical floor at the top end; the context is also more enterprise-corporate than software-product-led.",
        link="https://www.linkedin.com/jobs/view/4398021490/",
        source="LinkedIn",
        questions=role_questions(
            "What are the strongest examples of cloud cost optimization, environment consolidation, or infrastructure governance you can quantify?",
            "Do you have any multi-business-unit or multi-domain platform stories that can approximate enterprise scale?",
            "Which reliability or incident-management stories best demonstrate platform ownership rather than application delivery?",
            "Is there a stronger story around budget planning, vendor/platform selection, or executive reporting on infrastructure outcomes?",
        ),
    ),
    RoleSpec(
        company="Dropbox",
        role="Engineering Manager, Privacy Engineering",
        folder_name="20260412 - Dropbox - Engineering Manager - Privacy Engineering",
        headline="Engineering Manager | Privacy Engineering, Secure Platforms & Reliability",
        summary="Senior engineering leader and hands-on CTO with 20+ years building secure backend services, access-controlled platforms, and reliability-focused delivery systems. Experience spans cloud governance, secure APIs, observability, CI/CD discipline, and incident response across AWS, Java, Python, and TypeScript. Brings strong technical leadership, mentoring, and operational rigor to privacy- and trust-sensitive engineering work.",
        skills=[
            "Architecture & Systems: Distributed Systems • Backend Services • API Design • Observability • SLOs / Incident Response",
            "Security & Privacy: Access Controls / RBAC • Auditability • Vulnerability Remediation • Compliance-Aware Delivery",
            "Delivery Systems: CI/CD • Release Safety • Developer Tooling • Docker / Kubernetes",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=management_experiences(),
        lane="Lane 2",
        work_model="Remote U.S.",
        compensation="US Zone 2 $195.8K-$265K, US Zone 3 $174.1K-$235.5K",
        fit="Strong brand, privacy/compliance story, and credible management-at-scale proof.",
        risk="Cash is below floor in most geographies, and this is a management detour rather than a director-level bridge.",
        link="https://boards.greenhouse.io/embed/job_app?token=7256197",
        source="Greenhouse",
        questions=role_questions(
            "Which access-control, audit, or security-remediation stories can be reframed more explicitly as privacy/trust engineering?",
            "Do you have examples of handling sensitive data, PII, or regulated workflows that belong higher in the resume?",
            "What are the strongest mentoring or team-leadership examples for a management-at-scale role?",
            "Is there a stronger incident response or production issue story tied to security or privacy outcomes?",
        ),
    ),
    RoleSpec(
        company="Dropbox",
        role="Corporate Infrastructure Engineering Manager, Cloud Infrastructure",
        folder_name="20260412 - Dropbox - Corporate Infrastructure Engineering Manager - Cloud Infrastructure",
        headline="Engineering Manager | Cloud Infrastructure, Platform Reliability & Delivery",
        summary="Senior engineering leader and hands-on CTO with 20+ years building cloud-native platforms, secure delivery systems, and developer infrastructure. Experience spans AWS architecture, CI/CD governance, observability, reliability, and access-controlled environments across Java, Python, and TypeScript ecosystems. Brings pragmatic technical leadership, mentoring, and operational discipline to infrastructure-facing teams.",
        skills=[
            "Architecture & Systems: Distributed Systems • Backend Services • Platform Engineering • Observability • SLOs / Incident Response",
            "Delivery & Reliability: CI/CD • Release Safety • Developer Tooling • Docker / Kubernetes",
            "Governance: Access Controls / RBAC • Auditability • Cloud Security • Infrastructure Modernization",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=management_experiences(),
        lane="Lane 2",
        work_model="Remote U.S.",
        compensation="US Zone 2 $180.8K-$244.6K, US Zone 3 $160.7K-$217.3K",
        fit="Known brand plus cloud, platform, and infrastructure leadership scope.",
        risk="Compensation is materially below target and the title is a narrower management bridge.",
        link="https://boards.greenhouse.io/embed/job_app?token=7210704",
        source="Greenhouse",
        questions=role_questions(
            "What infrastructure or platform stories best show long-term ownership rather than application delivery?",
            "Do you have stronger examples around cloud cost, environment parity, or infrastructure standards that can be surfaced?",
            "Which mentoring and team-operating examples best fit an engineering manager role in infrastructure?",
            "Is there a stronger operational-reliability or incident-management story to include?",
        ),
    ),
    RoleSpec(
        company="Affirm",
        role="Manager, Release Engineering (Developer Productivity, CI/CD)",
        folder_name="20260412 - Affirm - Manager, Release Engineering - Developer Productivity, CI-CD",
        headline="Engineering Manager | Release Engineering, DevEx & CI/CD Governance",
        summary="Senior engineering leader and hands-on CTO with 20+ years improving release safety, developer productivity, and cloud-native delivery systems. Experience spans CI/CD, environment parity, observability, secure APIs, and incident-aware operations across AWS, Java, Python, and TypeScript. Brings strong technical leadership, mentoring, and pragmatic process discipline to reliability- and release-focused teams.",
        skills=[
            "Delivery & Reliability: CI/CD • Release Safety • Developer Productivity • Incident Response • IaC",
            "Platform Systems: Developer Tooling • Docker / Kubernetes • Environment Parity • Observability",
            "Governance: Access Controls / RBAC • Auditability • Compliance-Aware Delivery • Vulnerability Remediation",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=management_experiences(),
        lane="Lane 2",
        work_model="Remote U.S.",
        compensation="$225K-$275K in CA/WA/NY/NJ/CT, $200K-$250K in other U.S. states",
        fit="Good detour role if the goal is management-at-scale in developer productivity, release governance, and compliance-heavy delivery.",
        risk="Compensation is borderline to below floor outside the top band, and it does not directly move title upward.",
        link="https://boards.greenhouse.io/embed/job_app?token=6644302003",
        source="Greenhouse",
        questions=role_questions(
            "What developer-experience or release-process improvements have the clearest measurable impact?",
            "Do you have any stronger environment-parity, rollback-safety, or release-governance stories than the current set?",
            "Which examples best show mentoring engineers or leading process change rather than only doing the implementation?",
            "Is there a better CI/CD automation example that highlights compliance or control effectiveness?",
        ),
    ),
    RoleSpec(
        company="LaunchDarkly",
        role="Engineering Manager, Feature Management",
        folder_name="20260412 - LaunchDarkly - Engineering Manager - Feature Management",
        headline="Engineering Manager | Feature Platforms, Reliability & Delivery Systems",
        summary="Senior engineering leader and hands-on CTO with 20+ years building secure backend services, delivery systems, and cloud-native platforms. Experience spans CI/CD, release safety, developer tooling, observability, and incident-aware operations across AWS, Java, Python, and TypeScript. Brings a product-and-platform mindset plus pragmatic technical leadership for developer-facing systems.",
        skills=[
            "Architecture & Systems: Distributed Systems • Backend Services • API Design • Observability • SLOs / Incident Response",
            "Delivery Systems: CI/CD • Release Safety • Developer Tooling • Docker / Kubernetes",
            "Product Platform: Feature Delivery • Reliability • Platform Standards • Cross-Functional Execution",
            "Technical: AWS (RDS/Aurora, ECS, Lambda, S3, Bedrock) • Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL / MongoDB",
        ],
        experiences=management_experiences(),
        lane="Lane 2",
        work_model="Remote U.S.",
        compensation="Zone 1 $187K-$240K, Zone 2 $168.2K-$220K, Zone 3 $158.9K-$210K + RSUs",
        fit="Recognizable devtools brand and good management proof in a developer-facing product.",
        risk="Compensation is below floor and the scope is less directly aligned with the executive bridge lane.",
        link="https://boards.greenhouse.io/embed/job_app?token=6563764003",
        source="Greenhouse",
        questions=role_questions(
            "What developer-facing platform stories best show product thinking, not just infrastructure or process work?",
            "Do you have examples of feature rollout safety, progressive delivery, or release governance that map well here?",
            "Which team-leadership examples best support an engineering manager story at a product-infrastructure company?",
            "Is there a better reliability or incident example that highlights customer or developer impact?",
        ),
    ),
    RoleSpec(
        company="ClickUp",
        role="Principal Engineer, Collaboration Platforms",
        folder_name="20260412 - ClickUp - Principal Engineer - Collaboration Platforms",
        headline="Principal Engineer | Collaboration Platforms, Developer Systems & Applied AI",
        summary="Principal-level engineer and hands-on CTO with 20+ years designing distributed, cloud-native platforms and workflow-heavy systems. Deep experience building APIs, developer tooling, AI-integrated services, and production systems on AWS using Java, Python, and TypeScript, with strong grounding in CI/CD, observability, SLO-driven reliability, and secure operational workflows. Recently built Model Context Protocol (MCP)-integrated tooling and agentic admin workflows that connect LLMs to typed APIs and structured data without losing operational discipline.",
        skills=[
            "Architecture & Systems: Distributed Systems • Backend Services • API Design (REST, OAuth2, JWT) • Microservices • Observability • SLOs / Incident Response",
            "Languages & Frameworks: Java / Spring • Python • TypeScript / Node.js • JavaScript (React, Angular, Vue)",
            "Cloud & Data: AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3) • Kubernetes • PostgreSQL • MySQL • MongoDB • Redis",
            "AI & Developer Tooling: MCP • LLM API Integration (Bedrock / Claude) • Typed APIs • Agentic Admin Tooling",
        ],
        experiences=principal_experiences(),
        lane="Lane 3",
        work_model="Remote U.S.",
        compensation="$250K-$300K",
        fit="Credible AI-workspace brand, solid pay band, and strong platform/distributed-systems signal.",
        risk="Principal IC remains a detour away from the executive ladder.",
        link="https://jobs.ashbyhq.com/clickup/750fd29f-899d-4310-a8b1-8e0ce940e65d?embed=js",
        source="Ashby",
        questions=role_questions(
            "Which examples best map to collaboration or shared-workflow platforms rather than vertical SaaS products?",
            "Do you have stronger real-time collaboration, synchronization, or shared-state stories that should be surfaced?",
            "What is the clearest example of technical leadership across teams without formal org ownership?",
            "Is there a better product-platform story involving APIs, workflow orchestration, or developer extensibility?",
        ),
    ),
    RoleSpec(
        company="Motion",
        role="Principal Software Engineer",
        folder_name="20260412 - Motion - Principal Software Engineer",
        headline="Principal Software Engineer | Workflow Systems, Agentic Tools & Applied AI",
        summary="Principal-level engineer and hands-on CTO with 20+ years designing distributed, cloud-native platforms and workflow-heavy systems. Deep experience building APIs, developer tooling, AI-integrated services, and production systems on AWS using Java, Python, and TypeScript, with strong grounding in CI/CD, observability, SLO-driven reliability, and secure operational workflows. Recently built Model Context Protocol (MCP)-integrated tooling, generative search, and bounded agentic workflows that connect LLMs to typed APIs and structured data.",
        skills=[
            "Architecture & Systems: Distributed Systems • Backend Services • API Design (REST, OAuth2, JWT) • Microservices • Observability • SLOs / Incident Response",
            "Languages & Frameworks: Java / Spring • Python • TypeScript / Node.js • JavaScript (React, Angular, Vue)",
            "Cloud & Data: AWS (ECS, Lambda, Bedrock, Textract, RDS/Aurora, S3) • Kubernetes • PostgreSQL • MySQL • MongoDB • Redis",
            "AI & Developer Tooling: MCP • LLM API Integration (Bedrock / Claude) • Typed APIs • Agentic Admin Tooling",
        ],
        experiences=principal_experiences(),
        lane="Lane 3",
        work_model="Remote U.S./Canada",
        compensation="Total compensation $504K-$965K",
        fit="Very strong AI-agent / workflow-platform story with unusually strong upside.",
        risk="Startup profile is volatile, comp is not all base, and it is still an IC detour.",
        link="https://jobs.ashbyhq.com/motion/7355e80d-dab2-4ba1-89cc-a0197e08a83c",
        source="Ashby",
        questions=role_questions(
            "Which workflow-automation examples best demonstrate end-user productivity impact rather than only engineering efficiency?",
            "Do you have stronger AI-agent or asynchronous-workflow examples that should replace weaker bullets?",
            "What is the clearest principal-level leadership story across architecture, standards, or cross-team technical direction?",
            "Is there a better narrative around rapidly shipping 0→1 product capabilities under aggressive timelines?",
        ),
    ),
]


def existing_folder_names() -> set[str]:
    return {path.name for path in SEND_TO_DIR.iterdir() if path.is_dir()}


def main() -> int:
    existing_folders = existing_folder_names()
    created_specs: list[RoleSpec] = []

    for spec in ROLE_SPECS:
        folder = SEND_TO_DIR / spec.folder_name
        is_new = spec.folder_name not in existing_folders
        folder.mkdir(parents=True, exist_ok=True)

        resume_filename = f"Chris Tallent Resume - {sanitize_filename(spec.company)} - {sanitize_filename(spec.role)}.docx"
        resume_docx = folder / resume_filename
        resume_md = folder / resume_filename.replace(".docx", ".md")
        draft_md = folder / "draft.md"
        job_description = folder / "job description.txt"
        questions_md = folder / "questions.md"

        shutil.copyfile(TEMPLATE_DOCX, resume_docx)
        document_xml = build_document_xml(spec)
        write_docx(resume_docx, document_xml)
        resume_md.write_text(build_markdown(spec), encoding="utf-8")
        draft_md.write_text(
            textwrap.dedent(
                f"""\
                # {spec.company} - {spec.role}

                ## Base
                - Track: Principal / Engineering leadership shell
                - Source resume: {TEMPLATE_DOCX.name}
                - Output resume: {resume_filename}

                ## Role Notes
                - Lane: {spec.lane}
                - Work model: {spec.work_model}
                - Compensation: {spec.compensation}
                - Review source: {REVIEW_FILE.name}

                ## Next Pass
                - Review headline and summary against the live posting
                - Tighten any weak role-specific phrases after follow-up questions are answered
                - Export PDF after final proofread
                """
            ),
            encoding="utf-8",
        )
        job_description.write_text(build_job_description(spec), encoding="utf-8")
        questions_md.write_text(build_questions(spec), encoding="utf-8")
        refresh_cache(resume_docx)
        if is_new:
            created_specs.append(spec)

    appended = append_tracker_rows(created_specs) if created_specs else []

    print("Created folders:")
    for spec in created_specs:
        print(f"- {spec.folder_name}")
    print("Appended tracker rows:")
    for item in appended:
        print(f"- {item}")
    if not created_specs:
        print("- none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

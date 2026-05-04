#!/usr/bin/env python3
"""Build the canonical Engineering Manager resume from an existing .docx shell."""

from __future__ import annotations

import sys
import zipfile
from xml.dom import minidom
from pathlib import Path


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


PARAGRAPHS = [
    "CHRIS TALLENT",
    "Engineering Manager | Platform, Reliability & Product Delivery",
    "Cincinnati Metro Area • 859.394.2923 • chris@provenedge.com • linkedin.com/in/tallented",
    "──────────────────────────────────────────────────────────────────────────────────────────────────",
    "PROFESSIONAL SUMMARY",
    (
        "Engineering leader with 20+ years leading small-to-mid-sized software teams in startup "
        "and growth environments, often under CTO titles with direct responsibility for hiring, "
        "mentoring, architecture, and delivery. Proven record modernizing legacy systems, "
        "improving CI/CD and cloud operations, and partnering across product, design, security, "
        "and business teams to ship reliable software on AWS using Java, Python, and TypeScript. "
        "Brings a player-coach management style, strong technical judgment, and hands-on "
        "credibility for Engineering Manager and Senior Engineering Manager roles."
    ),
    "CORE SKILLS",
    (
        "Leadership & Delivery: Team Leadership • Hiring & Mentoring • Agile Delivery • "
        "Cross-Functional Execution • Incident Management"
    ),
    (
        "Platform & Reliability: CI/CD • Release Safety • Developer Tooling • Observability • "
        "SLOs / Incident Response"
    ),
    (
        "Security & Cloud: AWS • RBAC / IAM • Compliance-Aware Delivery • "
        "Vulnerability Remediation • Cost Optimization"
    ),
    "AI & Automation: Claude Code • AWS Bedrock / RAG • Document Workflows • Agentic Tooling",
    (
        "Technical: Java / Spring • Python • TypeScript / Node.js • PostgreSQL / MySQL • "
        "MongoDB • Docker / Kubernetes"
    ),
    "PROFESSIONAL EXPERIENCE",
    "Chief Technology Officer | Pitchstone Technology LLC",
    "Seattle, WA • February 2021 – Present",
    (
        "Scaled the engineering organization from 6 to roughly 35 across four agile teams, "
        "improving team structure, morale, and retention."
    ),
    (
        "Served as CTO and lead architect for Pitchstone Platform, setting platform "
        "architecture, cloud/security design, and engineering standards."
    ),
    (
        "Partnered on product direction, requirements, roadmap prioritization, and UX "
        "feasibility while guiding staged delivery."
    ),
    (
        "Built an AI-assisted modernization workflow with Claude Code for upgrades and test "
        "generation, cutting delivery time from 4 months to 3 weeks."
    ),
    (
        "Reduced non-production infrastructure cost 35-40% through ECS cluster consolidation "
        "and environment strategy improvements."
    ),
    (
        "Defined AWS account structure, RBAC, IAM Identity Center permission sets, and access "
        "boundaries across five AWS accounts."
    ),
    (
        "Directed ISO 27001 security compliance, overseeing penetration testing, audits, and "
        "vulnerability remediation."
    ),
    "Chief Technology Officer | Automobile Consumer Services Inc",
    "Cincinnati, OH • July 2016 – February 2021",
    (
        "Led technology transformation for a fintech organization, overseeing development, "
        "cloud migration, and Agile adoption."
    ),
    (
        "Re-architected a legacy PHP fintech platform into Angular and Java services on AWS "
        "Kubernetes, improving scalability and uptime to 99.99%."
    ),
    (
        "Implemented CI/CD pipelines and Agile delivery practices, reducing deployment cycles "
        "from weeks to hours."
    ),
    (
        "Built and delivered the NADA 2017 proof of concept in two months, enabling MVP "
        "showcase and faster business validation."
    ),
    "Owner & Fractional CTO | Proven Edge LLC",
    "Fort Thomas, KY • November 2015 – Present",
    (
        "Directed architecture, development, and DevOps for multiple SaaS clients, reducing "
        "implementation cost by up to 50%."
    ),
    (
        "Oversaw architecture and engineering-process governance for a laboratory-testing "
        "client, restoring management confidence during a staff transition."
    ),
    (
        "Built a reusable multi-platform application scaffold spanning web, mobile, desktop, "
        "API, and AI services with OIDC auth, RBAC, billing, and notifications."
    ),
    (
        "Built controlled AI admin tooling that enabled bounded operational actions through "
        "typed APIs and existing RBAC."
    ),
    (
        "Architected and delivered a React, Next.js, and Prisma legal SaaS MVP under "
        "aggressive launch timing."
    ),
    (
        "Reengineered a golf-handicapping SaaS platform used by thousands of active users, "
        "adding automated scoring, cheat analysis, and multi-source data aggregation."
    ),
    "Technical Co-Founder & Chief Technology Officer | Glamhive",
    "Seattle, WA • November 2013 – November 2015",
    "Co-founded a fashion-tech platform and launched Glamhive.com from concept to production on AWS.",
    (
        "Formed and led distributed agile teams in the U.S. and South America, cutting "
        "staffing costs by 60% vs. U.S.-only teams."
    ),
    (
        "Unified web and mobile codebases via Cordova and Ionic, reducing mobile development "
        "costs by 70%."
    ),
    (
        "Designed the data model and indexing strategy for real-time search and personalized "
        "recommendations."
    ),
    (
        "Won Seattle Angel Conference VII in 2015, securing $205K in investment after multiple "
        "rounds of demos and investor interviews."
    ),
    "Chief Technology Officer | Lela.com",
    "New York, NY • November 2011 – May 2014",
    (
        "Directed development of a personalized shopping recommendation platform with "
        "multi-retailer integrations."
    ),
    (
        "Refactored core recommendation services into modular Java components, improving "
        "maintainability and enabling feature experimentation."
    ),
    (
        "Rebuilt the engineering organization post-pivot, improving delivery speed by "
        "approximately 25% while introducing Agile practices and automated testing."
    ),
    (
        "Guided roadmap prioritization with management and presented product and technology "
        "updates to the board."
    ),
    "EARLIER ROLES",
    (
        "Owner & Consultant | Tallented Software LLC (2010–2011) — Delivered custom software "
        "for e-commerce and analytics clients, integrating payment gateways and real-time reporting."
    ),
    "Senior Associate | dunnhumbyUSA (2009–2010) — Developed C# and Flex-based systems; mentored junior developers.",
    "Senior Software Engineer | Fidelity Investments (2003–2009) — Engineered document generation system for 401k reporting.",
    "EDUCATION",
    "Bachelor of Science in Computer Science — University of Kentucky, Lexington, KY",
]


def paragraph_text_nodes(paragraph):
    return paragraph.getElementsByTagNameNS(NS["w"], "t")


def set_paragraph_text(document: minidom.Document, paragraph, text: str) -> None:
    text_nodes = paragraph_text_nodes(paragraph)
    if not text_nodes:
        raise ValueError("Paragraph has no text nodes to replace")

    first = text_nodes[0]
    if first.firstChild is None:
        first.appendChild(document.createTextNode(text))
    else:
        first.firstChild.data = text

    for node in text_nodes[1:]:
        if node.firstChild is None:
            node.appendChild(document.createTextNode(""))
        else:
            node.firstChild.data = ""


def build(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(source) as zin:
        source_document = zin.read("word/document.xml")
        document = minidom.parseString(source_document)
        paragraphs = [
            paragraph
            for paragraph in document.getElementsByTagNameNS(NS["w"], "p")
            if "".join(node.firstChild.data if node.firstChild else "" for node in paragraph_text_nodes(paragraph)).strip()
        ]

        if len(paragraphs) != len(PARAGRAPHS):
            raise ValueError(
                f"Template paragraph count changed: expected {len(PARAGRAPHS)}, found {len(paragraphs)}"
            )

        for paragraph, text in zip(paragraphs, PARAGRAPHS):
            set_paragraph_text(document, paragraph, text)

        document_xml = document.toxml(encoding="UTF-8")

        with zipfile.ZipFile(destination, "w") as zout:
            for item in zin.infolist():
                data = document_xml if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: build_canonical_em_resume.py <source.docx> <destination.docx>", file=sys.stderr)
        return 1

    build(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

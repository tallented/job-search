#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from shutil import copyfile
from xml.sax.saxutils import escape

from build_review_batch import NS, SECT_PR, bullet, p, refresh_cache, write_docx


WORKSPACE = Path("/Users/chris/2026 Resumes")
FOLDER = WORKSPACE / "Send To/20260505 - Datavant - VP Enterprise Engineering & Business Platforms"
DOCX = FOLDER / "Chris Tallent Resume - Datavant - VP Enterprise Engineering & Business Platforms.docx"
MD = FOLDER / "Chris Tallent Resume - Datavant - VP Enterprise Engineering & Business Platforms.md"
SOURCE = WORKSPACE / "CANONICAL - Chris Tallent Resume - CTO.docx"


HEADLINE = "Technology Executive | Enterprise Platforms, Integration Governance & Regulated Systems"

SUMMARY = (
    "Technology executive with 20+ years leading SaaS platform architecture, enterprise workflow "
    "modernization, and regulated systems delivery. Built and governed platforms across customer "
    "identity, payment and credit workflows, vendor selection, cloud security, API integration, "
    "and AI-enabled automation. Operates effectively in ambiguous environments where architecture, ownership, "
    "and delivery discipline need to be made explicit."
)

SKILLS = [
    "Leadership: VP / CTO Leadership • Org Design • Coaching • Vendor Governance • Executive Alignment",
    "Enterprise Platforms: Platform Strategy • Business Systems Architecture • Integration Governance • Change Control",
    "Integration & Identity: API Design • Middleware Patterns • Event-Driven Workflows • RBAC / IAM • Customer Access",
    "Financial & Automation: Payment / Credit Workflows • Billing Patterns • Audit Readiness • ISO 27001",
    "Technical: AWS • Java / Spring • TypeScript / React / Vue • Python • PostgreSQL / MySQL • Docker / Kubernetes",
]

EXPERIENCE = [
    (
        "Chief Technology Officer | Pitchstone Technology LLC",
        "Seattle, WA • February 2021 – Present",
        "CTO and lead architect for an AI-enabled enterprise workflow platform supporting a Fortune 100 wireless retailer across roughly 15,000 locations, with ownership of architecture, delivery, security, and compliance.",
        [
            "Served as product owner and lead architect for Pitchstone Platform, defining configuration-driven entities, fields, workflow behavior, APIs, OIDC authentication, client-configured RBAC, and technical standards.",
            "Coordinated multi-team, bi-directional workflows and API integrations across Pitchstone and multiple T-Mobile teams, including networking and cybersecurity dependencies.",
            "Defined AWS account structure, RBAC, IAM Identity Center permissions, and five-account access boundaries.",
            "Led ISO 27001 compliance, including pen-test selection, audit prep, vulnerability remediation, and controls.",
            "Evaluated compliance and requirements-management vendors through demos, quotes, RFPs, and hands-on assessments of fit, control coverage, implementation burden, and cost.",
            "Built engineering from a small initial team into four agile teams, improving ownership and retention.",
            "Built AI document workflows using AWS Bedrock, Textract, Comprehend, Gemini Vision, S3, and Python.",
            "Reduced non-production infrastructure cost 35-40% through ECS cluster consolidation and environment strategy.",
        ],
    ),
    (
        "Chief Technology Officer | Automobile Consumer Services Inc",
        "Cincinnati, OH • July 2016 – February 2021",
        "Led technology transformation for an automotive fintech platform handling payment, credit, PII, and consumer finance workflows, sequencing modernization and dealer-facing features against delivery risk.",
        [
            "Modernized legacy PHP into Angular and Java services on AWS Kubernetes, reaching 99.99% uptime.",
            "Designed JSON-driven configuration for dealer finance workflows and UI behavior without per-client code forks.",
            "Implemented CI/CD practices that reduced deployment cycles from weeks to hours with safer rollback paths.",
            "Owned production reliability for customer-facing finance workflows, including incident response, release planning, scaling, and infrastructure operations.",
        ],
    ),
    (
        "Owner & Fractional CTO | Proven Edge LLC",
        "Fort Thomas, KY • November 2015 – Present",
        "Fractional CTO for SaaS, legal-tech, health-tech, laboratory, and real-estate clients, setting architecture, delivery practices, DevOps, and AI-enabled operating workflows.",
        [
            "Built a reusable multi-platform scaffold across web, mobile, desktop, API, and AI services with OIDC auth, dynamic RBAC, billing, documents, notifications, and webhooks.",
            "Packaged common auth, billing, document, notification, webhook, and background-job capabilities so new products reused the same platform patterns.",
            "Built a governed AI admin assistant with MCP access for account management, job-queue inspection, and system health checks, routing actions through typed APIs with RBAC, audit logging, and gated actions.",
            "Built generative search over help docs using chunking, embeddings, and a Python vector store, grounding responses in linked source documentation.",
            "Advised client executives on product scope, architecture tradeoffs, delivery sequencing, and platform selection.",
            "Stabilized architecture and delivery practices for a laboratory-testing client during a staff transition.",
        ],
    ),
    (
        "Technical Co-Founder & Chief Technology Officer | Glamhive",
        "Seattle, WA • November 2013 – November 2015",
        "Technical co-founder for a fashion-tech marketplace, taking the product from concept to AWS production.",
        [
            "Designed the data model and indexing strategy for real-time search and recommendations.",
            "Led distributed agile teams in the U.S. and South America, cutting staffing costs by 60% vs. U.S.-only teams.",
            "Won Seattle Angel Conference VII in 2015, securing $205K after multiple demos and investor interviews.",
        ],
    ),
    (
        "Chief Technology Officer | Lela.com",
        "New York, NY • November 2011 – May 2014",
        "CTO for a personalized shopping platform with multi-retailer integrations, guiding product operations and engineering through a post-pivot rebuild.",
        [
            "Guided roadmap prioritization with executive leadership and board-level technology updates.",
            "Refactored core recommendation services into modular Java components behind an AngularJS user interface.",
            "Rebuilt engineering post-pivot, improving delivery speed about 25% with Agile practices and test automation.",
        ],
    ),
]

EARLIER_ROLES = [
    "Senior Associate | dunnhumbyUSA: Developed C# and Flex-based retail analytics systems; mentored junior developers in delivery and code quality.",
    "Senior Software Engineer | Fidelity Investments: Built regulated 401k reporting and document-generation systems.",
]


def document_xml() -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f"<w:document {NS}>",
        "<w:body>",
        p("CHRIS TALLENT", style="Heading1", center=True, spacing_before=120, spacing_after=40),
        p(HEADLINE, center=True, italic=True, spacing_before=40, spacing_after=40),
        p("Cincinnati Metro Area • 859.394.2923 • chris@provenedge.com • linkedin.com/in/tallented", center=True, spacing_before=40, spacing_after=40),
        p("────────────────────────────────────────────────────────────────────────────────────────"),
        p("PROFESSIONAL SUMMARY", style="Heading2", spacing_before=280),
        p(SUMMARY),
        p("CORE SKILLS", style="Heading2", spacing_before=280),
    ]
    parts.extend(p(line, spacing_after=120) for line in SKILLS)
    parts.append(p("PROFESSIONAL EXPERIENCE", style="Heading2", spacing_before=280))
    for title, dates, summary, bullets in EXPERIENCE:
        parts.append(p(title, style="Heading3"))
        parts.append(p(dates, spacing_after=40))
        parts.append(p(summary, spacing_after=40))
        parts.extend(bullet(item) for item in bullets)
    parts.append(p("EARLIER ROLES", style="Heading2", spacing_before=280))
    parts.extend(p(item, spacing_after=100) for item in EARLIER_ROLES)
    parts.append(p("EDUCATION", style="Heading2", spacing_before=220))
    parts.append(p("Bachelor of Science in Computer Science | University of Kentucky, Lexington, KY", spacing_after=100))
    parts.append(SECT_PR)
    parts.append("</w:body></w:document>")
    return "".join(parts)


def markdown() -> str:
    lines = [
        "# CHRIS TALLENT",
        "",
        f"*{HEADLINE}*",
        "",
        "Cincinnati Metro Area • 859.394.2923 • chris@provenedge.com • linkedin.com/in/tallented",
        "",
        "─────────────────────────────────────────────────────────────────────────────────────────────────",
        "",
        "## PROFESSIONAL SUMMARY",
        "",
        SUMMARY,
        "",
        "## CORE SKILLS",
        "",
    ]
    lines.extend(SKILLS)
    lines.extend(["", "## PROFESSIONAL EXPERIENCE", ""])
    for title, dates, summary, bullets in EXPERIENCE:
        lines.extend([f"### {title}", "", dates, ""])
        lines.extend([summary, ""])
        lines.extend(f"- {item}" for item in bullets)
        lines.append("")
    lines.extend(["## EARLIER ROLES", ""])
    lines.extend(EARLIER_ROLES)
    lines.extend(["", "## EDUCATION", "", "Bachelor of Science in Computer Science | University of Kentucky, Lexington, KY"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    copyfile(SOURCE, DOCX)
    write_docx(DOCX, document_xml())
    MD.write_text(markdown(), encoding="utf-8")
    refresh_cache(DOCX)
    bad = ["—"]
    text = markdown()
    for token in bad:
        if token in text:
            raise RuntimeError(f"disallowed punctuation found: {escape(token)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

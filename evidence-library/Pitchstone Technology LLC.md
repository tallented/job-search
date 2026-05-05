# Pitchstone Technology LLC

Validated: 2026-04-09 via resume-tailoring QA with Chris Tallent.

## Scope Summary

- Role: Chief Technology Officer
- Function in practice: CTO + lead architect + security/platform decision-maker
- Working model: hands-on early where leverage was highest, then transitioned day-to-day implementation to teams while retaining architecture, cloud/security, and standards ownership

## Org Scale

- Engineering organization scaled from `6` to roughly `35`
- Team model: `4` agile-style teams
- Typical team composition: `4-5` developers, `2-3` QA, `1` Product Owner
- Reporting structure: included a Development Manager reporting to Chris; teams reported through that manager

## Architecture Ownership

- Set platform architecture and security architecture
- Chose core technology platforms and AWS tooling for new product work
- Authored the first version of Pitchstone Platform personally, then transitioned implementation ownership to teams
- Retained ownership of architecture, cloud/security design, and technical standards after handoff

## Product / AI / Workflow Design

- Directly wrote and prototyped an AWS Bedrock knowledge-base solution for the TBuilder product
- Goal of the prototype was partly strategic: demonstrate to T-Mobile that Pitchstone could build real generative AI solutions and help guide feature direction
- Led technology selection and delivery of AI-based lease and LOI data-point extraction using:
  - AWS Textract
  - AWS Comprehend
  - vision OCR for image-based PDFs and `.docx` content when needed
- Extraction workflow targeted known backend data points, applied document-specific rules, then presented extracted values to the user for review or override before commit
- The extraction tooling was built for both:
  - TBuilder
  - Pitchstone Platform

## Product Partnership / Delivery Model

- Active participant in product discussions, roadmap prioritization, and UX feasibility analysis
- Typically involved from concept through feature prioritization, UX review, epic breakdown, sprint planning, and high-level estimation
- For internally driven Pitchstone Platform work, had a major hand in shaping product behavior and feature design
- Preferred staged, end-to-end delivery every two weeks to reduce ambiguity and avoid long waterfall cycles
- Pitchstone software was used in a large, production retail real-estate workflow rather than as a small internal tool
- Exact internal count note from Chris query (`2026-04-15`): `15,563` retail locations
- Resume-safe scale note: the workflow supported a Fortune 100 wireless retailer's store-planning / build / project process across roughly `15,000` retail locations

## Monitoring / Incident Response

- Owned Secureframe system used to monitor AWS accounts for security compliance and ISO 27001 issues
- If risks were indicated, Chris prioritized them into the engineering or DevOps queue for remediation
- Set up AWS alarms and alerts for positive and negative conditions, including situations where expected logs were missing
- De facto on-call for backend, server-to-server, and API-to-API issues
- Helped design support, escalation, and postmortem processes
- In smaller-company CTO roles, typically served as lead infrastructure architect and primary owner of AWS environment decisions, either directly or with one DevOps lead

## Cross-Team / Federated Workflow Coordination

- Frequently joined calls with multiple T-Mobile teams during feature planning, development, and production support
- Helped drive feature discovery, roadmap timing, capability analysis, and API design for team-to-team server communication
- Regularly worked with T-Mobile networking and cybersecurity teams because of locked-down network constraints
- Major TBuilder integration involved dealer franchise owner requests from a T-Mobile external system entering a multi-stage, bi-directional workflow
- Some workflows required coordination across:
  - Pitchstone
  - a primary T-Mobile team
  - a separate T-Mobile mapping / acceptable-regions team
  - T-Mobile cybersecurity / IT as needed
- Chris designed the federated process and explained network / risk / audit implications across those groups

## AWS / Access Control

- Designed AWS account structure for `5` AWS accounts total:
  - TBuilder production
  - TBuilder non-production
  - Pitchstone Platform production
  - Pitchstone Platform non-production
  - Pitchstone site / miscellaneous apps
- Worked with project manager to define RBAC and permission sets for employees, contractors, and vendors across all AWS accounts
- Set IAM roles and access boundaries
- Chose IAM Identity Center / SSO direction rather than using Google Workspace directly
- Built the AWS accounts and selected Pulumi as the IaC / DevOps stack with the DevOps lead

## Identity / Authorization / Credential Management

Validated: 2026-05-05 via user-provided detail during 1Password resume tailoring.

- Implemented identity and authentication patterns using JWTs; when needed, supported JWT expiration tracking through a database-backed expiration table
- Refactored TBuilder from custom username/password authentication to Microsoft Azure Entra SSO for T-Mobile cybersecurity alignment
- Built Pitchstone Platform from the ground up with a standalone Keycloak OIDC instance to support Google IDP and keep the application SSO/OIDC-ready
- Defined robust role and permission models in both:
  - TBuilder
  - Pitchstone Platform
- Managed application-level credentials through AWS Secrets Manager, with secrets injected only into runtimes rather than stored directly in application code or images
- Managed other API keys and non-application secrets in 1Password
- Signed build artifacts during the Bitbucket build process and verified signatures when executing production Docker images

## ISO 27001 / Security Program

- Full ISO 27001 certification attained in `April 2023`
- Passed surveillance / cert-update activity in `2024`
- Most recent recertification completed on `June 4, 2025`
- Core implementation team was `3` people:
  - Chris
  - project manager
  - DevOps lead
- Chris defined the technical compliance process, procedures, requirements, and rules
- Chris defined RBAC model and access-control approach
- Chris selected device requirements and technical enforcement approach
- Chris was heavily involved in maintaining compliance through internal and external reviews

## Vendor Evaluation / Tool Selection

- Evaluated and selected Secureframe as the compliance operations platform after reviewing alternatives for ISO 27001 implementation and ongoing audit readiness
- Ran an RFP and quote/demo process with `3-4` requirements-tracking vendors, including side-by-side evaluations of product fit, workflow support, and cost
- Focus of selection work was operational fit, control coverage, implementation burden, and budget practicality rather than brand preference alone
- This was closer to CTO-led vendor evaluation and tool selection than a formal procurement organization

## Security Operations

- Responsible for finding and selecting the pen-test vendor
- Set up access and guidance for pen-test execution
- Received results and prioritized remediation of critical, high, and medium findings
- Low findings could remain open when justified by risk prioritization
- Pen tests generally occurred before ISO audit windows; remediation might still be in progress at audit start and would be completed or documented as understood risk by certification
- Worked with DevOps lead to keep Secureframe real-time audit posture in the high `90s`
- Secureframe monitoring was tied to AWS security tooling including:
  - Security Hub
  - GuardDuty
  - Inspector
- Chris prioritized vulnerability remediation in the DevOps queue and ensured completion

## Stakeholders / Customer Security Reviews

- Communicated security and compliance requirements to management and engineering teams
- Presented security and compliance status to the broader Pitchstone management team
- Answered the technical side of annual T-Mobile risk assessments, questionnaires, and surveys
- Prepared executive-summary documentation with appendix detail for T-Mobile stakeholders

## Transition / Handoff

- During transition of the main TBuilder product to a third party, Chris produced:
  - runbooks
  - documentation
  - architecture docs
  - diagrams
  - security policy docs
  - account setup docs
  - account teardown docs
- Chris ran all technically focused transition meetings
- Chris granted read-only access to production and non-production AWS accounts using IAM Identity Center permission sets with least-privilege boundaries
- Chris set up a constrained sandbox database account with guardrails for third-party exploration
- Supporting docs live under:
  - `/Users/chris/Projects/pitchstone/tmobile/transition-docs/docs`

## Resume Takeaways

- Strong fit for cloud architecture, IAM / access-control, security tooling, compliance, cloud governance, and engineering manager roles
- Useful for roles that care about:
  - multi-account AWS design
  - IAM / RBAC / SSO controls
  - ISO 27001 implementation and recertification
  - pen-test and remediation ownership
  - customer-facing technical risk reviews
  - hands-on architect to engineering-leader transition
  - generative AI workflow design
  - cross-team workflow orchestration
  - launch-readiness and operational ownership

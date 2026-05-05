# Resume Dispatch Decisions - 2026-05-04

Purpose: decide which resume path gets each active or recently verified req out the door fastest.

Decision format:

- `Customize`: role is strong enough in title, salary, company desirability, or trajectory to justify a tailored resume.
- `Light customize`: use the canonical base and only adjust top-third/core bullets or a few role bullets.
- `Canonical direct`: use one of the three canonical resumes with little or no role-specific editing.
- `Hold/skip`: do not spend tailoring time unless the req reopens, the pipeline thins, or there is a deliberate strategy change.

## Current Tracker Rows

| Tracker Id | Company | Role | Needs customized resume? | Canonical base | Resume Decision |
| --- | --- | --- | --- | --- | --- |
| 55 | ServiceNow | Director, Software Engineering - Observability / AI Data Center Control Plane | Yes | Engineering Manager | `Customize | Canonical EM | strong: prepared; AI observability/platform; comp likely clears floor` |
| 59 | Upstart | Director of Engineering, Upstart Bank | Yes | Engineering Manager | `Customize | Canonical EM | strong: prepared; regulated platform/org build; comp clears floor` |
| 61 | Horizon3.ai | Head of Cloud Operations | Yes | Engineering Manager | `Customize | Canonical EM | strong: prepared; cloud/security platform; comp clears floor` |
| 60 | Tremendous | Engineering Manager | Light | Engineering Manager | `Light customize | Canonical EM | practical: title downshift; remote/comp/company quality are strong` |
| 30 | 1Password | Senior Director Engineering, Identity Security Platform Infrastructure | Yes | Engineering Manager | `Customize | Canonical EM | strong: security/platform brand; emphasize IAM, reliability, internal platform` |
| 31 | Confluent | Director of Engineering, Governance | Hold | Engineering Manager | `Hold/skip | Canonical EM | company-coherence risk after rejection; verify fresh req before spend` |
| 36 | Socure | Head of Engineering - Agentic Workflows and Internal Tools | Light | CTO | `Light customize | Canonical CTO | good AI/internal-tools fit; comp slightly below practical floor` |
| 39 | Vanta | Senior Director, Corporate Engineering | Yes | Engineering Manager | `Customize | Canonical EM | strong title/security brand; verify comp and req freshness` |
| 40 | GE HealthCare | Senior Director - Cloud Infrastructure & Platform Engineering | Yes | Engineering Manager | `Customize | Canonical EM | strong title/cloud platform; comp may clear floor with incentives` |
| 41 | Dropbox | Engineering Manager, Privacy Engineering | Canonical direct | Engineering Manager | `Canonical EM direct | privacy/security fit; title below target and comp mixed by zone` |
| 42 | Dropbox | Corporate Infrastructure Engineering Manager, Cloud Infrastructure | Canonical direct | Engineering Manager | `Canonical EM direct | infra fit; title below target and comp likely below floor` |
| 43 | Affirm | Manager, Release Engineering (Developer Productivity, CI/CD) | Canonical direct | Engineering Manager | `Canonical EM direct | devprod fit; manager title and comp likely below floor` |
| 44 | LaunchDarkly | Engineering Manager, Feature Management | Hold | Engineering Manager | `Hold/skip | Canonical EM | title and salary below floor; use only as fallback/direct submit` |
| 25 | Netflix | Engineering Manager - Launch Readiness | Yes if still open | Engineering Manager | `Customize | Canonical EM | exceptional salary/brand; verify req freshness before spend` |
| 23 | Zillow | Principal Software Engineer | Light | Principal Engineer | `Light customize | Canonical Principal | strong IC comp; verify req freshness before spend` |

## Verified Queue, Not Yet Tracked

These should not get NocoDB rows until promoted into active tailoring work.

| Company | Role | Needs customized resume? | Canonical base | Resume Decision |
| --- | --- | --- | --- | --- |
| NetBox Labs | Vice President, Engineering | Yes | Engineering Manager | `Customize | Canonical EM | very strong: VP execution system, platform/devex, AI-native practices` |
| SQUIRE | VP, Engineering | Yes | CTO | `Customize | Canonical CTO | strong VP/product/payments/AI adoption fit; frame org scale carefully` |
| Help Scout | VP of Engineering | Yes | CTO | `Customize | Canonical CTO | strong remote VP, AI strategy, modernization, P&L, product partnership` |
| SafelyYou | Vice President of Engineering, SafelyYou Platform | Yes | CTO | `Customize | Canonical CTO | strong remote VP/platform execution; AI life-safety/device fleet; prequalify comp` |
| CoderPad | Director of Engineering | Yes | Engineering Manager | `Customize | Canonical EM | strong devtools/AI coding adoption; comp clears floor` |
| Antenna | VP, Engineering | Yes | CTO | `Customize | Canonical CTO | strong data/AI VP role; data-stack depth is the stretch` |
| Doppler | Head of Engineering | Light | CTO | `Light customize | Canonical CTO | strong developer-infra/security fit; small startup/player-coach` |
| Red Cell Partners / DEFCON AI | VP of Engineering | Yes | CTO | `Customize | Canonical CTO | strong AI/security/platform; DoD/optimization is the stretch` |
| ACV Auctions | VP, Platform Engineering | Light | Engineering Manager | `Light customize | Canonical EM | strong platform scope; comp top below practical floor` |
| Huntress | Director of Engineering, EDR | Light | Engineering Manager | `Light customize | Canonical EM | security leadership fit; endpoint domain is the stretch` |
| Babylist | Senior Engineering Manager, Machine Learning | Light | Engineering Manager | `Light customize | Canonical EM | comp strong; title downshift and ML depth stretch` |
| Litmus | VP Engineering | Light | CTO | `Light customize | Canonical CTO | VP title; industrial IoT/edge specialization and comp floor risk` |
| Zocalo Health | VP, Engineering | Light | CTO | `Light customize | Canonical CTO | regulated healthcare/platform fit; comp below floor` |
| Teleskope | VP Of Engineering | Hold | CTO | `Hold/skip | Canonical CTO | strong role but NYC hybrid 3+ days is not current work-model fit` |

## Fast Dispatch Order

1. Submit already-prepared `ServiceNow`.
2. Submit already-prepared `Upstart`.
3. Submit already-prepared `Horizon3.ai`.
4. Submit already-prepared `Tremendous` with only light top-third polish if needed.
5. Create new tailored resume for `NetBox Labs`.
6. Create new tailored resume for `SQUIRE`, `Help Scout`, or `SafelyYou`, depending on whether the next push should be product/payments VP, remote SaaS VP, or AI-enabled mission-critical platform execution.

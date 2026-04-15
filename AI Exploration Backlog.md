# AI Exploration Backlog (Career-Aligned)

Purpose: keep a focused, role-aligned backlog of AI topics to explore so I can (1) build real capability and (2) credibly position my experience for CTO / Director Platform / Principal roles without chasing hype.

This backlog is prioritized for my current target lanes:

- CTO / VP / Director: AI enablement, platform strategy, governance, operational excellence
- Principal: building production-grade AI-enabled systems, reliability, performance, integration patterns

## Current / In-Flight Work (Use In Positioning Now)

- Lease document extraction:
  - Gemini + Anthropic (in progress)
  - Prior: AWS Textract lease parser (delivered)
- GenAI customer/help chatbot:
  - Gemini (in progress)
- Agentic capabilities:
  - Likely Gemini (in progress)
- RAG / knowledge workflows:
  - Prior: RAG on AWS Bedrock + S3 + Python (delivered)
- AI-assisted engineering productivity:
  - Prior: Claude Code driven modernization (dependency upgrades + test generation) reducing delivery cycles from 4 months to 3 weeks (delivered)

## Must-Have (Next 2-6 Weeks)

These are the highest ROI topics for Director/Principal roles that mention "GenAI" but do not require deep research-science credentials.

- Evaluation (practical, production):
  - Build a small evaluation harness for chatbot/document extraction.
  - Concepts: golden sets, regression tests, rubric-based scoring, human review loops, online metrics vs offline metrics.
  - Outputs to capture: a short write-up + example dashboards/metrics + "quality gate" approach.

- LLMOps basics:
  - Prompt/version control and change management.
  - Observability: request tracing, token/cost metrics, latency percentiles, error taxonomies.
  - Release strategy: staged rollout, A/B tests, canarying, kill switches, fallbacks.

- RAG beyond the basics:
  - Chunking strategies, metadata, filtering, caching.
  - Hybrid retrieval + reranking (when it helps; when it adds cost/latency without benefit).
  - Grounding/citations and policy constraints for safe outputs.

- Reliability patterns for AI features:
  - Timeouts, retries, circuit breakers, model/provider fallback, graceful degradation.
  - Determinism constraints: structured output, function/tool calling, schema validation.

## Nice-To-Have (Next 1-3 Months)

These help for "AI platform" narratives and agentic features, but should be learned via building, not just reading.

- Agent orchestration patterns (without overcommitting to a specific framework):
  - Router vs planner/executor; tool-use constraints; memory/state; guardrails.
  - When agents are a bad idea (cost, reliability, unpredictability).

- Orchestration/workflow:
  - DAG vs state machine mental models; where agent graphs fit.
  - Build one multi-step workflow: extraction -> validation -> exception handling -> human review queue.

- Security/governance basics for AI:
  - PII handling, data retention, logging redaction, access control boundaries.
  - Auditability: what to log to support compliance and incident response.

- Cost and performance tuning:
  - Prompt optimization, context window management, caching, batch strategies where applicable.
  - Provider selection tradeoffs (Gemini vs Anthropic) by workload type.

## Specialized (Only If Targeting "AIML Director" Lane)

Pursue these only if I decide to compete for roles that explicitly require ML platform depth (fine-tuning, model optimization, etc.).

- Fine-tuning (LoRA/QLoRA/PEFT) fundamentals:
  - When fine-tuning is justified vs better RAG/data improvements.
  - Datasets, evaluation, cost/latency tradeoffs.

- Advanced RAG techniques:
  - Contextual compression, query expansion, multi-vector retrieval.
  - Domain-specific retrieval strategies (legal/financial/real-estate documents).

- Responsible AI / model risk management (deeper):
  - Bias, interpretability/traceability, regulatory expectations for model governance.

## Evidence To Capture (So It’s Resume-Usable)

For each explored item, capture at least one of:

- A measurable before/after metric (accuracy, review time, cost, latency, false positives/negatives).
- A design artifact (architecture diagram, evaluation plan, rollout plan, runbook).
- A short "what we learned" summary (1 page) that is specific and non-hypey.

## Resume/Interview Translation (How To Say It)

- Prefer: "production-grade evaluation harness", "LLMOps (observability, rollout, guardrails)", "RAG pipelines with grounding and quality gates", "agentic workflows with deterministic outputs and fallbacks"
- Avoid: "vibe coding", "autonomous agents everywhere", claiming deep fine-tuning expertise unless actually done


# Proven Edge LLC

Validated: 2026-04-09 via resume-tailoring QA with Chris Tallent.

## Scope Summary

- Role: Owner / Fractional CTO
- Context: cross-client architecture and product work, plus internal platform / IP development

## Internal AI / Platform Work

- Built multiple AI capabilities as part of the app scaffold:
  - recreated document data-point extraction using Gemini and Gemini Vision
  - implemented generative search over help docs using chunking, embeddings, and a Python vector store
  - built an agentic AI assistant for admins that can query and act against the admin API
- Built Zitadel OIDC into the Proven Edge application scaffold from the beginning to support Google and Meta IDPs plus Zitadel-managed usernames with password or passcode authentication
- Built dynamic RBAC into the scaffold so team- or client-level administrators could configure roles and permissions around their employees and business needs
- Built MCP-integrated tooling on top of the internal Entity Engine so LLM-driven tools can query and act against structured application data rather than only unstructured text
- The admin assistant is a natural-language control plane for SUPERADMIN users rather than a simple chat surface:
  - supports user-management actions including listing users, viewing a user dashboard, inviting users, changing roles, and enabling or disabling accounts
  - supports background-job operations including queue stats, job inspection, retry, and cancel actions
  - exposes system-health information including service status, document counts, and AI configuration
- Entry point and architecture:
  - entry point is `POST /agent/admin` on the FastAPI AI service with SSE streaming responses
  - an agent loop drives LLM tool-calling against a defined tool schema
  - tool dispatch executes against the existing Hono admin API with service-to-service authentication
- Safety and governance characteristics:
  - destructive actions are confirmation-gated rather than executed immediately
  - confirmation payloads are HMAC-signed and re-verified before state changes occur
  - tools do not access the database directly; they call the existing admin API so RBAC, audit logging, and webhooks fire the same way they do from the admin UI
  - pattern was intentionally designed so the model could not unilaterally mutate system state
- Current internal pattern is not just chat or retrieval:
  - model-facing tools can reason over structured entities
  - tools can execute bounded admin actions through typed APIs
  - the same foundation can support both human-facing admin workflows and AI-assistant workflows
- Example admin-assistant capabilities include:
  - asking how many active users exist
  - asking how many active admin users exist
  - taking selected admin actions through the API

## Product Characteristics

- Internal scaffold is intended to accelerate future B2B and B2C application development
- Current work is still in validation / active development rather than public open-source distribution

## Operating Style

- Fractional / consulting work still follows the broader CTO operating model:
  - architecture ownership
  - product feasibility discussion
  - pragmatic delivery decisions
  - hands-on work where leverage is highest

## Resume Takeaways

- Useful for roles that value:
  - internal platform / accelerator work
  - AI-enabled product foundations
  - MCP integration and agent tooling
  - LLM tooling against structured data and typed APIs
  - governed agentic admin workflows
  - safe tool-calling patterns with confirmation gating, RBAC, and auditability
  - hands-on fractional CTO work

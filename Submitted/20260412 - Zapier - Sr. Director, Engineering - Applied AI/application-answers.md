# Zapier Application Answers

## LLM Time-Spent Answer

Recommendation: choose `<25%` if your honest trailing-12-month average is closer to `20%`.

Why:
- Zapier is more likely to care about the quality and specificity of your AI answers than whether you picked the more aggressive bucket.
- If your written answers clearly show deep, practical use of AI in both product and engineering workflows, `<25%` will not read as weak.
- `25-50%` is only better if you feel comfortable defending that as a true year-long average rather than a recent spike.

## 1. How did you hear about this role?

I found the role through Zapier’s Ashby posting while reviewing remote engineering leadership openings focused on applied AI and workflow automation.

Alternative if you want it a touch more direct:

I came across the role through Zapier’s Ashby job posting during a search for remote applied AI engineering leadership roles.

## 2. Please describe the team you're managing.

In my current CTO role at Pitchstone, I grew the engineering organization from 6 to about 35 people across four agile teams. The formal reporting structure included a Development Manager reporting to me, with the teams organized around product and platform delivery. Typical team composition was 4-5 developers, 2-3 QA engineers, and a Product Owner. I stayed directly involved in architecture, hiring, planning rhythms, product shaping, and engineering standards, while the teams were responsible for customer-facing platform work, document workflows, partner APIs, and production delivery.

## 3. What type of customer tools/features have you recently created or enhanced with AI? What business impact did it have?

The clearest recent example is at Pitchstone, where I led AI-based lease and LOI data-point extraction for a customer-facing real-estate platform using Textract, Comprehend, and vision OCR. The workflow extracted targeted data points from uploaded documents and presented the results to users for review or override before commit.

The business impact was that we turned a slow, manual document-review step into a product capability that customers could actually use in production. The win was not just speed. It improved consistency, reduced re-keying, and made the workflow more trustworthy because users could validate and correct the extracted values instead of treating AI output as a black box.

I also built AI knowledge workflows on Bedrock to support product direction and customer-facing retrieval use cases, helping show both internal stakeholders and external partners that we could ship practical generative AI features rather than just prototype them.

## 4. Over the past year, approximately how much of your time has been spent using LLMs?

Recommended answer: `<25%`

Reasoning:
- If you think the real yearly average is around 20%, use the truthful bucket.
- Your other answers already show serious usage, so you do not need to inflate this one.

## 5. Describe your experience working with machine learning (ML) over the past 7+ years...

My experience with ML has been more on the applied-product and engineering side than on the research or model-development side. At Lela, I led engineering for a personalized shopping recommendation platform, but the deeper ML-specific work was handled by a dedicated ML developer on the team. More recently at Pitchstone, my work has centered on production AI capabilities built on managed services and LLM workflows: Textract/Comprehend-based document data-point extraction, Bedrock-based knowledge workflows, embeddings/vector search, and LLM-driven tool and admin workflows.

What I do bring very directly is the engineering side of getting those capabilities into real products. I write and lead teams toward clean, maintainable code with strong modular boundaries, OOP where it fits, unit and integration testing, and reproducible packaging and deployment patterns. My hands-on work has spanned Java/Spring services, Python services, and TypeScript/React/Node applications, and I have also used AI-assisted development tools directly in modernization and testing workflows.

So I would not present myself as someone whose main focus has been building custom ML models from scratch. My strength is taking AI/ML-backed capabilities, integrating them into real products and workflows, and making them usable, reviewable, and production-ready.

## 6. Pick one AI workflow you've built. Walk us through what triggers it, what it does, and what you had to iterate on.

One workflow I built was a controlled AI admin assistant on top of an internal application scaffold and admin API.

Trigger:
A SUPERADMIN enters a natural-language request such as “disable this user,” “retry the failed jobs,” or “show me the current system status.”

What it does:
The request goes into an agent loop that maps the prompt to typed tools. Those tools call the existing admin API rather than hitting the database directly. The workflow can inspect users, background jobs, and system state, and it can take selected actions through the same API paths used by the admin UI. For destructive actions, it first returns a confirmation step instead of executing immediately.

What I had to iterate on:
The biggest iterations were around safety and trust. I moved the workflow away from unconstrained “chat” behavior and into typed tool calls. I added confirmation-gating for destructive actions, and I made sure those actions still flowed through the existing RBAC, audit logging, and webhook paths. I also had to tune how the assistant surfaced pending actions so the human reviewer understood exactly what would happen before approving it.

Link/screenshot note:
I've uploaded a public, redacted PDF to Google Drive with screen shots at https://drive.google.com/file/d/1l-71WKIy8a5aBNmR-ESS9YKyGOwIEwng/view?usp=sharing

## 7. Share a specific example where AI changed quality or stakeholder experience — not just speed.

The best example is the lease and LOI data-point extraction workflow at Pitchstone. The easy version of that story is “AI made document processing faster,” but the more important improvement was quality and trust.

Instead of treating extraction as a black-box output, I designed the workflow so the system extracted targeted values, applied document-specific rules, and then showed the results to the user for review or override before anything was committed. That changed stakeholder experience in a big way. Customers were no longer being asked to trust a generative answer on faith. They could see what the system extracted, correct it where needed, and move forward with confidence.

That made the feature usable in a real workflow. It improved quality because users caught edge cases before commit, and it improved the stakeholder experience because the AI felt assistive and accountable rather than magical and risky.

## 8. What’s one way you’ve expanded your impact at work with AI?

One of the clearest examples is how I used Claude Code in modernization work. The problem was a large upgrade and test-generation effort that would traditionally have taken about four months to work through safely. I started using AI to help plan upgrades, handle repetitive boilerplate, and migrate or generate tests across version changes while still reviewing the output carefully.

I approached it that way because this was exactly the kind of work where AI could help without lowering the bar. Over time, my approach evolved from one-off prompting into a more disciplined workflow: smaller upgrade batches, better review checkpoints, using AI where it shines for boilerplate and test migration, and keeping a high bar for what actually got merged.

The impact was not just faster output. It changed the stakeholder experience because modernization work that would normally drag on in the background became something we could move through in smaller, more reviewable increments. In one case, it cut delivery time from about four months to three weeks.

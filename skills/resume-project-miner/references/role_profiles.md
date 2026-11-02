# Role and JD profiles

## JD adaptation

Extract four lists before ranking: responsibilities, core technologies, bonus qualifications, and business/domain language. Map each term to an existing evidence-ledger row. Natural keyword use is allowed only when the project actually demonstrates it. Missing JD terms belong in the gap analysis, never in a fabricated bullet.

Rank candidates by `evidence strength × personal attribution × role relevance × technical judgment × result clarity`. Evidence and attribution outrank keyword overlap.

## Role lenses

| Direction | Prefer evidence about |
|---|---|
| Frontend | rendering and bundle performance, state boundaries, component systems, accessibility, interaction, engineering toolchain |
| Backend | API contracts, data models, transactions, caching, concurrency, authorization, failure handling, observability |
| Full stack | end-to-end boundary decisions, shared contracts, delivery, cross-layer debugging |
| iOS / Android / desktop | lifecycle, native APIs, concurrency, offline data, performance, compatibility, packaging |
| AI application | model integration, prompt/data boundaries, RAG, tool calling, evaluation, latency/cost controls, safety |
| Agent development | workflow/state machines, context and memory, tool permissions, recovery, evaluation, observability |
| Algorithm / ML | data lineage, experiment design, training, metrics, inference, reproducibility, model tradeoffs |
| Data engineering / analysis | ingestion, transformation, quality, lineage, orchestration, query performance, decision support |
| Test development | automation architecture, coverage evidence, quality gates, fault injection, flaky-test control, diagnosis |
| DevOps / SRE | CI/CD, infrastructure, rollout/rollback, SLO signals, incident prevention, cost/reliability tradeoffs |
| Security | trust boundaries, authentication/authorization, threat models, vulnerability remediation, audit/data protection |
| Systems / infrastructure | concurrency, storage, networking, resource control, protocols, profiling, portability |
| Audio/video/graphics/3D | render/media pipelines, codecs, latency, frame rate, memory, numerical correctness, device adaptation |
| Embedded | hardware interfaces, timing, memory/power limits, RTOS, reliability, testability |
| Product-technical hybrid | problem discovery, technical feasibility, delivery loop, measurable user/business outcome |
| Custom role | Derive a profile from the user's description or JD; retain the same evidence gates |

For a general request, select the three strongest directions by supported modules, contribution evidence, and demonstrated problem-solving. Explain why each fits and what evidence is missing.

## Highlight test

A highlight should answer: What constraint made this non-trivial? What did the user decide or change? Why was that choice appropriate? What observable capability or risk changed? Prefer solved problems over technology inventories, and decision tradeoffs over feature lists.

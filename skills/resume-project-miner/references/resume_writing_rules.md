# Chinese resume and interview output rules

## Writing rules

- Use natural, professional Chinese and one core value per bullet.
- Default to 2-4 dense bullets only for a single project or coherent workstream. For an internship or role spanning several substantial product and technical workstreams, use one contribution overview plus 3-6 labeled sub-bullets, and allow distinct algorithm/tooling or client workstreams to remain separate bullets. Do not mechanically enforce a bullet count at the cost of an explicitly requested or resume-relevant contribution.
- Shape each bullet as `强动词 + 关键问题/任务 + 技术行动 + 可验证结果或影响` without printing STAR labels.
- Name technology only where it explains the action or constraint. Avoid adjective stacking, generic praise, and AI-like slogans.
- When no metric is proven, state a concrete capability, boundary, risk reduction, test gate, or compatibility result instead of a number.
- Match verbs to attribution: `独立实现` and `主导` require strong evidence; otherwise use `负责`, `参与`, `协同完成`, or team-level wording.
- Keep evidence analysis and resume persuasion as separate surfaces. Put `mock`, `占位`, `半成品`, `未完成`, `证据不足`, ownership caveats, and tempting-but-rejected claims in the fact summary, confirmation list, or authenticity audit unless that state itself is the technical constraint being solved. In final resume prose, describe the supported completed capability, technical decision, product value, or current responsibility boundary without leaking internal audit language.
- For ongoing work, lead with shipped or implemented facts, then describe the active direction with `正在推进` or `持续参与`. Do not downgrade completed work to an experiment merely because the broader workstream continues, and do not claim the result of a refactor, optimization, launch, or adoption before evidence exists.
- A conservative version lowers attribution/effect strength. An enterprising version may foreground stronger A-grade evidence, but may not add facts.
- For projects with several related contributions, lead with one concise, evidence-backed contribution overview, then expand the strongest highlights. The overview must summarize only claims supported by the detailed bullets and must not introduce a broader ownership claim. When the user requests a hierarchy such as one major bullet followed by short labeled points, preserve it; use 2-6 Chinese-character labels such as `数据看板`, `性能优化`, `广告业务`, or `SEO 工程`, with one core value per labeled point.
- Order detailed bullets by resume value, not chronology or PR number: prioritize core-path impact, technical difficulty, demonstrated judgment, personal attribution strength, and target-role relevance. Treat evidence grade and attribution as hard gates; a technically central team feature does not outrank a strongly attributable contribution unless the user's bounded part remains explicit.
- Prefer media/rendering/data-flow/architecture work over peripheral fixes when it demonstrates a harder constraint and stronger role signal. Keep lower-level maintenance such as isolated copy or locale fixes only when it adds distinct evidence or fills available space.
- Treat `项目背景` and `个人负责` as optional orientation blocks, not mandatory filler. After evidence scanning, recommend and ask whether to include them when they help an interviewer understand the problem and the user's boundary faster than the bullets alone.
- Limit `项目背景` to 1-2 sentences covering the user/problem, product capability, and one essential system constraint. Do not copy README marketing, list features, claim market position, or exceed evidence grade B without corroboration.
- Limit `个人负责` to one sentence or at most three compact responsibility phrases. Derive it only from attributable A-grade boundaries, use the allowed contribution label, and distinguish owned modules from adjacent team systems. Never infer ownership from repository ownership, commit volume, dependency use, or broad participation.
- Keep orientation blocks and detailed bullets non-duplicative: background explains why the project exists; personal responsibility defines scope; contribution overview summarizes the verified change portfolio; detailed bullets prove the hardest actions and results. Remove a block when it repeats another or crowds out stronger evidence.
- Build a product capability map before drafting. Check at least: `核心任务闭环`, `输入/输出或创作模式`, `历史记录/内容沉淀`, `配置/模型/权限`, `首启/onboarding`, `平台集成`, and `交付/自动更新`. Add or remove categories to fit the product, but never skip a category merely because it is less technically difficult.
- For each mapped capability, record `用户价值 | current-state evidence | status`. Status must be one of `current`, `removed`, `UI-only`, `dependency-only`, or `unverified`. Mention only `current` capabilities in the project background or positioning.
- Derive positioning with `目标用户/场景 + existing alternative or friction + complete capability journey + differentiating value`. Keep it to one sentence and prefer a concrete workflow improvement over labels such as “AI-powered”, “all-in-one”, or “industry-leading”.
- Separate product breadth from resume highlights: the background may summarize the complete current journey, while detailed bullets select the strongest evidence-backed decisions without dropping a distinct required workstream. Preserve important breadth such as history, settings, onboarding, privacy, SEO, delivery, or updates when it materially explains product completeness; do not force every feature into a technical bullet.
- Pair product and technical meaning. For each core highlight, make clear which user journey, business workflow, or product outcome it serves and which engineering constraint or decision made the contribution non-trivial. Do not reduce the entry to either a feature inventory or a technology inventory. When several workstreams form one product journey, state that journey explicitly before the technical details.
- Build a `required coverage ledger` before drafting with one row for every user-named product line, workstream, platform, technical boundary, measurable result, and requested presentation element. Mark each row `include`, `audit-only`, or `omit-with-reason`. A final resume version must include every `include` row; if space requires removal, provide the compact omission rationale and retain the item in a fuller version. Never silently omit an item such as SEO, performance work, tooling, or client work merely because another highlight ranks higher.
- Add `技术栈：...` as the first content line of every project entry, before `项目背景`. Use Chinese enumeration commas (`、`) with no trailing punctuation list and normally keep 4-7 items.
- Rank stack items by project relevance: core framework/runtime first, then primary language or rendering/native boundary, then essential storage or communication technology. Adapt the order to the project rather than using a fixed frontend/backend sequence.
- Include only stack items that help an interviewer understand the architecture or strongest contribution. Exclude minor libraries, component kits, icons, CSS helpers, build/lint/format tools, test utilities, generic protocols, incidental plugins, and technologies used only in a narrow leaf feature. Do not list both a broad category and its trivial sub-tools merely to increase count.

## Required output

### A. 项目事实摘要

State the positioning value, current product capability map, problem, stack, architecture/core modules, user responsibility, repository/ref/time scope, and evidence coverage. Separate fact from inference, and call out removed/UI-only/dependency-only/unverified capabilities that are tempting to overclaim.

### B. 候选亮点池

Use a table with: `亮点 | 技术难度 | 岗位相关性 | 个人贡献 | 证据等级 | 安全证据来源 | 是否推荐写入`. Include rejected but tempting claims when useful for auditability.

### C. 最终简历版本

Provide project name, one-line positioning, a first-line `技术栈：A、B、C` summary, and paste-ready bullets. Record the user's choice on optional `项目背景` and `个人负责` blocks; if unanswered, provide a recommendation but keep the compact default limited to blocks that materially improve comprehension. When the project has multiple substantial contributions, use one `贡献总览` bullet followed by the number of detailed or labeled bullets needed to cover the required ledger without redundancy; do not force the single-project 2-4 default onto a multi-workstream internship. Preserve the user's requested hierarchy and labels. Include a general version and target-role/JD version. Add conservative/enterprising variants only when uncertainty makes the distinction useful; neither may invent evidence. The final resume version must read as a coherent product and engineering story, not a development log or authenticity report.

### D. STAR 证据表

Use `Situation | Task | Action | Result | Evidence | Grade | Confirmation needed`. STAR is analysis material, not resume prose. Results may be qualitative when that is all evidence supports.

### E. 面试材料

Provide a 30-second introduction, a structured 3-minute introduction, 5-10 likely questions with answer points, attribution/knowledge risk points, and focused topics to study. Flag any answer that depends on user confirmation.

### F. 投递建议

State best-fit directions, JD matches when supplied, current description gaps, and the most valuable measurable evidence to collect. Without a target role, recommend exactly three directions and cite reasons.

### G. 真实性审计

List four groups: `可以直接写`, `需要用户确认`, `不建议写`, `明确禁止写`. Every final bullet must map to the A/B/C/D ledger. Explicitly reject fabricated metrics, false ownership, dependency-as-implementation, and unsupported business impact.

## One-round questions

Ask no more than five after scanning. For each use:

`问题 | 为什么需要 | 如何查找/测量 | 不回答时的保守写法`

Prioritize identity/ownership, actual responsibility boundary, deployment/use status, measured before/after result, the hardest decision, and the optional presentation choice for `项目背景` / `个人负责`. Do not ask for factual information already discoverable from safe repository evidence; presentation preference may still be asked once when it changes the final resume structure.

## Final resume gate

Before returning the resume version, verify all of the following:

- Every user-requested product line, workstream, platform, and named result appears or has an explicit omission reason.
- The entry communicates both the product journey and the strongest technical decisions.
- Audit/process terms do not appear in resume prose unless they describe the actual problem solved.
- Ongoing work distinguishes completed facts from current direction without predicting results.
- The requested hierarchy, labels, language, and compactness are preserved.
- Each bullet maps to the evidence ledger and uses an attribution verb allowed by its grade.
- The compact version trims redundancy before dropping a distinct high-value contribution.

Red flags that require rewriting the final resume version:

- A user-named contribution such as SEO, performance, tooling, product workflow, or client work vanished without an omission reason.
- The prose says `占位页`, `半成品`, `只是 mock`, `证据不足`, or similar audit language instead of stating the supported contribution.
- A multi-workstream internship was compressed to an arbitrary bullet limit.
- Technology is listed without the product problem it serves, or product features are listed without the engineering decision behind them.
- Ongoing work is written only as unfinished, or its future benefit is presented as already achieved.

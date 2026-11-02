# Evidence and authenticity rules

## Evidence grades

| Grade | Threshold | Resume treatment |
|---|---|---|
| A | Code plus attributable commit/PR/blame, or a test/benchmark/configuration directly proves the claim | May write as fact; cite source internally |
| B | Implementation supports a reasonable inference, but ownership, intent, or effect needs confirmation | Use conservative wording or place under confirmation |
| C | Repository cannot establish the claim; only the user can confirm it | Ask once; do not write as fact before confirmation |
| D | Evidence conflicts, attribution is false, claim is inflated, or capability belongs only to a dependency | Exclude and list under prohibited/not recommended |

README text alone cannot exceed B. A dependency declaration proves adoption, not independent implementation. Code volume is never evidence of difficulty, ownership, or value.

Project background may combine A-grade repository facts with B-grade README/product positioning only when clearly separated from personal contribution. Personal responsibility requires attributable A-grade evidence; user confirmation may narrow or clarify the boundary but cannot override conflicting repository history.

Treat product capability as a temporal claim. A current source path plus reachable wiring, test, command registration, route, or configuration can prove a capability is current. Historical commits alone prove only that it once existed. A removed feature, mock UI, dormant dependency, unregistered handler, or disconnected screen must not appear in current positioning; record it as removed, UI-only, dependency-only, or unverified.

A manifest proves that a technology is present, not that it belongs in the resume stack. Include it only when current source and attributable work show that it materially shapes the architecture, core workflow, storage, rendering, native boundary, or network protocol. Exclude transitive dependencies, UI primitives, icon libraries, styling helpers, build/lint/format tools, test utilities, one-off plugins, and narrow implementation details unless the target role makes that detail central.

## Contribution labels

| Label | Required evidence |
|---|---|
| 独立实现 | User-authored history covers the feature and no material co-author/contradictory ownership appears |
| 主导 | Design/PR/commit history demonstrates primary decision-making and substantial implementation |
| 负责 | Attributable implementation spans the claimed boundary; leadership is not implied |
| 参与 | Attributable commits, reviews, tests, integration, or fixes prove a bounded contribution |
| 协同完成 | Multiple contributors share the outcome and the user's part is identifiable |
| 团队成果 | Repository proves the outcome but not the user's personal share |
| 无法归属 | Feature exists, but available identity/history cannot connect it to the user |

Resolve aliases from local Git name/email, GitHub login, `.mailmap`, commit authors, PR/review/Issue authors, and user confirmation. Do not equate the current OS account, repository owner, or most prolific author with the user. If aliases conflict, ask once after discovery.

## Claim ledger

Maintain one internal row per candidate:

`claim | project fact | user action | observable effect | grade | attribution label | role fit | safe evidence pointers | caveat`

Evidence pointers may include repository-relative path and symbol, commit SHA, PR/Issue/Review URL or number, test name, benchmark output, release, Action, migration, schema, or configuration. For private repositories, keep excerpts minimal and omit sensitive logic.

## Quantification gate

Write a number only when all are true:

1. A command, test, benchmark, Git query, bundle report, configuration, or user-provided record reproduces it.
2. The baseline and comparison are semantically valid.
3. The measurement is attributable to the claimed action.
4. The source and calculation are recorded.

Otherwise describe a verifiable qualitative improvement such as eliminating a duplicated path, adding a regression gate, defining an authorization boundary, or supporting an offline state. Never convert file counts, commits, stars, or LOC into business impact.

## Privacy and conflict handling

- Exclude `.env*`, credentials, certificates, key stores, tokens, auth headers, secret managers' values, and unrelated files.
- Mention only the category of suspected secret; never echo it.
- Do not paste private source, proprietary algorithms, complete schemas, customer names, internal URLs, personal emails, or unreleased business details. Use emails internally only to resolve identity, then redact them from user-facing output.
- Mark conflicting claims D until resolved. Repository facts override promotional prose; explicit user context may supplement, not rewrite, repository evidence.

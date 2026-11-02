# Resume Project Miner

Evidence-first Codex Skill for mining real Git and GitHub history into Chinese resume bullets, STAR evidence, interview preparation, role/JD adaptation, and authenticity audits.

It supports local repositories and authenticated public/private GitHub repositories while keeping repository operations read-only. Claims are graded A-D, personal contribution is separated from team outcomes, and unsupported metrics or ownership are rejected.

## Install

Clone into your personal Codex skills directory:

```bash
git clone https://github.com/auberginewly/resume-project-miner.git "${CODEX_HOME:-$HOME/.codex}/skills/resume-project-miner"
```

If your skills directory is managed by another repository, add this folder there or copy the six Skill files while preserving their paths.

Requirements: Bash and Git. Remote GitHub sources additionally require [GitHub CLI](https://cli.github.com/) with an existing `gh auth login` session. No token is stored by the Skill.

## Examples

```text
@resume-project-miner 扫描当前仓库，生成适合前端实习的简历项目描述。
@resume-project-miner 分析 owner/private-repo，读取我的 commit 和 PR，生成后端岗位版本。
@resume-project-miner 结合下面的招聘 JD 重新筛选亮点：<JD>
@resume-project-miner 只做真实性审计，检查现有项目描述是否夸大。
```

## Safety

- Repository access is read-only.
- Evidence artifacts redact email addresses and exclude common secret, dependency, generated, and build paths.
- Private source and credentials must not be reproduced in final output.
- Metrics and personal ownership require reproducible evidence.

See [SKILL.md](SKILL.md) for the workflow and the files under `references/` for evidence and writing rules.

## License

MIT

<p align="center"><img src="banner.svg" alt="AI Auto Resume" width="100%"></p>

<h1 align="center">AI Auto Resume</h1>
<p align="center">One prompt to turn your experience into a polished PDF resume.</p>
<p align="center"><a href="../README.md">简体中文</a> · <strong>English</strong></p>

<p align="center">
  <a href="https://github.com/Kidding-Ma/ai-auto-resume/stargazers"><img src="https://img.shields.io/github/stars/Kidding-Ma/ai-auto-resume?style=flat&amp;logo=github&amp;color=14b8a6" alt="GitHub stars"></a>
  <a href="https://github.com/Kidding-Ma/ai-auto-resume/actions/workflows/check.yml"><img src="https://github.com/Kidding-Ma/ai-auto-resume/actions/workflows/check.yml/badge.svg?branch=main" alt="Project checks"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/Code-MIT-2563eb" alt="Code license: MIT"></a>
  <img src="https://img.shields.io/badge/Output-PDF-0f766e" alt="PDF output">
  <img src="https://img.shields.io/badge/Typesetting-LaTeX-334155" alt="LaTeX typesetting">
</p>

This Chinese-language preview is fictional. Its name, school, company and experience do not belong to a real applicant.

[![Resume preview](preview.png)](preview.pdf)

No resume-writing or LaTeX knowledge is needed.

## Get started

**1. Put your materials in the folder opened by your AI assistant.**

An old resume or project notes are enough. Add a photo if you want one. Starting from scratch? Create `about-me.txt`:

```text
Education: school, major, degree and dates
Experience: what you did, your responsibilities and results
Skills: what you have learned and actually used
Name and contact details: add when ready
```

Use what you have; leave the rest blank. A target role is optional. You can also include a job description.

**2. Send this prompt to your assistant.**

```text
Follow the latest AGENTS.md at https://github.com/Kidding-Ma/ai-auto-resume and use the materials in my current folder with the fixed template to create an English PDF resume; reuse existing tools and do not invent experience or numbers.
```

Open the PDF linked by your assistant and check the facts and contact details before applying. The PDF and editable source are saved in `output/` in your original folder. To revise it, say “Fit it on one page” or “Tailor it to this job description.”

We recommend **VS Code + Codex**. OpenCode, DeepSeek Harness and other assistants can use the same workflow if they can read local files and run commands. No separate skill or agent installation is required.

Reuse your existing LaTeX installation, editor and extensions. Add only what is missing. A chat-only interface cannot operate local files and compile the PDF. [Help (Chinese)](help.md)

## Credits and privacy

Uses the [Overleaf Chinese Resume Template](https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb), includes [resume-project-miner](https://github.com/auberginewly/resume-project-miner), and adapts writing methods from Reactive Resume and ResumeSkills. See [sources and credits](../THIRD_PARTY_NOTICES.md) for authors, licenses and changes.

Keep personal materials and generated resumes out of public repositories. This project does not automatically upload files; a cloud AI service may receive the content your assistant reads.

[Help (Chinese)](help.md) · [Code license](../LICENSE) · [Contributing](../CONTRIBUTING.md) · [Report an issue](https://github.com/Kidding-Ma/ai-auto-resume/issues/new/choose)

If this helps you, a Star is appreciated. Good luck with your applications!

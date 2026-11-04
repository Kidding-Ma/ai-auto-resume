<p align="center"><img src="docs/banner.svg" alt="AI Auto Resume" width="100%"></p>

<h1 align="center">AI 自动生成简历</h1>
<p align="center">只要一句提示词，就能生成高质量简历。</p>
<p align="center"><strong>简体中文</strong> · <a href="docs/README.en.md">English</a></p>

<p align="center">
  <a href="https://github.com/Kidding-Ma/ai-auto-resume/stargazers"><img src="https://img.shields.io/github/stars/Kidding-Ma/ai-auto-resume?style=flat&amp;logo=github&amp;color=14b8a6" alt="GitHub stars"></a>
  <a href="https://github.com/Kidding-Ma/ai-auto-resume/actions/workflows/check.yml"><img src="https://github.com/Kidding-Ma/ai-auto-resume/actions/workflows/check.yml/badge.svg?branch=main" alt="Project checks"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Code-MIT-2563eb" alt="Code license: MIT"></a>
  <img src="https://img.shields.io/badge/Output-PDF-0f766e" alt="PDF output">
  <img src="https://img.shields.io/badge/Typesetting-LaTeX-334155" alt="LaTeX typesetting">
</p>

下面是虚构示例，姓名、学校、公司和经历都不对应真实求职者。

[![简历效果预览](docs/preview.png)](docs/preview.pdf)

不用会写简历，也不用会 LaTeX。

## 怎么用

**1. 把材料放进 AI 打开的文件夹。**

旧简历、项目资料都可以直接放。有照片也可以一起放。没有旧简历，就新建 `个人情况.txt`：

```text
教育：学校、专业、学历、起止时间
经历：做过什么，自己负责什么，有什么成果
技能：学过什么、实际用过什么
姓名和联系方式：可以最后补
```

有什么写什么，没有的留空。求职意向不用填；有招聘要求也可以一起放。

**2. 把这句话发给 AI。**

```text
请按 https://github.com/Kidding-Ma/ai-auto-resume 的最新 AGENTS.md，用当前文件夹里的材料和固定模板生成 PDF 简历；已有工具直接用，不编造经历和数据。
```

完成后，打开 AI 给出的 PDF，核对事实与联系方式再投递。简历和可编辑源文件保存在原文件夹的 `output/` 中。想调整，继续说“压到一页”或“按这份招聘要求修改”即可。

推荐 **VS Code + Codex**。OpenCode、DeepSeek Harness 等能读取本地文件、运行命令的助手也可以，无需另外安装 skill 或 agent。

已有 LaTeX、编辑器和插件直接用，缺什么再补。只有网页聊天功能的 AI 无法直接操作本地文件、生成 PDF。[使用帮助](docs/help.md)

## 来源与隐私

采用 [Overleaf 中文简历模板](https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb)，内置 [resume-project-miner](https://github.com/auberginewly/resume-project-miner)，参考 Reactive Resume、ResumeSkills 的写作方法。作者、许可和调整见[参考来源与致谢](THIRD_PARTY_NOTICES.md)。

个人材料和成品不要上传到公开仓库。项目不会自动上传文件；使用云端 AI 时，读取的内容可能发送给所选服务。

[使用帮助](docs/help.md) · [代码许可](LICENSE) · [参与改进](CONTRIBUTING.md) · [反馈问题](https://github.com/Kidding-Ma/ai-auto-resume/issues/new/choose)

如果对你有帮助，欢迎点个 Star。祝你找到满意的工作！

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

<p align="center"><a href="#怎么用">开始使用</a> · <a href="docs/preview.pdf">查看简历</a> · <a href="docs/faq.md">常见问题</a></p>

下面是虚构示例，姓名、学校、公司和经历都不对应真实求职者。

[![简历效果预览](docs/preview.png)](docs/preview.pdf)

把个人情况放进工作区，剩下交给 AI。没有旧简历也能开始。

## 怎么用

有旧简历或项目资料，直接放进 AI 当前打开的文件夹。没有就新建 `个人情况.txt`，照着写几行：

```text
教育：学校、专业、学历、入学和毕业时间
经历：实习、课程作业、比赛、社团，自己做了什么
技能：学过什么、实际用过什么
姓名和联系方式：按需填写
求职意向：有就写，没有可不填
```

有什么写什么，没有的留空。想加照片，就把照片也放进去。

用 AI 助手打开这个文件夹，发送：

```text
用这个项目帮我生成简历：https://github.com/Kidding-Ma/ai-auto-resume
我的个人情况和材料就在当前工作区。
请先读项目的 AGENTS.md，按其中的写作和检查规则，用固定模板直接生成 PDF 简历。
已有工具直接用，缺什么再告诉我。不要编造经历和数据。
```

AI 会根据材料选择内容和顺序，默认省略空泛概述、减少解释性括号、把奖项等级写在前面。材料少也会先做出可审阅版本。

完成后打开 `output/resume.pdf`，核对事实与联系方式再投递。缺少必要信息时，AI 会说明还需补什么。

想调整时，直接说“保留原话”“偏学术”或“按这份招聘要求修改”，不用先填选项。

推荐使用 **VS Code + Codex**。已有 OpenCode、DeepSeek Harness 或其他 AI 助手也可以，只要能读取本地文件、运行命令，就用上面这段提示词。

已有 LaTeX、编辑器和插件直接用，不用重复安装。


[材料怎么写](docs/materials.md) · [缺少工具怎么办](docs/setup.md) · [常见问题](docs/faq.md)

## 说明与致谢

个人材料和生成的简历不要上传到公开仓库。项目不会自动上传文件；使用云端 AI 时，读取的内容可能发送给你选择的 AI 服务。

- 项目经历整理：[resume-project-miner](https://github.com/auberginewly/resume-project-miner)，作者 auberginewly。已内置。
- 固定模板：[Overleaf 中文简历模板](https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb)，作者 xiangrongjingujiu。保留原版排版参数，商业字体以开源字体替代；照片不挤偏姓名。
- 写作方法参考：[Reactive Resume](https://github.com/reactive-resume/reactive-resume) 与 [ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)。采用的方法与许可见[参考来源与致谢](THIRD_PARTY_NOTICES.md)。

[代码许可](LICENSE) · [参考来源与致谢](THIRD_PARTY_NOTICES.md) · [参与改进](CONTRIBUTING.md) · [反馈问题](https://github.com/Kidding-Ma/ai-auto-resume/issues/new/choose)

帮忙点点 star，这对我真的很重要，祝 offer 多多，谢谢。


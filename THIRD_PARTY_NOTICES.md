# 参考来源与致谢

这个项目使用了开源简历模板，也参考了其他项目的写作方法。本页说明它们来自哪里、用了什么，以及做了哪些调整。

## 简历模板来自哪里？

使用 [Overleaf 中文简历模板](https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb)，作者 **xiangrongjingujiu**，按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 使用。[查看完整许可](https://creativecommons.org/licenses/by/4.0/legalcode)。

保留原模板的字号、页边距、章节样式和横线。为了让更多电脑能编译，做了以下调整：

- 用开源的 TeX Gyre Termes 和 Fandol 字体替代原来的商业字体；字形会有细微区别。
- 允许联系方式换行，照片放在右上角，姓名仍相对整页居中。
- 去掉没有用到的图标字体和序数宏包依赖。

公开示例中的人物和经历全部虚构。照片由使用者自行提供。商业字体、真人简历和照片均未随项目发布；使用的字体和排版组件遵循各自的许可。

早期版本参考过 [billryan/resume](https://github.com/billryan/resume)，其 [MIT 许可](licenses/billryan-resume-MIT.txt)继续保留。

## 项目经历如何整理？

已内置 **auberginewly** 的 [resume-project-miner](https://github.com/auberginewly/resume-project-miner)。它用项目代码和提交记录帮助区分项目事实与个人贡献，按 [MIT 许可](skills/resume-project-miner/LICENSE)使用。

## 写作方法参考了谁？

| 项目 | 本项目采用的方法 | 许可 |
| --- | --- | --- |
| [Reactive Resume](https://github.com/reactive-resume/reactive-resume)，Amruth Pillai | 先整理事实，按经历安排内容，用具体行动和真实结果写项目 | [MIT](licenses/reactive-resume-MIT.txt) |
| [ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)，Resume Skills | 检查每条描述是否说清做了什么、怎么做、有什么结果 | [MIT](licenses/resume-skills-MIT.txt) |

采用的方法已改写成适合中文简历的[写作规则](docs/writing-rules.md)，无需额外安装这两个项目。保留有证据的行动、做法和结果，不采用“每条必须有数字”或无依据估算指标的建议；多轮访谈简化为最多一轮关键事实确认。参考版本记录在 [provenance.json](provenance.json)，使用者无需安装这些参考项目。

## 流程和润色参考

- 参考 [RenderCV](https://github.com/rendercv/rendercv) 的命令行工作方式，编译和检查可用一条命令完成。遇到缺字或溢出时指出相关日志。
- 参考 [Resume Matcher](https://github.com/srbhr/Resume-Matcher) 的岗位定向思路和 PDF 文字检查。岗位相关内容从用户已有经历中取材，生成后检查 PDF 能否提取文字。
- 参考 [Humanizer](https://github.com/blader/humanizer) 和 [Humanizer-zh](https://github.com/op7418/Humanizer-zh) 的精简方法，删掉套话、翻译腔和机械句式，保留清楚的原句。
- 参考 [Academic Humanizer](https://github.com/AIScientists-Dev/academic-humanizer) 的保真润色原则，保留原意、数字、术语和结论的确定程度。简历中直接改写有问题的句子，保留原本清楚的句子。该项目面向论文和基金申请，见 [Nature 新闻报道](https://www.nature.com/articles/d41586-026-02105-3)。

以上是思路参考。本项目独立实现，无需安装这些项目。

本项目新增的代码和文档使用 [MIT 许可](LICENSE)。模板及引用内容按上面各自的许可使用，原作者不因此代表或认可本项目。[版本记录](provenance.json)保留了参考文件的标识。

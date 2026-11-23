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

在 [简历写作 skill](skills/write-resume/SKILL.md) 中，简历条目优先写本人行动和可核实结果。缺少数字时写交付物，冲突集中确认一次。[版本记录](provenance.json)列出早期参考文件。

## 职业中心指南

- Harvard Mignone Center for Career Success 建议用事实和具体动作写简历，按重要性排列栏目。本项目允许有扎实成果的竞赛经历提前。 [Harvard 简历指南](https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/)
- MIT Career Advising & Professional Development 用任务、动作和成果帮助读者判断贡献，也建议有足够相关材料才用两页。这里先删重复，第二页从完整条目开始，保持固定字号。 [写经历](https://capd.mit.edu/resources/resumes-writing-about-your-skills/) · [取舍和篇幅](https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/)

## 构建、展示与润色

| 来源 | 采用的方法 | 许可 |
| --- | --- | --- |
| RenderCV 团队（rendercv） | 用一条命令生成并指出错误。公开成品可与输入对照。 | [MIT](https://github.com/rendercv/rendercv/blob/main/LICENSE) |
| Resume Matcher，Saurabh Rai 和贡献者 | 按用户给的招聘要求组织已有经历，导出后检查 PDF 文本。 | [Apache-2.0](https://github.com/srbhr/Resume-Matcher/blob/main/LICENSE) |
| Awesome CV，posquit0 和贡献者 | 首页直接展示可打开的 PDF，方便在试用前查看成品。 | [LPPL-1.3c](https://github.com/posquit0/Awesome-CV/blob/master/LICENCE) |
| Humanizer，blader | 删掉套话和机械句式，保留清楚的原句。 | [MIT](https://github.com/blader/humanizer/blob/main/LICENSE) |
| Humanizer-zh，op7418 和贡献者 | 润色中文时保留术语、归属和确定程度。 | [MIT](https://github.com/op7418/Humanizer-zh/blob/main/LICENSE) |
| Academic Humanizer，AIScientists-Dev | 让措辞与证据强度相符，例如保留测试范围和论文实际状态。 | [MIT](https://github.com/AIScientists-Dev/academic-humanizer/blob/main/LICENSE) |

这些方法由本项目重新表述，相关项目无需安装。本项目新增代码和文档使用 [MIT 许可](LICENSE)，模板和随附内容沿用各自许可。

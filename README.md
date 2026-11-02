# AI 自动生成简历

AI 自动生成简历工作流，简单又好用。

下面是虚构示例，姓名、学校、公司和经历都不对应真实求职者。

[![简历效果预览](docs/preview.png)](docs/preview.pdf)

**把个人情况交给 AI，自动生成 PDF 简历。不会写简历也能开始。**

## 怎么用

有旧简历或项目资料，直接放进工作区。没有就新建 `个人情况.txt`，照着写几行：

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
请先读项目的 AGENTS.md，再根据我的材料直接生成 PDF 简历。
已有工具直接用，缺什么再告诉我。不要编造经历和数据。
```

完成后打开 `output/resume.pdf`，核对信息就可以投递。

推荐使用 **VS Code + Codex**。已有 OpenCode、DeepSeek Harness 或其他 AI 助手也可以，只要能读取本地文件、运行命令，就用上面这段提示词。

已有 LaTeX、编辑器和插件直接用，不用重复安装。

想修改，继续说：“压到一页”或“按这份招聘要求改一版”。

[材料怎么写](docs/materials.md) · [缺少工具怎么办](docs/setup.md) · [常见问题](docs/faq.md)

## 说明与致谢

个人材料和生成的简历不要上传到公开仓库。项目不会自动上传文件；使用云端 AI 时，读取的内容可能发送给你选择的 AI 服务。

- 项目经历整理：[resume-project-miner](https://github.com/auberginewly/resume-project-miner)，作者 auberginewly。已内置。
- LaTeX 模板：[billryan/resume](https://github.com/billryan/resume)，本项目调整了字体、间距和照片排版。
- 排版参考：[Overleaf 中文简历模板](https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb)，作者 xiangrongjingujiu。

[MIT 许可](LICENSE) · [第三方许可](THIRD_PARTY_NOTICES.md) · [参与改进](CONTRIBUTING.md) · [反馈问题](https://github.com/Kidding-Ma/ai-auto-resume/issues/new/choose)

觉得有用，欢迎点个 Star。

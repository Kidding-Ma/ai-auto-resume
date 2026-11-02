# 发布到 GitHub

仓库名称建议：`ai-auto-resume`

中文标题：AI 自动生成简历

一句话介绍（复制到 GitHub 的 Description）：

```text
把旧简历、项目资料和招聘要求交给 AI，生成用 LaTeX 排版的 PDF 简历。
```

## 最少操作的发布方法

1. 登录 GitHub，点击右上角 `+` → **New repository**。
2. 名称填 `ai-auto-resume`，可见性选 **Public**，点击 **Create repository**。
3. 解压准备好的公开发布包，把包内文件和文件夹上传到仓库根目录。README.md、AGENTS.md、templates、skills 等应直接位于根目录，别多套一层文件夹。
4. 检查上传列表，只应包含模板、虚构示例和通用说明。确认没有 materials 中的真人文件、workspace 草稿或 output 成品，再提交。
5. 在仓库右侧 About 设置一句话介绍，并添加话题：`ai`、`resume`、`latex`、`chinese-resume`、`job-search`、`vscode`、`codex`。

浏览器上传可能漏掉隐藏文件夹。务必确认 `.vscode` 和 `.github` 也已上传；如果文件选择器看不到它们，使用 Git 推送更稳妥。

使用 Git 的用户可在本项目目录下运行：

```powershell
git init -b main
git add README.md AGENTS.md LICENSE THIRD_PARTY_NOTICES.md CONTRIBUTING.md .gitignore .gitattributes provenance.json docs templates examples skills licenses scripts tests .vscode .github materials/README.md workspace/README.md output/README.md
python scripts/resume.py privacy
git diff --cached --stat
git diff --cached
git commit -m "Initial public release"
git remote add origin https://github.com/你的用户名/ai-auto-resume.git
git push -u origin main
```

若已初始化 Git 或配置 origin，跳过对应步骤。提交会使用本机 Git 作者配置；不想公开个人邮箱时，先在 GitHub 邮箱设置里启用隐私，并为当前项目设置 GitHub 提供的 noreply 邮箱。

## 发布前检查

- 首页保留三步流程和可直接复制的提示词，避免先讲一大段技术。
- 确认 README 提示词中的仓库地址可以打开。
- 保留虚构 PDF 预览，让大家先看到结果。
- 开启仓库的 **Template repository** 选项，方便他人创建自己的副本。
- 用 Release 发布检查过的公开源码 ZIP。不要打包整个求职工作区。

分享时可以用这段话：

```text
做了一个 AI 自动生成简历的开源项目。
把旧简历、实习记录、项目说明和岗位 JD 放进文件夹，告诉 AI 想投什么岗位，
它会整理经历、筛选项目亮点，生成用 LaTeX 排版的 PDF 简历。
不用自己写 LaTeX，照着三步教程就能开始。示例使用虚构信息，个人材料和简历默认不提交到 Git。
项目地址：https://github.com/Kidding-Ma/ai-auto-resume
```

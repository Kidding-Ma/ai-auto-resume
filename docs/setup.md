# 电脑需要装什么

**先检查，缺什么再装什么。** 已经能生成 PDF，就跳过安装。

把这段话发给 AI：

```text
请检查我电脑上的 LaTeX、编辑器和插件，试着编译本项目的示例。
已经能用的直接用，不要重复安装或覆盖配置。
如果失败，先检查是不是路径或组件缺失，只告诉我必须补哪一项。
```

## 已经装过 LaTeX

让 AI 先试。MiKTeX、TeX Live、MacTeX 都可以，本项目需要能运行 XeLaTeX。

提示“找不到 xelatex”时，先检查安装位置和系统搜索路径（PATH）。只缺 XeLaTeX、字体或宏包时，在现有安装中补齐，不必再装另一套。

## 从没装过 LaTeX

LaTeX 负责把简历文字排成 PDF。按电脑系统选一个即可：

| 系统 | 可以安装 |
| --- | --- |
| Windows | [MiKTeX](https://miktex.org/download) 或 [TeX Live](https://www.tug.org/texlive/) |
| macOS | [MacTeX](https://www.tug.org/mactex/) |
| Linux | 系统软件源中的 TeX Live，包含 XeLaTeX 和中文支持 |

如果选 MiKTeX，安装时将 **Install missing packages on-the-fly** 设为 **Always**。它会在第一次编译时下载缺少的组件，需要联网。[官方安装说明](https://miktex.org/howto/install-miktex)

安装完成后重新打开 AI 助手和编辑器，让它们找到新安装的程序。

## 想用 VS Code 查看和修改

已经有 VS Code 和可用的 LaTeX 插件就直接用。不需要为了这个项目再装一遍。

还没装、又希望手动编辑和预览时，可以安装：

1. [VS Code](https://code.visualstudio.com/)。
2. 在 VS Code 扩展中搜索 **LaTeX Workshop**，作者 **James Yu**。

用 VS Code 打开保存材料和 output 的文件夹。打开生成的 `output/resume.tex`，在左侧 TeX 面板点击 **Build LaTeX project**，编译后点击 **View LaTeX PDF** 查看。

本项目附带直接运行 XeLaTeX 的配置，不需要为这套配置另装 Perl。若模板下载在子文件夹中，让 AI 先检查当前工作区配置，必要时补充 XeLaTeX 编译方式。已有可用配置时保留即可。[插件说明](https://github.com/James-Yu/LaTeX-Workshop/wiki/Install)

AI 直接运行命令生成 PDF 时，可以不装 VS Code 或插件。

## AI 助手怎么选

使用你已有的、能读取本地文件和运行命令的 AI 助手即可，不限定模型。打开材料所在的文件夹，把首页提示词发给它。

DSH（DeepSeek Harness）、OpenCode 搭配 DeepSeek 等工具，都使用首页的同一段提示词，不用单独装简历插件。选择材料所在的文件夹作为工作区，允许助手读取材料并运行必要的编译命令即可。

还没有助手时，可以参考 [DSH 官方入口](https://deepseek.com/harness/) 或 [OpenCode 官方文档](https://opencode.ai/docs/zh-cn/)。已有工具能用就继续用，不用为了写简历换模型。

如果它说看不到你电脑上的文件，换到支持本地工作区的使用方式。只有聊天功能的窗口无法仅凭仓库链接操作电脑。

## 其他工具

项目提供了 Python 辅助脚本，但不是生成 PDF 的必需条件。已有 Python 3.10+ 可以直接运行；没有时，AI 也能直接调用 XeLaTeX，不必先装 Python。需要脚本时再从 [Python 官网](https://www.python.org/downloads/)安装。

有 Python 时，可以让 AI 运行 `python scripts/resume.py doctor` 检查工具。分析项目的提交记录还需要 Git，已经装过就直接用。

本项目已在 Windows + MiKTeX 上验证编译，其他环境请先让 AI 编译虚构示例，确认能用后再生成你的简历。

# 第三方内容与修改

## resume-project-miner

来源：[auberginewly/resume-project-miner](https://github.com/auberginewly/resume-project-miner)，作者 auberginewly。

位于 skills/resume-project-miner，保留原始 MIT LICENSE。以本机安装的公开版本为快照，未复制任何用户材料。具体版本摘要见 provenance.json。

## LaTeX 模板

来源：https://github.com/billryan/resume ，MIT；原始许可证完整保留于 licenses/billryan-resume-MIT.txt。

排版参考：Overleaf 上由 xiangrongjingujiu 发布的 Chinese Resume Template（中文简历模板）：
https://cn.overleaf.com/latex/templates/chinese-resume-template-zhong-wen-jian-li-mo-ban/fbdypsjmgwbb

Overleaf 展示页标注 CC BY 4.0。本项目从 billryan/resume 的 MIT 上游获取类文件，未复制该展示页的示例正文、照片、Adobe 字体或字体附件。templates/resume.tex 的虚构正文为本项目新增。

本项目对 resume.cls 的修改：将相对字体文件路径改为发行版提供的 Latin Modern（按字体文件名加载，避免依赖系统字体缓存）；移除对 Fontin SmallCaps 文件的依赖；移除 FontAwesome 图标依赖，个人主页和社交链接使用文字；标题改为粗体并收紧章节间距。中文通过 ctex + Fandol 字体处理，不要求商业字体。resume.tex 新增可选照片排版，照片由用户自行提供，仅保存在本地 output 中。

宏包和字体由用户的 TeX 发行版按各自许可安装，不在本项目重新分发。

# 一起改进

欢迎修正文档、改进模板、补充虚构示例和平台兼容性。

1. 小修改可以直接提 PR；较大改动先开 Issue 讨论。不要上传真实简历、联系方式、公司内部信息或密钥。
2. 修改公开文件。新增公开文件时，在 .gitignore 中添加该文件的准确路径；不要放开整个目录。
3. 改脚本时运行 `python -m unittest discover -s tests -v`，提交前运行 `python scripts/resume.py privacy`。改模板时运行 `python scripts/resume.py demo` 并检查生成的页面，示例生成在 output/.demo 中，只有明确虚构的预览才能更新 docs/preview.pdf 和 preview.png。
4. 提交前用 `git diff --cached` 检查待公开内容，包含模板来源和许可证。

不要提交 AI 编造的性能数字、真实求职者样本或没有授权的模板与字体。

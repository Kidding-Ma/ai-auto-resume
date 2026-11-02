"""Local helpers. No AI API, credentials or upload functionality. Python 3.10+."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ('materials/', 'workspace/', 'output/', '.private/')
PUBLIC_DIRS = ('docs/', 'templates/', 'examples/', 'skills/', 'licenses/', 'scripts/', '.vscode/', '.github/', 'tests/')
PUBLIC_FILES = {'README.md', 'AGENTS.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'CONTRIBUTING.md', '.gitignore', '.gitattributes', 'provenance.json'}


def doctor():
    print('Python:', sys.version.split()[0])
    for command, required in [('xelatex', True), ('git', False), ('code', False), ('pdftoppm', False)]:
        print(f'{command}: ' + ('OK' if shutil.which(command) else ('未找到，先检查已有 LaTeX 安装和 PATH；确实缺少时再补齐 XeLaTeX，见 docs/setup.md' if required else '未找到（可选）')))
    print('已有 LaTeX 环境、编辑器和插件可直接复用，无需重复安装；编译 PDF 不依赖 VS Code 或插件。')
    print('项目不调用 AI API；请在 AI 编程助手中阅读 AGENTS.md 后开始。')
    return 0 if shutil.which('xelatex') else 1


def init():
    for directory in ('materials', 'workspace', 'output'):
        (ROOT / directory).mkdir(exist_ok=True)
    for name in ('resume.tex', 'resume.cls'):
        dest = ROOT / 'output' / name
        if not dest.exists():
            shutil.copyfile(ROOT / 'templates' / name, dest)
            print('初始化:', dest.relative_to(ROOT))
        else:
            print('保留已有文件:', dest.relative_to(ROOT))
    print('初始 tex 含虚构示例。请让 AI 依据 materials 改写后再投递。')
    return 0


def compile_at(directory):
    compiler = shutil.which('xelatex')
    if not compiler:
        print('未找到 XeLaTeX。先检查已有 LaTeX 安装和 PATH，缺少组件时在现有发行版补齐；确实没有环境再按 docs/setup.md 安装。本次没有生成新 PDF。')
        return 1
    source = directory / 'resume.tex'
    if not source.exists():
        print('缺少 resume.tex，请先让 AI 生成源文件。')
        return 1
    pdf = directory / 'resume.pdf'
    # Preserve the previous result, but never present it as a new successful build.
    if pdf.exists():
        backup = directory / '.previous'
        backup.mkdir(exist_ok=True)
        shutil.copy2(pdf, backup / 'resume.pdf')
        pdf.unlink()
    args = [compiler, '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', 'resume.tex']
    for _ in range(2):
        try:
            run = subprocess.run(args, cwd=directory, capture_output=True, timeout=240)
        except (subprocess.TimeoutExpired, OSError) as error:
            if pdf.exists():
                pdf.unlink()
            print('编译中断:', type(error).__name__, '请查看本地 resume.log。')
            return 1
        if run.returncode:
            if pdf.exists():
                pdf.unlink()
            print(run.stdout.decode('utf-8', errors='replace')[-3500:])
            print('编译失败，没有生成可用的新 PDF。详细信息在该目录的 resume.log。')
            return 1
    if not pdf.exists() or not pdf.read_bytes().startswith(b'%PDF-'):
        print('编译器未生成有效 PDF。')
        return 1
    log = (directory / 'resume.log').read_text(encoding='utf-8', errors='replace')
    if re.search(r'Overfull \\[hv]box|Missing character:', log):
        print('排版检查失败：发现溢出或缺字，请修正并检查 PDF。')
        return 1
    pages = re.search(r'Output written on .*?\((\d+) page', log)
    print('已编译:', pdf)
    if pages:
        print('页数:', pages.group(1))
    print('请打开 PDF 核对排版和事实；编译成功不代表经历已验证。')
    return 0


def build():
    return compile_at(ROOT / 'output')


def demo():
    directory = ROOT / 'workspace' / 'demo'
    directory.mkdir(parents=True, exist_ok=True)
    for name in ('resume.tex', 'resume.cls'):
        shutil.copyfile(ROOT / 'templates' / name, directory / name)
    return compile_at(directory)


def inspect_paths(paths):
    problems = []
    for name in paths:
        name = name.replace('\\', '/')
        if name in {'materials/README.md', 'workspace/README.md', 'output/README.md'}:
            continue
        if name.startswith(PRIVATE):
            problems.append((name, '私人文件正在被 Git 跟踪'))
            continue
        if not (name in PUBLIC_FILES or name.startswith(PUBLIC_DIRS)):
            problems.append((name, '不在公开文件清单中，请人工核对'))
        p = ROOT / name
        if not p.is_file():
            continue
        if p.is_symlink():
            problems.append((name, '禁止发布符号链接，避免指向私人材料'))
            continue
        if p.suffix.lower() in {'.pdf', '.png', '.jpg', '.zip', '.docx'}:
            if name not in {'docs/preview.pdf', 'docs/preview.png'}:
                problems.append((name, '未批准的二进制文件'))
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}', text):
            problems.append((name, '疑似密钥，请在本地检查；不回显内容'))
    return problems


def privacy():
    if not (ROOT / '.git').exists():
        print('当前不是 Git 仓库：可检查公开文件结构，但尚未验证 Git 跟踪状态。')
        names = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not p.relative_to(ROOT).as_posix().startswith(PRIVATE) and '__pycache__' not in p.parts]
    else:
        run = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True)
        names = [p for p in run.stdout.decode('utf-8').split('\0') if p]
    problems = inspect_paths(names)
    for name, reason in problems:
        print(f'需处理: {name} — {reason}')
    if problems:
        return 1
    print('检查通过：公开文件清单未发现私人目录文件或常见密钥。')
    print('此检查不识别所有个人信息，也不检查 Git 历史。发布前仍需查看暂存区和历史。')
    return 0


def main():
    parser = argparse.ArgumentParser(description='AI 自动生成简历：本地辅助工具')
    parser.add_argument('command', choices=['doctor', 'init', 'build', 'demo', 'privacy'])
    args = parser.parse_args()
    return globals()[args.command]()


if __name__ == '__main__':
    raise SystemExit(main())

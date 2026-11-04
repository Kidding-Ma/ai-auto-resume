"""Local helpers. No AI API, credentials or upload functionality. Python 3.10+."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = None

def workspace_root():
    return WORKSPACE if WORKSPACE is not None else ROOT


PRIVATE = ('materials/', 'workspace/', 'output/', '.private/')
PUBLIC_FILES = {'README.md', 'AGENTS.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'CONTRIBUTING.md', '.gitignore', '.gitattributes', 'provenance.json', 'templates/resume.tex', 'templates/resume.cls'}


def guard_path(path):
    """Reject links (including junctions) and dangling links before writing."""
    path = Path(path).absolute()
    if path.is_symlink() or path.resolve() != path:
        raise ValueError('输出路径包含链接，请使用普通文件夹: ' + str(path))
    return path


def output_paths(directory):
    directory = guard_path(directory)
    for name in ('resume.tex', 'resume.cls', 'resume.pdf', 'resume.log', 'resume.aux',
                 'resume.out', 'resume.synctex.gz', '.previous'):
        guard_path(directory / name)
    return directory


def public_paths():
    names = set(PUBLIC_FILES)
    ignore = ROOT / '.gitignore'
    if ignore.is_file():
        for line in ignore.read_text(encoding='utf-8').splitlines():
            if line.startswith('!/') and not line.endswith('/'):
                name = line[2:]
                if not any(c in name for c in '*?[]'):
                    names.add(name)
    return names


def doctor():
    print('Python:', sys.version.split()[0])
    for command, required in [('xelatex', True), ('git', False), ('code', False), ('pdftoppm', False)]:
        print(f'{command}: ' + ('OK' if shutil.which(command) else ('未找到，先检查已有 LaTeX 安装和 PATH；确实缺少时再补齐 XeLaTeX，见 docs/setup.md' if required else '未找到（可选）')))
    print('已有 LaTeX 环境、编辑器和插件可直接复用，无需重复安装；编译 PDF 不依赖 VS Code 或插件。')
    print('项目不调用 AI API；请在 AI 编程助手中阅读 AGENTS.md 后开始。')
    return 0 if shutil.which('xelatex') else 1


def init():
    destination = output_paths(workspace_root() / 'output')
    destination.mkdir(exist_ok=True)
    for name in ('resume.tex', 'resume.cls'):
        dest = destination / name
        if not dest.exists():
            shutil.copyfile(ROOT / 'templates' / name, dest)
            print('初始化:', dest)
        else:
            print('保留已有文件:', dest)
    print('初始 tex 含虚构示例。请让 AI 依据工作区材料改写后再投递。')
    return 0


def compile_at(directory):
    directory = output_paths(directory)
    pdf = directory / 'resume.pdf'
    # Archive first: even a preflight failure must not leave an old PDF as output.
    if pdf.exists():
        backup = directory / '.previous'
        backup.mkdir(exist_ok=True)
        previous = guard_path(backup / 'resume.pdf')
        if previous.exists():
            previous = guard_path(backup / ('resume-' + str(time.time_ns()) + '.pdf'))
        shutil.copy2(pdf, previous)
        pdf.unlink()
    compiler = shutil.which('xelatex')
    if not compiler:
        print('未找到 XeLaTeX。先检查已有 LaTeX 安装和 PATH，缺少组件时在现有发行版补齐；确实没有环境再按 docs/setup.md 安装。本次没有生成新 PDF。')
        return 1
    source = directory / 'resume.tex'
    if not source.exists():
        print('缺少 resume.tex，请先让 AI 生成源文件。')
        return 1
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
        if pdf.exists():
            pdf.unlink()
        print('编译器未生成有效 PDF。')
        return 1
    logfile = directory / 'resume.log'
    if not logfile.is_file():
        pdf.unlink()
        print('缺少编译日志，无法检查本次 PDF。')
        return 1
    log = logfile.read_text(encoding='utf-8', errors='replace')
    if re.search(r'Overfull \\[hv]box|Missing character:', log):
        pdf.unlink()
        print('排版检查失败：发现溢出或缺字，本次 PDF 未作为成品保留。')
        return 1
    pages = re.search(r'Output written on .*?\((\d+) page', log)
    print('已编译:', pdf)
    if pages:
        print('页数:', pages.group(1))
    print('请打开 PDF 核对排版和事实；编译成功不代表经历已验证。')
    return 0


def build():
    return compile_at(workspace_root() / 'output')


def demo():
    directory = output_paths(ROOT / 'output' / '.demo')
    directory.mkdir(parents=True, exist_ok=True)
    for name in ('resume.tex', 'resume.cls'):
        shutil.copyfile(ROOT / 'templates' / name, directory / name)
    return compile_at(directory)


def inspect_paths(paths):
    problems = []
    allowed = public_paths()
    for name in paths:
        name = name.replace('\\', '/')
        if Path(name).is_absolute() or '..' in Path(name).parts:
            problems.append((name, '不是仓库内的相对路径'))
            continue
        if name.startswith(PRIVATE):
            problems.append((name, '私人文件正在被 Git 跟踪'))
            continue
        if name not in allowed:
            problems.append((name, '不在公开文件清单中，请人工核对'))
        p = ROOT / name
        if p.is_symlink() or p.resolve() != p.absolute():
            problems.append((name, '禁止发布符号链接，避免指向私人材料'))
            continue
        if not p.is_file():
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
    parser.add_argument('--workspace', type=Path, help='材料所在的工作区；默认使用项目目录')
    args = parser.parse_args()
    global WORKSPACE
    if args.workspace is not None:
        WORKSPACE = args.workspace.resolve()
        if not WORKSPACE.is_dir():
            parser.error('工作区目录不存在')
    try:
        return globals()[args.command]()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('未完成:', str(error))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())


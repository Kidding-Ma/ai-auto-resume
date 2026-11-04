"""Local helpers. No AI API, credentials or upload functionality. Python 3.10+."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import time
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = None
WORKFLOW_VERSION = '2026-11-04.3'

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
    print('流程版本:', WORKFLOW_VERSION)
    print('工具目录:', ROOT)
    print('Python:', sys.version.split()[0])
    for command, required in [('xelatex', True), ('git', False), ('code', False), ('pdftoppm', False)]:
        print(f'{command}: ' + ('OK' if shutil.which(command) else ('未找到，先检查已有 LaTeX 安装和 PATH；确实缺少时再补齐 XeLaTeX，见 docs/help.md' if required else '未找到（可选）')))
    print('已有 LaTeX 环境、编辑器和插件可直接复用，无需重复安装；编译 PDF 不依赖 VS Code 或插件。')
    print('项目不调用 AI API；请在 AI 编程助手中阅读 AGENTS.md 后开始。')
    print('Word/TXT 读取不需要额外依赖；PDF 读取和预览可选用 PyMuPDF。')
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
    work = work_directory(directory)
    state_file = guard_path(work / 'build.json')
    state = {'status': 'started', 'pdf': 'resume.pdf', 'log': 'resume.log'}
    state_file.write_text(json.dumps(state), encoding='utf-8')
    report = guard_path(work / 'checks.json')
    if report.exists():
        report.unlink()
    pdf = directory / 'resume.pdf'
    job = 'resume'
    # Archive first: even a preflight failure must not leave an old PDF as output.
    if pdf.exists():
        backup = directory / '.previous'
        backup.mkdir(exist_ok=True)
        previous = guard_path(backup / 'resume.pdf')
        if previous.exists():
            previous = guard_path(backup / ('resume-' + str(time.time_ns()) + '.pdf'))
        shutil.copy2(pdf, previous)
        try:
            pdf.unlink()
        except PermissionError:
            # Readers on Windows may lock the old PDF. Never call it a new result.
            job = 'resume-optimized'
            for ext in ('.pdf', '.log', '.aux', '.out'):
                guard_path(directory / (job + ext))
            pdf = directory / (job + '.pdf')
            if pdf.exists():
                saved = guard_path(backup / ('resume-optimized-' + str(time.time_ns()) + '.pdf'))
                shutil.copy2(pdf, saved)
                pdf.unlink()
            print('原 PDF 正被占用，本次结果将另存为:', pdf)
    compiler = shutil.which('xelatex')
    if not compiler:
        print('未找到 XeLaTeX。先检查已有 LaTeX 安装和 PATH，缺少组件时在现有发行版补齐；确实没有环境再按 docs/help.md 安装。本次没有生成新 PDF。')
        return 1
    source = directory / 'resume.tex'
    if not source.exists():
        print('缺少 resume.tex，请先让 AI 生成源文件。')
        return 1
    args = [compiler, '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', 'resume.tex']
    if job != 'resume':
        args.insert(-1, '-jobname=' + job)
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
    logfile = directory / (job + '.log')
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
    state.update(status='compiled', pdf=pdf.name, log=logfile.name,
                 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                 pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
    cls = directory / 'resume.cls'
    if cls.is_file():
        state['class_sha256'] = hashlib.sha256(cls.read_bytes()).hexdigest()
    state_file.write_text(json.dumps(state), encoding='utf-8')
    print('请打开 PDF 核对排版和事实；编译成功不代表经历已验证。')
    return 0


def build():
    directory = output_paths(workspace_root() / 'output')
    problems = template_issues(directory)
    if problems:
        work = work_directory(directory)
        state = guard_path(work / 'build.json')
        state.write_text(json.dumps({'status': 'template-rejected', 'workflow_version': WORKFLOW_VERSION}), encoding='utf-8')
        report = guard_path(work / 'checks.json')
        if report.exists():
            report.unlink()
        for problem in problems:
            print('未生成:', problem)
        print('请备份已有文件，从当前项目模板恢复页眉和样式，再迁入真实正文。')
        return 1
    return compile_at(directory)


def fixed_header(text):
    """Mask only the identity macro; the rest of the template stays fixed."""
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    sections = list(re.finditer(r'\\section\s*\{', text))
    if not sections:
        raise ValueError('缺少简历章节')
    header = text[:sections[0].start()]
    matches = list(re.finditer(r'\\newcommand\s*\{\s*\\resumeidentity\s*\}\s*\{', header))
    if len(matches) != 1:
        raise ValueError('固定页眉结构不完整')
    match = matches[0]
    start = match.end()
    depth = 1
    end = start
    while end < len(header) and depth:
        char = header[end]
        slashes = len(header[:end]) - len(header[:end].rstrip('\\'))
        if slashes % 2 == 0:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
        end += 1
    if depth:
        raise ValueError('姓名与联系方式宏的括号不完整')
    identity = header[start:end - 1]
    masked = header[:start] + '<identity>' + header[end - 1:]
    return re.sub(r'\s+', '', masked), identity, text[sections[0].start():]


def template_issues(directory):
    directory = output_paths(directory)
    source, cls = directory / 'resume.tex', directory / 'resume.cls'
    if not source.is_file() or not cls.is_file():
        return ['缺少固定模板的 resume.tex 或 resume.cls，请先初始化']
    template = ROOT / 'templates'
    problems = []
    if cls.read_text(encoding='utf-8').strip() != (template / 'resume.cls').read_text(encoding='utf-8').strip():
        problems.append('resume.cls 与当前固定模板不同')
    try:
        expected, _, _ = fixed_header((template / 'resume.tex').read_text(encoding='utf-8'))
        actual, identity, body = fixed_header(source.read_text(encoding='utf-8'))
        if actual != expected:
            problems.append('页眉、字体或版式设置已偏离当前固定模板')
        overrides = r'\\(?:setmainfont|setsansfont|setmonofont|setCJK\w*font|linespread|setstretch|fontsize|geometry|newgeometry|restoregeometry|titlespacing|titleformat|setlength|addtolength|renewcommand|vspace|hspace|tiny|scriptsize|footnotesize|small)\b'
        if re.search(overrides, identity + '\n' + body):
            problems.append('正文或身份区域包含修改字号、行距、字体或版式的命令')
    except ValueError as error:
        problems.append(str(error))
    return problems


def demo():
    directory = output_paths(ROOT / 'output' / '.demo')
    directory.mkdir(parents=True, exist_ok=True)
    for name in ('resume.tex', 'resume.cls'):
        shutil.copyfile(ROOT / 'templates' / name, directory / name)
    return compile_at(directory)


def work_directory(directory):
    directory = output_paths(directory)
    directory.mkdir(exist_ok=True)
    work = guard_path(directory / '.work')
    work.mkdir(exist_ok=True)
    return work


def pdf_library():
    try:
        import pymupdf
        return pymupdf
    except ImportError:
        try:
            import fitz
            return fitz
        except ImportError:
            raise ValueError('缺少可选工具 PyMuPDF。可在当前 Python 中安装：python -m pip install PyMuPDF；也可用已有的 PDF 工具。')


def extract_material(source, directory):
    source = Path(source).resolve()
    if not source.is_file():
        raise ValueError('材料文件不存在')
    suffix = source.suffix.lower()
    if suffix == '.docx':
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        lines = []
        with zipfile.ZipFile(source) as archive:
            parts = ['word/document.xml'] + sorted(n for n in archive.namelist()
                if re.fullmatch(r'word/(?:header\d+|footer\d+|footnotes|endnotes)\.xml', n))
            for part in parts:
                for para in ET.fromstring(archive.read(part)).findall('.//w:p', ns):
                    text = ''.join(node.text or '' for node in para.findall('.//w:t', ns))
                    if text.strip():
                        lines.append(text)
            has_images = any(n.startswith('word/media/') for n in archive.namelist())
        text = '\n'.join(lines)
        if has_images:
            print('Word 中有图片：文字提取不等于识别图片，AI 需要另行查看。')
    elif suffix in {'.txt', '.md'}:
        data = source.read_bytes()
        try:
            text = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = data.decode('gb18030')
    elif suffix == '.pdf':
        engine = pdf_library()
        with engine.open(source) as doc:
            text = '\n'.join(page.get_text() for page in doc)
        if len(text.strip()) < 20:
            raise ValueError('PDF 提取出的文字太少，可能是扫描件，需要识别图片文字，不能当作材料为空。')
    else:
        raise ValueError('脚本支持 DOCX、TXT、MD 和有文字的 PDF；其他格式请用已有工具读取。')
    if not text.strip():
        raise ValueError('没有提取到文字，请检查材料是否只有图片。')
    work = work_directory(directory)
    key = hashlib.sha256(str(source).encode('utf-8')).hexdigest()[:12]
    target = guard_path(work / ('material-' + key + '.txt'))
    target.write_text(text, encoding='utf-8')
    print('已提取为 UTF-8 文本:', target)
    print('请让 AI 读取这个文件；不用把全部内容打印到终端。')
    return target


def check_pdf(directory, max_pages=1, render=True):
    """Check geometry and render with one engine; never infer factual accuracy."""
    directory = output_paths(directory)
    work = work_directory(directory)
    report_path = guard_path(work / 'checks.json')
    # Clear the old report before any failure, including a missing dependency.
    if report_path.exists():
        report_path.unlink()
    engine = pdf_library()
    issues, warnings = template_issues(directory), []
    state_file = guard_path(work / 'build.json')
    state = json.loads(state_file.read_text(encoding='utf-8')) if state_file.is_file() else {}
    if state and state.get('status') != 'compiled':
        issues.append('最近一次编译未成功，不能把旧 PDF 当作本次结果')
    if not state:
        warnings.append('没有辅助脚本的编译记录，只能检查现有 PDF；请人工确认它对应当前源文件')
    pdf_name = state.get('pdf', 'resume.pdf')
    log_name = state.get('log', 'resume.log')
    if pdf_name not in ('resume.pdf', 'resume-optimized.pdf') or log_name not in ('resume.log', 'resume-optimized.log'):
        raise ValueError('编译记录中的文件名无效')
    pdf_file = guard_path(directory / pdf_name)
    source = directory / 'resume.tex'
    if not source.is_file():
        raise ValueError('缺少 resume.tex，无法对照模板检查姓名')
    text = source.read_text(encoding='utf-8')
    if state.get('status') == 'compiled':
        if hashlib.sha256(source.read_bytes()).hexdigest() != state.get('source_sha256'):
            issues.append('源文件在编译后发生变化，需要重新生成 PDF')
        if hashlib.sha256(pdf_file.read_bytes()).hexdigest() != state.get('pdf_sha256'):
            issues.append('PDF 与最近一次编译记录不一致')
        if state.get('class_sha256') and hashlib.sha256((directory / 'resume.cls').read_bytes()).hexdigest() != state['class_sha256']:
            issues.append('模板在编译后发生变化，需要重新生成 PDF')
    match = re.search(r'\\name\s*\{([^{}]*)\}', text)
    expected_name = match.group(1).strip() if match else ''
    report = {'passed': False, 'issues': issues, 'warnings': warnings,
              'workflow_version': WORKFLOW_VERSION,
              'previews': [], 'facts_verified': False, 'pdf': pdf_name}
    with engine.open(pdf_file) as doc:
        report['pages'] = len(doc)
        if len(doc) > max_pages:
            issues.append('页数超过本次要求')
        if not expected_name:
            issues.append('没有填写模板中的姓名')
        if len(doc):
            page = doc[0]
            names = [box for box in page.search_for(expected_name) if box.y0 < page.rect.height / 4] if expected_name else []
            if len(names) != 1:
                issues.append('未能在页眉唯一识别姓名，需要查看预览')
            else:
                name = names[0]
                offset = (name.x0 + name.x1 - page.rect.width) / 2
                report['name_center_offset_pt'] = round(offset, 3)
                if abs(offset) > 1:
                    issues.append('姓名没有相对页面居中')
            for i, page in enumerate(doc):
                page_text = page.get_text()
                if not page_text.strip():
                    issues.append('存在无法提取文字的页面')
                spans = [span for block in page.get_text('dict')['blocks']
                         for line in block.get('lines', []) for span in line['spans']
                         if span['text'].strip()]
                for span in spans:
                    box = engine.Rect(span['bbox'])
                    if box.x0 < -1 or box.y0 < -1 or box.x1 > page.rect.width + 1 or box.y1 > page.rect.height + 1:
                        issues.append('文字超出页面边界')
                        break
                for image in page.get_image_info():
                    rect = engine.Rect(image['bbox'])
                    if any(rect.intersects(engine.Rect(s['bbox'])) for s in spans):
                        issues.append('图片可能遮挡文字')
                if render and i < max_pages:
                    preview = guard_path(work / ('page-' + str(i + 1) + '.png'))
                    page.get_pixmap(matrix=engine.Matrix(1.5, 1.5)).save(preview)
                    report['previews'].append(preview.name)
        else:
            issues.append('PDF 没有页面')
    log = guard_path(directory / log_name)
    if not log.is_file():
        issues.append('缺少本次编译日志')
    elif re.search(r'Overfull \\[hv]box|Missing character:', log.read_text(encoding='utf-8', errors='replace')):
        issues.append('编译日志存在溢出或缺字')
    if any(sample in text for sample in ('林小满', 'lin@example.com', '示例大学')):
        warnings.append('存在模板示例文字，请确认已替换')
    if re.search(r'[（(]', text):
        warnings.append('存在括号，请逐个核对是否必要')
    report['issues'] = list(dict.fromkeys(issues))
    report['passed'] = not issues
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('排版自动检查' + ('通过' if report['passed'] else '未通过') + ':', report_path)
    for issue in report['issues']:
        print('需处理:', issue)
    for warning in warnings:
        print('需核对:', warning)
    print('请查看生成的预览；检查结果不代表事实、奖项顺序或论文状态已核实。')
    return 0 if report['passed'] else 1


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
    parser.add_argument('--version', action='version', version=WORKFLOW_VERSION)
    parser.add_argument('command', choices=['doctor', 'init', 'build', 'demo', 'privacy', 'read', 'check'])
    parser.add_argument('--workspace', type=Path, help='材料所在的工作区；默认使用项目目录')
    parser.add_argument('--input', type=Path, dest='input_path', help='read 命令要读取的材料')
    parser.add_argument('--max-pages', type=int, default=1, help='check 允许的页数；默认 1')
    args = parser.parse_args()
    global WORKSPACE
    if args.workspace is not None:
        WORKSPACE = args.workspace.resolve()
        if not WORKSPACE.is_dir():
            parser.error('工作区目录不存在')
    try:
        if args.command == 'read':
            if args.input_path is None:
                parser.error('read 需要 --input 材料文件路径')
            extract_material(args.input_path, workspace_root() / 'output')
            return 0
        if args.command == 'check':
            if args.max_pages < 1:
                parser.error('--max-pages 必须大于 0')
            return check_pdf(workspace_root() / 'output', max_pages=args.max_pages)
        return globals()[args.command]()
    except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, ET.ParseError, subprocess.CalledProcessError) as error:
        print('未完成:', str(error))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    raise SystemExit(main())




"""Check privacy boundaries and preserve existing user work."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('resume', Path(__file__).resolve().parents[1] / 'scripts/resume.py')
resume = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resume)


class HelpersTest(unittest.TestCase):
    def test_private_and_unknown_files_blocked(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp).resolve()):
            problems = resume.inspect_paths(['materials/cv.txt', 'output/resume.pdf', 'workspace/facts.md', 'unknown.txt'])
            self.assertEqual(len(problems), 4)
            self.assertEqual(resume.inspect_paths(['README.md', 'templates/resume.tex']), [])

    def test_init_preserves_personal_draft(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp).resolve()):
            root = Path(tmp).resolve()
            (root / 'templates').mkdir()
            (root / 'output').mkdir()
            (root / 'templates/resume.tex').write_text('demo', encoding='utf-8')
            (root / 'templates/resume.cls').write_text('class', encoding='utf-8')
            (root / 'output/resume.tex').write_text('my own work', encoding='utf-8')
            resume.init()
            self.assertEqual((root / 'output/resume.tex').read_text(), 'my own work')
            self.assertTrue((root / 'output/resume.cls').exists())

    def test_external_workspace_keeps_materials_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            material = workspace / '旧简历.txt'
            material.write_text('Original material', encoding='utf-8')
            with patch.object(resume, 'WORKSPACE', workspace):
                resume.init()
                self.assertTrue((workspace / 'output/resume.cls').is_file())
                self.assertEqual(material.read_text(encoding='utf-8'), 'Original material')
                self.assertFalse((workspace / 'materials').exists())
                self.assertFalse((workspace / 'workspace').exists())
                with patch.object(resume, 'compile_at', return_value=0) as compile_at:
                    resume.build()
                    compile_at.assert_called_once_with(workspace / 'output')

    def test_git_ignores_new_materials_and_allows_public_files(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
            (workspace / '.gitignore').write_bytes((resume.ROOT / '.gitignore').read_bytes())
            paths = ['旧简历.pdf', '笔记.txt', '经历.docx', '项目/说明.md', 'output/resume.pdf', 'docs/私人材料.txt']
            result = subprocess.run(['git', 'check-ignore', '--stdin'], cwd=workspace,
                                    input='\n'.join(paths)+'\n', encoding='utf-8', capture_output=True)
            self.assertEqual(len(result.stdout.splitlines()), len(paths))
            public = subprocess.run(['git', 'check-ignore', 'README.md', 'templates/resume.tex'], cwd=workspace, capture_output=True)
            self.assertEqual(public.returncode, 1)

    def test_failed_build_does_not_leave_stale_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'resume.tex').write_text('broken', encoding='utf-8')
            (root / 'resume.pdf').write_bytes(b'%PDF-previous')
            with patch.object(resume.shutil, 'which', return_value='xelatex'), patch.object(resume.subprocess, 'run') as run:
                run.return_value.returncode = 1
                run.return_value.stdout = b'failed'
                self.assertEqual(resume.compile_at(root), 1)
            self.assertFalse((root / 'resume.pdf').exists())
            self.assertEqual((root / '.previous/resume.pdf').read_bytes(), b'%PDF-previous')

    def test_preflight_failure_archives_pdf_without_overwriting_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'resume.pdf').write_bytes(b'%PDF-newer')
            (root / '.previous').mkdir()
            (root / '.previous/resume.pdf').write_bytes(b'%PDF-older')
            with patch.object(resume.shutil, 'which', return_value=None):
                self.assertEqual(resume.compile_at(root), 1)
            self.assertFalse((root / 'resume.pdf').exists())
            self.assertEqual((root / '.previous/resume.pdf').read_bytes(), b'%PDF-older')
            self.assertEqual([p.read_bytes() for p in (root / '.previous').glob('resume-*.pdf')], [b'%PDF-newer'])

    def test_bad_layout_missing_log_and_invalid_pdf_are_not_deliverables(self):
        for log, data in [('Overfull \\hbox', b'%PDF-test'), ('Missing character:', b'%PDF-test'),
                          (None, b'%PDF-test'), ('Output written on resume.pdf (1 page)', b'broken')]:
            with self.subTest(log=log, data=data), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                (root / 'resume.tex').write_text('source')
                def fake_run(*args, **kwargs):
                    from types import SimpleNamespace
                    (root / 'resume.pdf').write_bytes(data)
                    if log is not None:
                        (root / 'resume.log').write_text(log)
                    return SimpleNamespace(returncode=0, stdout=b'')
                with patch.object(resume.shutil, 'which', return_value='xelatex'), patch.object(resume.subprocess, 'run', side_effect=fake_run):
                    self.assertEqual(resume.compile_at(root), 1)
                self.assertFalse((root / 'resume.pdf').exists())

    def test_init_rejects_dangling_link_without_writing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'output').mkdir()
            target = root / 'unrelated.txt'
            try:
                (root / 'output/resume.tex').symlink_to(target)
            except OSError:
                self.skipTest('creating symlinks is not permitted')
            with patch.object(resume, 'WORKSPACE', root):
                with self.assertRaises(ValueError):
                    resume.init()
            self.assertFalse(target.exists())

    def test_privacy_requires_exact_paths_even_inside_docs(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp).resolve()):
            root = Path(tmp).resolve()
            (root / '.gitignore').write_text('*\n!/docs/\n!/docs/faq.md\n')
            self.assertEqual(resume.inspect_paths(['docs/faq.md']), [])
            self.assertEqual(len(resume.inspect_paths(['docs/personal.txt', '../outside.txt'])), 2)

    def test_locked_pdf_is_preserved_and_new_result_has_its_own_record(self):
        import json
        from types import SimpleNamespace
        original_unlink = Path.unlink
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            old = root / 'resume.pdf'
            old.write_bytes(b'%PDF-original')
            (root / 'resume.tex').write_text('source')
            def unlink(path, *args, **kwargs):
                if path == old:
                    raise PermissionError('reader locks PDF')
                return original_unlink(path, *args, **kwargs)
            def run(args, **kwargs):
                self.assertIn('-jobname=resume-optimized', args)
                (root / 'resume-optimized.pdf').write_bytes(b'%PDF-new')
                (root / 'resume-optimized.log').write_text('Output written on resume-optimized.pdf (1 page)')
                return SimpleNamespace(returncode=0, stdout=b'')
            with patch.object(Path, 'unlink', unlink), patch.object(resume.shutil, 'which', return_value='xelatex'), patch.object(resume.subprocess, 'run', side_effect=run):
                self.assertEqual(resume.compile_at(root), 0)
            self.assertEqual(old.read_bytes(), b'%PDF-original')
            self.assertEqual((root / 'resume-optimized.pdf').read_bytes(), b'%PDF-new')
            state = json.loads((root / '.work/build.json').read_text())
            self.assertEqual(state['status'], 'compiled')
            self.assertEqual(state['pdf'], 'resume-optimized.pdf')

    def test_secret_detection_does_not_echo_secret(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp).resolve()):
            (Path(tmp).resolve() / 'README.md').write_text('ghp_' + 'x' * 30, encoding='utf-8')
            result = resume.inspect_paths(['README.md'])
            self.assertEqual(len(result), 1)
            self.assertNotIn('x' * 30, str(result))


class TemplateContractTest(unittest.TestCase):
    def prepare(self, root):
        (root / 'resume.tex').write_text((resume.ROOT / 'templates/resume.tex').read_text(encoding='utf-8'), encoding='utf-8')
        (root / 'resume.cls').write_bytes((resume.ROOT / 'templates/resume.cls').read_bytes())

    def test_identity_and_body_changes_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.prepare(root)
            source = root / 'resume.tex'
            text = source.read_text(encoding='utf-8').replace('林小满', '测试人').replace('lin@example.com', 'test@example.com').replace('校园预约系统', '真实课程作业')
            source.write_text(text, encoding='utf-8')
            self.assertEqual(resume.template_issues(root), [])

    def test_changed_mac_font_or_line_spacing_is_rejected(self):
        for before, after in [('fontset=none', 'fontset=macnew'),
                              (r'\section{教育背景}', r'\linespread{1.2}\section{教育背景}'),
                              ('p{2.4cm}', 'p{1.5cm}')]:
            with self.subTest(after=after), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                self.prepare(root)
                source = root / 'resume.tex'
                text = source.read_text(encoding='utf-8')
                self.assertIn(before, text)
                source.write_text(text.replace(before, after), encoding='utf-8')
                self.assertTrue(resume.template_issues(root))

    def test_class_geometry_change_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.prepare(root)
            cls = root / 'resume.cls'
            cls.write_text(cls.read_text(encoding='utf-8').replace('left=0.7in', 'left=0.4in'), encoding='utf-8')
            self.assertTrue(resume.template_issues(root))

    def test_build_does_not_compile_rejected_template(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            out = root / 'output'
            out.mkdir()
            self.prepare(out)
            source = out / 'resume.tex'
            source.write_text(source.read_text(encoding='utf-8').replace('fontset=none', 'fontset=macnew'), encoding='utf-8')
            with patch.object(resume, 'WORKSPACE', root), patch.object(resume, 'compile_at') as compile_at:
                self.assertEqual(resume.build(), 1)
                compile_at.assert_not_called()
            state = json.loads((out / '.work/build.json').read_text(encoding='utf-8'))
            self.assertEqual(state['status'], 'template-rejected')


if __name__ == '__main__':
    unittest.main()




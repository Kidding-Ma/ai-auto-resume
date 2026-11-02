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
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp)):
            problems = resume.inspect_paths(['materials/cv.txt', 'output/resume.pdf', 'workspace/facts.md', 'unknown.txt'])
            self.assertEqual(len(problems), 4)
            self.assertEqual(resume.inspect_paths(['README.md', 'templates/resume.tex']), [])

    def test_init_preserves_personal_draft(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp)):
            root = Path(tmp)
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
            workspace = Path(tmp)
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
            workspace = Path(tmp)
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
            root = Path(tmp)
            (root / 'resume.tex').write_text('broken', encoding='utf-8')
            (root / 'resume.pdf').write_bytes(b'%PDF-previous')
            with patch.object(resume.shutil, 'which', return_value='xelatex'), patch.object(resume.subprocess, 'run') as run:
                run.return_value.returncode = 1
                run.return_value.stdout = b'failed'
                self.assertEqual(resume.compile_at(root), 1)
            self.assertFalse((root / 'resume.pdf').exists())
            self.assertEqual((root / '.previous/resume.pdf').read_bytes(), b'%PDF-previous')

    def test_secret_detection_does_not_echo_secret(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(resume, 'ROOT', Path(tmp)):
            (Path(tmp) / 'README.md').write_text('ghp_' + 'x' * 30, encoding='utf-8')
            result = resume.inspect_paths(['README.md'])
            self.assertEqual(len(result), 1)
            self.assertNotIn('x' * 30, str(result))


if __name__ == '__main__':
    unittest.main()

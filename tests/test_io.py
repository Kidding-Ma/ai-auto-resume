"""Exercise portable material reading and PDF checks with fictional fixtures."""
import importlib.util
from pathlib import Path
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

spec = importlib.util.spec_from_file_location('resume', Path(__file__).resolve().parents[1] / 'scripts/resume.py')
resume = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resume)
try:
    engine = resume.pdf_library()
except ValueError:
    engine = None


class MaterialTest(unittest.TestCase):
    def test_docx_unicode_and_table_order_without_extra_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source = root / '中文 材料.docx'
            body = """<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
              <w:body><w:p><w:r><w:t>姓名：测试人</w:t></w:r></w:p>
              <w:tbl><w:tr><w:tc><w:p><w:r><w:t>项目：算法&#160;😀</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
              <w:p><w:r><w:t>末行：通过六级</w:t></w:r></w:p></w:body></w:document>"""
            with zipfile.ZipFile(source, 'w') as archive:
                archive.writestr('word/document.xml', body)
            result = resume.extract_material(source, root / 'output')
            self.assertEqual(result.read_text(encoding='utf-8').splitlines(),
                             ['姓名：测试人', '项目：算法\u00a0😀', '末行：通过六级'])

    def test_text_encodings_and_multiple_materials_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            first, second = root / 'first.txt', root / 'second.txt'
            first.write_bytes('教育：示例'.encode('utf-8-sig'))
            second.write_bytes('技能：中文'.encode('gb18030'))
            a = resume.extract_material(first, root / 'output')
            b = resume.extract_material(second, root / 'output')
            self.assertNotEqual(a, b)
            self.assertEqual(a.read_text(encoding='utf-8'), '教育：示例')
            self.assertEqual(b.read_text(encoding='utf-8'), '技能：中文')

    def test_empty_docx_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source = root / 'empty.docx'
            with zipfile.ZipFile(source, 'w') as archive:
                archive.writestr('word/document.xml', '<document/>')
            with self.assertRaisesRegex(ValueError, '没有提取到文字'):
                resume.extract_material(source, root / 'output')


@unittest.skipUnless(engine, 'requires PyMuPDF')
class PDFCheckTest(unittest.TestCase):
    def fixture(self, root, *, offset=0, overlap=False):
        name = 'TEST PERSON'
        original = (resume.ROOT / 'templates/resume.tex').read_text(encoding='utf-8')
        header = original[:original.index(r'\section{')]
        header = header.replace(r'\name{林小满}', r'\name{' + name + '}')
        header = header.replace('lin@example.com', '')
        (root / 'resume.tex').write_text(header + r'\section{Test} Fictional content.\end{document}', encoding='utf-8')
        shutil.copyfile(resume.ROOT / 'templates/resume.cls', root / 'resume.cls')
        (root / 'resume.log').write_text('Output written on resume.pdf (1 page)', encoding='utf-8')
        doc = engine.open()
        page = doc.new_page(width=595, height=842)
        x = (595 - engine.get_text_length(name, fontsize=20)) / 2 + offset
        page.insert_text((x, 60), name, fontsize=20)
        page.insert_text((60, 150), 'Fictional content for PDF checks.', fontsize=11)
        if overlap:
            image = engine.Pixmap(engine.csRGB, engine.IRect(0, 0, 10, 10), False).tobytes('png')
            page.insert_image(engine.Rect(x, 35, x + 100, 70), stream=image)
        doc.save(root / 'resume.pdf')
        doc.close()

    def test_valid_pdf_checks_and_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.fixture(root)
            self.assertEqual(resume.check_pdf(root), 0)
            data = json.loads((root / '.work/checks.json').read_text(encoding='utf-8'))
            self.assertTrue(data['passed'])
            self.assertFalse(data['facts_verified'])
            self.assertTrue((root / '.work/page-1.png').is_file())

    def test_off_centre_and_obscured_name_are_rejected(self):
        for options in ({'offset': -40}, {'overlap': True}):
            with self.subTest(options=options), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                self.fixture(root, **options)
                self.assertEqual(resume.check_pdf(root, render=False), 1)
                data = json.loads((root / '.work/checks.json').read_text(encoding='utf-8'))
                self.assertFalse(data['passed'])
                self.assertTrue(data['issues'])

    def test_missing_engine_removes_old_success_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / '.work').mkdir()
            report = root / '.work/checks.json'
            report.write_text('{"passed": true}')
            with patch.object(resume, 'pdf_library', side_effect=ValueError('missing')):
                with self.assertRaises(ValueError):
                    resume.check_pdf(root)
            self.assertFalse(report.exists())

    def test_failed_build_cannot_certify_an_old_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.fixture(root)
            (root / '.work').mkdir()
            (root / '.work/build.json').write_text('{"status":"started","pdf":"resume.pdf","log":"resume.log"}')
            self.assertEqual(resume.check_pdf(root, render=False), 1)
            report = json.loads((root / '.work/checks.json').read_text(encoding='utf-8'))
            self.assertIn('最近一次编译未成功，不能把旧 PDF 当作本次结果', report['issues'])

    def test_changed_source_invalidates_previous_build(self):
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.fixture(root)
            (root / '.work').mkdir()
            state = {'status': 'compiled', 'pdf': 'resume.pdf', 'log': 'resume.log',
                     'source_sha256': hashlib.sha256((root / 'resume.tex').read_bytes()).hexdigest(),
                     'pdf_sha256': hashlib.sha256((root / 'resume.pdf').read_bytes()).hexdigest()}
            (root / '.work/build.json').write_text(json.dumps(state))
            (root / 'resume.tex').write_text(r'\name{TEST PERSON}' + '\n% revised')
            self.assertEqual(resume.check_pdf(root, render=False), 1)


"""Render fictional cases; regress page-centred headers, photos and sparse drafts."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

try:
    import fitz
except ImportError:
    fitz = None

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('xelatex') and fitz, 'requires XeLaTeX and PyMuPDF')
class LayoutTest(unittest.TestCase):
    def test_page_centre_with_without_photo_and_sparse_content(self):
        from PIL import Image
        for photo in (None, 'photo.jpg', 'photo.png'):
            with self.subTest(photo=photo), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp).resolve()
                shutil.copyfile(ROOT / 'templates/resume.cls', target / 'resume.cls')
                source = (ROOT / 'templates/resume.tex').read_text(encoding='utf-8')
                # Use the fixed header; only replace the public body with sparse facts.
                source = source[:source.index(r'\section{')] + r"""
\section{教育经历}
\datedsubsection{示例大学，计算机，本科}{2022 -- 2026}
\section{课程实践}
完成课程作业中的查询页面，支持按名称检索记录。
\section{竞赛荣誉}
\textbf{金奖}｜示例课程竞赛｜2025
\section{技能}
使用 Python 处理文本文件。
\end{document}
"""
                (target / 'resume.tex').write_text(source, encoding='utf-8')
                if photo:
                    Image.new('RGB', (220, 280), '#91a7bb').save(target / photo)
                for _ in range(2):
                    run = subprocess.run(['xelatex', '-no-shell-escape', '-interaction=nonstopmode',
                                          '-halt-on-error', 'resume.tex'],
                                         cwd=target, capture_output=True, timeout=120)
                    self.assertEqual(run.returncode, 0, run.stdout.decode(errors='replace')[-2000:])
                log = (target / 'resume.log').read_text(encoding='utf-8', errors='replace')
                self.assertNotRegex(log, r'Overfull \\[hv]box|Missing character:')
                with fitz.open(target / 'resume.pdf') as pdf:
                    self.assertEqual(len(pdf), 1)
                    page = pdf[0]
                    names = page.search_for('林小满')
                    self.assertEqual(len(names), 1)
                    name = names[0]
                    self.assertAlmostEqual((name.x0 + name.x1) / 2, page.rect.width / 2, delta=1)
                    self.assertEqual(len(page.get_images()), int(photo is not None))
                    self.assertIn('金奖', page.get_text())
                    self.assertNotIn('个人概述', page.get_text())
                    if photo:
                        rect = page.get_image_rects(page.get_images()[0][0])[0]
                        self.assertFalse(rect.intersects(name))
                        heading = page.search_for('教育经历')[0]
                        self.assertGreater(heading.y0, rect.y1)



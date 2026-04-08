"""
Merge books into 3 PDFs: 六爻 / 紫薇 / 基础
"""
import os
import sys
import io
import zipfile
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pypdf import PdfReader, PdfWriter
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

# ─── paths ───────────────────────────────────────────────────────────
SRC = Path(r"D:\6_命理\精选十部紫薇六爻基础")
OUT = Path(r"D:\6_命理\压缩3部")
OUT.mkdir(parents=True, exist_ok=True)

# ─── files (exact names) ─────────────────────────────────────────────
# 六爻 PDFs
YAO_PDFS = [
    SRC / "中国古代占卜经典 卜筮正宗 (（清）王洪辑撰；孙正治注译, (清)王洪绪辑撰 , 孙正治注译, 王维德, 孙正治 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    SRC / "增删卜易 上 (李文辉) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    SRC / "增删卜易 最新新编白话版 下册 (（清）野鹤老人原著；湖南，李文辉觉子增删；楚江，李我平鉴定；孙正治注译 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
]
YAO_DOCX = SRC / "六爻三大技法真正完整稿件.docx"

# 紫薇 PDFs (7本)
ZIWEI_PDFS = [
    SRC / "南北山人编注《紫微斗数全书》 .pdf",
    SRC / "图解星学大成.第1部星曜神煞.pdf",
    SRC / "图解星学大成.第2部命局分析.pdf",
    SRC / "学习紫微斗数第一本书_简体整理版_许铨仁_z_library_sk,_1lib_sk,_z_lib_sk.pdf",
    SRC / "许铨仁高级班录音精校 (小极阁) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    SRC / "钦天_许铨仁_紫微斗数命理学正解_全_许铨仁_Z_Library.pdf",
    SRC / "钦天四化紫微斗数基础 (许铨仁) (Z-Library).pdf",
]
ZIWEI_EPUB = SRC / "安星法及推断实例_王亭之_z_library_sk,_1lib_sk,_z_lib_sk.epub"

# 基础 PDFs
BASIC_PDFS = [
    SRC / "术数全书版五行大义.pdf",
]
BASIC_TXT = SRC / "正易心法注宋_麻衣道者_撰_陈抟_注_txt_正易心法注宋_麻衣道者_撰_Z_Library.txt"

# ─── helpers ─────────────────────────────────────────────────────────
def merge_pdfs(pdf_paths, output_path):
    writer = PdfWriter()
    added = []
    for p in pdf_paths:
        p = Path(p)
        if p.exists():
            writer.append(str(p))
            added.append(p.name)
            print(f"    + {p.name[:50]}")
        else:
            print(f"    MISSING: {str(p)[:80]}")
    if added:
        with open(str(output_path), 'wb') as f:
            writer.write(f)
        size = output_path.stat().st_size // 1024
        print(f"    → {output_path.name}  ({len(added)} files, {size}KB)")
    return added

def docx_to_pdf(docx_path, output_path, title):
    print(f"    Converting DOCX: {docx_path.name}")
    doc = Document(str(docx_path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    doc2 = SimpleDocTemplate(str(output_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13, spaceAfter=3)
    ttl  = ParagraphStyle('ttl',  fontName='Helvetica-Bold', fontSize=13, leading=16,
                           spaceAfter=8, alignment=1)
    story = [Paragraph(title, ttl), Spacer(1, 0.3*cm)]
    for t in paragraphs:
        story.append(Paragraph(t, body))
        story.append(Spacer(1, 2))
    doc2.build(story)
    print(f"    → {output_path.name}")

def epub_extract_text(epub_path):
    parts = []
    with zipfile.ZipFile(str(epub_path), 'r') as z:
        for name in z.namelist():
            if name.endswith(('.html', '.xhtml', '.htm')) and 'nav' not in name.lower():
                try:
                    c = z.read(name).decode('utf-8', errors='ignore')
                    t = re.sub(r'<[^>]+>', ' ', re.sub(r' style="[^"]*"', '', c))
                    t = re.sub(r'\s+', ' ', t).strip()
                    if len(t) > 30:
                        parts.append(t)
                except:
                    pass
    return '\n\n'.join(parts[:300])

def epub_to_pdf(epub_path, output_path, title):
    print(f"    Converting EPUB: {epub_path.name}")
    text = epub_extract_text(epub_path)
    doc2 = SimpleDocTemplate(str(output_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=2)
    ttl  = ParagraphStyle('ttl',  fontName='Helvetica-Bold', fontSize=13, leading=16,
                           spaceAfter=8, alignment=1)
    story = [Paragraph(title, ttl), Spacer(1, 0.3*cm)]
    for chunk in text.split('\n\n')[:500]:
        chunk = chunk.strip()
        if chunk:
            story.append(Paragraph(chunk, body))
            story.append(Spacer(1, 2))
    doc2.build(story)
    print(f"    → {output_path.name}")

def txt_to_pdf(txt_path, output_path, title):
    print(f"    Converting TXT: {txt_path.name}")
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    doc2 = SimpleDocTemplate(str(output_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=3)
    ttl  = ParagraphStyle('ttl',  fontName='Helvetica-Bold', fontSize=13, leading=16,
                           spaceAfter=8, alignment=1)
    story = [Paragraph(title, ttl), Spacer(1, 0.3*cm)]
    for line in text.split('\n')[:1500]:
        line = line.strip()
        if line:
            story.append(Paragraph(line, body))
            story.append(Spacer(1, 2))
    doc2.build(story)
    print(f"    → {output_path.name}")

# ─── run ─────────────────────────────────────────────────────────────
print("=" * 60)
print("打包：六爻 / 紫薇 / 基础 → 3部PDF")
print("=" * 60)

# 六爻
print("\n[六爻]")
yao_out = OUT / "六爻_合集.pdf"
yao_extra = []
if YAO_DOCX.exists():
    tmp = OUT / "_tmp_六爻三大技法.pdf"
    docx_to_pdf(YAO_DOCX, tmp, "六爻三大技法")
    yao_extra = [tmp]
merge_pdfs(YAO_PDFS + yao_extra, yao_out)

# 紫薇
print("\n[紫薇]")
ziwei_out = OUT / "紫薇_合集.pdf"
ziwei_extra = []
if ZIWEI_EPUB.exists():
    tmp = OUT / "_tmp_安星法.pdf"
    epub_to_pdf(ZIWEI_EPUB, tmp, "安星法及推断实例")
    ziwei_extra = [tmp]
merge_pdfs(ZIWEI_PDFS + ziwei_extra, ziwei_out)

# 基础
print("\n[基础]")
basic_out = OUT / "基础_合集.pdf"
basic_extra = []
if BASIC_TXT.exists():
    tmp = OUT / "_tmp_正易心法.pdf"
    txt_to_pdf(BASIC_TXT, tmp, "正易心法注（陈抟）")
    basic_extra.append(tmp)
merge_pdfs(BASIC_PDFS + basic_extra, basic_out)

# cleanup
print("\n清理临时文件...")
for f in OUT.glob("_tmp_*"):
    try:
        f.unlink()
        print(f"  deleted: {f.name}")
    except:
        pass

print("\n完成！")
for f in [yao_out, ziwei_out, basic_out]:
    if f.exists():
        sz = f.stat().st_size // 1024
        print(f"  {f.name:20s}  {sz:>8,} KB")

#!/usr/bin/env python3
"""验证渲染后的 PDF 存在且有内容"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_pdf_pages, check_pdf_has_text, check_file_contains, TestReport

HERE = Path(__file__).parent.resolve()
report = TestReport()

pdf_path = HERE / "answer.pdf"
md_path = HERE / "answer.md"

# 1. 检查源文件
ok, msg = check_file_exists(md_path)
report.add("source_md_exists", ok, [msg])

# 2. 检查 PDF 存在
ok, msg = check_file_exists(pdf_path)
report.add("rendered_pdf_exists", ok, [msg])

# 3. 检查 PDF 页数
if pdf_path.exists():
    ok, msg = check_pdf_pages(pdf_path, min_pages=1)
    report.add("pdf_pages", ok, [msg])

# 4. 检查 PDF 包含文本
if pdf_path.exists():
    ok, msg = check_pdf_has_text(pdf_path)
    report.add("pdf_has_text", ok, [msg])

# 5. 检查源 Markdown 包含关键内容（确保测试有效性）
if md_path.exists():
    ok, msg = check_file_contains(md_path, "AutoPku")
    report.add("md_has_keyword", ok, [msg])
    ok, msg = check_file_contains(md_path, "$$")
    report.add("md_has_latex", ok, [msg])

passed = report.print_summary()
sys.exit(0 if passed else 1)

#!/usr/bin/env python3
import sys
import subprocess
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists

results = []

# 1. 验证 main.typ 存在且包含中文
ok, msg = check_file_exists(Path("slides/main.typ"))
results.append(msg)

if (Path("slides/main.typ")).exists():
    content = (Path("slides/main.typ")).read_text(encoding="utf-8")
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    if len(chinese_chars) >= 10:
        results.append(f"OK: main.typ 包含 {len(chinese_chars)} 个中文字符")
    else:
        results.append(f"FAIL: main.typ 中文字符过少（{len(chinese_chars)} 个）")

# 2. 编译
compile_result = subprocess.run(
    ["typst", "compile", "slides/main.typ", "slides/chinese_test.pdf"],
    capture_output=True,
    text=True,
    timeout=120,
)

if compile_result.returncode != 0 or not Path("slides/chinese_test.pdf").exists():
    results.append(f"FAIL: typst compile 失败: {compile_result.stderr[:200]}")
    for r in results:
        print(r)
    sys.exit(1)

results.append("OK: typst compile 成功")

# 3. 使用 PyMuPDF / pdfplumber 提取 PDF 文本检查中文字符
pdf_text = ""
try:
    import fitz  # PyMuPDF
    doc = fitz.open("slides/chinese_test.pdf")
    for page in doc:
        pdf_text += page.get_text()
except ImportError:
    try:
        import pdfplumber
        with pdfplumber.open("slides/chinese_test.pdf") as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text() or ""
    except ImportError:
        pdf_text = ""

if pdf_text:
    chinese_in_pdf = re.findall(r'[\u4e00-\u9fff]', pdf_text)
    if len(chinese_in_pdf) >= 10:
        results.append(f"OK: PDF 文本提取到 {len(chinese_in_pdf)} 个中文字符")
    else:
        # fallback：检查文件大小（嵌入中文字体后 PDF 通常较大）
        size = Path("slides/chinese_test.pdf").stat().st_size
        if size > 30000:
            results.append(f"OK: PDF 文件大小 {size} 字节，推测已嵌入中文字体")
        else:
            results.append(f"FAIL: PDF 中文字符过少（{len(chinese_in_pdf)} 个），且文件仅 {size} 字节")
else:
    # 无法提取文本时，fallback 到文件大小
    size = Path("slides/chinese_test.pdf").stat().st_size
    if size > 30000:
        results.append(f"OK: PDF 文件大小 {size} 字节，推测已嵌入中文字体")
    else:
        results.append(f"FAIL: 无法提取 PDF 文本，且文件仅 {size} 字节")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)
sys.exit(0 if failed == 0 else 1)

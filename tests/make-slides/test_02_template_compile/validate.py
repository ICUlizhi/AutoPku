#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_pdf_pages, check_pdf_has_text

results = []

# 1. 验证模板已通过 git clone 获取到缓存目录
template_dir = Path.home() / ".autopku/templates/touying-ethan"
ok, msg = check_file_exists(template_dir / ".git" / "config", msg="模板未通过 git clone 获取")
results.append(msg)

# 检查关键模板文件存在
for f in ["style/index.typ", "slides/index.typ", "figures/background.png"]:
    ok, msg = check_file_exists(template_dir / f, msg=f"模板文件 {f} 缺失")
    results.append(msg)

# 2. 验证 slides/main.typ 存在
ok, msg = check_file_exists(Path("slides/main.typ"))
results.append(msg)

# 3. 验证 main.typ 语法合法（typst compile 成功）
compile_result = subprocess.run(
    ["typst", "compile", "slides/main.typ", "slides/test_output.pdf"],
    capture_output=True,
    text=True,
    timeout=120,
)

if compile_result.returncode == 0 and Path("slides/test_output.pdf").exists():
    results.append("OK: typst compile 成功生成 PDF")

    # 4. 验证 PDF 页数
    try:
        import fitz
        doc = fitz.open("slides/test_output.pdf")
        pages = len(doc)
        if pages >= 1:
            results.append(f"OK: PDF {pages} 页")
        else:
            results.append(f"FAIL: PDF 页数 {pages} < 1")
    except Exception as e:
        ok, msg = check_pdf_pages(Path("slides/test_output.pdf"), min_pages=1)
        results.append(msg)

    # 5. 验证 PDF 包含实际文本
    ok, msg = check_pdf_has_text(Path("slides/test_output.pdf"))
    results.append(msg)
else:
    results.append(f"FAIL: typst compile 失败: {compile_result.stderr[:200]}")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)
sys.exit(0 if failed == 0 else 1)

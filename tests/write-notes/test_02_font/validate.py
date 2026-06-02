#!/usr/bin/env python3
"""
test_02_font 验证脚本
验证 PDF 渲染时使用正确的中文字体，中文内容不丢失
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists


def main():
    pdf_path = Path("output/note.pdf")

    # 1. 检查 PDF 是否存在
    ok, msg = check_file_exists(pdf_path)
    print(msg)
    if not ok:
        print("INFO: 请先执行 run.sh 中的步骤生成 PDF")
        return 1

    # 2. 使用 strings 提取 PDF 文本内容
    result = subprocess.run(
        ["strings", str(pdf_path)],
        capture_output=True, text=True, timeout=10
    )
    text = result.stdout

    # 3. 检查常见中文字符是否被正确嵌入
    chinese_chars = ["命题", "逻辑", "定理", "完备性", "真值", "联结词"]
    found = 0
    for char in chinese_chars:
        if char in text:
            found += 1
            print(f"OK: PDF 中包含 '{char}'")
        else:
            print(f"FAIL: PDF 中未找到 '{char}'")

    if found >= 3:
        print("OK: test_02_font 通过")
        return 0
    else:
        print(f"FAIL: 中文字体检出率过低 ({found}/{len(chinese_chars)})")
        return 1


if __name__ == "__main__":
    sys.exit(main())

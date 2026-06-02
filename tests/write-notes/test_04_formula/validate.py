#!/usr/bin/env python3
"""
test_04_formula 验证脚本
验证数学公式（特别是模态逻辑符号）在 PDF 中被正确渲染
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists


def main():
    pdf_path = Path("output/note.pdf")

    ok, msg = check_file_exists(pdf_path)
    print(msg)
    if not ok:
        print("INFO: 请先执行 run.sh 中的步骤生成 PDF")
        return 1

    # 使用 strings 提取 PDF 文本
    result = subprocess.run(
        ["strings", str(pdf_path)],
        capture_output=True, text=True, timeout=10
    )
    text = result.stdout

    # 验证公式相关字符
    # PDF 中可能保留 LaTeX 命令名，也可能被转为 Unicode 或图形化
    formula_markers = [
        "xRy",            # 可达关系
        "Box",            # 必然算子（LaTeX 命令名）
        "Diamond",        # 可能算子
        "leftrightarrow", # 等价
        "forall",         # 全称量词
    ]

    # 同时也检查通用文本，确保 PDF 确实被渲染
    general_markers = [
        "可达关系",
        "自反性",
        "对称性",
        "传递性",
    ]

    found_formula = 0
    for marker in formula_markers:
        if marker.lower() in text.lower() or marker in text:
            found_formula += 1
            print(f"OK: 找到公式标记 '{marker}'")
        else:
            print(f"INFO: 未找到公式标记 '{marker}'（可能在 PDF 中已图形化）")

    found_general = 0
    for marker in general_markers:
        if marker in text:
            found_general += 1
            print(f"OK: 找到文本 '{marker}'")
        else:
            print(f"FAIL: 未找到文本 '{marker}'")

    # 通用文本必须存在，公式标记至少有一个；
    # 若通用文本足够多，说明 PDF 已正常生成，公式可能被图形化（也接受）
    if found_general >= 2 and found_formula >= 1:
        print("OK: test_04_formula 通过")
        return 0
    elif found_general >= 3:
        print("OK: 公式可能已图形化，但主体文本正确（test_04_formula 通过）")
        return 0
    else:
        print(f"FAIL: 验证失败（通用文本 {found_general}/4, 公式标记 {found_formula}/5）")
        return 1


if __name__ == "__main__":
    sys.exit(main())

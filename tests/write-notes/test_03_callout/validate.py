#!/usr/bin/env python3
"""
test_03_callout 验证脚本
验证 callout 的正文内容（不仅是标题）被完整包含在最终输出中
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists


def main():
    # 支持 PDF 或 Markdown 输出
    output_paths = [
        Path("output/note.pdf"),
        Path("output/note.md"),
        Path("notes/note.md"),
    ]
    output_path = None
    for p in output_paths:
        if p.exists():
            output_path = p
            break

    if not output_path:
        print("FAIL: 未找到输出文件（请先执行 run.sh 步骤）")
        return 1

    print(f"OK: 找到输出文件 {output_path}")

    # 读取内容
    if output_path.suffix == ".pdf":
        result = subprocess.run(
            ["strings", str(output_path)],
            capture_output=True, text=True, timeout=10
        )
        content = result.stdout
    else:
        content = output_path.read_text(encoding="utf-8")

    # 验证 callout 正文内容被包含（这些是容易丢失的折叠/展开内容）
    callout_bodies = [
        "不可区分关系",
        "前后关系",
        "框架 (frame) 是一个二元组",
        "非空的可能世界集合",
        "赋值函数得到的结构",
    ]

    found = 0
    for text in callout_bodies:
        if text in content:
            found += 1
            print(f"OK: 包含 callout 正文 '{text}'")
        else:
            print(f"FAIL: 未找到 callout 正文 '{text}'")

    if found >= 3:
        print("OK: test_03_callout 通过")
        return 0
    else:
        print(f"FAIL: callout 内容包含率过低 ({found}/{len(callout_bodies)})")
        return 1


if __name__ == "__main__":
    sys.exit(main())

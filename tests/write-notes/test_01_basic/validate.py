#!/usr/bin/env python3
"""
test_01_basic 验证脚本
验证 PDF 课件 → 笔记基础流程
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_dir_structure, check_file_contains


def main():
    notes_dir = Path("notes")

    # 1. 检查 notes/ 目录下存在 .md 文件
    ok, details = check_dir_structure(notes_dir, ["*.md"])
    for d in details:
        print(d)
    if not ok:
        print("FAIL: notes/ 目录下未找到 .md 笔记文件（请先执行 run.sh）")
        return 1

    # 2. 验证笔记内容包含核心知识点
    md_files = list(notes_dir.glob("*.md"))
    note_file = md_files[0]
    print(f"OK: 找到笔记文件 {note_file}")

    ok, msg = check_file_contains(note_file, "定义", min_occurrences=1)
    print(msg)
    if not ok:
        return 1

    ok, msg = check_file_contains(note_file, "定理", min_occurrences=1)
    print(msg)
    if not ok:
        return 1

    print("OK: test_01_basic 通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

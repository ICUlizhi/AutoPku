#!/usr/bin/env python3
"""
test_05_idempotent 验证脚本
验证多次执行渲染不会导致内容重复（检查唯一标记只出现一次）
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists


def main():
    # 检查可能的输出位置
    output_candidates = [
        Path("output/note.pdf"),
        Path("output/note_v1.pdf"),
        Path("output/note_v2.pdf"),
        Path("notes/note.md"),
        Path("notes/逻辑导论完整笔记.md"),
    ]

    output_path = None
    for p in output_candidates:
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

    # 验证唯一标记不重复出现
    markers = [
        "UNIQUE_MARKER_7A3F9E2D_第一讲结束",
        "UNIQUE_MARKER_7A3F9E2D_第二讲结束",
        "UNIQUE_MARKER_7A3F9E2D_第三讲结束",
    ]

    all_ok = True
    for marker in markers:
        count = content.count(marker)
        if count == 1:
            print(f"OK: 标记 '{marker}' 出现 1 次（未重复）")
        elif count == 0:
            print(f"FAIL: 标记 '{marker}' 未找到")
            all_ok = False
        else:
            print(f"FAIL: 标记 '{marker}' 出现 {count} 次（可能重复渲染！）")
            all_ok = False

    if all_ok:
        print("OK: test_05_idempotent 通过")
        return 0
    else:
        print("FAIL: 检测到重复渲染或内容丢失")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_dir_structure, check_file_contains

base = Path("test00/太极拳")
results = []

ok, msgs = check_dir_structure(base, ["作业", "通知", "资料", "通知摘要.md"])
results.extend(msgs)

if (base / "通知摘要.md").exists():
    ok, msg = check_file_contains(base / "通知摘要.md", "太极拳"); results.append(msg)
    # 验证空数据提示（支持多种常见表述）
    content = (base / "通知摘要.md").read_text(encoding="utf-8")
    empty_markers = ["无新通知", "暂无通知", "无通知", "没有新通知", "无待交"]
    if any(m in content for m in empty_markers):
        results.append("OK: 摘要中包含空数据提示")
    else:
        results.append("FAIL: 摘要中未找到空数据提示")
else:
    results.append("FAIL: 通知摘要.md 不存在")

if (base / "通知摘要.md").exists():
    content = (base / "通知摘要.md").read_text(encoding="utf-8")
    if "\x1b[" in content:
        results.append("FAIL: ANSI 颜色码残留")
    else:
        results.append("OK: 无 ANSI 残留")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results: print(r)
sys.exit(0 if failed == 0 else 1)

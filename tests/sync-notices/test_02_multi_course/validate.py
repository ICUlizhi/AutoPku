#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_dir_structure, check_file_contains

results = []

# 验证逻辑导论
base_logic = Path("test00/逻辑导论")
ok, msgs = check_dir_structure(base_logic, ["作业", "通知", "资料", "通知摘要.md"])
results.extend(msgs)

if (base_logic / "通知摘要.md").exists():
    ok, msg = check_file_contains(base_logic / "通知摘要.md", "逻辑导论"); results.append(msg)
    ok, msg = check_file_contains(base_logic / "通知摘要.md", "待交"); results.append(msg)
else:
    results.append("FAIL: 逻辑导论/通知摘要.md 不存在")

# 验证哲学导论
base_philo = Path("test00/哲学导论")
ok, msgs = check_dir_structure(base_philo, ["作业", "通知", "资料", "通知摘要.md"])
results.extend(msgs)

if (base_philo / "通知摘要.md").exists():
    ok, msg = check_file_contains(base_philo / "通知摘要.md", "哲学导论"); results.append(msg)
    ok, msg = check_file_contains(base_philo / "通知摘要.md", "待交"); results.append(msg)
else:
    results.append("FAIL: 哲学导论/通知摘要.md 不存在")

# 验证无 ANSI 残留
for course in ["逻辑导论", "哲学导论"]:
    summary = Path(f"test00/{course}/通知摘要.md")
    if summary.exists():
        content = summary.read_text(encoding="utf-8")
        if "\x1b[" in content:
            results.append(f"FAIL: {course}/通知摘要.md 存在 ANSI 颜色码残留")
        else:
            results.append(f"OK: {course}/通知摘要.md 无 ANSI 残留")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results: print(r)
sys.exit(0 if failed == 0 else 1)

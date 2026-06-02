#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_dir_structure, check_file_exists

base = Path("test00/逻辑导论/slides")
results = []

# 1. 验证 slides/ 目录结构
ok, msgs = check_dir_structure(base, ["main.typ", "outline.md", "figures"])
results.extend(msgs)

# 2. 验证 main.typ 存在且非空
ok, msg = check_file_exists(base / "main.typ")
results.append(msg)
if (base / "main.typ").exists():
    size = (base / "main.typ").stat().st_size
    if size > 0:
        results.append(f"OK: main.typ 大小 {size} 字节")
    else:
        results.append("FAIL: main.typ 为空文件")

# 3. 验证 outline.md 存在且非空
ok, msg = check_file_exists(base / "outline.md")
results.append(msg)
if (base / "outline.md").exists():
    size = (base / "outline.md").stat().st_size
    if size > 0:
        results.append(f"OK: outline.md 大小 {size} 字节")
    else:
        results.append("FAIL: outline.md 为空文件")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)
sys.exit(0 if failed == 0 else 1)

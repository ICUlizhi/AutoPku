#!/usr/bin/env python3
"""验证提交前确认流程文档完整"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_file_contains, TestReport

HERE = Path(__file__).parent.resolve()
report = TestReport()

# 1. README.md 必须存在且包含关键流程描述
readme_path = HERE / "README.md"
ok, msg = check_file_exists(readme_path)
report.add("readme_exists", ok, [msg])

if ok:
    checks = []
    all_ok = True
    for keyword in ["AskUserQuestion", "提交", "save_only", "二次确认"]:
        k_ok, k_msg = check_file_contains(readme_path, keyword)
        checks.append(k_msg)
        if not k_ok:
            all_ok = False
    report.add("readme_has_confirm_flow", all_ok, checks)

# 2. run.sh 必须存在且描述了确认步骤
runsh_path = HERE / "run.sh"
ok, msg = check_file_exists(runsh_path)
report.add("runsh_exists", ok, [msg])

if ok:
    checks = []
    all_ok = True
    for keyword in ["AskUserQuestion", "submit", "save_only"]:
        k_ok, k_msg = check_file_contains(runsh_path, keyword)
        checks.append(k_msg)
        if not k_ok:
            all_ok = False
    report.add("runsh_has_confirm_steps", all_ok, checks)

# 3. 检查是否有任何"严禁自动提交"或类似安全提示
if readme_path.exists():
    ok, msg = check_file_contains(readme_path, "严禁")
    if not ok:
        ok2, msg2 = check_file_contains(readme_path, "不得")
        if ok2:
            ok, msg = ok2, msg2
    report.add("readme_has_safety_warning", ok, [msg if ok else f"INFO: {msg}（建议添加安全警告）"])

passed = report.print_summary()
sys.exit(0 if passed else 1)

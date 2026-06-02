#!/usr/bin/env python3
"""验证 PDF 解析产物结构正确"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_dir_structure, TestReport

HERE = Path(__file__).parent.resolve()
report = TestReport()

# 1. 检查输入文件
pdf_path = HERE / "homework_mock.pdf"
ok, msg = check_file_exists(pdf_path, "(mock PDF)")
report.add("mock_pdf_exists", ok, [msg])

# 若 PDF 是占位文件（reportlab 未安装），跳过解析验证，仅做结构检查
is_placeholder = pdf_path.exists() and pdf_path.read_text(errors="ignore").startswith("# Mock PDF placeholder")

# 2. 检查 homework_parsed.json
parsed_path = HERE / "homework_parsed.json"
ok, msg = check_file_exists(parsed_path)
if ok:
    try:
        data = json.loads(parsed_path.read_text(encoding="utf-8"))
        checks = []
        if "pages" in data and isinstance(data["pages"], list):
            checks.append(f"OK: pages 字段存在，共 {len(data['pages'])} 页")
        else:
            checks.append("FAIL: pages 字段缺失或类型错误")
            ok = False
        if "problems" in data and isinstance(data["problems"], list) and len(data["problems"]) >= 1:
            checks.append(f"OK: problems 字段存在，共 {len(data['problems'])} 题")
        else:
            checks.append("FAIL: problems 字段缺失、类型错误或为空")
            ok = False
        report.add("homework_parsed_structure", ok, checks)
    except Exception as e:
        report.add("homework_parsed_structure", False, [f"FAIL: JSON 解析错误: {e}"])
else:
    report.add("homework_parsed_structure", False, [msg])

# 3. 检查 answers.json
answers_path = HERE / "answers.json"
ok, msg = check_file_exists(answers_path)
if ok:
    try:
        data = json.loads(answers_path.read_text(encoding="utf-8"))
        checks = []
        answers = data.get("answers", [])
        if isinstance(answers, list) and len(answers) >= 1:
            checks.append(f"OK: answers 列表存在，共 {len(answers)} 条")
            # 检查每个 answer 是否有 number 和 content
            all_have_fields = all("number" in a and "content" in a for a in answers)
            if all_have_fields:
                checks.append("OK: 每条 answer 均包含 number 和 content")
            else:
                checks.append("FAIL: 部分 answer 缺少 number 或 content")
                ok = False
        else:
            checks.append("FAIL: answers 字段缺失或为空")
            ok = False
        report.add("answers_structure", ok, checks)
    except Exception as e:
        report.add("answers_structure", False, [f"FAIL: JSON 解析错误: {e}"])
else:
    report.add("answers_structure", False, [msg])

# 汇总
passed = report.print_summary()
sys.exit(0 if passed else 1)

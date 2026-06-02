#!/usr/bin/env python3
"""验证字数统计结果正确"""
import sys
import json
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, TestReport

HERE = Path(__file__).parent.resolve()
report = TestReport()

# 1. 检查输入文件
essay_path = HERE / "essay.md"
ok, msg = check_file_exists(essay_path)
report.add("essay_md_exists", ok, [msg])

# 2. 重新计算参考字数（仅中文字符）
if ok:
    text = essay_path.read_text(encoding="utf-8")
    ref_chinese = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    report.add("reference_wordcount", True, [f"OK: 参考中文字符数 = {ref_chinese}"])
else:
    ref_chinese = None

# 3. 检查 AI 生成的统计结果
result_path = HERE / "wordcount_result.json"
ok, msg = check_file_exists(result_path)
if ok:
    try:
        data = json.loads(result_path.read_text(encoding="utf-8"))
        checks = []
        ai_count = data.get("chinese_chars")
        if ai_count is None:
            checks.append("FAIL: wordcount_result.json 中缺少 chinese_chars 字段")
            ok = False
        elif ref_chinese is not None and ai_count == ref_chinese:
            checks.append(f"OK: chinese_chars = {ai_count}，与参考值一致")
        else:
            checks.append(f"FAIL: chinese_chars = {ai_count}，参考值 = {ref_chinese}")
            ok = False
        report.add("wordcount_result", ok, checks)
    except Exception as e:
        report.add("wordcount_result", False, [f"FAIL: 解析 wordcount_result.json 出错: {e}"])
else:
    report.add("wordcount_result", False, [msg])

# 4. 额外验证：统计代码本身逻辑正确（验证过滤标点和空格）
if ref_chinese is not None:
    # 用 re 提取所有中文字符
    re_count = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 用 str.split 统计 "词" 是不准确的，应检查是否仅统计了中文字符
    naive_word_count = len(text.split())  # 按空格分词，对中文无意义
    report.add("stat_logic_sanity", True, [
        f"OK: re.findall 中文字符数 = {re_count}",
        f"INFO: 按空格 naive split 词数 = {naive_word_count}（对中文不准确，应被排除）"
    ])

passed = report.print_summary()
sys.exit(0 if passed else 1)

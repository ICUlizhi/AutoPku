#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_file_contains

paper_tex = Path("test00/学术英语写作/论文/paper.tex")
template_tex = Path("test00/学术英语写作/论文/template.tex")
results = []

# 1. 模板文件存在（来源检查）
ok, msg = check_file_exists(template_tex)
results.append(msg)

# 2. paper.tex 存在
ok, msg = check_file_exists(paper_tex)
results.append(msg)

if paper_tex.exists():
    content = paper_tex.read_text(encoding="utf-8")

    # 3. 所有占位符已被替换（无残留）
    placeholders = [
        "在此填写题目",
        "在此填写页眉（可以是论文题目）",
        "在此填写姓名",
        "在此填写学号",
        "在此填写院系",
        "在此填写摘要内容",
    ]
    all_replaced = True
    for ph in placeholders:
        if ph in content:
            results.append(f"FAIL: 占位符 '{ph}' 未被替换")
            all_replaced = False
    if all_replaced:
        results.append("OK: 所有占位符均已替换")

    # 4. 实际值正确填入
    expected_values = {
        "A Comparative Study of Sino-Western Business Etiquette": "论文题目",
        "徐靖": "学生姓名",
        "2000012345": "学号",
        "光华管理学院": "院系",
        "This paper compares": "摘要内容",
    }
    for value, label in expected_values.items():
        if value in content:
            results.append(f"OK: {label} 已正确填入")
        else:
            results.append(f"FAIL: {label} 未正确填入（期望包含 '{value}'）")

    # 5. 模板结构完整
    structure_items = [
        ("\\documentclass", "文档类声明"),
        ("\\begin{document}", "document 开始"),
        ("\\end{document}", "document 结束"),
        ("\\section", "正文章节"),
    ]
    for cmd, desc in structure_items:
        if cmd in content:
            results.append(f"OK: {desc} 存在")
        else:
            results.append(f"FAIL: {desc} 缺失")

    # 6. 模板与生成文件对比：确认占位符确实被替换而非原样复制
    if template_tex.exists():
        template_content = template_tex.read_text(encoding="utf-8")
        template_ph_count = sum(1 for ph in placeholders if ph in template_content)
        paper_ph_count = sum(1 for ph in placeholders if ph in content)
        results.append(
            f"OK: 模板含 {template_ph_count} 个占位符，paper.tex 含 {paper_ph_count} 个占位符"
        )

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)

sys.exit(0 if failed == 0 else 1)

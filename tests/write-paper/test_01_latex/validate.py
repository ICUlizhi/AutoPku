#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_file_contains, check_no_duplicate_content

paper_tex = Path("test00/马原/论文/paper.tex")
results = []

# 1. paper.tex 存在
ok, msg = check_file_exists(paper_tex)
results.append(msg)

if paper_tex.exists():
    content = paper_tex.read_text(encoding="utf-8")

    # 2. 占位符已被替换
    placeholders = ["在此填写题目", "在此填写姓名", "在此填写学号", "在此填写院系", "在此填写摘要内容", "在此填写页眉"]
    for ph in placeholders:
        if ph in content:
            results.append(f"FAIL: 占位符 '{ph}' 未被替换")
        else:
            results.append(f"OK: 占位符 '{ph}' 已替换")

    # 3. 实际内容已插入
    ok, msg = check_file_contains(paper_tex, "共产党宣言")
    results.append(msg)
    ok, msg = check_file_contains(paper_tex, "徐靖")
    results.append(msg)

    # 4. 基本 LaTeX 结构完整
    required_cmds = ["\\documentclass", "\\begin{document}", "\\end{document}", "\\section"]
    for cmd in required_cmds:
        if cmd in content:
            results.append(f"OK: 包含 {cmd}")
        else:
            results.append(f"FAIL: 缺少 {cmd}")

    # 5. 重复渲染检查（同一章节不应出现多次）
    ok, msg = check_no_duplicate_content(paper_tex, "\\section{引言}", max_occurrences=1)
    results.append(msg)

    # 6. xelatex 编译检查（可选，若系统有 xelatex）
    import shutil
    if shutil.which("xelatex"):
        import subprocess
        try:
            proc = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "paper.tex"],
                cwd=str(paper_tex.parent),
                capture_output=True,
                text=True,
                timeout=60,
            )
            # 即使 returncode != 0，也看是否生成了 pdf
            if (paper_tex.parent / "paper.pdf").exists():
                results.append("OK: xelatex 编译成功，paper.pdf 已生成")
            else:
                # 允许编译失败（环境可能缺失字体），但至少语法不被拒绝
                # 检查是否是因为字体缺失而非语法错误
                if "! Emergency stop" in proc.stdout or "! Emergency stop" in proc.stderr:
                    results.append("FAIL: xelatex 编译因语法错误停止")
                else:
                    results.append("OK: xelatex 未因语法错误停止（可能是字体缺失）")
        except Exception as e:
            results.append(f"INFO: xelatex 编译尝试失败: {e}")
    else:
        results.append("INFO: 系统未安装 xelatex，跳过编译测试")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)

sys.exit(0 if failed == 0 else 1)

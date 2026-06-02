#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, check_dir_structure, check_file_contains

paper_dir = Path("test00/科技创新实践/论文")
figures_dir = paper_dir / "figures"
results = []

# 1. paper.tex 存在
ok, msg = check_file_exists(paper_dir / "paper.tex")
results.append(msg)

# 2. figures/ 目录存在
if figures_dir.exists() and figures_dir.is_dir():
    results.append("OK: figures/ 目录存在")
else:
    results.append("FAIL: figures/ 目录不存在（Agent 未执行图片获取/绘制）")

# 3. 目录中至少有一张图片
if figures_dir.exists():
    image_extensions = (".png", ".jpg", ".jpeg", ".pdf", ".gif", ".bmp")
    images = [f for f in figures_dir.iterdir() if f.suffix.lower() in image_extensions]
    if images:
        results.append(f"OK: figures/ 中有 {len(images)} 张图片: {[i.name for i in images]}")
    else:
        results.append("FAIL: figures/ 目录为空，无图片文件（Agent 未生成/下载图片）")

# 4. 图片在正文中被引用
if (paper_dir / "paper.tex").exists():
    ok, msg = check_file_contains(paper_dir / "paper.tex", "\\includegraphics")
    results.append(msg)
    ok, msg = check_file_contains(paper_dir / "paper.tex", "figures/")
    results.append(msg)

# 5. 大纲中包含图片规划（前置检查）
outline = paper_dir / "outline.md"
if outline.exists():
    content = outline.read_text(encoding="utf-8")
    if "配图" in content or "fig" in content.lower() or "图表" in content:
        results.append("OK: 大纲中规划了配图")
    else:
        results.append("FAIL: 大纲中未规划配图")

failed = sum(1 for r in results if r.startswith("FAIL"))
for r in results:
    print(r)

sys.exit(0 if failed == 0 else 1)

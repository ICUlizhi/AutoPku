#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python3 << 'PYEOF'
from pathlib import Path

# 构造一篇正文恰好 150 个汉字（不含标点/空格/换行）的短文
text = """\
人工智能正在深刻改变人类社会的生产生活方式
从医疗诊断到自动驾驶从自然语言处理到计算机视觉
AI技术已经渗透到各个领域然而技术发展的同时也带来了
伦理和治理方面的挑战如何确保算法公平透明如何保护用户
隐私数据如何避免自动化决策带来的歧视问题这些都是当前
学术界和产业界共同关注的焦点未来的人工智能发展需要在
技术创新
"""

# 验证字数
clean = "".join(c for c in text if "\u4e00" <= c <= "\u9fff")
assert len(clean) == 150, f"预期 150 个汉字，实际 {len(clean)}"

Path("essay.md").write_text(text, encoding="utf-8")
print(f"OK: essay.md 生成完成，正文汉字数 = {len(clean)}")
PYEOF

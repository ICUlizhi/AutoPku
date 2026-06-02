#!/bin/bash
set -e

# 创建课程目录和模拟课件
mkdir -p test00/逻辑导论/lectures
mkdir -p test00/逻辑导论/slides/figures
touch test00/逻辑导论/slides/figures/.gitkeep

# 使用 conftest 中的 generate_mock_lecture_pdf 生成模拟课件 PDF
python3 << 'PYEOF'
import sys
from pathlib import Path

# 插入 tests 目录到 path
sys.path.insert(0, str(Path.cwd().parent.parent))
from conftest import generate_mock_lecture_pdf

generate_mock_lecture_pdf(
    Path("test00/逻辑导论/lectures/lecture1.pdf"),
    title="逻辑导论 第1讲：命题逻辑"
)
generate_mock_lecture_pdf(
    Path("test00/逻辑导论/lectures/lecture2.pdf"),
    title="逻辑导论 第2讲：谓词逻辑"
)
PYEOF

# 模拟 AI Agent 生成的 slides 输出（用于 validate 的结构验证）
cat > test00/逻辑导论/slides/main.typ << 'EOF'
#import "style/index.typ": presentation-theme
#import "slides/index.typ": (
  agenda-page, cover-page, end-page, subject-content-page, transition-page,
)

#let report-title = [逻辑导论课程汇报]
#let report-author = [测试作者]
#let report-institution = [北京大学]
#let report-date = [2026-06-02]
#let demo-image = "figures/background.png"

#show: presentation-theme

#cover-page(
  title: report-title,
  author: report-author,
  institution: report-institution,
  date: report-date,
)

#agenda-page(
  sections: (
    [01 / 命题逻辑],
    [02 / 谓词逻辑],
  ),
)

#transition-page(
  number: [01],
  title: [命题逻辑],
  description: [介绍命题逻辑的基本概念与推理规则。],
)

#subject-content-page(
  title: [命题逻辑基础],
  header-left-offset: 10em,
  top-content: [一句话结论：命题逻辑是形式化推理的基础。],
  content: [
    - 命题是可以判断真假的陈述句
    - 联结词包括：否定、合取、析取、蕴涵、等价
    - 真值表用于判断命题公式的真假
  ],
)

#end-page(
  title: [谢谢聆听],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
EOF

cat > test00/逻辑导论/slides/outline.md << 'EOF'
# 幻灯片大纲：逻辑导论课程汇报

## 第1页：封面
- 类型：cover-page
- 内容：标题、作者、单位、日期

## 第2页：目录
- 类型：agenda-page
- sections: ["01 / 命题逻辑", "02 / 谓词逻辑"]

## 第3页：过渡页
- 类型：transition-page
- number: "01"
- title: "命题逻辑"
- description: "介绍命题逻辑的基本概念与推理规则。"

## 第4页：内容页
- 类型：subject-content-page
- title: "命题逻辑基础"
- top-content: "一句话结论：命题逻辑是形式化推理的基础。"
- content: ["命题是可以判断真假的陈述句", "联结词包括：否定、合取、析取、蕴涵、等价", "真值表用于判断命题公式的真假"]

## 第5页：结束页
- 类型：end-page
- 内容：致谢
EOF

echo "setup complete"

#!/bin/bash
# AI Agent 执行步骤：
# 1. 将 input/note.md 渲染为 PDF
# 2. 使用支持数学公式的引擎，例如：
#    pandoc input/note.md -o output/note.pdf \
#      --pdf-engine=xelatex \
#      -V CJKmainfont="PingFang SC" \
#      --mathjax 或 --mathml
# 3. 或者使用 Typst 等现代排版引擎，确保 unicode-math 符号正确
# 4. 确保模态逻辑符号（Box, Diamond, forall, leftrightarrow）正确渲染
# 5. 保存到 output/note.pdf

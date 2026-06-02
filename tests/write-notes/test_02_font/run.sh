#!/bin/bash
# AI Agent 执行步骤：
# 1. 将 input/note.md 渲染为 PDF
# 2. 使用支持中文的字体参数，例如：
#    pandoc input/note.md -o output/note.pdf \
#      --pdf-engine=xelatex \
#      -V CJKmainfont="PingFang SC" \
#      -V mainfont="PingFang SC"
#    或者使用 Songti SC：
#      -V CJKmainfont="Songti SC" \
#      -V CJKmainfontoptions="BoldFont=Songti SC Bold"
# 3. 确保 PDF 中中文字符可正常显示

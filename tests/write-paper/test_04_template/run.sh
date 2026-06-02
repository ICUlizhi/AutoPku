#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给学术英语写作写课程论文"
# Step 3: Agent 执行 write-paper 流程
#   - Phase 1: 获取论文要求（固定题目）
#   - Phase 2: 用户确认
#   - Phase 5:
#     a) git worktree add /tmp/pku-paper-template source
#     b) cp 模板到 test00/学术英语写作/论文/template.tex
#     c) 替换所有占位符：题目、页眉、姓名、学号、院系、摘要
#     d) 插入正文、参考文献
#     e) git worktree remove /tmp/pku-paper-template
#     f) xelatex 编译
# Step 4: python validate.py

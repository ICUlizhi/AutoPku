#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给马原写课程论文，用 LaTeX 格式"
# Step 3: Agent 执行 write-paper 流程
#   - Phase 1: 扫描 test00/马原/通知/ 和 test00/马原/资料/ 获取论文要求
#   - Phase 2: AskUserQuestion 确认题目、格式、字数
#   - Phase 3: 生成大纲（含图片规划）
#   - Phase 4: Agent Team 并行生成各章节 LaTeX 正文
#   - Phase 5: 获取模板 → 替换占位符 → 插入正文 → 编译 xelatex
# Step 4: python validate.py

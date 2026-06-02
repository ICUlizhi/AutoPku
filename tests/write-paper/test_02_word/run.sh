#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给财务报表分析写课程论文，用 Word 格式"
# Step 3: Agent 执行 write-paper 流程
#   - Phase 1: 扫描 test00/财务报表分析/通知/ 获取论文要求
#   - Phase 2: AskUserQuestion 确认题目、格式、字数
#   - Phase 3: 生成大纲
#   - Phase 4: Agent Team 并行生成各章节正文（Markdown 格式）
#   - Phase 4.5: 图片获取与绘制（matplotlib 数据图表）
#   - Phase 5: 使用 python-docx 渲染 Word，注意修改 core_properties
# Step 4: python validate.py

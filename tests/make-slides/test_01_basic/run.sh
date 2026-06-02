#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给逻辑导论做个汇报PPT"
# Step 3: Agent 执行 make-slides 流程：
#   - Phase 1: 检测 test00/逻辑导论/lectures/ 下的课件 PDF
#   - Phase 2: 提取课件核心内容（定义、定理、结论）
#   - Phase 3: 生成幻灯片大纲，保存到 slides/outline.md
#   - Phase 4: 并行生成各页 typst 代码
#   - Phase 5: 获取 touying-ethan 模板，组装 main.typ，typst compile
#   - Phase 6: 用户确认
# Step 4: python validate.py

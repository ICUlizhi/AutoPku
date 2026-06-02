#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "生成中文幻灯片"
# Step 3: Agent 确保模板已获取，生成包含中文内容的 main.typ
#   - 封面、目录、过渡页、正文页均使用中文
#   - 注意数学公式与中文混排
# Step 4: typst compile 并验证中文字符正确渲染
# Step 5: python validate.py

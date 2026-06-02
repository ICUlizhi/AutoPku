#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给XX课做个汇报PPT"
# Step 3: Agent 执行 slide-renderer 工具：
#   - 检查 ~/.autopku/templates/touying-ethan/ 是否存在
#   - 若不存在，git clone https://github.com/hanlife02/touying-ethan.git
#   - 复制模板到 {course}/slides/
#   - 根据大纲组装 main.typ（覆盖模板示例）
#   - typst compile main.typ slides.pdf
#   - 验证编译输出
# Step 4: python validate.py

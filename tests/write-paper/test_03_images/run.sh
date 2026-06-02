#!/bin/bash
# Step 1: 确认在 AutoPku 项目根目录
# Step 2: 用户意图 "给科技创新实践写课程论文"
# Step 3: Agent 执行 write-paper 流程
#   - Phase 3: 生成大纲（必须包含图片规划）
#   - Phase 4.5: **关键步骤** — 检测到 outline 中有配图规划
#               必须引用 tools/image-handler.md 搜索/绘制图片
#               创建 figures/ 目录并保存图片
#   - Phase 5: 渲染时确保 \includegraphics 路径正确
# Step 4: python validate.py

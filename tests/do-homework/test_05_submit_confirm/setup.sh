#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# 创建模拟的作业目录结构和一份待提交 PDF
cat > confirm_prompt.md << 'EOF'
# 提交前确认提示

作业已完成渲染，路径：course/作业/hw5_answer.pdf

请在执行提交命令前，先向用户确认：
- 是否查看 PDF 预览？
- 是否确认提交到教学网？

严禁在未获得用户明确同意的情况下执行 pku3b a submit。
EOF

echo "OK: 模拟作业结构和确认提示已创建"

#!/bin/bash
set -e
mkdir -p test00/逻辑导论
mkdir -p test00/哲学导论
mkdir -p fixtures
cat > fixtures/mock_assignments.txt << 'EOF'
逻辑导论
  [1] 第二次作业
    状态: 待提交
    截止日期: 2026-06-10
    附件: homework2.pdf
  [2] 第一次作业
    状态: 已完成
    截止日期: 2026-05-20

哲学导论
  [1] 期中论文
    状态: 待提交
    截止日期: 2026-06-15
    附件: midterm_prompt.pdf
  [2] 阅读笔记
    状态: 已完成
    截止日期: 2026-05-25
EOF
echo "setup complete"

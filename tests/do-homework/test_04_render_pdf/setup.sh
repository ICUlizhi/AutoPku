#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

cat > answer.md << 'EOF'
# 人工智能课程作业解答

## 第一题：设计思想

AutoPku 的设计思想可以概括为 **Skill 即代码** 与 **Agent Team 协作**。

在能量与质量的关系中，著名的质能方程为 $E = mc^2$。该方程揭示了质量与能量之间的等价关系。

对于更复杂的推导，我们可以写出积分形式：

$$
\int_{0}^{\infty} e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

这一结果在概率论和量子力学中都有广泛应用。

## 第二题：协作模式

Agent Team 采用主从架构：

1. **Planner** 负责任务分解
2. **Solver** 负责具体求解
3. **Reviewer** 负责质量检查

通过 AskUserQuestion 实现人机协同，确保关键节点由用户确认。
EOF

echo "OK: answer.md 生成完成"

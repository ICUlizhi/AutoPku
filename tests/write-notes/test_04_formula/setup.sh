#!/bin/bash
set -e

mkdir -p input output

# 创建包含数学公式的 Markdown 文件
cat > input/note.md << 'EOF'
# 模态逻辑公式

## 可达关系

$xRy$ 表示世界 $x$ 可以到达世界 $y$。

## 模态算子

- 必然算子：$\Box \phi$
- 可能算子：$\Diamond \psi$
- 双重否定：$\neg \neg \alpha \leftrightarrow \alpha$

## 关系性质

自反性：$\forall x (xRx)$

对称性：$\forall x \forall y (xRy \to yRx)$

传递性：$\forall x \forall y \forall z ((xRy \land yRz) \to xRz)$

EOF

echo "OK: 公式测试笔记已创建到 input/note.md"

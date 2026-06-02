#!/bin/bash
set -e

mkdir -p input output notes

# 创建包含唯一标记的笔记源文件
cat > input/note.md << 'EOF'
# 逻辑导论完整笔记

## 第一讲 命题逻辑

这是第一讲的内容，介绍命题、真值、联结词等基本概念。

UNIQUE_MARKER_7A3F9E2D_第一讲结束

## 第二讲 谓词逻辑

这是第二讲的内容，介绍量词、谓词、模型等概念。

UNIQUE_MARKER_7A3F9E2D_第二讲结束

## 第三讲 模态逻辑

这是第三讲的内容，介绍可能世界、可达关系、模态算子等。

UNIQUE_MARKER_7A3F9E2D_第三讲结束

EOF

echo "OK: 幂等性测试笔记已创建到 input/note.md"

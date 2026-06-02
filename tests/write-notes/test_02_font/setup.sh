#!/bin/bash
set -e

mkdir -p input output

# 创建包含中文字符的 Markdown 文件
cat > input/note.md << 'EOF'
# 逻辑导论笔记

## 命题逻辑

在命题逻辑中，我们研究**命题**之间的关系。

### 基本概念

- **命题**：能够判断真假的陈述句
- **真值**：真或假
- **联结词**：且、或、非、如果…那么…

### 重要定理

完备性定理：命题逻辑是完备的。

EOF

echo "OK: 中文测试笔记已创建到 input/note.md"

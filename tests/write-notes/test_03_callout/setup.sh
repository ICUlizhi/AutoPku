#!/bin/bash
set -e

mkdir -p input output notes

# 创建包含 callout 语法的 Markdown 文件
# 注意：callout 正文故意写得较长，以验证内容是否被完整包含
cat > input/note.md << 'EOF'
# 模态逻辑笔记

## 可达关系

在模态逻辑中，可达关系 $R$ 是一个关键概念。

> [!tip]
> 可达关系在不同语境下有不同名称：在时态逻辑中称为「前后关系」，在认知逻辑中称为「不可区分关系」。
> 记住：$xRy$ 表示世界 $x$ 可以到达世界 $y$。

> [!note]
> 框架 (frame) 是一个二元组 $\langle W, R \rangle$，其中 $W$ 是非空的可能世界集合，$R$ 是 $W$ 上的二元关系。
> 一个模型是在框架上附加赋值函数得到的结构。

## 模态算子

$\Box \phi$ 表示在所有可达世界中 $\phi$ 为真。

EOF

echo "OK: Callout 测试笔记已创建到 input/note.md"

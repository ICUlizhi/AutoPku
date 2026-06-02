#!/bin/bash
set -e

# 创建模拟课程目录结构
COURSE_DIR="test00/马原"
mkdir -p "${COURSE_DIR}/通知"
mkdir -p "${COURSE_DIR}/资料"
mkdir -p "${COURSE_DIR}/论文"
mkdir -p "${COURSE_DIR}/论文/figures"

# 模拟论文要求文件（来自教学网通知）
cat > "${COURSE_DIR}/通知/论文要求.md" << 'EOF'
# 马克思主义基本原理课程论文要求

## 题目
从以下选题中任选一题：
1. 马克思劳动价值论在数字经济时代的现实意义
2. 《共产党宣言》中的全球化思想及其当代价值

## 要求
- 字数：不少于 3000 字
- 格式：LaTeX 或 Word 均可，鼓励使用 LaTeX
- 提交方式：教学网提交 PDF
- 截止日期：2026-06-20
- 必须包含：摘要、关键词、参考文献
EOF

# 模拟大纲（由 Agent 生成）
cat > "${COURSE_DIR}/论文/outline.md" << 'EOF'
# 论文大纲：《共产党宣言》中的全球化思想及其当代价值

## 一、引言（约 500 字）
- 简述《共产党宣言》的历史背景
- 提出全球化研究的核心问题

## 二、《共产党宣言》中的全球化思想（约 1200 字）
- 世界市场的形成
- 资产阶级在历史上起到的革命性作用
- "一切国家的生产和消费都成为世界性的"

## 三、全球化思想的当代价值（约 1000 字）
- 对理解当代经济全球化的启示
- 对构建人类命运共同体的理论贡献

## 四、结论（约 300 字）
- 总结全文观点
- 展望未来研究方向

## 参考文献
1. 马克思, 恩格斯. 共产党宣言[M]. 北京: 人民出版社, 2018.
EOF

# 模拟已生成的 paper.tex（由 Agent 渲染输出）
cat > "${COURSE_DIR}/论文/paper.tex" << 'EOF'
\documentclass[UTF8,12pt,a4paper]{ctexart}

\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{graphicx}
\usepackage{hyperref}

\title{《共产党宣言》中的全球化思想及其当代价值}
\author{徐靖}
\date{2026年6月}

\begin{document}

\maketitle

\begin{abstract}
《共产党宣言》作为科学社会主义的纲领性文献，蕴含了深刻的全球化思想。
本文通过文本分析，梳理了马克思、恩格斯关于世界市场、国际分工和资本扩张的论述，
并探讨了这些思想对理解当代经济全球化及构建人类命运共同体的理论价值。
\end{abstract}

\section{引言}

1848年，《共产党宣言》的发表标志着科学社会主义的诞生。在这部经典著作中，
马克思和恩格斯以敏锐的洞察力揭示了资本主义推动世界市场形成的历史进程。

\section{《共产党宣言》中的全球化思想}

\subsection{世界市场的形成}

资产阶级通过开拓世界市场，使一切国家的生产和消费都成为世界性的了。

\subsection{资产阶级的革命性作用}

资产阶级在它的不到一百年的阶级统治中所创造的生产力，比过去一切世代
创造的全部生产力还要多，还要大。

\section{全球化思想的当代价值}

\subsection{对理解当代经济全球化的启示}

\subsection{对构建人类命运共同体的理论贡献}

\section{结论}

本文通过分析《共产党宣言》中的全球化思想，揭示了其对当代全球化研究的
深刻启示。

\section*{参考文献}
\begin{enumerate}
    \item 马克思, 恩格斯. 共产党宣言[M]. 北京: 人民出版社, 2018.
\end{enumerate}

\end{document}
EOF

# 模拟校徽图片
touch "${COURSE_DIR}/论文/figures/pku.pdf"

echo "setup complete"

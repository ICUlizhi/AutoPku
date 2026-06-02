#!/bin/bash
set -e

COURSE_DIR="test00/科技创新实践"
mkdir -p "${COURSE_DIR}/通知"
mkdir -p "${COURSE_DIR}/资料"
mkdir -p "${COURSE_DIR}/论文"

# 模拟论文要求
cat > "${COURSE_DIR}/通知/论文要求.md" << 'REQEOF'
# 科技创新实践课程论文要求

## 题目
围绕"人工智能在医疗领域的应用"撰写课程论文

## 要求
- 字数：4000字左右
- 格式：LaTeX
- 必须包含：框架图、流程图或数据图表（至少1张）
- 提交：PDF
REQEOF

# 模拟大纲（明确规划了配图）
cat > "${COURSE_DIR}/论文/outline.md" << 'OUTEOF'
# 人工智能在医疗领域的应用研究

## 一、引言（约 400 字）
- AI 医疗的发展背景
- 研究问题与意义

## 二、AI 医疗技术框架（约 1200 字）
- 机器学习、深度学习、计算机视觉在医疗中的应用
- **配图：fig1_framework.png** — AI 医疗技术应用框架图

## 三、典型案例分析（约 1200 字）
- 医学影像诊断
- 药物研发
- **配图：fig2_case.png** — 某 AI 诊断系统的流程图

## 四、挑战与展望（约 800 字）
- 数据隐私、伦理问题
- 未来发展趋势

## 五、结论（约 400 字）

## 参考文献
1. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence[J]. Nature Medicine, 2019.
OUTEOF

# 模拟正文（包含图片引用）
cat > "${COURSE_DIR}/论文/paper.tex" << 'TEXEOF'
\documentclass[UTF8,12pt,a4paper]{ctexart}
\usepackage{geometry,graphicx}
\title{人工智能在医疗领域的应用研究}
\author{徐靖}
\begin{document}
\maketitle
\section{引言}
人工智能技术在医疗领域的应用日益广泛。
\section{AI 医疗技术框架}
如图 \ref{fig:framework} 所示，AI 医疗技术主要包括三个层次。
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig1_framework.png}
    \caption{AI 医疗技术应用框架}
    \label{fig:framework}
\end{figure}
\section{典型案例分析}
\section{挑战与展望}
\section{结论}
\end{document}
TEXEOF

# 注意：故意不创建 figures/ 目录和图片
# 这是为了模拟踩坑场景 — Agent 若未执行 image-handler，figures/ 就不存在

echo "setup complete"

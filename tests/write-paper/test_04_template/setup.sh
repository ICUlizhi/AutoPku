#!/bin/bash
set -e

COURSE_DIR="test00/学术英语写作"
mkdir -p "${COURSE_DIR}/通知"
mkdir -p "${COURSE_DIR}/资料"
mkdir -p "${COURSE_DIR}/论文"
mkdir -p "${COURSE_DIR}/论文/figures"

# 模拟论文要求
cat > "${COURSE_DIR}/通知/论文要求.md" << 'REQEOF'
# 学术英语写作课程论文要求

## 题目
A Comparative Study of Sino-Western Business Etiquette（固定题目）

## 要求
- 字数：3000词左右
- 格式：LaTeX，使用课程提供的模板
- 提交：PDF
REQEOF

# 模拟从 git worktree 获取的模板（含占位符）
cat > "${COURSE_DIR}/论文/template.tex" << 'TEXEOF'
\documentclass[UTF8,12pt,a4paper]{ctexart}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{graphicx}
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{在此填写页眉（可以是论文题目）}
\renewcommand{\headrulewidth}{0.4pt}

\title{在此填写题目}
\author{在此填写姓名}
\date{}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{2cm}
    {\LARGE 北京大学课程论文}\\[2cm]
    {\Huge \textbf{在此填写题目}}\\[1cm]
    {\large 姓名：在此填写姓名}\\[0.3cm]
    {\large 学号：在此填写学号}\\[0.3cm]
    {\large 院系：在此填写院系}\\[2cm]
\end{titlepage}

\newpage
\section*{摘要}
在此填写摘要内容

\newpage
\tableofcontents
\newpage

% 正文插入位置

\section*{参考文献}

\end{document}
TEXEOF

# 模拟替换后的 paper.tex（由 Agent 渲染输出）
# 注意：故意保留一个未替换的占位符，用于测试验证脚本能否发现
cat > "${COURSE_DIR}/论文/paper.tex" << 'TEXEOF'
\documentclass[UTF8,12pt,a4paper]{ctexart}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{graphicx}
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{A Comparative Study of Sino-Western Business Etiquette}
\renewcommand{\headrulewidth}{0.4pt}

\title{A Comparative Study of Sino-Western Business Etiquette}
\author{徐靖}
\date{}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{2cm}
    {\LARGE 北京大学课程论文}\\[2cm]
    {\Huge \textbf{A Comparative Study of Sino-Western Business Etiquette}}\\[1cm]
    {\large 姓名：徐靖}\\[0.3cm]
    {\large 学号：2000012345}\\[0.3cm]
    {\large 院系：光华管理学院}\\[2cm]
\end{titlepage}

\newpage
\section*{摘要}
This paper compares the differences between Chinese and Western business etiquette.

\newpage
\tableofcontents
\newpage

\section{Introduction}
Business etiquette varies significantly across cultures.

\section{Literature Review}
Previous studies have examined various aspects of cross-cultural communication.

\section{Analysis}
The main differences lie in greeting manners, dining etiquette, and gift-giving customs.

\section{Conclusion}
Understanding these differences is crucial for international business success.

\section*{参考文献}
\begin{enumerate}
    \item Smith, J. (2020). Cross-Cultural Business Communication. Harvard Business Review.
\end{enumerate}

\end{document}
TEXEOF

# 模拟校徽
touch "${COURSE_DIR}/论文/figures/pku.pdf"

echo "setup complete"

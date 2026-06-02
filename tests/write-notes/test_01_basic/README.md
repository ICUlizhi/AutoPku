# test_01_basic — PDF 课件 → 笔记基础流程

## 目的
验证 write-notes skill 能够从 PDF 课件中提取核心内容，并生成结构化的 Markdown 笔记。

## 场景
模拟从「逻辑导论」课件 PDF 提取定义、定理等关键知识点，生成 notes/lecture.md。

## 文件结构
- `input/lecture.pdf` — 模拟课件（由 setup.sh 生成）
- `notes/*.md` — 生成的笔记（由 AI Agent 执行 run.sh 后产生）

## 验证点
1. notes/ 目录下存在 .md 文件
2. 笔记内容包含「定义」关键词
3. 笔记内容包含「定理」关键词

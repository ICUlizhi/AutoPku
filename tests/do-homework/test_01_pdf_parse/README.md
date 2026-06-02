# test_01_pdf_parse — PDF 作业解析与答案生成

## 目标
验证 AutoPku 的 `do-homework` Skill 能正确解析 PDF 作业文件，提取题目结构，并生成对应的解答 JSON。

## 输入
- `homework_mock.pdf`：模拟的课程作业 PDF（reportlab 生成，包含 3 道题目）

## 期望执行流程（AI Agent）
1. 使用 `tools/pdf-reader.md` 中的逻辑解析 PDF，生成 `homework_parsed.json`
2. 创建 Solver Agent，逐题解答，生成 `answers.json`
3. （可选）将答案渲染为 Markdown / PDF

## 期望输出
- `homework_parsed.json`：包含 `pages` 和 `problems` 字段，problems 数量 >= 1
- `answers.json`：包含 `answers` 列表，每个元素有 `number` 和 `content`

## 备注
若环境中未安装 reportlab，setup.sh 会生成文本占位文件，validate.py 将跳过 PDF 解析相关验证，仅检查结构。

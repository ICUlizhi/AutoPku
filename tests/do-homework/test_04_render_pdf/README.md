# test_04_render_pdf — Markdown → PDF 渲染

## 目标
验证 `do-homework.md` 中的渲染流程能正确将包含 LaTeX 公式的 Markdown 转换为 PDF，且 PDF 有实际内容、页数正常。

## 输入
- `answer.md`：包含标题、正文、LaTeX 行内公式 `$E=mc^2$` 和块级公式 `$$...$$` 的 Markdown 文件

## 期望执行流程（AI Agent）
1. 使用 `markdown` 库将 Markdown 转为 HTML
2. 插入 MathJax 脚本以渲染 LaTeX
3. 使用 Chrome Headless 打印为 PDF

## 期望输出
- `answer.pdf`：渲染后的 PDF 文件
  - 页数 >= 1
  - 包含可提取文本（非空白/图片-only）
  - 包含原 Markdown 中的核心文字（如 "AutoPku"、"设计思想"）

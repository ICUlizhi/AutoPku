# test_03_callout — Callout 文本正确包含

## 目的
验证笔记中的 Obsidian callout（如 `[!tip]`、`[!note]`）的正文内容被完整包含在最终输出中，而不仅仅是标题。

## 来源
来自 Kimi session 踩坑：`> [!note]` 的折叠/展开内容在渲染或导出时未被实际包含进最终 PDF，导致知识点丢失。

## 文件结构
- `input/note.md` — 包含 callout 语法的测试 Markdown（由 setup.sh 生成）
- `output/note.pdf` 或 `notes/note.md` — 最终输出（由 AI Agent 执行 run.sh 后产生）

## 验证点
1. 最终输出文件中包含 callout 的标题
2. **更重要的是**：callout 内部的正文描述（如「不可区分关系」「框架是一个二元组」等）也被完整保留

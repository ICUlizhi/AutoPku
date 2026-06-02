#!/bin/bash
# AI Agent 执行步骤：
# 1. 将 input/note.md 转换为最终输出格式（PDF 或处理后的 Markdown）
# 2. 确保 callout 的正文内容（不仅仅是标题）被完整包含在输出中
# 3. 如果使用 Pandoc 处理 Obsidian callout，需要确保折叠/展开内容都保留
# 4. 如果使用 Obsidian 导出 PDF，注意先展开所有 callout 再导出
# 5. 保存到 output/note.pdf 或 notes/note.md

# test_05_idempotent — 幂等性 / 不重复渲染

## 目的
验证同一笔记源文件多次执行渲染时，不会导致内容重复追加（如 PDF 页数翻倍、同一知识点出现多次）。

## 来源
来自 Kimi session 踩坑：PDF 被渲染两次，110 页的内容被重放为 220 页；或 Markdown 笔记被追加写入导致内容翻倍。

## 文件结构
- `input/note.md` — 包含唯一标记的源文件（由 setup.sh 生成）
- `output/note.pdf` / `notes/note.md` — 最终输出（由 AI Agent 执行 run.sh 后产生）

## 验证点
1. 最终输出中每个 `UNIQUE_MARKER_7A3F9E2D_*` 标记只出现 **一次**
2. 若出现多次，则说明存在重复渲染/追加写入问题

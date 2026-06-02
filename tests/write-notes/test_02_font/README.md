# test_02_font — 宋体字体渲染

## 目的
验证 Markdown 笔记渲染为 PDF 时，中文字体（PingFang SC / Songti SC）被正确使用，中文内容不会乱码或丢失。

## 来源
来自 Kimi session 踩坑：用 songti 渲染笔记时，若未指定中文字体参数，中文会显示为空白或乱码。

## 文件结构
- `input/note.md` — 包含中文字符的测试 Markdown（由 setup.sh 生成）
- `output/note.pdf` — 渲染后的 PDF（由 AI Agent 执行 run.sh 后产生）

## 验证点
1. 生成的 PDF 文件存在
2. 通过 `strings` 命令可在 PDF 中检出中文字符（如「命题」「逻辑」「定理」）

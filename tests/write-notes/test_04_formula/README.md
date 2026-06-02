# test_04_formula — 数学公式渲染

## 目的
验证模态逻辑等复杂数学公式（如 `$xRy$`、`$\Box \phi$`）在渲染为 PDF 时符号正确、不丢失。

## 来源
来自 Kimi session 踩坑：模态逻辑的 $xRy$ 符号在渲染后变成乱码或空白；Box、Diamond 等特殊符号未被正确处理。

## 文件结构
- `input/note.md` — 包含数学公式的测试 Markdown（由 setup.sh 生成）
- `output/note.pdf` — 渲染后的 PDF（由 AI Agent 执行 run.sh 后产生）

## 验证点
1. 生成的 PDF 文件存在
2. 公式相关文本（如「xRy」「Box」「Diamond」等）在 PDF 中可被 `strings` 检出
3. 或至少主体文本（如「可达关系」「自反性」）正确存在

# test_03_docx_security — DOCX 隐藏文字安全扫描

## 背景
来自 PR #16 和 `pr16_test/` 目录的真实案例：
- 某课程作业 DOCX 中存在**隐藏文字**（`w:vanish`）和**与背景色同色的文字**
- 若 AI 直接提取全部文本并作为题目输入，可能把隐藏提示/答案也传给 Solver，导致学术诚信风险

## 目标
验证 `tools/docx-reader.md` / `tools/pdf-reader.md` 中的安全扫描逻辑能正确检测 DOCX 中的：
1. **vanish 隐藏文字** (`w:vanish`)
2. **颜色异常**（文字颜色与背景色过于接近）

## 输入
- `suspicious.docx`：包含正常题目 + 隐藏提示文字 + 浅色背景色文字的 DOCX

## 期望执行流程（AI Agent）
1. 使用 `scan_docx_hidden_text()` 扫描文档
2. 若发现 alerts，在解析结果中标注，并提示用户

## 期望输出
- `docx_scan_report.json`：扫描报告，包含检测到的 alerts 列表
- alerts 数量应 **>= 2**（vanish 隐藏 + 颜色异常）

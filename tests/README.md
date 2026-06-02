# AutoPku 真实案例集

从本地 Kimi Sessions 中提取的真实使用案例，每个案例包含用户原始输入、Agent 执行过程、踩坑分析与修复记录。

## 数据来源

- `~/.kimi/user-history/*.jsonl` — 用户输入历史
- `~/.kimi/sessions/<session_id>/<turn_id>/wire.jsonl` — 完整对话记录（含 Agent 思考、工具调用）
- `~/.kimi/sessions/<session_id>/<turn_id>/context.jsonl` — 上下文消息

## 案例列表

| # | 案例 | 来源 Session | 涉及功能 | 核心问题 |
|---|------|-------------|---------|---------|
| 1 | [马原论文 PDF → Word 转换](cases/case_01_marxism_paper_pdf_to_word.md) | `5f918769...` | `write-paper` | PDF 文本提取、Word 格式化、中文字体 |
| 2 | [笔记 Callout 文本丢失](cases/case_02_notes_callout_missing.md) | `33e4e429...` | `write-notes` | Callout 正文被吞、lua filter 修复 |
| 3 | [笔记 PDF 重复渲染](cases/case_03_notes_duplicate_rendering.md) | `5f918769...` | `write-notes` | 110页重复内容、幂等性 |
| 4 | [Kimi Agent Team 支持](cases/case_04_kimi_runtime_support.md) | `5f918769...` | `runtime` | 跨平台 Agent 创建语法差异 |
| 5 | [论文图片功能缺失](cases/case_05_paper_images_missing.md) | `4041a8d...` | `write-paper` | 图片搜索/绘制未触发 |

## 案例格式

每个案例文件包含：
1. **用户原始输入** — 真实触发问题的用户意图
2. **Agent 思考过程** — 从 `wire.jsonl` 中提取的 thinking 内容
3. **关键工具调用序列** — 实际执行的 Shell/ReadFile/WriteFile 等工具
4. **问题根因** — 为什么出现了问题
5. **修复过程** — 如何修复（如已修复）
6. **测试价值** — 可用于验证什么功能点

## 如何提取新案例

```bash
# 查看 user-history 中 AutoPku 相关的消息
grep -i "autopku\|skill\|pku3b\|写笔记\|写论文\|做作业\|同步通知" ~/.kimi/user-history/*.jsonl

# 查看 session 中的详细对话
head -100 ~/.kimi/sessions/<session_id>/<turn_id>/wire.jsonl
```

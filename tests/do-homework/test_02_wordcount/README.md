# test_02_wordcount — 字数统计检查

## 背景
来自真实踩坑：Kimi session 中 AI 曾忽略词数要求，导致作业被退回。用户反馈：
> "词数你单独写代码统计一下"、"将词数统计这一细节记录到 do-homework.md"

## 目标
验证 `do-homework.md` 中定义的字数统计脚本能正确计算**中文字数**（不含标点、空格、英文单词按空格分隔计数）。

## 输入
- `essay.md`：一篇已知字数的中文短文（正文 150 个汉字，不含标点和空格）

## 期望执行流程（AI Agent）
1. 读取 `essay.md`
2. 运行字数统计脚本（过滤标点、空格）
3. 将统计结果记录到日志或元数据文件

## 期望输出
- `wordcount_result.json`：包含 `chinese_chars`（中文字符数）、`total_chars`（总字符数）等字段
- `chinese_chars` 应等于 **150**

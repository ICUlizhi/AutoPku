# 测试：write-paper — 模板替换正确性

## 场景描述
write-paper 流程中通过 git worktree 获取 LaTeX 模板后，必须将模板中的占位符
全部替换为实际值（题目、姓名、学号、院系、摘要、页眉等）。
本测试验证占位符替换的完整性。

## 前置条件
- git worktree 可正常添加/移除（或模拟模板文件）

## 输入
- 模拟模板：`test00/学术英语写作/论文/template.tex`（含占位符）
- 实际值：
  - 题目 = "A Comparative Study of Sino-Western Business Etiquette"
  - 姓名 = "徐靖"
  - 学号 = "2000012345"
  - 院系 = "光华管理学院"
  - 摘要 = "This paper compares..."

## 期望输出
1. 所有占位符均被替换，无残留
2. 实际值正确填入对应位置
3. 模板结构未被破坏（documentclass、begin/end document 完整）

## 验证命令
```bash
python validate.py
```

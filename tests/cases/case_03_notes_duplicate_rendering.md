# 真实案例 #3：笔记 PDF 重复渲染（110页 → 重复内容）

> **来源**: Kimi Session `5f91876922590e8cef7197ec2eb3d1a2` / user-history
> **时间**: 2026-04
> **涉及功能**: `write-notes`（PDF 渲染）

---

## 用户原始输入序列

### Turn 1: 发现重复渲染

```
/Users/moonshot/Desktop/桌面整理/项目/pku大四下/逻辑导论/notes main.pdf
似乎是被渲染了两次
```

### Turn 2: 确认问题

```
或者你再渲染一遍，我看到的.pdf是110页，重放了一次
```

### Turn 3: 要求重新渲染

```
你再次渲染一下吧
```

## 问题描述

用户发现 `逻辑导论/notes/main.pdf` 有 **110 页**，怀疑内容被**重复渲染了一次**。

这意味着：
1. Agent 执行了两次渲染流程（可能是用户多次触发，或 Agent 自己重复执行）
2. 第二次渲染没有清空第一次的输出，而是**追加**到了同一个 PDF
3. 导致 PDF 页数翻倍，内容重复

## 根因推测

根据 `write-notes.md` 的渲染流程：

```bash
pandoc \
  notes/README.md \
  notes/lec01_*.md notes/lec02_*.md ... \
  -o pdf/{course_name}课程笔记.pdf \
  ...
```

如果 Agent 在**未清空旧文件**的情况下执行了多次 pandoc 命令，且输出文件名相同，pandoc 会覆盖旧文件——所以直接重复执行 pandoc 不会导致追加。

更可能的情况是：
1. Agent 先将多个 md 文件**合并为一个大 md**，然后渲染
2. 合并过程中重复追加了内容
3. 或者 Agent 使用了错误的 pandoc 参数，导致多文件输入时内容被重复包含

## 测试价值

此案例对应 `write-notes/test_05_idempotent`：

- 验证多次执行 `write-notes` 渲染不会导致内容重复
- 检查最终 PDF 页数是否合理（不超过源材料页数的合理倍数）
- 验证幂等性：同一输入多次渲染应产生相同输出

## 验证方法

```python
# 检查唯一标记是否只出现一次
marker = "## 核心问题/Motivation"
count = pdf_text.count(marker)
assert count == 1, f"标记出现 {count} 次，可能重复渲染"
```

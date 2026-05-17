---
name: autopku-runtime-codex
description: Codex Native Subagent 运行时接口
---

# Codex Native Subagent 运行时

## 创建 Subagent

Codex 使用内置的 subagent 机制：

```
请创建 subagent 处理以下任务：

Subagent: {course}-agent

任务：
1. 处理课程 {course} 的作业
2. 下载附件到指定目录
3. 生成通知摘要

工作目录：{work_dir}
```

## 并行执行

```
请为以下课程并行创建 subagents：
{course_list}

每个 subagent 独立处理一门课程，完成后返回结果。
```

## Coordinator 模式

```
你作为 Coordinator，协调以下 subagents 按顺序执行：

Phase 1: 指派 parser-agent 解析 PDF
Phase 2: 收到结果后，指派 solver-agent 解答
Phase 3: 收到结果后，指派 writer-agent 格式化
Phase 4: 收到结果后，指派 submitter-agent 保存

使用 subagent 完成各 phase，等待每个 phase 完成后再进行下一个。
```

## 与 Claude Code 的差异

| 特性 | Claude Code | Codex |
|------|-------------|-------|
| Agent 创建 | `Agent()` tool | Natural language + subagent |
| 通信方式 | `SendMessage()` tool | Return values + context |
| 并行控制 | Team coordination | Parallel subagent requests |
| 状态跟踪 | `TaskCreate/TaskUpdate` | Session context |

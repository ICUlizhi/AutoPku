---
name: autopku-runtime-claude
description: Claude Code Agent Team 运行时接口
---

# Claude Code Agent Team 运行时

## 创建并行 Agent

```python
# 为多个任务并行创建 agents
for course in courses:
    Agent({
        "name": f"{course}-agent",
        "prompt": f"处理课程: {course}...",
        "description": f"处理 {course} 的专属 agent"
    })
```

## Agent 间通信

```python
# Coordinator 发送任务给 agent
SendMessage({
    "to": f"{course}-agent",
    "message": "Phase 1 任务内容..."
})

# Agent 完成任务后回复
SendMessage({
    "to": "coordinator",
    "message": "Phase 1 完成，结果如下..."
})
```

## 完整 Coordinator 示例

```python
# Phase 1: 并行创建解析 agents
for course in courses:
    Agent({
        "name": f"{course}-parser",
        "prompt": f"解析 {course} 的作业 PDF...",
        "description": f"{course} PDF解析器"
    })

# 等待所有 agent 完成（通过消息机制协调）
# 然后进入 Phase 2...
```

## 约束条件

- 最多同时运行 N 个 agents（根据系统资源）
- Agent 之间通过 `SendMessage` 通信
- 使用 `TaskCreate/TaskUpdate` 跟踪进度（如需要）

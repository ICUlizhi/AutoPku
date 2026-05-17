---
name: autopku-runtime-kimi
description: Kimi Code CLI Agent Team 运行时接口
---

# Kimi Code CLI Agent Team 运行时

## 创建 Subagent

Kimi Code CLI 使用内置 `Agent()` tool 创建子代理，支持三种类型：

```python
# explore: 快速探查代码库、定位文件和逻辑
Agent({
    "description": "探索 {course} 作业结构",
    "prompt": f"请快速探查 {course} 目录下的作业文件和课件结构，列出所有需要处理的文件。",
    "subagent_type": "explore"
})

# coder: 处理代码编写、修改、调试任务（默认）
Agent({
    "description": f"处理 {course} 作业",
    "prompt": f"请完成 {course} 的本次作业：解析 PDF、解答题目、生成 Markdown 答案。",
    "subagent_type": "coder"
})

# plan: 实现前的架构规划和步骤拆解
Agent({
    "description": f"规划 {course} 解题方案",
    "prompt": f"请为 {course} 的本次作业制定详细的解题计划，包括每道题的分析思路和所需工具。",
    "subagent_type": "plan"
})
```

## 并行执行

Kimi 支持两种方式实现并行：

### 方式 1：同时发起多个 Agent 调用

在同一个回复中发起多个 `Agent()` 调用，Kimi 会并行调度执行：

```python
# 为多个课程同时创建专属 agent
for course in courses:
    Agent({
        "description": f"处理 {course}",
        "prompt": f"你是课程 {course} 的专属 agent。请处理该课程的通知同步任务...",
        "subagent_type": "coder"
    })
```

### 方式 2：后台任务（长时间运行）

对于需要持续运行的任务（如编译、测试、服务器），使用 `run_in_background=True`：

```python
# 启动后台任务
Agent({
    "description": "启动本地服务器",
    "prompt": "请在后台启动 npm run dev，并监控其输出。",
    "subagent_type": "coder",
    "run_in_background": True
})

# 查询后台任务状态
TaskList({"active_only": True})
TaskOutput({"task_id": "<task_id>"})

# 停止后台任务
TaskStop({"task_id": "<task_id>"})
```

## 结果收集

Kimi 的子代理**没有 `SendMessage()` 工具**。子代理的结果会直接返回给父代理，由父代理统一收集：

```python
results = []
for course in courses:
    result = Agent({
        "description": f"处理 {course}",
        "prompt": f"请处理 {course} 的通知摘要，完成后直接返回摘要内容。",
        "subagent_type": "coder"
    })
    results.append({"course": course, "summary": result})
```

## Coordinator 模式

```python
# Phase 1: 并行创建解析 agents
parsed = []
for course in courses:
    result = Agent({
        "description": f"解析 {course} PDF",
        "prompt": f"解析 {course} 的作业 PDF，提取题目和截止日期。",
        "subagent_type": "coder"
    })
    parsed.append(result)

# Phase 2: 收到结果后，指派 solver agent 解答
solved = Agent({
    "description": "解答所有题目",
    "prompt": f"根据以下解析结果进行解答：\n{parsed}",
    "subagent_type": "coder"
})

# Phase 3: 指派 writer agent 格式化
final = Agent({
    "description": "格式化答案",
    "prompt": f"将以下解答整理成规范的 Markdown 格式：\n{solved}",
    "subagent_type": "coder"
})
```

## 约束条件

- Agent 之间**不直接通信**，结果通过父代理传递
- 长时间任务建议使用 `run_in_background=True` + `TaskList/TaskOutput`
- `timeout` 参数可以控制子代理最大运行时间（单位：秒）
- 默认 `subagent_type` 为 `"coder"`，探查类任务推荐 `"explore"`，规划类任务推荐 `"plan"`

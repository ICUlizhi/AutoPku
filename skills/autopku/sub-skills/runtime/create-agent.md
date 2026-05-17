---
name: autopku-runtime-create-agent
description: 统一的 Agent 创建接口，自动适配当前 AI 环境
---

# 统一 Agent 创建接口

## 快速开始

在 task skill 中引用此文件来创建 agents，无需关心底层 AI 环境。

## 接口定义

### create_agents(task_list, agent_config)

**参数：**
- `task_list`: 任务列表，每个元素是一个字典，包含任务参数
- `agent_config`: agent 配置模板

**示例：**

```markdown
## 并行处理课程

引用: `sub-skills/runtime/create-agent.md`

任务：为每个课程创建专属 agent

任务列表：
```json
[
  {"course": "逻辑导论", "work_dir": "./test/逻辑导论"},
  {"course": "哲学导论", "work_dir": "./test/哲学导论"}
]
```

Agent 模板：
```
你是课程 "{course}" 的专属 agent。

工作目录：{work_dir}
任务：...
```
```

## 运行时适配逻辑

### Claude Code 环境

```python
for task in task_list:
    Agent({
        "name": f"{task['course']}-agent",
        "prompt": agent_template.format(**task),
        "description": f"处理 {task['course']}"
    })
```

### Kimi Code CLI 环境

```python
for task in task_list:
    Agent({
        "description": f"处理 {task['course']}",
        "prompt": agent_template.format(**task),
        "subagent_type": "coder"
    })
```

### Codex 环境

```
请为以下课程并行创建 subagents：

{formatted_task_list}

每个 subagent 使用对应的配置模板。
```

### Fallback 环境

串行执行，逐个处理任务。

## 完整示例

### sync-notices.md 中的使用

```markdown
# 同步课程通知

## 并行处理

引用: `sub-skills/runtime/create-agent.md`

为每门课程创建 agent，并行执行：

```python
# 自动检测环境并执行
agents = create_agents(
    task_list=[
        {"course": c, "base_dir": base_dir}
        for c in courses
    ],
    agent_template="""
你是课程 "{course}" 的专属 agent。

工作目录：{base_dir}/{course}/

任务：
1. 创建目录结构（作业/通知/资料/）
2. 下载作业附件
3. 生成通知摘要.md
"""
)
```
```

## 注意事项

1. 不要直接调用此接口，而是通过引用方式使用
2. 实际的 agent 创建语法由运行时环境决定
3. 在 Codex 环境中，使用自然语言描述并行任务
4. 在 Kimi 环境中，Agent 结果直接返回，无需额外消息通信机制

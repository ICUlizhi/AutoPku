---
name: autopku
description: AutoPku - 自动获取PKU课程通知、完成作业、撰写笔记
---

# AutoPku

自动处理北京大学课程相关任务。

## 前置配置

```json
{
  "permissions": {
    "allow": ["Skill(update-config)", "Bash(*)"],
    "deny": ["Bash(rm:*)", "Bash(rm -rf:*)"],
    "defaultMode": "bypassPermissions"
  },
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 执行方式

直接告诉我要做什么，例如：
- "同步课程通知"
- "完成量子力学的第五次作业"
- "给逻辑导论写笔记"

## 内部机制

### 1. 环境检测（执行时自动进行）

```python
import os

if os.environ.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"):
    RUNTIME = "claude"
elif os.environ.get("CODEX") == "1":
    RUNTIME = "codex"
else:
    RUNTIME = "serial"
```

### 2. 统一 Agent 创建

根据检测到的环境，自动选择 agent 创建方式：

**Claude Code**: 使用 `Agent()` tool 并行创建
**Codex**: 使用 native subagents
**其他**: 串行执行

### 3. Task 执行

理解用户意图 → 确认关键信息 → 引用对应 task skill → 执行

## Task Skills

| 任务 | 说明 | 引用 |
|------|------|------|
| 同步通知 | 获取课程作业/公告，生成摘要 | `tasks/sync-notices.md` |
| 完成作业 | 解析→解答→渲染→询问→提交 | `tasks/do-homework.md` |
| 撰写笔记 | 从课件提取数学核心 | `tasks/write-notes.md` |

## Tool Skills

- `tools/pku3b-setup.md` - pku3b 配置
- `tools/data-parser.md` - 数据解析
- `tools/pdf-reader.md` - PDF读取
- `tools/agent-helpers.md` - Agent模板

## 踩坑记录

见 `ignore/archived-skill.md`

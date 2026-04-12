---
name: autopku
description: AutoPku - 自动获取PKU课程通知、完成作业、撰写笔记
---

# AutoPku

自动处理北京大学课程相关任务：同步通知、完成作业、撰写笔记。

## 前置配置

确保 `.claude/settings.local.json` 包含：

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

## 你能做的事

直接告诉我想做什么，例如：

- "帮我同步一下课程通知"
- "看看有哪些作业要交"
- "完成简明量子力学的第五次习题"
- "给逻辑导论写个笔记"
- "下载所有课程的附件"
- "检查一下哪些作业快到期了"

## 可用能力

| 能力 | 说明 | 引用 |
|------|------|------|
| **同步通知** | 获取所有课程作业/公告，生成摘要 | `tasks/sync-notices.md` |
| **完成作业** | 解析作业PDF→解答→渲染→询问→提交 | `tasks/do-homework.md` |
| **撰写笔记** | 从课件提取数学核心，去除噪声 | `tasks/write-notes.md` |

## 工具库

- `tools/pku3b-setup.md` - 教学网工具配置
- `tools/data-parser.md` - 数据解析
- `tools/pdf-reader.md` - PDF读取
- `tools/agent-helpers.md` - Agent模板
- `runtime/create-agent.md` - 统一Agent创建

## 执行原则

1. **理解意图** → 根据用户描述判断要做什么
2. **确认关键信息** → 用 AskUserQuestion 确认课程名、作业选择等
3. **引用对应 skill** → 调用相应的 task sub-skill
4. **自动适配环境** → Claude Code / Codex 自动检测

## 踩坑记录

见 `ignore/archived-skill.md`

关键提示：
- `pku3b init` 需 expect 脚本交互登录
- 部分课程用 Canvas/微信群，教学网无记录

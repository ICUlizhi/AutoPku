---
name: autopku
description: 自动获取和整理北京大学课程通知，完成作业并提交
---

## 上游说明

这个文件是仓库根目录 `skill.md` 的安装时参考副本，供 Codex 版 skill 在独立安装后继续读取领域规则和踩坑记录。

- Claude Code 主入口仍然是仓库根目录 `skill.md`
- Codex 主入口是 `codex/autopku/SKILL.md`

## Claude 特定提示

原始 `skill.md` 中包含 `.claude/settings.local.json`、`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 等 Claude Code 特定配置。

Codex 使用这个参考文件时：

- 把这些内容视为上游背景说明
- 不要把它们当成 Codex 的必需配置步骤
- 保留其中关于 `pku3b`、`expect`、课程抓取、作业解析、提交流程的领域知识

## 原始入口提示

> Claude Code 入口。
> 如果你使用 Codex，请改为读取 `codex/autopku/SKILL.md`。

其余具体执行细节，请优先参考仓库根目录 `skill.md` 的最新版本；如果当前是独立安装的 Codex skill，则以本目录安装副本和实际命令输出为准。

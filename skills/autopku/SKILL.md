---
name: autopku
description: AutoPku - 自动获取PKU课程通知、完成作业、撰写笔记
---

# AutoPku

自动处理北京大学课程相关任务：同步通知、完成作业、撰写笔记。

## 配置说明

### 全局配置（推荐）

**文件位置**: `~/.claude/settings.json`

```json
{
  "permissions": {
    "allow": ["Skill(update-config)", "Bash(*)"],
    "deny": ["Bash(rm:*)", "Bash(rm -rf:*)"],
    "defaultMode": "bypassPermissions"
  },
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "USER_TYPE": "ant"
  }
}
```

**Kimi Code CLI 用户**: 建议设置环境变量 `KIMI_CODE_CLI=1` 以启用 Kimi Agent Team 支持（或通过 `which kimi` 自动检测）。

### 本地配置（项目特定）

**文件位置**: `.claude/settings.local.json`（项目根目录）

内容同上，本地配置会覆盖全局配置。

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用 Agent Team 并行处理功能 |
| `USER_TYPE` | 用户类型标识（ant 为开发测试账号） |
| `permissions.allow` | 允许使用的工具 |
| `permissions.deny` | 禁止使用的工具（安全保护） |
| `defaultMode` | 默认权限模式 |

## 使用方式

直接告诉我要做什么：

| 用户意图示例 | 执行的任务 |
|-------------|-----------|
| "同步课程通知" / "看看有什么作业" | 同步所有课程通知和作业 |
| "完成量子力学的第五次作业" | 完成指定课程作业（解析→解答→渲染→询问→提交） |
| "给逻辑导论写笔记" | 从课件提取数学核心内容撰写笔记 |

## 执行架构

### 1. 环境检测

执行时自动检测运行环境：

```python
import os
import shutil

if os.environ.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"):
    RUNTIME = "claude"      # 使用 Agent() tool + SendMessage()
elif os.environ.get("CODEX") == "1":
    RUNTIME = "codex"       # 使用 native subagents
elif os.environ.get("KIMI_CODE_CLI") == "1" or os.environ.get("KIMI") == "1" or shutil.which("kimi"):
    RUNTIME = "kimi"        # 使用 Kimi Agent() + TaskList/TaskOutput
else:
    RUNTIME = "serial"      # 串行执行
```

### 2. 任务路由

根据用户意图，引用对应的 task skill：

```
用户: "同步课程通知"
  ↓
引用: sub-skills/tasks/sync-notices.md
  ↓
执行同步流程

用户: "完成作业"
  ↓
引用: sub-skills/tasks/do-homework.md
  ↓
执行作业流程（含用户确认）

用户: "写笔记"
  ↓
引用: sub-skills/tasks/write-notes.md
  ↓
执行笔记撰写流程
```

### 3. Agent 创建

主 skill 根据 RUNTIME 创建 agents：

```python
# Claude Code 环境
for config in agent_configs:
    Agent({
        "name": config["name"],
        "prompt": config["task"],
        "description": config.get("description", "")
    })

# Kimi Code CLI 环境
for config in agent_configs:
    Agent({
        "description": config.get("description", ""),
        "prompt": config["task"],
        "subagent_type": config.get("subagent_type", "coder")
    })

# Codex 环境
# 使用自然语言描述并行 subagent 任务

# 其他环境
# 串行执行
```

## 核心依赖: pku3b

### 安装

```bash
# 检查是否已安装
which pku3b 2>/dev/null || echo "NOT_FOUND"

# 未安装时执行（macOS Apple Silicon 示例）
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.11.0/pku3b-0.11.0-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.11.0-aarch64-apple-arm64.tar.gz
chmod +x pku3b-0.11.0-aarch64-apple-darwin/pku3b
ln -sf pku3b-0.11.0-aarch64-apple-darwin/pku3b pku3b
./pku3b --version
```

**重要**: 
- 正确仓库: `sshwy/pku3b` (原 `yang-er/pku3b` 已失效)
- 推荐版本: v0.11.0+ (支持公告 `ann` 和课表 `ct` 功能)

### 登录

使用 expect 脚本（TTY-safe）：

```bash
cat > /tmp/pku3b_login.exp << 'EOF'
#!/usr/bin/expect -f
set timeout 30
spawn /tmp/pku3b init
expect "username:"
send "学号\r"
expect "password:"
send "密码\r"
expect eof
EOF
chmod +x /tmp/pku3b_login.exp
/tmp/pku3b_login.exp
```

**踩坑**: 直接管道输入会报错 "input device is not a TTY"，必须使用 expect。

### 常用命令

```bash
# 作业
/tmp/pku3b a ls --all-term              # 所有学期作业（带ANSI颜色码）
/tmp/pku3b a download <ID> -d <dir>     # 下载附件
/tmp/pku3b a submit <ID> <file>         # 提交作业

# 公告 (v0.11.0+)
/tmp/pku3b ann ls                       # 列出公告
/tmp/pku3b ann show <ID>                # 查看公告详情

# 课表 (v0.11.0+)
/tmp/pku3b ct -r                        # 获取课表 JSON

# 选课
/tmp/pku3b s -d major show              # 主修课程（可能返回302，作为可选）
```

## Task Skills 索引

| Task | 文件 | 说明 |
|------|------|------|
| 同步通知 | `tasks/sync-notices.md` | 获取作业/公告，生成摘要，并行处理课程 |
| 完成作业 | `tasks/do-homework.md` | 解析PDF→解答→渲染→询问用户→提交 |
| 撰写笔记 | `tasks/write-notes.md` | 从课件提取数学核心，去除噪声 |

## Tool Skills 索引

| Tool | 文件 | 说明 |
|------|------|------|
| pku3b配置 | `tools/pku3b-setup.md` | 安装、登录、命令参考 |
| 数据解析 | `tools/data-parser.md` | ANSI颜色码处理、正则提取 |
| PDF读取 | `tools/pdf-reader.md` | PyMuPDF/pdfplumber 代码示例 |
| Agent模板 | `tools/agent-helpers.md` | Coordinator/Parser/Solver/Writer/Submitter Prompts |

## Runtime Skills 索引

| Runtime | 文件 | 说明 |
|---------|------|------|
| 环境检测 | `runtime/_detect.md` | 自动检测 Claude/Codex/Kimi/Fallback |
| Agent 创建 | `runtime/create-agent.md` | 统一的跨平台 Agent 创建接口 |
| Claude Team | `runtime/claude-team.md` | Claude Code Agent Team 语法 |
| Codex Subagent | `runtime/codex-subagent.md` | Codex native subagent 语法 |
| Kimi Team | `runtime/kimi-team.md` | Kimi Code CLI Agent Team 语法 |

## 关键踩坑记录

### 1. 课程筛选遗漏

**问题**: 选课系统显示"未选上"但作业系统有记录（如"学术英语写作"）。

**解决**: 从作业系统提取所有课程，对比选课系统，标注不一致状态。

### 2. 附件下载问题

| 情况 | 说明 | 示例 |
|------|------|------|
| 无附件 | 提交类作业无下载内容 | 操作系统（实验班）|
| 教学网无作业 | 使用Canvas/微信群 | 哲学导论、逻辑导论 |
| 体育课 | 通常无在线作业 | 太极拳 |

**检查**: `grep "课程名" /tmp/pku_assignments_raw.txt | grep "附件"`

### 3. 数据格式问题

- **无 `--json` 参数**: pku3b 输出纯文本带ANSI颜色码，需正则解析
- **`pku3b a ls -a` 不完整**: 只显示有作业的课程，需用 `pku3b s show` 补全
- **`--all-term` 返回所有历史学期**: 需筛选当前学期

### 4. 用户确认（重要）

完成作业前**必须**:
1. 列出所有待交作业
2. 使用 `AskUserQuestion` 让用户选择
3. 二次确认后才创建 Agent Team
4. 渲染完成后询问是否提交

**禁止**: 自动选择最新作业、未经确认直接提交

## 输出规范

### 同步通知输出

```
test/
├── 通知摘要汇总.md
├── {course1}/
│   ├── 作业/           # 下载的附件
│   ├── 通知/           # 公告详情
│   ├── 资料/           # 课程资料
│   └── 通知摘要.md     # 该课程摘要
└── {course2}/
    └── ...
```

### 完成作业输出

```
{course}/
├── 作业/
│   ├── Homework202605.pdf          # 原题
│   ├── homework_parsed.json        # 解析结果
│   ├── answers.json                # 解答数据
│   ├── Homework202605_answer.md    # Markdown答案
│   └── Homework202605_answer.pdf   # PDF答案
└── 提交/                           # 最终提交文件
    └── Homework202605_answer.pdf
```

## 安全规则

- 从不回显密码到日志
- 不自动提交作业（必须用户确认）
- 不自动选择作业（必须用户选择）
- 安全处理课程名中的特殊字符

## 参考

- 原完整 skill 备份: `archive/archived-skill.md`
- pku3b 仓库: https://github.com/sshwy/pku3b

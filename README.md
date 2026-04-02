# AutoPku

> 北大课程通知自动化管理系统 | PKU Course Notification Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 **Claude Code** + **pku3b** 的自动化课程通知管理方案，一键获取、分类、汇总教学网通知。

---

## 功能特性

- 🤖 **全自动获取**：定时从教学网拉取所有课程通知
- 📁 **智能分类**：自动按课程、类型（作业/通知/资料/考试）整理
- 📊 **可视报告**：生成任务看板、DDL统计、考试时间表
- 🔧 **易于扩展**：支持任意数量课程，配置简单
- 📝 **Markdown输出**：原生支持 Obsidian/Notion 等笔记软件

---

## 快速开始

### 1. 安装依赖

```bash
# 安装 pku3b（命令行教学网客户端）
# Windows:
irm https://github.com/yang-er/pku3b/raw/main/install.ps1 | iex

# macOS/Linux:
curl -fsSL https://github.com/yang-er/pku3b/raw/main/install.sh | sh

# 配置登录
pku3b auth login

# 安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

### 2. 克隆本仓库

```bash
git clone https://github.com/ICUlizhi/AutoPku.git
cd AutoPku
```

### 3. 配置课程

编辑 `config/courses.yaml`，添加你的课程：

```yaml
courses:
  - name: "量子力学"
    folder: "./量子力学"
    keywords: ["量子", "简明量子力学"]
  
  - name: "马原"  
    folder: "./马原"
    keywords: ["马原", "马克思主义基本原理"]
```

### 4. 运行自动化

```bash
claude
# 然后在 Claude Code 中：读取 skill.md 并执行
```

---

## 项目结构

```
AutoPku/
├── skill.md              # Agent 配置模板（核心）
├── config/
│   └── courses.yaml      # 课程配置
├── reports/              # 生成的报告
│   ├── dashboard.md      # 总览看板
│   ├── task-stack.md     # 任务栈
│   └── exam-timeline.md  # 考试时间表
├── courses/              # 课程文件夹（自动生成）
│   └── {课程名}/
│       ├── 作业/
│       ├── 通知/
│       ├── 资料/
│       └── 通知摘要.md
├── 公众号文章.md         # 微信公众号教程
└── README.md             # 本文件
```

---

## 使用教程

### 基础用法

```bash
# 进入项目目录
cd AutoPku

# 启动 Claude Code
claude

# 执行自动化（在 Claude Code 中输入）
读取 skill.md 并执行课程通知获取任务
```

### 定时自动运行

**macOS/Linux - crontab：**

```bash
# 每天早8点自动同步
0 8 * * * cd /path/to/AutoPku && claude run skill.md

# 每周日晚上生成周报
0 20 * * 0 cd /path/to/AutoPku && claude run reports/weekly.md
```

**Windows - 任务计划程序：**

1. 打开"任务计划程序"
2. 创建基本任务 → 设置每天触发
3. 操作：启动程序 `claude`，参数 `run skill.md`

---

## 配置说明

### 单 Agent 模式（推荐入门）

适合课程数量较少（1-5门）的场景，一个 Agent 处理所有课程。

编辑 `config/courses.yaml`：

```yaml
# 基础配置
team:
  name: "autopku"
  mode: "single"  # single 或 multi

# 课程列表
courses:
  - name: "课程显示名称"
    folder: "./课程文件夹名"  # 相对路径或绝对路径
    keywords:                 # 用于匹配教学网课程名
      - "关键词1"
      - "关键词2"
    color: "blue"             # 报告中的颜色标识
```

### 多 Agent Team 模式（高级）

适合课程数量多（5+门）或需要并行处理的场景。

```yaml
team:
  name: "course-notifiers"
  mode: "multi"

agents:
  - name: "quantum-agent"
    course: "简明量子力学"
    folder: "./量子力学"
    keywords: ["量子"]
    color: "cyan"
  
  - name: "thesis-agent"
    course: "毕业论文"
    folder: "./毕设"
    keywords: ["毕设", "毕业论文"]
    color: "purple"
```

启动命令：

```bash
# 创建 Team
claude team create course-notifiers

# 并行启动所有 Agents
for agent in config/agents/*.yaml; do
  claude agent create --team course-notifiers --config $agent &
done
```

---

## 高级功能

### 自定义分类规则

```yaml
classification:
  assignment:
    patterns: ["作业", "Assignment", "Homework"]
    folder: "作业"
  
  exam:
    patterns: ["考试", "测验", "Quiz", "Exam"]
    folder: "考试"
    priority: "high"  # 高优先级提醒
```

### Webhook 推送

```yaml
notifications:
  webhook:
    url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."
    events: ["新作业发布", "DDL提醒"]
  
  email:
    smtp: "smtp.pku.edu.cn"
    to: "your_email@pku.edu.cn"
```

### 与 Obsidian 集成

```bash
# 软链接报告到 Obsidian 仓库
ln -s $(pwd)/reports/dashboard.md ~/Obsidian/PKU/课程看板.md

# 或使用 Git 同步
```

---

## 故障排除

### pku3b 相关问题

```bash
# 检查登录状态
pku3b auth status

# 重新登录
pku3b auth logout
pku3b auth login

# 测试连接
pku3b assignment list
```

### Claude Code 权限问题

**macOS：**

1. 打开 "系统设置" → "隐私与安全性"
2. 找到"完全磁盘访问权限"
3. 添加 Terminal/iTerm2/Claude Code

**Windows：**

以管理员身份运行 PowerShell/CMD

### 课程匹配失败

1. 查看教学网原始课程名：
   ```bash
   pku3b assignment list
   ```

2. 在 `keywords` 中添加更多匹配词：
   ```yaml
   keywords: ["马原", "马克思主义", "马克思主义基本原理概论"]
   ```

---

## 相关项目

- [pku3b](https://github.com/yang-er/pku3b) - 命令行教学网客户端
- [Claude Code](https://github.com/anthropics/claude-code) - AI 编程助手

---

## 贡献指南

欢迎 Issue 和 PR！

1. Fork 本仓库
2. 创建 feature 分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -am 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 许可证

MIT License - 自由使用和修改

---

## 致谢

- [@yang-er](https://github.com/yang-er) - pku3b 开发者
- [Anthropic](https://www.anthropic.com/) - Claude Code
- 所有贡献者和使用者

---

*Happy Coding at PKU! 🎓*

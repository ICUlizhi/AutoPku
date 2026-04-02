# AutoPku - 北大课程通知自动管理

> 基于 Claude Code + pku3b 的自动化课程通知管理系统

## 概述

AutoPku 是一套用于自动从北京大学教学网(pku3b)拉取课程通知、分门别类整理到对应课程文件夹，并生成任务统计报告的自动化方案。

**核心特点**：
- 🤖 全自动：一键获取所有课程通知
- 📁 智能分类：自动按课程、类型整理文件
- 📊 可视报告：生成任务看板、DDL统计
- 🔧 易扩展：支持任意数量课程，配置简单

---

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  教学网API   │────▶│  pku3b CLI  │────▶│  AutoPku Agent  │
└─────────────┘     └─────────────┘     └─────────────────┘
                                                  │
                                                  ▼
                                        ┌─────────────────┐
                                        │  课程文件夹/      │
                                        │  ├── 作业/       │
                                        │  ├── 通知/       │
                                        │  ├── 资料/       │
                                        │  └── 通知摘要.md │
                                        └─────────────────┘
```

---

## 快速开始

### 1. 安装依赖

#### 安装 pku3b

```bash
# Windows (PowerShell)
irm https://github.com/yang-er/pku3b/raw/main/install.ps1 | iex

# macOS/Linux
curl -fsSL https://github.com/yang-er/pku3b/raw/main/install.sh | sh
```

#### 配置 pku3b

```bash
# 首次运行，按提示输入学号和密码
pku3b auth login

# 测试是否正常工作
pku3b assignment list
```

#### 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 配置方法

### 方法一：单 Agent 模式（推荐入门）

创建一个通用 Agent 处理所有课程：

```json
{
  "name": "autopku-agent",
  "description": "自动获取所有课程通知",
  "type": "general-purpose"
}
```

**Prompt 模板**：

```markdown
你是 AutoPku Agent，负责自动管理北京大学课程通知。

## 配置信息

**课程列表**（在配置文件中定义）：
```yaml
courses:
  - name: "课程名称"
    folder: "课程文件夹路径"
    keywords: ["匹配关键词1", "匹配关键词2"]
  # ... 更多课程
```

## 执行流程

1. **获取数据**
   ```bash
   pku3b assignment list --json
   ```

2. **解析与分类**
   - 遍历每个 assignment
   - 根据 course.keywords 匹配归属课程
   - 分类：作业/通知/资料/考试

3. **文件存储**
   在每个课程的 folder 下创建：
   ```
   {folder}/
   ├── 作业/          # 作业要求和附件
   ├── 通知/          # 一般通知
   ├── 资料/          # 课程资料
   └── 通知摘要.md     # 汇总报告
   ```

4. **生成报告**
   - 待完成任务列表（含DDL）
   - 逾期作业提醒
   - 考试时间表
   - 本周任务优先级排序

## 输出格式

每个课程生成 `通知摘要.md`：

```markdown
# {课程名称} - 通知摘要

## 统计概览
- 总通知数：X
- 待交作业：Y
- 本周截止：Z
- 考试安排：W

## 待完成作业（按优先级）

### 🔴 紧急（7天内截止）
- [ ] 作业名称 - 截止：YYYY-MM-DD

### 🟡 进行中（30天内截止）
- [ ] 作业名称 - 截止：YYYY-MM-DD

### 🟢 已发布（暂无DDL）
- [ ] 作业名称

## 考试安排
| 考试类型 | 日期 | 范围 |
|---------|------|------|
| 期中/期末 | YYYY-MM-DD | 章节X-Y |

## 最新通知

### YYYY-MM-DD 通知标题
内容摘要...

## 附件列表
- [文件名](链接)
```

## 汇总报告

同时生成 `reports/dashboard.md`：
- 所有课程任务总览
- 本周任务堆栈
- 考试时间表
```

---

### 方法二：多 Agent Team 模式（推荐高级用户）

为每门课程创建独立的 Agent，实现并行处理：

**配置结构**：

```yaml
# config/autopku.yaml
team:
  name: "course-notifiers"
  description: "PKU课程通知自动管理Team"

agents:
  - name: "course-agent-{course_id}"
    course: "课程名称"
    folder: "课程文件夹路径"
    keywords: ["匹配关键词"]
    color: "blue"  # 用于报告颜色标识

# 例如：
agents:
  - name: "maYuan-agent"
    course: "马克思主义基本原理"
    folder: "马原"
    keywords: ["马原", "马克思主义基本原理"]
    color: "blue"
  
  - name: "thesis-agent"
    course: "毕业论文"
    folder: "毕设"
    keywords: ["毕设", "毕业论文", "毕业设计"]
    color: "purple"
```

**启动命令**：

```bash
# 创建 Team
claude team create course-notifiers

# 为每个课程创建 Agent（并行）
for agent in config/agents/*.yaml; do
  claude agent create --team course-notifiers --config $agent &
done

# 广播执行任务
claude broadcast --team course-notifiers "执行通知获取任务"
```

---

## 高级配置

### 自定义分类规则

在配置文件中添加分类规则：

```yaml
classification:
  assignment:
    patterns: ["作业", "Assignment", "Homework"]
    folder: "作业"
  
  notification:
    patterns: ["通知", "公告", "Notice"]
    folder: "通知"
  
  material:
    patterns: ["资料", "课件", "PPT", "讲义"]
    folder: "资料"
  
  exam:
    patterns: ["考试", "测验", "Quiz", "Exam"]
    folder: "考试"
```

### 定时任务配置

使用系统定时任务自动运行：

```bash
# crontab -e

# 每天早8点自动同步
0 8 * * * cd /path/to/autopku && claude run skill.md

# 每周日晚上生成周报
0 20 * * 0 cd /path/to/autopku && claude run reports/weekly.md
```

### 通知推送（可选）

配置企业微信/钉钉/Webhook 推送：

```yaml
notifications:
  webhook:
    url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/..."
    events: ["新作业发布", "DDL提醒", "考试安排"]
  
  email:
    smtp: "smtp.pku.edu.cn"
    to: "your_email@pku.edu.cn"
    schedule: "daily"
```

---

## 文件结构

```
AutoPku/
├── skill.md              # 本文件 - Agent 配置模板
├── config/
│   ├── autopku.yaml      # 主配置文件
│   └── courses.yaml      # 课程列表
├── reports/
│   ├── dashboard.md      # 总览看板
│   ├── task-stack.md     # 任务栈
│   └── exam-timeline.md  # 考试时间表
├── scripts/
│   ├── init.sh           # 初始化脚本
│   └── sync.sh           # 手动同步脚本
├── courses/              # 课程文件夹（自动生成）
│   ├── 马原/
│   ├── 学术英语写作/
│   └── ...
└── README.md             # 项目说明
```

---

## 权限配置

Agents 运行时需要以下权限：

| 权限类型 | 说明 | 建议 |
|---------|------|------|
| Bash (pku3b) | 执行 pku3b 命令 | **允许** |
| Bash (mkdir/ls) | 创建目录和列出文件 | **允许** |
| Read/Write | 读写课程文件 | **允许** |
| Bash (rm -rf) | 删除文件/目录 | **手动确认** |

---

## 故障排除

### pku3b 无法运行

```bash
# 检查是否已登录
pku3b auth status

# 重新登录
pku3b auth login

# 检查版本
pku3b --version
```

### 课程匹配失败

- 检查 `keywords` 是否包含课程名称的所有可能变体
- 使用 `pku3b assignment list` 查看原始课程名
- 在配置中添加更多关键词

### 权限被拒绝

- 确保 Claude Code 有文件系统访问权限
- 检查课程文件夹是否可写
- macOS: 检查"完全磁盘访问权限"

---

## 扩展开发

### 添加新功能

1. **Fork 本仓库**
2. **创建 feature 分支**
3. **修改 skill.md 或添加脚本**
4. **提交 PR**

### 插件系统

支持自定义插件扩展功能：

```python
# plugins/custom_plugin.py
from autopku import Plugin

class MyPlugin(Plugin):
    def on_assignment_found(self, assignment):
        # 自定义处理逻辑
        pass
    
    def on_report_generated(self, report):
        # 自定义报告格式
        pass
```

---

## 相关链接

- **pku3b**: https://github.com/yang-er/pku3b
- **Claude Code**: https://github.com/anthropics/claude-code
- **AutoPku**: https://github.com/ICUlizhi/AutoPku

---

## 贡献者

- @ICUlizhi - 项目创建
- 欢迎提交 Issue 和 PR

---

## License

MIT License - 自由使用和修改

---

*Happy Coding at PKU! 🎓*

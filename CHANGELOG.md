# AutoPku 演进历程

> 从第一版单文件 skill 到模块化、多运行时、自然语言驱动的学业自动化系统

---

## 阶段一：原型搭建 (Initial Commit)

**Commit:** `1f5bd38`

- 项目初始化，包含一个庞大的 `skill.md`（398 行）
- 提供基础的课程自动化概念：同步通知、完成作业、写笔记
- 配置文件 `config/courses.yaml` 和目录结构 `courses/`、`reports/`
- 附赠一篇科幻隐喻文章《2010》

---

## 阶段二：Agent Team 化重构

**Commit:** `9d50bc5`

这是项目的第一次大重构，核心理念从"脚本自动化"转向 **Agent Team 协作**：

- **重写 `README.md`**：添加项目背景和《2010》科幻隐喻
- **大幅扩展 `skill.md`**：从 398 行膨胀到包含完整的 Agent Team Prompt 模板
- **新增作业完成全链路**：PDF 解析 → 解答 → 渲染 → 用户确认 → 提交
- **确立安全基线**：禁止自动选择作业、禁止未经确认直接提交
- 删除冗余配置文件，简化项目结构

---

## 阶段三：完善项目介绍

**Commits:** `c06740f`, `b1408a5`

- 更新 README 介绍文字
- 添加 4 张系统架构/使用流程截图到 `images/`
- 调整 README 篇幅，更聚焦核心功能

---

## 阶段四：跨平台支持 — Claude & Codex 双模式

**Commits:** `9588521` → `339049f` (PR #2)

- **约束**：macOS 默认文件系统大小写不敏感，根目录 `skill.md` 和 `SKILL.md` 无法共存
- **方案**：保留 Claude 入口 `skill.md`，新增 `codex/autopku/SKILL.md`
- 使 Codex skill 自包含（不依赖仓库根目录的相对链接）
- 验证 `pku3b` 本地行为：修正 `s -d major show` 不稳定（返回 302）的问题
- 最终合并 PR #2，仓库可同时服务 Claude Code 和 Codex 两个环境

---

## 阶段五：pku3b 工具链升级

**Commit:** `cc4114f`

- 将 `pku3b` 升级到 **v0.11.0**（原 `yang-er/pku3b` 已失效，切换到 `sshwy/pku3b`）
- **新增公告功能**：`pku3b ann ls/show`
- **新增课表功能**：`pku3b ct -r`
- 提供公告解析和课表转 iCalendar 的示例代码
- 更新 Agent Prompt 模板，在通知摘要中包含公告章节

---

## 阶段六：PDF 处理能力补强

**Commits:** `96b7e9a`, `9ccd42e`

- 在 `skill.md` 中添加 PyMuPDF / pdfplumber 快速参考
- 新建 `sub-skills/pdf-reader.md`（253 行），作为 Agent 读取 PDF 的工具手册

---

## 阶段七：架构大重构 — 模块化 sub-skills

**Commit:** `03b9475`

这是项目架构上最重要的一次演进，从**单体 skill** 拆分为**模块化 sub-skills**：

```
skill.md              # 简化为主入口 (~80 行)，负责任务路由
sub-skills/
├── runtime/          # AI 环境抽象层
│   ├── _detect.md    # 自动检测 Claude/Codex/其他环境
│   ├── claude-team.md
│   ├── codex-subagent.md
│   ├── create-agent.md  # 统一 agent 创建接口
│   └── kimi-team.md     # (后续添加)
├── tools/            # 可复用工具
│   ├── pku3b-setup.md
│   ├── data-parser.md
│   ├── pdf-reader.md
│   └── agent-helpers.md
└── tasks/            # 任务执行流
    ├── sync-notices.md
    └── do-homework.md
```

核心设计目标：
- **AI-agnostic**：自动检测运行时，适配不同的 agent 创建语法
- **用户确认**：`do-homework` 在提交前必须询问用户
- 原 skill 备份至 `ignore/archived-skill.md`

---

## 阶段八：笔记撰写任务

**Commit:** `b118918`

- 新增 `sub-skills/tasks/write-notes.md`
- 支持 `autopku notes <course>` 自然语言指令
- 聚焦数学核心内容：定义、定理、证明
- 去除噪声：历史背景、故事轶事、无关例子
- 生成带 LaTeX 公式和索引的 Markdown 笔记

---

## 阶段九：自然语言驱动简化

**Commits:** `3f75d67`, `e62b4ba`, `ae8aedb`, `fa80bb5`

这一阶段的核心目标是**让 AI 直接理解用户意图**，用户无需记忆固定命令：

- **移除 rigid command syntax**：用户可以说"帮我同步课程通知"、"完成量子力学作业"、"给逻辑导论写笔记"
- **简化 task skills**：`sync-notices.md`、`do-homework.md` 只提供 agent configs，主 skill 统一处理运行时检测和 agent 创建
- **重写 `skill.md`**：
  - 添加配置文件路径（全局 `~/.claude/settings.json` + 本地 `.claude/settings.local.json`）
  - 恢复 `USER_TYPE=ant` 环境变量
  - 整理所有关键踩坑记录
  - 强调安全规则（不自动提交、不回显密码）
  - 规范各任务的输出目录结构

---

## 阶段十：Kimi Code CLI 支持

**Commit:** `7cd5469`

- 新增 `sub-skills/runtime/kimi-team.md`，适配 Kimi Agent Team 语法
- 更新 `_detect.md`：通过 `KIMI_CODE_CLI`、`KIMI` 环境变量或 `which kimi` 识别 Kimi 环境
- 更新 `create-agent.md` 和 `agent-helpers.md`，加入 Kimi 并行策略
- `skill.md` 索引同步更新

---

## 阶段十一：PDF 渲染踩坑与 callout 修复

**Commit:** `d2c3996`

本次在真实课程（操作系统实验班）笔记生成中踩到多个坑，并同步更新 skill：

### 笔记生成修复 (`write-notes.md`)
- **重写 `callout.lua`**：
  - 通过 `tag_idx` + `SoftBreak` 精确定位 callout 的标题与正文边界，**解决正文丢失/重复的问题**
  - 增加 `escape_latex()`，**自动转义 `& $ % # _ ^ { } ~ \` 等特殊字符**，避免 tcolorbox title 注入报错
  - 将 emoji 图标（💡📝⚠️）替换为纯文字 `[TIP]`/`[NOTE]`/`[WARN]`/`[EX]`，解决 LaTeX 字体缺失问题
- **渲染参数优化**：增加 `-V mainfont="PingFang SC"` 和 `-V monofont="Menlo"`，解决 xelatex 中西文 Unicode 符号（`≠ μ` 等）缺失的 warning
- **新增"关键踩坑记录"小节**：汇总 6 条 PDF 渲染实战经验（callout 切分、LaTeX 转义、符号缺失、emoji 兼容性、lualatex 差异、mermaid 渲染限制）

### 作业流程增强 (`do-homework.md`)
- 新增**写作类作业字数检查**：对 Reflection、Essay、Annotated Bibliography 等类型，在定稿前使用脚本统计字数，确保符合要求后再渲染提交

---

## 演进主线总结

| 阶段 | 核心变化 |
|------|---------|
| **单体 skill** | 一个 `skill.md` 包罗万象 |
| **Agent Team 化** | 引入多 Agent 协作完成学业任务 |
| **双平台支持** | 同时支持 Claude Code 和 Codex |
| **模块化重构** | 拆分为 `runtime` / `tools` / `tasks` sub-skills |
| **自然语言驱动** | 用户无需记命令，直接说意图 |
| **多运行时支持** | 新增 Kimi Code CLI |
| **实战打磨** | 在真实课程中踩坑、修复、沉淀经验到 skill |

当前系统已支持：
- **3 大任务**：同步通知、完成作业、撰写笔记
- **3 大运行时**：Claude Code、Codex、Kimi Code CLI
- **完整的用户确认链**：特别是作业提交前必须二次确认
- **PDF/Markdown/Word/HTML 多格式输出**

---
name: autopku-task-write-notes
description: 读取课程slides，使用Agent Team撰写精简数学笔记，去除噪声内容
---

# 任务：撰写课程笔记

## 前置询问（必须）

在执行前，使用 `AskUserQuestion` 询问用户：

```python
AskUserQuestion({
    "questions": [
        {
            "question": "选择要撰写笔记的课件：",
            "options": [
                {"label": "全部课件", "value": "all"},
                {"label": "指定范围", "value": "range"}
            ],
            "multiSelect": False
        },
        {
            "question": "笔记详细程度：",
            "options": [
                {"label": "精简（只保留核心定义和定理）", "value": "minimal"},
                {"label": "标准（包含证明思路）", "value": "standard"},
                {"label": "详细（完整推导过程）", "value": "detailed"}
            ],
            "multiSelect": False
        },
        {
            "question": "额外要求（多选）：",
            "options": [
                {"label": "添加LaTeX公式编号", "value": "numbered_eq"},
                {"label": "添加概念之间的关联图", "value": "concept_map"},
                {"label": "添加例题（如有）", "value": "examples"},
                {"label": "生成Anki卡片", "value": "anki"}
            ],
            "multiSelect": True
        }
    ]
})
```

## 执行流程

1. **发现课件**: 扫描 `lectures/` 目录，列出所有 PDF
2. **用户确认**: 询问笔记范围和详细程度
3. **并行处理**: 为每个 PDF 创建 agent，引用 `pdf-reader` 解析
4. **汇总索引**: 生成 `notes/README.md` 索引文件
5. **渲染 PDF**: 将所有 md 合并渲染为单个 PDF（详见"PDF 渲染"一节）

## Agent 工作流

### Coordinator

```
你是 Coordinator，协调笔记撰写任务。

输入目录：{lectures_dir}
输出目录：{notes_dir}

任务列表：{pdf_list}

执行：
1. 为每个 PDF 并行创建 writer agent
2. 收集所有 agent 完成报告
3. 生成 notes/README.md 索引

返回：
- 处理了多少个 PDF
- 生成了多少个笔记文件
- 索引文件路径
```

### Writer Agent（每个 PDF 一个）

```
你是笔记撰写专家，从课件中提取数学核心内容。

输入：{pdf_path}
输出：{notes_dir}/{lecture_name}.md

## 引用工具
引用: `sub-skills/tools/pdf-reader.md`

使用 PyMuPDF 读取 PDF：
```python
import fitz
doc = fitz.open("{pdf_path}")
text = "\n\n".join([page.get_text() for page in doc])
doc.close()
```

## 内容筛选原则（重要）

### ✅ 保留内容
- **Motivation**: 为什么要研究这个问题？核心问题是什么？
- **定义**: 形式化定义、符号表示
- **定理/命题**: 精确陈述，编号
- **证明**: 关键证明步骤、核心技巧
- **结论**: 主要结果、推论
- **技术工具**: 关键引理、构造方法

### ❌ 去除内容
- **历史背景**: 谁发明的、发展历程
- **故事/轶事**: 麻雀、哲学家轶事等
- **日常用例**: 用自然语言解释的例子（除非是必要的直觉）
- **复杂无关概念**: 用更复杂的概念解释简单概念
- **重复性内容**: 多处出现的相同解释
- **装饰性语言**: "让我们来看看"、"有趣的是"等

### ❌ 写作反模式（严禁）
- **"不是X而是Y"句式**: 直接说Y是什么，不要绕弯。例如"真值不是客观事实，而是……" → 直接写"真值指……"
- **过度分段**: 能用一段话讲清楚的不要拆成多段，避免每句话一个段落
- **废话填充**: 不要用过渡句、总结句、重复换词说同一件事

## 笔记格式

```markdown
# {Lecture 标题}

> [!tip] 学习指南
> 本节核心：{一句话概括本节要解决什么问题}
> 前置知识：{需要哪些前面的概念}
> 重点关注：{考试/理解的关键点}

## 核心问题/Motivation
- 本节要解决的中心问题
- 与前文的关系（如有）

## 定义

### 定义 X.X （概念名）
**陈述**: 形式化定义

**符号**: $...$

> [!note] 直觉理解
> {用一两句话帮助建立直觉，适合第一次接触的学生}

## 定理与命题

### 定理 X.X （定理名）
**陈述**: 精确数学陈述

**证明**:
1. 关键步骤...
2. 核心技巧...
3. ...

> [!warning] 易错点
> {常见误解或易混淆之处，如有}

## 概念关系

用 mermaid 图展示本节概念之间的逻辑关系：

​```mermaid
graph TD
    A[概念A] --> B[概念B]
    B --> C[定理C]
​```

## 技术工具/引理

### 引理 X.X
...

## 结论
- 本节主要结果总结
- 关键公式/事实

> [!tip] 期中复习要点
> {本节最值得记住的1-3个结论}

## 记号速查
| 符号 | 含义 |
|-----|------|
| $...$ | ... |
```

### Callout 使用规范

在笔记中积极使用 Markdown callout 辅助理解：

| Callout 类型 | 用途 | 示例场景 |
|-------------|------|---------|
| `> [!tip] 学习指南` | 每节开头，概括重点和前置知识 | 帮助预习定位 |
| `> [!note] 直觉理解` | 定义/定理旁，建立直觉 | "可以类比为……" |
| `> [!warning] 易错点` | 常见误解、易混淆概念 | "注意X和Y的区别" |
| `> [!tip] 期中复习要点` | 每节结尾，总结必记结论 | 快速回顾用 |
| `> [!example] 例题` | 典型例题（如用户选择了"添加例题"） | 巩固理解 |

### Mermaid 图使用规范

在以下场景必须使用 mermaid 图，而非纯文字罗列：

- **概念依赖关系**: 定义之间的推导链、定理之间的蕴含关系
- **证明结构**: 较长证明的步骤流程
- **分类讨论**: 情况分支（用 `graph TD` 或 `flowchart`）
- **时间线/流程**: 构造过程的先后顺序

## 约束
- 笔记必须可渲染（标准 Markdown，含 callout 和 mermaid 语法）
- 数学公式使用 LaTeX（$...$ 行内，$$...$$ 行间）
- 保留原始课件的结构层次（章节编号）
- 如某节无数学内容（纯故事/历史），标注"本节为导言/背景，略"
- **写作风格**:
  - 行文紧凑，能合并为一段的不拆段
  - 禁用"不是X而是Y"句式，直接阐述Y
  - 不堆砌过渡词和重复性解释
  - 用 callout 提供学习指点（每节开头 `[!tip] 学习指南`，重要概念旁 `[!note]`/`[!warning]`）
  - 用 mermaid 图替代纯文字的关系描述和流程罗列
- **目标读者**: 预习或备考期中的大学生，侧重帮助快速建立理解框架

返回：
- 处理页数
- 提取的定义数、定理数
- 输出文件路径
- 备注（如有难以处理的内容）
```

## 输出文件

### 单个笔记文件
`notes/{lecture_name}.md`

### 主文档（渲染入口）
`notes/README.md`

README.md 是整份笔记的主文档，pandoc 渲染时以它为第一个输入文件，后接各讲 md 文件。README.md 自身包含封面信息、课程概览、概念图谱和术语表；各讲内容不要重复写入 README，而是由 pandoc 多文件输入自动拼接，pandoc 会从所有输入文件的标题中生成统一目录。

### 最终 PDF
`pdf/{课程名}课程笔记.pdf`

## PDF 渲染

笔记生成流程的最后一步自动执行。

### 核心思路

**README.md 作为主文档入口，pandoc 接收多个 md 文件按序渲染，自动生成目录。** 不要先合并成一个大 md 再渲染——直接传多文件给 pandoc。

### 步骤

1. **确认可用工具**（按优先级）：
   ```bash
   which pandoc 2>/dev/null && echo "pandoc OK"
   which typst 2>/dev/null && echo "typst OK"
   # 仅当用户明确要求 LaTeX 时：
   which xelatex 2>/dev/null && echo "xelatex OK"
   ```
   优先级：`pandoc` > `typst` > `xelatex`。

2. **创建输出目录和 lua filter**：
   ```bash
   mkdir -p pdf/
   ```
   生成 callout 渲染 filter（见下方 lua filter）。

3. **pandoc 多文件渲染**（推荐方案）：
   ```bash
   pandoc \
     notes/README.md \
     notes/lec01_*.md notes/lec02_*.md ... notes/lec13_*.md \
     -o pdf/{course_name}课程笔记.pdf \
     --pdf-engine=xelatex \
     -V CJKmainfont="PingFang SC" \
     -V mainfont="PingFang SC" \
     -V monofont="Menlo" \
     -V geometry:margin=2cm \
     -V documentclass=report \
     --toc --toc-depth=2 \
     --highlight-style=tango \
     --lua-filter=pdf/callout.lua \
     -V colorlinks=true \
     --top-level-division=chapter
   ```
   关键参数说明：
   - 第一个输入是 README.md（封面+概览），后续按文件名排序
   - `--toc` 自动从所有文件的标题生成目录
   - `--top-level-division=chapter` 让每个文件的 h1 成为章，自动分页
   - `-V documentclass=report` 支持 chapter 级别
   - `--lua-filter` 处理 callout 语法

4. **验证输出**：
   ```bash
   # 检查页数（macOS）
   mdls -name kMDItemNumberOfPages pdf/{course_name}课程笔记.pdf
   # 检查首页有文本
   strings pdf/{course_name}课程笔记.pdf | head -20
   ```
   页数必须 > 0，strings 输出必须包含实际文本。

### Callout Lua Filter

pandoc 原生不支持 `> [!tip]` 语法，需要 lua filter 转换：

```lua
-- pdf/callout.lua
-- 将 > [!tip] / [!note] / [!warning] / [!example] 转为带样式的 LaTeX 环境

local callout_config = {
  tip     = {color = "green!70!black",  icon = "[TIP]"},
  note    = {color = "blue!70!black",   icon = "[NOTE]"},
  warning = {color = "orange!80!black", icon = "[WARN]"},
  example = {color = "violet!70!black", icon = "[EX]"},
}

local function escape_latex(s)
  local r = s:gsub("\\", "\\textbackslash{}")
  r = r:gsub("([&%%#_$^{}~])", "\\%1")
  return r
end

function BlockQuote(el)
  local first = el.content[1]
  if not first or first.t ~= "Para" then return nil end

  local inlines = first.content
  if not inlines or #inlines == 0 then return nil end

  -- 精确定位 [!type] 标签位置
  local tag_idx = nil
  for i, inline in ipairs(inlines) do
    if inline.t == "Str" and inline.text:match("^%[! ?%w+ ?%]$") then
      tag_idx = i
      break
    end
  end
  if not tag_idx then return nil end

  local ctype = inlines[tag_idx].text:match("^%[! ?(%w+) ?%]$")
  if not ctype then return nil end
  ctype = ctype:lower()

  local cfg = callout_config[ctype]
  if not cfg then return nil end

  -- 标题：标签后到 SoftBreak/LineBreak 之前的内容
  local break_idx = nil
  for i = tag_idx + 1, #inlines do
    if inlines[i].t == "SoftBreak" or inlines[i].t == "LineBreak" then
      break_idx = i
      break
    end
  end

  local title_inlines = {}
  local body_inlines = {}

  if break_idx then
    for i = tag_idx + 1, break_idx - 1 do
      table.insert(title_inlines, inlines[i])
    end
    for i = break_idx + 1, #inlines do
      table.insert(body_inlines, inlines[i])
    end
  else
    for i = tag_idx + 1, #inlines do
      table.insert(title_inlines, inlines[i])
    end
  end

  local title = pandoc.utils.stringify(title_inlines)
  if not title or title == "" then title = ctype end

  local latex_begin = string.format(
    "\\begin{tcolorbox}[colback=%s!5!white, colframe=%s, left=2mm, right=2mm, top=1mm, bottom=1mm, boxrule=0.4mm, arc=1.5mm, title={%s %s}]",
    cfg.color, cfg.color, cfg.icon, escape_latex(title)
  )

  local result = {pandoc.RawBlock("latex", latex_begin)}

  if #body_inlines > 0 then
    table.insert(result, pandoc.Para(body_inlines))
  end

  for i = 2, #el.content do
    table.insert(result, el.content[i])
  end

  table.insert(result, pandoc.RawBlock("latex", "\\end{tcolorbox}"))
  return result
end
```

### Pandoc header-includes（自动注入）

渲染前在 README.md 的 YAML frontmatter 或通过 `-H` 参数注入 LaTeX 包：

```yaml
---
header-includes:
  - \usepackage[most]{tcolorbox}
  - \usepackage{fontspec}
---
```

或命令行：
```bash
echo '\usepackage[most]{tcolorbox}' > pdf/header.tex
pandoc ... -H pdf/header.tex
```

### Typst 替代方案

如果 typst 可用且用户偏好：
```bash
# 需要先将多个 md 转为 typst 格式
pandoc notes/README.md notes/lec*.md -o pdf/_combined.typ -t typst
typst compile pdf/_combined.typ pdf/{course_name}课程笔记.pdf
```

### 工具缺失时

```
缺少 PDF 渲染工具，推荐安装：
  brew install pandoc     # 通用，推荐
  brew install typst      # 轻量替代
笔记 md 文件已生成在 notes/，可手动渲染。
```

### 关键踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| **Callout 正文丢失或重复** | 旧 filter 把 `> [!note] 标题\n> 正文` 的第一整段全部当作 tcolorbox `title`，导致正文被吞或重复 | 在 Lua filter 中通过 `tag_idx` + `SoftBreak` 精确定位，切分 `title_inlines` 和 `body_inlines` |
| **tcolorbox title 编译报错（`Misplaced alignment tab character &`）** | callout 标题中含 `& $ % # _ ^ { } ~ \` 等特殊字符时，直接注入 LaTeX title 会报错 | 在 Lua filter 中增加 `escape_latex()` 函数，对 title 进行转义 |
| **xelatex 西文符号缺失（`≠ μ` 等 warning）** | xelatex 默认西文 fallback 到 Latin Modern，该字体不支持部分 Unicode 数学符号 | 增加 `-V mainfont="PingFang SC"`（或 Songti/Heiti），让西文也使用支持 Unicode 的系统字体 |
| **emoji 图标显示为空白方框** | tcolorbox title 中的 💡 📝 ⚠️ 等 emoji 在默认 LaTeX 字体中缺失 | 将 icon 替换为纯文字 `[TIP]` `[NOTE]` `[WARN]` `[EX]`，保证跨平台稳定 |
| **lualatex 无 warning，但 chapter 分页略有不同** | lualatex 字体回退更完善，但 `--top-level-division=chapter` 与 xelatex 的换页行为存在微小差异 | 追求零 warning 时用 lualatex；需要与历史输出完全一致时用 xelatex |
| **mermaid 图在 PDF 中无法渲染** | pandoc → LaTeX 和 typst 都不原生支持 mermaid 语法 | 当前保留为纯文本代码块；如需真正渲染，需额外使用 mermaid-cli 预先生成图片再插入 |

### README.md 模板

README.md 作为主文档入口，只写封面级内容，不重复各讲正文：

```markdown
---
title: "{课程名}课程笔记"
author: "AutoPku"
date: "{timestamp}"
header-includes:
  - \usepackage[most]{tcolorbox}
---

# 课程概览

{课程简介，2-3 句话}

# 知识图谱

```mermaid
graph TD
    ...
```

# 全局术语中英对照

| 中文 | English | 首次出现 |
|------|---------|---------|
| ... | ... | ... |
```

各讲内容通过 pandoc 多文件输入自动追加在 README 之后，目录自动生成。

## 使用示例

```bash
skill: autopku notes 逻辑导论
```

或在其他目录使用：

```bash
skill: autopku notes /path/to/lectures /path/to/notes
```

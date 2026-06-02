---
name: autopku-task-make-slides
description: 基于 pkusli 模板自动生成课程汇报/展示幻灯片（Typst PDF）
---

# 任务：生成幻灯片

基于 [pkusli](https://github.com/hanlife02/pkusli)（Typst + Touying 中文汇报模板）自动生成学术汇报幻灯片。

## 流程

```
Phase 1: 数据源检测与用户确认 → Phase 2: 内容提取 → Phase 3: 生成大纲 →
Phase 4: Agent Team 并行生成各页 → Phase 4.5: 图片获取（可选）→
Phase 5: 组装与渲染 → Phase 6: 用户确认
```

## Phase 1: 数据源检测与用户确认

### 1.1 自动检测可用数据源

扫描课程目录下的潜在内容源：

```python
import os
from pathlib import Path

course_dir = Path("{course}")
data_sources = []

# 检测课件
lectures_dir = course_dir / "lectures"
if lectures_dir.exists():
    pdfs = list(lectures_dir.glob("*.pdf"))
    if pdfs:
        data_sources.append({"type": "lectures", "path": str(lectures_dir), "count": len(pdfs)})

# 检测已有笔记
notes_dir = course_dir / "notes"
if notes_dir.exists():
    mds = list(notes_dir.glob("*.md"))
    if mds:
        data_sources.append({"type": "notes", "path": str(notes_dir), "count": len(mds)})

# 检测已有论文
paper_dir = course_dir / "论文"
if paper_dir.exists():
    tex_or_pdf = list(paper_dir.glob("*.tex")) + list(paper_dir.glob("*.pdf"))
    if tex_or_pdf:
        data_sources.append({"type": "paper", "path": str(paper_dir), "count": len(tex_or_pdf)})
```

### 1.2 AskUserQuestion 确认参数

```python
# 构建数据源选项
source_options = [{"label": "手动输入主题", "value": "manual"}]
for src in data_sources:
    label_map = {
        "lectures": f"课件 PDF（{src['count']} 个）",
        "notes": f"已有笔记（{src['count']} 个 md）",
        "paper": f"已有论文（{src['count']} 个文件）",
    }
    source_options.append({"label": label_map.get(src["type"], src["type"]), "value": src["type"]})

AskUserQuestion({
    "questions": [
        {
            "question": "幻灯片汇报主题：",
            "options": [
                {"label": f"使用课程名：{course} 课程汇报", "value": f"{course} 课程汇报"},
                {"label": "手动输入", "value": "custom"}
            ]
        },
        {
            "question": "选择内容来源：",
            "options": source_options
        },
        {
            "question": "目标页数：",
            "options": [
                {"label": "精简（8-12页）", "value": "short"},
                {"label": "标准（15-20页）", "value": "standard"},
                {"label": "详细（25-30页）", "value": "long"}
            ]
        },
        {
            "question": "额外需求（多选）：",
            "options": [
                {"label": "添加配图（自动搜索/生成）", "value": "images"},
                {"label": "包含参考文献页", "value": "references"},
                {"label": "添加动画效果（pause/uncover）", "value": "animation"}
            ],
            "multi_select": True
        }
    ]
})
```

若用户选择"手动输入主题"，继续追问获取具体主题和简要内容描述。

### 1.3 收集作者信息

```python
AskUserQuestion({
    "questions": [
        {
            "question": "确认作者信息：",
            "options": [
                {"label": "从配置读取（如可用）", "value": "config"},
                {"label": "手动输入", "value": "manual"}
            ]
        }
    ]
})
```

## Phase 2: 内容提取

根据用户选择的数据源提取关键内容。

### 数据源：课件 PDF

引用: `sub-skills/tools/pdf-reader.md`

```python
Agent({
    "description": f"{course} 课件内容提取",
    "prompt": f"""
你是内容提炼专家。从 {course} 的课件 PDF 中提取适合制作汇报幻灯片的核心内容。

课件目录：{course}/lectures/

要求：
1. 使用 PyMuPDF 读取所有 PDF 的文本内容
2. 提炼每份课件的核心知识点（定义、定理、方法、结论）
3. 去除故事/轶事/历史背景等噪声（参考 write-notes 的内容筛选原则）
4. 保留 MOTIVATION：为什么要研究这个问题？
5. 保留关键公式（使用 LaTeX 格式）
6. 保留重要图表的描述（文字描述即可，图片后续单独处理）

输出格式：
```markdown
## 课件 {n}: {标题}
- 核心主题：...
- 关键知识点：
  1. ...
  2. ...
- 重要公式：...
- 结论：...
```

返回：提炼后的结构化内容文本。
"""
})
```

### 数据源：已有笔记

```python
Agent({
    "description": f"{course} 笔记内容提取",
    "prompt": f"""
你是内容提炼专家。从 {course} 的已有笔记中提取适合制作汇报幻灯片的核心内容。

笔记目录：{course}/notes/

要求：
1. 读取所有 .md 文件
2. 提取核心定义、定理、结论
3. 保留概念之间的关系描述
4. 去除学习指南、复习要点、callout 等辅助性内容
5. 将 mermaid 图的关系转换为文字描述

输出：结构化的核心内容摘要。
"""
})
```

### 数据源：已有论文

```python
Agent({
    "description": f"{course} 论文内容提取",
    "prompt": f"""
你是内容提炼专家。从 {course} 的课程论文中提取适合制作答辩/汇报幻灯片的核心内容。

论文目录：{course}/论文/

要求：
1. 提取论文的核心论点、方法、实验结果
2. 保留研究背景和动机
3. 保留关键数据和结论
4. 将长段落压缩为 bullet points

输出：结构化的论文核心内容摘要。
"""
})
```

### 数据源：手动输入

跳过此阶段，直接使用用户在 Phase 1 中提供的内容描述。

## Phase 3: 生成幻灯片大纲

创建大纲生成 Agent：

```python
Agent({
    "description": f"{course} 幻灯片大纲生成",
    "prompt": f"""
你是幻灯片设计专家，为北京大学{course}课程的汇报设计幻灯片大纲。

汇报主题：{title}
目标页数：{page_target}（short=8-12页, standard=15-20页, long=25-30页）
数据来源摘要：
{extracted_content}

设计要求：
1. 设计 3-6 个章节（大模块）
2. 每个章节下设计若干页面（遵循目标页数）
3. 为每页指定页面类型（见下方类型指南）
4. 为每页写出：标题、核心要点（3-5条 bullet points）、配图需求（如有）
5. 页面内容必须来源于上方摘要，不要编造不存在的内容
6. 封面页和结束页计入总页数

页面类型指南（严格使用这些函数名）：
| 类型 | 函数 | 适用场景 |
|------|------|---------|
| 封面 | cover-page | 标题、作者、单位、日期 |
| 目录 | agenda-page | 展示章节结构，3-6项 |
| 过渡页 | transition-page | 大章节切换，带序号和描述 |
| 纯文字要点 | subject-content-page | 列表形式的核心内容，含 top-content 一句话结论 |
| 图文混排 | subject-text-image-page | 左侧文字+右侧图片，适合展示架构/流程 |
| 三图对比 | subject-triple-gallery-page | 三个图并列，适合实验结果对比 |
| 参考文献 | references-manual-page | 列出参考文献 |
| 结束页 | end-page | 致谢 |

输出格式（Markdown）：
```markdown
# 幻灯片大纲：{title}

## 第1页：封面
- 类型：cover-page
- 内容：标题、作者、单位、日期

## 第2页：目录
- 类型：agenda-page
- sections: ["01 / 章节1", "02 / 章节2", ...]

## 第3页：章节过渡
- 类型：transition-page
- number: "01"
- title: "章节1标题"
- description: "一句话描述本章内容"

## 第4页：内容页
- 类型：subject-content-page
- title: "页面标题"
- top-content: "一句话结论"
- content: ["要点1", "要点2", "要点3"]
- 配图需求：无 / 需要XX类型配图

...
```

注意：
- 纯文字页（subject-content-page）应占主体（约 60%）
- 图文页（subject-text-image-page）用于展示关键架构/流程（约 20%）
- 过渡页每个大章节一个（约 10%）
- 封面+目录+结束页固定 3 页
"""
})
```

保存大纲：`{course}/slides/outline.md`

## Phase 4: Agent Team 并行生成各页

解析大纲，按章节分组创建并行 Agent。引用: `sub-skills/runtime/create-agent.md`

```python
# 按章节分组
sections = parse_outline(outline_md)  # 从 outline.md 解析

agent_configs = []
for i, section in enumerate(sections):
    agent_configs.append({
        "name": f"{course}-slides-section-{i}",
        "task": f"""
你是幻灯片内容生成专家。请为以下章节生成 pkusli 模板的 Typst 页面调用代码。

汇报主题：{title}
当前章节：{section['title']}
章节页面列表：
{section['pages']}

原始内容摘要（供参考，不要编造不存在的内容）：
{extracted_content}

## 输出要求

输出纯 Typst 代码（不需要 import/show 语句，只需要页面调用序列）。

可用的页面函数（必须严格使用这些函数名和参数）：

### cover-page（仅封面页使用）
```typst
#cover-page(
  title: report-title,
  subtitle: [副标题],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
```

### agenda-page（仅目录页使用）
```typst
#agenda-page(
  sections: (
    [01 / 章节1],
    [02 / 章节2],
    [03 / 章节3],
  ),
)
```

### transition-page（章节过渡页）
```typst
#transition-page(
  number: [01],
  title: [章节标题],
  description: [一句话描述本章核心内容],
)
```

### subject-content-page（纯文字要点页 — 最常用）
```typst
#subject-content-page(
  title: [页面标题],
  header-left-offset: 10em,
  top-content: [一句话结论：...],
  content: [
    - 要点一
    - 要点二
    - 要点三
  ],
)
```

### subject-text-image-page（图文混排页）
```typst
#subject-text-image-page(
  "figures/图片文件名.png",
  title: [页面标题],
  header-left-offset: 10em,
  top-content: [一句话结论：...],
  image-caption: [图 X. 图片说明。],
  text-body: [
    - 左侧文字要点一
    - 左侧文字要点二
  ],
  swap-sides: false,  // true 则图片在左文字在右
)
```

### subject-triple-gallery-page（三图对比页）
```typst
#subject-triple-gallery-page(
  title: [页面标题],
  header-left-offset: 10em,
  image-one: "figures/图1.png",
  image-one-caption: [图 A],
  image-two: "figures/图2.png",
  image-two-caption: [图 B],
  image-three: "figures/图3.png",
  image-three-caption: [图 C],
  text-body: [总结说明文字...],
)
```

### references-manual-page（参考文献页）
```typst
#references-manual-page(
  entries: (
    [作者. 标题. 出版社, 年份.],
    [作者. 标题. 期刊, 年份.],
  ),
)
```

### end-page（结束页）
```typst
#end-page(
  title: [谢谢聆听],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
```

## 内容规范

1. 每页的 `top-content` 必须是一句话结论，概括该页核心信息
2. `content` 和 `text-body` 中使用列表形式，每页 3-5 个要点
3. 数学公式使用 Typst 语法：`$x^2 + y^2 = z^2$`（行内），`$ ... $`（行间）
4. 中文内容直接写，不需要额外转义
5. 图片路径统一使用 `"figures/xxx.png"` 格式（图片后续会放到该目录）
6. 如果某页需要配图但图片尚未生成，先写占位路径 `"figures/placeholder.png"`
7. 不要输出任何解释文字，只输出 typst 代码

## 动画（如用户选择了 animation）

如需添加动画，使用 Touying 提供的语法：
- `#pause` — 暂停，点击后显示后续内容
- `#uncover("2-")["内容"]` — 从第 2 步开始显示
- `#only("1")["内容"]` — 仅在第 1 步显示

注意：不要过度使用动画，每页最多 1-2 处。

返回：该章节所有页面的完整 typst 代码。
"""
    })
```

等待所有 Agent 完成后，按章节顺序拼接 `pages_code`。

> **Kimi 环境注意**: Kimi Agent 结果直接返回，按顺序收集各 Agent 的 typst 代码输出。

## Phase 4.5: 图片获取（可选）

扫描 `pages_code` 中引用的图片路径，判断哪些需要生成/搜索：

```python
import re

# 提取所有图片引用
img_refs = re.findall(r'"figures/([^"]+)"', pages_code)
needed_images = [img for img in img_refs if img != "background.png" and img != "placeholder.png"]

if needed_images:
    # 引用 tools/image-handler.md
    for img_name in needed_images:
        Agent({
            "description": f"生成幻灯片配图 {img_name}",
            "prompt": f"""
引用 skill: autopku-tool-image-handler
图片类型：根据大纲判断（数据图表 / 框架图 / 流程图 / 网络图片 / 示意图）
输出路径：{course}/slides/figures/{img_name}

注意：
1. 图片用于幻灯片展示，建议分辨率不低于 300 DPI
2. 配色简洁，适合投影展示（避免浅色文字）
3. 中文标签字体清晰
4. 保存为 PNG 格式
"""
        })
```

对于 `placeholder.png`，替换为 `background.png`（模板自带的占位图）：

```python
pages_code = pages_code.replace('"figures/placeholder.png"', '"figures/background.png"')
```

## Phase 5: 组装与渲染

引用: `sub-skills/tools/slide-renderer.md`

```python
# 组装参数
render_params = {
    "course": course,
    "title": title,
    "subtitle": subtitle or "",
    "author": author,
    "institution": institution,
    "date": date,
    "pages_code": pages_code,
}

# 调用 slide-renderer
Agent({
    "description": f"{course} 幻灯片渲染",
    "prompt": f"""
引用 skill: autopku-tool-slide-renderer

参数：
- course: {course}
- title: {title}
- subtitle: {subtitle or ''}
- author: {author}
- institution: {institution}
- date: {date}
- pages_code: |
{pages_code}

执行步骤：
1. 获取 pkusli 模板（git clone 缓存）
2. 复制到 {course}/slides/
3. 确保 figures/ 目录存在，将已生成的图片复制到 {course}/slides/figures/
4. 组装 main.typ
5. typst compile main.typ slides.pdf
6. 验证输出
"""
})
```

## Phase 6: 用户确认

渲染完成后询问用户：

```python
AskUserQuestion({
    "questions": [
        {
            "question": "幻灯片已生成，是否需要修改？",
            "options": [
                {"label": "无需修改，直接完成", "value": "done"},
                {"label": "修改某页内容", "value": "edit_content"},
                {"label": "调整页面结构（增删页面）", "value": "edit_structure"},
                {"label": "补充图片/配图", "value": "add_images"}
            ]
        }
    ]
})
```

若用户选择修改，定位到具体页面，使用 Agent 重新生成该页代码，然后重新渲染。

## 输出规范

```
{course}/
└── slides/
    ├── main.typ              # Typst 源文件
    ├── slides.pdf            # 最终 PDF
    ├── outline.md            # 幻灯片大纲
    ├── figures/              # 图片目录
    │   ├── background.png    # 模板占位图（来自模板）
    │   └── ...               # 生成的配图
    └── references.bib        # BibTeX 参考文献（如使用自动引用）
```

## 关键踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| Agent 生成非法 typst 语法 | Agent 不熟悉 Touying 函数签名 | 在 prompt 中提供完整的函数签名示例，要求严格遵循 |
| 数学公式显示异常 | 使用了 LaTeX 语法而非 Typst 语法 | Typst 公式：`$x^2$` 而非 `$$x^2$$`；行间用 `#math.equation` 或块级 `$...$` |
| 图片路径错误 | Agent 使用了绝对路径或错误相对路径 | 强制要求 `"figures/xxx.png"` 格式 |
| 内容过多导致一页放不下 | Agent 没有控制内容量 | 在 prompt 中强调每页 3-5 个要点，超出则拆分为多页 |
| 中文标点显示异常 | 使用了全角标点但字体 fallback 不完整 | 通常不影响；若有问题可统一使用半角标点 |
| 编译后页数与目标差距大 | 大纲规划或 Agent 生成阶段未控制 | 在大纲 Agent prompt 中明确目标页数约束 |
| 模板更新后接口变化 | pkusli 仓库更新了函数签名 | slide-renderer 中 `git pull` 会自动获取最新模板；如接口变更需更新 skill |
| typst 首次编译下载 Touying 包慢 | 需要从 Typst Universe 下载依赖 | 正常现象，约 10-30 秒；缓存后后续编译快 |

## 与现有 Task 的协作

| 场景 | 使用方式 |
|------|---------|
| 从课件生成汇报 slides | `skill: autopku slides {course}` 或 "给{course}做个汇报PPT" |
| 基于已有笔记生成 slides | 先执行 `write-notes`，再执行 `make-slides`，数据源选"已有笔记" |
| 基于论文生成答辩 slides | 先执行 `write-paper`，再执行 `make-slides`，数据源选"已有论文" |
| 纯手动主题 | 数据源选"手动输入"，Agent 会基于通用知识生成 |

## 使用示例

```bash
skill: autopku slides 逻辑导论
skill: autopku 给学术英语写作做个汇报PPT
skill: autopku make-slides 马原
```

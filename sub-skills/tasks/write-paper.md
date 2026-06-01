---
name: autopku-task-write-paper
description: 生成PKU课程论文（LaTeX/Word），从大纲到正文到编译输出
---

# 任务：撰写课程论文

## 流程

```
Phase 1: 获取要求 → Phase 2: 用户确认 → Phase 3: 生成大纲 →
Phase 4: 生成正文 → Phase 4.5: 图片获取与绘制 → Phase 5: 渲染输出 → 询问用户
```

## 步骤

### 1. 获取论文要求

扫描课程目录下的 `通知/` 和 `资料/`，查找包含以下关键词的文件：
- "课程论文"、"期末论文"、"term paper"、"essay"
- "论文题目"、"选题"、"写作要求"
- "字数"、"字"、"不少于"
- "格式"、"模板"、"提交方式"

提取信息：
- 论文题目（或选题范围）
- 字数要求
- 格式要求（LaTeX / Word / PDF）
- 截止日期
- 特殊要求（是否需要参考文献、图表等）

### 2. 用户确认

使用 `AskUserQuestion` 确认写作参数：

```python
AskUserQuestion({
    "questions": [
        {
            "question": "请确认论文题目：",
            "options": [
                {"label": f"使用通知中的题目：{detected_title}", "value": detected_title},
                {"label": "手动输入", "value": "custom"}
            ]
        },
        {
            "question": "选择输出格式：",
            "options": [
                {"label": "LaTeX（推荐，支持图表公式）", "value": "latex"},
                {"label": "Word（.docx，简单通用）", "value": "word"}
            ]
        },
        {
            "question": "目标字数：",
            "options": [
                {"label": "3000字左右", "value": "3000"},
                {"label": "5000字左右", "value": "5000"},
                {"label": "8000字左右", "value": "8000"},
                {"label": "自定义", "value": "custom"}
            ]
        }
    ]
})
```

若用户选择自定义题目或字数，继续追问获取具体值。

### 3. 生成论文大纲

创建 Agent 生成论文大纲：

```python
Agent({
    "description": f"生成{course}论文大纲",
    "prompt": f"""
你是学术写作助手，为北京大学{course}课程生成论文大纲。

论文题目：{title}
目标字数：{word_count}字
课程性质：{course_type}

要求：
1. 设计合理的章节结构（含引言、3-4个主体章节、结论）
2. 每个章节写出简要的内容要点（100字左右）
3. 标出每个章节的预估字数分配
4. 提供5-8条参考文献建议（含作者、书名/文章名、出版社/期刊、年份）
5. 如果课程是人文社科类，注意理论深度和文献引用；如果是理工类，注意逻辑推导和数据分析
6. **图片规划**：判断论文是否需要配图（数据图表、框架图、流程图、案例图片），若需要则列出每张图的编号、标题、类型、内容描述和插入位置

输出格式：
- 使用 Markdown 格式
- 章节标题用 ## 和 ###
- 参考文献用 [1]、[2] 编号
"""
})
```

### 4. 生成正文（Agent Team 并行）

根据大纲，为每个章节创建独立 Agent 并行生成正文：

```python
agent_configs = []
for i, section in enumerate(sections):
    agent_configs.append({
        "name": f"{course}-paper-section-{i}",
        "task": f"""
你是学术写作助手，负责撰写北京大学{course}课程论文的以下章节：

论文题目：{title}
当前章节：{section['title']}
内容要点：{section['points']}
目标字数：{section['words']}字
章节编号：{section['number']}

写作要求：
1. 直接输出 LaTeX 格式的正文（使用 \\section{{}}、\\subsection{{}} 等命令）
2. 中文段落之间用空行分隔
3. 引用格式使用脚注或文内标注，如"（毛泽东，1991）"
4. 语言风格：学术规范、逻辑清晰、论证充分
5. 不要输出任何解释性文字，只输出 LaTeX 正文代码
6. 不要包含 \\begin{{document}} 或 \\end{{document}}
"""
    })
```

等待所有 Agent 完成后，按章节顺序拼接正文。

> **Word 模式**：Agent 生成纯文本/Markdown 格式正文，后续用 python-docx 渲染。

### 4.5 图片获取与绘制（可选）

若大纲中规划了配图，引用 `tools/image-handler.md` 执行：

```python
# 图片规划结果来自 Phase 3 的大纲 Agent
images = outline.get("images", [])

if images:
    for img in images:
        Agent({
            "description": f"生成图片 {img['id']}",
            "prompt": f"""
引用 skill: autopku-tool-image-handler
图片类型：{img['type']}  # 数据图表 / 框架图 / 流程图 / 网络图片
图片标题：{img['title']}
内容描述：{img['description']}
输出路径：{course}/论文/figures/{img['id']}.png
"""
        })
```

图片处理完成后，将对应的 LaTeX 插入代码（`\begin{figure}...\end{figure}`）嵌入到各章节正文的对应位置。

> 人文社科类课程论文通常 1-3 张图即可；若论文要求未提及配图，此阶段可跳过。

### 5. 渲染输出

#### LaTeX 模式

1. **获取模板**（从 `source` 分支通过 git worktree）：

   ```bash
   # 在 AutoPku 仓库根目录执行
   git worktree add /tmp/pku-paper-template source
   # 读取模板
   cp /tmp/pku-paper-template/pkucourse_paper_template/main.tex {course}/论文/template.tex
   cp -r /tmp/pku-paper-template/pkucourse_paper_template/figures {course}/论文/
   # 清理 worktree
   git worktree remove /tmp/pku-paper-template
   ```

   > 也可用 `git show source:pkucourse_paper_template/main.tex` 直接读取单文件，但 worktree 更方便批量复制 figures。

2. **替换占位符**：
   - `在此填写题目` → 论文题目
   - `在此填写页眉（可以是论文题目）` → 论文题目
   - `在此填写姓名` → 从配置或用户输入获取
   - `在此填写学号` → 从配置或用户输入获取
   - `在此填写院系` → 从配置或用户输入获取
   - `在此填写摘要内容` → Agent 生成的摘要（200-300字）
3. **插入正文**：将生成的各章节 LaTeX 代码（含图片插入代码）插入到 `\tableofcontents` 之后、`\section{结论}` 之前
4. **插入参考文献**：将大纲中的参考文献转换为 `\section*{参考文献}` 下的列表格式
5. **图片检查**：确认 `figures/` 目录下所有引用的图片文件存在，且格式为 PNG/JPG/PDF
5. **保存文件**：`{course}/论文/paper.tex`
6. **编译 PDF**：

   ```bash
   # 检测 xelatex
   which xelatex || echo "NOT_FOUND"

   # 编译（需执行两次以生成目录）
   cd {course}/论文
   xelatex -interaction=nonstopmode paper.tex
   xelatex -interaction=nonstopmode paper.tex
   ```

**编译踩坑**：
- 若提示字体缺失，检查系统是否安装了宋体/黑体（macOS 通常自带）
- 若 `figures/pku.pdf` 缺失，确认 worktree 已正确复制
- 若中文显示为方框，确保使用 `ctexart` 文档类且编译器为 xelatex

#### Word 模式

使用 python-docx 生成：

```python
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()
style = doc.styles['Normal']
style.font.name = '宋体'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 标题
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title_p.add_run(title)
run.font.name = '黑体'
run.font.size = Pt(16)
run.bold = True
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

# 作者信息
author_p = doc.add_paragraph()
author_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = author_p.add_run(f"姓名：{name}    学号：{student_id}    院系：{department}")
run.font.name = '楷体'
run.font.size = Pt(12)
run._element.rPr.rFonts.set(qn('w:eastAsia'), '楷体')

# 摘要
doc.add_paragraph()
abs_title = doc.add_paragraph()
abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = abs_title.add_run("摘  要")
run.font.name = '黑体'
run.font.size = Pt(14)
run.bold = True
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

abs_p = doc.add_paragraph()
abs_p.paragraph_format.first_line_indent = Cm(0.74)
abs_p.paragraph_format.line_spacing = 1.5
run = abs_p.add_run(abstract_text)
run.font.name = '宋体'
run.font.size = Pt(12)
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 正文各章节
for section in sections:
    # 一级标题
    h1_p = doc.add_paragraph()
    h1_p.paragraph_format.line_spacing = 1.5
    h1_p.paragraph_format.space_before = Pt(12)
    run = h1_p.add_run(section['title'])
    run.font.name = '黑体'
    run.font.size = Pt(14)
    run.bold = True
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    # 段落
    for para in section['content'].split('\n\n'):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0.74)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(para.strip())
        run.font.name = '宋体'
        run.font.size = Pt(12)
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 参考文献
doc.add_paragraph()
ref_title = doc.add_paragraph()
ref_title.paragraph_format.line_spacing = 1.5
run = ref_title.add_run("参考文献")
run.font.name = '黑体'
run.font.size = Pt(14)
run.bold = True
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(ref)
    run.font.name = '宋体'
    run.font.size = Pt(10.5)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.save(f'{course}/论文/paper.docx')

# 修改文档属性，去除 python-docx 生成痕迹
from datetime import datetime, timezone
props = doc.core_properties
props.author = name                    # 设置为学生姓名
props.last_modified_by = name
props.title = title                    # 设置为论文题目
props.subject = f'{course}课程论文'
props.comments = ''                    # 清空备注（默认为 "generated by python-docx"）
props.created = datetime.now(timezone.utc)
props.modified = datetime.now(timezone.utc)
doc.save(f'{course}/论文/paper.docx')
```

### 6. 输出与用户确认

输出规范：

```
{course}/
└── 论文/
    ├── paper.tex              # LaTeX 源文件（仅 LaTeX 模式）
    ├── paper.pdf              # 最终 PDF
    ├── paper.docx             # Word 文件（仅 Word 模式）
    ├── outline.md             # 论文大纲
    └── figures/               # 图片目录
        ├── pku.pdf            # 校徽（来自模板）
        ├── fig1.png           # 生成的配图（若有）
        └── fig2.png           # 生成的配图（若有）
```

渲染完成后询问用户：
- "论文已生成，是否需要修改某章节内容？"
- "是否需要调整格式或补充参考文献？"

**禁止**：未经用户确认自动提交论文到任何平台。

## 关键踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| xelatex 未安装 | 系统缺少 TeX Live / MacTeX | 提示用户安装，或回退到 Word 模式 |
| 中文字体显示异常 | Latin Modern 不支持中文 | 使用 `ctexart` + xelatex，已内置中文字体配置 |
| LaTeX 特殊字符报错 | `% $ & # _ { } ~ ^ \` 未转义 | Agent 生成内容时避免裸特殊字符，或用 `\verb` 包裹 |
| 图片路径错误 | `figures/` 相对路径不对 | 确保编译工作目录与 tex 文件同级，且 `figures/` 存在 |
| 图片未显示 | 使用了不支持的格式 | 转换为 PNG 或 PDF 格式 |
| matplotlib 中文乱码 | 系统字体缺失 | 尝试 `Arial Unicode MS`、`SimHei`、`PingFang SC` |
| graphviz 未安装 | 无 `dot` 命令 | `brew install graphviz` 或退化为 matplotlib 绘制 |
| 目录未生成 | 只编译了一次 xelatex | 需编译两次以生成 `toc` 文件 |
| Word 中公式显示差 | python-docx 不支持 LaTeX 公式 | 简单公式用纯文本，复杂公式建议用 LaTeX 模式 |
| Word 文档属性暴露生成方式 | python-docx 默认作者为 "python-docx" | 生成后修改 core_properties，将 author 设为学生姓名 |

## 使用示例

```bash
skill: autopku write-paper 马原
skill: autopku 写论文 学术英语写作
skill: autopku paper 逻辑导论
```

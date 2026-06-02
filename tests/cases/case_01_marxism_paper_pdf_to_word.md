# 真实案例 #1：马原论文 PDF → Word 转换

> **来源**: Kimi Session `5f91876922590e8cef7197ec2eb3d1a2` / Turn `60ae75ed-bd2b-491a-a50f-327b7c084abc`
> **时间**: 2026-05-15
> **涉及功能**: `write-paper`（Word 模式）、PDF 读取

---

## 用户原始输入

```
课程论文-12-徐靖-知行合一从《实践论》
  看认识与实践的辩证统一及其当代价值.pdf 你看看这个是怎么被渲染的，来一个word版本
```

## Agent 思考过程

1. **意图识别**: 用户想把一个已生成的 PDF 论文转换成 Word 版本
2. **文件定位**: 用 `find` 命令在 `./马原/` 下找到 PDF 文件
3. **依赖准备**: 安装 `python-docx` 和 `pymupdf`
4. **文本提取**: 用 PyMuPDF (`fitz`) 逐页提取 PDF 文本（共 349 行）
5. **Word 生成**: 编写 Python 脚本，用 `python-docx` 创建格式化的 Word 文档

## 关键工具调用序列

```
TurnBegin: "...来一个word版本"
  ↓
Step 1: Shell(find) → 定位到 ./马原/课程论文-12-徐靖-知行合一...pdf
  ↓
Step 2: Shell(pip install python-docx pymupdf) + Shell(python3 -c "import fitz; ...")
  ↓
Step 3: Shell(python3 -c "...提取完整文本到 /tmp/pdf_text.txt") → 349 行
  ↓
Step 4: ReadFile(/tmp/pdf_text.txt) → 获取完整文本内容
  ↓
Step 5: WriteFile(/tmp/gen_docx.py) → 生成 32072 字节的 Python 脚本
  ↓
Step 6: Shell(python3 /tmp/gen_docx.py) → 生成 Word 文档
```

## 提取的 PDF 内容片段（第 1 页）

```
知行合一：从《实践论》看认识与实践的辩证统一及其当代价值
姓名徐靖
学号2200012917
院系信息科学技术学院

摘 要
毛泽东的《实践论》是马克思主义认识论中国化的经典文献，系统阐述了实践在认识
过程中的基础地位与决定性作用，揭示了认识运动"实践—认识—再实践—再认识"的
辩证发展规律。...
```

## 生成的 Word 脚本核心逻辑

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_run_font(run, font_name='宋体', size=Pt(12), bold=False):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = size
    run.font.bold = bold

# 标题
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('知行合一：从《实践论》看认识与实践的辩证统一及其当代价值')
set_run_font(run, '黑体', Pt(22), bold=True)

# 作者信息
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run('姓名：徐靖\t\t学号：2200012917\t\t院系：信息科学技术学院')
set_run_font(run, '宋体', Pt(12))
```

## 踩坑与经验

1. **PDF 文本提取顺序**: PyMuPDF 按阅读顺序提取，但目录页的页码和标题会交错，需要后处理
2. **中文字体设置**: 必须用 `run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')` 才能正确设置中文字体
3. **页眉页脚**: PDF 中的页眉页脚被提取为正文内容，需要过滤
4. **图片丢失**: PDF 中的图片无法直接转换，只能保留图片标注文字

## 测试价值

此案例可用于验证：
- `write-paper` 的 Word 模式是否能正确生成格式化文档
- PDF → Word 的转换质量（文本完整性、格式保留度）
- 中文字体是否正确设置

---
name: autopku-tool-slide-renderer
description: 基于 pkusli 模板生成 Typst 幻灯片并编译为 PDF
---

# 工具：幻灯片渲染器

负责获取 pkusli 模板、组装 `main.typ`、编译输出 PDF。供 `make-slides` 任务 skill 在 Phase 5 调用。

## 依赖

- `git` — 克隆模板仓库
- `typst` — 编译 `.typ` 为 PDF
- `bash` / `cp` — 文件操作

## 模板获取

使用缓存机制，避免每次重复 clone：

```bash
TEMPLATE_DIR="$HOME/.autopku/templates/pkusli"
COURSE_SLIDES_DIR="{course}/slides"

# 1. 确保模板缓存存在且最新
if [ ! -d "$TEMPLATE_DIR/.git" ]; then
    echo "首次下载 pkusli 模板..."
    mkdir -p "$HOME/.autopku/templates"
    git clone --depth 1 https://github.com/hanlife02/pkusli.git "$TEMPLATE_DIR"
else
    echo "更新 pkusli 模板..."
    cd "$TEMPLATE_DIR" && git pull --depth 1
fi

# 2. 复制到课程工作目录
mkdir -p "$COURSE_SLIDES_DIR"
cp -r "$TEMPLATE_DIR"/* "$COURSE_SLIDES_DIR/"
rm -f "$COURSE_SLIDES_DIR/main.pdf"  # 清除示例 PDF
```

> **踩坑**: 模板仓库未发布到 Typst Universe，必须以 git clone 方式获取。使用 `--depth 1` 减少下载量。

## main.typ 组装

### 输入参数

| 参数 | 说明 |
|------|------|
| `title` | 汇报标题 |
| `subtitle` | 副标题（可选） |
| `author` | 作者姓名 |
| `institution` | 单位/院系 |
| `date` | 日期（如 `2026-06-02`） |
| `pages_code` | Agent 生成的页面调用代码（typst 语法） |
| `output_dir` | 输出目录，默认 `{course}/slides/` |

### 组装逻辑

直接生成完整的 `main.typ` 文件，覆盖模板自带的示例：

```python
main_typ_content = f'''#import "style/index.typ": presentation-theme
#import "slides/index.typ": (
  agenda-page, cover-page, end-page, references-manual-page,
  subject-content-page, subject-text-image-page,
  subject-triple-gallery-page, transition-page,
)

#let report-title = [{title}]
#let report-author = [{author}]
#let report-institution = [{institution}]
#let report-date = [{date}]
#let demo-image = "figures/background.png"

#show: presentation-theme

{pages_code}
'''

with open(f"{output_dir}/main.typ", "w", encoding="utf-8") as f:
    f.write(main_typ_content)
```

> **注意**: `pages_code` 中必须包含完整的页面调用序列，从 `#cover-page(...)` 开始到 `#end-page(...)` 结束。不需要包含 import 和 show 语句，因为骨架已经提供了。

### 示例 pages_code

```typst
// 封面
#cover-page(
  title: report-title,
  subtitle: [{subtitle}],
  author: report-author,
  institution: report-institution,
  date: report-date,
)

// 目录
#agenda-page(
  sections: (
    [01 / 研究背景],
    [02 / 方法设计],
    [03 / 实验结果],
  ),
)

// 过渡页
#transition-page(
  number: [01],
  title: [研究背景],
  description: [介绍问题定义与研究动机。],
)

// 正文页
#subject-content-page(
  title: [问题定义],
  header-left-offset: 10em,
  top-content: [一句话结论：现有方法在 X 场景下存在不足。],
  content: [
    - 挑战一：数据稀缺
    - 挑战二：标注成本高
    - 挑战三：泛化能力弱
  ],
)

// 图文页
#subject-text-image-page(
  "figures/arch.png",
  title: [系统架构],
  header-left-offset: 10em,
  top-content: [一句话结论：三层架构实现端到端优化。],
  image-caption: [图 1. 系统架构示意图。],
  text-body: [
    - 输入层：多模态特征提取
    - 中间层：注意力机制融合
    - 输出层：联合预测头
  ],
)

// 三图页
#subject-triple-gallery-page(
  title: [实验结果],
  header-left-offset: 10em,
  image-one: "figures/result1.png",
  image-one-caption: [数据集 A],
  image-two: "figures/result2.png",
  image-two-caption: [数据集 B],
  image-three: "figures/result3.png",
  image-three-caption: [数据集 C],
  text-body: [在三组数据集上均取得 SOTA 结果...],
)

// 参考文献（手动）
#references-manual-page(
  entries: (
    [Touying package documentation. Typst Universe.],
    [Typst documentation. Typst 官方文档.],
  ),
)

// 结束页
#end-page(
  title: [谢谢聆听],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
```

## 图片插入代码（Typst 语法）

在 `pages_code` 中插入图片时，使用 Typst 原生语法：

```typst
#figure(
  image("figures/fig1.png", width: 60%),
  caption: [图1. 系统架构示意图],
) <fig1>
```

对于 `subject-text-image-page` 和 `subject-triple-gallery-page`，直接传图片路径字符串即可，模板内部会处理插入：

```typst
#subject-text-image-page(
  "figures/arch.png",   // ← 直接传路径
  title: [...],
  ...
)
```

## 编译

```bash
cd "{course}/slides"

# 检查 typst
which typst 2>/dev/null || echo "TYPST_NOT_FOUND"

# 编译
typst compile main.typ slides.pdf

# 验证输出
if [ -f "slides.pdf" ]; then
    ls -lh slides.pdf
    echo "编译成功"
else
    echo "编译失败"
fi
```

### 编译参数（可选）

```bash
# 指定字体路径（若系统字体不在默认搜索路径）
typst compile main.typ slides.pdf --font-path /Library/Fonts/

# 指定输出目录
typst compile main.typ --root . ../slides.pdf
```

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| `typst: command not found` | 未安装 typst | `brew install typst` (macOS) 或从官网下载 |
| 中文显示为方框/ tofu | 缺少 Songti SC / STSong 字体 | macOS 通常自带；Linux 需安装 `fonts-noto-cjk` |
| `error: unknown variable` | Agent 生成了未 import 的函数 | 检查 `pages_code` 中使用的函数是否在 import 列表中 |
| 图片未显示 | 路径错误或图片不存在 | 确保图片在 `figures/` 目录且路径为相对 `main.typ` |
| Touying 包下载慢/失败 | 网络问题，Typst Universe 连接超时 | 检查网络；typst 首次编译会自动缓存包到 `~/.cache/typst/packages/` |
| `error: file not found` | `style/` 或 `slides/` 目录缺失 | 确认模板已完整复制到课程目录 |
| 编译后 PDF 空白页 | `pages_code` 为空或语法错误 | 检查 `main.typ` 中页面调用代码是否完整 |
| 西文数学符号缺失 | 字体 fallback 不完整 | 不影响编译，typst 会自动 fallback；若追求完美可安装 Latin Modern Math |

## 验证输出

```bash
cd "{course}/slides"

# 1. PDF 存在且非空
[ -s "slides.pdf" ] && echo "PDF 文件正常" || echo "PDF 为空或不存在"

# 2. 页数检查（macOS）
mdls -name kMDItemNumberOfPages slides.pdf

# 3. 文本检查
strings slides.pdf | head -20

# 4. 文件大小（应 > 10KB）
stat -f%z slides.pdf
```

## 使用示例

```bash
# 在 make-slides 流程中自动调用
skill: autopku slide-renderer

# 参数示例
# title="多模态评测框架设计"
# author="张三"
# institution="北京大学"
# date="2026-06-02"
# pages_code="...Agent 生成的 typst 页面代码..."
```

## 模板结构说明

复制到课程目录后的结构：

```
{course}/slides/
├── main.typ              # ← 由本工具生成/覆盖
├── slides.pdf            # ← 编译输出
├── style/                # ← 来自模板（不修改）
│   ├── index.typ
│   ├── presentation-theme.typ
│   └── ...
├── slides/               # ← 来自模板（不修改）
│   ├── index.typ
│   ├── cover/
│   ├── subject/
│   └── ...
├── figures/              # ← 图片目录（由 make-slides 填充）
│   └── ...
└── references.bib        # ← 可选，自动生成参考文献时使用
```

> **重要**: 不要修改 `style/` 和 `slides/` 目录下的文件。如需定制主题，应在 `make-slides` 任务中通过参数调整，而非直接改模板源码。

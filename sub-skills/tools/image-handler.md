---
name: autopku-tool-image-handler
description: 论文配图的智能搜索、生成与插入
---

# 工具：论文图片处理

为 PKU 课程论文自动获取或生成配图，支持网络图片搜索、数据图表绘制、框架图/流程图生成，并输出标准 LaTeX 插入代码。

## 使用场景

- 论文需要概念示意图、逻辑框架图、数据可视化图表
- 课程论文要求"图文并茂"或包含数据分析图表
- 为增强论证说服力，需要补充现实案例图片

## 图片类型与处理策略

| 类型 | 说明 | 处理方式 |
|------|------|----------|
| **数据图表** | 柱状图、折线图、饼图、热力图等 | Python matplotlib / seaborn 绘制 |
| **框架/流程图** | 概念模型、逻辑框架、流程图 | graphviz / matplotlib + networkx |
| **网络图片** | 现实案例照片、历史图片、截图等 | Web 搜索 + 下载 |
| **示意图** | 抽象概念可视化 | Python 绘制或 ASCII + 截图 |

## 流程

### 1. 图片规划

在论文大纲生成后，根据内容判断是否需要配图：

```python
# 判断条件
needs_images = any([
    "数据" in section_content,
    "趋势" in section_content,
    "对比" in section_content,
    "框架" in section_content,
    "流程" in section_content,
    "案例" in section_content,
    论文要求中明确提到"图表"、"图片"、"figures"
])
```

若需要配图，创建图片规划 Agent：

```python
Agent({
    "description": f"{course}论文图片规划",
    "prompt": f"""
你是学术配图规划助手。论文题目：{title}

论文大纲：
{outline}

请规划论文需要的配图，对每张图输出：
1. 图片编号（fig1, fig2...）
2. 图片标题
3. 图片类型（数据图表/框架图/流程图/网络图片/示意图）
4. 内容描述（详细说明图中应包含什么元素）
5. 建议尺寸（如 0.6\\textwidth）
6. 插入位置（对应章节）

注意：
- 人文社科类论文通常 1-3 张图即可，不宜过多
- 优先选择能直接增强论证的图（如数据对比、逻辑框架）
- 避免无意义的装饰性图片
- 网络图片必须确保版权合规（优先使用公开数据、新闻图片、政府发布素材）

输出 Markdown 列表格式。
"""
})
```

### 2. 图片获取与生成（并行 Agent）

对每张规划好的图片，创建独立 Agent 并行处理：

#### 类型 A：数据图表（Python matplotlib）

```python
Agent({
    "description": f"绘制{fig_id}数据图表",
    "prompt": f"""
你是数据可视化专家。请用 Python matplotlib 绘制以下图表：

图片标题：{fig_title}
内容描述：{fig_description}
输出路径：{course}/论文/figures/{fig_id}.png

要求：
1. 使用 matplotlib 中文支持（macOS 通常自带字体，可尝试 'Arial Unicode MS' 或 'SimHei'）
2. 图片分辨率不低于 300 DPI
3. 配色简洁专业，避免花哨
4. 必须有清晰的标题、坐标轴标签、图例
5. 保存为 PNG 格式
6. 如果涉及真实数据，可用合理估计值或公开数据源（需注明数据来源）

输出要求：
- 先输出完整的 Python 代码
- 然后执行代码生成图片
- 最后报告图片是否成功生成

若字体报错，尝试以下方案：
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
```
"""
})
```

#### 类型 B：框架/流程图（graphviz）

```python
Agent({
    "description": f"绘制{fig_id}框架图",
    "prompt": f"""
你是技术制图专家。请用 graphviz 绘制以下框架/流程图：

图片标题：{fig_title}
内容描述：{fig_description}
输出路径：{course}/论文/figures/{fig_id}.png

要求：
1. 使用 graphviz DOT 语言编写
2. 节点样式统一，字体清晰
3. 布局合理，避免交叉线过多
4. 输出为 PNG 格式（通过 dot 命令或 Python graphviz 包）

执行方案：
```bash
which dot || echo "GRAPHVIZ_NOT_FOUND"
# 若未安装，使用 pip install graphviz + brew install graphviz
```

若系统无 graphviz，退化为 Python matplotlib + patches 绘制简单框图。
"""
})
```

#### 类型 C：网络图片搜索与下载

```python
Agent({
    "description": f"搜索{fig_id}网络图片",
    "prompt": f"""
你是学术资料搜集助手。请为论文搜索并下载合适的配图。

图片标题：{fig_title}
内容描述：{fig_description}
输出路径：{course}/论文/figures/{fig_id}.png

流程：
1. 使用 SearchWeb 搜索相关图片资源
   - 搜索词应包含论文主题关键词 + "图片/数据/统计"
   - 优先搜索政府网站、学术机构、权威媒体的公开素材
2. 使用 FetchURL 访问候选图片页面，获取图片 URL
3. 使用 curl 下载图片到指定路径
4. 检查图片质量（分辨率、清晰度）

版权合规要求：
- 优先使用 Creative Commons 许可或公有领域图片
- 新闻图片、政府发布数据图通常可合理使用
- 若来源明确，在图注中标注来源
- 避免直接下载受版权保护的摄影/艺术作品

最终输出：
- 图片文件路径
- 图片来源 URL
- 建议的 LaTeX 图注（包含来源说明）
"""
})
```

### 3. LaTeX 图片插入代码生成

所有图片生成后，统一生成 LaTeX 插入代码：

```python
def generate_latex_figure(fig_id, caption, label, width="0.7\\textwidth", source=None):
    source_note = f"\\footnotesize 数据来源：{source}" if source else ""
    return f"""
\\\\begin{{figure}}[h]
    \\\\centering
    \\\\includegraphics[width={width}]{{figures/{fig_id}.png}}
    \\\\caption{{{caption}}}
    \\\\label{{{label}}}
    {source_note}
\\\\end{{figure}}
"""
```

将生成的 LaTeX 代码按插入位置分发给各章节 Agent，或集中插入到 paper.tex 的对应位置。

### 4. 图片质量检查

在最终编译前执行：

```bash
# 检查 figures 目录
cd {course}/论文/figures
ls -la

# 检查图片尺寸（至少 600px 宽）
file *.png *.jpg 2>/dev/null

# 若图片缺失，标记并在编译时跳过
```

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| matplotlib 中文乱码 | 系统缺少中文字体 | 尝试 'Arial Unicode MS'、'SimHei'、'PingFang SC' |
| graphviz 未安装 | 系统无 dot 命令 | `brew install graphviz` 或退化为 matplotlib 绘制 |
| 网络图片下载失败 | URL 防盗链或格式问题 | 尝试 wget --user-agent，或换源搜索 |
| 图片在 LaTeX 中过大/过小 | scale 参数不当 | 使用 `width=0.6\\textwidth` 等相对尺寸 |
| PNG 在 xelatex 中模糊 | 分辨率不足 | 生成时设置 dpi=300 以上 |
| 图片版权风险 | 使用了受保护素材 | 优先搜索政府/学术公开数据，图注标注来源 |

## 使用示例

```bash
# 在 write-paper 流程中自动调用
skill: autopku image-handler 马原
# 或论文完成后单独补充图片
skill: autopku 给论文加一张数据图
```

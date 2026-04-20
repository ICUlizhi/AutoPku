# DOCX Reader Skill

读取Word文档(.docx)的Python工具，支持文本提取、表格读取和隐藏文字安全检测。用于防御Prompt注入攻击（通过颜色、透明度或vanish属性隐藏的文字）。

## 安装依赖

```bash
pip install python-docx
```

## 快速开始

### 方法1: 文本提取

Word 文档由 **paragraphs（段落）** 组成，每个 paragraph 包含若干 **runs（文字片段）**。使用 `python-docx` 的 `Document(path)` 打开，遍历 `doc.paragraphs` 读取 `para.text`，再按需要拆分 `para.runs` 分析格式属性。

### 方法2: 表格提取

Word 表格通过 `doc.tables` 访问。每个 table 包含 rows，每行包含 cells，每个 cell 内部又有 paragraphs。遍历 `table.rows → row.cells → cell.text` 提取内容。

### 方法3: 隐藏文字安全检测（反Prompt注入）

聚焦检测Word中通过**颜色**（与背景同色）、**透明度**（极低不透明度）或**vanish属性**隐藏的文本。

**核心检测**：

- **颜色异常**（`color_mismatch`）：文本颜色与背景色相同或极接近
- **透明度异常**（`alpha_anomaly`）：`w14:alpha` 透明度极高（>80%）
- **vanish隐藏**（`vanish_hidden`）：Word原生隐藏文字属性

```python
from docx import Document
from docx.oxml.ns import qn


W14_NS = 'http://schemas.microsoft.com/office/word/2010/wordml'


def scan_docx_hidden_text(docx_path, color_threshold=0.08, alpha_threshold=80000):
    """扫描Word隐藏文字：颜色 + 透明度 + vanish检测"""
    alerts = []
    doc = Document(docx_path)
    bg_rgb = _get_docx_bg_color(doc)

    for pi, para in enumerate(doc.paragraphs):
        for run in para.runs:
            text = run.text.strip()
            if not text:
                continue

            run_rgb = _get_run_color(run)
            if run_rgb and _color_distance(run_rgb, bg_rgb) < color_threshold:
                alerts.append({"para": pi + 1, "text": text,
                    "type": "color_mismatch", "details": "文本颜色与背景色过于接近"})
                continue

            alpha = _get_run_alpha(run)
            if alpha is not None and alpha > alpha_threshold:
                transparency_pct = round(alpha / 1000, 1)
                alerts.append({"para": pi + 1, "text": text,
                    "type": "alpha_anomaly", "details": f"透明度极高({transparency_pct}%)"})
                continue

            if _is_vanish(run):
                alerts.append({"para": pi + 1, "text": text,
                    "type": "vanish_hidden", "details": "Word隐藏文字属性(vanish)"})

    return alerts


def _get_run_color(run):
    """获取run的RGB颜色，auto/None返回None"""
    color = run.font.color
    if color is None or color.rgb is None:
        return None
    rgb = color.rgb
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def _get_run_alpha(run):
    """获取run的w14不透明度(alpha)，范围0-100000；None表示未设置"""
    rPr = run._element.find(qn('w:rPr'))
    if rPr is None:
        return None
    textFill = rPr.find(f'{{{W14_NS}}}textFill')
    if textFill is None:
        return None
    solidFill = textFill.find(f'{{{W14_NS}}}solidFill')
    if solidFill is None:
        return None
    for tag in ['srgbClr', 'schemeClr']:
        clr = solidFill.find(f'{{{W14_NS}}}{tag}')
        if clr is not None:
            alpha_el = clr.find(f'{{{W14_NS}}}alpha')
            if alpha_el is not None:
                return int(alpha_el.get(f'{{{W14_NS}}}val'))
    return None


def _get_docx_bg_color(doc):
    """获取文档背景色，默认白色"""
    try:
        return (1.0, 1.0, 1.0)
    except Exception:
        return (1.0, 1.0, 1.0)


def _is_vanish(run):
    """检查run是否有Word vanish隐藏属性"""
    rPr = run._element.find(qn('w:rPr'))
    if rPr is None:
        return False
    return rPr.find(qn('w:vanish')) is not None


def _color_distance(rgb1, rgb2):
    if rgb1 is None or rgb2 is None:
        return float('inf')
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5
```

## 注意事项

1. **不要用 `open()` 读取 `.docx`**：`.docx` 是 ZIP 压缩的 XML 包，直接用 `open()` 会得到二进制乱码。必须用 `python-docx` 的 `Document(path)`。
2. **背景色默认白色**：Word 页面背景色可通过 XML 自定义，但 `python-docx` 不支持读取。若文档使用深色背景，颜色检测可能误报，此时需手动指定背景色。
3. **vanish 属性**：Word 的"隐藏文字"功能（字体设置 → 效果 → 隐藏）会设置 `<w:vanish>` 标签，打印和屏幕显示时均不可见，但 `python-docx` 会正常读到。
4. **颜色为 auto**：`run.font.color.rgb` 为 `None` 时表示"自动"（通常为黑色），不作为隐藏文字处理。

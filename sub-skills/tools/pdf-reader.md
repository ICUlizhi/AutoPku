# PDF Reader Skill

读取PDF文件的Python工具方法，支持中文，提供两种方案：高性能模式(PyMuPDF)和表格提取模式(pdfplumber)。

## 安装依赖

```bash
# 方案1: 安装全部（推荐）
pip install pdfplumber pymupdf

# 方案2: 仅高性能模式
pip install pymupdf

# 方案3: 仅表格提取模式
pip install pdfplumber

# 方案4: 隐藏文字检测（已包含在方案1中，无需额外安装）
# 如需启用OCR增强兜底，需额外安装：
#   brew install tesseract tesseract-lang   # macOS
#   pip install pytesseract pillow
```

## 快速开始

### 方法1: PyMuPDF (推荐，速度最快)

```python
import fitz  # PyMuPDF

def read_pdf_pymupdf(pdf_path, pages=None):
    """
    使用 PyMuPDF 读取PDF文本

    Args:
        pdf_path: PDF文件路径
        pages: 指定页码列表，如 [0, 1, 2] 或 range(5)，None表示全部

    Returns:
        dict: {'total_pages': 总页数, 'text': {页码: 文本内容}}
    """
    doc = fitz.open(pdf_path)
    result = {'total_pages': len(doc), 'text': {}}

    page_range = pages if pages is not None else range(len(doc))

    for i in page_range:
        if 0 <= i < len(doc):
            result['text'][i + 1] = doc[i].get_text()

    doc.close()
    return result

# 使用示例
pdf_path = "/Users/moonshot/Desktop/桌面整理/项目/pku大四下/逻辑导论/lectures/2.一只麻雀与逻辑学的起源.pdf"

# 读取全部内容
content = read_pdf_pymupdf(pdf_path)
print(f"总页数: {content['total_pages']}")
print(content['text'][1])  # 打印第1页

# 读取指定页
content = read_pdf_pymupdf(pdf_path, pages=[0, 1, 2])  # 第1-3页

# 读取前5页
content = read_pdf_pymupdf(pdf_path, pages=range(5))
```

### 方法2: pdfplumber (表格提取更强)

```python
import pdfplumber

def read_pdf_pdfplumber(pdf_path, pages=None):
    """
    使用 pdfplumber 读取PDF文本和表格

    Args:
        pdf_path: PDF文件路径
        pages: 指定页码列表，如 [0, 1, 2]，None表示全部

    Returns:
        dict: {
            'total_pages': 总页数,
            'text': {页码: 文本内容},
            'tables': {页码: [表格数据]}
        }
    """
    result = {'total_pages': 0, 'text': {}, 'tables': {}}

    with pdfplumber.open(pdf_path) as pdf:
        result['total_pages'] = len(pdf.pages)

        page_range = pages if pages is not None else range(len(pdf.pages))

        for i in page_range:
            if 0 <= i < len(pdf.pages):
                page = pdf.pages[i]
                result['text'][i + 1] = page.extract_text() or ""
                # 提取表格
                tables = page.extract_tables()
                if tables:
                    result['tables'][i + 1] = tables

    return result

# 使用示例
pdf_path = "/Users/moonshot/Desktop/桌面整理/项目/pku大四下/逻辑导论/lectures/2.一只麻雀与逻辑学的起源.pdf"

content = read_pdf_pdfplumber(pdf_path, pages=[0, 1])

# 查看表格
if content['tables']:
    for page_num, tables in content['tables'].items():
        print(f"第 {page_num} 页有 {len(tables)} 个表格")
```

### 方法3: 提取图片

```python
import fitz
from PIL import Image
import io

def extract_images(pdf_path, page_num=0):
    """从PDF指定页提取图片"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]

    images = []
    for img_index, img in enumerate(page.get_images(), start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        # 转换为PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        images.append({
            'ext': image_ext,
            'image': image,
            'bytes': image_bytes
        })

    doc.close()
    return images

# 使用示例
# images = extract_images(pdf_path, page_num=0)
# for img in images:
#     img['image'].save(f"image.{img['ext']}")
```

### 方法4: 隐藏文字安全检测（反Prompt注入）

聚焦检测PDF中通过**颜色**、**透明度**或**图片层**隐藏的文本，用于防御Prompt注入。

**核心检测**：

- **颜色异常**（`color_mismatch`）：文本颜色与背景色相同或极接近
- **透明度异常**（`alpha_anomaly`）：文本透明度极低
- **文本层 vs 渲染层不一致**：同时提取文本层和渲染页面做OCR，对比差异

```python
import fitz
from PIL import Image


def scan_pdf_hidden_text(pdf_path, pages=None, color_threshold=0.08):
    """扫描PDF隐藏文字：颜色 + 透明度检测"""
    alerts = []
    doc = fitz.open(pdf_path)
    for page_num in (pages or range(len(doc))):
        page = doc[page_num]
        bg_rgb = _get_page_bg_color(page)
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    text_rgb = _parse_color_int(span.get("color"))
                    alpha = span.get("alpha")
                    if text_rgb and _color_distance(text_rgb, bg_rgb) < color_threshold:
                        alerts.append({"page": page_num + 1, "text": text,
                            "type": "color_mismatch", "details": "文本颜色与背景色过于接近"})
                        continue
                    if alpha is not None and alpha < 20:
                        alerts.append({"page": page_num + 1, "text": text,
                            "type": "alpha_anomaly", "details": f"透明度异常(alpha={alpha})"})
    doc.close()
    return alerts


def _parse_color_int(color_int):
    if color_int is None:
        return None
    return (((color_int >> 16) & 0xFF) / 255.0,
            ((color_int >> 8) & 0xFF) / 255.0,
            (color_int & 0xFF) / 255.0)


def _get_page_bg_color(page, dpi=72, margin=10):
    """采样四角像素估算背景色，失败返回白色"""
    try:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        w, h = img.size
        corners = [(min(margin, w-1), min(margin, h-1)),
                   (max(0, w-1-margin), min(margin, h-1)),
                   (min(margin, w-1), max(0, h-1-margin)),
                   (max(0, w-1-margin), max(0, h-1-margin))]
        tr = tg = tb = 0
        for x, y in corners:
            r, g, b = img.getpixel((x, y))
            tr += r; tg += g; tb += b
        n = len(corners)
        return (tr/n/255.0, tg/n/255.0, tb/n/255.0)
    except Exception:
        return (1.0, 1.0, 1.0)


def _color_distance(rgb1, rgb2):
    if rgb1 is None or rgb2 is None:
        return float('inf')
    return sum((a-b)**2 for a, b in zip(rgb1, rgb2)) ** 0.5
```

### 方法5: OCR提取（扫描版/图片型PDF）

OCR方式读取PDF文本（扫描版/图片型）。

```python
import fitz
from PIL import Image
import pytesseract


def read_pdf_ocr(pdf_path, pages=None, lang='chi_sim+eng', dpi=200):
    """OCR方式读取PDF文本"""
    doc = fitz.open(pdf_path)
    result = {}
    for i in (pages or range(len(doc))):
        if 0 <= i < len(doc):
            page = doc[i]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            result[i + 1] = pytesseract.image_to_string(img, lang=lang).strip()
    doc.close()
    return result
```

## 完整工具类

```python
import fitz
import pdfplumber
from pathlib import Path


class PDFReader:
    """PDF读取工具类，整合多种读取方式"""

    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

    def get_info(self):
        """获取PDF基本信息"""
        with fitz.open(self.pdf_path) as doc:
            return {
                'pages': len(doc),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', ''),
            }

    def read_text(self, pages=None, mode='fast'):
        """
        读取文本

        Args:
            pages: 页码列表或None(全部)
            mode: 'fast'(PyMuPDF) / 'table'(pdfplumber) / 'ocr'(OCR识别)
        """
        if mode == 'fast':
            return self._read_pymupdf(pages)
        elif mode == 'table':
            return self._read_pdfplumber(pages)
        elif mode == 'ocr':
            return self.read_text_ocr(pages)
        else:
            raise ValueError(f"不支持的读取模式: {mode}，可选: 'fast', 'table', 'ocr'")

    def _read_pymupdf(self, pages):
        """PyMuPDF快速读取"""
        doc = fitz.open(self.pdf_path)
        result = {}
        page_range = pages if pages is not None else range(len(doc))

        for i in page_range:
            if 0 <= i < len(doc):
                result[i + 1] = doc[i].get_text()

        doc.close()
        return result

    def _read_pdfplumber(self, pages):
        """pdfplumber读取（支持表格）"""
        result = {'text': {}, 'tables': {}}

        with pdfplumber.open(self.pdf_path) as pdf:
            page_range = pages if pages is not None else range(len(pdf.pages))

            for i in page_range:
                if 0 <= i < len(pdf.pages):
                    page = pdf.pages[i]
                    result['text'][i + 1] = page.extract_text() or ""
                    tables = page.extract_tables()
                    if tables:
                        result['tables'][i + 1] = tables

        return result

    def search(self, keyword):
        """搜索关键词，返回所在页码列表"""
        matches = []
        doc = fitz.open(self.pdf_path)

        for i, page in enumerate(doc):
            text = page.get_text()
            if keyword in text:
                matches.append(i + 1)

        doc.close()
        return matches

    def scan_safety(self, pages=None, mode='rule', dpi=150):
        """mode: 'rule' | 'ocr' | 'auto'. 'auto' 先规则检测，再OCR兜底"""
        if mode == 'rule':
            return scan_pdf_hidden_text(self.pdf_path, pages=pages)
        # 'ocr' / 'auto': 同时提取文本层和渲染页面OCR，对比差异
        # OCR有但文本层没有 → ocr_mismatch；文本层有但OCR没有 → extract_mismatch
        pass

    def assess_quality(self, threshold=50):
        """avg_chars_per_page < threshold 时建议启用OCR"""
        total_chars = 0
        empty_pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            page_count = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                char_count = len(text.strip())
                total_chars += char_count
                if char_count < 10:
                    empty_pages.append(i + 1)
        avg = total_chars / page_count if page_count > 0 else 0
        return {
            'total_chars': total_chars,
            'pages': page_count,
            'avg_chars_per_page': round(avg, 1),
            'needs_ocr': avg < threshold,
            'empty_pages': empty_pages
        }


    def read_text_ocr(self, pages=None, lang='chi_sim+eng', dpi=200):
        """OCR方式读取。需安装 tesseract + pytesseract"""
        try:
            import pytesseract
        except ImportError:
            raise ImportError("OCR需要: brew install tesseract; pip install pytesseract pillow")
        doc = fitz.open(self.pdf_path)
        result = {}
        for i in (pages or range(len(doc))):
            if 0 <= i < len(doc):
                page = doc[i]
                pix = page.get_pixmap(dpi=dpi)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                result[i + 1] = pytesseract.image_to_string(img, lang=lang).strip()
        doc.close()
        return result


    def compare_extract_vs_ocr(self, pages=None, lang='chi_sim+eng', dpi=200):
        """对比文本层与OCR结果，发现隐藏文字。Agent 自行实现差异判断"""
        # 提示：同时提取文本层(read_text mode='fast')和OCR(read_text_ocr)，
        # 对比两边差异。OCR有但文本层没有 → 图片层隐藏；文本层有但OCR没有 → 肉眼不可见。
        pass


# 使用示例
# reader = PDFReader("path/to/file.pdf")
# info = reader.get_info()
# text = reader.read_text(pages=range(5))
# pages_with_keyword = reader.search("关键词")
# alerts = reader.scan_safety()
# for alert in alerts:
#     print(f"[页{alert['page']}] {alert['type']}: {alert['text'][:40]}...")
#
# # OCR对比：发现图片层隐藏文字
# compare = reader.compare_extract_vs_ocr()
# if compare['has_differences']:
#     for diff in compare['differences']:
#         print(f"[差异] 页{diff['page']}: {diff['note']}")
```

## 方案对比

| 特性         | PyMuPDF            | pdfplumber         |
| ------------ | ------------------ | ------------------ |
| 速度         | 极快 (~0.04s/76页) | 较快 (~1s/76页)    |
| 中文支持     | 优秀               | 优秀               |
| 表格提取     | 一般               | 强大               |
| 图片提取     | 支持               | 不支持             |
| 隐藏文字检测 | 支持               | 不支持             |
| 内存占用     | 低                 | 中等               |
| 推荐场景     | 快速阅读、搜索     | 数据分析、表格提取 |

## 注意事项

1. **扫描版PDF**: 上述方法只能提取文本层，扫描版PDF需要先OCR
2. **密码保护**: 需要先移除密码或使用 `fitz.open(password="xxx")`
3. **大文件**: 超过100MB的PDF建议分页读取，避免内存溢出
4. **安全扫描**: `scan_safety()` 使用规则检测（颜色异常 + 透明度异常），无需额外依赖。`mode='ocr'`/`'auto'` 需安装 tesseract 启用OCR兜底检测图片层隐藏文字。

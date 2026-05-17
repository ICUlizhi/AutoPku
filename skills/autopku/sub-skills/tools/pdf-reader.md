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
            mode: 'fast'(PyMuPDF) 或 'table'(pdfplumber)
        """
        if mode == 'fast':
            return self._read_pymupdf(pages)
        else:
            return self._read_pdfplumber(pages)

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


# 使用示例
# reader = PDFReader("path/to/file.pdf")
# info = reader.get_info()
# text = reader.read_text(pages=range(5))
# pages_with_keyword = reader.search("关键词")
```

## 方案对比

| 特性 | PyMuPDF | pdfplumber |
|------|---------|------------|
| 速度 | 极快 (~0.04s/76页) | 较快 (~1s/76页) |
| 中文支持 | 优秀 | 优秀 |
| 表格提取 | 一般 | 强大 |
| 图片提取 | 支持 | 不支持 |
| 内存占用 | 低 | 中等 |
| 推荐场景 | 快速阅读、搜索 | 数据分析、表格提取 |

## 注意事项

1. **扫描版PDF**: 上述方法只能提取文本层，扫描版PDF需要先OCR
2. **密码保护**: 需要先移除密码或使用 `fitz.open(password="xxx")`
3. **大文件**: 超过100MB的PDF建议分页读取，避免内存溢出

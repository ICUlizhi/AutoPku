---
name: autopku-task-do-homework
description: 完成PKU课程作业（解析→解答→渲染→询问用户→提交）
---

# 任务：完成作业并提交

## 流程

```
Phase 1: PDF解析 → Phase 2: 解答 → Phase 3: 渲染 → 
询问用户 → [确认] → Phase 4: 提交
```

## 步骤

### 1. 用户确认

列出该课程待交作业，用 AskUserQuestion 让用户选择：

```python
AskUserQuestion({
    "questions": [{
        "question": "请选择要完成的作业：",
        "options": [
            {"label": "第五次习题 (截止: 3天后)", "value": "hw5"}
        ]
    }]
})
```

二次确认后开始执行。

### 2. PDF 解析

引用: `tools/pdf-reader.md`

```python
import pdfplumber
import json
import re

def parse_homework(pdf_path, output_json):
    content = {'pages': [], 'problems': []}
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            content['pages'].append({'page_num': i+1, 'text': text})
    
    full_text = '\n'.join(p['text'] for p in content['pages'])
    
    # 提取题目
    pattern = r'(?:^|\n)\s*(?:Problem\s*)?(\d+)[\.、\)]\s*([^\n]+)(.*?)(?=\n(?:\d+|Problem|\Z))'
    matches = re.findall(pattern, full_text, re.DOTALL | re.IGNORECASE)
    
    for num, title, body in matches:
        content['problems'].append({
            'number': num.strip(),
            'title': title.strip(),
            'content': body.strip()
        })
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    return content
```

### 3. 解答

为主 skill 提供 agent 配置：

```python
agent_config = {
    "name": f"{course}-solver",
    "task": f"""
你是 Solver，完成 {course} {assignment} 的解答。

输入：{base_dir}/{course}/作业/homework_parsed.json
资料：{base_dir}/{course}/资料/
输出：{base_dir}/{course}/作业/answers.json

逐题解答（公式、推导、答案），标注参考资料，保存 JSON。
"""
}

# 由主 skill 创建 agent
```

### 4. 质量检查（写作类作业）

若作业包含字数/词数要求（如 Reflection、Essay、Annotated Bibliography），在定稿前使用脚本精确统计并核对：

```python
import re

def count_words(text):
    words = text.split()
    # 过滤纯标点符号项
    cleaned = [w for w in words if re.search(r"[a-zA-Z0-9]", w)]
    return len(words), len(cleaned)

with open("{md_path}", "r", encoding="utf-8") as f:
    content = f.read()

# 按章节统计示例
sections = {
    "Annotated Bibliography": re.search(r"## .*?Annotated Bibliography.*?\n(.*?)(?=\n## )", content, re.DOTALL),
    "Reflection": re.search(r"## .*?Reflection.*?\n(.*?)(?=\n---\n|\Z)", content, re.DOTALL),
}

for name, match in sections.items():
    if match:
        raw, clean = count_words(match.group(1).strip())
        print(f"{name}: {clean} words")
```

发现超字数或不足时，立即调整内容，确保符合要求后再进入渲染。

### 5. 渲染

生成 Markdown，然后转换为 PDF：

```bash
pip3 install markdown

python3 << 'PYEOF'
import markdown

with open('{md_path}', 'r', encoding='utf-8') as f:
    md = f.read()

html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
html_full = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body {{ font-family: "Noto Serif CJK SC", serif; margin: 40px; }}</style>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head><body>{html}</body></html>'''

with open('{html_path}', 'w', encoding='utf-8') as f:
    f.write(html_full)
PYEOF

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --print-to-pdf="{pdf_path}" "file://{html_path}"
```

### 6. 询问用户

```python
AskUserQuestion({
    "questions": [{
        "question": "作业已完成渲染。是否提交到教学网？",
        "options": [
            {"label": "提交", "value": "submit"},
            {"label": "仅保存本地", "value": "save_only"}
        ]
    }]
})
```

### 7. 提交

```bash
/tmp/pku3b a ls --all-term | grep -i "{course}"
/tmp/pku3b a submit {assignment_id} "{pdf_path}"
```

## 输出

- `{course}/作业/{assignment}_answer.md`
- `{course}/作业/{assignment}_answer.pdf`
- 教学网提交状态

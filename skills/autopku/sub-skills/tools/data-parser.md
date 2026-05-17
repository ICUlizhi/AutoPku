---
name: autopku-tool-data-parser
description: 解析 pku3b 输出数据（ANSI颜色码处理、作业提取、课程筛选）
---

# 教学网数据解析

## ANSI 颜色码清理

```python
import re

def strip_ansi(text):
    """移除 ANSI 颜色码"""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)
```

## 作业列表解析

```python
import re
import json

def parse_assignments(raw_text):
    """
    解析 pku3b a ls --all-term 输出
    
    Returns:
        [{"course": "课程名", "assignment": "作业名", "status": "状态"}]
    """
    pattern = r'\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\x1b\[2m>\x1b\[0m\s+\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\(([^)]+)\)'
    matches = re.findall(pattern, raw_text)
    
    return [
        {"course": c.strip(), "assignment": a.strip(), "status": s.strip()}
        for c, a, s in matches
    ]
```

## 选课列表解析

```python
def parse_courses(raw_text):
    """
    解析 pku3b s -d major show 输出
    提取"已选上"的课程
    """
    pattern = r'已选上.*?\x1b\[32m([^\x1b]+)\x1b\[0m'
    return re.findall(pattern, raw_text)
```

## 公告解析

```python
def parse_announcements(raw_text):
    """
    解析 pku3b ann ls 输出
    
    Returns:
        [{"course": "课程名", "title": "公告标题", "id": "公告ID"}]
    """
    pattern = r'\x1b\[36m([^\x1b]+?)\x1b\[0m\s+>\s+\x1b\[1m([^\x1b]+?)\x1b\[0m\s+\(ID:\s+([^)]+)\)'
    matches = re.findall(pattern, raw_text)
    
    return [
        {"course": c.strip(), "title": t.strip(), "id": i.strip()}
        for c, t, i in matches
    ]
```

## 课程筛选

```python
def filter_current_semester(assignments, current_courses):
    """
    筛选当前学期作业
    同时检查"未选上"但有作业的课程
    """
    current = [a for a in assignments if a['course'] in current_courses]
    
    # 检查遗漏课程
    all_courses = set(a['course'] for a in assignments)
    missed = all_courses - set(current_courses)
    
    return current, list(missed)
```

## 附件检测

```python
def has_attachment(raw_text, course_name):
    """检查课程是否有可下载附件"""
    pattern = rf'{re.escape(course_name)}.*?\[附件\]'
    return bool(re.search(pattern, raw_text))
```

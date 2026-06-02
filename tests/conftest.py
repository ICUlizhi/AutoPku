#!/usr/bin/env python3
"""
AutoPku 测试框架公共工具
提供验证辅助函数、mock 数据生成器等
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# ============ 路径常量 ============
TESTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = TESTS_DIR.parent
FIXTURES_DIR = TESTS_DIR / "_fixtures"


# ============ 验证工具 ============

def check_file_exists(path: Path, msg: str = "") -> Tuple[bool, str]:
    """检查文件是否存在"""
    if path.exists():
        return True, f"OK: {path}"
    return False, f"FAIL: 文件不存在 {path} {msg}"


def check_dir_structure(base: Path, expected: List[str]) -> Tuple[bool, List[str]]:
    """检查目录结构是否符合预期
    
    Args:
        base: 基础目录
        expected: 期望存在的相对路径列表（支持 glob 模式）
    
    Returns:
        (是否全部通过, 详细结果列表)
    """
    results = []
    all_ok = True
    for pattern in expected:
        matches = list(base.glob(pattern))
        if matches:
            results.append(f"OK: {pattern} -> {matches}")
        else:
            results.append(f"FAIL: 未找到 {pattern}")
            all_ok = False
    return all_ok, results


def check_file_contains(path: Path, expected: str, min_occurrences: int = 1) -> Tuple[bool, str]:
    """检查文件内容是否包含指定字符串"""
    if not path.exists():
        return False, f"FAIL: 文件不存在 {path}"
    
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"FAIL: 无法读取 {path}: {e}"
    
    count = content.count(expected)
    if count >= min_occurrences:
        return True, f"OK: 找到 {count} 次 '{expected[:50]}...'"
    return False, f"FAIL: 期望至少 {min_occurrences} 次，实际 {count} 次 '{expected[:50]}...'"


def check_pdf_pages(path: Path, min_pages: int = 1, max_pages: Optional[int] = None) -> Tuple[bool, str]:
    """检查 PDF 页数是否在范围内（macOS 使用 mdls）"""
    if not path.exists():
        return False, f"FAIL: PDF 不存在 {path}"
    
    try:
        result = subprocess.run(
            ["mdls", "-name", "kMDItemNumberOfPages", "-raw", str(path)],
            capture_output=True, text=True, timeout=10
        )
        pages = int(result.stdout.strip())
    except Exception as e:
        return False, f"FAIL: 无法获取页数 {path}: {e}"
    
    if pages < min_pages:
        return False, f"FAIL: 页数 {pages} < 最小要求 {min_pages}"
    if max_pages and pages > max_pages:
        return False, f"FAIL: 页数 {pages} > 最大要求 {max_pages}"
    return True, f"OK: PDF {pages} 页（范围 {min_pages}-{max_pages or '∞'}）"


def check_pdf_has_text(path: Path) -> Tuple[bool, str]:
    """检查 PDF 是否包含实际文本（非空白）"""
    if not path.exists():
        return False, f"FAIL: PDF 不存在 {path}"
    
    try:
        result = subprocess.run(
            ["strings", str(path)],
            capture_output=True, text=True, timeout=10
        )
        text = result.stdout.strip()
        # 过滤掉常见噪声
        meaningful = [t for t in text.split("\n") if len(t) > 5 and not t.startswith("/")]
        if len(meaningful) > 3:
            return True, f"OK: PDF 包含 {len(meaningful)} 条有意义文本"
        return False, f"FAIL: PDF 文本过少（{len(meaningful)} 条）"
    except Exception as e:
        return False, f"FAIL: 无法读取 {path}: {e}"


def check_no_duplicate_content(path: Path, marker: str, max_occurrences: int = 1) -> Tuple[bool, str]:
    """检查文件内容中某标记是否重复出现（用于检测重复渲染）"""
    if not path.exists():
        return False, f"FAIL: 文件不存在 {path}"
    
    content = path.read_text(encoding="utf-8")
    count = content.count(marker)
    if count > max_occurrences:
        return False, f"FAIL: 标记 '{marker[:30]}' 出现 {count} 次，期望最多 {max_occurrences} 次（可能重复渲染）"
    return True, f"OK: 标记出现 {count} 次（<= {max_occurrences}）"


# ============ Mock 数据生成器 ============

def generate_mock_ansi_output(courses: List[Dict]) -> str:
    """生成模拟的 pku3b a ls 输出（带 ANSI 颜色码）"""
    lines = []
    for c in courses:
        name = c.get("name", "未知课程")
        status = c.get("status", "待提交")
        deadline = c.get("deadline", "2026-06-30")
        lines.append(f"\x1b[32m{name}\x1b[0m - {status} (截止: {deadline})")
    return "\n".join(lines)


def generate_mock_homework_pdf(output_path: Path, title: str = "测试作业") -> None:
    """生成一个简单的测试用 PDF 作业文件（使用 reportlab）"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        # 回退：创建一个空白文件，测试时跳过 PDF 相关验证
        output_path.write_text("# Mock PDF placeholder\nInstall reportlab to generate real PDF.")
        return
    
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica", 16)
    c.drawString(50, height - 50, title)
    
    c.setFont("Helvetica", 12)
    y = height - 100
    questions = [
        "1. 请简述AutoPku的设计思想。",
        "2. 解释Agent Team协作模式的优势。",
        "3. 分析Skill即代码架构的优缺点。",
    ]
    for q in questions:
        c.drawString(50, y, q)
        y -= 30
    
    c.save()


def generate_mock_lecture_pdf(output_path: Path, title: str = "测试课件") -> None:
    """生成一个简单的测试用课件 PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        output_path.write_text("# Mock PDF placeholder")
        return
    
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica", 18)
    c.drawString(50, height - 50, title)
    
    c.setFont("Helvetica", 12)
    content = [
        "定义 1.1 (测试定义): 这是一个形式化定义。",
        "",
        "定理 1.1 (测试定理): 如果 A 则 B。",
        "证明: 使用归纳法...",
        "",
        "结论: 本节核心内容是测试。",
    ]
    y = height - 100
    for line in content:
        c.drawString(50, y, line)
        y -= 25
    
    c.save()


# ============ 测试报告 ============

class TestReport:
    """简单的测试报告收集器"""
    
    def __init__(self):
        self.results: List[Dict] = []
    
    def add(self, test_name: str, passed: bool, details: List[str]):
        self.results.append({
            "name": test_name,
            "passed": passed,
            "details": details,
        })
    
    def print_summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        print("\n" + "=" * 60)
        print(f"测试结果汇总: {passed}/{total} 通过, {failed}/{total} 失败")
        print("=" * 60)
        
        for r in self.results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            print(f"\n{status} | {r['name']}")
            for d in r["details"]:
                print(f"  {d}")
        
        print("\n" + "=" * 60)
        return failed == 0


if __name__ == "__main__":
    # 简单自检
    print("conftest.py 加载成功")
    print(f"TESTS_DIR: {TESTS_DIR}")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")

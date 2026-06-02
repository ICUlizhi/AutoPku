#!/usr/bin/env python3
"""
基于 case_06: pkusli 模板获取与编译测试
验证模板仓库可访问、main.typ 组装正确、typst 编译成功
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

TEMPLATE_URL = "https://github.com/hanlife02/pkusli"
TEMPLATE_DIR = Path.home() / ".autopku" / "templates" / "pkusli"

errors = []


def test_repo_accessible():
    """测试 pkusli 仓库可访问"""
    print("[1/4] 检查 pkusli 仓库可访问性...")
    result = subprocess.run(
        ["curl", "-sI", TEMPLATE_URL],
        capture_output=True, text=True, timeout=30
    )
    if "200" in result.stdout or "301" in result.stdout or "302" in result.stdout:
        print("  ✅ 仓库可访问")
        return True
    else:
        errors.append(f"仓库不可访问: {result.stdout[:200]}")
        print(f"  ❌ 仓库不可访问")
        return False


def test_template_clone():
    """测试 git clone pkusli 模板"""
    print("[2/4] 测试 git clone 模板...")
    
    # 清理旧的测试目录
    test_dir = Path(tempfile.gettempdir()) / "autopku_test_pkusli"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    result = subprocess.run(
        ["git", "clone", "--depth", "1", TEMPLATE_URL + ".git", str(test_dir)],
        capture_output=True, text=True, timeout=60
    )
    
    if result.returncode != 0:
        errors.append(f"git clone 失败: {result.stderr}")
        print(f"  ❌ clone 失败")
        return False
    
    # 检查关键文件
    required = ["main.typ", "style/index.typ", "slides/index.typ"]
    for f in required:
        if not (test_dir / f).exists():
            errors.append(f"模板缺少关键文件: {f}")
            print(f"  ❌ 缺少 {f}")
            return False
    
    print("  ✅ 模板 clone 成功，关键文件完整")
    
    # 清理
    shutil.rmtree(test_dir)
    return True


def test_typst_compile():
    """测试 typst 编译模板"""
    print("[3/4] 测试 typst 编译...")
    
    # 检查 typst 是否安装
    result = subprocess.run(["which", "typst"], capture_output=True)
    if result.returncode != 0:
        print("  ⚠️  typst 未安装，跳过编译测试")
        return True  # 不视为失败
    
    # clone 到临时目录
    test_dir = Path(tempfile.gettempdir()) / "autopku_test_pkusli_compile"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    subprocess.run(
        ["git", "clone", "--depth", "1", TEMPLATE_URL + ".git", str(test_dir)],
        capture_output=True, timeout=60
    )
    
    # 编译
    result = subprocess.run(
        ["typst", "compile", str(test_dir / "main.typ"), str(test_dir / "test.pdf")],
        capture_output=True, text=True, timeout=120
    )
    
    if result.returncode != 0:
        errors.append(f"typst 编译失败: {result.stderr}")
        print(f"  ❌ 编译失败")
        shutil.rmtree(test_dir)
        return False
    
    # 检查 PDF
    pdf = test_dir / "test.pdf"
    if not pdf.exists() or pdf.stat().st_size < 1000:
        errors.append("编译后的 PDF 不存在或过小")
        print(f"  ❌ PDF 异常")
        shutil.rmtree(test_dir)
        return False
    
    print(f"  ✅ 编译成功，PDF {pdf.stat().st_size} bytes")
    shutil.rmtree(test_dir)
    return True


def test_chinese_content():
    """测试中文内容渲染（基于 case_06 的 songti 踩坑）"""
    print("[4/4] 测试中文内容渲染...")
    
    result = subprocess.run(["which", "typst"], capture_output=True)
    if result.returncode != 0:
        print("  ⚠️  typst 未安装，跳过")
        return True
    
    # 创建包含中文的最小 typst 文件
    test_typ = Path(tempfile.gettempdir()) / "test_chinese.typ"
    test_typ.write_text('#set text(font: "PingFang SC")\n#lorem(20)\n这是中文测试。\n', encoding="utf-8")
    
    test_pdf = Path(tempfile.gettempdir()) / "test_chinese.pdf"
    result = subprocess.run(
        ["typst", "compile", str(test_typ), str(test_pdf)],
        capture_output=True, text=True, timeout=60
    )
    
    if result.returncode != 0:
        errors.append(f"中文内容编译失败: {result.stderr}")
        print(f"  ❌ 中文编译失败")
        return False
    
    # 检查 PDF 包含中文（使用 PyMuPDF，strings 对 typst 字体编码不友好）
    try:
        import fitz
        doc = fitz.open(str(test_pdf))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if "中文测试" not in text:
            errors.append("PDF 中未找到中文字符")
            print(f"  ❌ 中文未渲染")
            return False
    except ImportError:
        print("  ⚠️  PyMuPDF 未安装，跳过中文内容验证")
        return True
    
    print("  ✅ 中文渲染正常")
    test_typ.unlink(missing_ok=True)
    test_pdf.unlink(missing_ok=True)
    return True


def main():
    print("=" * 60)
    print("pkusli 模板测试 (基于 case_06)")
    print("=" * 60)
    
    test_repo_accessible()
    test_template_clone()
    test_typst_compile()
    test_chinese_content()
    
    if errors:
        print(f"\n❌ {len(errors)} 个失败:")
        for e in errors:
            print(f"  - {e}")
        return 1
    
    print("\n✅ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

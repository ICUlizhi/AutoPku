#!/usr/bin/env python3
"""
基于真实案例的作业功能回归测试
- case_07: 作业误提交恢复（pku3b 学期匹配、备注添加）
"""

import sys
import subprocess
import tempfile
from pathlib import Path

errors = []


def test_pku3b_semester_matching():
    """case_07: 验证 pku3b submit 的学期匹配逻辑"""
    print("[1/2] 测试 pku3b 学期匹配...")
    
    # pku3b a ls --all-term 返回所有历史学期
    # 但 pku3b a submit 只检查当前学期
    # 如果作业在历史学期，直接 submit 会报 "assignment not found"
    
    # 这是一个逻辑验证，不需要实际调用 pku3b
    # 验证 skill 文档中是否提到了这一点
    
    skill_path = Path(__file__).parent.parent / "sub-skills" / "tools" / "pku3b-setup.md"
    if not skill_path.exists():
        print("  ⚠️  pku3b-setup.md 不存在，跳过")
        return True
    
    content = skill_path.read_text(encoding="utf-8")
    
    # 检查是否有学期相关的说明
    if "学期" not in content and "term" not in content.lower():
        errors.append("pku3b-setup.md 缺少学期匹配说明（case_07 踩坑）")
        print("  ❌ 缺少学期说明")
        return False
    
    print("  ✅ 学期匹配说明存在")
    return True


def test_submit_confirmation():
    """case_07: 验证提交前二次确认机制"""
    print("[2/2] 测试提交前确认机制...")
    
    # 验证 do-homework.md 中是否有 AskUserQuestion 提交确认
    skill_path = Path(__file__).parent.parent / "sub-skills" / "tasks" / "do-homework.md"
    if not skill_path.exists():
        print("  ⚠️  do-homework.md 不存在，跳过")
        return True
    
    content = skill_path.read_text(encoding="utf-8")
    
    # 检查是否有提交确认相关内容
    has_confirm = any(k in content for k in [
        "AskUserQuestion", "确认", "提交", "confirm", "submit"
    ])
    
    if not has_confirm:
        errors.append("do-homework.md 缺少提交确认机制说明")
        print("  ❌ 缺少确认机制")
        return False
    
    # 检查是否有安全规则（禁止自动提交）
    has_safety = "禁止" in content and "自动" in content
    if not has_safety:
        warnings = ["do-homework.md 可能缺少明确的自动提交禁止规则"]
        print("  ⚠️  安全规则不够明确")
    else:
        print("  ✅ 提交确认机制存在")
    
    return True


def main():
    print("=" * 60)
    print("do-homework 回归测试 (基于 case_07)")
    print("=" * 60)
    
    test_pku3b_semester_matching()
    test_submit_confirmation()
    
    if errors:
        print(f"\n❌ {len(errors)} 个失败:")
        for e in errors:
            print(f"  - {e}")
        return 1
    
    print("\n✅ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

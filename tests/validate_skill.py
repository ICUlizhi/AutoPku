#!/usr/bin/env python3
"""
Skill 文档静态检查
验证所有 skill 文件的格式正确性、内部链接有效性
"""

import sys
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SKILLS = list((PROJECT_ROOT / "sub-skills").rglob("*.md"))
SKILLS.append(PROJECT_ROOT / "skill.md")

errors = []
warnings = []


def check_yaml_frontmatter(path: Path, content: str):
    """检查 YAML frontmatter"""
    if not content.startswith("---"):
        errors.append(f"{path}: 缺少 YAML frontmatter")
        return
    
    # 提取 frontmatter
    match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append(f"{path}: YAML frontmatter 格式错误")
        return
    
    fm = match.group(1)
    if "name:" not in fm:
        errors.append(f"{path}: frontmatter 缺少 name 字段")
    if "description:" not in fm:
        warnings.append(f"{path}: frontmatter 缺少 description 字段")


def check_internal_links(path: Path, content: str):
    """检查内部链接指向的文件是否存在"""
    # 匹配 `sub-skills/xxx/xxx.md` 格式的链接
    for match in re.finditer(r"`?(sub-skills/[^`\s)]+\.md)`?", content):
        link = match.group(1)
        target = PROJECT_ROOT / link
        if not target.exists():
            errors.append(f"{path}: 内部链接指向不存在的文件: {link}")


def check_code_blocks(path: Path, content: str):
    """检查代码块标签是否有效"""
    valid_tags = {"python", "bash", "typst", "json", "lua", "markdown", "text", ""}
    for match in re.finditer(r"```(\w*)", content):
        tag = match.group(1)
        if tag and tag not in valid_tags:
            warnings.append(f"{path}: 未知代码块标签: {tag}")


def check_touying_ethan_renamed(content: str, path: Path):
    """检查是否还有旧的 touying-ethan 引用（应该已改为 pkusli）"""
    if "touying-ethan" in content:
        errors.append(f"{path}: 仍包含旧的 'touying-ethan'，应改为 'pkusli'")


def main():
    print(f"检查 {len(SKILLS)} 个 skill 文件...")
    
    for path in SKILLS:
        content = path.read_text(encoding="utf-8")
        rel = path.relative_to(PROJECT_ROOT)
        
        check_yaml_frontmatter(rel, content)
        check_internal_links(rel, content)
        check_code_blocks(rel, content)
        check_touying_ethan_renamed(content, rel)
    
    # 输出结果
    if warnings:
        print(f"\n⚠️  {len(warnings)} 个警告:")
        for w in warnings:
            print(f"  {w}")
    
    if errors:
        print(f"\n❌ {len(errors)} 个错误:")
        for e in errors:
            print(f"  {e}")
        print(f"\n❌ 测试失败")
        return 1
    
    print(f"\n✅ 所有 {len(SKILLS)} 个 skill 文件检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

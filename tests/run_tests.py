#!/usr/bin/env python3
"""AutoPku 回归测试总入口"""

import sys
import subprocess
from pathlib import Path

TESTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = TESTS_DIR.parent

TEST_FILES = [
    "validate_skill.py",
    "test_pkusli.py",
    "test_write_notes.py",
    "test_write_paper.py",
    "test_do_homework.py",
]


def run_file(path: Path) -> dict:
    """运行单个测试文件，返回结果"""
    print(f"\n{'='*60}")
    print(f">>> 运行: {path.name}")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(PROJECT_ROOT),
        capture_output=False,  # 直接输出到终端
    )
    
    return {
        "name": path.name,
        "passed": result.returncode == 0,
        "returncode": result.returncode,
    }


def main():
    print("=" * 60)
    print("AutoPku Regression Tests")
    print("=" * 60)
    
    results = []
    for name in TEST_FILES:
        path = TESTS_DIR / name
        if not path.exists():
            print(f"\n⚠️  跳过: {name} (文件不存在)")
            results.append({"name": name, "passed": False, "returncode": -1})
            continue
        results.append(run_file(path))
    
    # 汇总
    print("\n" + "=" * 60)
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    print(f"汇总: {passed}/{total} 通过 | {failed}/{total} 失败")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']} (exit={r['returncode']})")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

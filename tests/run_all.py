#!/usr/bin/env python3
"""
AutoPku 测试框架总入口
一键发现、运行并汇总所有测试用例
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict

TESTS_DIR = Path(__file__).parent.resolve()


def discover_tests() -> List[Path]:
    """发现所有测试用例目录"""
    tests = []
    for module_dir in TESTS_DIR.iterdir():
        if not module_dir.is_dir() or module_dir.name.startswith("_"):
            continue
        for test_dir in module_dir.iterdir():
            if test_dir.is_dir() and test_dir.name.startswith("test_"):
                tests.append(test_dir)
    return sorted(tests)


def run_test(test_dir: Path) -> Dict:
    """运行单个测试用例"""
    result = {
        "name": str(test_dir.relative_to(TESTS_DIR)),
        "passed": False,
        "details": [],
    }
    
    readme = test_dir / "README.md"
    setup = test_dir / "setup.sh"
    validate = test_dir / "validate.py"
    
    # 检查必需文件
    if not readme.exists():
        result["details"].append("FAIL: README.md 不存在")
        return result
    
    # 1. 执行 setup（如果存在）
    if setup.exists():
        try:
            proc = subprocess.run(
                ["bash", str(setup)],
                cwd=str(test_dir),
                capture_output=True,
                text=True,
                timeout=60,
            )
            if proc.returncode != 0:
                result["details"].append(f"setup.sh 失败: {proc.stderr[:200]}")
                return result
            result["details"].append("OK: setup.sh 完成")
        except subprocess.TimeoutExpired:
            result["details"].append("FAIL: setup.sh 超时")
            return result
        except Exception as e:
            result["details"].append(f"FAIL: setup.sh 异常: {e}")
            return result
    else:
        result["details"].append("INFO: 无 setup.sh")
    
    # 2. 检查是否有 run.sh（供 AI 执行的步骤说明）
    run_sh = test_dir / "run.sh"
    if run_sh.exists():
        result["details"].append("INFO: run.sh 存在（需 AI Agent 按步骤执行）")
    
    # 3. 执行 validate（如果存在）
    if validate.exists():
        try:
            proc = subprocess.run(
                [sys.executable, str(validate)],
                cwd=str(test_dir),
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = proc.stdout + proc.stderr
            lines = [l for l in output.strip().split("\n") if l.strip()]
            
            if proc.returncode == 0:
                result["passed"] = True
                result["details"].extend(lines)
            else:
                result["details"].extend(lines)
        except subprocess.TimeoutExpired:
            result["details"].append("FAIL: validate.py 超时")
        except Exception as e:
            result["details"].append(f"FAIL: validate.py 异常: {e}")
    else:
        result["details"].append("INFO: 无 validate.py（纯手动测试）")
    
    return result


def main():
    print("=" * 60)
    print("AutoPku Test Suite Runner")
    print("=" * 60)
    
    tests = discover_tests()
    print(f"\n发现 {len(tests)} 个测试用例:\n")
    for t in tests:
        print(f"  - {t.relative_to(TESTS_DIR)}")
    
    print("\n" + "-" * 60)
    print("注意：部分测试需要 AI Agent 按 run.sh 执行 skill 后才能验证")
    print("      本脚本仅执行 setup + validate（机器可自动化部分）")
    print("-" * 60 + "\n")
    
    results = []
    for test_dir in tests:
        print(f"\n>>> 运行: {test_dir.relative_to(TESTS_DIR)}")
        result = run_test(test_dir)
        results.append(result)
    
    # 汇总报告
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    
    print("\n" + "=" * 60)
    print(f"汇总: {passed}/{total} 通过 | {failed}/{total} 失败")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"\n{status} {r['name']}")
        for d in r["details"]:
            prefix = "    "
            if d.startswith("OK:"):
                prefix = "    ✅ "
            elif d.startswith("FAIL:"):
                prefix = "    ❌ "
            elif d.startswith("INFO:"):
                prefix = "    ℹ️  "
            print(f"{prefix}{d}")
    
    # 保存 JSON 报告
    report_path = TESTS_DIR / "_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

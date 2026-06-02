#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# 使用 conftest 中的生成器创建 mock PDF
python3 << 'PYEOF'
import sys
from pathlib import Path
# cwd 是 test_01_pdf_parse/
sys.path.insert(0, str(Path.cwd().parent.parent))
from conftest import generate_mock_homework_pdf

generate_mock_homework_pdf(Path("homework_mock.pdf"), title="自动测试作业")
print("OK: mock PDF 生成完成")
PYEOF

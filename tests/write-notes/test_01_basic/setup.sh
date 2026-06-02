#!/bin/bash
set -e

# 创建测试目录结构
mkdir -p input notes

# 创建模拟课件 PDF（使用 reportlab，如果没有则创建文本占位）
python3 << 'EOF'
import sys
from pathlib import Path
# setup.sh 在 test_01_basic 下执行，向上两级到 tests 目录
sys.path.insert(0, str(Path.cwd().parent.parent))
from conftest import generate_mock_lecture_pdf

generate_mock_lecture_pdf(Path("input/lecture.pdf"), title="逻辑导论第一讲")
EOF

echo "OK: Mock 课件已创建到 input/lecture.pdf"

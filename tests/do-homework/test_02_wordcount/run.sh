#!/usr/bin/env bash
# AI Agent 执行步骤

echo "========================================"
echo "test_02_wordcount — AI 执行步骤"
echo "========================================"
echo ""
echo "1. 读取 essay.md"
echo ""
echo "2. 执行字数统计（参考 do-homework.md 第 4 节）："
echo "   python3 -c \""
echo "   import re"
echo "   text = open('essay.md').read()"
echo "   chinese_chars = len([c for c in text if '\\u4e00' <= c <= '\\u9fff'])"
echo "   ..."
echo "   \""
echo ""
echo "3. 将结果写入 wordcount_result.json"
echo ""

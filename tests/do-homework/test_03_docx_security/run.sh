#!/usr/bin/env bash
# AI Agent 执行步骤

echo "========================================"
echo "test_03_docx_security — AI 执行步骤"
echo "========================================"
echo ""
echo "1. 扫描 DOCX 隐藏文字（参考 tools/docx-reader.md）："
echo "   python3 -c \""
echo "   from docx import Document"
echo "   from docx.oxml.ns import qn"
echo "   ..."
echo "   scan_docx_hidden_text('suspicious.docx')"
echo "   \""
echo ""
echo "2. 将扫描结果写入 docx_scan_report.json"
echo ""
echo "3. 若发现 alerts，在 homework_parsed.json 中标注并提示用户"
echo ""

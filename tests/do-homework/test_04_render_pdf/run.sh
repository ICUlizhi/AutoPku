#!/usr/bin/env bash
# AI Agent 执行步骤

echo "========================================"
echo "test_04_render_pdf — AI 执行步骤"
echo "========================================"
echo ""
echo "1. Markdown -> HTML（参考 do-homework.md 第 5 节）："
echo "   python3 -c \""
echo "   import markdown"
echo "   md = open('answer.md').read()"
echo "   html = markdown.markdown(md, extensions=['tables','fenced_code'])"
echo "   ..."
echo "   \""
echo ""
echo "2. Chrome Headless 打印 PDF："
echo '   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \\'
echo '       --headless --print-to-pdf="answer.pdf" "file://..."'
echo ""

#!/usr/bin/env bash
# AI Agent 执行步骤

echo "========================================"
echo "test_05_submit_confirm — AI 执行步骤"
echo "========================================"
echo ""
echo "1. 完成作业渲染，得到 hw5_answer.pdf"
echo ""
echo "2. 调用 AskUserQuestion 进行二次确认："
echo '   AskUserQuestion({'
echo '       "questions": [{'
echo '           "question": "作业已完成渲染。是否提交到教学网？",'
echo '           "options": ['
echo '               {"label": "提交", "value": "submit"},'
echo '               {"label": "仅保存本地", "value": "save_only"}'
echo '           ]'
echo '       }]'
echo '   })'
echo ""
echo "3. 根据用户选择执行："
echo "   - submit      → /tmp/pku3b a submit {assignment_id} hw5_answer.pdf"
echo "   - save_only   → 跳过提交，保留本地文件"
echo ""

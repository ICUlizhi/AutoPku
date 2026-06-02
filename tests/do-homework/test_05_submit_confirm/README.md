# test_05_submit_confirm — 提交前二次确认流程

## 目标
验证 `do-homework.md` 中定义的**提交前二次确认流程**被正确执行，防止 AI 在未经用户同意的情况下自动提交作业。

## 背景
在自动完成作业的 pipeline 中，最后一步（Phase 4: 提交）具有不可逆性。教学网一旦提交，可能无法撤回或修改。因此必须在提交前强制引入用户确认节点。

## 期望流程（AI Agent）

```
Phase 1: 解析作业
Phase 2: 生成解答
Phase 3: 渲染 PDF
    ↓
[AskUserQuestion] 作业渲染完成，是否提交？
    ↓
用户选择 "提交" → 执行 pku3b a submit
用户选择 "仅保存本地" → 跳过提交，保留本地文件
```

## 确认问题规范

AI 必须调用 `AskUserQuestion`，问题结构如下：

```python
AskUserQuestion({
    "questions": [{
        "question": "作业已完成渲染。是否提交到教学网？",
        "options": [
            {"label": "提交", "value": "submit"},
            {"label": "仅保存本地", "value": "save_only"}
        ]
    }]
})
```

## 验收标准
1. **必须有 AskUserQuestion 调用**：不允许 AI 直接执行 `pku3b a submit`
2. **必须提供两个选项**："提交" 和 "仅保存本地"
3. **必须有二次确认文案**：明确告知用户 "作业已完成渲染"
4. **若用户拒绝，不得提交**：选择 "仅保存本地" 后，仅保留 `{course}/作业/{assignment}_answer.pdf`

## 测试方法
本测试用例为**流程测试**，validate.py 主要检查：
- `run.sh` 中是否描述了上述确认步骤
- `README.md` 中是否包含完整的确认流程规范

> 注：真正的 AskUserQuestion 调用发生在 AI Agent 运行时，无法通过静态脚本直接验证，因此本测试侧重于**流程文档完整性**和**规范符合性**。

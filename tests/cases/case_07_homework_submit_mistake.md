# 真实案例 #7：AutoPku 误将 Lab3 代码提交到 Lab2 及恢复

> **来源**: Kimi Session `6aa5954900c0958ddd8010f507e189a6` / Turn `e2dfbbbe-2868-4caa-9e2f-f97f9e7e356a`
> **时间**: 2025-05-18
> **涉及功能**: `homework-submit`（pku3b 提交、误操作恢复、助教备注）

---

## 用户原始输入序列

```
[1] 都做完了就打包吧，然后你在本地找有没有autopku这个skill仓库，用这里面的方式去打包提交

[2] /Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku

[3] 不能交这个lab2啊

[4] 你能加备注吗，告诉助教上次提交是autopku不小心把lab3当lab2交了，这次or第一次是正常的
```

---

## 问题描述

用户在完成 Tacos 操作系统 Lab3（Virtual Memory）后，要求 Agent 使用 AutoPku skill 的方式自动打包并提交作业。过程中发生了以下连锁问题：

1. **找不到 skill**：Agent 在默认 skill 目录搜索 `autopku` 未果
2. **学期限制**：`pku3b` 只能提交当前学期的作业，T-Lab3 不在当前学期，返回 `assignment not found`
3. **误提交**：Agent 在测试 `pku3b a submit` 行为时，将 Lab3 代码包错误提交到了 Tacos Lab2 入口，覆盖了用户之前的 Lab2 代码
4. **需加备注**：用户要求向助教说明误操作情况，但 `pku3b` 不支持提交备注

---

## Agent 执行过程

### Phase 1：定位 AutoPku skill

Agent 首先搜索本地 skill 目录，未找到 `autopku`：

```
Step 1: Shell(find /Users/moonshot/.config/agents/skills ... -name "autopku") → 无结果
Step 2: Shell(find /Users/moonshot -maxdepth 4 -type d -name "autopku") → 无结果
```

用户随后提供了路径 `/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku`，Agent 读取 `skill.md` 了解到：
- 使用 `pku3b` 命令行工具与 PKU 课程系统交互
- 提交流程：`pku3b a ls` → 用户确认 → `pku3b a submit <ID> <file>`
- skill 明确声明：**不自动选择作业**、**不自动提交作业（必须用户确认）**

### Phase 2：尝试提交 T-Lab3

```
Step 3: Shell(pku3b a ls --all-term) → 找到 T-Lab3: Virtual Memory (ID: a34d31eca44d3c43)
Step 4: Shell(pku3b a submit a34d31eca44d3c43 subworkspace/Tacos/submission.tar.bz2)
         → 报错: assignment not found
```

Agent 分析发现：
- `pku3b a ls`（当前学期）**不显示 T-Lab3**
- `pku3b a ls --all-term` 显示 T-Lab3 为 `due`，但它属于历史学期
- `pku3b a submit` 没有 `--term` 参数，只搜索当前学期

### Phase 3：误操作——测试 submit 时交到 Lab2

Agent 为验证 `submit` 命令是否可用，错误地将 Lab3 代码包提交到了 Tacos Lab2：

```
Step 5: Shell(pku3b a submit d228b52b970d91f4 subworkspace/Tacos/submission.tar.bz2)
         → 提交成功（但交错了作业！Lab3 代码交到了 Lab2）
```

**状态变化**：
- 提交前：Tacos Lab2 显示 `已完成: 尝试 26-4-24 下午12:22`
- 提交后：显示 `已完成: 尝试3 (逾期) 26-5-18 下午2:21`

用户立即发现："不能交这个lab2啊"

### Phase 4：恢复 Lab2 + 添加备注

Agent 找到用户之前的 Lab2 提交包 `submission_2200012917.tar.bz2`，执行恢复：

```
Step 6: Shell(cd /tmp/lab2_restore && tar -xjf submission_2200012917.tar.bz2)
Step 7: WriteFile(NOTE_TO_TA.md) → 添加说明文件
Step 8: Shell(tar -cjf submission_2200012917.tar.bz2 $(ls -A))
Step 9: Shell(pku3b a submit d228b52b970d91f4 subworkspace/Tacos/submission_2200012917.tar.bz2)
         → 恢复成功，显示尝试5
```

添加的 `NOTE_TO_TA.md` 内容：

```markdown
# 提交说明

助教您好，

本次提交（以及第一次提交）是正常的 Lab2: User Programs 代码。

上一次提交（尝试3）是误操作——AI 助手在调试 pku3b 时不小心将 Lab3 的代码包
提交到了此处，非常抱歉给您带来的困扰。

请以本次提交或第一次提交为准进行批改。

学号：2200012917
```

---

## 踩坑与经验

### 1. pku3b 的学期限制

| 命令 | 搜索范围 | T-Lab3 可见？ | 可提交？ |
|------|---------|-------------|---------|
| `pku3b a ls` | 当前学期 | ❌ | — |
| `pku3b a ls --all-term` | 所有学期历史 | ✅ (显示为 due) | — |
| `pku3b a submit <ID>` | 当前学期 | — | ❌ `assignment not found` |

**教训**：`--all-term` 能列出历史作业，但 `submit` 命令硬编码只查当前学期。这是 `pku3b` 的固有限制，Agent 不应在测试时随意向其他作业入口提交。

### 2. 测试 submit 命令的风险

Agent 为验证 "submit 是否正常工作"，使用了真实的作业 ID 和文件进行测试，导致：
- Lab3 代码覆盖了 Lab2 的提交
- 提交次数从 "尝试" 变为 "尝试3"
- 用户之前的 Lab2 代码可能丢失

**教训**：
- 测试提交命令前，必须先确认 `<ID>` 和 `<file>` 完全匹配
- 不应使用真实作业做 "命令是否可用" 的探针测试
- 如需测试，应先询问用户确认

### 3. pku3b 不支持备注

`pku3b a submit --help` 显示参数只有 `[ID] [PATH]`，没有 `--message` 或 `--note`。

** workaround**：在提交压缩包内添加 `NOTE_TO_TA.md` 等说明文件，助教下载后可见。

### 4. 恢复策略

当误提交发生后，恢复步骤：
1. 找到该作业之前正确的提交包（如 `submission_2200012917.tar.bz2`）
2. 在包内添加说明文件，解释误操作
3. 重新打包并提交覆盖
4. 向用户如实报告情况

---

## 测试价值

此案例可用于验证 AutoPku 提交模块的以下安全机制：

1. **学期匹配检查**：在调用 `submit` 前，应通过 `ls`（非 `--all-term`）确认目标作业在当前学期是否可见
2. **作业-文件一致性校验**：提交前应比对作业名称和文件内容，防止 "Lab3 代码交到 Lab2"
3. **用户二次确认**：即使 skill 中已声明 "不自动提交"，在测试/调试阶段仍需用户明确确认每一个 submit 操作
4. **误提交恢复流程**：验证能否自动定位历史提交包、添加备注文件、重新提交
5. **备注传递机制**：当平台不支持提交备注时，验证能否通过包内文件实现等效功能

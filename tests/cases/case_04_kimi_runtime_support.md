# 真实案例 #4：为 AutoPku 添加 Kimi Agent Team 支持

> **来源**: Kimi Session `5f91876922590e8cef7197ec2eb3d1a2` / user-history
> **时间**: 2026-04
> **涉及功能**: `runtime/`（跨平台 Agent Team 支持）

---

## 用户原始输入

```
你在 /Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/sub-skills/runtime
里面添加对你的 agent team 的支持，（当然前提是你先理解了这个 skill 体系，
有问题随时和我汇报）
```

## 执行过程

Agent 需要完成以下工作：

1. **理解现有 runtime 体系**：
   - `_detect.md`：环境检测（Claude/Codex/Kimi）
   - `create-agent.md`：统一 Agent 创建接口
   - `claude-team.md`：Claude Code 的 Agent Team 语法
   - `codex-subagent.md`：Codex 的 native subagent 语法
   - `kimi-team.md`：当时尚未编写

2. **分析 Kimi 与 Claude 的差异**：
   - Claude：使用 `Agent()` tool + `SendMessage()` 进行通信
   - Kimi：使用 `Agent()` tool，但**结果直接返回**，无需 `SendMessage`
   - Kimi 支持 `TaskList` / `TaskOutput` 管理后台任务

3. **新增 `kimi-team.md`**：
   - 定义 Kimi 环境下的 Agent Team 语法
   - 提供与 `claude-team.md` 对应的示例

4. **更新 `create-agent.md`**：
   - 添加 Kimi 环境的适配逻辑

5. **验证**：
   - 用户要求 "你再整体检查一下运行逻辑，没问题的话 push 上去吧"

## 关键代码差异

### Claude Code（原实现）

```python
# Agent 创建后，通过 SendMessage 通信
Agent({
    "name": f"{course}-agent",
    "prompt": agent_template.format(**task),
})
# 需要使用 SendMessage 等待结果
```

### Kimi Code CLI（新增实现）

```python
# Agent 结果直接返回，无需 SendMessage
Agent({
    "description": f"处理 {task['course']}",
    "prompt": agent_template.format(**task),
    "subagent_type": "coder"
})
# 结果直接作为返回值
```

## 测试价值

此案例验证 `runtime/` 层的跨平台兼容性：
- `test_01_basic` 等测试用例的 `run.sh` 中需要说明不同运行时的 Agent 创建语法差异
- 验证 Kimi 环境下 Agent Team 是否能正常并行执行
- 验证 Agent 结果是否能正确收集（无需 SendMessage）

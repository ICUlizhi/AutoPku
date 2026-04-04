---
name: autopku
description: 自动获取和整理北京大学课程通知，完成作业并提交
---

> Claude Code 入口。
> 如果你使用 Codex，请改为读取 `codex/autopku/SKILL.md`。

## 前置配置

在执行此 skill 前，需要确保本地 `.claude/settings.local.json` 包含以下配置：

```json
{
  "permissions": {
    "allow": [
      "Skill(update-config)",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(rm -rf:*)"
    ],
    "defaultMode": "bypassPermissions"
  },
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "USER_TYPE": "ant"
  }
}
```

> **说明**：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` 是启用 Agent Team 功能的必需环境变量。

# AutoPku

执行此 skill 来自动获取和整理北京大学课程通知。

## 需要用户提供的信息

- 学号
- 教学网密码

## 执行步骤

### 步骤 1：检查并安装 pku3b

检查 pku3b 是否已安装：
```bash
which pku3b 2>/dev/null || echo "NOT_FOUND"
```

如果未找到，从 GitHub Release 下载（以 macOS Apple Silicon 为例）：
```bash
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.10.3/pku3b-0.10.3-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.10.3-aarch64-apple-darwin.tar.gz
chmod +x pku3b
./pku3b --version
```

> **踩坑记录**：原仓库 `yang-er/pku3b` 已不存在或失效，安装脚本返回 404。正确仓库是 `sshwy/pku3b`：
> - GitHub: https://github.com/sshwy/pku3b

### 步骤 2：登录教学网

pku3b 登录是交互式的，使用 expect 脚本自动输入（避免手动交互）：

```bash
cat > /tmp/pku3b_login.exp << 'EOF'
#!/usr/bin/expect -f
set timeout 30
spawn /tmp/pku3b init
expect "username:"
send "学号\r"
expect "password:"
send "密码\r"
expect eof
EOF
chmod +x /tmp/pku3b_login.exp
/tmp/pku3b_login.exp
```

验证登录：
```bash
/tmp/pku3b a ls
```

> 注意：`pku3b auth status` 和 `pku3b auth login` 命令不存在，正确命令是 `pku3b init`

> **踩坑记录**：`pku3b init` 需要交互式输入学号和密码，直接管道输入不工作（报错 "input device is not a TTY"）。需要使用 expect 脚本自动登录（见上方代码）。

### 步骤 3：获取所有作业数据

获取作业列表（纯文本格式，带 ANSI 颜色码）：
```bash
/tmp/pku3b a ls --all-term > /tmp/pku_assignments_raw.txt
```

> **踩坑记录**：原步骤中提到 `--json` 参数，但实际 pku3b 输出是纯文本格式（带 ANSI 颜色码），不是 JSON。需要使用 Python 正则表达式解析。

> **踩坑记录**：`pku3b a ls -a`（不加 `--all-term`）只显示**有作业的**当前学期课程，会漏掉还没布置作业的课程。如需获取准确课程列表，应使用 `pku3b s show -d major`（主修）和 `pku3b s show -d minor`（辅修）查看选课结果。

解析文本提取课程和作业信息（Python）：
```python
import re
import json

with open('/tmp/pku_assignments_raw.txt', 'r') as f:
    content = f.read()

# 提取课程和作业（格式：ESC[36mESC[1m课程名ESC[0mESC[0m > ESC[36mESC[1m作业名ESC[0mESC[0m (状态)）
pattern = r'\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\x1b\[2m>\x1b\[0m\s+\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\(([^)]+)\)'
matches = re.findall(pattern, content)

assignments = []
for course, assignment, status in matches:
    assignments.append({
        'course': course.strip(),
        'assignment': assignment.strip(),
        'status': status.strip()
    })

# 保存为 JSON 供后续使用
with open('/tmp/pku_assignments.json', 'w') as f:
    json.dump(assignments, f, ensure_ascii=False, indent=2)
```

获取准确的课程列表（从选课系统）：
```bash
# 主修课程
/tmp/pku3b s -d major show > /tmp/major_courses.txt

# 辅修课程（如有）
/tmp/pku3b s -d minor show > /tmp/minor_courses.txt
```

> **踩坑记录**：`pku3b a ls -a` 只显示有作业的课程，会漏掉还没布置作业的课程。必须从 `pku3b s show` 获取完整选课列表。

解析选课结果提取课程名：
```python
import re

with open('/tmp/major_courses.txt', 'r') as f:
    content = f.read()

# 提取已选上的课程（绿色标记）
pattern = r'已选上.*?\x1b\[32m([^\x1b]+)\x1b\[0m'
courses = re.findall(pattern, content)
print(f"主修课程: {courses}")
```

筛选当前学期作业数据：

> **踩坑记录**：`pku3b a ls --all-term` 会返回所有历史学期的作业（可能超过200个），需要筛选出当前学期的。

```python
import re

current_courses = ['课程1', '课程2', ...]  # 从选课结果获取

# 筛选当前学期作业（包含选课系统未选上但有作业的课程）
current_assignments = [
    a for a in assignments 
    if a['course'] in current_courses
]

# 检查是否有"未选上"但有作业的课程
all_courses_in_assignments = set(a['course'] for a in assignments)
missed_courses = all_courses_in_assignments - set(current_courses)
print(f"注意：以下课程不在选课列表但作业系统有记录: {missed_courses}")
```

检查课程是否有附件：

```python
# 检查课程是否有可下载的附件
with open('/tmp/pku_assignments_raw.txt', 'r') as f:
    content = f.read()

# 查找有附件的课程
attachment_pattern = r'\[附件\].*?\x1b\[4m([^\x1b]+)\x1b\[0m'
attachments = re.findall(attachment_pattern, content)
print(f"找到 {len(attachments)} 个附件")
```

### 步骤 4：召唤 Agent Team

请你创建一个agent team，为每个当前学期课程创建一个专属 agent，**并行启动**。

> **踩坑记录**：
> 1. 先确定真正需要处理的**当前学期课程**（可能16门），为每门课程创建一个 Agent，并行执行
> 2. 每个 Agent 独立处理自己的课程目录和通知摘要
> 3. Agent Prompt 要点：
>    - 明确指定工作目录 `test/{课程名}/`
>    - 要求 Agent 读取 `/tmp/pku_assignments.json`
>    - 要求 Agent 筛选对应课程的作业
>    - 要求创建 `作业/`、`通知/`、`资料/` 三个子目录
>    - 要求生成 `通知摘要.md`

**Agent 名称：** `{course_name}-agent`

**Agent Prompt 模板（生成通知摘要）：**
```
你是课程 "{course_name}" 的专属 agent。

工作目录：/Users/xxx/test

你的任务：
1. 读取 /tmp/pku_assignments.json
2. 使用 Bash 运行 `/tmp/pku3b a ls --all-term` 获取原始数据
3. 筛选 course 字段匹配 "{course_name}" 的作业
4. 创建目录结构：
   test/{course_name}/
   ├── 作业/
   ├── 通知/
   ├── 资料/
   └── 通知摘要.md

5. 下载作业附件（如果有）：
   - 运行 `/tmp/pku3b a download <作业ID> -d test/{course_name}/作业/`
   - 注意：如果没有附件，命令会返回 Done. 但不会创建文件
   - 下载完成后检查目录是否为空

6. 生成 "test/{course_name}/通知摘要.md"，包含：
   - 课程统计（总作业数、待交作业数、已完成数、逾期数）
   - 待完成作业列表（带 🔴🟡🟢 紧急程度标识）
   - 逾期作业列表
   - 已完成作业列表
   - 下载的文件列表（如果有）
   - 最新通知

7. 返回执行摘要：
   - 找到的作业数量
   - 待交作业数量
   - 下载的文件数量
   - 创建的文件路径

注意：
- 使用 Bash 工具执行 pku3b 命令
- 使用 Python 处理 JSON 数据
- 清理 ANSI 颜色码（re.sub(r'\x1b\[[0-9;]*m', '', status)）
- 确保目录存在（os.makedirs(..., exist_ok=True)）
- 如果课程在教学网中找不到作业，报告"教学网无该课程作业"
```

**Agent Prompt 模板（完成作业并提交）：**
```
你是课程 "{course_name}" 的作业完成专家 agent。

你的任务是为 "{course_name}" 完成并提交作业 "{assignment_name}"。

工作目录：/Users/xxx/test/{course_name}

## 作业信息
- 课程：{course_name}
- 作业：{assignment_name}
- 作业ID：{assignment_id}
- 截止时间：{deadline}
- 要求：{requirements}

## 执行步骤

### 步骤1：下载作业要求和附件
```bash
/tmp/pku3b a download {assignment_id} -d /Users/xxx/test/{course_name}/作业/
```

检查下载的文件，阅读作业要求。

### 步骤2：完成作业
根据作业要求完成作业内容：
- 如果是编程题：编写代码并测试
- 如果是论文/报告：撰写文档
- 如果是选择题/填空题：完成答题

将完成的作业文件保存到：/Users/xxx/test/{course_name}/作业/

### 步骤3：提交作业
```bash
/tmp/pku3b a submit {assignment_id} -f /Users/xxx/test/{course_name}/作业/完成的作品文件
```

注意：
- 确保提交的文件格式正确
- 提交前检查文件是否完整
- 记录提交结果

### 步骤4：验证提交
```bash
/tmp/pku3b a ls | grep "{assignment_name}"
```
确认作业状态变为"已完成"或有提交记录。

## 返回执行摘要
- 作业完成状态：成功/失败
- 提交文件路径
- 提交时间
- 任何错误或警告信息

## 注意事项
- 使用 Bash 工具执行 pku3b 命令
- 使用 Read/Edit/Write 工具处理作业文件
- 如果无法完成作业，说明原因并报告进度
- 确保在截止时间前提交
```

---

## Agent Team 作业完成与提交流程（本地PDF模式）

适用于本地已有作业PDF文件的场景，**不依赖教学网下载**。

### 使用场景
- 作业PDF已在本地（如 `/test/{课程}/作业/Homework202605.pdf`）
- 需要通过代码解析PDF（不直接读取）
- 本地完成作业后保存到 `/test/{课程}/提交/` 目录

### Agent Team 结构

| Agent 角色 | 职责 | 关键约束 |
|-----------|------|---------|
| **coordinator** | 任务分配、流程控制、结果汇总 | 协调4个子agent按序执行 |
| **pdf_parser** | 使用Python代码间接解析PDF | **禁止直接读取PDF**，必须使用代码提取 |
| **solver** | 根据解析的题目和资料完成解答 | 逐题解答，参考 `/资料/` 目录 |
| **writer** | 将答案格式化为提交文档 | 生成PDF或Markdown |
| **submitter** | 保存最终文件到提交目录 | 命名格式：`Homework{编号}_answer.pdf` |

### 执行流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ coordinator │────▶│ pdf_parser  │────▶│   solver    │────▶│   writer    │────▶│  submitter  │
│  (协调者)    │     │ (PDF解析器)  │     │  (解题者)    │     │  (撰写者)    │     │  (提交者)    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                   │                   │                   │
      │              使用代码解析PDF            逐题解答             格式化答案           保存到
      │              提取题目内容              参考资料              生成文档          提交目录
```

### Coordinator Prompt 模板

```
你是 Coordinator，负责协调 agent team 完成 {course_name} 的 {assignment_id} 作业。

## 工作目录
{base_dir}/test/{course_name}

## 作业文件
{base_dir}/test/{course_name}/作业/{pdf_filename}

## 执行计划

### Phase 1: PDF 解析（指派 pdf_parser）
发送消息给 pdf_parser，要求：
1. 使用 Python 代码（pdfplumber/PyPDF2）解析 {pdf_path}
2. **禁止直接读取PDF文件**，必须通过代码间接提取
3. 返回解析出的题目内容（按题号组织）

### Phase 2: 解题（指派 solver）
接收到 pdf_parser 的结果后，发送消息给 solver，要求：
1. 根据解析的题目逐题解答
2. 参考 {base_dir}/test/{course_name}/资料/ 目录下的文件
3. 返回每道题的详细解答过程

### Phase 3: 格式化（指派 writer）
接收到 solver 的答案后，发送消息给 writer，要求：
1. 将答案整理为美观的提交格式
2. 生成 Markdown 或 PDF 文件
3. 返回文件路径

### Phase 4: 提交（指派 submitter）
接收到 writer 的文件后，发送消息给 submitter，要求：
1. 将最终文件复制到 {base_dir}/test/{course_name}/提交/
2. 文件命名为 {output_filename}
3. 返回提交结果

## 通信规则
- 使用 SendMessage 工具与其他 agent 通信
- 等待每个 phase 完成后再进行下一个
- 汇总所有 agent 的执行结果
- 如果某 phase 失败，报告错误并停止

## 返回最终报告
- 作业完成情况
- 各 agent 执行状态
- 最终提交文件路径
- 遇到的问题（如有）
```

### PDF Parser Prompt 模板

```
你是 PDF Parser，负责使用代码间接解析作业 PDF。

## 任务
解析 PDF 文件：{pdf_path}

## 约束条件
**绝对禁止直接读取 PDF 文件！必须使用 Python 代码间接提取内容。**

## 执行步骤
1. 检查 PDF 文件是否存在
2. 使用 Python 代码（推荐 pdfplumber）提取文本：

```python
import pdfplumber
import json

def extract_homework_content(pdf_path):
    content = {
        'pages': [],
        'problems': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            content['pages'].append({
                'page_num': i + 1,
                'text': text
            })
    
    # 尝试按题号分割题目（根据常见格式）
    full_text = '\n'.join(p['text'] for p in content['pages'])
    
    # 提取题目（支持多种格式：1. / 1、 / Problem 1 / 第1题）
    import re
    # 匹配题号模式
    problem_pattern = r'(?:^|\n)\s*(?:Problem\s*)?(\d+)[\.、\)]\s*([^\n]+)(.*?)(?=\n(?:\d+|Problem|\Z))'
    matches = re.findall(problem_pattern, full_text, re.DOTALL | re.IGNORECASE)
    
    if not matches:
        # 备选：简单按数字分段
        problem_pattern = r'\n(\d+)\s*\n(.*?)(?=\n\d+\s*\n|$)'
        matches = re.findall(problem_pattern, '\n' + full_text, re.DOTALL)
    
    for num, title, body in matches:
        content['problems'].append({
            'number': num.strip(),
            'title': title.strip() if title else '',
            'content': body.strip() if body else ''
        })
    
    # 保存解析结果
    output_path = '{output_json_path}'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    return content, output_path

# 执行
content, output_path = extract_homework_content('{pdf_path}')
print(f"解析完成，找到 {len(content['problems'])} 道题目")
print(f"结果保存到: {output_path}")
```

3. 验证解析结果：
   - 确认提取了完整的题目内容
   - 检查题号是否连续
   - 如有问题，尝试调整正则表达式

## 返回结果
- 解析出的题目数量
- 每道题的简要摘要
- 输出 JSON 文件路径
- 解析过程中遇到的问题
```

### Solver Prompt 模板

```
你是 Solver，负责根据解析的题目和资料完成作业。

## 输入
已解析的题目数据：{parsed_problems_json_path}

## 参考资料目录
{base_dir}/test/{course_name}/资料/

## 执行步骤

1. 读取解析的题目 JSON 文件

2. 检查参考资料目录，读取所有相关文件：
   - PDF 文件（如有需要，使用代码提取）
   - Markdown/文本文件
   - 图片文件

3. 逐题解答：
   - 理解题目要求
   - 列出关键公式/概念
   - 给出详细推导过程
   - 得出最终答案
   - 标注使用的参考资料

4. 将答案组织为结构化格式：

```json
{
  "answers": [
    {
      "problem_number": "1",
      "problem_summary": "题目简述",
      "solution_steps": ["步骤1", "步骤2", ...],
      "key_formulas": ["公式1", "公式2"],
      "final_answer": "最终答案",
      "references": ["资料文件名"]
    },
    ...
  ]
}
```

5. 保存答案 JSON：
   路径：{answers_json_path}

## 约束条件
- 每道题必须有完整推导过程
- 必须标注使用的参考资料
- 如遇到无法解答的题目，说明原因
- 确保数学公式使用 LaTeX 格式

## 返回结果
- 完成的题目数量
- 每道题的答案摘要
- 答案 JSON 文件路径
- 遇到的困难（如有）
```

### Writer Prompt 模板

```
你是 Writer，负责将答案格式化为美观的提交文档。

## 输入
答案数据：{answers_json_path}
原始题目：{parsed_problems_json_path}

## 输出要求
生成 Markdown 文档，最终转换为 PDF（如需）

## 文档格式

```markdown
# {course_name} - {assignment_id} 作业答案

**姓名：** ____________  
**学号：** ____________  
**日期：** {date}

---

## 第 1 题

**题目：** {problem_content}

**解答：**

{detailed_solution}

**答案：** {final_answer}

---

## 第 2 题

...
```

## 执行步骤

1. 读取答案 JSON 和题目 JSON
2. 为每道题生成格式化的解答
3. 添加 LaTeX 公式支持（使用 $...$ 和 $$...$$）
4. 保存 Markdown 文件：{output_md_path}
5. （可选）使用 Python 转换为 PDF：

```python
# 使用 markdown-pdf 或其他工具
import markdown
from weasyprint import HTML, CSS

with open('{output_md_path}', 'r', encoding='utf-8') as f:
    md_content = f.read()

html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
html_full = f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: "Noto Serif CJK SC", serif; margin: 40px; line-height: 1.8; }}
h1 {{ text-align: center; }}
h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
.math {{ font-style: italic; }}
</style>
</head>
<body>
{html}
</body>
</html>
'''

HTML(string=html_full).write_pdf('{output_pdf_path}')
```

## 返回结果
- 生成的文档路径
- 文档页数/字数统计
- 格式说明（如使用了特殊排版）
```

### Submitter Prompt 模板

```
你是 Submitter，负责将完成的作业保存到提交目录。

## 输入
完成的作业文件：{completed_file_path}

## 目标目录
{base_dir}/test/{course_name}/提交/

## 执行步骤

1. 验证输入文件存在且非空
2. 检查目标目录是否存在，不存在则创建
3. 复制文件到目标目录，命名为：{final_filename}
4. 验证复制成功：
   - 文件大小一致
   - 文件可读

4. （可选）生成提交记录：

```json
{
  "course": "{course_name}",
  "assignment": "{assignment_id}",
  "submitted_file": "{final_filename}",
  "submitted_at": "{timestamp}",
  "file_size": "{size}",
  "status": "success"
}
```

保存到：{submission_record_path}

## 返回结果
- 提交状态（成功/失败）
- 提交文件路径
- 文件大小
- 提交时间
- 备注（如覆盖了已有文件）
```

### 一键启动 Prompt

```
请创建 agent team 完成 {course_name} 的 {assignment_id} 作业。

## 路径信息
- 作业PDF：{base_dir}/test/{course_name}/作业/{pdf_filename}
- 资料目录：{base_dir}/test/{course_name}/资料/
- 提交目录：{base_dir}/test/{course_name}/提交/
- 输出文件：{final_filename}

## Agent Team 配置

创建以下 agents：
1. **{course_name}-coordinator**：协调者，负责整体流程
2. **{course_name}-parser**：PDF解析器，使用代码间接解析PDF
3. **{course_name}-solver**：解题者，参考资料完成所有题目
4. **{course_name}-writer**：撰写者，格式化答案为提交文档
5. **{course_name}-submitter**：提交者，保存到提交目录

## 执行要求

1. coordinator 按 Phase 1-4 顺序协调各 agent
2. pdf_parser **必须使用 Python 代码解析 PDF**，禁止直接读取
3. solver 必须参考 `/资料/` 目录完成解答
4. writer 生成美观的提交文档
5. submitter 保存到 `/提交/` 目录

## 返回最终报告
- 各 agent 执行状态
- 解析的题目数量
- 完成的题目数量
- 最终提交文件路径
- 总耗时
```

**并行策略**：

工作目录：/Users/xxx/test

你的任务：
1. 读取 /tmp/pku_assignments.json
2. 使用 Bash 运行 `/tmp/pku3b a ls --all-term` 获取原始数据
3. 筛选 course 字段匹配 "{course_name}" 的作业
4. 创建目录结构：
   test/{course_name}/
   ├── 作业/
   ├── 通知/
   ├── 资料/
   └── 通知摘要.md

5. 下载作业附件（如果有）：
   - 运行 `/tmp/pku3b a download <作业ID> -d test/{course_name}/作业/`
   - 注意：如果没有附件，命令会返回 Done. 但不会创建文件
   - 下载完成后检查目录是否为空

6. 生成 "test/{course_name}/通知摘要.md"，包含：
   - 课程统计（总作业数、待交作业数、已完成数、逾期数）
   - 待完成作业列表（带 🔴🟡🟢 紧急程度标识）
   - 逾期作业列表
   - 已完成作业列表
   - 下载的文件列表（如果有）
   - 最新通知

7. 返回执行摘要：
   - 找到的作业数量
   - 待交作业数量
   - 下载的文件数量
   - 创建的文件路径

注意：
- 使用 Bash 工具执行 pku3b 命令
- 使用 Python 处理 JSON 数据
- 清理 ANSI 颜色码（re.sub(r'\x1b\[[0-9;]*m', '', status)）
- 确保目录存在（os.makedirs(..., exist_ok=True)）
- 如果课程在教学网中找不到作业，报告"教学网无该课程作业"
```

**并行策略**：
```python
# 为每个课程创建一个 Agent 调用
for course in current_semester_courses:
    # 并行执行，不要等待上一个完成
    Agent(prompt=f"...{course}...")
```

### 步骤 5：处理特殊课程

**检查"未选上"但有作业的课程**：

```python
# 找出作业系统中有但选课系统中没有的课程
all_courses_in_assignments = set(a['course'] for a in assignments)
courses_in_syllabus = set(current_courses)
missed_courses = all_courses_in_assignments - courses_in_syllabus

if missed_courses:
    print(f"⚠️ 以下课程在选课系统显示'未选上'但作业系统有记录: {missed_courses}")
    # 为这些课程也创建 Agent 处理
    for course in missed_courses:
        # 并行创建 Agent，见步骤4
```

### 步骤 6：生成汇总报告

所有 agent 完成后，创建 "通知摘要汇总.md"：

```python
import json
from datetime import datetime

# 读取所有 agent 生成的数据
with open('/tmp/pku_assignments.json', 'r') as f:
    assignments = json.load(f)

# 统计信息
total_courses = len(current_semester)
total_unfinished = sum(1 for a in assignments if '已完成' not in a['status'])
urgent = [a for a in assignments if 'in' in a['status'] and ('h' in a['status'] or 'd' in a['status'])]

report = f"""# PKU 课程通知汇总

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 紧急任务（7天内截止）
| 课程 | 作业 | 截止时间 | 状态 |
|-----|------|---------|------|
"""

for a in urgent[:10]:  # 显示前10个
    report += f"| {a['course']} | {a['assignment']} | - | {a['status']} |\n"

report += f"""
## 各课程统计
- 课程A：X个待交作业
- ...

## 创建的文件结构
```
test/
├── 通知摘要汇总.md
├── {course1}/
│   ├── 作业/
│   ├── 通知/
│   ├── 资料/
│   └── 通知摘要.md
└── ...
```

---
*由 AutoPku 自动生成*
"""

with open('test/通知摘要汇总.md', 'w') as f:
    f.write(report)
```

### 步骤 7：输出最终报告

显示完成摘要：
```
[AutoPku] 完成！

课程总数：{N} 门
待交作业总数：{M}
紧急（7天内）：{X}
下载文件数：{Y}

课程摘要：
- {course1}: {n1}个待交
- {course2}: {n2}个待交
...

⚠️ 特殊情况：
  • {课程名}: 选课系统显示"未选上"但作业系统有记录，请确认课程状态
  • {课程名}: 教学网无作业（可能使用Canvas/微信群）
  • {课程名}: 作业无附件（代码提交类）

⚠️ 紧急提醒：
  • xxx 作业仅剩 X 小时！
  • xxx 作业 Y 天内截止（逾期有惩罚）

创建的文件：
- {course1}/通知摘要.md
- {course2}/通知摘要.md
- {course1}/作业/xxx.pdf (如有附件)
- ...
- 通知摘要汇总.md
```

## 需要的权限

- Bash 执行权限（运行 pku3b 命令）
- 文件读写权限（创建目录和文件）
- Agent 创建权限（并行处理各课程）

## 注意事项

- 如果 pku3b 登录失败，提示用户检查学号和密码
- 如果没有找到作业，报告"未找到通知"
- 安全处理课程名称中的特殊字符

## 踩坑记录与解决方案

### 1. 课程筛选遗漏问题

**问题**："学术英语写作"在选课系统中显示"未选上"，但作业系统中有8个作业记录。

**原因**：Agent 只筛选了选课系统中"已选上"的课程，遗漏了这种状态不一致的课程。

**解决方案**：
```python
# 正确的筛选逻辑
1. 从选课系统获取"已选上"的课程列表
2. 额外检查作业列表中是否有其他课程（可能状态不一致）
3. 对于"未选上"但有作业的课程，在报告中特别标注提醒用户
```

### 2. 作业附件下载问题

**问题**：下载 Agent 报告"未找到课程"或"下载0个文件"。

**原因分析**：
| 情况 | 说明 | 示例课程 |
|------|------|----------|
| 作业无附件 | 作业是提交类（代码/PDF），无下载内容 | 操作系统（实验班）|
| 教学网无作业 | 课程使用其他平台（Canvas/微信群）| 哲学导论、逻辑导论 |
| 教学网无记录 | 体育课通常不录视频/无在线作业 | 太极拳 |

**检查方法**：
```bash
# 检查课程是否有附件
grep "课程名" /tmp/pku_assignments_raw.txt | grep "附件"

# 检查课程在视频回放中是否存在
/tmp/pku3b v ls | grep "课程名"
```

### 3. Agent Team 最佳实践

**并行创建 Agent**：
```python
# 为每个课程并行创建 Agent，不要等待
for course in current_semester_courses:
    Agent(prompt=f"处理{course}...", name=f"{course}-agent")
```

**Agent Prompt 要点**：
- 明确指定工作目录 `test/{课程名}/`
- 要求使用 Bash 工具执行 pku3b 命令
- 要求验证下载结果并报告统计信息

### 4. 下载命令使用

```bash
# 下载指定作业到指定目录
/tmp/pku3b a download <作业ID> -d <目标目录>

# 注意：如果没有附件，命令返回 Done. 但不会创建文件
# 需要检查目录是否为空来判断是否有附件
```

### 5. 视频回放下载

如需下载课程视频：
```bash
# 列出视频
/tmp/pku3b v ls

# 下载视频
/tmp/pku3b v download <视频ID> -d <目标目录>
```

## 改进建议

1. **课程状态检查**：在生成报告时，对比选课系统和作业系统的课程列表，标记不一致的情况
2. **附件预检查**：在创建下载 Agent 前，先检查课程是否有附件，避免不必要的 Agent 创建
3. **视频下载**：可考虑为每门课程同时下载课程回放视频到 `资料/` 目录

---

## 附录：完整作业流程（写作业 → 渲染 → 提交）

### Phase 5: 渲染（Markdown → PDF）

在 writer 生成 Markdown 后，需要转换为 PDF 格式以便提交。

#### Renderer Prompt 模板

```
你是 Renderer，负责将 Markdown 答案文档渲染为 PDF 格式。

## 输入
Markdown 文件：{md_path}

## 输出
PDF 文件：{pdf_path}

## 执行步骤

### 方法1：使用 Chrome Headless（推荐）
```bash
# 先安装 markdown 模块
pip3 install markdown

# 生成 HTML
python3 << 'PYEOF'
import markdown
import sys
sys.path.insert(0, '/Users/moonshot/Library/Python/3.9/lib/python/site-packages')

with open('{md_path}', 'r', encoding='utf-8') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

html_full = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: "Noto Serif CJK SC", "SimSun", serif; margin: 40px; line-height: 1.8; }
h1 { text-align: center; border-bottom: 2px solid #333; }
h2 { border-bottom: 1px solid #ccc; margin-top: 30px; }
</style>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>''' + html_body + '''</body></html>'''

with open('{html_path}', 'w', encoding='utf-8') as f:
    f.write(html_full)
print("HTML generated")
PYEOF

# 使用 Chrome 转换为 PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu \
    --print-to-pdf="{pdf_path}" \
    --run-all-compositor-stages-before-draw \
    "file://{html_path}"
```

### 方法2：使用 WeasyPrint
```bash
pip install weasyprint
python3 -c "
import markdown
from weasyprint import HTML

with open('{md_path}', 'r') as f:
    md = f.read()
html = markdown.markdown(md, extensions=['tables'])
HTML(string=html).write_pdf('{pdf_path}')
"
```

## 返回结果
- PDF 文件路径
- 文件大小
- 渲染状态
```

### Phase 6: 提交到教学网

将生成的 PDF 提交到北京大学教学网。

#### Portal Submitter Prompt 模板

```
你是 Portal Submitter，负责将完成的作业提交到教学网。

## 前置条件
- pku3b 已安装并登录
- 作业 PDF 已生成

## 输入
- PDF 文件路径：{pdf_path}
- 课程名称：{course_name}
- 作业编号/名称：{assignment_name}

## 执行步骤

1. **查找作业 ID**
```bash
/tmp/pku3b a ls --all-term | grep -i "{course_name}"
```

从输出中提取目标作业的 ID（格式如：`e0c401873622b44b`）。

2. **验证文件**
```bash
ls -la "{pdf_path}"
```

3. **提交作业**
```bash
/tmp/pku3b a submit <作业ID> "{pdf_path}"
```

注意：命令格式为 `pku3b a submit [ID] [PATH]`，不要使用 `-f` 参数。

4. **验证提交**
```bash
/tmp/pku3b a ls --all-term | grep -i "{assignment_name}"
```

确认作业状态变为"已完成"。

## 返回结果
- 提交状态（成功/失败）
- 作业 ID
- 提交时间
- 错误信息（如有）
```

### 用户确认步骤（重要）

在执行作业流程前，**必须**先向用户确认要完成的作业信息：

#### 确认流程

1. **列出该课程所有待交作业**
```bash
/tmp/pku3b a ls --all-term | grep -i "{course_name}"
```

2. **使用 AskUserQuestion 工具询问用户**

```python
AskUserQuestion({
    "questions": [{
        "question": "该课程有多个待交作业，请选择要完成的作业：",
        "options": [
            {"label": "第一次习题 (截止: 3天后)", "value": "hw1"},
            {"label": "第二次习题 (截止: 5天后)", "value": "hw2"},
            {"label": "第三次习题 (截止: 7天后)", "value": "hw3"}
        ],
        "multiSelect": False
    }]
})
```

3. **确认本地PDF文件存在**
```bash
ls -la "{base_dir}/test/{course_name}/作业/Homework*.pdf"
```

4. **二次确认**
```python
AskUserQuestion({
    "questions": [{
        "question": "确认要为 {course_name} 完成 {assignment_name} 吗？",
        "options": [
            {"label": "确认开始", "value": "confirm"},
            {"label": "取消", "value": "cancel"}
        ],
        "multiSelect": False
    }]
})
```

#### 注意事项

- **禁止自动选择**：不要默认选择最新或最先截止的作业
- **必须明确确认**：用户明确选择后才能创建 agent team
- **提供作业信息**：显示截止时间、当前状态等信息帮助用户决策
- **支持取消**：用户选择取消时，优雅退出并报告"用户取消操作"

### 一键完成完整流程

```
请创建 agent team 完成 {course_name} 的 {assignment_id}，包含完整的写作业、渲染、提交流程。

## 路径信息
- 作业PDF：{base_dir}/test/{course_name}/作业/{pdf_filename}
- 资料目录：{base_dir}/test/{course_name}/资料/
- 提交目录：{base_dir}/test/{course_name}/提交/

## Agent Team 配置

创建以下 agents 按顺序执行：

1. **{course_name}-parser**：使用代码解析 PDF，提取题目
2. **{course_name}-solver**：逐题解答，参考资料目录
3. **{course_name}-writer**：生成 Markdown 答案文档
4. **{course_name}-renderer**：将 Markdown 渲染为 PDF
5. **{course_name}-portal-submitter**：提交 PDF 到教学网

## 执行流程

Phase 1: parser → 生成 homework_parsed.json
Phase 2: solver → 生成 answers.json
Phase 3: writer → 生成 HomeworkXXXX_answer.md
Phase 4: renderer → 生成 HomeworkXXXX_answer.pdf
Phase 5: portal-submitter → 提交到教学网

## 返回最终报告
- 各 phase 执行状态
- 解析/完成/提交的题目数量
- 最终 PDF 路径
- 教学网提交状态
- 总耗时
```

### 完整执行示例（简明量子力学 hw5）

```bash
# 1. 创建 agent team
skill: autopku 简明量子力学 hw5

# 2. 等待各 phase 完成
# Phase 1: 解析 Homework202605.pdf → homework_parsed.json
# Phase 2: 解答 5 道题目 → answers.json
# Phase 3: 生成 Markdown → Homework202605_answer.md
# Phase 4: 渲染 PDF → Homework202605_answer.pdf (1.2MB)
# Phase 5: 提交到教学网 → 成功提交至"第五次习题"

# 3. 验证提交
/tmp/pku3b a ls --all-term | grep "简明量子力学"
# 输出：简明量子力学 > 第五次习题 (已完成)
```

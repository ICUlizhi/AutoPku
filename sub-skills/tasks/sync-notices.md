---
name: autopku-task-sync-notices
description: 同步PKU课程通知，为每门课程创建目录结构和摘要
---

# 任务：同步课程通知

在 AutoPku 桌面端中，如果用户只说“同步通知”“看看有什么作业”“DDL”等短请求，必须先执行本任务的 pku3b 读取步骤。不要只基于旧会话、旧摘要或目录里的缓存文件回答。如果本轮当前终端里没有实际调用这些 pku3b 命令，就不能声称完成同步，必须先调用或报告具体失败命令和原因。

## 执行步骤

### 1. 检查并安装 pku3b

```bash
PKU3B="$(command -v pku3b || true)"
test -n "$PKU3B" || echo "NOT_FOUND"
```

如未安装，按 `tools/pku3b-setup.md` 安装。

### 2. 登录教学网

如果 `pku3b a ls` 提示未登录或凭证失效，在当前嵌入式 Kimi Code 终端运行 `pku3b init`，需要账号、密码、验证码时直接向用户追问。不要生成 expect 脚本或明文密码文件。

### 3. 获取数据

```bash
pku3b ct -r > /tmp/pku_course_table_raw.json
pku3b a ls --all-term > /tmp/pku_assignments_raw.txt
pku3b ann ls > /tmp/pku_announcements_raw.txt
pku3b s -d major show > /tmp/major_courses.txt 2>/dev/null || true
```

### 4. 解析数据

```python
import re
import json

# 解析作业
with open('/tmp/pku_assignments_raw.txt') as f:
    raw = f.read()
pattern = r'\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\x1b\[2m>\x1b\[0m\s+\x1b\[36m\x1b\[1m([^\x1b]+?)\x1b\[0m\x1b\[0m\s+\(([^)]+)\)'
assignments = [{'course': c.strip(), 'assignment': a.strip(), 'status': s.strip()}
               for c, a, s in re.findall(pattern, raw)]

with open('/tmp/pku_assignments.json', 'w') as f:
    json.dump(assignments, f, ensure_ascii=False, indent=2)

# 解析课程
try:
    with open('/tmp/major_courses.txt') as f:
        courses = re.findall(r'已选上.*?\x1b\[32m([^\x1b]+)\x1b\[0m', f.read())
except:
    courses = list(set(a['course'] for a in assignments))
```

### 5. 并行处理课程

为主 skill 提供 agent 配置，由主 skill 统一创建：

```python
agent_configs = []
for course in courses:
    agent_configs.append({
        "name": f"{course}-agent",
        "task": f"""
你是课程 "{course}" 的专属 agent。

工作目录：{base_dir}/{course}/

任务：
1. 创建目录：作业/、通知/、资料/
2. 读取 /tmp/pku_assignments.json，筛选 course="{course}" 的作业
3. 下载附件（如有）：pku3b a download <ID> -d {course}/作业/
4. 生成 {course}/通知摘要.md：
   - 统计：总作业数、待交、已完成、逾期
   - 待完成作业（🔴紧急<1天 🟡临期<7天 🟢正常）
   - 逾期列表、已完成列表
   - 下载文件列表

返回：找到X个作业，待交Y个，下载Z个文件
"""
    })

# 由主 skill 根据 RUNTIME 环境统一创建 agents
# create_agents(agent_configs)
```

### 6. 生成汇总报告

```python
from datetime import datetime

report = f"""# PKU 课程通知汇总
生成时间：{datetime.now():%Y-%m-%d %H:%M}

## 统计
- 课程数：{len(courses)}
- 总作业：{len(assignments)}
- 待交：{sum(1 for a in assignments if '已完成' not in a['status'])}

*由 AutoPku 自动生成*
"""

with open(f'{base_dir}/通知摘要汇总.md', 'w') as f:
    f.write(report)
```

## 输出

- `test/通知摘要汇总.md`
- `test/{course}/通知摘要.md`
- `test/{course}/作业/`（附件）

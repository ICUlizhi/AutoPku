# AutoPku Test Suite

AutoPku 功能回归测试框架。每个测试用例采用类似 OJ（Online Judge）题目的格式组织，包含题目描述、前置条件、输入数据、期望输出和验证脚本。

## 设计理念

AutoPku 是 **AI-Native** 系统——核心执行逻辑由 AI Agent 在读取 skill 文档后自行完成。因此本测试框架采用**半自动化**策略：

- **机器负责**：环境准备、数据构造、输出验证
- **AI Agent 负责**：按测试步骤执行 skill 逻辑（模拟真实用户交互）

## 目录结构

```
tests/
├── README.md              # 本文件
├── conftest.py            # 公共工具函数
├── run_all.py             # 一键运行所有测试
├── sync-notices/          # 同步通知测试
├── do-homework/           # 完成作业测试
├── write-notes/           # 撰写笔记测试
├── write-paper/           # 撰写论文测试
└── make-slides/           # 生成幻灯片测试
```

## 测试用例格式

每个测试用例是一个独立目录，内部结构如下：

```
test_XX_名称/
├── README.md          # 题目描述（场景、前置条件、输入、期望输出）
├── setup.sh           # 环境准备（创建 mock 数据、目录结构）
├── run.sh             # 执行步骤（供 AI Agent 按步骤执行）
├── validate.py        # 输出验证（检查文件、内容、格式）
└── fixtures/          # 测试数据（PDF、mock ANSI 输出等）
```

### README.md 模板

```markdown
# 测试：XXX

## 场景描述
...

## 前置条件
- ...

## 输入
- 用户意图："..."
- 测试数据：fixtures/xxx.pdf

## 期望输出
1. 文件结构：...
2. 内容检查：...
3. 边界条件：...

## 验证命令
```bash
python validate.py
```
```

## 运行方式

### 单个测试

```bash
cd tests/write-notes/test_01_basic
bash setup.sh
# 按 run.sh 中的步骤，让 AI Agent 执行 skill
python validate.py
```

### 全部测试

```bash
cd tests
python run_all.py
```

## 测试分类

| 功能模块 | 测试数量 | 核心场景 |
|---------|---------|---------|
| sync-notices | 3 | 单课程同步、多课程并行、空数据 |
| do-homework | 5 | PDF解析、字数统计、DOCX安全、渲染PDF、提交确认 |
| write-notes | 5 | PDF→笔记、Callout包含、公式渲染、字体、多文件合并 |
| write-paper | 4 | LaTeX/Word双模式、图片绘制、参考文献、模板替换 |
| make-slides | 3 | 课件→幻灯片、模板编译、中文渲染 |

## 从 Kimi Session 提取的踩坑场景

以下场景直接来自真实使用中的问题，已转化为测试用例：

1. **笔记 Callout 丢失** → `write-notes/test_03_callout`
2. **笔记 PDF 重复渲染**（110页被渲染两次）→ `write-notes/test_05_idempotent`
3. **模态逻辑公式渲染错误**（xRy 符号）→ `write-notes/test_04_formula`
4. **宋体字体渲染异常** → `write-notes/test_02_font`
5. **论文字数统计不准确** → `do-homework/test_02_wordcount`
6. **DOCX 隐藏文字未扫描** → `do-homework/test_03_docx_security`
7. **论文图片搜索缺失** → `write-paper/test_03_images`

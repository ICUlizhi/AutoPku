# 测试：make-slides — 课件 → 幻灯片基础流程

## 场景描述
用户要求基于课件生成汇报幻灯片。Agent 应正确检测课件、提取内容、生成 slides 目录结构。

## 前置条件
- 课程目录已存在
- lectures/ 下有课件 PDF

## 输入
- 用户意图: `"给逻辑导论做个汇报PPT"`
- 测试数据: test00/逻辑导论/lectures/lecture1.pdf、lecture2.pdf（模拟课件）

## 期望输出
1. `slides/` 目录结构完整（含 `main.typ`、`outline.md`、`figures/`）
2. `main.typ` 存在且非空
3. `outline.md` 存在且包含大纲内容

## 验证命令
```bash
python validate.py
```

# 测试：write-paper — 图片搜索与绘制（踩坑回归）

## 场景描述
真实踩坑记录：某次论文生成流程中，大纲已规划了配图（如数据图表、框架图），
但 Agent 在执行时未引用 `image-handler` 工具搜索或绘制图片，导致最终论文
`figures/` 目录为空或不存在。

本测试验证：当大纲中明确要求配图时，Agent 必须执行图片获取/绘制阶段。

## 前置条件
- 大纲中已规划至少 1 张配图

## 输入
- 用户意图: `"给科技创新实践写课程论文"`
- 模拟课程: `test00/科技创新实践/`
- 大纲中规划了配图：`figures/fig1_framework.png`（概念框架图）

## 期望输出
1. `test00/科技创新实践/论文/figures/` 目录存在
2. 目录中至少有一张图片（.png / .jpg / .jpeg / .pdf）
3. 图片在 paper.tex / paper.docx 中被引用

## 踩坑记录
> autopku 的流程中没有明确要求 Agent 去搜索获取图片，
> 需要在大纲生成后主动检查 `images` 字段并触发 image-handler。

## 验证命令
```bash
python validate.py
```

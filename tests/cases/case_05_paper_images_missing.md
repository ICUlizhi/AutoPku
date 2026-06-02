# 真实案例 #5：论文图片搜索与绘制功能缺失

> **来源**: Kimi Session `4041a8d31ef0acf11a92b92f04406870` / user-history
> **时间**: 2026-04
> **涉及功能**: `write-paper`（图片获取）

---

## 用户原始输入

```
autopku 的流程中没有让你搜索获取图片和自己绘制图片吗，
如果没有的话请你加上并 push 回 autopku
```

## 问题描述

用户在使用 `write-paper` 功能生成马原课程论文后，发现：
1. 论文中没有配图
2. 即使大纲中规划了配图（数据图表、案例图片等），Agent 也没有执行图片搜索或绘制
3. `write-paper.md` 的 skill 流程中**缺少图片获取阶段**

## 修复过程

### 1. 新增 `image-handler.md` 工具 skill

创建了 `sub-skills/tools/image-handler.md`，提供：
- 数据图表绘制（matplotlib）
- 框架/流程图绘制（graphviz）
- 网络图片搜索与下载
- LaTeX 图片插入代码生成

### 2. 更新 `write-paper.md`

在论文生成流程中新增 Phase 4.5：

```markdown
### 4.5 图片获取与绘制（可选）

若大纲中规划了配图，引用 `tools/image-handler.md` 执行：

```python
# 图片规划结果来自 Phase 3 的大纲 Agent
images = outline.get("images", [])

if images:
    for img in images:
        Agent({
            "description": f"生成图片 {img['id']}",
            "prompt": f"""
引用 skill: autopku-tool-image-handler
图片类型：{img['type']}
图片标题：{img['title']}
内容描述：{img['description']}
输出路径：{course}/论文/figures/{img['id']}.png
"""
        })
```
```

### 3. 图片规划集成到大纲生成

大纲 Agent 的 prompt 中增加了：

```markdown
6. **图片规划**：判断论文是否需要配图（数据图表、框架图、流程图、案例图片），
   若需要则列出每张图的编号、标题、类型、内容描述和插入位置
```

## 测试价值

此案例对应 `write-paper/test_03_images`：
- 验证论文大纲中是否规划了配图
- 验证 `image-handler` 是否被正确调用
- 验证 `figures/` 目录下是否有生成的图片
- 验证 LaTeX/Word 文档中是否正确引用了图片

## 回归测试要点

```python
# validate.py 关键检查
assert (base / "论文" / "figures").exists(), "figures/ 目录不存在"
assert len(list((base / "论文" / "figures").glob("*.png"))) > 0, "未生成配图"
```

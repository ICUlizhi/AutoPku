# 真实案例 #2：笔记 Callout 文本丢失

> **来源**: Kimi Session `33e4e4296efbe536c72f943cd4cdb771` / user-history
> **时间**: 2026-04
> **涉及功能**: `write-notes`（Markdown callout → PDF 渲染）

---

## 用户原始输入序列

### Turn 1: 要求生成笔记

```
用 /Users/moonshot/Desktop/桌面整理/项目/pku大四下/autopku 的 skill
为 test00 的操作系统实验班的资料生成笔记（可以先把原有的删了）
```

### Turn 2: 指定字体

```
用 songti 吧，把你之前踩的坑包括 note 不显示写到 autopku 那个笔记 task skill 里面
```

### Turn 3: 发现 Callout 丢失（关键踩坑）

```
你所有的笔记都没有把 >note 的文本实际包含进去
```

### Turn 4: 要求修复并记录

```
那就重跑计量经济学的数据
```

```
你需要做的是在认识到计量经济学数据清洗的过程中遇到问题时，
优化我们的数据处理 pipeline，而不是单独为计量经济学做什么
```

```
你所有的笔记都没有把 >note 的文本实际包含进去
```

```
用 songti 吧，把你之前踩的坑包括 note 不显示写到 autopku 那个笔记 task skill 里面
```

## 问题根因分析

用户在多次使用 `write-notes` 功能后发现：

1. Agent 生成的 Markdown 笔记中包含了 `> [!note]` / `> [!tip]` callout 语法
2. 但后续渲染为 PDF 时，callout 的**正文内容**被丢失了
3. 只剩下 callout 的标题，或者整个 callout 被跳过

这对应 `write-notes.md` 中后来添加的踩坑记录：

> **Callout 正文丢失或重复**: 旧 filter 把 `> [!note] 标题\n> 正文` 的第一整段全部当作 tcolorbox title，导致正文被吞或重复。

## 修复过程

在 `write-notes.md` 的 PDF 渲染章节中，后来增加了专门的 `callout.lua` filter，通过 `tag_idx` + `SoftBreak` 精确定位标题与正文边界，解决了这个问题。

```lua
-- 精确定位 [!type] 标签位置
local tag_idx = nil
for i, inline in ipairs(inlines) do
  if inline.t == "Str" and inline.text:match("^%[! ?%w+ ?%]$") then
    tag_idx = i
    break
  end
end

-- 标题：标签后到 SoftBreak/LineBreak 之前的内容
local break_idx = nil
for i = tag_idx + 1, #inlines do
  if inlines[i].t == "SoftBreak" or inlines[i].t == "LineBreak" then
    break_idx = i
    break
  end
end
```

## 测试价值

此案例可用于验证 `write-notes/test_03_callout`：
- Markdown 中 `> [!note] 标题\n> 正文内容` 的正文是否被正确保留
- pandoc → LaTeX 的 callout.lua filter 是否工作正常
- 渲染后的 PDF 中 callout 内是否有完整的正文

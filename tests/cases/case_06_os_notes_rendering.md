# 真实案例 #6：操作系统笔记生成与 PDF 渲染踩坑

> **来源**: Kimi Session `33e4e4296efbe536c72f943cd4cdb771` / Sub-session `335a5b1c-8b0c-4e57-95c8-b6e30bc30415`
> **时间**: 2026-04
> **涉及功能**: `write-notes`（PDF 渲染、callout filter、字体选择）

---

## 用户原始输入序列

### Turn 1: 要求生成笔记

```
用 /Users/moonshot/Desktop/桌面整理/项目/pku大四下/autopku 的 skill
为 test00 的操作系统实验班的资料生成笔记（可以先把原有的删了）
```

### Turn 2: 继续完善

```
继续
```

### Turn 3: 要求多尝试渲染方式

```
你多尝试几种渲染方式
```

### Turn 4: 发现 Callout 丢失（关键踩坑）

```
你所有的笔记都没有把 >note 的文本实际包含进去
```

### Turn 5: 继续修复后验证

```
继续
```

### Turn 6: 指定字体并记录踩坑

```
用 songti 吧，把你之前踩的坑包括 note 不显示写到 autopku 那个笔记 task skill 里面
```

---

## 问题描述与执行过程

### 阶段一：大规模笔记生成

Agent 读取 `write-notes.md` skill 后，执行了以下操作：

1. **扫描课件**：发现 `test00/操作系统（实验班）/资料/` 下有 13 个 Lecture PDF，共计 **686 页**。
2. **删除旧笔记**：清空 `notes/` 和 `pdf/` 目录下的旧文件。
3. **并行生成 Markdown**：启动 5 个 Writer Agent 同时处理，按课程特点调整策略（保留定义、算法、伪代码、同步机制，去除历史背景和轶事）。
4. **生成 README.md**：自动汇总课程概览、知识图谱和各章索引。
5. **首次 PDF 渲染**：使用 pandoc + xelatex 渲染，但遇到大量 emoji 缺失警告（`💡📝⚠️` 在 `lmmono10-regular` 中不存在）。

首次渲染出的 PDF 有 52 页，但 callout 框内只有标题图标，正文内容被完全吞掉——此时用户尚未发现这个问题。

---

### 阶段二：多种渲染方式尝试

用户要求"多尝试几种渲染方式"后，Agent 在已安装工具链的基础上进行了系统性探索：

| 渲染方式 | 参数特点 | 结果 |
|---------|---------|------|
| **xelatex + PingFang SC** | 默认方案 | 成功，但 emoji 缺失 |
| **lualatex + PingFang SC** | 换编译引擎 | 成功，无 emoji 警告 |
| **xelatex + article class** | 更紧凑，无 chapter 分页 | 成功 |
| **xelatex + Heiti SC** | 黑体中文 | 成功 |
| **xelatex + Songti SC** | 宋体中文 | 成功 |
| **xelatex + compact** | 小边距(1.5cm)、10pt字体、暗色代码高亮 | 成功 |
| **typst** | 通过 `cargo install typst-cli` 安装后渲染 | 成功，43 页 |
| **HTML** | pandoc 导出 | 成功 |
| **合并 Markdown** | 纯文本合并 | 成功 |

同时尝试用 `monofont="Menlo"` 修复代码块中的 `≤` / `≥` 符号缺失问题。

---

### 阶段三：Callout 正文丢失（核心 Bug）

用户发现关键问题：

> "你所有的笔记都没有把 >note 的文本实际包含进去"

Agent 的排查与修复过程：

**根因分析**：
- Markdown callout 写法：
  ```markdown
  > [!note] 直觉理解
  > 线程就是CPU上"此刻正在跑的是谁"——...
  ```
- Pandoc 解析时，这两行**被合并为一个 `Para`**，内部结构为：
  ```
  Str "[!note]" → Space → Str "直觉理解" → SoftBreak → Str "线程就是CPU上..."
  ```
- 旧版 `callout.lua` 直接丢弃 `el.content[1]`（即整个 `Para`），导致正文全部丢失。

**第一次修复**：改为遍历 inlines，在检测到 `[!type]` 后收集剩余内容。但引入了新问题——**标题和内容重复**：
- `SoftBreak` 之前的标题文字也被收集到了 body 中，导致 PDF 里出现：
  ```
  [NOTE] 直觉理解
  直觉理解线程就是CPU上...
  ```

**第二次修复**：通过 `tag_idx` + `SoftBreak` / `LineBreak` 精确定位边界：
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

**第三次修复**：Callout 标题中含 `&` 等特殊字符（如 `Base & Bound`）导致 LaTeX 编译报错 `Misplaced alignment tab character &`。增加 `escape_latex()` 函数对 title 进行转义：
```lua
local function escape_latex(s)
  local r = s:gsub("\\", "\\textbackslash{}")
  r = r:gsub("([&%%#_$^{}~])", "\\%1")
  return r
end
```

---

### 阶段四：Unicode 符号缺失（`≠` `μ`）

修复 callout 后重新渲染，xelatex 仍报 `Missing character: There is no ≠ (U+2260) in font [lmmono10-regular]`。

Agent 的排查过程：
1. 误以为字符在代码块中，检查等宽字体（Menlo、Courier New 等）。
2. 实际发现 `≠` 和 `μ` 出现在 callout body 的正文中（如 `进程切换 ≠ 线程切换`、`~3–4 μs`）。
3. 深入检查生成的 `.tex` 文件，确认字符确实在 `tcolorbox` body 内，但 xelatex 仍尝试用 `lmmono10-regular` 渲染。
4. 最终发现：**xelatex 的默认西文字体是 Latin Modern，不支持这些 Unicode 符号**，而 `CJKmainfont` 只覆盖中日韩字符，数学符号和希腊字母仍走西文字体回退路径。

**修复**：给 xelatex 增加 `-V mainfont="PingFang SC"`，让西文字符也使用 PingFang SC：
```bash
pandoc notes/*.md \
  --pdf-engine=xelatex \
  -V CJKmainfont="PingFang SC" \
  -V mainfont="PingFang SC" \
  -V monofont="Menlo" \
  ...
```

重新渲染后所有版本均 **zero warning**。

---

### 阶段五：踩坑记录写入 Skill

用户要求：
> "用 songti 吧，把你之前踩的坑包括 note 不显示写到 autopku 那个笔记 task skill 里面"

Agent 执行：
1. 将 `*_songti.pdf` 复制覆盖为默认版本。
2. 更新 `sub-skills/tasks/write-notes.md`：
   - 更新 pandoc 命令示例（增加 `-V mainfont` 和 `-V monofont`）。
   - 更新 `callout.lua` 示例为修复后的完整版本。
   - 新增 **"关键踩坑记录"** 表格，汇总 6 条实战经验：
     | 问题 | 原因 | 解决 |
     |------|------|------|
     | Callout 正文丢失或重复 | 旧 filter 把第一整段全部当作 tcolorbox title | `tag_idx` + `SoftBreak` 精确定位 |
     | tcolorbox title 编译报错 | 标题含 `& $ % # _` 等特殊字符 | `escape_latex()` 转义 |
     | xelatex Unicode 符号缺失 | 默认西文字体 Latin Modern 不含 `≠ μ` | `-V mainfont="PingFang SC"` |
     | emoji 缺失 | xelatex 不支持彩色 emoji | 改用纯文字 `[TIP]` / `[NOTE]` |
     | lualatex vs xelatex 差异 | 字体回退机制不同 | 推荐 lualatex 作为最干净方案 |
     | mermaid 图表无法渲染 | pandoc 原生不支持 mermaid → image | 保留代码块供在线查看 |

3. 一并更新了 `do-homework.md`（增加写作类作业字数检查）。
4. Commit 并 push 到 GitHub。

---

## 踩坑与经验

1. **Callout 切分必须基于 AST 结构，而非简单丢弃第一段**：pandoc 会把 `> [!note] 标题
> 正文` 合并为一个 `Para`，旧 filter 的 `el.content[1]` 策略会直接把正文也丢掉。

2. **SoftBreak / LineBreak 是精确切分的关键**：通过定位 `[!type]` 后的第一个换行 inline，才能把 title 和 body  cleanly 分开。

3. **LaTeX title 必须转义**：`& $ % # _ ^ { } ~ \` 在 `tcolorbox` 的 `title={...}` 中都是特殊字符，直接注入会导致编译失败。

4. **xelatex 的字体回退陷阱**：`CJKmainfont` 只覆盖 CJK 区，数学符号（`≠`）和希腊字母（`μ`）仍走西文字体路径，必须显式设置 `mainfont`。

5. **lualatex 的字体处理更健壮**：在相同参数下，lualatex 不产生任何 Unicode 缺失警告，可作为优先推荐的引擎。

6. **emoji 在 LaTeX 中不可靠**：即使某些引擎支持，跨平台兼容性差。用纯文字 `[TIP]` / `[NOTE]` / `[WARN]` / `[EX]` 更稳妥。

---

## 测试价值

此案例可用于验证 `write-notes` 的以下方面：

- **大规模并行生成**：13 个 PDF、686 页、5 个 Writer Agent 并行，验证系统在高负载下的稳定性。
- **多引擎 PDF 渲染**：xelatex / lualatex / typst 三种引擎是否都能正确输出。
- **Callout 正文完整性**：`> [!note] 标题
> 正文内容` 的正文是否被正确保留，不丢失、不重复。
- **特殊字符支持**：PDF 中是否包含 `≠`、`μ`、`≤`、`≥` 等 Unicode 符号。
- **中文字体渲染**：宋体、黑体、苹方等不同中文字体在 PDF 中的显示效果。
- **Skill 踩坑记录同步**：修复后的 `callout.lua` 和 pandoc 参数是否被正确写回 `write-notes.md`。

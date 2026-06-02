# 测试：make-slides — touying-ethan 模板获取与编译

## 场景描述
验证 touying-ethan 模板能通过 `git clone` 正确获取到本地缓存，且 `typst compile` 能成功生成 PDF。

## 前置条件
- `git` 已安装
- `typst` 已安装（v0.11.0+）

## 输入
- 模板仓库: `https://github.com/hanlife02/touying-ethan.git`
- 最小化 `main.typ`（覆盖模板自带示例）

## 期望输出
1. `~/.autopku/templates/touying-ethan/` 存在且包含 `.git` 目录
2. `slides/main.typ` 语法合法
3. `typst compile` 成功生成 `slides.pdf`
4. PDF 页数 ≥ 1 且包含实际文本

## 验证命令
```bash
python validate.py
```

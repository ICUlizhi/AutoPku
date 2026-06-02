# 测试：make-slides — 中文内容渲染

## 场景描述
验证幻灯片能正确渲染中文字符，不会出现 tofu（豆腐块）或乱码。

## 前置条件
- `typst` 已安装
- 系统已安装中文字体（macOS 自带 Songti SC / PingFang SC / STSong）

## 输入
- 包含中文封面、目录、内容页的 `main.typ`
- 中文内容：标题、要点、公式混排

## 期望输出
1. `typst compile` 成功，无字体缺失警告
2. 生成的 PDF 可通过文本提取读取到中文字符
3. PDF 文件大小合理（嵌入中文字体后通常 > 30KB）

## 验证命令
```bash
python validate.py
```

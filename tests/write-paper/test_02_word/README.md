# 测试：write-paper — Word 模式论文生成

## 场景描述
用户要求生成某课程的 Word 格式论文。Agent 应使用 python-docx 正确渲染，
并将文档属性（author 等）设置为学生本人信息，而非默认的 "python-docx"。

## 前置条件
- pku3b 已安装且已登录
- python-docx 可用

## 输入
- 用户意图: `"给财务报表分析写课程论文，用 Word 格式"`
- 模拟课程: `test00/财务报表分析/`
- 论文要求文件: `通知/期末论文要求.txt`

## 期望输出
1. `test00/财务报表分析/论文/paper.docx` 存在
2. 文档 core_properties.author 为学生姓名（非 "python-docx"）
3. 标题、摘要、正文等中文字体正确（黑体、宋体、楷体）
4. 段落格式规范（首行缩进、行距 1.5 倍等）

## 验证命令
```bash
python validate.py
```

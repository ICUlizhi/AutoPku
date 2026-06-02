# 测试：sync-notices — 单课程基础同步

## 场景描述
用户要求同步单一课程的通知。Agent 应正确解析 ANSI 颜色码，生成通知摘要。

## 前置条件
- pku3b 已安装
- 已登录教学网

## 输入
- 用户意图: `"同步逻辑导论的通知"`
- mock 数据: fixtures/mock_assignments.txt

## 期望输出
1. test00/逻辑导论/ 目录结构完整
2. 通知摘要.md 包含课程统计、待交作业、下载文件列表
3. 无 ANSI 颜色码残留

## 验证命令
python validate.py

---
name: autopku-tool-pku3b-setup
description: PKU教学网工具 pku3b 的安装、配置和登录
---

# pku3b 工具配置

## 安装检查

```bash
PKU3B="$(command -v pku3b || true)"
test -n "$PKU3B" || echo "NOT_FOUND"
```

## 安装

### macOS Apple Silicon
```bash
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.11.0/pku3b-0.11.0-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.11.0-aarch64-apple-darwin.tar.gz
chmod +x pku3b-0.11.0-aarch64-apple-darwin/pku3b
mkdir -p "$HOME/.local/bin"
install -m 755 pku3b-0.11.0-aarch64-apple-darwin/pku3b "$HOME/.local/bin/pku3b"
pku3b --version
```

### 其他平台
从 [sshwy/pku3b releases](https://github.com/sshwy/pku3b/releases) 下载对应版本。

> **版本说明**: v0.11.0+ 支持公告 (`ann`) 和课表 (`ct`) 功能

## 登录

`pku3b init` 只需执行一次，凭证持久化到 `~/Library/Application Support/org.sshwy.pku3b/cfg.toml`。

### 1. 检查是否已登录

```bash
pku3b a ls 2>&1 || echo "NOT_LOGGED_IN"
```

正常返回作业列表 → 已登录，跳过步骤 2-3。返回 `NOT_LOGGED_IN` → 执行步骤 2。

### 2. 交互式登录（仅在未登录时）

```bash
pku3b init
```

`pku3b init` 检查 TTY，直接管道输入会报错 "input device is not a TTY"。AutoPku 已经提供嵌入式 Kimi Code 终端，所以不要生成 expect 脚本或明文密码文件；需要账号、密码、验证码时直接在这个终端里追问用户。

### 3. 验证

```bash
# 验证登录成功
pku3b a ls
```

## 常用命令

```bash
# 作业
pku3b a ls --all-term               # 所有学期作业
pku3b a download <ID> -d <dir>      # 下载附件
pku3b a submit <ID> <file>          # 提交作业

# 公告
pku3b ann ls                        # 列出公告
pku3b ann show <ID>                 # 查看公告详情

# 课表
pku3b ct -r                         # 获取课表 JSON

# 选课
pku3b s -d major show               # 主修课程
```

## 踩坑记录

- `pku3b init` 需要交互式输入，直接管道输入不工作；AutoPku 内部直接使用嵌入式 Kimi Code 终端交互
- `pku3b auth status/login` 命令不存在，正确命令是 `pku3b init`
- `pku3b s -d major show` 可能在某些账号返回 `302 Found`，作为可选步骤处理

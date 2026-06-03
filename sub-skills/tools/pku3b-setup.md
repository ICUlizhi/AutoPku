---
name: autopku-tool-pku3b-setup
description: PKU教学网工具 pku3b 的安装、配置和登录
---

# pku3b 工具配置

## 安装检查

```bash
which pku3b 2>/dev/null || echo "NOT_FOUND"
```

## 安装

### 推荐版本

**重要**: 使用 **v0.14.0+** 以避免 TLS 握手错误。v0.11.0 存在已知的连接问题。

### macOS Apple Silicon
```bash
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.14.0/pku3b-0.14.0-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.14.0-aarch64-apple-darwin.tar.gz
chmod +x pku3b-0.14.0-aarch64-apple-darwin/pku3b
ln -sf /tmp/pku3b-0.14.0-aarch64-apple-darwin/pku3b /tmp/pku3b
/tmp/pku3b --version
```

### 其他平台
从 [sshwy/pku3b releases](https://github.com/sshwy/pku3b/releases) 下载对应版本。

> **版本说明**: 
> - v0.14.0+: 修复 TLS 握手问题，推荐使用
> - v0.11.0+: 支持公告 (`ann`) 和课表 (`ct`) 功能，但存在连接问题

## 登录

`pku3b init` 只需执行一次，凭证持久化到 `~/Library/Application Support/org.sshwy.pku3b/cfg.toml`。

### 1. 检查是否已登录

```bash
/tmp/pku3b a ls 2>&1 || echo "NOT_LOGGED_IN"
```

正常返回作业列表 → 已登录，跳过步骤 2-3。返回 `NOT_LOGGED_IN` → 执行步骤 2。

### 2. TTY-safe 登录（仅在未登录时）

```bash
cat > /tmp/pku3b_login.exp << 'EOF'
#!/usr/bin/expect -f
set timeout 30
spawn /tmp/pku3b init
expect "username:"
send "学号\r"
expect "password:"
send "密码\r"
expect eof
EOF
chmod +x /tmp/pku3b_login.exp
/tmp/pku3b_login.exp
```

`pku3b init` 检查 TTY，直接管道输入会报错 "input device is not a TTY"，必须使用 expect。

### 3. 验证并清理

```bash
# 验证登录成功
/tmp/pku3b a ls

# 立即覆写临时文件，清除明文密码
echo "" > /tmp/pku3b_login.exp
```

## 常用命令

```bash
# 作业
/tmp/pku3b a ls --all-term          # 所有学期作业
/tmp/pku3b a download <ID> -d <dir> # 下载附件
/tmp/pku3b a submit <ID> <file>     # 提交作业

# 公告
/tmp/pku3b ann ls                   # 列出公告
/tmp/pku3b ann show <ID>            # 查看公告详情

# 课表
/tmp/pku3b ct -r                    # 获取课表 JSON

# 选课
/tmp/pku3b s -d major show          # 主修课程
```

## 踩坑记录

### TLS 握手失败（v0.11.0）

**问题**: 
```
Error: login to blackboard: `hyper` client error: received fatal alert: HandshakeFailure
```

**原因**: pku3b v0.11.0 的 Rust HTTP 客户端（hyper）与 PKU 教学网的 TLS 配置不兼容。

**解决方案**: 升级到 v0.14.0+
```bash
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.14.0/pku3b-0.14.0-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.14.0-aarch64-apple-darwin.tar.gz
chmod +x pku3b-0.14.0-aarch64-apple-darwin/pku3b
ln -sf /tmp/pku3b-0.14.0-aarch64-apple-darwin/pku3b /tmp/pku3b
/tmp/pku3b --version  # 应显示 0.14.0
```

验证修复：
```bash
/tmp/pku3b a ls 2>&1 | head -5  # 应正常显示作业列表
```

### 其他已知问题

- `pku3b init` 需要交互式输入，直接管道输入不工作
- `pku3b auth status/login` 命令不存在，正确命令是 `pku3b init`
- `pku3b s -d major show` 可能在某些账号返回 `302 Found`，作为可选步骤处理

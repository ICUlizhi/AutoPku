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

### macOS Apple Silicon
```bash
cd /tmp
curl -LO "https://github.com/sshwy/pku3b/releases/download/0.11.0/pku3b-0.11.0-aarch64-apple-darwin.tar.gz"
tar -xzf pku3b-0.11.0-aarch64-apple-darwin.tar.gz
chmod +x pku3b-0.11.0-aarch64-apple-darwin/pku3b
ln -sf pku3b-0.11.0-aarch64-apple-darwin/pku3b pku3b
./pku3b --version
```

### 其他平台
从 [sshwy/pku3b releases](https://github.com/sshwy/pku3b/releases) 下载对应版本。

> **版本说明**: v0.11.0+ 支持公告 (`ann`) 和课表 (`ct`) 功能

## TTY-safe 登录

使用 expect 脚本避免 "input device is not a TTY" 错误：

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

## 验证登录

```bash
/tmp/pku3b a ls
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

- `pku3b init` 需要交互式输入，直接管道输入不工作
- `pku3b auth status/login` 命令不存在，正确命令是 `pku3b init`
- `pku3b s -d major show` 可能在某些账号返回 `302 Found`，作为可选步骤处理

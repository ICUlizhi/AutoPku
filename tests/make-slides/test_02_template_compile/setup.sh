#!/bin/bash
set -e

# 检查依赖
if ! command -v git &> /dev/null; then
    echo "SKIP: git 未安装"
    exit 0
fi

if ! command -v typst &> /dev/null; then
    echo "SKIP: typst 未安装"
    exit 0
fi

# 确保模板缓存存在
TEMPLATE_DIR="$HOME/.autopku/templates/touying-ethan"
if [ ! -d "$TEMPLATE_DIR/.git" ]; then
    echo "首次克隆 touying-ethan 模板..."
    mkdir -p "$HOME/.autopku/templates"
    git clone --depth 1 https://github.com/hanlife02/touying-ethan.git "$TEMPLATE_DIR" || {
        echo "SKIP: 模板克隆失败"
        exit 0
    }
else
    echo "更新 touying-ethan 模板..."
    (cd "$TEMPLATE_DIR" && git pull --depth 1) || true
fi

# 复制到工作目录
mkdir -p slides
cp -r "$TEMPLATE_DIR"/* slides/
rm -f slides/main.pdf

# 创建最小化测试 main.typ（覆盖模板自带的示例）
cat > slides/main.typ << 'EOF'
#import "style/index.typ": presentation-theme
#import "slides/index.typ": (
  agenda-page, cover-page, end-page, subject-content-page, transition-page,
)

#let report-title = [模板编译测试]
#let report-author = [Test User]
#let report-institution = [PKU]
#let report-date = [2026-06-02]
#let demo-image = "figures/background.png"

#show: presentation-theme

#cover-page(
  title: report-title,
  author: report-author,
  institution: report-institution,
  date: report-date,
)

#agenda-page(
  sections: (
    [01 / Test Section],
  ),
)

#subject-content-page(
  title: [Validation Page],
  header-left-offset: 10em,
  top-content: [This is a minimal test page for template compilation.],
  content: [
    - Item 1: Template cloned successfully
    - Item 2: Typst compilation works
  ],
)

#end-page(
  title: [Thanks],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
EOF

echo "setup complete"

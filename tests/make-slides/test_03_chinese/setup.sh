#!/bin/bash
set -e

if ! command -v typst &> /dev/null; then
    echo "SKIP: typst 未安装"
    exit 0
fi

TEMPLATE_DIR="$HOME/.autopku/templates/touying-ethan"
if [ ! -d "$TEMPLATE_DIR/.git" ]; then
    echo "克隆 touying-ethan 模板..."
    mkdir -p "$HOME/.autopku/templates"
    (cd "$HOME/.autopku/templates" && git clone --depth 1 https://github.com/hanlife02/touying-ethan.git "$TEMPLATE_DIR") || {
        echo "SKIP: 模板克隆失败"
        exit 0
    }
fi

mkdir -p slides
cp -r "$TEMPLATE_DIR"/* slides/
rm -f slides/main.pdf

# 创建包含中文内容的 main.typ
cat > slides/main.typ << 'EOF'
#import "style/index.typ": presentation-theme
#import "slides/index.typ": (
  agenda-page, cover-page, end-page, subject-content-page, transition-page,
)

#let report-title = [中文渲染测试]
#let report-subtitle = [副标题示例]
#let report-author = [张三]
#let report-institution = [北京大学]
#let report-date = [2026-06-02]
#let demo-image = "figures/background.png"

#show: presentation-theme

#cover-page(
  title: report-title,
  subtitle: report-subtitle,
  author: report-author,
  institution: report-institution,
  date: report-date,
)

#agenda-page(
  sections: (
    [01 / 研究背景],
    [02 / 实验结果],
  ),
)

#transition-page(
  number: [01],
  title: [研究背景],
  description: [介绍本研究的问题定义与核心动机。],
)

#subject-content-page(
  title: [中文内容页],
  header-left-offset: 10em,
  top-content: [一句话结论：中文渲染必须正常显示，不能出现豆腐块。],
  content: [
    - 要点一：中文字符集包含常用汉字
    - 要点二：Typst 使用系统字体进行回退渲染
    - 要点三：macOS 自带宋体与黑体支持
    - 要点四：公式与中文可以混排，如 $E = m c^2$
  ],
)

#end-page(
  title: [谢谢聆听],
  author: report-author,
  institution: report-institution,
  date: report-date,
)
EOF

echo "setup complete"

#!/bin/bash
# AI Agent 执行步骤：
# 1. 将 input/note.md 渲染为 PDF，保存到 output/note_v1.pdf（或 notes/note.md）
# 2. 再次对同一个源文件执行渲染/转换，覆盖或保存到新文件
# 3. 观察 write-notes skill 的行为：
#    - 是否将内容追加到已有文件？
#    - 是否重复生成同一章节？
#    - 最终 notes/ 或 output/ 中的文件页数/字数是否正常
# 4. 确保最终输出中每个 UNIQUE_MARKER_7A3F9E2D_* 标记只出现一次

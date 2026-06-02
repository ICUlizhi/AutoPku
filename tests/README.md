# AutoPku 回归测试

基于真实 Kimi Session 案例构建的可执行回归测试。运行：`python3 -m pytest tests/` 或 `python3 tests/run_tests.py`

## 测试分类

| 测试文件 | 覆盖功能 | 来源案例 |
|---------|---------|---------|
| `validate_skill.py` | Skill 文档静态检查（格式、链接、代码块） | 全项目 |
| `test_pkusli.py` | pkusli 模板获取、编译、中文渲染 | case_06 |
| `test_write_notes.py` | 笔记 Callout、幂等性、列表渲染、字体 | case_02, case_03, case_06, case_08 |
| `test_write_paper.py` | 论文 PDF→Word、图片规划、模板替换 | case_01, case_05 |
| `test_do_homework.py` | 作业提交安全、学期匹配 | case_07 |

## 运行方式

```bash
# 运行所有测试
cd /path/to/AutoPku
python3 tests/run_tests.py

# 运行单个测试文件
python3 tests/test_pkusli.py
python3 tests/test_write_notes.py
```

## 设计理念

- **基于真实案例**：每个测试场景来自 `cases/` 中记录的真实 session
- **机器可自动化**：setup + validate 全流程无需 AI 参与
- **快速反馈**：单个测试在 30 秒内完成

#!/usr/bin/env python3
"""验证 DOCX 隐藏文字扫描逻辑正确"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from conftest import check_file_exists, TestReport

HERE = Path(__file__).parent.resolve()
report = TestReport()

# 1. 检查输入文件
docx_path = HERE / "suspicious.docx"
ok, msg = check_file_exists(docx_path)
report.add("docx_exists", ok, [msg])

is_placeholder = docx_path.exists() and docx_path.read_text(errors="ignore").startswith("# placeholder")

# 2. 检查扫描报告
report_path = HERE / "docx_scan_report.json"
ok, msg = check_file_exists(report_path)
if ok:
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        checks = []
        alerts = data.get("alerts", [])
        if isinstance(alerts, list) and len(alerts) >= 2:
            checks.append(f"OK: alerts 数量 = {len(alerts)} >= 2")
            # 检查是否包含预期类型
            types = {a.get("type") for a in alerts}
            if "vanish_hidden" in types:
                checks.append("OK: 检测到 vanish_hidden")
            else:
                checks.append("FAIL: 未检测到 vanish_hidden")
                ok = False
            if "color_mismatch" in types:
                checks.append("OK: 检测到 color_mismatch")
            else:
                checks.append("FAIL: 未检测到 color_mismatch")
                ok = False
        else:
            checks.append(f"FAIL: alerts 数量 = {len(alerts)}，期望 >= 2")
            ok = False
        report.add("scan_report", ok, checks)
    except Exception as e:
        report.add("scan_report", False, [f"FAIL: 解析报告出错: {e}"])
else:
    report.add("scan_report", False, [msg])

# 3. 若 DOCX 真实存在，本地再扫描一次作为交叉验证
if ok and not is_placeholder:
    try:
        from docx import Document
        from docx.oxml.ns import qn
        from docx.shared import RGBColor

        doc = Document(str(docx_path))
        bg_rgb = (1.0, 1.0, 1.0)
        local_alerts = []

        for pi, para in enumerate(doc.paragraphs):
            for run in para.runs:
                text = run.text.strip()
                if not text:
                    continue
                # vanish
                rPr = run._element.find(qn('w:rPr'))
                if rPr is not None and rPr.find(qn('w:vanish')) is not None:
                    local_alerts.append({"type": "vanish_hidden", "text": text})
                # color
                color = run.font.color
                if color and color.rgb:
                    rgb = (color.rgb[0]/255.0, color.rgb[1]/255.0, color.rgb[2]/255.0)
                    dist = sum((a-b)**2 for a,b in zip(rgb, bg_rgb))**0.5
                    if dist < 0.08:
                        local_alerts.append({"type": "color_mismatch", "text": text})

        report.add("local_cross_check", True, [
            f"OK: 本地交叉验证发现 {len(local_alerts)} 条 alert(s)",
            f"    {local_alerts}"
        ])
    except Exception as e:
        report.add("local_cross_check", False, [f"FAIL: 本地扫描异常: {e}"])

passed = report.print_summary()
sys.exit(0 if passed else 1)

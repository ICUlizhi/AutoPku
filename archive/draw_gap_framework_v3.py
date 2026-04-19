#!/usr/bin/env python3
"""
Academic Conceptual Framework v3: Clean, symmetric, no overlaps.
Uses a 3-column layout with clear vertical bridging stack.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Polygon, Rectangle
import numpy as np

plt.rcParams['font.family'] = ['Arial Unicode MS', 'Helvetica Neue', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(13, 9.5))
ax.set_xlim(0, 13)
ax.set_ylim(0, 9.5)
ax.axis('off')

# ===================== Palette =====================
c_req = '#1B4F72'
c_gap = '#922B21'
c_agent = '#1E8449'
c_bridge = '#6C3483'
c_sub = '#5D6D7E'
c_light = '#ABB2B9'

fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ===================== Title =====================
ax.text(6.5, 9.1, 'Bridging the Final Gap', fontsize=20, fontweight='bold',
        ha='center', va='center', color='#1C2833', family='serif')
ax.text(6.5, 8.65, 'From Real-World Requirements to General-Purpose Agent',
        fontsize=11, ha='center', va='center', color=c_sub, style='italic')
ax.text(6.5, 8.25, '打破真实需求与通用 Agent 之间的最后一层 Gap',
        fontsize=13, ha='center', va='center', color='#1C2833', fontweight='bold')

# ===================== Column 1: Real Requirements =====================
c1_x, c1_y = 0.6, 2.0
c1_w, c1_h = 3.0, 5.0
req_box = FancyBboxPatch((c1_x, c1_y), c1_w, c1_h, boxstyle="round,pad=0.12",
                          facecolor='#D4E6F1', edgecolor=c_req, linewidth=2)
ax.add_patch(req_box)

ax.text(c1_x + c1_w/2, c1_y + c1_h - 0.4, 'Real Requirements',
        fontsize=12, fontweight='bold', ha='center', va='center', color=c_req, family='serif')
ax.text(c1_x + c1_w/2, c1_y + c1_h - 0.75, '真实需求层',
        fontsize=10, fontweight='bold', ha='center', va='center', color=c_req)

reqs = [
    ('Long-tail Scenarios', '长尾场景'),
    ('Implicit Knowledge', '隐性知识'),
    ('Dynamic Constraints', '动态约束'),
    ('Multi-modal Input', '多模态输入'),
    ('Domain Terminology', '领域术语'),
]
for i, (en, cn) in enumerate(reqs):
    y = c1_y + c1_h - 1.35 - i * 0.82
    r = FancyBboxPatch((c1_x + 0.2, y - 0.26), c1_w - 0.4, 0.54,
                        boxstyle="round,pad=0.05", facecolor='white',
                        edgecolor='#85C1E9', linewidth=1)
    ax.add_patch(r)
    ax.text(c1_x + c1_w/2, y + 0.04, en, fontsize=9, ha='center', va='center',
            color=c_req, fontweight='bold')
    ax.text(c1_x + c1_w/2, y - 0.13, cn, fontsize=8, ha='center', va='center', color=c_sub)

# ===================== Column 3: General Agent =====================
c3_x, c3_y = 9.4, 2.0
c3_w, c3_h = 3.0, 5.0
agent_box = FancyBboxPatch((c3_x, c3_y), c3_w, c3_h, boxstyle="round,pad=0.12",
                            facecolor='#D5F5E3', edgecolor=c_agent, linewidth=2)
ax.add_patch(agent_box)

ax.text(c3_x + c3_w/2, c3_y + c3_h - 0.4, 'General-Purpose Agent',
        fontsize=12, fontweight='bold', ha='center', va='center', color=c_agent, family='serif')
ax.text(c3_x + c3_w/2, c3_y + c3_h - 0.75, '通用 Agent',
        fontsize=10, fontweight='bold', ha='center', va='center', color=c_agent)

agents = [
    ('LLM Foundation', '大模型基座'),
    ('Tool Use', '工具调用'),
    ('Multi-turn Reasoning', '多轮推理'),
    ('Generalization', '泛化能力'),
    ('Open-domain', '开放域交互'),
]
for i, (en, cn) in enumerate(agents):
    y = c3_y + c3_h - 1.35 - i * 0.82
    r = FancyBboxPatch((c3_x + 0.2, y - 0.26), c3_w - 0.4, 0.54,
                        boxstyle="round,pad=0.05", facecolor='white',
                        edgecolor='#82E0AA', linewidth=1)
    ax.add_patch(r)
    ax.text(c3_x + c3_w/2, y + 0.04, en, fontsize=9, ha='center', va='center',
            color=c_agent, fontweight='bold')
    ax.text(c3_x + c3_w/2, y - 0.13, cn, fontsize=8, ha='center', va='center', color=c_sub)

# ===================== Column 2: The GAP =====================
c2_x, c2_y = 4.3, 2.0
c2_w, c2_h = 4.4, 5.0
gap_box = FancyBboxPatch((c2_x, c2_y), c2_w, c2_h, boxstyle="round,pad=0.12",
                          facecolor='#FADBD8', edgecolor=c_gap, linewidth=2, linestyle='--')
ax.add_patch(gap_box)

# Gap header
gh = FancyBboxPatch((c2_x + c2_w/2 - 1.0, c2_y + c2_h - 0.72), 2.0, 0.5,
                     boxstyle="round,pad=0.08", facecolor='white',
                     edgecolor=c_gap, linewidth=1.5)
ax.add_patch(gh)
ax.text(c2_x + c2_w/2, c2_y + c2_h - 0.47, 'THE GAP', fontsize=12, fontweight='bold',
        ha='center', va='center', color=c_gap, family='serif')
ax.text(c2_x + c2_w/2, c2_y + c2_h - 0.92, '最后一层 Gap', fontsize=9, fontweight='bold',
        ha='center', va='center', color=c_gap)

# Gap causes (left side, 2 items)
gap_left = [
    ('Semantic\nGap', '语义鸿沟'),
    ('Capability\nBoundary', '能力边界'),
]
for i, (en, cn) in enumerate(gap_left):
    y = c2_y + c2_h - 2.0 - i * 1.1
    e = Ellipse((c2_x + 1.1, y), 1.6, 0.65, facecolor='white', edgecolor=c_gap, linewidth=1.2)
    ax.add_patch(e)
    ax.text(c2_x + 1.1, y + 0.05, en, fontsize=8, ha='center', va='center',
            color=c_gap, fontweight='bold')
    ax.text(c2_x + 1.1, y - 0.14, cn, fontsize=7, ha='center', va='center', color=c_sub)

# Gap causes (right side, 2 items)
gap_right = [
    ('Context\nMissing', '上下文缺失'),
    ('Feedback\nLoop', '反馈闭环'),
]
for i, (en, cn) in enumerate(gap_right):
    y = c2_y + c2_h - 2.0 - i * 1.1
    e = Ellipse((c2_x + c2_w - 1.1, y), 1.6, 0.65, facecolor='white', edgecolor=c_gap, linewidth=1.2)
    ax.add_patch(e)
    ax.text(c2_x + c2_w - 1.1, y + 0.05, en, fontsize=8, ha='center', va='center',
            color=c_gap, fontweight='bold')
    ax.text(c2_x + c2_w - 1.1, y - 0.14, cn, fontsize=7, ha='center', va='center', color=c_sub)

# ===================== Bridging Stack (vertical in center of gap) =====================
bridge_stack = ['RAG', 'Tool Learning', 'Prompt Engineering', 'Fine-Tuning']
stack_x = c2_x + c2_w/2
stack_top = c2_y + c2_h - 2.2
stack_h = 0.42
stack_gap = 0.52

for i, label in enumerate(bridge_stack):
    y = stack_top - i * stack_gap
    bw = len(label) * 0.13 + 0.35
    b = FancyBboxPatch((stack_x - bw/2, y - stack_h/2), bw, stack_h,
                        boxstyle="round,pad=0.06", facecolor='white',
                        edgecolor=c_bridge, linewidth=1.2, alpha=0.95, zorder=12)
    ax.add_patch(b)
    ax.text(stack_x, y, label, fontsize=9, ha='center', va='center',
            color=c_bridge, fontweight='bold', zorder=13)

# ===================== Horizontal Arrows =====================
arrow_y_positions = [c1_y + c1_h - 1.35 - i * 0.82 for i in range(5)]
arrow_start = c1_x + c1_w + 0.05
arrow_end = c3_x - 0.05

for y in arrow_y_positions:
    ax.annotate('', xy=(arrow_end, y), xytext=(arrow_start, y),
                arrowprops=dict(arrowstyle='->', color=c_bridge, lw=1.6,
                               connectionstyle='arc3,rad=0'))

# ===================== Bottom =====================
insight_box = FancyBboxPatch((1.0, 0.3), 11, 1.3, boxstyle="round,pad=0.1",
                              facecolor='#F4F6F7', edgecolor=c_light, linewidth=1)
ax.add_patch(insight_box)

ax.text(6.5, 1.35, 'Core Insight', fontsize=11, fontweight='bold',
        ha='center', va='center', color='#1C2833', family='serif')
ax.text(6.5, 0.95,
        'The final gap is essentially an adaptation problem: transforming general capabilities',
        fontsize=9, ha='center', va='center', color=c_sub)
ax.text(6.5, 0.65,
        'into specialized deployment, requiring domain knowledge injection, requirement',
        fontsize=9, ha='center', va='center', color=c_sub)
ax.text(6.5, 0.35,
        'formalization, closed feedback loops, and continuous evolutionary mechanisms.',
        fontsize=9, ha='center', va='center', color=c_sub)

# Side labels
ax.text(0.15, 1.3, 'Fragmented\n& Implicit', fontsize=8, ha='center', va='center',
        color=c_sub, style='italic', alpha=0.6)
ax.text(12.85, 1.3, 'Generalized\n& Explicit', fontsize=8, ha='center', va='center',
        color=c_sub, style='italic', alpha=0.6)

# ===================== Save =====================
plt.tight_layout()
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_v3.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_v3.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: gap_framework_v3.png / .pdf")

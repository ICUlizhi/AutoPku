#!/usr/bin/env python3
"""
Academic Conceptual Framework v2: Bridging the Final Gap
Cleaner layout, better typography, no overlaps.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Polygon
import numpy as np

plt.rcParams['font.family'] = ['Arial Unicode MS', 'Helvetica Neue', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# ===================== Color Palette (Academic, muted) =====================
c_req = '#2C3E50'
c_gap = '#C0392B'
c_agent = '#1E8449'
c_bridge = '#7D3C98'
c_bg = '#F4F6F7'
c_text = '#2C3E50'
c_sub = '#5D6D7E'
c_light = '#BDC3C7'

fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ===================== Title =====================
ax.text(7, 9.5, 'Bridging the Final Gap', fontsize=22, fontweight='bold',
        ha='center', va='center', color=c_text, family='serif')
ax.text(7, 9.05, 'From Real-World Requirements to General-Purpose Agent',
        fontsize=12, ha='center', va='center', color=c_sub, style='italic')
ax.text(7, 8.6, '打破真实需求与通用 Agent 之间的最后一层 Gap',
        fontsize=14, ha='center', va='center', color=c_text, fontweight='bold')

# ===================== Left: Real Requirements (tall rounded rect) =====================
left_x, left_y = 0.8, 2.0
left_w, left_h = 3.4, 5.2
req_box = FancyBboxPatch((left_x, left_y), left_w, left_h, boxstyle="round,pad=0.15",
                          facecolor='#EBF5FB', edgecolor=c_req, linewidth=2.2, alpha=0.9)
ax.add_patch(req_box)

ax.text(left_x + left_w/2, left_y + left_h - 0.45, 'Real Requirements',
        fontsize=13, fontweight='bold', ha='center', va='center', color=c_req, family='serif')
ax.text(left_x + left_w/2, left_y + left_h - 0.85, '真实需求层',
        fontsize=11, fontweight='bold', ha='center', va='center', color=c_req)

req_items = [
    ('Long-tail Scenarios', '长尾场景'),
    ('Implicit Knowledge', '隐性知识'),
    ('Dynamic Constraints', '动态约束'),
    ('Multi-modal Input', '多模态输入'),
    ('Domain Terminology', '领域术语'),
]

for i, (en, cn) in enumerate(req_items):
    y = left_y + left_h - 1.5 - i * 0.85
    item_box = FancyBboxPatch((left_x + 0.25, y - 0.28), left_w - 0.5, 0.58,
                               boxstyle="round,pad=0.06", facecolor='white',
                               edgecolor='#AED6F1', linewidth=1.2, alpha=0.95)
    ax.add_patch(item_box)
    ax.text(left_x + left_w/2, y + 0.06, en, fontsize=9.5, ha='center', va='center',
            color=c_req, fontweight='bold')
    ax.text(left_x + left_w/2, y - 0.14, cn, fontsize=8.5, ha='center', va='center', color=c_sub)

# ===================== Right: General Agent =====================
right_x, right_y = 9.8, 2.0
right_w, right_h = 3.4, 5.2
agent_box = FancyBboxPatch((right_x, right_y), right_w, right_h, boxstyle="round,pad=0.15",
                            facecolor='#EAFAF1', edgecolor=c_agent, linewidth=2.2, alpha=0.9)
ax.add_patch(agent_box)

ax.text(right_x + right_w/2, right_y + right_h - 0.45, 'General-Purpose Agent',
        fontsize=13, fontweight='bold', ha='center', va='center', color=c_agent, family='serif')
ax.text(right_x + right_w/2, right_y + right_h - 0.85, '通用 Agent',
        fontsize=11, fontweight='bold', ha='center', va='center', color=c_agent)

agent_items = [
    ('LLM Foundation', '大模型基座'),
    ('Tool Use', '工具调用'),
    ('Multi-turn Reasoning', '多轮推理'),
    ('Generalization', '泛化能力'),
    ('Open-domain', '开放域交互'),
]

for i, (en, cn) in enumerate(agent_items):
    y = right_y + right_h - 1.5 - i * 0.85
    item_box = FancyBboxPatch((right_x + 0.25, y - 0.28), right_w - 0.5, 0.58,
                               boxstyle="round,pad=0.06", facecolor='white',
                               edgecolor='#A9DFBF', linewidth=1.2, alpha=0.95)
    ax.add_patch(item_box)
    ax.text(right_x + right_w/2, y + 0.06, en, fontsize=9.5, ha='center', va='center',
            color=c_agent, fontweight='bold')
    ax.text(right_x + right_w/2, y - 0.14, cn, fontsize=8.5, ha='center', va='center', color=c_sub)

# ===================== Center: The GAP (large rounded box) =====================
gap_x, gap_y = 4.7, 2.3
gap_w, gap_h = 4.6, 4.6
gap_box = FancyBboxPatch((gap_x, gap_y), gap_w, gap_h, boxstyle="round,pad=0.15",
                          facecolor='#FDF2E9', edgecolor=c_gap, linewidth=2.0,
                          linestyle='--', alpha=0.85)
ax.add_patch(gap_box)

# Title badge in gap
badge = FancyBboxPatch((gap_x + gap_w/2 - 1.1, gap_y + gap_h - 0.75), 2.2, 0.55,
                        boxstyle="round,pad=0.1", facecolor='white',
                        edgecolor=c_gap, linewidth=1.5)
ax.add_patch(badge)
ax.text(gap_x + gap_w/2, gap_y + gap_h - 0.47, 'THE GAP', fontsize=13, fontweight='bold',
        ha='center', va='center', color=c_gap, family='serif')

# Gap sub-components (2x2 grid)
gap_comps = [
    ('Semantic Gap', '语义鸿沟'),
    ('Context Missing', '上下文缺失'),
    ('Capability Boundary', '能力边界'),
    ('Feedback Loop', '反馈闭环'),
]

for i, (en, cn) in enumerate(gap_comps):
    col = i % 2
    row = i // 2
    cx = gap_x + 0.6 + col * 1.9
    cy = gap_y + gap_h - 1.4 - row * 1.3
    
    # Small oval
    oval = Ellipse((cx, cy), 1.5, 0.7, facecolor='white', edgecolor=c_gap,
                   linewidth=1.3, alpha=0.95, zorder=10)
    ax.add_patch(oval)
    ax.text(cx, cy + 0.06, en, fontsize=8.5, ha='center', va='center',
            color=c_gap, fontweight='bold', zorder=11)
    ax.text(cx, cy - 0.12, cn, fontsize=7.5, ha='center', va='center',
            color=c_sub, zorder=11)

# ===================== Bridge Arrows (horizontal, with labels above) =====================
bridge_items = [
    ('RAG', 6.55),
    ('Tool Learning', 5.45),
    ('Prompt Engineering', 4.35),
    ('Fine-Tuning', 3.25),
]

arrow_start = left_x + left_w + 0.1
arrow_end = right_x - 0.1

for label, y in bridge_items:
    # Arrow shaft
    ax.annotate('', xy=(arrow_end, y), xytext=(arrow_start, y),
                arrowprops=dict(arrowstyle='->', color=c_bridge, lw=2.0,
                               connectionstyle='arc3,rad=0'))
    # Label badge above arrow
    badge_w = len(label) * 0.15 + 0.3
    badge_x = 7.0 - badge_w/2
    label_badge = FancyBboxPatch((badge_x, y + 0.15), badge_w, 0.42,
                                  boxstyle="round,pad=0.08", facecolor='white',
                                  edgecolor=c_bridge, linewidth=1.2, alpha=0.95, zorder=12)
    ax.add_patch(label_badge)
    ax.text(7.0, y + 0.36, label, fontsize=9, ha='center', va='center',
            color=c_bridge, fontweight='bold', zorder=13)

# ===================== Side annotations =====================
ax.text(0.2, 1.3, 'Fragmented\n& Implicit', fontsize=9, ha='center', va='center',
        color=c_sub, style='italic', alpha=0.7)
ax.text(13.8, 1.3, 'Generalized\n& Explicit', fontsize=9, ha='center', va='center',
        color=c_sub, style='italic', alpha=0.7)

# ===================== Bottom Insight =====================
insight_y = 0.5
insight_box = FancyBboxPatch((1.0, insight_y - 0.35), 12, 1.3, boxstyle="round,pad=0.12",
                              facecolor=c_bg, edgecolor=c_light, linewidth=1)
ax.add_patch(insight_box)

ax.text(7, insight_y + 0.65, 'Core Insight', fontsize=11, fontweight='bold',
        ha='center', va='center', color=c_text, family='serif')
ax.text(7, insight_y + 0.25,
        'The final gap is essentially an adaptation problem: transforming general capabilities into',
        fontsize=9.5, ha='center', va='center', color=c_sub)
ax.text(7, insight_y - 0.05,
        'specialized deployment. Systematic bridging requires domain knowledge injection,',
        fontsize=9.5, ha='center', va='center', color=c_sub)
ax.text(7, insight_y - 0.35,
        'requirement formalization, closed feedback loops, and continuous evolutionary mechanisms.',
        fontsize=9.5, ha='center', va='center', color=c_sub)

# ===================== Save =====================
plt.tight_layout()
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_v2.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_v2.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: gap_framework_v2.png / .pdf")

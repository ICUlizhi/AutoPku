#!/usr/bin/env python3
"""
Academic Conceptual Framework: Bridging the Final Gap
Real-World Requirements <-> General-Purpose Agent
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams['font.family'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# ===================== Color Palette (Academic) =====================
c_req = '#2C3E50'      # Dark blue-gray: Requirements
c_gap = '#C0392B'      # Muted red: Gap
c_agent = '#1A5F3F'    # Deep green: Agent
c_bridge = '#8E44AD'   # Purple: Bridging mechanism
c_bg = '#F8F9FA'       # Light gray background
c_text = '#2C3E50'     # Main text
c_sub = '#7F8C8D'      # Subtitle text

fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ===================== Title =====================
ax.text(7, 8.6, 'Bridging the Final Gap', fontsize=20, fontweight='bold',
        ha='center', va='center', color=c_text, family='serif')
ax.text(7, 8.2, 'From Real-World Requirements to General-Purpose Agent',
        fontsize=12, ha='center', va='center', color=c_sub, style='italic')
ax.text(7, 7.85, '打破真实需求与通用 Agent 之间的最后一层 Gap',
        fontsize=13, ha='center', va='center', color=c_text, fontweight='bold')

# ===================== Left Block: Real Requirements =====================
# Main container
req_box = FancyBboxPatch((0.5, 2.5), 3.8, 4.5, boxstyle="round,pad=0.15",
                          facecolor='#ECF0F1', edgecolor=c_req, linewidth=2.5)
ax.add_patch(req_box)

ax.text(2.4, 6.6, 'Real Requirements', fontsize=13, fontweight='bold',
        ha='center', va='center', color=c_req, family='serif')
ax.text(2.4, 6.25, '真实需求层', fontsize=11, fontweight='bold',
        ha='center', va='center', color=c_req)

# Requirement items (small rounded boxes)
req_items = [
    ('Long-tail Scenarios', '长尾场景'),
    ('Implicit Knowledge', '隐性知识'),
    ('Dynamic Constraints', '动态约束'),
    ('Multi-modal Input', '多模态输入'),
    ('Domain Terminology', '领域术语'),
]

for i, (en, cn) in enumerate(req_items):
    y = 5.6 - i * 0.65
    item_box = FancyBboxPatch((0.9, y-0.22), 3.0, 0.5, boxstyle="round,pad=0.08",
                               facecolor='white', edgecolor='#BDC3C7', linewidth=1)
    ax.add_patch(item_box)
    ax.text(2.4, y, f'{en}', fontsize=9.5, ha='center', va='center', color=c_req, fontweight='bold')
    ax.text(2.4, y-0.15, cn, fontsize=8.5, ha='center', va='center', color=c_sub)

# ===================== Right Block: General Agent =====================
agent_box = FancyBboxPatch((9.7, 2.5), 3.8, 4.5, boxstyle="round,pad=0.15",
                            facecolor='#E8F6EF', edgecolor=c_agent, linewidth=2.5)
ax.add_patch(agent_box)

ax.text(11.6, 6.6, 'General-Purpose Agent', fontsize=13, fontweight='bold',
        ha='center', va='center', color=c_agent, family='serif')
ax.text(11.6, 6.25, '通用 Agent', fontsize=11, fontweight='bold',
        ha='center', va='center', color=c_agent)

agent_items = [
    ('LLM Foundation', '大模型基座'),
    ('Tool Use', '工具调用'),
    ('Multi-turn Reasoning', '多轮推理'),
    ('Generalization', '泛化能力'),
    ('Open-domain', '开放域交互'),
]

for i, (en, cn) in enumerate(agent_items):
    y = 5.6 - i * 0.65
    item_box = FancyBboxPatch((10.1, y-0.22), 3.0, 0.5, boxstyle="round,pad=0.08",
                               facecolor='white', edgecolor='#A3E4C0', linewidth=1)
    ax.add_patch(item_box)
    ax.text(11.6, y, f'{en}', fontsize=9.5, ha='center', va='center', color=c_agent, fontweight='bold')
    ax.text(11.6, y-0.15, cn, fontsize=8.5, ha='center', va='center', color=c_sub)

# ===================== Center: The GAP =====================
# Draw a "broken bridge" / chasm in the center
gap_x_center = 7.0
gap_width = 2.2

# Gap background (subtle)
gap_bg = FancyBboxPatch((gap_x_center - gap_width/2, 2.8), gap_width, 4.0,
                         boxstyle="round,pad=0.1", facecolor='#FDF2E9',
                         edgecolor=c_gap, linewidth=2, linestyle='--')
ax.add_patch(gap_bg)

# "THE GAP" text
ax.text(gap_x_center, 6.4, 'THE GAP', fontsize=15, fontweight='bold',
        ha='center', va='center', color=c_gap, family='serif',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=c_gap, linewidth=1.5))
ax.text(gap_x_center, 6.0, '最后一层 Gap', fontsize=10, fontweight='bold',
        ha='center', va='center', color=c_gap)

# Gap components (floating in the chasm)
gap_components = [
    ('Semantic\nGap', '语义鸿沟'),
    ('Context\nMissing', '上下文缺失'),
    ('Capability\nBoundary', '能力边界'),
    ('Feedback\nLoop', '反馈闭环'),
]

for i, (en, cn) in enumerate(gap_components):
    col = i % 2
    row = i // 2
    x = gap_x_center - 0.5 + col * 1.0
    y = 5.0 - row * 1.1
    
    # Small circle markers
    circle = Circle((x, y), 0.35, facecolor='white', edgecolor=c_gap, linewidth=1.5, zorder=10)
    ax.add_patch(circle)
    ax.text(x, y+0.05, en, fontsize=7.5, ha='center', va='center', color=c_gap, fontweight='bold')
    ax.text(x, y-0.12, cn, fontsize=6.5, ha='center', va='center', color=c_sub)

# ===================== Bridging Mechanisms (Arrows + Labels) =====================
# Horizontal arrows from left to right
bridge_mechanisms = [
    ('RAG', 5.0),
    ('Tool\nLearning', 4.2),
    ('Prompt\nEngineering', 3.4),
    ('Fine-\nTuning', 2.6),
]

for label, y in bridge_mechanisms:
    # Arrow from left to right
    arrow = FancyArrowPatch((4.3, y), (9.7, y),
                            arrowstyle='->', mutation_scale=20,
                            color=c_bridge, linewidth=2, linestyle='-',
                            connectionstyle="arc3,rad=0")
    ax.add_patch(arrow)
    
    # Label on the arrow
    ax.text(7.0, y + 0.18, label, fontsize=9, ha='center', va='bottom',
            color=c_bridge, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=c_bridge, alpha=0.95, linewidth=1))

# ===================== Bottom Insight Box =====================
insight_box = FancyBboxPatch((1.5, 0.3), 11, 1.6, boxstyle="round,pad=0.12",
                              facecolor='#F4F6F7', edgecolor='#BDC3C7', linewidth=1)
ax.add_patch(insight_box)

ax.text(7, 1.55, 'Core Insight', fontsize=11, fontweight='bold',
        ha='center', va='center', color=c_text, family='serif')
ax.text(7, 1.15, 'The final gap is essentially an adaptation problem: transforming general capabilities into',
        fontsize=9.5, ha='center', va='center', color=c_sub)
ax.text(7, 0.82, 'specialized deployment. Systematic bridging requires domain knowledge injection, requirement',
        fontsize=9.5, ha='center', va='center', color=c_sub)
ax.text(7, 0.49, 'formalization, closed feedback loops, and continuous evolutionary mechanisms.',
        fontsize=9.5, ha='center', va='center', color=c_sub)

# ===================== Side annotations =====================
ax.text(0.3, 1.8, 'Fragmented\n& Implicit', fontsize=8, ha='center', va='center',
        color=c_sub, style='italic')
ax.text(13.7, 1.8, 'Generalized\n& Explicit', fontsize=8, ha='center', va='center',
        color=c_sub, style='italic')

# ===================== Save =====================
plt.tight_layout()
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_academic.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig('/Users/moonshot/Desktop/桌面整理/项目/pku大四下/AutoPku/images/gap_framework_academic.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: gap_framework_academic.png / .pdf")

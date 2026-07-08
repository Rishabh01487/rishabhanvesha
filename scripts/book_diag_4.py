#!/usr/bin/env python3
"""Diagram 4: Asset Lifecycle State Machine"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'

PRIMARY = '#415b69'
ACCENT = '#3593c1'
SECONDARY = '#b14053'
BG = '#f6f7f7'
TEXT = '#1d1f20'
MUTED = '#707679'
FILL = '#e9ebec'

fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(8, 8.5, 'Asset Lifecycle State Machine',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Tokenized asset states from creation to completion',
        ha='center', va='center', color=MUTED, fontsize=11)

# States arranged in a circular/flow pattern
states = [
    ("draft", 2.5, 6.5, PRIMARY),
    ("documents_uploaded", 5.5, 7.2, PRIMARY),
    ("ai_analyzing", 8.5, 7.2, ACCENT),
    ("verified", 11.5, 6.5, ACCENT),
    ("compliance_review", 13.0, 4.5, PRIMARY),
    ("active", 11.5, 2.5, ACCENT),
    ("funding", 8.5, 1.8, ACCENT),
    ("funded", 5.5, 1.8, PRIMARY),
    ("payout_pending", 3.0, 2.8, PRIMARY),
    ("completed", 2.0, 5.0, '#2d8a56'),
]

# Terminal states
reject_state = ("rejected", 14.2, 6.8, SECONDARY)
expire_state = ("expired", 13.8, 2.0, '#8a6d2d')

box_w = 2.0
box_h = 0.9

def draw_state(x, y, label, color, w=box_w, h=box_h):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                           facecolor=FILL, edgecolor=color, linewidth=2.2)
    ax.add_patch(rect)
    display = label.replace('_', '\n')
    ax.text(x, y, display, ha='center', va='center',
            color=TEXT, fontsize=8.5, fontweight='bold', linespacing=1.2)
    return (x, y)

# Draw main states
state_positions = {}
for name, x, y, color in states:
    pos = draw_state(x, y, name, color)
    state_positions[name] = pos

# Draw terminal states
for name, x, y, color in [reject_state, expire_state]:
    pos = draw_state(x, y, name, color, w=1.5, h=0.7)
    state_positions[name] = pos

# Main flow arrows (sequential)
flow_order = ["draft", "documents_uploaded", "ai_analyzing", "verified", 
              "compliance_review", "active", "funding", "funded", "payout_pending", "completed"]

for i in range(len(flow_order) - 1):
    s1 = flow_order[i]
    s2 = flow_order[i+1]
    x1, y1 = state_positions[s1]
    x2, y2 = state_positions[s2]
    # Calculate edge points
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    if dist > 0:
        ux, uy = dx/dist, dy/dist
    else:
        ux, uy = 0, 0
    ax.annotate('', xy=(x2 - ux*1.0, y2 - uy*0.45),
                xytext=(x1 + ux*1.0, y1 + uy*0.45),
                arrowprops=dict(arrowstyle='->', color=PRIMARY, lw=1.8,
                               connectionstyle='arc3,rad=0.1'))

# Rejected arrow from ai_analyzing
x1, y1 = state_positions["ai_analyzing"]
x2, y2 = state_positions["rejected"]
ax.annotate('', xy=(x2 - 0.7, y2), xytext=(x1 + 1.0, y1 + 0.3),
            arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=1.5,
                           connectionstyle='arc3,rad=-0.2', linestyle='dashed'))
ax.text(13.2, 7.5, 'AI fails', ha='center', va='center', color=SECONDARY, fontsize=7)

# Rejected arrow from compliance_review
x1, y1 = state_positions["compliance_review"]
ax.annotate('', xy=(x2 - 0.3, y2 + 0.35), xytext=(x1 + 0.2, y1 + 0.45),
            arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=1.5,
                           connectionstyle='arc3,rad=0.1', linestyle='dashed'))
ax.text(14.5, 5.5, 'compliance\nfails', ha='center', va='center', color=SECONDARY, fontsize=7, linespacing=1.2)

# Expired arrow from active
x1, y1 = state_positions["active"]
x2, y2 = state_positions["expired"]
ax.annotate('', xy=(x2 - 0.6, y2), xytext=(x1 + 0.8, y1 - 0.3),
            arrowprops=dict(arrowstyle='->', color='#8a6d2d', lw=1.5,
                           connectionstyle='arc3,rad=0.2', linestyle='dashed'))
ax.text(13.5, 2.5, 'timeout', ha='center', va='center', color='#8a6d2d', fontsize=7)

# Expired arrow from funding
x1, y1 = state_positions["funding"]
ax.annotate('', xy=(x2 - 0.5, y2 + 0.1), xytext=(x1 + 0.8, y1),
            arrowprops=dict(arrowstyle='->', color='#8a6d2d', lw=1.5,
                           connectionstyle='arc3,rad=0.15', linestyle='dashed'))

# Start indicator
ax.annotate('START', xy=(state_positions["draft"][0] - 1.0, state_positions["draft"][1]),
            xytext=(state_positions["draft"][0] - 2.0, state_positions["draft"][1]),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2),
            color=ACCENT, fontsize=9, fontweight='bold', va='center')

# Legend
legend_items = [
    (PRIMARY, 'Normal transition'),
    (SECONDARY, 'Failure path (rejected)'),
    ('#8a6d2d', 'Timeout (expired)'),
    ('#2d8a56', 'Terminal success'),
]
ly = 0.7
lx = 1.0
ax.text(lx, ly + 0.4, 'Legend:', ha='left', va='center', color=TEXT, fontsize=9, fontweight='bold')
for i, (c, label) in enumerate(legend_items):
    px = lx + 1.5 + i * 3.3
    line = FancyBboxPatch((px, ly + 0.15), 0.6, 0.2, boxstyle="round,pad=0.03",
                           facecolor=c, edgecolor=c, linewidth=1)
    ax.add_patch(line)
    ax.text(px + 0.8, ly + 0.25, label, ha='left', va='center', color=MUTED, fontsize=8)

plt.savefig('/home/z/my-project/download/book_diagrams/asset_lifecycle.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: asset_lifecycle.png")
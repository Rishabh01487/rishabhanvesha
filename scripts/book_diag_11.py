#!/usr/bin/env python3
"""Diagram 11: Marketplace Ecosystem"""
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

ax.text(8, 8.5, 'Marketplace Ecosystem',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Multi-stakeholder platform with bidirectional value flows',
        ha='center', va='center', color=MUTED, fontsize=11)

# Central platform
cx, cy = 8, 4.5
platform_r = FancyBboxPatch((cx - 2.2, cy - 1.0), 4.4, 2.0, boxstyle="round,pad=0.15",
                              facecolor=PRIMARY, edgecolor=PRIMARY, linewidth=3)
ax.add_patch(platform_r)
ax.text(cx, cy + 0.35, 'AVERON', ha='center', va='center', color='white', fontsize=18, fontweight='bold')
ax.text(cx, cy - 0.05, 'PLATFORM', ha='center', va='center', color='white', fontsize=14, fontweight='bold')
ax.text(cx, cy - 0.5, 'Tokenization · Trading · Settlement', ha='center', va='center',
        color='#a0c4d8', fontsize=9)

# Stakeholders around the platform
stakeholders = [
    ("Asset\nOwners", 2.0, 7.0, ACCENT, "List assets\nUpload docs\nReceive payout"),
    ("Investors", 14.0, 7.0, SECONDARY, "Browse assets\nPlace orders\nTrade tokens"),
    ("Validators", 1.5, 2.0, '#6a8a45', "Verify documents\nAudit assets\nEarn fees"),
    ("Developers", 14.5, 2.0, '#8a6d2d', "Build dApps\nSmart contracts\nAPI access"),
    ("Institutions", 4.0, 0.3, '#5a4b8a', "Compliance\nLarge investments\nPortfolio mgmt"),
    ("Regulators", 12.0, 0.3, PRIMARY, "Audit access\nCompliance reports\nTransparency"),
]

for name, x, y, color, desc in stakeholders:
    # Stakeholder box
    bw, bh = 2.4, 1.6
    r = FancyBboxPatch((x - bw/2, y - bh/2), bw, bh, boxstyle="round,pad=0.1",
                        facecolor=FILL, edgecolor=color, linewidth=2)
    ax.add_patch(r)
    ax.text(x, y + 0.35, name, ha='center', va='center', color=color, fontsize=11, fontweight='bold', linespacing=1.2)
    ax.text(x, y - 0.4, desc, ha='center', va='center', color=MUTED, fontsize=7.5, linespacing=1.2)
    
    # Connection line to center
    dx = cx - x
    dy = cy - y
    dist = np.sqrt(dx**2 + dy**2)
    ux, uy = dx/dist, dy/dist
    
    # Start from stakeholder edge
    sx = x + ux * (bw/2 if abs(dx) > abs(dy) else bh/2)
    sy = y + uy * (bh/2 if abs(dy) > abs(dx) else bw/2)
    
    # End at platform edge
    ex = cx - ux * 2.2 if abs(dx) > abs(dy) else cx - ux * 1.0
    ey = cy - uy * 1.0 if abs(dy) > abs(dx) else cy - uy * 0.5
    
    # Outward arrow (stakeholder -> platform)
    ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5, alpha=0.7,
                               connectionstyle='arc3,rad=0.15'))
    # Return arrow (platform -> stakeholder)
    ax.annotate('', xy=(sx, sy), xytext=(ex, ey),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, alpha=0.4,
                               connectionstyle='arc3,rad=-0.15', linestyle='dashed'))

# Legend
ax.text(8, 8.5, '', ha='center', va='center')  # spacer
ax.text(8, -0.1, '── solid: primary value flow  ·  - - dashed: data/response flow',
        ha='center', va='center', color=MUTED, fontsize=8, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/marketplace_ecosystem.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: marketplace_ecosystem.png")
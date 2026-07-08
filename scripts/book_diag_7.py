#!/usr/bin/env python3
"""Diagram 7: Price Discovery Model"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'

PRIMARY = '#415b69'
ACCENT = '#3593c1'
SECONDARY = '#b14053'
BG = '#f6f7f7'
TEXT = '#1d1f20'
MUTED = '#707679'
FILL = '#e9ebec'
GREEN = '#2d8a56'

fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(8, 8.5, 'Price Discovery Model',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Algorithmic pricing based on supply dynamics and asset funding activity',
        ha='center', va='center', color=MUTED, fontsize=11)

# Formula box
formula_x, formula_y = 2.0, 6.5
formula_w, formula_h = 12.0, 1.2
fr = FancyBboxPatch((formula_x, formula_y), formula_w, formula_h, boxstyle="round,pad=0.12",
                      facecolor='#1d1f20', edgecolor=PRIMARY, linewidth=2)
ax.add_patch(fr)
ax.text(formula_x + formula_w/2, formula_y + formula_h/2 + 0.15,
        'P  =  P_initial  ×  ( 1  +  totalSupply / 10,000  )  ×  ( 1  +  totalAssetsFunded  ×  0.04  )',
        ha='center', va='center', color='white', fontsize=14, fontweight='bold', family='monospace')
ax.text(formula_x + formula_w/2, formula_y + 0.2,
        'Bonding curve with supply factor (left)  ·  Market activity factor (right)',
        ha='center', va='center', color=ACCENT, fontsize=9)

# Factor 1: Supply Factor
f1_x, f1_y = 1.5, 3.8
f1_w, f1_h = 5.5, 2.3
r1 = FancyBboxPatch((f1_x, f1_y), f1_w, f1_h, boxstyle="round,pad=0.1",
                      facecolor=FILL, edgecolor=ACCENT, linewidth=2)
ax.add_patch(r1)
ax.text(f1_x + f1_w/2, f1_y + f1_h - 0.4, 'Supply Factor', ha='center', va='center',
        color=ACCENT, fontsize=13, fontweight='bold')
ax.text(f1_x + f1_w/2, f1_y + f1_h - 0.75, '(1 + totalSupply / 10,000)', ha='center', va='center',
        color=MUTED, fontsize=10, family='monospace')

# Mini chart for supply curve
chart_x = f1_x + 0.4
chart_y = f1_y + 0.2
chart_w = 4.7
chart_h = 1.4
# Axes
ax.plot([chart_x, chart_x + chart_w], [chart_y, chart_y], color=MUTED, lw=1, alpha=0.5)
ax.plot([chart_x, chart_x], [chart_y, chart_y + chart_h], color=MUTED, lw=1, alpha=0.5)
ax.text(chart_x - 0.15, chart_y + chart_h/2, 'P', ha='right', va='center', color=MUTED, fontsize=8)
ax.text(chart_x + chart_w/2, chart_y - 0.15, 'Supply', ha='center', va='top', color=MUTED, fontsize=8)

# Curve
xs = np.linspace(0, 1, 100)
ys = 1 + xs * 1.5
ax.plot(chart_x + xs * chart_w, chart_y + (ys / 2.5) * chart_h, color=ACCENT, lw=2.5)
# Fill
ax.fill_between(chart_x + xs * chart_w, chart_y, chart_y + (ys / 2.5) * chart_h, color=ACCENT, alpha=0.1)

# Data points
for sv, pv in [(2000, 1.2), (5000, 1.5), (10000, 2.0), (25000, 3.5)]:
    xn = chart_x + (sv / 30000) * chart_w
    yn = chart_y + ((1 + sv/10000) / 4) * chart_h
    ax.plot(xn, yn, 'o', color=ACCENT, markersize=5, zorder=5)

# Labels
ax.text(f1_x + 0.4, f1_y + f1_h - 1.05, '• Linear bonding curve', ha='left', va='center', color=TEXT, fontsize=8)
ax.text(f1_x + 0.4, f1_y + f1_h - 1.3, '• 0.01% per unit increase', ha='left', va='center', color=TEXT, fontsize=8)
ax.text(f1_x + 0.4, f1_y + f1_h - 1.55, '• Predictable mint/burn pricing', ha='left', va='center', color=TEXT, fontsize=8)

# Factor 2: Market Activity Factor
f2_x, f2_y = 9.0, 3.8
f2_w, f2_h = 5.5, 2.3
r2 = FancyBboxPatch((f2_x, f2_y), f2_w, f2_h, boxstyle="round,pad=0.1",
                      facecolor=FILL, edgecolor=SECONDARY, linewidth=2)
ax.add_patch(r2)
ax.text(f2_x + f2_w/2, f2_y + f2_h - 0.4, 'Market Activity Factor', ha='center', va='center',
        color=SECONDARY, fontsize=13, fontweight='bold')
ax.text(f2_x + f2_w/2, f2_y + f2_h - 0.75, '(1 + totalAssetsFunded × 0.04)', ha='center', va='center',
        color=MUTED, fontsize=10, family='monospace')

# Bar chart for funded assets
bar_data = [(5, '5 assets'), (10, '10'), (20, '20'), (50, '50')]
bx = f2_x + 0.5
by = f2_y + 0.2
bw = 0.8
for i, (count, label) in enumerate(bar_data):
    bh = count / 50 * 1.3
    bar = FancyBboxPatch((bx + i * 1.2, by), bw, bh, boxstyle="round,pad=0.03",
                           facecolor=SECONDARY, edgecolor=SECONDARY, linewidth=1, alpha=0.6 + i*0.1)
    ax.add_patch(bar)
    ax.text(bx + i * 1.2 + bw/2, by + bh + 0.1, f'{1 + count*0.04:.2f}x',
            ha='center', va='bottom', color=TEXT, fontsize=8, fontweight='bold')
    ax.text(bx + i * 1.2 + bw/2, by - 0.12, label, ha='center', va='top', color=MUTED, fontsize=7)

ax.text(f2_x + 0.4, f2_y + f2_h - 1.05, '• 4% per funded asset', ha='left', va='center', color=TEXT, fontsize=8)
ax.text(f2_x + 0.4, f2_y + f2_h - 1.3, '• Rewards platform growth', ha='left', va='center', color=TEXT, fontsize=8)
ax.text(f2_x + 0.4, f2_y + f2_h - 1.55, '• Compounding network effect', ha='left', va='center', color=TEXT, fontsize=8)

# Example calculation
ex_y = 2.2
ex_r = FancyBboxPatch((2.5, ex_y), 11.0, 1.2, boxstyle="round,pad=0.1",
                        facecolor='#edeeef', edgecolor=MUTED, linewidth=1)
ax.add_patch(ex_r)
ax.text(8, ex_y + 0.85, 'Example Calculation', ha='center', va='center', color=TEXT, fontsize=11, fontweight='bold')
ax.text(8, ex_y + 0.45,
        'P = $1.00 × (1 + 15,000/10,000) × (1 + 12 × 0.04) = $1.00 × 2.50 × 1.48 = $3.70',
        ha='center', va='center', color=ACCENT, fontsize=10, family='monospace')
ax.text(8, ex_y + 0.1,
        'P_initial=$1.00  ·  Supply=15,000 tokens  ·  12 assets funded  →  Final token price: $3.70',
        ha='center', va='center', color=MUTED, fontsize=8.5)

# Bottom note
ax.text(8, 1.4, '▲ Both factors are transparent and verifiable on-chain',
        ha='center', va='center', color=MUTED, fontsize=9, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/price_discovery.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: price_discovery.png")
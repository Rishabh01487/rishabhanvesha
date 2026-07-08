#!/usr/bin/env python3
"""Diagram 6: Trading Engine Architecture"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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

ax.text(8, 8.5, 'Trading Engine Architecture',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Order matching, execution, and on-chain settlement pipeline',
        ha='center', va='center', color=MUTED, fontsize=11)

# Stage boxes
stages = [
    ("Order\nSubmission", 1.0, 4.5, PRIMARY, [
        "REST / WebSocket API",
        "Order Validation",
        "Balance Check",
        "Signature Verification"
    ]),
    ("Order\nBook", 4.2, 4.5, ACCENT, [
        "Bids (Buy Orders)",
        "Asks (Sell Orders)",
        "Price Sorting",
        "Depth Management"
    ]),
    ("Matching\nEngine", 7.4, 4.5, ACCENT, [
        "Price-Time Priority",
        "FIFO Matching",
        "Partial Fill Logic",
        "Spread Calculation"
    ]),
    ("Trade\nExecution", 10.6, 4.5, SECONDARY, [
        "Fill Confirmation",
        "Price Determination",
        "Quantity Allocation",
        "Trade ID Generation"
    ]),
    ("On-Chain\nSettlement", 13.0, 4.5, PRIMARY, [
        "Atomic Swap Tx",
        "Token Transfer",
        "State Update",
        "Block Confirmation"
    ]),
]

for label, x, y, color, subs in stages:
    # Main box
    r = FancyBboxPatch((x, y - 0.5), 2.4, 1.0, boxstyle="round,pad=0.1",
                        facecolor=FILL, edgecolor=color, linewidth=2.5)
    ax.add_patch(r)
    ax.text(x + 1.2, y, label, ha='center', va='center', color=TEXT, fontsize=11, fontweight='bold', linespacing=1.2)
    
    # Sub-items
    for i, sub in enumerate(subs):
        sy = y - 1.2 - i * 0.48
        sr = FancyBboxPatch((x + 0.1, sy - 0.15), 2.2, 0.38, boxstyle="round,pad=0.05",
                             facecolor='#edeeef', edgecolor=MUTED, linewidth=0.8, alpha=0.9)
        ax.add_patch(sr)
        ax.text(x + 1.2, sy + 0.04, sub, ha='center', va='center', color=MUTED, fontsize=7.5)
    
    # Vertical line from box to subs
    ax.plot([x + 1.2, x + 1.2], [y - 0.5, y - 0.95], color=MUTED, lw=1, alpha=0.5)

# Arrows between stages
for i in range(len(stages) - 1):
    x1 = stages[i][1] + 2.4
    x2 = stages[i+1][1]
    y = 4.5
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=PRIMARY, lw=2.5))

# Fee Collection branch
fee_x = 13.0
fee_y = 1.0
ax.annotate('', xy=(fee_x + 1.2, 1.8), xytext=(fee_x + 1.2, 2.5),
            arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=1.8, linestyle='dashed'))
fr = FancyBboxPatch((fee_x - 0.3, fee_y), 3.0, 0.8, boxstyle="round,pad=0.08",
                      facecolor='#fde8e8', edgecolor=SECONDARY, linewidth=1.5)
ax.add_patch(fr)
ax.text(fee_x + 1.2, fee_y + 0.55, 'Fee Collection', ha='center', va='center',
        color=SECONDARY, fontsize=11, fontweight='bold')
ax.text(fee_x + 1.2, fee_y + 0.2, 'Maker: 0.1%  ·  Taker: 0.25%  ·  Protocol: 0.05%',
        ha='center', va='center', color=MUTED, fontsize=8)

# Order book detail inset (top)
inset_x, inset_y = 3.5, 6.5
inset_r = FancyBboxPatch((inset_x, inset_y), 4.5, 1.6, boxstyle="round,pad=0.1",
                           facecolor='white', edgecolor=ACCENT, linewidth=1.5, linestyle='--')
ax.add_patch(inset_r)
ax.text(inset_x + 2.25, inset_y + 1.35, 'Order Book Snapshot', ha='center', va='center',
        color=ACCENT, fontsize=10, fontweight='bold')

# Bids
ax.text(inset_x + 0.8, inset_y + 1.0, 'BIDS (Buy)', ha='center', va='center', color=GREEN, fontsize=8, fontweight='bold')
bid_data = [("100.50", "500"), ("100.25", "1,200"), ("100.00", "3,000")]
for i, (p, q) in enumerate(bid_data):
    ax.text(inset_x + 0.3, inset_y + 0.7 - i*0.22, f'$ {p}', ha='left', va='center', color=GREEN, fontsize=7.5)
    ax.text(inset_x + 2.0, inset_y + 0.7 - i*0.22, f'{q} units', ha='left', va='center', color=MUTED, fontsize=7.5)

# Asks
ax.text(inset_x + 3.3, inset_y + 1.0, 'ASKS (Sell)', ha='center', va='center', color=SECONDARY, fontsize=8, fontweight='bold')
ask_data = [("101.00", "2,000"), ("101.25", "800"), ("101.50", "300")]
for i, (p, q) in enumerate(ask_data):
    ax.text(inset_x + 2.7, inset_y + 0.7 - i*0.22, f'$ {p}', ha='left', va='center', color=SECONDARY, fontsize=7.5)
    ax.text(inset_x + 4.0, inset_y + 0.7 - i*0.22, f'{q} units', ha='left', va='center', color=MUTED, fontsize=7.5)

# Spread indicator
ax.text(inset_x + 2.25, inset_y + 0.05, 'Spread: $0.50 (0.49%)', ha='center', va='center',
        color=MUTED, fontsize=7.5, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/trading_engine.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: trading_engine.png")
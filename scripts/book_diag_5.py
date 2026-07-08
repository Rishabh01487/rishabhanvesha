#!/usr/bin/env python3
"""Diagram 5: Escrow Mechanism"""
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

ax.text(8, 8.5, 'Per-Asset Escrow Mechanism',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Smart contract-governed fund custody with automated settlement',
        ha='center', va='center', color=MUTED, fontsize=11)

# Investor boxes (left)
investors = [("Investor A", 1.5, 6.2), ("Investor B", 1.5, 4.5), ("Investor C", 1.5, 2.8)]
for name, x, y in investors:
    r = FancyBboxPatch((x, y - 0.4), 2.2, 0.8, boxstyle="round,pad=0.08",
                        facecolor=FILL, edgecolor=PRIMARY, linewidth=2)
    ax.add_patch(r)
    ax.text(x + 1.1, y, name, ha='center', va='center', color=TEXT, fontsize=11, fontweight='bold')

# INVEST arrows
for name, x, y in investors:
    ax.annotate('', xy=(5.0, 5.0), xytext=(x + 2.2, y),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))
    ax.text(3.8, y + 0.15, 'INVEST', ha='center', va='center', color=ACCENT, fontsize=8, fontweight='bold')

# Per-Asset Escrow Account (center)
escrow_x, escrow_y = 5.0, 3.5
escrow_w, escrow_h = 3.5, 3.0
er = FancyBboxPatch((escrow_x, escrow_y), escrow_w, escrow_h, boxstyle="round,pad=0.12",
                      facecolor='#dceef8', edgecolor=ACCENT, linewidth=2.5)
ax.add_patch(er)
ax.text(escrow_x + escrow_w/2, escrow_y + escrow_h - 0.5, 'Per-Asset Escrow', 
        ha='center', va='center', color=ACCENT, fontsize=13, fontweight='bold')
ax.text(escrow_x + escrow_w/2, escrow_y + escrow_h - 0.9, 'Smart Contract Account',
        ha='center', va='center', color=MUTED, fontsize=9)

# Escrow details
details = [
    f"Total Locked: $2,450,000",
    f"Asset: Real Estate #042",
    f"Deadline: 2025-06-30",
    f"Status: FUNDING",
    f"Min. Funding: $2,000,000",
]
dy = escrow_y + escrow_h - 1.4
for d in details:
    ax.text(escrow_x + 0.3, dy, d, ha='left', va='center', color=TEXT, fontsize=8.5)
    dy -= 0.35

# Lock icon
lock = plt.Circle((escrow_x + escrow_w - 0.5, escrow_y + 0.5), 0.25,
                   color=ACCENT, alpha=0.2, zorder=3)
ax.add_patch(lock)
ax.text(escrow_x + escrow_w - 0.5, escrow_y + 0.5, '[L]', ha='center', va='center', fontsize=10, fontweight='bold', color=ACCENT, zorder=4)

# SUCCESS path (top right)
ax.annotate('', xy=(11.0, 6.8), xytext=(escrow_x + escrow_w, escrow_y + escrow_h - 0.5),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.5))
ax.text(9.5, 6.2, 'SUCCESS\n(funding goal met)', ha='center', va='center',
        color=GREEN, fontsize=9, fontweight='bold', linespacing=1.2)

# Fee deduction box (center right)
fee_x, fee_y = 9.5, 4.0
fee_r = FancyBboxPatch((fee_x, fee_y), 2.5, 1.2, boxstyle="round,pad=0.08",
                         facecolor='#fde8e8', edgecolor=SECONDARY, linewidth=1.5)
ax.add_patch(fee_r)
ax.text(fee_x + 1.25, fee_y + 0.9, 'Fee Deduction', ha='center', va='center',
        color=SECONDARY, fontsize=10, fontweight='bold')
ax.text(fee_x + 1.25, fee_y + 0.55, 'Platform: 1.5% = $36,750', ha='center', va='center',
        color=MUTED, fontsize=8)
ax.text(fee_x + 1.25, fee_y + 0.2, 'Validator: 0.5% = $12,250', ha='center', va='center',
        color=MUTED, fontsize=8)

ax.annotate('', xy=(fee_x, fee_y + 0.6), xytext=(escrow_x + escrow_w, escrow_y + escrow_h/2),
            arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=1.5, linestyle='dashed'))

# Payout to Owner
payout_x, payout_y = 12.5, 6.5
payout_r = FancyBboxPatch((payout_x, payout_y - 0.5), 3.0, 1.0, boxstyle="round,pad=0.08",
                            facecolor='#e8f5e9', edgecolor=GREEN, linewidth=2)
ax.add_patch(payout_r)
ax.text(payout_x + 1.5, payout_y + 0.15, 'PAYOUT → Asset Owner', ha='center', va='center',
        color=GREEN, fontsize=11, fontweight='bold')
ax.text(payout_x + 1.5, payout_y - 0.2, '$2,401,000', ha='center', va='center',
        color=TEXT, fontsize=10)

ax.annotate('', xy=(payout_x, payout_y), xytext=(fee_x + 2.5, fee_y + 0.8),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))

# EXPIRY path (bottom right)
ax.annotate('', xy=(11.0, 1.8), xytext=(escrow_x + escrow_w, escrow_y + 0.3),
            arrowprops=dict(arrowstyle='->', color='#8a6d2d', lw=2.5, linestyle='dashed'))
ax.text(9.5, 2.3, 'EXPIRY\n(deadline passed)', ha='center', va='center',
        color='#8a6d2d', fontsize=9, fontweight='bold', linespacing=1.2)

# Refund to Investors
refund_x, refund_y = 12.0, 1.3
refund_r = FancyBboxPatch((refund_x, refund_y - 0.5), 3.3, 1.0, boxstyle="round,pad=0.08",
                            facecolor='#fdf3e0', edgecolor='#8a6d2d', linewidth=2)
ax.add_patch(refund_r)
ax.text(refund_x + 1.65, refund_y + 0.15, 'REFUND → Investors', ha='center', va='center',
        color='#8a6d2d', fontsize=11, fontweight='bold')
ax.text(refund_x + 1.65, refund_y - 0.2, 'Full amount (no fees)', ha='center', va='center',
        color=MUTED, fontsize=9)

ax.annotate('', xy=(refund_x, refund_y), xytext=(11.0, 1.8),
            arrowprops=dict(arrowstyle='->', color='#8a6d2d', lw=2))

# Legend at bottom
ax.text(8, 0.4, '● Funds remain locked until funding goal met or deadline expires · All settlements are on-chain and immutable',
        ha='center', va='center', color=MUTED, fontsize=8.5, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/escrow_flow.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: escrow_flow.png")
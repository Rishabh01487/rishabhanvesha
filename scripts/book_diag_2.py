#!/usr/bin/env python3
"""Diagram 2: Blockchain Structure"""
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

fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(8, 8.6, 'Blockchain Structure — Block & Transaction Anatomy',
        ha='center', va='center', color=TEXT, fontsize=19, fontweight='bold')

fields = ['Previous Hash', 'Timestamp', 'Transactions[]', 'Nonce', 'Merkle Root', 'Difficulty']

def draw_block(x, y, block_num, block_hash):
    w, h = 3.6, 5.5
    # Block header bar
    header = FancyBboxPatch((x, y + h - 0.8), w, 0.8, boxstyle="round,pad=0.08",
                             facecolor=PRIMARY, edgecolor=PRIMARY, linewidth=2)
    ax.add_patch(header)
    ax.text(x + w/2, y + h - 0.4, f'Block #{block_num}', ha='center', va='center',
            color='white', fontsize=13, fontweight='bold')
    
    # Block body
    body = FancyBboxPatch((x, y), w, h - 0.8, boxstyle="round,pad=0.08",
                           facecolor=FILL, edgecolor=PRIMARY, linewidth=2)
    ax.add_patch(body)
    
    # Fields
    fy = y + h - 1.4
    for i, field in enumerate(fields):
        color = ACCENT if field == 'Transactions[]' else TEXT
        fw = 'bold' if field == 'Transactions[]' else 'normal'
        fs = 9.5 if field == 'Transactions[]' else 9
        ax.text(x + 0.25, fy, field, ha='left', va='center',
                color=color, fontsize=fs, fontweight=fw)
        # Value placeholder
        if field == 'Previous Hash':
            val = f'0x{block_hash[:8]}...'
        elif field == 'Transactions[]':
            val = f'[TX_{block_num}x, TX_{block_num}y]'
        elif field == 'Merkle Root':
            val = f'0xmerkle{block_num}ab'
        elif field == 'Nonce':
            val = str(42000 + block_num * 1337)
        elif field == 'Timestamp':
            val = f'2025-01-{10+block_num:02d} 09:00'
        else:
            val = str(3 + block_num)
        ax.text(x + w - 0.2, fy, val, ha='right', va='center',
                color=MUTED, fontsize=7.5)
        # Separator line
        if i < len(fields) - 1:
            ax.plot([x + 0.15, x + w - 0.15], [fy - 0.25, fy - 0.25],
                    color=MUTED, lw=0.5, alpha=0.5)
        fy -= 0.65
    
    # Block hash at bottom
    ax.text(x + w/2, y + 0.15, f'Hash: 0x{block_hash}...', ha='center', va='center',
            color=SECONDARY, fontsize=7, fontweight='bold')
    return (x, y + h/2)

# Draw 3 blocks
blocks = [
    (0.5, 1.0, 0, 'a3f7b2c1'),
    (5.5, 1.0, 1, 'e8d4f6a9'),
    (10.5, 1.0, 2, '7c2e8b5d'),
]

positions = []
for x, y, num, hsh in blocks:
    pos = draw_block(x, y, num, hsh)
    positions.append(pos)

# Chain arrows
for i in range(len(positions) - 1):
    x1 = positions[i][0] + 3.6
    y1 = positions[i][1]
    x2 = positions[i+1][0]
    ax.annotate('', xy=(x2, y1), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=2.5))
    ax.text((x1+x2)/2, y1 + 0.35, 'hash reference',
            ha='center', va='center', color=MUTED, fontsize=8, fontstyle='italic')

# Genesis label
ax.text(blocks[0][0] + 1.8, blocks[0][1] - 0.7, 'GENESIS', ha='center', va='center',
        color=ACCENT, fontsize=9, fontweight='bold')

# Transaction structure inset
inset_x, inset_y = 10.8, 7.0
inset_w, inset_h = 4.8, 1.5
inset_bg = FancyBboxPatch((inset_x - 0.1, inset_y - 0.1), inset_w + 0.2, inset_h + 0.2,
                           boxstyle="round,pad=0.15", facecolor='white',
                           edgecolor=ACCENT, linewidth=1.5, linestyle='--')
ax.add_patch(inset_bg)
ax.text(inset_x + inset_w/2, inset_y + inset_h - 0.15, 'Transaction Structure',
        ha='center', va='center', color=ACCENT, fontsize=10, fontweight='bold')

tx_fields = ['sender', 'receiver', 'amount', 'type', 'signature', 'timestamp']
tx_x = inset_x + 0.1
for i, f in enumerate(tx_fields):
    fx = tx_x + (i % 3) * 1.6
    fy = inset_y + inset_h - 0.55 - (i // 3) * 0.5
    pill = FancyBboxPatch((fx, fy - 0.12), 1.4, 0.35, boxstyle="round,pad=0.06",
                           facecolor='#e0f0fa', edgecolor=ACCENT, linewidth=1)
    ax.add_patch(pill)
    ax.text(fx + 0.7, fy + 0.05, f, ha='center', va='center',
            color=TEXT, fontsize=7.5, fontweight='bold')

# Chain label
ax.text(8, 0.5, '◀── Immutability guaranteed by cryptographic hash chain ──▶',
        ha='center', va='center', color=MUTED, fontsize=9, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/blockchain_structure.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: blockchain_structure.png")
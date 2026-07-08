#!/usr/bin/env python3
"""Diagram 1: Five-Layer Architecture"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

plt.rcParams['font.family'] = 'DejaVu Sans'

# Colors
PRIMARY = '#415b69'
ACCENT = '#3593c1'
SECONDARY = '#b14053'
BG = '#f6f7f7'
TEXT = '#1d1f20'
MUTED = '#707679'
FILL_LIGHT = '#e9ebec'
FILL_MID = '#edeeef'

fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

layers = [
    ("Security Layer", "Authentication · Authorization · Encryption\nDDoS Protection · Audit Logging", SECONDARY, 7.5),
    ("Application Layer", "REST API · GraphQL · WebSocket\nWeb Dashboard · Mobile SDK", PRIMARY, 6.2),
    ("AI Processing Layer", "Document Verification · OCR · NER\nFraud Detection · Risk Scoring", ACCENT, 4.9),
    ("Data Layer", "PostgreSQL · Redis Cache · IPFS Storage\nElasticsearch · Time-Series DB", PRIMARY, 3.6),
    ("Blockchain Layer", "Smart Contracts · AVM · Consensus\nToken Management · State Channels", SECONDARY, 2.3),
]

box_w = 10
box_h = 1.0
x_start = 3

for label, desc, color, y in layers:
    # Main box
    rect = FancyBboxPatch((x_start, y), box_w, box_h, boxstyle="round,pad=0.1",
                           facecolor=FILL_LIGHT, edgecolor=color, linewidth=2.5)
    ax.add_patch(rect)
    # Layer number circle
    idx = layers.index((label, desc, color, y)) + 1
    circle = plt.Circle((x_start + 0.7, y + 0.5), 0.32, color=color, alpha=0.9, zorder=5)
    ax.add_patch(circle)
    ax.text(x_start + 0.7, y + 0.5, str(idx), ha='center', va='center',
            color='white', fontsize=14, fontweight='bold', zorder=6)
    # Label
    ax.text(x_start + 1.4, y + 0.72, label, ha='left', va='center',
            color=TEXT, fontsize=15, fontweight='bold')
    # Description
    ax.text(x_start + 1.4, y + 0.3, desc, ha='left', va='center',
            color=MUTED, fontsize=9.5, linespacing=1.3)

# Arrows between layers
for i in range(len(layers) - 1):
    y_from = layers[i][3]
    y_to = layers[i + 1][3] + layers[0][1] if False else layers[i + 1][3] + box_h
    mid_x = x_start + box_w / 2
    ax.annotate('', xy=(mid_x, y_to), xytext=(mid_x, y_from),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.8, 
                               connectionstyle='arc3,rad=0'))
    # Also downward arrow
    ax.annotate('', xy=(mid_x + 1.5, y_from), xytext=(mid_x + 1.5, y_to),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.8, alpha=0.5,
                               connectionstyle='arc3,rad=0'))

# Bidirectional label
ax.text(x_start + box_w / 2, layers[2][3] + box_h + 0.25, '↕ bidirectional data flow',
        ha='center', va='center', color=MUTED, fontsize=8, fontstyle='italic')

# Title
ax.text(8, 8.7, 'Averon Platform — Five-Layer Architecture',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.3, 'Secure, modular, end-to-end asset tokenization infrastructure',
        ha='center', va='center', color=MUTED, fontsize=11)

# Side labels
ax.text(x_start - 0.3, 6.2, 'USER-\nFACING', ha='right', va='center',
        color=ACCENT, fontsize=9, fontweight='bold', linespacing=1.5, alpha=0.8)
ax.text(x_start - 0.3, 3.6, 'BACKEND\nSERVICES', ha='right', va='center',
        color=PRIMARY, fontsize=9, fontweight='bold', linespacing=1.5, alpha=0.8)
ax.text(x_start - 0.3, 2.3, 'LEDGER', ha='right', va='center',
        color=SECONDARY, fontsize=9, fontweight='bold', linespacing=1.5, alpha=0.8)

plt.savefig('/home/z/my-project/download/book_diagrams/five_layer_arch.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: five_layer_arch.png")
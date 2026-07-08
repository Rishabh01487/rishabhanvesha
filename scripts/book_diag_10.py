#!/usr/bin/env python3
"""Diagram 10: Averon Virtual Machine"""
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

ax.text(8, 8.5, 'Averon Virtual Machine (AVM)',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Dedicated execution runtime for Averon smart contracts',
        ha='center', va='center', color=MUTED, fontsize=11)

# Application Layer (top)
app_r = FancyBboxPatch((1.0, 6.8), 14.0, 0.9, boxstyle="round,pad=0.1",
                         facecolor=FILL, edgecolor=PRIMARY, linewidth=2)
ax.add_patch(app_r)
ax.text(8, 7.5, 'Application Layer', ha='center', va='center',
        color=PRIMARY, fontsize=14, fontweight='bold')
ax.text(8, 7.1, 'REST API  ·  Web Dashboard  ·  Mobile SDK  ·  Third-Party Integrations',
        ha='center', va='center', color=MUTED, fontsize=9)

# AVM Layer (center, large)
avm_r = FancyBboxPatch((0.5, 2.0), 15.0, 4.3, boxstyle="round,pad=0.15",
                         facecolor='#dceef8', edgecolor=ACCENT, linewidth=3)
ax.add_patch(avm_r)
ax.text(8, 5.9, 'AVERON VIRTUAL MACHINE (AVM)', ha='center', va='center',
        color=ACCENT, fontsize=16, fontweight='bold')

# AVM components
avm_components = [
    ("Smart Contract\nCompiler", 1.0, 3.5, [
        "Solidity-like syntax",
        "Formal verification",
        "Gas estimation",
        "AST optimization",
    ], PRIMARY),
    ("Execution\nEngine", 4.8, 3.5, [
        "Stack-based VM",
        "Deterministic execution",
        "Precompiled contracts",
        "Event emission",
    ], ACCENT),
    ("State\nManager", 8.6, 3.5, [
        "Merkle Patricia Trie",
        "Account state DB",
        "Storage slots",
        "State snapshots",
    ], '#6a8a45'),
    ("Consensus\nInterface", 12.4, 3.5, [
        "Block proposal",
        "Vote submission",
        "Finality proof",
        "Epoch management",
    ], SECONDARY),
]

for label, x, y, items, color in avm_components:
    # Component box
    cr = FancyBboxPatch((x, y), 3.2, 2.0, boxstyle="round,pad=0.1",
                          facecolor='white', edgecolor=color, linewidth=2)
    ax.add_patch(cr)
    # Header bar
    hr = FancyBboxPatch((x, y + 1.4), 3.2, 0.6, boxstyle="round,pad=0.06",
                          facecolor=color, edgecolor=color, linewidth=1.5)
    ax.add_patch(hr)
    ax.text(x + 1.6, y + 1.7, label, ha='center', va='center',
            color='white', fontsize=10, fontweight='bold', linespacing=1.2)
    # Items
    for i, item in enumerate(items):
        ax.text(x + 0.2, y + 1.15 - i * 0.3, f'• {item}', ha='left', va='center',
                color=TEXT, fontsize=8)

# Arrows between AVM components
for i in range(3):
    x1 = avm_components[i][1] + 3.2
    x2 = avm_components[i+1][1]
    y = 4.5
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.5))

# Blockchain Layer (bottom)
bc_r = FancyBboxPatch((1.0, 0.5), 14.0, 0.9, boxstyle="round,pad=0.1",
                        facecolor=FILL, edgecolor=PRIMARY, linewidth=2)
ax.add_patch(bc_r)
ax.text(8, 1.2, 'Blockchain Layer', ha='center', va='center',
        color=PRIMARY, fontsize=14, fontweight='bold')
ax.text(8, 0.8, 'Distributed Ledger  ·  Consensus Protocol  ·  Cryptographic Primitives  ·  P2P Network',
        ha='center', va='center', color=MUTED, fontsize=9)

# Arrows connecting layers
ax.annotate('', xy=(8, 6.8), xytext=(8, 6.3),
            arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=2.5))
ax.text(9.2, 6.55, 'Contract calls\n& events', ha='left', va='center', color=MUTED, fontsize=8, linespacing=1.2)

ax.annotate('', xy=(8, 2.0), xytext=(8, 1.4),
            arrowprops=dict(arrowstyle='<->', color=PRIMARY, lw=2.5))
ax.text(9.2, 1.7, 'State commits\n& proofs', ha='left', va='center', color=MUTED, fontsize=8, linespacing=1.2)

plt.savefig('/home/z/my-project/download/book_diagrams/avm_architecture.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: avm_architecture.png")
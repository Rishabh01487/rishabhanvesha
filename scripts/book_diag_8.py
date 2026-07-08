#!/usr/bin/env python3
"""Diagram 8: Security Defense-in-Depth"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Wedge
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

ax.text(8, 8.5, 'Security — Defense in Depth',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Multiple concentric layers of security from edge to blockchain immutability',
        ha='center', va='center', color=MUTED, fontsize=11)

# Concentric layers (right side visual)
cx, cy = 11.5, 4.5
layers_data = [
    (3.5, '#e9ebec', PRIMARY, 0.6, 'Blockchain\nImmutability'),
    (2.8, '#edeeef', ACCENT, 0.7, 'Audit Logging\n(Hash Chain)'),
    (2.1, '#e9ebec', '#6a8a45', 0.8, 'Input\nSanitization'),
    (1.4, '#edeeef', '#8a6d2d', 0.9, 'Rate\nLimiting'),
    (0.7, '#e9ebec', SECONDARY, 1.0, 'JWT\nAuth'),
]

# Draw concentric ellipses
for radius, facecolor, edgecolor, alpha, label in layers_data:
    e = Ellipse((cx, cy), radius * 2.2, radius * 2, facecolor=facecolor,
                edgecolor=edgecolor, linewidth=2.5, alpha=0.8)
    ax.add_patch(e)

# Core
core = plt.Circle((cx, cy), 0.35, color=SECONDARY, alpha=0.9, zorder=10)
ax.add_patch(core)
ax.text(cx, cy, '[L]', ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=11)

# Layer labels on the right
for i, (radius, _, edgecolor, alpha, label) in enumerate(layers_data):
    angle = np.pi/2 + i * 0.55
    lx = cx + radius * 1.15 * np.cos(angle)
    ly = cy + radius * 1.0 * np.sin(angle)
    if i < 3:
        lx = cx + 1.8
        ly = cy + 1.6 - i * 0.85
        ax.text(lx + 1.8, ly, label, ha='left', va='center', color=edgecolor,
                fontsize=9, fontweight='bold', linespacing=1.2)
        ax.plot([lx + 0.1, lx + 1.6], [ly, ly], color=edgecolor, lw=1, alpha=0.4)

# Left side: detailed layer boxes
details = [
    ("Layer 1: JWT Authentication", SECONDARY, [
        "RS256 signed tokens",
        "Token rotation (15 min access, 7 day refresh)",
        "Role-based access control (RBAC)",
        "Multi-factor authentication (MFA)",
    ]),
    ("Layer 2: Rate Limiting", '#8a6d2d', [
        "Sliding window: 100 req/min per user",
        "IP-based throttling: 1000 req/min",
        "Burst allowance with token bucket",
        "DDoS mitigation via CloudFlare",
    ]),
    ("Layer 3: Input Sanitization", '#6a8a45', [
        "Parameterized SQL queries",
        "XSS filter & CSP headers",
        "Schema validation (JSON Schema)",
        "File upload scanning (ClamAV)",
    ]),
    ("Layer 4: Audit Logging (Hash Chain)", ACCENT, [
        "Immutable hash chain of all actions",
        "Cryptographic linkage: H(n) = SHA256(prev + data)",
        "Tamper-evident audit trail",
        "Real-time anomaly detection",
    ]),
    ("Layer 5: Blockchain Immutability", PRIMARY, [
        "All critical state on-chain",
        "Consensus-validated transactions",
        "Immutable smart contract rules",
        "Cryptographic proof of history",
    ]),
]

box_x = 0.5
for i, (title, color, items) in enumerate(details):
    by = 6.8 - i * 1.35
    # Number badge
    badge = plt.Circle((box_x + 0.25, by + 0.3), 0.2, color=color, alpha=0.9, zorder=5)
    ax.add_patch(badge)
    ax.text(box_x + 0.25, by + 0.3, str(i+1), ha='center', va='center',
            color='white', fontsize=10, fontweight='bold', zorder=6)
    
    # Title
    ax.text(box_x + 0.6, by + 0.35, title, ha='left', va='center',
            color=TEXT, fontsize=10, fontweight='bold')
    # Items
    for j, item in enumerate(items):
        ax.text(box_x + 0.7, by + 0.05 - j * 0.2, f'• {item}', ha='left', va='center',
                color=MUTED, fontsize=7.5)

# Bottom
ax.text(8, 0.3, 'Each layer independently mitigates attack vectors — no single point of failure',
        ha='center', va='center', color=MUTED, fontsize=9, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/security_architecture.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: security_architecture.png")
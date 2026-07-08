#!/usr/bin/env python3
"""Diagram 12: Identity & Compliance Layer"""
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

ax.text(8, 8.5, 'Identity & Compliance Layer',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Decentralized identity management with jurisdiction-aware compliance',
        ha='center', va='center', color=MUTED, fontsize=11)

# Six components flowing left to right
components = [
    ("DID Wallet", ACCENT, [
        "W3C Decentralized Identifier",
        "Self-sovereign identity",
        "Key pair management",
        "Cross-chain identity portability",
        "Privacy-preserving proofs",
    ], "DID"),
    ("Verifiable\nCredentials", PRIMARY, [
        "W3C VC standard",
        "Issuer-signed claims",
        "Selective disclosure",
        "Revocation registry",
        "Credential manifest",
    ], "VC"),
    ("KYC/AML\nEngine", SECONDARY, [
        "Document verification (AI)",
        "Sanctions screening (OFAC/EU)",
        "PEP (Politically Exposed) check",
        "Adverse media monitoring",
        "Risk scoring (1-100)",
    ], "KYC"),
    ("Jurisdiction\nRules", '#8a6d2d', [
        "US (SEC Reg D, Reg S)",
        "EU (MiCA, GDPR)",
        "Singapore (MAS)",
        "UAE (VARA)",
        "Dynamic rule updates",
    ], "JUR"),
    ("Audit Trail", GREEN, [
        "Hash-chain immutability",
        "Consent records",
        "Access logs",
        "Decision explanations",
        "Regulatory reporting",
    ], "AUD"),
    ("Permission\nManager", '#5a4b8a', [
        "ABAC policy engine",
        "Role & attribute grants",
        "Resource-level ACLs",
        "Temporal access tokens",
        "Delegation chains",
    ], "PM"),
]

box_w = 2.2
box_h = 3.8
gap = 0.35
x_start = 0.5

for i, (label, color, items, icon) in enumerate(components):
    x = x_start + i * (box_w + gap)
    y = 2.5
    
    # Icon circle at top
    ic = plt.Circle((x + box_w/2, y + box_h + 0.5), 0.35, color=color, alpha=0.15, zorder=3)
    ax.add_patch(ic)
    ax.text(x + box_w/2, y + box_h + 0.5, icon, ha='center', va='center', fontsize=9, fontweight='bold', color=color, zorder=4)
    
    # Step number
    step = plt.Circle((x + 0.3, y + box_h - 0.1), 0.18, color=color, alpha=0.9, zorder=5)
    ax.add_patch(step)
    ax.text(x + 0.3, y + box_h - 0.1, str(i+1), ha='center', va='center',
            color='white', fontsize=8, fontweight='bold', zorder=6)
    
    # Main box
    r = FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.1",
                        facecolor=FILL, edgecolor=color, linewidth=2.2)
    ax.add_patch(r)
    
    # Header
    hr = FancyBboxPatch((x, y + box_h - 0.65), box_w, 0.65, boxstyle="round,pad=0.06",
                          facecolor=color, edgecolor=color, linewidth=1.5)
    ax.add_patch(hr)
    ax.text(x + box_w/2, y + box_h - 0.32, label, ha='center', va='center',
            color='white', fontsize=10, fontweight='bold', linespacing=1.2)
    
    # Items
    for j, item in enumerate(items):
        ax.text(x + 0.15, y + box_h - 1.0 - j * 0.5, f'• {item}',
                ha='left', va='center', color=TEXT, fontsize=7, linespacing=1.1)
    
    # Arrow to next
    if i < len(components) - 1:
        ax.annotate('', xy=(x + box_w + gap - 0.05, y + box_h/2),
                    xytext=(x + box_w + 0.05, y + box_h/2),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=2))

# User entry arrow (left)
ax.annotate('User\nOnboards', xy=(x_start, 4.4), xytext=(x_start - 1.2, 4.4),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2),
            color=ACCENT, fontsize=9, fontweight='bold', ha='center', va='center')

# Access granted (right)
last_x = x_start + 5 * (box_w + gap) + box_w
ax.annotate('', xy=(last_x + 1.2, 4.4), xytext=(last_x, 4.4),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))
ax.text(last_x + 1.3, 4.4, 'Access\nGranted', ha='left', va='center',
        color=GREEN, fontsize=9, fontweight='bold', linespacing=1.2)

# Bottom flow summary
flow_y = 1.2
flow_items = ["DID Created", "Credentials Issued", "KYC Cleared", "Jurisdiction Matched", "Audit Logged", "Permissions Set"]
for i, item in enumerate(flow_items):
    fx = x_start + i * (box_w + gap) + box_w/2
    ax.text(fx, flow_y, item, ha='center', va='center', color=components[i][1], fontsize=7.5, fontweight='bold')
    if i < len(flow_items) - 1:
        ax.annotate('', xy=(fx + box_w/2 + gap/2 - 0.05, flow_y),
                    xytext=(fx + box_w/2 + 0.05, flow_y),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, alpha=0.5))

ax.text(8, 0.6, 'End-to-end identity verification: from wallet creation to permissioned platform access',
        ha='center', va='center', color=MUTED, fontsize=9, fontstyle='italic')

plt.savefig('/home/z/my-project/download/book_diagrams/identity_compliance.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: identity_compliance.png")
#!/usr/bin/env python3
"""Diagram 9: Database Schema Overview"""
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

ax.text(8, 8.5, 'Database Schema Overview',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Six domain clusters with relational and document stores',
        ha='center', va='center', color=MUTED, fontsize=11)

groups = [
    ("User Management", ACCENT, 0.3, 3.8, [
        ("users", "id, email, password_hash,\nrole, created_at, status"),
        ("wallets", "id, user_id, address,\nbalance, currency, type"),
        ("kyc_records", "id, user_id, status,\nverified_at, documents"),
        ("sessions", "id, user_id, token,\nip, user_agent, expires"),
    ]),
    ("Asset Management", PRIMARY, 5.5, 3.8, [
        ("assets", "id, owner_id, type,\ntitle, status, value"),
        ("documents", "id, asset_id, hash,\ntype, upload_date, ai_score"),
        ("tokens", "id, asset_id, supply,\nprice, contract_addr"),
    ]),
    ("Escrow", '#6a8a45', 10.5, 5.5, [
        ("escrow_accounts", "id, asset_id, amount,\ndeadline, status"),
        ("escrow_txns", "id, escrow_id, type,\namount, from, to, tx_hash"),
    ]),
    ("Trading", SECONDARY, 10.5, 2.5, [
        ("orders", "id, user_id, asset_token_id,\nside, price, qty, status"),
        ("trades", "id, maker_id, taker_id,\nprice, qty, fee, timestamp"),
    ]),
    ("Economic Model", '#8a6d2d', 0.3, 0.3, [
        ("token_supply", "id, total_minted,\ntotal_burned, circulating"),
        ("fee_schedule", "id, fee_type, rate,\nrecipient, active"),
        ("rewards", "id, user_id, amount,\nreason, distributed_at"),
    ]),
    ("Payment", '#5a4b8a', 5.5, 0.3, [
        ("payment_methods", "id, user_id, type,\nprovider, last_four"),
        ("transactions", "id, user_id, amount,\ncurrency, status, ref"),
        ("payouts", "id, escrow_id, amount,\nrecipient, status, tx_hash"),
    ]),
]

def draw_table_group(gx, gy, title, color, tables):
    # Cluster background
    # Calculate cluster size
    cw = 4.6
    ch = 0.6 + len(tables) * 1.05
    cluster = FancyBboxPatch((gx, gy), cw, ch, boxstyle="round,pad=0.15",
                              facecolor=color, edgecolor=color, linewidth=2, alpha=0.08)
    ax.add_patch(cluster)
    cluster_border = FancyBboxPatch((gx, gy), cw, ch, boxstyle="round,pad=0.15",
                                      facecolor='none', edgecolor=color, linewidth=1.5, alpha=0.4)
    ax.add_patch(cluster_border)
    
    # Title
    ax.text(gx + cw/2, gy + ch - 0.2, title, ha='center', va='center',
            color=color, fontsize=11, fontweight='bold')
    
    # Tables
    for i, (tname, fields) in enumerate(tables):
        ty = gy + ch - 0.7 - i * 1.05
        tw = 4.2
        th = 0.85
        # Table header
        header = FancyBboxPatch((gx + 0.2, ty + th - 0.3), tw, 0.3, boxstyle="round,pad=0.04",
                                 facecolor=color, edgecolor=color, linewidth=1.2)
        ax.add_patch(header)
        ax.text(gx + 0.2 + tw/2, ty + th - 0.15, f'▸ {tname}', ha='center', va='center',
                color='white', fontsize=8.5, fontweight='bold')
        # Fields
        ax.text(gx + 0.4, ty + th/2 - 0.15, fields, ha='left', va='center',
                color=MUTED, fontsize=6.5, linespacing=1.3)

for title, color, gx, gy, tables in groups:
    draw_table_group(gx, gy, title, color, tables)

# Relationship lines
# Users -> Wallets
ax.annotate('', xy=(5.5, 6.0), xytext=(4.9, 5.8),
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, linestyle=':'))
# Users -> KYC
ax.annotate('', xy=(5.5, 4.8), xytext=(4.9, 5.2),
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, linestyle=':'))
# Assets -> Documents
ax.annotate('', xy=(10.5, 5.8), xytext=(10.1, 5.8),
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, linestyle=':'))
# Assets -> Tokens
ax.annotate('', xy=(10.5, 5.0), xytext=(10.1, 5.0),
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, linestyle=':'))
# Escrow -> Payouts
ax.annotate('', xy=(5.5, 1.2), xytext=(5.5, 2.5),
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, linestyle=':'))

plt.savefig('/home/z/my-project/download/book_diagrams/database_schema.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: database_schema.png")
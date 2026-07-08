#!/usr/bin/env python3
"""Diagram 3: AI Document Verification Pipeline"""
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

ax.text(8, 8.5, 'AI Document Verification Pipeline',
        ha='center', va='center', color=TEXT, fontsize=20, fontweight='bold')
ax.text(8, 8.1, 'Five-stage automated document processing for asset verification',
        ha='center', va='center', color=MUTED, fontsize=11)

stages = [
    ("Image\nPreprocessing", ["Rotation\nCorrection", "Noise\nReduction", "Contrast\nEnhancement", "Skew\nDetection"]),
    ("OCR\nExtraction", ["Tesseract\nEngine", "Layout\nAnalysis", "Table\nDetection", "Handwriting\nRecognition"]),
    ("Text\nClassification", ["BERT-based\nClassifier", "Document\nType Detection", "Confidence\nScoring", "Language\nDetection"]),
    ("Named Entity\nRecognition", ["spaCy NER\nModel", "Address\nExtraction", "Amount\nParsing", "Date\nNormalization"]),
    ("Verification\nScoring", ["Cross-Reference\nCheck", "Forgery\nDetection", "Completeness\nAudit", "Risk\nAssessment"]),
]

box_w = 2.4
box_h = 1.2
sub_w = 1.05
sub_h = 0.7
gap = 0.7
x_start = 0.8
y_main = 6.2
y_sub = 3.2

for i, (label, subs) in enumerate(stages):
    x = x_start + i * (box_w + gap)
    
    # Stage number
    num_circle = plt.Circle((x + box_w/2, y_main + box_h + 0.4), 0.28,
                             color=ACCENT if i < 4 else SECONDARY, alpha=0.9, zorder=5)
    ax.add_patch(num_circle)
    ax.text(x + box_w/2, y_main + box_h + 0.4, str(i+1), ha='center', va='center',
            color='white', fontsize=12, fontweight='bold', zorder=6)
    
    # Main box
    color = ACCENT if i < 4 else SECONDARY
    rect = FancyBboxPatch((x, y_main), box_w, box_h, boxstyle="round,pad=0.1",
                           facecolor=FILL, edgecolor=color, linewidth=2.5)
    ax.add_patch(rect)
    ax.text(x + box_w/2, y_main + box_h/2, label, ha='center', va='center',
            color=TEXT, fontsize=11, fontweight='bold', linespacing=1.3)
    
    # Arrow to next stage
    if i < len(stages) - 1:
        ax.annotate('', xy=(x + box_w + 0.1, y_main + box_h/2),
                    xytext=(x + box_w - 0.1, y_main + box_h/2),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=2))
    
    # Vertical connector
    ax.plot([x + box_w/2, x + box_w/2], [y_main, y_sub + 0.2],
            color=MUTED, lw=1, linestyle='--', alpha=0.5)
    
    # Sub-operation boxes
    for j, sub in enumerate(subs):
        sx = x + j * (sub_w + 0.05)
        sy = y_sub + (3 - j) * (sub_h + 0.12) - sub_h
        sr = FancyBboxPatch((sx, sy), sub_w, sub_h, boxstyle="round,pad=0.06",
                             facecolor='#edeeef', edgecolor=PRIMARY, linewidth=1, alpha=0.8)
        ax.add_patch(sr)
        ax.text(sx + sub_w/2, sy + sub_h/2, sub, ha='center', va='center',
                color=MUTED, fontsize=7, linespacing=1.2)

# Input/Output labels
ax.text(x_start - 0.1, y_main + box_h/2, 'Raw\nDocument', ha='right', va='center',
        color=ACCENT, fontsize=9, fontweight='bold', linespacing=1.3)
ax.annotate('', xy=(x_start - 0.05, y_main + box_h/2),
            xytext=(x_start - 0.6, y_main + box_h/2),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))

last_x = x_start + 4 * (box_w + gap) + box_w
ax.text(last_x + 0.6, y_main + box_h/2, 'Verified\n  Score', ha='left', va='center',
        color=SECONDARY, fontsize=9, fontweight='bold', linespacing=1.3)
ax.annotate('', xy=(last_x + 0.55, y_main + box_h/2),
            xytext=(last_x + 0.05, y_main + box_h/2),
            arrowprops=dict(arrowstyle='->', color=SECONDARY, lw=2))

# Confidence bar at bottom
bar_y = 1.3
bar_x = x_start
bar_w_total = 4 * (box_w + gap) + box_w
ax.text(bar_x, bar_y + 0.5, 'Confidence Threshold: 85%', ha='left', va='center',
        color=TEXT, fontsize=9, fontweight='bold')
# Bar background
bg_bar = FancyBboxPatch((bar_x, bar_y), bar_w_total, 0.35, boxstyle="round,pad=0.04",
                          facecolor='#edeeef', edgecolor=MUTED, linewidth=1)
ax.add_patch(bg_bar)
# Bar fill (92%)
fill_bar = FancyBboxPatch((bar_x, bar_y), bar_w_total * 0.92, 0.35, boxstyle="round,pad=0.04",
                            facecolor=ACCENT, edgecolor=ACCENT, linewidth=1, alpha=0.7)
ax.add_patch(fill_bar)
ax.text(bar_x + bar_w_total * 0.92 + 0.2, bar_y + 0.17, '92%', ha='left', va='center',
        color=ACCENT, fontsize=10, fontweight='bold')

plt.savefig('/home/z/my-project/download/book_diagrams/ai_pipeline.png',
            dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print("OK: ai_pipeline.png")
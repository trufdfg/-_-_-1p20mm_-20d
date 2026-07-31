from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = Path(__file__).resolve().parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 1.0,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})
COLORS = {
    "blue": "#1f5a99", "orange": "#d9822b", "green": "#3b8a5a",
    "purple": "#7f5aa6", "red": "#b73a4a", "gray": "#5b6670",
    "dark": "#111827", "lightgray": "#e5e7eb"
}
def clean_axes(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis:
        ax.grid(axis=grid_axis, color="#e5e7eb", linewidth=0.6, zorder=0)
def savefig(fig, stem):
    fig.tight_layout(pad=0.8)
    fig.savefig(BASE / f"{stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(BASE / f"{stem}.pdf", bbox_inches="tight")
    print("saved:", BASE / f"{stem}.png")
    print("saved:", BASE / f"{stem}.pdf")

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

df = pd.read_csv(BASE / 'data.csv')
fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=300)
ax.set_axis_off()
for _, r in df.iterrows():
    x,y,w,h = r['x'],r['y'],r['w'],r['h']
    color = COLORS[r['color']]
    box = FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.015,rounding_size=0.018",
                         linewidth=2.0, edgecolor=color, facecolor="white")
    ax.add_patch(box)
    ax.text(x+w/2, y+h*0.66, r['title'], ha='center', va='center', fontsize=13, fontweight='bold', color=color)
    ax.text(x+w/2, y+h*0.35, r['subtitle'], ha='center', va='center', fontsize=10.5, color=COLORS['dark'])

def arrow(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=16, linewidth=1.4, color=COLORS['gray']))
arrow((0.33,0.73),(0.38,0.73)); arrow((0.66,0.73),(0.71,0.73)); arrow((0.85,0.62),(0.85,0.44)); arrow((0.71,0.33),(0.66,0.33)); arrow((0.38,0.33),(0.33,0.33))
ax.text(0.05, 0.05, 'Trace-water screening workflow for silicone oil in high-voltage cable terminals', fontsize=12.5, color=COLORS['dark'])
ax.set_xlim(0,1); ax.set_ylim(0,1)
savefig(fig, 'Figure_01_workflow')

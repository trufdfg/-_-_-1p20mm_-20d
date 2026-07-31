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

df=pd.read_csv(BASE/'data.csv')
fig, ax=plt.subplots(figsize=(3.3,3.0), dpi=300)
ax.bar(df['kf_mgkg'].astype(str),df['within_level_cv_percent'],color=COLORS['purple'],edgecolor=COLORS['dark'],linewidth=0.5)
ax.set_xlabel(r'KF moisture (mg kg$^{-1}$)'); ax.set_ylabel('Within-level CV (%)')
ax.set_ylim(0,37); clean_axes(ax); ax.text(-0.12,1.05,'b', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig5b_within_level_cv')

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
cols=df['type'].map({'Endpoint':COLORS['red'],'Interior':COLORS['green']})
ax.bar(df['held_out_kf_mgkg'].astype(str),df['holdout_rmse_mgkg'],color=cols,edgecolor=COLORS['dark'],linewidth=0.6)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=COLORS['red'],edgecolor=COLORS['dark'],label='Endpoint'),Patch(facecolor=COLORS['green'],edgecolor=COLORS['dark'],label='Interior')], frameon=False, loc='upper right', fontsize=8)
ax.set_xlabel(r'Held-out KF moisture (mg kg$^{-1}$)'); ax.set_ylabel(r'Holdout RMSE (mg kg$^{-1}$)')
ax.set_ylim(0,31.5); clean_axes(ax); ax.text(-0.12,1.05,'c', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig5c_holdout_rmse')

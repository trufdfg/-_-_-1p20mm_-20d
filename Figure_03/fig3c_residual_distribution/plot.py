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
ax.hist(df['residual_mgkg'], bins=np.arange(-40,22,5), color=COLORS['blue'], edgecolor='white', linewidth=0.4)
mean_val=df['residual_mgkg'].mean()
ax.axvline(mean_val, color=COLORS['orange'], lw=1.2, ls='--')
ax.axvline(0, color=COLORS['gray'], lw=1.0, ls='--')
ax.text(-35,88, 'mean=%.2f'%mean_val, fontsize=8.5)
ax.set_xlabel(r'Residual (mapped - KF, mg kg$^{-1}$)'); ax.set_ylabel('Scan count')
ax.set_xlim(-40,20); clean_axes(ax); ax.text(-0.12,1.05,'c', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig3c_residual_distribution')

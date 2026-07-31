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
colors={'North':COLORS['blue'],'South':COLORS['orange']}
for side,g in df.groupby('side'):
    ax.errorbar(g['kf_mgkg'],g['mapped_mgkg'],yerr=g['mapped_sd'],fmt='o',ms=5.2,color=colors[side],ecolor='#dbe2ea',elinewidth=1.0,capsize=0,label=side,zorder=3)
    for _,r in g.iterrows():
        ax.text(r['kf_mgkg']+0.08,r['mapped_mgkg']+0.05,r['sample'],fontsize=8)
ax.plot([77.5,87],[77.5,87],ls='--',color=COLORS['gray'],lw=1.0)
ax.set_xlabel(r'KF moisture (mg kg$^{-1}$)'); ax.set_ylabel(r'Mapped moisture (mg kg$^{-1}$)')
ax.set_xlim(77.6,86.9); ax.set_ylim(77.6,86.9)
ax.legend(frameon=False, loc='upper left')
clean_axes(ax); ax.text(-0.12,1.05,'a', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig4a_field_mapping')

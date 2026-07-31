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
fig, ax=plt.subplots(figsize=(3.0,2.75), dpi=300)
style={75:'-',84:'--',91:'-.',99:':',113:'--'}
color={75:COLORS['blue'],84:COLORS['orange'],91:COLORS['green'],99:COLORS['purple'],113:COLORS['red']}
for kf,g in df.groupby('kf_mgkg'):
    ax.plot(g['frequency_thz'],g['eps_real'], style[int(kf)], lw=1.15, color=color[int(kf)])
ax.set_xlabel('Frequency (THz)'); ax.set_ylabel(r"Dielectric constant, $\epsilon'$")
ax.set_xlim(0.5,2.0); ax.set_ylim(0.55,2.45); ax.set_yticks([1.0,1.5,2.0])
clean_axes(ax); ax.text(-0.18,1.05,'c', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig2c_dielectric_spectra')

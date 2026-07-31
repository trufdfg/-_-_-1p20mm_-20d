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
x=df['kf_mgkg'].to_numpy(); y=df['eps_real_1p9418'].to_numpy()
coef=np.polyfit(x,y,1); xx=np.linspace(72,116,100); yy=np.polyval(coef,xx)
yhat=np.polyval(coef,x); r2=1-((y-yhat)**2).sum()/((y-y.mean())**2).sum()
fig, ax=plt.subplots(figsize=(3.0,2.75), dpi=300)
ax.scatter(x,y,s=26,color=COLORS['blue'],edgecolor='white',linewidth=0.5,zorder=3)
ax.plot(xx,yy,color=COLORS['red'],lw=1.2)
ax.text(75,1.47, '1.9418 THz\n$R^2$ = %.3f'%r2, fontsize=8.5, ha='left', va='top')
ax.set_xlabel(r'KF moisture (mg kg$^{-1}$)'); ax.set_ylabel(r"Dielectric constant, $\epsilon'$")
ax.set_xlim(73,115); ax.set_ylim(1.03,1.52); ax.set_xticks([80,100]); ax.set_yticks([1.1,1.2,1.3,1.4,1.5])
clean_axes(ax); ax.text(-0.18,1.05,'d', transform=ax.transAxes, fontsize=11, fontweight='bold', va='top')
savefig(fig,'fig2d_sensitive_frequency_fit')

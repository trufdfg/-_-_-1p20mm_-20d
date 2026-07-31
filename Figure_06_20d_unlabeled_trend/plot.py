# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.2,
    "axes.linewidth": 0.9,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

COLORS = {
    0: "#1f77b4",
    3: "#ff7f0e",
    10: "#2ca02c",
    15: "#9467bd",
    20: "#6b7280",
    30: "#d62728",
}

def clean(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis:
        ax.grid(axis=grid_axis, color="#e5e7eb", linewidth=0.5, zorder=0)

spec12 = pd.read_csv(BASE / "data_spectra_1p20mm_day_mean.csv")
unit = pd.read_csv(BASE / "data_unit_feature_1p9418.csv")
pca = pd.read_csv(BASE / "data_pca_unit_scores.csv")
var = pd.read_csv(BASE / "data_pca_variance.csv")
unit["cell_thickness_mm"] = 1.20
pca["cell_thickness_mm"] = 1.20
pc1_var = 100 * float(var.loc[var["component"] == "PC1", "explained_variance_ratio"].iloc[0])
pc2_var = 100 * float(var.loc[var["component"] == "PC2", "explained_variance_ratio"].iloc[0])

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.35), dpi=300)

# a. Mean spectra under the corrected uniform 1.20 mm cell path
ax = axes[0]
for day in [3, 10, 15, 20, 30]:
    g = spec12[spec12["day"] == day].sort_values("frequency_thz")
    if g.empty:
        continue
    label = "20 d unlabeled" if day == 20 else f"{day} d"
    ls = "--" if day == 20 else "-"
    lw = 1.35 if day == 20 else 1.05
    ax.plot(g["frequency_thz"], g["eps_real_mean"], color=COLORS[day], lw=lw, ls=ls, label=label)
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel(r"Dielectric constant, $\epsilon'$")
ax.set_xlim(0.5, 2.0)
ax.set_ylim(1.15, 1.65)
clean(ax)
ax.legend(frameon=False, fontsize=6.2, loc="best", handlelength=1.7)
ax.text(0.02, 0.05, "Uniform 1.20 mm cell", transform=ax.transAxes, fontsize=6.4, color="#4b5563", va="bottom")
ax.text(-0.18, 1.06, "a", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")

# b. Unit-level response; 20 d remains unlabeled and is shown as open diamonds
ax = axes[1]
for day in sorted(unit["day"].unique()):
    g = unit[unit["day"] == day]
    face = "white" if day == 20 else COLORS.get(int(day), "#6b7280")
    edge = COLORS.get(int(day), "#6b7280")
    marker = "D" if day == 20 else "o"
    ax.scatter(
        g["day"], g["eps_real_1p9418_mean"],
        s=32 if day == 20 else 24,
        marker=marker,
        facecolors=face, edgecolors=edge, linewidths=0.9, alpha=0.95,
        zorder=3
    )
ax.axvline(20, color="#9ca3af", ls="--", lw=0.8)
ax.text(20.4, ax.get_ylim()[1] - 0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]), "unlabeled", fontsize=6.5, color="#4b5563", va="top")
ax.set_xlabel("Moisture uptake time (d)")
ax.set_ylabel(r"$\epsilon'$ at 1.9418 THz")
ax.set_xlim(-1.5, 31.5)
clean(ax)
legend_elements = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor="#9ca3af", markeredgecolor="#4b5563", markersize=5, label="sampling unit"),
    Line2D([0], [0], marker="D", color="none", markerfacecolor="white", markeredgecolor=COLORS[20], markersize=5, label="20 d")
]
ax.legend(handles=legend_elements, frameon=False, fontsize=6.3, loc="best", handletextpad=0.4)
ax.text(-0.18, 1.06, "b", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")

# c. PCA projection
ax = axes[2]
for _, row in pca.iterrows():
    day = int(row["day"])
    if day == 20:
        marker = "D"; face = "white"; edge = COLORS[20]; size = 30
    else:
        marker = "o"; face = COLORS.get(day, "#6b7280"); edge = face; size = 22
    ax.scatter(row["pc1"], row["pc2"], s=size, marker=marker, facecolors=face, edgecolors=edge, linewidths=0.9, zorder=3)
ax.axhline(0, color="#d1d5db", lw=0.6)
ax.axvline(0, color="#d1d5db", lw=0.6)
ax.set_xlabel(f"PC1 ({pc1_var:.1f}%)")
ax.set_ylabel(f"PC2 ({pc2_var:.1f}%)")
clean(ax, grid_axis=None)
legend_days = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS[d], markeredgecolor=COLORS[d], markersize=5, label=f"{d} d")
    for d in [0, 3, 10, 15, 30]
]
legend_days.append(Line2D([0], [0], marker="D", color="none", markerfacecolor="white", markeredgecolor=COLORS[20], markersize=5, label="20 d"))
ax.legend(handles=legend_days, frameon=False, fontsize=6.0, loc="best", ncol=1, handletextpad=0.35)
ax.text(-0.18, 1.06, "c", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")

fig.tight_layout(w_pad=1.05)
fig.savefig(BASE / "Figure_06_20d_unlabeled_trend.png", dpi=600, bbox_inches="tight")
fig.savefig(BASE / "Figure_06_20d_unlabeled_trend.pdf", bbox_inches="tight")
print("saved", BASE / "Figure_06_20d_unlabeled_trend.png")
print("saved", BASE / "Figure_06_20d_unlabeled_trend.pdf")

"""Figures for the reader's summary of the Blas & Oller check (summary/blas-oller-check-summary.pdf).

Every plotted number is copied from a log in ../notes/, named next to each array, so the
figures show exactly what the check's scripts printed. Run from the repository root:
    python3 checks/2026-10-11-blas-oller-gw-decay/summary/make_figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "fig"
OUT.mkdir(exist_ok=True)

INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
REF = "#8a8984"
SERIES_1 = "#2a78d6"
SERIES_2 = "#eb6834"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "text.color": INK,
    "axes.labelcolor": INK_2,
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "none",
    "figure.dpi": 150,
})


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# Figure 4 in the summary. Yield of the outgoing half of B&O's own packet, produced beyond r_min, as a fraction
# of B&O's exact S-matrix total (x C_coh). notes/taskB_outgoing.log, section (h).
r_min = np.array([0.159, 0.318, 0.5, 1, 2, 5, 10, 30, 100, 300, 1000])
frac = np.array([1.752e-3, 4.662e-4, 1.530e-4, 2.401e-5, 3.364e-6, 2.305e-7,
                 2.947e-8, 1.108e-9, 3.007e-11, 1.115e-12, 3.013e-14])

fig, ax = plt.subplots(figsize=(5.6, 3.1))
ref_r = np.array([3, 1000])
ref = 100 * frac[r_min == 100][0] * (ref_r / 100.0) ** -3  # drawn 100x above the data so both show
ax.plot(ref_r, ref, color=REF, lw=1.2, ls=(0, (4, 3)), zorder=1)
ax.text(170, 100 * frac[r_min == 100][0] * 1.7 ** -3 * 4, "reference slope −3", color=INK_2, fontsize=8.5)
ax.plot(r_min, frac, color=SERIES_1, lw=1.6, marker="o", ms=4.5, mec="white", mew=0.8, zorder=3)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("r_min, the radius beyond which pairs are counted (wavelengths)")
ax.set_ylabel("fraction of B&O's total")
ax.annotate("1.8e-3 at λ/2π", (0.159, 1.752e-3), (0.45, 1.2e-2), color=INK, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=REF, lw=0.8))
ax.annotate("3e-11 at 100λ", (100, 3.007e-11), (8, 3e-12), color=INK, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=REF, lw=0.8))
ax.set_ylim(1e-14, 1e-1)
save(fig, "fig4_yield_vs_rmin")


# Figure 1 in the summary. Coefficient of eq. 8 for physical coherent shells, as a fraction of B&O's 3/(25 pi).
# notes/taskA3b_bo_plus_grid2.log (literal real-f shell) and notes/taskA3b_smooth.log (binary,
# linear); circular polarisation is exactly 0 (report section 4.1).
labels = ["Circular-binary quadrupole", "Linear quadrupole", "B&O's literal shell, physical phases",
          "Purely circular polarisation"]
values = [0.604477, 0.337429, 0.25391, 0.0]

fig, ax = plt.subplots(figsize=(5.6, 2.3))
y = np.arange(len(labels))[::-1]
ax.barh(y, values, height=0.5, color=SERIES_1, zorder=2)
ax.axvline(1.0, color=REF, lw=1.2, ls=(0, (4, 3)), zorder=1)
ax.text(0.985, y[0] + 0.42, "B&O eq. 8 = 1", color=INK_2, fontsize=8.5, ha="right")
for yi, v in zip(y, values):
    ax.text(v + 0.015, yi, f"{v:.3f}" if v else "0 (exactly)", va="center", fontsize=8.5, color=INK)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlim(0, 1.05)
ax.set_xlabel("coefficient ÷ B&O's 3/(25π)")
ax.grid(axis="y", visible=False)
save(fig, "fig1_coefficients")


# Figure 3 in the summary. Time profile of pair production for B&O's own state: R(t)/R(0) = sinc^4(sigma t/2),
# whose area equals a rectangle of height 1 and width 4 pi/(3 sigma). Exact-kinematics points:
# notes/taskC1.log, part (d), at sigma/omega = 0.1.
st = np.linspace(-14, 14, 1401)
u = st / 2
sinc4 = np.where(u == 0, 1.0, (np.sin(u) / np.where(u == 0, 1, u)) ** 4)
pts_t = np.array([0, 0.5, 1.0, 1.5, 2.0])
pts_r = np.array([1.0, 0.95889, 0.84453, 0.68088, 0.49946])
w = 4 * np.pi / 3

fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.plot([-w / 2, -w / 2, w / 2, w / 2], [0, 1, 1, 0], color=REF, lw=1.2, ls=(0, (4, 3)), zorder=1)
ax.plot(st, sinc4, color=SERIES_1, lw=1.6, zorder=2)
ax.plot(pts_t, pts_r, ls="none", marker="o", ms=5, color=SERIES_2, mec="white", mew=0.8, zorder=3)
ax.text(2.6, 0.83, "exact kinematics\n(σ/ω = 0.1)", color=INK, fontsize=8.5)
ax.text(-13.5, 0.83, "same area:\nheight 1, width 4π/(3σ)", color=INK_2, fontsize=8.5)
ax.text(5.2, 0.12, "sinc⁴(σt/2)", color=INK, fontsize=8.5)
ax.set_xlabel("σt (time in units of 1/σ, the packet's inverse bandwidth)")
ax.set_ylabel("pair rate ÷ peak rate")
ax.set_xlim(-14, 14)
ax.set_ylim(0, 1.12)
save(fig, "fig3_time_profile")


# Figure 2 in the summary. Where B&O's probability is generated: share of the total produced inside a sphere of
# radius r around the focus. notes/taskB_where_grid.log ("window in ...").
r = np.array([0.5, 1, 2, 4, 8])
l0 = np.array([0.6078, 0.8499, 0.9526, 0.9870, 0.9967])
l2 = np.array([0.0929, 0.4941, 0.8209, 0.9495, 0.9869])

fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.plot(r, l0, color=SERIES_1, lw=1.6, marker="o", ms=4.5, mec="white", mew=0.8)
ax.plot(r, l2, color=SERIES_2, lw=1.6, marker="s", ms=4.5, mec="white", mew=0.8)
ax.text(0.52, 0.93, "spherical (l = 0) shell", color=INK, fontsize=8.5)
ax.text(1.45, 0.42, "quadrupole (l = 2) shell", color=INK, fontsize=8.5)
ax.set_xscale("log", base=2)
ax.set_xticks(r)
ax.set_xticklabels(["λ/2", "λ", "2λ", "4λ", "8λ"])
ax.set_xlabel("radius of the sphere around the focus")
ax.set_ylabel("share of the total")
ax.set_ylim(0, 1.05)
save(fig, "fig2_where_generated")

print("wrote", sorted(p.name for p in OUT.glob("*.svg")))

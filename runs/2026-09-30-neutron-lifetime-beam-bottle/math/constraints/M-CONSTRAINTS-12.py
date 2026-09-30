"""M-CONSTRAINTS-12 (F14, K10): size of each systematic needed. Gap D = tau_BL1 - tau_UCN; fraction D/tau_BL1;
rate 1/tau_UCN - 1/tau_BL1 = D/(tau_UCN tau_BL1). A lifetime shift dt at tau corresponds to a rate dt/tau^2.
Material-bottle mean: inverse-variance mean of Gravitrap, Serebrov 04/5, MAMBO II, Steyerl, Arzumanov (stat (+) sys),
error scaled by S = sqrt(chi2/(N-1))."""
import math
from _common import near, TAU_BL1, S_BL1, TAU_UCN, TAU_GRAV, S_GRAV, wmean
from math_checks import identity, series, units, finish

identity("1/a - 1/b", "(b - a)/(a*b)")
series("1/a - 1/(a + d)", "d", 0, 2, "d/a**2")
units("(9.88 s) / ((877.82 s) * (887.7 s))", "frequency")
D = TAU_BL1 - TAU_UCN
near("gap", D, 9.88, 0.006); near("fraction %", 100 * D / TAU_BL1, 1.113, 6e-4)
rate = 1 / TAU_UCN - 1 / TAU_BL1
near("rate 1e-5/s", rate * 1e5, 1.268, 6e-4)
near("x BL1 sys 1.9", D / 1.9, 5.2, 0.06); near("x BL1 total", D / S_BL1, 4.4, 0.06)
near("sigma of 2.2 s item", D / 2.2, 4.5, 0.06); near("sigma of 1.7 s line", D / 1.7, 5.8, 0.06)
near("sigma of 0.8 s items", D / 0.8, 12.35, 0.1)
near("x nonlinearity 5.3", D / 5.3, 1.86, 0.05); near("x absorption 5.4", D / 5.4, 1.83, 0.05)
near("Caylor 0.3% in s", 0.003 * TAU_BL1, 2.7, 0.06); near("Caylor fraction of gap", 0.003 * TAU_BL1 / D, 0.27, 0.006)
near("UCNtau multiple of +0.20 s", D / 0.20, 49, 0.6)
rate_g = 1 / TAU_GRAV - 1 / TAU_BL1
near("Gravitrap rate 1e-6/s", rate_g * 1e6, 7.9, 0.06)
near("Gravitrap multiple of 0.6 s", (TAU_BL1 - TAU_GRAV) / 0.6, 10, 0.4)
near("material weaker by", 1 - rate_g / rate, 0.38, 0.006)
mat = [(TAU_GRAV, S_GRAV), (878.5, math.hypot(0.7, 0.3)), (880.7, math.hypot(1.3, 1.2)),
       (882.5, math.hypot(1.4, 1.5)), (880.2, 1.2)]
m, s, chi2 = wmean(mat)
S = math.sqrt(chi2 / 4)
near("material mean", m, 880.03, 0.006); near("material err (scaled)", s * max(S, 1), 0.70, 0.006)
near("material chi2", chi2, 8.2, 0.06)
raise SystemExit(finish())

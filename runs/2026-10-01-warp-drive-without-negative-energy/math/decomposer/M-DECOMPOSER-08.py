"""M-DECOMPOSER-08: all-observer NEC on the rebuilt shell (published mass 4.49e27 kg, R1 = 10 m,
R2 = 20 m) as a function of beta_warp. Uses the run's shared tools warp_shell (metric) and
numeric_stress_energy (finite-difference Einstein tensor, all-observer classification); the
sampling, the lines and the bisection are ours, not the lens's script.
Lines: r = 8..22 m (step 0.25 m) at polar angles 90 deg (perpendicular to the shift, along z) and
45 deg in the x-z plane; h = 0.05 m. Geometric units, T in 1/m^2.
Claims: beta = 0.02 clean (and beta = 0); beta = 0.04 violates the NEC, worst about -7.9e-5 m^-2
near r = 12.25 m perpendicular; first NEC failure at beta = 0.0246."""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np
from math_checks import quantity, identity, finish
from warp_shell import build_shell
from numeric_stress_energy import NumericSpacetime

shell = build_shell(M=4.49e27, R1=10.0, R2=20.0, beta_warp=0.0)
rs = np.arange(8.0, 22.0 + 1e-9, 0.25)
pts = []
for ang in (90.0, 45.0):
    th = math.radians(ang)
    for r in rs:
        pts.append([0.0, r * math.cos(th), 0.0, r * math.sin(th)])
pts = np.array(pts)


def scan(beta, h=0.05):
    shell.beta_warp = beta
    def g(t, x, y, z):
        return np.moveaxis(shell.metric_cartesian(t, x, y, z), [-2, -1], [0, 1])
    st = NumericSpacetime(g, h=h)
    return st.scan_energy_conditions(pts)


res = {}
for b in (0.0, 0.02, 0.04):
    s = scan(b)
    res[b] = s
    print(f"beta = {b}: points {s['points']}, NEC/WEC/SEC/DEC violations {s['violations']}, types {s['types']}, "
          f"worst nec_min {s['worst']['nec_min']}, min Eulerian rho {s['worst']['rho_eulerian'][0]:.3e} m^-2, "
          f"unconverged {s['unconverged']}")
identity(str(sum(res[0.0]['violations'].values()) + sum(res[0.02]['violations'].values())), "0")
print("beta=0.04 NEC violated:", res[0.04]['violations']['nec'] > 0)
identity(str(int(res[0.04]['violations']['nec'] > 0)), "1")
quantity(f"{-res[0.04]['worst']['nec_min'][0]}", "7.9e-5", rel_tol=0.15)

lo, hi = 0.02, 0.04
for _ in range(9):
    mid = 0.5 * (lo + hi)
    if scan(mid)['violations']['nec'] > 0:
        hi = mid
    else:
        lo = mid
print(f"first NEC failure on our lines: beta in [{lo:.5f}, {hi:.5f}] (claim 0.0246)")
quantity(f"{0.5*(lo+hi)}", "0.0246", rel_tol=0.05)
print("h = 0.025 m recheck at beta =", round(hi, 5), ":", scan(hi, h=0.025)['violations'],
      "; at", round(lo, 5), ":", scan(lo, h=0.025)['violations'])
raise SystemExit(finish())

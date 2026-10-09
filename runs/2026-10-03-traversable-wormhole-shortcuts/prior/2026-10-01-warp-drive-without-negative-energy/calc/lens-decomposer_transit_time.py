"""Decomposer lens: does the 2024 warp shell's interior shift ever beat light through
undisturbed (flat) space?  A one-way travel-time test along the shift axis.

Metric: Fuchs et al. 2024 shell as rebuilt by the run's warp_shell.py tool (shell frame =
exterior asymptotic rest frame, Schwarzschild exterior). Coordinates (ct, x, y, z) in metres.
Null ray along the x axis through the centre, y = z = 0.  Null condition:
    -e2a (c dt)^2 + 2 g0x (c dt) dx + e2b dx^2 = 0
=> c dt/|dx| = (s*g0x + sqrt(g0x^2 + e2a*e2b)) / e2a,  s = sign(dx).
Excess time relative to flat space: dT = (1/c) * int (c dt/|dx| - 1) |dx|.
Negative dT would be a time advance relative to light in undisturbed (flat) space between
points at rest in the exterior, the brief's travel-time sense.

Caveats (stated in output):
 - shell-frame Schwarzschild time is the asymptotic rest-frame time; far-field Shapiro delay
   grows like ln D, so D is printed;
 - this tests one straight path through the centre, not the fastest path (Gao-Wald);
 - warp_shell.py's smoothing span is a parameter it chose, not the paper's.
SI units throughout; times printed in ns.
"""
import math
import sys
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import warp_shell as ws  # noqa: E402

C = 299792458.0
G = 6.67430e-11
MJ = 1.898e27


def transit(shell, D, n_in=40001, n_out=40001):
    """One-way excess times (+x direction, -x direction) in seconds, from x=-D to x=+D."""
    xin = np.linspace(-60.0, 60.0, n_in)
    xo = np.geomspace(60.0, D, n_out)
    x = np.unique(np.concatenate([-xo[::-1], xin, xo]))
    zeros = np.zeros_like(x)
    g = shell.metric_cartesian(0.0, x, zeros, zeros)
    e2a = -g[:, 0, 0]
    g0x = g[:, 0, 1]
    e2b = g[:, 1, 1]
    root = np.sqrt(g0x ** 2 + e2a * e2b)
    plus = (g0x + root) / e2a - 1.0   # ray moving toward +x
    minus = (-g0x + root) / e2a - 1.0  # ray moving toward -x
    return np.trapezoid(plus, x) / C, np.trapezoid(minus, x) / C


def cavity_lapse2(shell):
    g = shell.metric_cartesian(0.0, np.array([0.0]), np.array([0.0]), np.array([0.0]))
    return -g[0, 0, 0]


def main():
    print("=== Fuchs et al. 2024 shell, M = 2.365 M_J, R1 = 10 m, R2 = 20 m ===")
    M = 2.365 * MJ
    print(f"M = {M:.4e} kg; 2GM/c^2 = {2*G*M/C**2:.3f} m; 2GM/(c^2 R2) = {2*G*M/(C**2*20):.3f}")
    for beta in [0.0, 0.02, 0.04, 0.1, 0.2, 0.3, 0.4]:
        sh = ws.build_shell(M, 10.0, 20.0, beta_warp=beta)
        a2 = cavity_lapse2(sh)
        for D in [100.0, 1.0e3, 1.0e5]:
            tp, tm = transit(sh, D)
            print(f"beta_warp = {beta:4.2f}  D = {D:8.0f} m  cavity e2a = {a2:.4f}  "
                  f"excess(+x) = {tp*1e9:9.2f} ns  excess(-x) = {tm*1e9:9.2f} ns  "
                  f"(-x) - (+x) = {(tm-tp)*1e9:7.2f} ns")
    sh0 = ws.build_shell(M, 10.0, 20.0, beta_warp=0.0)
    a2 = cavity_lapse2(sh0)
    print(f"\nCavity-only advance criterion (flat cavity, lapse^2 = e2a, shift beta):"
          f" advance per metre in cavity needs beta > (1 - e2a)/2 = {(1-a2)/2:.4f}")
    # beta needed for a net advance on the full straight path at D = 1e3 m
    lo, hi = 0.0, 0.95
    sh_hi = ws.build_shell(M, 10.0, 20.0, beta_warp=hi)
    tp_hi, _ = transit(sh_hi, 1.0e3)
    print(f"At beta_warp = {hi}: excess(+x, D=1e3 m) = {tp_hi*1e9:.2f} ns")
    if tp_hi < 0:
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            tp, _ = transit(ws.build_shell(M, 10.0, 20.0, beta_warp=mid), 1.0e3)
            if tp < 0:
                hi = mid
            else:
                lo = mid
        print(f"beta_warp at which the +x straight path first shows a net advance (D=1e3 m): {hi:.4f}")
    else:
        print("No net advance on the +x straight path for beta_warp up to 0.95 (D = 1e3 m).")

    print("\n=== Linearized cross-check (weak field, thin shell at R, dust) ===")
    # Shapiro excess for a line through the centre, -D..D: (2GM/c^3) * 2[1 + ln(D/R)]
    for R, D in [(15.0, 1.0e3), (15.0, 1.0e5)]:
        dt = 2 * G * M / C ** 3 * 2 * (1 + math.log(D / R))
        print(f"R = {R} m, D = {D:.0e} m: weak-field Shapiro excess = {dt*1e9:.1f} ns")
    # shift advance across cavity+wall, one way, beta * L / c
    for beta in [0.02, 0.04]:
        for L in [20.0, 40.0]:
            print(f"beta = {beta}, L = {L} m: first-order shift saving beta*L/c = {beta*L/C*1e9:.2f} ns;"
                  f" two-way (Sagnac) difference 2*beta*L/c = {2*beta*L/C*1e9:.2f} ns")
    print(f"L_eff implied by Fuchs Table 1 (7.6 ns at 0.04c) if 7.6 ns = 2*beta*L/c: {7.6e-9*C/(2*0.04):.1f} m")
    print(f"L_eff if 7.6 ns = beta*L/c: {7.6e-9*C/0.04:.1f} m")

    print("\n=== Lower-compactness shells (same R1, R2), beta_warp = 0.04 ===")
    for frac in [0.01, 0.1, 0.5, 1.0]:
        sh = ws.build_shell(frac * M, 10.0, 20.0, beta_warp=0.04)
        tp, tm = transit(sh, 1.0e3)
        print(f"M = {frac:4.2f} x 2.365 M_J: excess(+x) = {tp*1e9:8.2f} ns  excess(-x) = {tm*1e9:8.2f} ns")


if __name__ == "__main__":
    main()

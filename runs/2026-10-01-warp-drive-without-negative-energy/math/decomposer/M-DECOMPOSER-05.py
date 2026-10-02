"""M-DECOMPOSER-05/06/07: axial null transit through the rebuilt Fuchs shell (warp_shell.py, the
run's shared metric tool; NOT the lens's script). Our own derivation of the axial null cone and
our own quadrature. Coordinates x^0 = ct, frame comoving with shell = exterior rest frame.
On the x axis (y = z = 0) the metric reduces to g00 = -A(r), g0x = -S(r) beta, gxx = e^{2b}(r).
Axis is invariant under the axial and y -> -y, z -> -z symmetries, so an axial null curve is a
null geodesic. Null condition with w = dx^0/dx:
  +x ray: w+ = [sqrt(S^2 beta^2 + A gxx) - S beta]/A ;  -x ray: w- = [sqrt(...) + S beta]/A
  w- - w+ = 2 S beta / A exactly (linear in beta, independent of D once D > R2).
One-way excess over flat light between rest points x = -D, +D:  dt = (1/c) int_{-D}^{D} (w - 1) dx.
SI units (ns). Mode chosen by MODE below / argv: 05 (published mass), 06 (light shells), 07 (thresholds)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np
from scipy.optimize import brentq
from math_checks import quantity, identity, finish
from warp_shell import build_shell
c = 2.99792458e8
MPUB = 4.49e27
_trap = getattr(np, "trapezoid", None) or np.trapz


class Axis:
    def __init__(self, M, D):
        s = build_shell(M=M, R1=10.0, R2=20.0, beta_warp=0.5)
        x_in = np.linspace(0.0, 30.0, 300001)
        x_out = np.geomspace(30.0, D, 200001)
        self.parts = []
        for xs in (x_in, x_out):
            g = s.metric_cartesian(0.0, xs, 0.0 * xs, 0.0 * xs)
            A = -g[:, 0, 0]
            gxx = g[:, 1, 1]
            S = -g[:, 0, 1] / 0.5
            self.parts.append((xs, A, gxx, S))
        self.A0 = float(self.parts[0][1][0])
        self.D = D

    def excess(self, beta, sign=+1):
        tot = 0.0
        for xs, A, gxx, S in self.parts:
            root = np.sqrt((S * beta) ** 2 + A * gxx)
            w = (root - sign * S * beta) / A
            tot += 2 * _trap(w - 1.0, xs)      # even integrand: [-D,0] equals [0,D]
        return tot / c * 1e9                    # ns


def run(mode):
    if mode == "05":
        ax = Axis(MPUB, 1e3)
        print(f"cavity A = e^(2a) = {ax.A0:.4f} (tool rebuild, smoothed)")
        claims = {0.0: 240.0, 0.02: 236.6, 0.04: 233.3, 0.40: 187.2, 0.95: 150.8}
        for b, v in claims.items():
            e = ax.excess(b)
            print(f"beta = {b}: +x excess = {e:.2f} ns (claim {v})")
            quantity(f"{e} ns", f"{v} ns", rel_tol=0.01)
        for b, v in ((0.02, 6.86), (0.04, 13.72)):
            d = ax.excess(b, -1) - ax.excess(b, +1)
            print(f"beta = {b}: co/counter difference = {d:.3f} ns (claim {v})")
            quantity(f"{d} ns", f"{v} ns", rel_tol=0.01)
        for D in (1e2, 1e5):
            a2 = Axis(MPUB, D)
            d = a2.excess(0.02, -1) - a2.excess(0.02, +1)
            print(f"D = {D:.0e} m: difference at beta=0.02 = {d:.3f} ns; +x excess beta=0 {a2.excess(0.0):.1f} ns")
            quantity(f"{d} ns", "6.86 ns", rel_tol=0.01)
        b76 = 0.02 * 7.6 / (ax.excess(0.02, -1) - ax.excess(0.02, +1))
        print(f"beta needed for 7.6 ns difference = {b76:.4f}")
        quantity(f"{b76}", "0.022", rel_tol=0.02)
    elif mode == "06":
        for f, v in ((0.01, -1.87), (0.1, 16.9)):
            ax = Axis(f * MPUB, 1e3)
            e = ax.excess(0.04)
            print(f"M = {f} x published, beta = 0.04: +x excess = {e:.3f} ns (claim {v}); cavity A = {ax.A0:.5f}")
            quantity(f"{e} ns", f"{v} ns", rel_tol=0.03)
    elif mode == "07":
        claims = {0.001: 2.1e-3, 0.01: 0.021, 0.1: 0.225, 0.5: None, 1.0: None}
        for f, v in claims.items():
            ax = Axis(f * MPUB, 1e3)
            e95 = ax.excess(0.95)
            if e95 > 0:
                print(f"M = {f} x: no advance up to beta = 0.95 (excess {e95:.1f} ns); claim {v}")
                if v is None:
                    identity("1", "1")
                else:
                    quantity("1", "0")
                continue
            bt = brentq(ax.excess, 0.0, 0.95, xtol=1e-7)
            print(f"M = {f} x: first advance at beta = {bt:.5f} (claim {v}); cavity A = {ax.A0:.5f}, local (1-A)/2 = {(1-ax.A0)/2:.5f}")
            quantity(f"{bt}", f"{v}", rel_tol=0.05)


if __name__ == "__main__":
    run("05")
    raise SystemExit(finish())

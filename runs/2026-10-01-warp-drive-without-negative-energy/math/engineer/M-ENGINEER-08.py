"""M-ENGINEER-08 (F13): interior static lapse 0.761 (re-derived in M-ENGINEER-02) => crew clocks run at
0.761 of asymptotic static clocks in the shell frame: 24% less ageing, 0.761 x 109.25 yr = 83 yr on the
coast. Le's radiative steering m_i/m_f = exp(3L) with L = 2 artanh(v) (lens's reading): 1.27 at 0.04c,
against the photon rocket's (1+v)/(1-v) = exp(L) = 1.083. Identity: exp(3L) = [(1+v)/(1-v)]^3."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, quantity, finish

v = sp.symbols("v", positive=True)
L = 2 * sp.atanh(v)
identity(sp.exp(3 * L), ((1 + v) / (1 - v))**3, domain={"v": (0.001, 0.99)})
limit(sp.exp(3 * L), "v", 0, "1")
near("crew time on 109.25 yr coast (yr)", 0.7612 * 4.37 / 0.04, 83, 0.5)
near("ageing saving", 1 - 0.7612, 0.24, 0.005)
le = math.exp(3 * 2 * math.atanh(0.04))
near("Le exp(3L) at 0.04c", le, 1.27, 0.005)
inequality(repr(le), ">", repr(1.04 / 0.96))
gam = 1 / math.sqrt(1 - 0.04**2)
print(f"  kinematic gamma at 0.04c = {gam:.6f} (extra 0.08% saving relative to exterior-frame clocks; negligible)")
quantity("0.7612 * 109.25 yr", "83.2 yr", rel_tol=2e-3)
raise SystemExit(finish())

"""M-EXAMINER-05: Fell-Heisenberg static interior with N = 1 and shift magnitude 1.26.

Geometric units, lengths in metres (FH length unit ASSUMED 1 m, as the lens states).
ds^2 = -N^2 dt^2 + (dx + beta dt)^2 + dy^2 + dz^2 with N = 1, |beta| = 1.26 taken UNIFORM over the
12 m interior diameter (the lens's model; the real profile peaks at the centre).
Claims: g_tt = -N^2 + beta^2 > 0 (d/dt spacelike); a ray along the shift crosses at coordinate speed
N + |beta| = 2.26 and gains L(1 - 1/2.26) = 6.69 m = 22.3 ns on flat-space light over L = 12 m.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, quantity, units, finish

w, bb, L = sp.symbols("w b L", positive=True)
Nl = sp.Symbol("Nl", positive=True)
gtt = -Nl**2 + bb**2
sign(gtt.subs({Nl: 1, bb: sp.Rational(126, 100)}), "positive")
speeds = sp.solve(sp.Eq((w - bb)**2, Nl**2), w)     # shift oriented along +x: dx/dt = b +/- N
print("axial null speeds:", speeds)
fwd = max(speeds, key=lambda e: e.subs({Nl: 1, bb: 1}))
identity(fwd, Nl + bb)
gain = L - L/fwd                                     # flat light needs time L; ray needs L/(N+b)
identity(gain.subs(Nl, 1), L*bb/(1 + bb))
limit(gain.subs(Nl, 1), "b", 0, "0")
val = float(gain.subs({Nl: 1, bb: 1.26, L: 12}))
print(f"gain = {val:.4f} m")
ok = abs(val - 6.69) < 0.01
print(("PASS" if ok else "FAIL") + f" FH local advance {val:.4f} m vs claimed 6.69 m")
quantity("6.690 m / c", "22.3 ns", rel_tol=2e-3)
units("6.69 m / c", "time")
raise SystemExit(finish())

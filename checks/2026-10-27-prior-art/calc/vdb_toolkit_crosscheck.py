"""Light cross-check of the curvature radius with the toolkit (gr_tensors.Spacetime.curvature_at),
independent of the hand derivation in vdb_qi_recompute.py. Region II after x' = x - v t is
ds^2 = -dt^2 + B(r)^2 (dx^2+dy^2+dz^2); lengths in units of Dt (Rt = Dt = 1), so r_c = Dt/k."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime

T, X, Y, Z = sp.symbols("t x y z", real=True)
rr = sp.symbols("rr", positive=True)
B = sp.Function("B")
rad = sp.sqrt(X**2 + Y**2 + Z**2)
st = Spacetime(sp.diag(-1, B(rad)**2, B(rad)**2, B(rad)**2), [T, X, Y, Z])
n = 80
for alpha, w in (("1e34", 0.348), ("1e17", 0.57417)):
    wr = 2 - rr
    prof = sp.Lambda(rr, sp.Float(alpha, 40) * (-(n - 1) * wr**n + n * wr**(n - 1)) + 1)
    pt = (0.0, 2.0 - w, 0.0, 0.0)
    cur = st.curvature_at(pt, functions={B: prof})
    rho = st.evaluate(st.energy_density(), pt, functions={B: prof}, precision=50)
    print(f"alpha={alpha}, w={w}: toolkit max orthonormal |R| = {cur['max_frame_component']:.6g} /Dt^2,"
          f" r_c = Dt/{1/cur['curvature_radius']:.5g}; Eulerian rho = {rho:.6g} /Dt^2")

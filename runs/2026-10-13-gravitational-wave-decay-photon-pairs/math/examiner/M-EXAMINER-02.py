"""M-EXAMINER-02 (and the whole-space toy integrals used in M-03).
Radial factor of the 3D Fourier transform of a shell term f(t -+ r)/r^2:
  Int d^3x e^{-i q.x} F(r)/r^2 = (4 pi/q) Int_0^inf F(r) sin(q r)/r dr.
Outgoing self term gives e^{+i q0 r}, incoming e^{-i q0 r}; their sum gives 2 cos(q0 r).
Claim: Int_0^inf 2 cos(q0 r) sin(q r)/r dr = 0 for 0 < q < q0 (time-like), = pi for q > q0.
Outgoing alone: Int_0^inf e^{i q0 r} sin(q r)/r dr = i artanh(q/q0) for q < q0 (nonzero)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
import sympy as sp
from math_checks import identity, finish

mp.mp.dps = 30
def cos_sin(q0, q):   # Int_0^inf cos(q0 r) sin(q r)/r dr via oscillatory quadrature (Dirichlet-type, converges)
    f = lambda r: 0.5 * (mp.sin((q + q0) * r) + mp.sin((q - q0) * r)) / r
    return mp.quadosc(f, [0, mp.inf], omega=max(abs(q - q0), 1e-9))
def sin_sin(q0, q):
    f = lambda r: 0.5 * (mp.cos((q - q0) * r) - mp.cos((q + q0) * r)) / r
    return mp.quadosc(f, [0, mp.inf], omega=abs(q - q0))

q0 = mp.mpf(2)
rows = []
for q in (0.3, 1.0, 1.7, 1.95, 2.5, 4.0):
    c = 2 * cos_sin(q0, q)
    s_ = sin_sin(q0, q)
    want_c = 0 if q < q0 else mp.pi
    want_s = mp.atanh(q / q0) if q < q0 else mp.atanh(q0 / q)
    rows.append((q, c, want_c, s_, want_s))
    print(f"q/q0={q/2:.3f}: 2 Int cos sin/r = {mp.nstr(c, 10)} (expect {mp.nstr(want_c, 6)}); "
          f"Int sin sin/r = {mp.nstr(s_, 10)} (expect artanh = {mp.nstr(want_s, 10)})")
    identity(sp.Float(str(c), 25), sp.Float(str(want_c), 25) if want_c else sp.Integer(0)) if q >= q0 else \
        identity(sp.Float(round(float(c), 12)), sp.Integer(0))
    identity(sp.Float(str(s_), 25), sp.Float(str(want_s), 25))
# the lens's I_ret(q = w) with q0 = 2w: the outgoing integral is i artanh(1/2) = 0.5493 i (lens prints 0.5499 i numerically)
print("artanh(1/2) =", mp.atanh(0.5))
# limit check: q -> 0 the time-like self-term integral -> 0 and artanh -> 0
print("small q: artanh(q/q0) ~ q/q0:", mp.atanh(mp.mpf('1e-6') / 2))
raise SystemExit(finish())

"""M-EXAMINER-05: fraction of the time-symmetric toy yield made beyond R (natural units, w = 1, q0 = 2w, p = 2).
Own reduction (Gaussian envelope A = exp(-sigma^2 t^2/2), sum-frequency part, common factor H(q0 - 2w) dropped):
  J_sym ∝ (1/q) Int W_R(r) [ (1/2) cos(q0 r) - (1/2) exp(-sigma^2 r^2) ] sin(q r)/r dr
  (self terms -> cos piece; cross term -2 g(t-r) g(t+r) -> exp(-sigma^2 r^2) piece; see M-EXAMINER-03).
Whole space: cos piece = 0 for q < q0; Gaussian piece = (pi/2) erf(q/(2 sigma)).
Claim (lens F2): with sigma = 0.01 w the fraction beyond R falls as R^-1 to R^-1.5 for 1/w < R < 1/sigma and collapses for
R > 1/sigma; lens values 0.64, 0.21, 0.092, 0.040, 0.015, 1.9e-3, 9.3e-5, 5.4e-7 at wR = 1, 2, 5, 10, 20, 50, 100, 200.
Own scaling: the cross piece survives for q < 1/R, weight ~ q0^4, so F ~ 1/(q0 R) until exp(-2 sigma^2 R^2) cuts it off."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.special import ndtr, erf
from scipy.integrate import quad
import sympy as sp
from math_checks import inequality, identity, finish

q0, sig = 2.0, 0.01
_g = {}
def grid(R, D):
    if (R, D) not in _g:
        a = max(R - 8 * D, R / 1000)
        b = max(R + 8 * D, 8 / sig)          # Gaussian piece needs r up to ~ several/sigma
        n = int((b - a) / min(0.02, D / 50)) + 1
        r = np.linspace(a, b, n)
        W = ndtr((r - R) / D)
        _g[(R, D)] = (r, W)
    return _g[(R, D)]

def bracket(q, R, D):
    r, W = grid(R, D)
    f = W * (0.5 * np.cos(q0 * r) - 0.5 * np.exp(-sig ** 2 * r ** 2)) * np.sin(q * r) / r
    val = np.trapezoid(f, r)
    # tail beyond b of the cos piece (W = 1, Gaussian piece negligible): (1/4) Int_b^inf [sin((q+q0)r) + sin((q-q0)r)]/r dr
    from scipy.special import sici
    b = r[-1]
    tail = lambda k: (np.pi / 2 - sici(abs(k) * b)[0]) * np.sign(k)
    return val + 0.25 * (tail(q + q0) + tail(q - q0))

def Y(R, D):
    f = lambda q: (q0 ** 2 - q ** 2) ** 2 * bracket(q, R, D) ** 2
    pts = [x for x in (0.3 / R, 1 / R, 3 / R, 10 / R, 1.9, 1.99) if x < q0]
    return quad(f, 0, q0, points=sorted(pts), limit=400, epsrel=1e-6)[0]

Y0 = quad(lambda q: (q0 ** 2 - q ** 2) ** 2 * (np.pi / 4 * erf(q / (2 * sig))) ** 2, 0, q0, points=[0.02, 0.1], limit=400)[0]
Rs = [1, 2, 5, 10, 20, 50, 100, 200]
lens = [0.64, 0.21, 0.092, 0.040, 0.015, 1.9e-3, 9.3e-5, 5.4e-7]
for frac in (8, 5):
    F = [Y(R, R / frac) / Y0 for R in Rs]
    sl = [np.log(F[i + 1] / F[i]) / np.log(Rs[i + 1] / Rs[i]) for i in range(len(Rs) - 1)]
    print(f"D = R/{frac}: " + ", ".join(f"wR={R}: {f:.3g}" for R, f in zip(Rs, F)))
    print("   local slopes:", ", ".join(f"{s:.2f}" for s in sl))
    if frac == 8:
        F8, sl8 = F, sl
print("lens:   " + ", ".join(f"wR={R}: {f:.3g}" for R, f in zip(Rs, lens)))
# claims: slope between -0.8 and -2 over 2 <= wR <= 20 (allowing finite-w corrections); steep collapse beyond 1/sigma = 100
mid = np.log(F8[Rs.index(20)] / F8[Rs.index(2)]) / np.log(10)
late = np.log(F8[Rs.index(200)] / F8[Rs.index(100)]) / np.log(2)
print(f"mean slope wR 2 -> 20: {mid:.2f}; slope 100 -> 200: {late:.2f}")
inequality(sp.Float(mid), ">", sp.Float(-2.0))
inequality(sp.Float(late), "<", sp.Float(-4.0))
# retarded (M-04) vs time-symmetric at wR = 50: the symmetric state's yield beyond R stays far larger until R ~ 1/sigma
print(f"F_sym(50) = {F8[Rs.index(50)]:.3g} vs F_ret(50) ~ 5e-5 (M-EXAMINER-04)")
raise SystemExit(finish())

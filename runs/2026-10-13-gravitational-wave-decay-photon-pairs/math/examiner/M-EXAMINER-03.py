"""M-EXAMINER-03: whole-space yield of the retarded vs time-symmetric toy field (natural units, c = 1).
Toy: phi_ret = g(t-r)/r, phi_sym = [g(t-r) - g(t+r)]/r, g = A(t) cos(w t), A a slow envelope (width 1/sigma << ... ),
source j = phi^2; yield Y = Int d^4q theta(q0) theta(q^2) (q^2)^p |J(q)|^2 (massless pair: 2-body phase space constant).
Own derivation (narrow band, sum-frequency q0 ~ 2w part; common factor H(q0 - 2w) = FT of A^2 cancels in ratios):
  J_ret(q0, q) = (4 pi/q) H (1/4) Int_0^inf e^{i q0 r} sin(q r)/r dr = (4 pi/q) H (i/4) artanh(q/q0)
  J_sym(q0, q) = (4 pi/q) H [ (1/2) Int cos(q0 r) sin(qr)/r dr  -  (1/2) Int a(r) sin(qr)/r dr ],
  where the first term is 0 for q < q0 (M-EXAMINER-02) and the cross-term envelope a(r) -> 1 on scales << 1/sigma, so
  for q >> sigma the bracket -> -(1/2)(pi/2) = -pi/4.
  d^3q = 4 pi q^2 dq cancels the 1/q^2, so with x = q/q0:
  ratio_p = Int_0^1 (1-x^2)^p artanh(x)^2 dx / (pi^2 Int_0^1 (1-x^2)^p dx).
Claims: ratio_0 = 1/12 exactly; ratio_2 = 0.020."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
import sympy as sp
from math_checks import identity, limit, finish

mp.mp.dps = 30
def ratio(p):
    num = mp.quad(lambda x: (1 - x ** 2) ** p * mp.atanh(x) ** 2, [0, 0.5, 0.9, 0.99, 1])
    den = mp.pi ** 2 * mp.quad(lambda x: (1 - x ** 2) ** p, [0, 1])
    return num / den
for p in (0, 1, 2, 3):
    print(f"p = {p}: retarded / time-symmetric whole-space yield = {mp.nstr(ratio(p), 12)}")
# exact p = 0: Int_0^1 artanh^2 = pi^2/12, so ratio = 1/12
x = sp.Symbol("x", positive=True)
I0 = sp.integrate(sp.atanh(x) ** 2, (x, 0, 1))
print("Int_0^1 artanh(x)^2 dx (sympy) =", sp.nsimplify(sp.N(I0, 30), [sp.pi]))
identity(sp.Float(str(ratio(0)), 25), sp.Rational(1, 12))
identity(sp.Float(str(round(float(ratio(2)), 3))), sp.Float("0.020"))
# limit: as p -> large the weight pins x -> 0 where artanh -> 0, so the ratio -> 0 (monotone decrease checked)
print("ratios decrease with p:", [mp.nstr(ratio(p), 4) for p in (0, 2, 6, 20)])
# finite-sigma check of the cross-term envelope for a Gaussian A = exp(-sigma^2 t^2/2):
# a(r) = exp(-sigma^2 r^2), Int_0^inf exp(-s^2 r^2) sin(q r)/r dr = (pi/2) erf(q/(2 s)) -> pi/2 for q >> sigma
s = mp.mpf("0.01")
num = mp.quad(lambda q: (4 - q ** 2) ** 2 * mp.atanh(q / 2) ** 2 / 16, [0, 1, 1.9, 1.99, 2])
den = mp.quad(lambda q: (4 - q ** 2) ** 2 * (mp.pi / 4 * mp.erf(q / (2 * s))) ** 2, [0, 0.05, 2])
print(f"finite sigma = 0.01 w, Gaussian envelope, p = 2: ratio = {mp.nstr(num / den, 8)}")
num0 = mp.quad(lambda q: mp.atanh(q / 2) ** 2 / 16, [0, 1, 1.9, 1.99, 2])
den0 = mp.quad(lambda q: (mp.pi / 4 * mp.erf(q / (2 * s))) ** 2, [0, 0.05, 2])
print(f"finite sigma = 0.01 w, p = 0: ratio = {mp.nstr(num0 / den0, 8)} (lens numeric 0.0842; narrow-band limit 1/12 = 0.08333)")
raise SystemExit(finish())

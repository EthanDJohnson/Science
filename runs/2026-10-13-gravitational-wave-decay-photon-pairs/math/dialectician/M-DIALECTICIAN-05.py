"""M-DIALECTICIAN-05: top-hat linear chirp, J ratio -> 3 pi/(sigma t_c) (F4).

f = sigma^(-1/2) exp(i beta x^2) on x in [-sigma/2, sigma/2]; the group delay 2 beta x spans
t_c = 2 beta sigma (the sweep duration). Route: J/(2 pi) = int |a(t)|^4 dt (Parseval, M-02),
with a(t) computed by direct quadrature (no FFT of C). Stationary phase: |a|^2 -> 1/t_c over
t_c, so int|a|^4 -> 1/t_c and J -> 2 pi/t_c; J_TL = 2 sigma/3 => ratio 3 pi/(sigma t_c).
Lens values of J/J_TL / asymptote: 0.84, 0.967, 0.993, 0.998 at sigma t_c = 10, 50, 200, 800.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import identity, quantity, finish

sig = 1.0
JTL = 2 * sig / 3
identity("(2*pi/tc)/(2*sigma/3)", "3*pi/(sigma*tc)")

def J_direct(tc):
    beta = tc / (2 * sig)
    # C(y) = int f(x) f(y - x) dx directly, y in [-sigma, sigma]
    n = 6001 if tc <= 200 else 20001
    xs = np.linspace(-sig / 2, sig / 2, n)
    dx = xs[1] - xs[0]
    f = sig ** -0.5 * np.exp(1j * beta * xs**2)
    C = np.convolve(f, f) * dx  # rectangle rule, error O(dx/sigma)
    return np.sum(np.abs(C) ** 2) * dx

lens = {10: 0.84, 50: 0.967, 200: 0.993, 800: 0.998}
J0 = J_direct(0.0)
print(f"J(0) = {J0:.6f} (expect {JTL:.6f})")
quantity(f"{J0}", f"{JTL}", rel_tol=1e-3)
for tc, lv in lens.items():
    Jc = J_direct(float(tc))
    ratio = Jc / JTL
    asym = 3 * np.pi / (sig * tc)
    print(f"sigma t_c = {tc}: J/J_TL = {ratio:.5f}, asymptote {asym:.5f}, ratio/asym = {ratio/asym:.4f} (lens {lv})")
    quantity(f"{ratio/asym}", f"{lv}", rel_tol=1.5e-2)
raise SystemExit(finish())

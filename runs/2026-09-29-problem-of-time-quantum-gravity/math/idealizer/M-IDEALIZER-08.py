"""M-IDEALIZER-08 (F8): inner-product facet. Each component obeys psi_n'' + k_n(x)^2 psi_n = 0, k_n^2 = 2M(M e(x) - E_n)
(hbar = 1, model units). Exact invariant: Wronskian current j_n = Im(psi_n^* psi_n') (the KG current), constant in x.
WKB: |psi_n|^2 = j_n/k_n, so Schrodinger populations p_n = (|c_n|^2/k_n)/sum drift as e changes:
d ln(p_n/p_0) = -(E_n/(2 M e)) d ln e + O(M^-2). Claim numbers (M = 100, E = 0,1,2.5, equal KG weights, e: 25.3 -> 74.7):
level 2: 0.3334211 -> 0.3333631, level 0: 0.3332566 -> 0.3333073.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp
from math_checks import quantity, series, identity, finish

E = np.array([0.0, 1.0, 2.5]); M = 100.0
def pops(e):
    k = np.sqrt(2 * M * (M * e - E)); w = 1 / k; return w / w.sum()
pa, pb = pops(25.3), pops(74.7)
print("pops at e=25.3", pa, " at e=74.7", pb)
quantity(f"{pa[2]}", "0.3334211", rel_tol=2e-7)
quantity(f"{pb[2]}", "0.3333631", rel_tol=2e-7)
quantity(f"{pa[0]}", "0.3332566", rel_tol=2e-7)
quantity(f"{pb[0]}", "0.3333073", rel_tol=2e-7)
# scaling: ln(p_n/p_0) = (1/2) ln(Me/(Me-E_n)) -> expand in u = 1/(M e)
u, En = sp.symbols("u E_n", positive=True)
series(sp.Rational(1, 2) * sp.log(1 / (1 - En * u)), "u", 0, 2, En * u / 2)
print("E_S/(2 M e) at mid e = 50:", 2.5 / (2 * M * 50))
quantity(f"{2.5/(2*M*50)}", "2.5e-4", rel_tol=1e-9)

# ODE: Wronskian exactly conserved, M = 3, e(x) = 50 + 20 tanh(x) (slowly varying), E = 2.5
Mo = 3.0; Eo = 2.5
e = lambda x: 50 + 20 * np.tanh(x / 3)
def rhs(x, y):
    psi = y[0] + 1j * y[1]; dpsi = y[2] + 1j * y[3]
    k2 = 2 * Mo * (Mo * e(x) - Eo)
    dd = -k2 * psi
    return [dpsi.real, dpsi.imag, dd.real, dd.imag]
x0 = -12.0; k0 = np.sqrt(2 * Mo * (Mo * e(x0) - Eo))
y0 = [1 / np.sqrt(k0), 0.0, 0.0, np.sqrt(k0)]  # WKB right-mover, j = 1
sol = solve_ivp(rhs, (x0, 12.0), y0, rtol=1e-11, atol=1e-13, dense_output=True)
xs = np.linspace(x0, 12, 7)
js, kps = [], []
for xx in xs:
    y = sol.sol(xx); psi = y[0] + 1j * y[1]; dpsi = y[2] + 1j * y[3]
    js.append(np.imag(np.conj(psi) * dpsi))
    kps.append(np.sqrt(2 * Mo * (Mo * e(xx) - Eo)) * abs(psi) ** 2)
print("Wronskian j(x):", np.round(js, 10))
print("k|psi|^2 (WKB proxy):", np.round(kps, 6))
quantity(f"{max(js)}", f"{min(js)}", rel_tol=1e-8)
quantity(f"{max(kps)}", f"{min(kps)}", rel_tol=1e-3)
raise SystemExit(finish())

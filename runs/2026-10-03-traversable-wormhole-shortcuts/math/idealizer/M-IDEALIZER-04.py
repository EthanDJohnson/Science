"""M-IDEALIZER-04: exotic mass of an Ellis throat and of a flat-space thin-shell wormhole.

Ellis (Phi = 0) in proper radial distance l: ds^2 = -dt^2 + dl^2 + (b0^2 + l^2) dOmega^2, G = c = 1.
rho = T_tt = G_tt/(8 pi) computed here from the metric (gr_tensors, Einstein tensor).
Claim: "integral of rho dV over both sheets = -b0" (times c^2/G in SI).
Two measures are computed:
  (a) mass-function measure 4 pi r^2 |dr/dl| dl  (= 4 pi r^2 dr per sheet, Morris-Thorne m(r));
  (b) proper volume 4 pi r^2 dl.
Thin shell: two copies of Schwarzschild(M) exterior r >= a glued at r = a, static.
Lanczos: S^i_j = -(1/8pi)([K^i_j] - delta^i_j [K]); K^theta_theta = sqrt(1-2M/a)/a, K^tau_tau = (M/a^2)/sqrt(1-2M/a),
jumps are twice the one-sided values (normals point away from the throat on both sides).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, limit, sign, quantity, units, finish

t, l, th, ph = sp.symbols("t l theta phi", real=True)
b0 = sp.symbols("b0", positive=True)
r2 = b0**2 + l**2
st = Spacetime(sp.diag(-1, 1, r2, r2 * sp.sin(th)**2), [t, l, th, ph])
T = st.stress_energy()
rho = sp.simplify(T[0, 0])
print("rho(l) =", rho)
identity(rho, -b0**2 / (8 * sp.pi * r2**2))
r = sp.sqrt(r2)
drdl = sp.Abs(sp.diff(r, l))
mass_fn = 2 * sp.integrate(sp.simplify(rho * 4 * sp.pi * r2 * l / r), (l, 0, sp.oo))   # both sheets, l>0 doubled
proper = sp.integrate(sp.simplify(rho * 4 * sp.pi * r2), (l, -sp.oo, sp.oo))
print("mass-function measure, both sheets:", sp.simplify(mass_fn))
print("proper-volume measure, both sheets:", sp.simplify(proper))
identity(mass_fn, -b0)
identity(proper, -sp.pi * b0 / 2)

# thin shell
a, M = sp.symbols("a M", positive=True)
Kth = sp.sqrt(1 - 2 * M / a) / a
Ktt = (M / a**2) / sp.sqrt(1 - 2 * M / a)
jth, jtt = 2 * Kth, 2 * Ktt
jK = jtt + 2 * jth
S_tt = -(jtt - jK) / (8 * sp.pi)        # S^tau_tau = -sigma
sigma = -S_tt
identity(sigma, -sp.sqrt(1 - 2 * M / a) / (2 * sp.pi * a), domain={"M": (0.01, 0.4), "a": (1, 10)})
limit(4 * sp.pi * a**2 * sigma, "M", 0, -2 * a)

# SI scale c^2/G
units("1 m * c^2 / G", "mass")
quantity("1 m * c^2 / G", "1.347e27 kg", rel_tol=1e-3)
quantity("2 m * c^2 / G", "2.69e27 kg", rel_tol=2e-3)
raise SystemExit(finish())

"""M-EXAMINER-04: thin-shell model of the 2024 shell (Fuchs et al. parameters), axial light delay.

Units: SI for the mass; lengths in metres, times as metres of light (1 m = 3.33564 ns).
Model: exterior Schwarzschild (mass M, r > R_s), thin shell at areal radius R_s, flat interior.
Continuity of g_tt across the shell (first junction condition, Schwarzschild time t):
interior ds^2 = -N^2 dt^2 + (dx + beta dt)^2 + dy^2 + dz^2 with N = sqrt(1 - 2m/R_s), m = GM/c^2.
(ADM form, the brief's convention; beta is a constant interior contravariant shift, sign chosen
to help the forward ray.) Axial null speeds inside: dx/dt = N + |beta| forward, N - |beta| backward.
Claims checked: m = 3.3342 m; N_in = 0.5772/0.7283/0.8164 at R_s = 10/14.2/20 m; unshifted interior
delay 2R_s(1/N - 1) = 14.65/10.60/8.99 m; exterior radial Shapiro excess R_s -> 100 m on both sides
= 44.4/33.6/26.0 m; forward delay with beta = 0.04: 12.4/8.6/6.7 m; advance threshold beta > 1 - N
= 0.4228/0.2717/0.1836 (10.6x/6.8x/4.6x); co-minus-counter 9.3-16.1 ns across beta and beta*N readings.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, inequality, finish

G, c = 6.67430e-11, 299792458.0
M = 4.49e27
m = G*M/c**2
print(f"GM/c^2 = {m:.5f} m")
quantity("6.67430e-11 m^3/(kg*s^2) * 4.49e27 kg / c^2", "3.3342 m", rel_tol=1e-4)
units("G * 4.49e27 kg / c^2", "length")

# Symbolic: interior null speeds in the ADM form
w, Nn, b = sp.symbols("w N_n b", positive=True)
roots = sp.solve(sp.Eq(-Nn**2 + (w - b)**2, 0), w)  # dx/dt = w with shift helping: (dx - b dt)^2 = N^2 dt^2
print("interior axial null speeds:", roots)
identity(max(roots, key=lambda e: e.subs({Nn: 0.5, b: 0.1})), Nn + b)
# Delay over a diameter 2R relative to flat light: 2R(1/(N+b) - 1); advance iff N + b > 1
Rs = sp.symbols("R_s", positive=True)
delay = 2*Rs*(1/(Nn + b) - 1)
limit(delay.subs(b, 0), "N_n", 1, "0")   # flat limit: no delay
# Co-minus-counter difference, reading (a): beta = b; reading (b): beta = b*N
diff_a = 2*Rs*(1/(Nn - b) - 1/(Nn + b))
identity(diff_a, 4*Rs*b/(Nn**2 - b**2))
diff_b = 2*Rs*(1/(Nn*(1 - b)) - 1/(Nn*(1 + b)))
identity(diff_b, 4*Rs*b/(Nn*(1 - b**2)))

# Exterior Schwarzschild radial null ray: dt/dr = 1/(1 - 2m/r); excess over flat
r, r1, r2, mm = sp.symbols("r r1 r2 m", positive=True)
exc = sp.integrate(1/(1 - 2*mm/r) - 1, (r, r1, r2), conds="none")
print("radial Shapiro excess (one side):", sp.simplify(exc))
limit(2*mm*sp.log((r2 - 2*mm)/(r1 - 2*mm)), "m", 0, "0")
# numeric equality of sympy integral with 2m ln((r2-2m)/(r1-2m)) at a sample point
val_int = float(exc.subs({mm: 3.3342, r1: 10, r2: 100}))
val_cf = 2*3.3342*math.log((100 - 2*3.3342)/(10 - 2*3.3342))
print(f"integral {val_int:.5f} vs closed form {val_cf:.5f}")

def chk(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(("PASS" if ok else "FAIL") + f" {name}: ours {got:.4f} vs claimed {want} (tol {tol})")

claims = {10.0: dict(N=0.5772, d0=14.65, sh=44.4, d4=12.4, th=0.4228, fac=10.6),
          14.2: dict(N=0.7283, d0=10.60, sh=33.6, d4=8.6, th=0.2717, fac=6.8),
          20.0: dict(N=0.8164, d0=8.99, sh=26.0, d4=6.7, th=0.1836, fac=4.6)}
ns = 1e9/c
diffs = []
for R_s, cl in claims.items():
    N = math.sqrt(1 - 2*m/R_s)
    d0 = 2*R_s*(1/N - 1)
    sh = 2 * 2*m*math.log((100 - 2*m)/(R_s - 2*m))
    d4 = 2*R_s*(1/(N + 0.04) - 1)
    th = 1 - N
    th_alt = (1 - N**2)/2     # alternative: g_tt held at -N^2, covariant g_tx = beta added
    da = 4*R_s*0.04/(N**2 - 0.04**2)*ns
    db = 4*R_s*0.04/(N*(1 - 0.04**2))*ns
    diffs += [da, db]
    print(f"R_s={R_s}: N={N:.4f} d0={d0:.3f} m ({d0*ns:.1f} ns) Shapiro(2 sides)={sh:.2f} m d(0.04)={d4:.3f} m "
          f"threshold={th:.4f} ({th/0.04:.2f}x) alt-convention threshold={th_alt:.4f} ({th_alt/0.04:.2f}x) "
          f"co-counter: beta-reading {da:.2f} ns, beta*N-reading {db:.2f} ns")
    chk(f"N_in R_s={R_s}", N, cl["N"], 6e-5)
    chk(f"unshifted delay R_s={R_s}", d0, cl["d0"], 6e-3)
    chk(f"exterior Shapiro both sides R_s={R_s}", sh, cl["sh"], 0.06)
    chk(f"forward delay beta=0.04 R_s={R_s}", d4, cl["d4"], 0.06)
    chk(f"advance threshold R_s={R_s}", th, cl["th"], 6e-5)
    chk(f"threshold factor R_s={R_s}", th/0.04, cl["fac"], 0.06)
chk("co-minus-counter range min [ns]", min(diffs), 9.3, 0.06)
chk("co-minus-counter range max [ns]", max(diffs), 16.1, 0.06)
# Robustness: the alternative shift convention threshold (1 - N^2)/2 also exceeds 0.04 at all three radii
inequality("(1 - N_n**2)/2", ">", "0.04", domain={"N_n": (0.5772, 0.8164)})
quantity("2*3.3342 m * 1", "6.6684 m")
raise SystemExit(finish())

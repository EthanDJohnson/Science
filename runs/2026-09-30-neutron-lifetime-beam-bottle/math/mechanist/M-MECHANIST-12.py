"""M-MECHANIST-12 (F14): SM tau_beta = K/(Vud^2 (1 + 3 lambda^2)).
K two independent ways:
 (a) first principles: K = 2 pi^3 hbar / (G_F^2 m_e^5 f (1 + delta_R')(1 + DeltaR^V)), f = 1.6887,
     delta_R' = 0.014902 (neutron outer correction, literature value, ASSUMED), DeltaR^V = 0.02479 (GS2023);
 (b) the GS2023 self-consistency point (D-44): tau 877.75 s, lambda 1.27641 -> Vud 0.97404.
Vud = 0.97361(32) (GS2024 superallowed, D-43). lambda: PERKEO III 1.27641(56); PDG 1.2754(13); aSPECT 2024 1.2668(27).
Br_X = 1 - tau_bottle/tau_beta, tau_bottle = 877.82 +- 0.287 s. Beam 887.97 +- 2.04 s. s (SI)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

GF = 1.1663788e-5; me = 0.51099895e-3; hbar = 6.582119569e-25   # GeV^-2, GeV, GeV s
Ka = 2 * math.pi**3 * hbar / (GF**2 * me**5 * 1.6887 * 1.014902 * 1.02479)
Kb = 877.75 * 0.97404**2 * (1 + 3 * 1.27641**2)
print(f"K first principles = {Ka:.2f} s; K from GS2023 point = {Kb:.2f} s")
units("6.582119569e-25 GeV*s / (1.1663788e-5 GeV^-2)^2 / (0.51099895e-3 GeV)^5", "s")
quantity(f"{Ka} s", f"{Kb} s", rel_tol=5e-4)
K, sK = Kb, 0.19
V, sV = 0.97361, 0.00032
lam, Vs, Ks = sp.symbols("lambda V K", positive=True)
tb = Ks / (Vs**2 * (1 + 3 * lam**2))
identity(sp.diff(tb, lam), -6 * lam * tb / (1 + 3 * lam**2))
identity(sp.diff(tb, Vs), -2 * tb / Vs)
limit(tb, "lambda", 0, Ks / Vs**2)
ucn, su = 877.82, math.hypot(0.22, 0.185)
beam, sb = 887.97, 2.04
out = {}
for name, l, sl, claim in (("PERKEO III", 1.27641, math.hypot(0.00045, 0.00033), (878.50, 0.88)),
                           ("PDG 2024", 1.2754, 0.0013, (879.65, 1.61)),
                           ("aSPECT 2024", 1.2668, 0.0027, (889.58, 3.20))):
    t = K / (V**2 * (1 + 3 * l**2))
    st = t * math.sqrt((6 * l * sl / (1 + 3 * l**2)) ** 2 + (2 * sV / V) ** 2 + (sK / K) ** 2)
    br = 1 - ucn / t
    sbr = (ucn / t) * math.hypot(st / t, su / ucn)
    ul = br + 1.6448536 * sbr
    zb = (beam - t) / math.hypot(sb, st)
    out[name] = (t, st, br, sbr, ul, zb)
    print(f"{name}: tau_beta = {t:.2f} +- {st:.2f} s (lens {claim}); Br_X = {br*100:.3f} +- {sbr*100:.3f} %, "
          f"95% UL {ul*100:.2f} %; beam above by {zb:.2f} sigma; with K_a: {Ka/(V**2*(1+3*l**2)):.2f} s")
    quantity(f"{t} s", f"{claim[0]} s", rel_tol=1e-4)
    quantity(f"{st} s", f"{claim[1]} s", rel_tol=0.02)
t, st, br, sbr, ul, zb = out["PERKEO III"]
quantity(f"{br}", "0.00077", rel_tol=0.1); quantity(f"{sbr}", "0.00106", rel_tol=0.02)
quantity(f"{ul}", "0.0025", rel_tol=0.03); quantity(f"{zb}", "4.3", rel_tol=0.02)
t, st, br, sbr, ul, zb = out["PDG 2024"]
quantity(f"{br}", "0.0021", rel_tol=0.1); quantity(f"{ul}", "0.0051", rel_tol=0.05); quantity(f"{zb}", "3.2", rel_tol=0.02)
t, st, br, sbr, ul, zb = out["aSPECT 2024"]
quantity(f"{br}", "0.0132", rel_tol=0.01); quantity(f"{sbr}", "0.0036", rel_tol=0.03)
raise SystemExit(finish())

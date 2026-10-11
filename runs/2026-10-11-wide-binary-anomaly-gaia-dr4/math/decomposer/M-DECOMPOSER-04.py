"""M-DECOMPOSER-04 and -05: independent noise-free Kepler Monte Carlo for pure binaries.

Model (built here from Kepler's laws, not the run's generator): units G M = a = 1 (Kepler orbits
are self-similar, so the v~ distribution does not depend on a or M). e ~ f(e) propto e^alpha on
[0, 0.999]; mean anomaly uniform; isotropic orientation (uniform random rotation via a unit
quaternion). s = sky-projected separation, v_p = sky-projected relative speed,
v~ = v_p / sqrt(gam G M / s) * sqrt(gam) = v_p_true / sqrt(G M / s) where MOND is approximated as
Keplerian with G -> gam G (velocities scale by sqrt(gam) at fixed positions).

M-04 claims (lens calc C, TEST bin, DR3 noise, HTZ template): gamma_app = (med v~_truth /
med v~_template)^2 = 0.935 (truth alpha = 2), 1.063 (thermal), 1.305 (uniform); CAL: 0.865, 0.997,
1.246; differentials 1.080 / 1.067 / 1.048.  HTZ alpha in the TEST bin (s ~ 5-17 kau for 1-2 Msun
at 10^-10.5..10^-9.5 m/s^2; log10 a ~ 3.7-4.25) is ~1.17-1.32; in the CAL bin (0.2-1.7 kau)
~0.8-1.3.  Here: template alpha_T in {1.2, 1.25, 1.3} (TEST) and alpha_C in {0.95, 1.05, 1.15} (CAL).
M-05 claims (calc D): P(v~ > sqrt2) for pure MOND binaries with mean gam 1.291 / 1.266 = 0.0125 /
0.0108; truncating at sqrt2 lowers the median by 0.9%; v~ <= sqrt(2 gam) always.
Self-tests: v~ <= sqrt2 (Newton), <r> = a(1 + <e^2>/2), <sin theta> = pi/4, energy.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish

rng = np.random.default_rng(20261011)
N = 2_000_000

def kepler_E(M, e):
    E = M + e * np.sin(M)
    E = np.where(e > 0.8, np.pi * np.ones_like(M), E)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def quat_rot(n):
    q = rng.standard_normal((n, 4)); q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    R = np.empty((n, 3, 3))
    R[:, 0] = np.stack([1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)], 1)
    R[:, 1] = np.stack([2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)], 1)
    R[:, 2] = np.stack([2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)], 1)
    return R

def sample(alpha, n=N):
    e = np.minimum(rng.random(n) ** (1.0 / (alpha + 1.0)), 0.999)
    M = rng.uniform(0, 2 * np.pi, n)
    E = kepler_E(M, e)
    sq = np.sqrt(1 - e * e)
    pos = np.stack([np.cos(E) - e, sq * np.sin(E), np.zeros(n)], 1)
    den = 1 - e * np.cos(E)
    vel = np.stack([-np.sin(E) / den, sq * np.cos(E) / den, np.zeros(n)], 1)
    R = quat_rot(n)
    P = np.einsum("nij,nj->ni", R, pos); V = np.einsum("nij,nj->ni", R, vel)
    r = np.linalg.norm(pos, axis=1); v = np.linalg.norm(vel, axis=1)
    s = np.hypot(P[:, 0], P[:, 1]); vp = np.hypot(V[:, 0], V[:, 1])
    return dict(e=e, r=r, v=v, s=s, vt=vp / np.sqrt(1.0 / s), sin_theta=s / r)

# ---- self tests (thermal) ----
d = sample(1.0)
quantity(f"{np.max(d['vt']) / np.sqrt(2)}", "1.0", rel_tol=0.02)          # v~ max approaches sqrt2
inequality(f"{np.max(d['vt'])}", "<=", f"{np.sqrt(2) * (1 + 1e-9)}")
quantity(f"{np.mean(d['r'])}", f"{1 + np.mean(d['e'] ** 2) / 2}", rel_tol=2e-3)
quantity(f"{np.mean(d['sin_theta'])}", f"{np.pi / 4}", rel_tol=2e-3)
quantity(f"{np.max(np.abs(d['v'] ** 2 / 2 - 1 / d['r'] + 0.5))}", "0", rel_tol=1e-6) if False else None
inequality(f"{np.max(np.abs(d['v'] ** 2 / 2 - 1 / d['r'] + 0.5))}", "<", "1e-9")  # vis-viva, a = GM = 1

med = {}
for al in (0.0, 0.95, 1.0, 1.05, 1.15, 1.2, 1.25, 1.3, 2.0):
    med[al] = np.median(sample(al)["vt"])
    print(f"alpha={al}: median v~ = {med[al]:.4f}")

print("\nM-04: gamma_app = (med_truth/med_template)^2")
tab = {}
for name, al in (("alpha2", 2.0), ("thermal", 1.0), ("uniform", 0.0)):
    T = [(med[al] / med[aT]) ** 2 for aT in (1.2, 1.25, 1.3)]
    C = [(med[al] / med[aC]) ** 2 for aC in (0.95, 1.05, 1.15)]
    D = [t / c for t in T for c in C]
    tab[name] = (T, C, D)
    print(f"{name}: TEST {min(T):.3f}-{max(T):.3f}; CAL {min(C):.3f}-{max(C):.3f}; diff {min(D):.3f}-{max(D):.3f}")
# lens TEST values must lie within ~0.02 of the noise-free span (noise dilutes shifts slightly)
for name, lensT, lensC in (("alpha2", 0.935, 0.865), ("thermal", 1.063, 0.997), ("uniform", 1.305, 1.246)):
    T, C, D = tab[name]
    inequality(f"{lensT}", ">=", f"{min(T) - 0.02}"); inequality(f"{lensT}", "<=", f"{max(T) + 0.02}")
    inequality(f"{lensC}", ">=", f"{min(C) - 0.03}"); inequality(f"{lensC}", "<=", f"{max(C) + 0.03}")
# lever size claim: differential |ln| <= ln 1.08-ish for alpha in [0, 2]
for name in tab:
    inequality(f"{max(abs(np.log(x)) for x in tab[name][2])}", "<", f"{np.log(1.10)}")

print("\nM-05: truncation at sqrt2, HTZ-like alpha = 1.25")
base = sample(1.25)
for gam, claim in ((1.291, 0.0125), (1.266, 0.0108)):
    vt = base["vt"] * np.sqrt(gam)
    frac = np.mean(vt > np.sqrt(2))
    m_all = np.median(vt); m_cut = np.median(vt[vt <= np.sqrt(2)])
    print(f"gam={gam}: P(v~>sqrt2) = {frac:.4f}; median {m_all:.4f} -> {m_cut:.4f} ({(m_cut/m_all-1)*100:.2f}%); max/sqrt(2gam) = {vt.max()/np.sqrt(2*gam):.4f}")
    quantity(f"{frac}", f"{claim}", rel_tol=0.35)
    inequality(f"{vt.max()}", "<=", f"{np.sqrt(2 * gam) * (1 + 1e-9)}")
    inequality(f"{abs(m_cut / m_all - 1)}", "<", "0.012")
    if gam == 1.291:
        quantity(f"{m_cut / m_all - 1}", "-0.009", rel_tol=0.35)
quantity(f"{np.mean(base['vt'] > np.sqrt(2))}", "0", rel_tol=1e-9) if False else inequality(f"{np.mean(base['vt'] > np.sqrt(2))}", "==", "0") if False else None
inequality(f"{np.mean(base['vt'] > np.sqrt(2) * (1 + 1e-9))}", "<=", "0")
raise SystemExit(finish())

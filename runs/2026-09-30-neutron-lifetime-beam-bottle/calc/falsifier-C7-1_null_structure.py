"""Falsifier C7-1 (evidence angle): does the data allow a gap 'spread over several experiments, none dominant'?
All lifetimes in s (SI). Inputs: D-20, D-22, D-23, D-27..D-30 as transcribed in math/statistician/_inputs.py.
Parts:
 (1) Where the gap sits: per-experiment chi^2 contributions about the common mean; minimum-norm allocation of
     the proton-vs-storage gap between BL1 and UCNtau.
 (2) The null's own listed shifts (candidates.md C7 'Shift by class'): BL1 +3..+6 s, J-PARC +-several s,
     material +2 s, magnetic 0. What each does to the proton-vs-storage gap.
 (3) Diffuse-inflation null: Gaussian errors all inflated by k (k^2 = chi2/dof of all 11). Probability of the
     observed concentration (4-class between chi2 >= obs AND within <= obs), by Monte Carlo.
 (4) Heavy-tail null (Student-t, unit scale, nu = 2,3,4, independent per experiment): same joint probability,
     plus P(proton-vs-rest z >= 4.70) and where the maximum pull lands.
"""
import math, sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from _inputs import BL1, SUS, MATERIAL, MAGNETIC, JPARC, wmean, q

rows = [BL1, SUS] + MATERIAL + MAGNETIC + [JPARC]
cls = ["P", "P"] + ["M"] * len(MATERIAL) + ["G"] * len(MAGNETIC) + ["J"]
x = np.array([r[1] for r in rows]); s = np.array([r[2] for r in rows]); names = [r[0] for r in rows]

print("=== (1) Where the chi^2 sits (common mean of all 11) ===")
w = 1 / s**2; m = np.sum(w * x) / np.sum(w)
chi = w * (x - m) ** 2
print(f"common mean {m:.3f} s, total chi2 {chi.sum():.2f}/10")
for n, xi, si, c in zip(names, x, s, chi):
    print(f"  {n:18s} {xi:7.2f} +- {si:4.2f}  pull {((xi-m)/si):+5.2f}  chi2 share {c/chi.sum():5.1%}")
# min-norm allocation of the BL1-UCNtau difference: minimise (d1/s1)^2+(d2/s2)^2 s.t. d1 - d2 = Delta
b = BL1; u = MAGNETIC[0]
D = b[1] - u[1]
share_b = b[2]**2 / (b[2]**2 + u[2]**2)
print(f"BL1 - UCNtau = {D:.2f} s; least-squares allocation puts {share_b:.1%} ({share_b*D:.2f} s) on BL1, "
      f"{1-share_b:.1%} ({(1-share_b)*D:.2f} s) on UCNtau")
print(f"  i.e. BL1 pull {share_b*D/b[2]:.2f} sigma, UCNtau pull {(1-share_b)*D/u[2]:.2f} sigma")
# if UCNtau carried half of the gap:
print(f"  if UCNtau carried half the gap ({D/2:.2f} s): UCNtau pull {D/2/u[2]:.1f} sigma vs BL1 {D/2/b[2]:.1f} sigma")

print("\n=== (2) The null's own listed shifts applied as corrections ===")
def gap(xarr):
    p = [(xarr[i], s[i]) for i in range(len(xarr)) if cls[i] == "P"]
    st = [(xarr[i], s[i]) for i in range(len(xarr)) if cls[i] in "MG"]
    mp_ = wmean([("", a, e) for a, e in p]); ms = wmean([("", a, e) for a, e in st])
    sig_s = ms[1] * ms[4]
    d = mp_[0] - ms[0]; sd = math.hypot(mp_[1], sig_s)
    return d, sd, d / sd, ms[4]
d0 = gap(x)
print(f"baseline proton - storage: {d0[0]:.2f} +- {d0[1]:.2f} s = {d0[2]:.2f} sigma (storage S {d0[3]:.2f})")
for label, dBL1, dmat, dJ in [("BL1 -3, material -2", 3, 2, 0), ("BL1 -6, material -2", 6, 2, 0),
                              ("J-PARC +-5 only", 0, 0, 5), ("material -2 only", 0, 2, 0),
                              ("BL1 -3 only", 3, 0, 0), ("BL1 -6 only", 6, 0, 0)]:
    xc = x.copy()
    xc[0] -= dBL1
    for i, c in enumerate(cls):
        if c == "M": xc[i] -= dmat
        if c == "J": xc[i] += dJ
    d = gap(xc)
    print(f"  {label:22s}: gap {d[0]:6.2f} +- {d[1]:.2f} s = {d[2]:.2f} sigma  (change {d[0]-d0[0]:+.2f} s)")

def partition_chi2(xarr, sarr, labels):
    wv = 1 / sarr**2; mm = np.sum(wv * xarr, axis=-1, keepdims=True) / np.sum(wv)
    within = 0.0; between = 0.0
    for c in sorted(set(labels)):
        idx = [i for i, l in enumerate(labels) if l == c]
        wc = wv[idx]; xc = xarr[..., idx]
        mc = np.sum(wc * xc, axis=-1, keepdims=True) / np.sum(wc)
        within = within + np.sum(wc * (xc - mc) ** 2, axis=-1)
        between = between + np.sum(wc) * (mc[..., 0] - mm[..., 0]) ** 2
    return within, between

def prot_rest_z(xarr, sarr):
    P = [0, 1]; R = [i for i in range(len(sarr)) if i not in P]
    wv = 1 / sarr**2
    mP = np.sum(wv[P] * xarr[..., P], axis=-1) / wv[P].sum(); mR = np.sum(wv[R] * xarr[..., R], axis=-1) / wv[R].sum()
    return (mP - mR) / math.sqrt(1 / wv[P].sum() + 1 / wv[R].sum())

_wv = 1 / s**2
_P = [0, 1]; _R = [i for i in range(len(s)) if i not in _P]
GAPC = np.array([(_wv[i] / _wv[_P].sum()) if i in _P else (-_wv[i] / _wv[_R].sum()) for i in range(len(s))])
def mP_minus_mR(y):
    return np.sum(GAPC * y, axis=-1)
_yobs = x - np.sum(_wv[_R] * x[_R]) / _wv[_R].sum()
_t = GAPC * _yobs
print("observed proton-rest gap decomposition (s), rest mean as zero:")
for n, ti in zip(names, _t):
    print(f"  {n:18s} {ti:+7.3f}")
print(f"  total {mP_minus_mR(_yobs):.3f} s; largest single term {names[int(np.argmax(_t))]} = {_t.max()/mP_minus_mR(_yobs):.1%}")
W_obs, B_obs = partition_chi2(x, s, cls)
z_obs = prot_rest_z(x, s)
print(f"\nobserved 4-class within {W_obs:.2f}/7, between {B_obs:.2f}/3; proton-vs-rest z {z_obs:.2f}")

print("\n=== (3) Diffuse-inflation null: all sigmas x k, Gaussian ===")
k = math.sqrt(chi.sum() / 10)
print(f"k = {k:.3f}")
rng = np.random.default_rng(12345)
N = 2_000_000
def mc(draw, label):
    y = draw(N) * s  # deviations in s, true value 0
    Wt, Bt = partition_chi2(y, s, cls)
    zt = prot_rest_z(y, s)
    joint = np.mean((Bt >= B_obs) & (Wt <= W_obs))
    pb = np.mean(Bt >= B_obs); pw = np.mean(Wt <= W_obs)
    pz = np.mean(zt >= z_obs)
    # where is the largest |pull|?
    pulls = np.abs(y / s)
    imax = np.argmax(pulls, axis=1)
    frac_bl1 = np.mean(imax == 0)
    # given z>=z_obs, fraction of cases where one experiment's squared pull exceeds half of total chi2 about common mean
    wv = 1 / s**2
    mm = np.sum(wv * y, axis=1, keepdims=True) / wv.sum()
    c2 = wv * (y - mm) ** 2
    dom = (c2.max(axis=1) / c2.sum(axis=1)) >= 0.5
    sel = zt >= z_obs
    pdom = np.mean(dom[sel]) if sel.sum() > 0 else float('nan')
    # gap decomposition: gap = sum_i c_i y_i with c_i = +w_i/W_P (proton) or -w_i/W_R (rest)
    terms = GAPC * y
    gshare = terms.max(axis=1) / (mP_minus_mR(y))
    pg = np.mean(gshare[sel] >= 0.5) if sel.sum() > 0 else float('nan')
    print(f"   {label}: P(one experiment supplies >=50% of the proton-rest gap | z>=obs) = {pg:.2f}")
    print(f"{label}: P(between>=obs)={pb:.2e}  P(within<=obs)={pw:.3f}  P(joint)={joint:.2e}  "
          f"P(z_proton-rest>=obs, one-sided)={pz:.2e}  n(z>=obs)={sel.sum()}  "
          f"P(one experiment carries >=50% of chi2 | z>=obs)={pdom:.2f}")
mc(lambda n: k * rng.standard_normal((n, len(s))), f"Gaussian x{k:.2f}")

print("\n=== (4) Heavy-tail null: Student-t, unit scale, independent per experiment ===")
for nu in (2, 3, 4):
    mc(lambda n, nu=nu: rng.standard_t(nu, (n, len(s))), f"Student-t nu={nu}")
print("\nObserved: share of chi2 carried by the single largest contributor:",
      f"{chi.max()/chi.sum():.1%} ({names[int(np.argmax(chi))]})")

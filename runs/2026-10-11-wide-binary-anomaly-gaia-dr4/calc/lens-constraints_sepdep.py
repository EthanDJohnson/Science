#!/usr/bin/env python3
"""Constraints lens: separation-dependent systematics that survive high-acceleration calibration.

1. Hidden inner binaries: kick kappa = (Gaia-baseline-averaged, sky-projected photocentre
   velocity)/v_c(s) as a function of wide separation s, for a log-normal inner period
   distribution (Raghavan et al. 2010: peak ~300 yr; width sigma_logP an ASSUMPTION, varied),
   q_in ~ U(0.1,1), L ~ m^3.5, circular inner orbits, stability a_in < f_stab * r_wide.
   Crude detectability proxies (ASSUMPTIONS, labelled): RUWE-like flag if P_in < T and the
   photocentre semi-amplitude > 0.1 mas; acceleration flag if P_in > T and the photocentre
   deviation from linear motion over T, a_acc T^2/8, exceeds thr_acc (0.05 mas DR3-like,
   epoch precision held fixed; DR4 gains through T^2).
   Then the full-median and truncated-median gamma for f_multi = 0.3 at each s, with the mass
   underestimate included, before and after removing flagged systems.
2. Measurement noise sigma_v~(s, d, G) for DR3 and DR4 (ESA DR4 model in D-51; DR3 = DR4/0.42),
   and the implied full-median bias with a noise-free template.
3. Galactic tide vs internal acceleration (Oort constants and local density are ASSUMED inputs).
SI units; au, pc, km/s for printing.
"""
import numpy as np

G = 6.67430e-11; MSUN = 1.3271244e20 / G; AU = 1.495978707e11; PC = 3.0856775814913673e16
YR = 365.25 * 86400.0; DAY = 86400.0
M_W = 1.5 * MSUN; M1 = 0.75 * MSUN          # wide pair total; mass of the component hosting the inner pair
D = 150 * PC
rng = np.random.default_rng(23)

# --- base Newtonian v~ population (alpha = 1.3), same construction as lens-constraints_vtilde.py
def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(50):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def iso(n):
    v = rng.normal(size=(n, 3)); return v / np.linalg.norm(v, axis=1)[:, None]

def base_pop(n, alpha=1.3):
    e = rng.uniform(0, 1, n) ** (1 / (alpha + 1)) * 0.999
    E = kepler_E(rng.uniform(0, 2 * np.pi, n), e)
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e * e) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / den, np.sqrt(1 - e * e) * np.cos(E) / den, np.zeros(n)], 1)
    # random rotation via two isotropic vectors (Gram-Schmidt)
    a = iso(n); b = iso(n); b -= (a * b).sum(1)[:, None] * a; b /= np.linalg.norm(b, axis=1)[:, None]
    c = np.cross(a, b)
    R = np.stack([a, b, c], 2)
    p = np.einsum("nij,nj->ni", R, pos); v = np.einsum("nij,nj->ni", R, vel)
    s = np.hypot(p[:, 0], p[:, 1]); r = np.linalg.norm(p, axis=1)
    return v[:, :2] * np.sqrt(s)[:, None], s ** 0.6, s / r   # v~ vec, weight, s/r

def wq(x, w, q):
    i = np.argsort(x); cw = np.cumsum(w[i]); cw /= cw[-1]; return np.interp(q, cw, x[i])

N = 300_000
vt, w, s_over_r = base_pop(N)
m0 = wq(np.hypot(vt[:, 0], vt[:, 1]), w, 0.5)
print("base median v~ (alpha=1.3) = %.4f" % m0)

def inner_kicks(n, s_au, T_yr, sig_logP=2.3, mu_logP=np.log10(300 * 365.25), f_stab=0.2,
                thr_ruwe_mas=0.1, thr_acc_mas=0.05, d=D):
    """kappa vectors (sky 2D, units of v_c(s)), mass ratio M_true/M_est, flags."""
    q = rng.uniform(0.1, 1.0, n)
    m_in = M1 * (1 + q)
    r_w = s_au * AU / np.clip(s_over_r[:n], 0.05, 1)      # wide 3D separation for these pairs
    a_max = f_stab * r_w
    # log-normal P truncated by stability: draw P, convert to a, redraw if a > a_max (simple rejection)
    P = 10 ** rng.normal(mu_logP, sig_logP, n) * DAY
    a_in = (G * m_in * P ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    for _ in range(30):
        bad = (a_in > a_max) | (a_in < 0.02 * AU)
        if not bad.any():
            break
        P[bad] = 10 ** rng.normal(mu_logP, sig_logP, bad.sum()) * DAY
        a_in[bad] = (G * m_in[bad] * P[bad] ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    bad = (a_in > a_max) | (a_in < 0.02 * AU)
    a_in[bad] = np.clip(a_in[bad], 0.02 * AU, a_max[bad]); P = 2 * np.pi * np.sqrt(a_in ** 3 / (G * m_in))
    l = q ** 3.5
    beta = np.abs(q / (1 + q) - l / (1 + l))               # photocentre factor (Belokurov+20 eq. 4 form)
    v_in = np.sqrt(G * m_in / a_in)
    T = T_yr * YR
    x = np.pi * T / P
    avg = np.abs(np.sinc(x / np.pi))                        # mean velocity over T of a circular orbit
    # photocentre velocity vector: random direction in the inner orbital plane, then sky-projected
    nrm = iso(n); u = iso(n); u -= (nrm * u).sum(1)[:, None] * nrm; u /= np.linalg.norm(u, axis=1)[:, None]
    dv = (beta * v_in * avg)[:, None] * u
    vc = np.sqrt(G * M_W / (s_au * AU))
    kap = dv[:, :2] / vc
    # flags
    amp_mas = beta * a_in / d / AU * 1000.0 * (AU / PC) * 1.0   # semi-amplitude in mas: (beta a_in[au]) / d[pc] arcsec
    amp_mas = beta * (a_in / AU) / (d / PC) * 1000.0
    ruwe_flag = (P < T) & (amp_mas > thr_ruwe_mas)
    acc = beta * v_in ** 2 / a_in                             # photocentre acceleration (m/s^2)
    dev_mas = acc * T ** 2 / 8 / d * 206264.806 * 1000.0      # deviation from linear motion, mas
    acc_flag = (P >= T) & (dev_mas > thr_acc_mas)
    mu = (M1 * (1 + q) + (M_W - M1)) / (M1 * (1 + q ** 3.5) ** (1 / 3.5) + (M_W - M1))
    return kap, mu, ruwe_flag, acc_flag, P

print()
print("=== 1. Inner-binary kicks vs wide separation (f_multi = 0.3, d = 150 pc, M_wide = 1.5 Msun) ===")
F_MULTI = 0.3
for sig_logP in [2.3, 1.5]:
    print("-- sigma_logP = %.1f dex (assumed); P peak 300 yr (Raghavan+10)" % sig_logP)
    for s_au in [500, 1000, 2000, 5000, 10000, 20000]:
        out = {}
        for rel, T_yr, thr in [("DR3", 34 / 12, 0.05), ("DR4", 66 / 12, 0.05)]:
            kap, mu, rf, af, P = inner_kicks(N, s_au, T_yr, sig_logP=sig_logP, thr_acc_mas=thr)
            k = np.hypot(kap[:, 0], kap[:, 1])
            is_t = rng.uniform(size=N) < F_MULTI
            vo = vt.copy()
            vo[is_t] += kap[is_t]
            vo[is_t] *= np.sqrt(mu[is_t])[:, None]
            vm = np.hypot(vo[:, 0], vo[:, 1])
            g_full = (wq(vm, w, 0.5) / m0) ** 2
            sel = vm < np.sqrt(2)
            g_tr = (wq(vm[sel], w[sel], 0.5) / m0) ** 2
            keep_r = ~(is_t & rf)
            vr_ = vm[keep_r]; wr_ = w[keep_r]
            g_full_r = (wq(vr_, wr_, 0.5) / m0) ** 2
            selr = vr_ < np.sqrt(2)
            g_tr_r = (wq(vr_[selr], wr_[selr], 0.5) / m0) ** 2
            keep = ~(is_t & (rf | af))
            vk = vm[keep]; wk = w[keep]
            g_full_k = (wq(vk, wk, 0.5) / m0) ** 2
            selk = vk < np.sqrt(2)
            g_tr_k = (wq(vk[selk], wk[selk], 0.5) / m0) ** 2
            out[rel] = (np.mean(k > 0.3), np.mean(k > 1.0), np.mean(rf), np.mean(af), g_full, g_tr, g_full_k, g_tr_k,
                        np.mean((k > 0.3) & ~(rf | af)), g_full_r, g_tr_r)
        d3, d4 = out["DR3"], out["DR4"]
        print("             RUWE-only removal: DR3 full %.3f trunc %.3f | DR4 full %.3f trunc %.3f" % (d3[9], d3[10], d4[9], d4[10]))
        print("  s=%5d au: P(kappa>0.3)=%.3f P(kappa>1)=%.3f | DR3 flags ruwe %.3f acc %.3f; DR4 flags ruwe %.3f acc %.3f"
              % (s_au, d3[0], d3[1], d3[2], d3[3], d4[2], d4[3]))
        print("             gamma (all triples kept): full %.3f trunc %.3f | after DR3 flags: full %.3f trunc %.3f | after DR4 flags: full %.3f trunc %.3f | unflagged kappa>0.3 frac DR3 %.3f DR4 %.3f"
              % (d3[4], d3[5], d3[6], d3[7], d4[6], d4[7], d3[8], d4[8]))

print()
print("=== 2. Measurement noise sigma_v~ per axis (M = 1.5 Msun) ===")
# ESA DR4 predicted parallax errors (uas), D-51; sigma_mu(DR4) = 0.54 sigma_plx; DR3 = DR4 / 0.42
G_mag = {13: 10, 15: 22, 17: 59, 19: 211}
sig_grid = np.array([0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6])
nz = rng.normal(size=(N, 2))
gb = []
for sg in sig_grid:
    vm = np.hypot(vt[:, 0] + sg * nz[:, 0], vt[:, 1] + sg * nz[:, 1])
    gb.append((wq(vm, w, 0.5) / m0) ** 2)
gb = np.array(gb)
print("  bias table sigma -> gamma: " + ", ".join("%.2f->%.3f" % (a, b) for a, b in zip(sig_grid, gb)))
for Gm, splx in G_mag.items():
    smu4 = 0.54 * splx * 1e-3      # mas/yr per star
    smu3 = smu4 / 0.42
    for d_pc in [100, 200, 300]:
        row = []
        for s_au in [2000, 5000, 10000, 20000]:
            vc = np.sqrt(G * M_W / (s_au * AU)) / 1e3   # km/s
            sv3 = 4.740470 * d_pc / 1e3 * np.sqrt(2) * smu3 / vc
            sv4 = 4.740470 * d_pc / 1e3 * np.sqrt(2) * smu4 / vc
            row.append("s=%dk: %.3f/%.3f (bias %.3f/%.3f)" % (s_au // 1000, sv3, sv4, np.interp(sv3, sig_grid, gb), np.interp(sv4, sig_grid, gb)))
        print("  G=%d d=%dpc sigma_mu DR3 %.4f DR4 %.4f mas/yr | sigma_v~ DR3/DR4: %s" % (Gm, d_pc, smu3, smu4, "; ".join(row)))

print()
print("=== 3. Galactic tide (ASSUMED inputs: Oort A = 15.3, B = -11.9 km/s/kpc; rho0 = 0.1 Msun/pc^3) ===")
kms_kpc = 1e3 / (1e3 * PC)
A = 15.3 * kms_kpc; B = -11.9 * kms_kpc
rho0 = 0.1 * MSUN / PC ** 3
rJ = (G * M_W / (4 * A * (A - B))) ** (1 / 3)
print("  Jacobi radius (1.5 Msun) r_J = %.0f au = %.2f pc" % (rJ / AU, rJ / PC))
for s_au in [5000, 10000, 30000]:
    r = s_au * AU
    gN = G * M_W / r ** 2
    t_in = 4 * A * (A - B) * r; t_z = 4 * np.pi * G * rho0 * r
    print("  r = %d au: g_N = %.3e m/s^2, in-plane tide %.3e (ratio %.2e), vertical tide %.3e (ratio %.2e)"
          % (s_au, gN, t_in, t_in / gN, t_z, t_z / gN))

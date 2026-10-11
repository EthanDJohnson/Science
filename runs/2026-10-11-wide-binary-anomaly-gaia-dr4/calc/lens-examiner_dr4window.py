"""Examiner lens, premise 11 ("DR4 settles it"): which hidden inner binaries perturb the wide-pair
proper-motion velocity by >= v_c(s), and which of those can DR3/DR4 flag?

Order-of-magnitude model (stated approximations, not a population synthesis):
- inner pair M_in = 1.2 Msun (0.8 + 0.4, q = 0.5), photocentre factor f_ph = 0.27 (dossier D-40);
- photocentre speed v_ph = f_ph * sqrt(G M_in / a_in) (circular inner orbit);
- velocity-relevant if v_ph >= v_c(s) of the wide pair (M_wide = 1.5 Msun) and P_in >= baseline T
  (shorter periods average out of the proper motion and show up as RUWE / orbit solutions instead);
- acceleration-detectable if photocentre acceleration f_ph*G M_in/a_in^2 / d >= 5 sigma_g,
  sigma_g = sqrt(60) sigma_mu / T (uniform sampling, quadratic fit);
- resolvable if a_in / d >= 0.5 arcsec (rough Gaia pair resolution at moderate contrast);
- a_in distribution log-uniform (Opik) for the fraction estimate (Moe & Di Stefano log-normal would differ).
Units: au, yr, pc, km/s, mas.
"""
import numpy as np

AU_KMS = 4.74047          # 1 au/yr in km/s
GM_SUN = 4 * np.pi ** 2   # au^3/yr^2
f_ph, M_in, M_wide = 0.27, 1.2, 1.5

def v_c_kms(s_au):
    return np.sqrt(GM_SUN * M_wide / s_au) * AU_KMS

def v_ph_kms(a):
    return f_ph * np.sqrt(GM_SUN * M_in / a) * AU_KMS

# sigma_mu [mas/yr] per star: DR4 from D-51 (sigma_mu = 0.54 sigma_plx); DR3 ~ D-14 medians (0.02-0.03 at G 9-14)
cases = {
    "DR3 G~13": dict(T=34 / 12, smu=0.025),
    "DR3 G~17": dict(T=34 / 12, smu=0.10),
    "DR4 G~13": dict(T=66 / 12, smu=0.54 * 0.010),
    "DR4 G~17": dict(T=66 / 12, smu=0.54 * 0.059),
}
for s in (3000, 10000, 20000):
    vc = v_c_kms(s)
    a_max_v = M_in * (f_ph * np.sqrt(GM_SUN) * AU_KMS / vc) ** 2      # v_ph = v_c
    a_stab = 0.3 * s * 1.2 * (1 - 0.6)                                   # ~0.3 a_out (1 - e), a_out ~ 1.2 s, e ~ 0.6
    print(f"\n--- s = {s} au: v_c = {vc:.3f} km/s; v_ph >= v_c for a_in <= {a_max_v:.0f} au; stability a_in <~ {a_stab:.0f} au")
    for name, c in cases.items():
        T = c["T"]
        a_lo = (T ** 2 * M_in) ** (1 / 3)                                # P_in = T
        for d in (100, 200):
            sg = np.sqrt(60) * c["smu"] / T                                # mas/yr^2
            # accel [mas/yr^2] = f_ph * GM_in / a^2 [au/yr^2] * (1000/d) [mas/au]
            a_acc = np.sqrt(f_ph * GM_SUN * M_in * 1000 / d / (5 * sg))
            a_res = 0.5 * d                                               # 0.5 arcsec in au
            a_hi = min(a_max_v, a_stab)
            lo_hidden = max(a_lo, a_acc)
            hi_hidden = min(a_hi, a_res)
            frac = max(0.0, np.log(hi_hidden / lo_hidden)) / np.log(a_hi / a_lo) if a_hi > a_lo else 0.0
            print(f"{name:9s} d={d:3d} pc: P=T at a={a_lo:.1f} au; 5sig accel to a={a_acc:.0f} au; resolved beyond {a_res:.0f} au;"
                  f" hidden velocity-relevant window [{lo_hidden:.0f}, {hi_hidden:.0f}] au -> log-uniform fraction {frac:.2f}")

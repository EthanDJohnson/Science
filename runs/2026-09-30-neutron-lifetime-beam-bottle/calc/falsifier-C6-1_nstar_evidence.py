"""Falsifier C6-1 (evidence angle): n* (Koch-Hummel) hypothesis checks.
Units: SI (lifetimes and times in s). Dimensionless fractions.

1. Composition-averaged lifetime of a beam mixture, tau_n = -n/ndot (Koch-Hummel eq. 6),
   solved exactly for the n*/n ratio needed, compared with their eq. (10)/(19).
2. C6's prediction for J-PARC (electron-counting cold beam, normalised by 3He capture in
   the same volume) if n* survives J-PARC's flight, against the observed 877.2 s.
3. The tau_gamma window needed for BL1 long AND J-PARC short, given flight-time differences.
"""
import math

tau_g = 878.32           # s, all-storage mean (candidates.md reference)
dtau_ref = 9.65          # s, proton-beam minus storage (reference gap)
dtau_bl1 = 9.88          # s, BL1 minus UCNtau
tau_bl1 = 887.7          # s, BL1 (Yue 2013)
sig_bl1 = math.hypot(1.2, 1.9)

print("== 1. n* abundance needed (rate-averaged, exact) vs Koch-Hummel eq.10 ==")
for label, dtau in [("reference gap", dtau_ref), ("BL1-UCNtau", dtau_bl1)]:
    for dte_label, dtau_e in [("16/9 tau_g (KH eq.19 state)", 16 * tau_g / 9), ("tau_e -> inf", None)]:
        if dtau_e is None:
            # tau_e -> infinity: 1/(tau_g+dtau) = ng/(ng+ne)/tau_g  -> ne/(ng+ne) = dtau/(tau_g+dtau)
            f = dtau / (tau_g + dtau)
            x = f / (1 - f)
            print(f"{label}: {dte_label}: exact ne/ng = {x:.4e}, ne/(ne+ng) = {f:.4e}")
            continue
        tau_e = tau_g + dtau_e
        x_exact = (tau_e / tau_g) * dtau / (dtau_e - dtau)
        x_kh = dtau / (dtau_e - dtau)
        # verify by forward computation
        ng, ne = 1.0, x_exact
        tau_mix = (ng + ne) / (ng / tau_g + ne / tau_e)
        print(f"{label}: {dte_label}: tau_e = {tau_e:.1f} s; exact ne/ng = {x_exact:.4e}; "
              f"KH eq.10 ne/ng = {x_kh:.4e}; ratio exact/KH = {x_exact/x_kh:.3f}; "
              f"check tau_mix(exact) - tau_g = {tau_mix - tau_g:.3f} s")
        ne = x_kh
        tau_mix_kh = (ng + ne) / (ng / tau_g + ne / tau_e)
        print(f"    forward check: KH abundance gives tau_mix - tau_g = {tau_mix_kh - tau_g:.3f} s "
              f"(target {dtau} s)")

print()
print("== 2. C6 prediction for J-PARC if n* survives its flight (tau_gamma >> t_J) ==")
tau_J, stat_J, sysp_J, sysm_J = 877.2, 1.7, 4.0, 3.6   # s, Fuwa 2024 (preprint)
S_J = 2.29                                               # J-PARC internal scale factor [M-STATISTICIAN-05]
for pred_label, pred in [("storage + reference gap", tau_g + dtau_ref), ("BL1 value", tau_bl1)]:
    # prediction is above J-PARC, so use the upper systematic of J-PARC
    sJ = math.hypot(stat_J, sysp_J)
    z_meas_only = (pred - tau_J) / sJ
    z_scaled = (pred - tau_J) / (sJ * S_J)
    print(f"pred ({pred_label}) = {pred:.2f} s; J-PARC obs = {tau_J} s; diff = {pred - tau_J:.2f} s; "
          f"sigma_J = {sJ:.2f} s -> {z_meas_only:.2f} sigma; with S = {S_J}: {z_scaled:.2f} sigma")
    if pred_label == "BL1 value":
        s2 = math.hypot(sJ, sig_bl1)
        print(f"   (J-PARC vs BL1 direct, sigma = {s2:.2f} s: {(pred - tau_J)/s2:.2f} sigma)")

print()
print("== 3. tau_gamma window for BL1 long and J-PARC short simultaneously ==")
print("Model: beam shift dtau(t) ~ dtau0 * exp(-t/tau_gamma) (small-f limit).")
print("Require BL1 shift = 9.88 s and J-PARC shift <= X s; X = 4.35 s (1 sigma_J above storage).")
X = 4.35
need_ratio = X / dtau_bl1
need_dt_over_tg = -math.log(need_ratio)
print(f"needed survival ratio J/BL1 <= {need_ratio:.3f}  ->  (t_J - t_B)/tau_gamma >= {need_dt_over_tg:.3f}")
for dt_ms in [0, 5, 10, 20, 50, 100]:
    dt = dt_ms * 1e-3
    tg_max = dt / need_dt_over_tg if dt > 0 else 0.0
    print(f"  t_J - t_B = {dt_ms:4d} ms -> tau_gamma <= {tg_max*1e3:7.2f} ms "
          f"(KH window lower edge t_beam ~ 20 ms; Blatnik upper edge 139 s)")
print("If J-PARC neutrons are not older than BL1's (t_J <= t_B), no tau_gamma > 0 works: J-PARC")
print("would read at least as long as BL1.")
print()
print("== 4. Flight times since production: BL1 (NIST NG-6) vs J-PARC (BL05 TPC) ==")
h_over_m = 6.62607015e-34 / 1.67492750e-27   # m^2/s, h/m_n
kB = 1.380649e-23; mn = 1.67492750e-27
L_B = 68.0     # m, cold source to NG-6 end station (Nico 2005: "approximately 68 m")
T_B = 40.0     # K, effective temperature of the emerging cold spectrum (Nico 2005)
v_mp = math.sqrt(2 * kB * T_B / mn)
v_mean = math.sqrt(8 * kB * T_B / (math.pi * mn))
print(f"BL1: L = {L_B} m; 40 K Maxwellian v_mp = {v_mp:.0f} m/s, <v> = {v_mean:.0f} m/s")
for v in [400, v_mp, v_mean, 1500, 2000]:
    print(f"   v = {v:6.0f} m/s -> t_B = {L_B / v * 1e3:6.1f} ms")
L_J = 19.3     # m, moderator to upstream face of TPC (Sato/SFC paper Table III), TPC 1 m long
for lam_nm in [0.32, 0.55, 0.78]:
    v = h_over_m / (lam_nm * 1e-9)
    print(f"J-PARC: lambda = {lam_nm} nm -> v = {v:.0f} m/s -> t_J = {L_J / v * 1e3:.1f}"
          f"-{(L_J + 1.0) / v * 1e3:.1f} ms (TPC entry to exit)")
print("BL1 needs 68 m; J-PARC needs 19.3-20.3 m: for equal speeds t_J/t_B = "
      f"{L_J/L_B:.2f}-{(L_J+1)/L_B:.2f}. J-PARC neutrons are younger; exp(-t/tau_gamma) is larger,")
print("so under n* J-PARC's rate-averaged lifetime is >= BL1's for every tau_gamma.")
# the extremes: slowest J-PARC (0.78 nm) vs fastest plausible BL1 (2000 m/s)
v_slowJ = h_over_m / 0.78e-9
print(f"Extreme case: slowest J-PARC t_J = {(L_J+1)/v_slowJ*1e3:.1f} ms vs BL1 at 2000 m/s t_B = {L_B/2000*1e3:.1f} ms")

print()
print("Width of the surviving window (KH lower edge 2e-2 s to Blatnik 139 s): "
      f"{math.log10(139/2e-2):.2f} decades in tau_gamma")

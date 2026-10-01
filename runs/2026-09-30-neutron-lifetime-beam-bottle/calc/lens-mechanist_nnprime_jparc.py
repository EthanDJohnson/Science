"""Mechanist lens: (A) n -> n' (SPECULATIVE, Berezhiani strong-field model) conversion in the field
profiles of a proton-trap beam, J-PARC, material bottles and magnetic traps, against the SNS regeneration
limit; (B) J-PARC per-condition pressure trend. SI units unless stated (neV for energies in printouts).

Inputs: Berezhiani worked example dm = 280 neV, theta0 = 1e-3, B = 4.6 T [D-89]; SNS regeneration
p < 2.5e-8 (95% CL) [D-62]; J-PARC Table II per-condition values [D-24]; target shift 1.143 %
(lens-mechanist_required_sizes.py). Cold-beam velocity grid and UCN collision rates are ASSUMED.
"""
import math, sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import nn_mirror_osc as nn

NEV = nn.NEV
target = 1.01143
v_grid = np.array([400., 600., 800., 1000., 1200., 1500., 2000.])   # m/s, ASSUMED cold spectrum
flux = v_grid**3*np.exp(-(v_grid/800.)**2)                            # ASSUMED Maxwellian-like flux
w = flux/v_grid                                                       # density weighting (tool doc)

print("[A1] Proton-trap beam, Berezhiani geometry (0.6 m solenoid, 4.6 T), velocity-averaged")
for dm_nev in (200., 260., 280., 300.):
    for th in (1e-4, 3e-4, 1e-3):
        r = nn.beam_solenoid(dm_nev*NEV, theta0=th, B_center=4.6, v=v_grid, weights=w)
        print(f"  dm={dm_nev:.0f} neV theta0={th:.0e}: B_res={r['B_res_T']:.2f} T  P_trap={r['P_trap']:.3e} "
              f"P_det={r['P_det']:.3e}  tau_beam/tau_beta={r['tau_beam_over_tau_beta']:.5f}  "
              f"(shift {(r['tau_beam_over_tau_beta']-1)*877.8:+.2f} s)")

# theta0 needed for the target shift at dm = 280 neV (bisection on log theta0)
def shift(th, dm=280.):
    return nn.beam_solenoid(dm*NEV, theta0=th, B_center=4.6, v=v_grid, weights=w)
lo, hi = 1e-5, 3e-2
for _ in range(50):
    mid = math.sqrt(lo*hi)
    if shift(mid)["tau_beam_over_tau_beta"] < target: lo = mid
    else: hi = mid
r = shift(hi)
print(f"  theta0 needed for +1.143% at dm=280 neV: {hi:.3e}; P_trap={r['P_trap']:.3e}, P_det={r['P_det']:.3e}, tau_nn'={r['tau_nn_s']:.3e} s")
Pneed = r["P_trap"]

print("\n[A2] SNS regeneration test (P1*P2, same model, ASSUMING each passage converts about as much as the trap)")
print(f"  predicted regeneration ~ P^2 = {Pneed**2:.2e} vs limit 2.5e-8 -> ratio {Pneed**2/2.5e-8:.1e}")
Pmax = math.sqrt(2.5e-8)
print(f"  max per-passage P allowed = {Pmax:.2e} -> max beam shift ~ {Pmax*100:.4f} % = {Pmax*877.8:.2f} s")

print("\n[A3] Other measurement classes in the same model (theta0 above, dm = 280 neV)")
th = hi; dm = 280.*NEV; eps = nn.eps_from_theta0(th, dm)
# J-PARC: ~0 T (and LiNA 0.6 T): time-averaged mixing, no loss mechanism in a beam -> counts decays of n only;
for B in (0.0, 0.6):
    avgP = np.mean([nn.rabi_time_average(eps, nn.detuning(dm, B, s)) for s in (+1, -1)])
    print(f"  J-PARC-type beam at {B} T: time-averaged P = {avgP:.2e} -> shift {avgP*877.8:.4f} s")
# material bottle: each wall bounce projects; loss per bounce <P>, rate = <P> * collision rate (ASSUMED)
for B in (0.0, 1e-6):
    avgP = np.mean([nn.rabi_time_average(eps, nn.detuning(dm, B, s)) for s in (+1, -1)])
    for nu in (5., 50.):
        rate = avgP*nu
        print(f"  material bottle B={B} T, {nu:.0f} bounces/s: loss/bounce={avgP:.2e}, rate={rate:.2e} s^-1, "
              f"apparent tau={nn.apparent_lifetime(878.0, rate):.2f} s (before size extrapolation)")
# magnetic trap: fields up to ~1-2 T never reach B_res = 4.64 T -> no resonance crossings; mixing stays ~2 theta^2
print(f"  magnetic trap (B < B_res = {nn.resonance_field(dm):.2f} T): no resonance crossing; no projecting walls -> loss ~0 in this model")

print("\n[B] J-PARC per-condition values (stat only, and stat (+) mean of the two unlabelled columns)")
cond = {"100/old": (870.9, 3.5, (1.8+2.8)/2, (5.5+4.9)/2), "100/new": (868.3, 4.0, (1.5+2.9)/2, (3.8+3.2)/2),
        "50/old": (868.2, 7.7, (2.7+0.9)/2, (4.8+3.9)/2), "50/new": (884.8, 2.4, (0.8+1.3)/2, (3.2+3.0)/2)}
def wm(items):
    ws = [1/s**2 for _, s in items]; m = sum(v*x for (v, _), x in zip(items, ws))/sum(ws)
    return m, math.sqrt(1/sum(ws))
for label, use in (("stat only", lambda c: c[1]), ("stat+sys(approx)", lambda c: math.sqrt(c[1]**2+c[2]**2+c[3]**2))):
    p100 = wm([(cond[k][0], use(cond[k])) for k in ("100/old", "100/new")])
    p50 = wm([(cond[k][0], use(cond[k])) for k in ("50/old", "50/new")])
    old = wm([(cond[k][0], use(cond[k])) for k in ("100/old", "50/old")])
    new = wm([(cond[k][0], use(cond[k])) for k in ("100/new", "50/new")])
    # linear model tau(P) = tau0 + k*P  through the two pressure means; extrapolate to P = 0
    k = (p100[0]-p50[0])/50.0; tau0 = p50[0] - k*50.0
    s_tau0 = math.sqrt((2*p50[1])**2 + p100[1]**2)
    print(f"  {label}: 100 kPa {p100[0]:.1f}+-{p100[1]:.1f}; 50 kPa {p50[0]:.1f}+-{p50[1]:.1f}; diff {p50[0]-p100[0]:.1f}+-{math.hypot(p50[1],p100[1]):.1f} s "
          f"({(p50[0]-p100[0])/math.hypot(p50[1],p100[1]):.1f} sigma)")
    print(f"     linear extrapolation to 0 kPa: {tau0:.1f} +- {s_tau0:.1f} s (ASSUMES bias proportional to pressure)")
    print(f"     old SFC {old[0]:.1f}+-{old[1]:.1f}; new SFC {new[0]:.1f}+-{new[1]:.1f}")
# J-PARC vs the two sides (symmetrised errors)
sj = math.hypot(1.7, 4.0)   # upper error toward the beam
print(f"\n  J-PARC 877.2 vs 887.97 (beam): {(887.97-877.2)/math.hypot(sj, 2.04):.2f} sigma; vs UCNtau 877.82: {(877.82-877.2)/math.hypot(math.hypot(1.7,3.6),0.29):.2f} sigma")

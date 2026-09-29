"""Falsifier C6-0: is the causal obstacle 'binding, not quantitative'?

Geometric units G = c = 1, lengths in m; 1 m of mass = 1.3466e27 kg.
Alcubierre metric ds^2 = -dt^2 + (dx - v f dt)^2 + dy^2 + dz^2.
Eulerian density rho = -(v^2/32pi) (y^2+z^2)/r^2 f'(r)^2  (Alcubierre 1994).

Computes:
 1. share of Eulerian E_- in f < 1 - 1/v (outside the comoving-timelike zone), vs v,
    for tanh (sigma from PF Delta=1 m), linear ramp and Bobrick-Martire optimal f=min(R/r,1);
    split into front (x>0) and rear (x<0) halves.
 2. causal reach from the ship centre: integrate forward and backward photons in bubble
    frame xi = x - v t; show backward photon passes the rear horizon into the rear wall,
    forward photon stalls at the front horizon.
 3. |E_-| vs v across v = 0.5 ... 10 (Delta = 1 m tanh, and QI-limited wall) to show
    the quantitative requirement is continuous across v = 1 while the causal obstruction
    switches on only at v > 1.
"""
import numpy as np

KG_PER_M = 1.3466e27
MSUN = 1.989e30
LP = 1.616255e-35
R = 100.0

def f_tanh(r, sigma):
    return (np.tanh(sigma*(r+R)) - np.tanh(sigma*(r-R)))/(2*np.tanh(sigma*R))

def fp_tanh(r, sigma):
    return sigma*(1/np.cosh(sigma*(r+R))**2 - 1/np.cosh(sigma*(r-R))**2)/(2*np.tanh(sigma*R))

def sigma_from_PF(Delta):
    # PF: Delta = (1+tanh^2 sR)^2/(2 s tanh sR) ~ 2/s for sR >> 1
    return 2.0/Delta

def radial_integrals(fun, fpfun, rgrid, v):
    f = fun(rgrid); fp = fpfun(rgrid)
    w = fp**2 * rgrid**2
    tot = np.trapezoid(w, rgrid)
    out = np.trapezoid(np.where(f < 1-1/v, w, 0.0), rgrid) if v > 1 else 0.0
    return tot, out

def energy_tanh(v, Delta):
    s = sigma_from_PF(Delta)
    r = np.linspace(max(R-40*Delta, 0), R+40*Delta, 400001)
    tot, _ = radial_integrals(lambda x: f_tanh(x, s), lambda x: fp_tanh(x, s), r, v)
    # angular factor: int (sin^2 th) dOmega = 8pi/3 -> E = -(v^2/32pi)(8pi/3) int f'^2 r^2 dr = -(v^2/12) int
    return -(v**2/12.0)*tot  # m (geometric)

print("=== 1. Share of Eulerian E_- outside comoving-timelike zone (f < 1-1/v) ===")
print("  (angular weight (y^2+z^2)/r^2 is even in x, so front and rear halves are equal)")
for v in [1.0, 1.1, 1.5, 2.0, 5.0, 10.0, 100.0]:
    s = sigma_from_PF(1.0)
    r = np.linspace(R-40, R+40, 400001)
    tot, out = radial_integrals(lambda x: f_tanh(x, s), lambda x: fp_tanh(x, s), r, v)
    # linear ramp over Delta = 1 m from R to R+1
    fl = lambda x: np.clip((R+1-x)/1.0, 0, 1)
    fpl = lambda x: np.where((x > R) & (x < R+1), -1.0, 0.0)
    rl = np.linspace(R-1, R+2, 300001)
    totl, outl = radial_integrals(fl, fpl, rl, v)
    # BM optimal f = min(R/r,1): share of int R^2/r^2 dr beyond f<1-1/v analytic = 1-1/v
    bm = (1-1/v) if v > 1 else 0.0
    sh = out/tot
    print(f"  v={v:6.1f}c  tanh {100*sh:6.2f}%  (front {50*sh:5.2f}% / rear {50*sh:5.2f}%)   "
          f"linear {100*outl/totl:6.2f}%   BM-optimal {100*bm:6.2f}%")

print("\n=== 2. Causal reach from ship centre (bubble frame xi = x - v t, along axis, v=10c, tanh Delta=1 m) ===")
v = 10.0; s = sigma_from_PF(1.0)
def dxi_dt(xi, sign):
    return v*(f_tanh(abs(xi), s) - 1) + sign
for sign, label in [(+1, "forward photon"), (-1, "backward photon")]:
    xi = 0.0; t = 0.0; dt = 1e-3
    for _ in range(2_000_000):
        xi += dxi_dt(xi, sign)*dt; t += dt
        if abs(xi) > R + 20: break
    fh = f_tanh(abs(xi), s)
    print(f"  {label}: after t={t:.1f} m, xi={xi:+.4f} m, f there={fh:.4f} (horizon f=1-1/v={1-1/v:.2f})")

print("\n=== 3. |E_-| vs v (tanh, R=100 m): quantitative demand is continuous across v=1 ===")
for v in [0.5, 0.9, 0.99, 1.01, 1.1, 2.0, 10.0]:
    E1 = energy_tanh(v, 1.0)*KG_PER_M
    # QI-limited PF wall Delta_QI = 97.7 v L_P (dossier D-54, alpha = 0.1); E ~ -v^2 R^2/(18 Delta)
    DQI = 97.7*v*LP
    EQI = -(v**2*R**2/(18*DQI))*KG_PER_M
    print(f"  v={v:5.2f}c  E(Delta=1 m) = {E1:.3e} kg ({E1/MSUN:.3e} Msun)   E(QI wall {DQI:.2e} m) = {EQI:.3e} kg")
print("  Ratio E(v=1.01)/E(v=0.99), Delta=1 m:", energy_tanh(1.01,1.0)/energy_tanh(0.99,1.0))

"""Falsifier C8-2 (scale): is causal access or the negative-energy requirement the binding
obstacle once the traveller lays the route in its own causal future (Krasnikov tube)?

Sources of the formulas (quoted in the verdict):
- Everett & Roman 1997 (gr-qc/9702049) p.7: return to Earth at Earth time t_E = D*delta
  (wall thickness neglected), round trip "arbitrarily small" by choice of delta.
- Everett & Roman 1997 Eq.(51)-(52): E ~ -alpha * rho_max * D / eps (geometric/Planck units),
  QI bound eps ~ l_P / sigma^2; their example eps = 100 l_P.
SI throughout unless marked geo (G = c = 1).
"""
import math

G = 6.674e-11        # SI
c = 2.998e8          # m/s
lP = 1.616e-35       # m
mP = 2.176e-8        # kg
Msun = 1.989e30      # kg
Mgal = 1e12 * Msun   # Everett-Roman's galaxy mass convention
ly = 9.461e15        # m
yr = 3.156e7         # s

D = 4.37 * ly        # Earth -> alpha Cen, m
print(f"D = {D:.3e} m (4.37 ly)")

# --- 1. Timing: tube laid on outbound leg, return leg hastened (Everett-Roman p.7) ---
t_out = D / c / yr   # outbound at ~c, Earth clock, yr
for delta in (0.5, 0.1, 0.01):
    tE = delta * D / c / yr
    print(f"delta={delta}: Earth-clock return t_E = {tE:.4f} yr; light round trip 2D/c = {2*t_out:.2f} yr; "
          f"light from B at departure (t=D/c) reaches A at {2*t_out:.2f} yr -> return leg advance = {2*t_out - tE:.3f} yr")

# --- 2. Negative energy of the alpha-Cen tube (Everett-Roman scaling) ---
rho_max = 1.0        # m, tube radius
def E_tube_kg(alpha, rho, Dlen, eps):
    E_geo = alpha * rho * Dlen / eps        # metres (geo)
    return E_geo * c**2 / G                 # kg
for alpha in (1.0, 0.01):
    for eps_lab, eps in (("QI eps=100 lP", 100 * lP), ("eps=1 m (QI ignored)", 1.0)):
        M = E_tube_kg(alpha, rho_max, D, eps)
        print(f"alpha={alpha}, {eps_lab}: |E|/c^2 = {M:.3e} kg = {M/Msun:.3e} Msun = {M/Mgal:.3e} Mgal")
# check against Everett-Roman 1 m x 1 m example: 1e68 m_P
M1 = E_tube_kg(1.0, 1.0, 1.0, 100 * lP)
print(f"check 1 m tube, alpha=1, eps=100 lP: {M1/mP:.3e} m_P (E-R quote ~1e68 m_P with 1 m = 1e35 lP)")

# Hubble-volume mass-energy at critical density, as a scale reference
H0 = 67.7e3 / 3.086e22   # 1/s
M_H = c**3 / (2 * G * H0)  # = rho_c * (4/3) pi (c/H0)^3
print(f"Hubble-volume critical-density mass c^3/(2 G H0) = {M_H:.3e} kg")
M_QI = E_tube_kg(0.01, rho_max, D, 100 * lP)
print(f"alpha=0.01 QI tube / Hubble-volume mass = {M_QI/M_H:.3e} (log10 {math.log10(M_QI/M_H):.1f})")

# --- 3. Cost of solving causal access: the subluminal outbound leg itself ---
m_pay = 1e5  # kg
world_E = 6.0e20  # J/yr, order of world primary energy (reference scale)
for beta in (0.1, 0.5, 0.99):
    gam = 1 / math.sqrt(1 - beta**2)
    KE = (gam - 1) * m_pay * c**2
    # ideal photon rocket, accelerate then stop: mass ratio = exp(2*rapidity)
    phi = math.atanh(beta)
    R = math.exp(2 * phi)
    E_fuel = (R - 1) * m_pay * c**2
    print(f"outbound at {beta}c: trip {D/(beta*c)/yr:.1f} yr; KE = {KE:.3e} J ({KE/world_E:.2e} world-years); "
          f"photon rocket accel+stop fuel energy = {E_fuel:.3e} J ({E_fuel/world_E:.2e} world-years)")

E_neg_J = M_QI * c**2
E_fuel_01 = (math.exp(2 * math.atanh(0.1)) - 1) * m_pay * c**2
print(f"gap: negative-energy requirement (alpha=0.01, QI wall) {E_neg_J:.3e} J vs causal-access leg {E_fuel_01:.3e} J "
      f"-> {math.log10(E_neg_J/E_fuel_01):.1f} orders of magnitude")
E_fuel_99 = (math.exp(2 * math.atanh(0.99)) - 1) * m_pay * c**2
print(f"near-c outbound (0.99c, needed for a short Earth-clock round trip): {E_fuel_99:.3e} J -> gap {math.log10(E_neg_J/E_fuel_99):.1f} orders")
# slow outbound: return leg still beats light sent from B at the ship's departure from B
v = 0.1 * c
t_arrB = D / v
for delta in (0.1, 0.01):
    t_ret = t_arrB - D * (1 - delta) / c
    print(f"outbound 0.1c, delta={delta}: depart B at {t_arrB/yr:.2f} yr, return to A at {t_ret/yr:.2f} yr, "
          f"light from B arrives {(t_arrB + D/c)/yr:.2f} yr -> return-leg advance {(t_arrB + D/c - t_ret)/yr:.2f} yr")
E_neg_thick = E_tube_kg(0.01, rho_max, D, 1.0) * c**2
print(f"even with eps = 1 m (QI ignored), alpha=0.01: {E_neg_thick:.3e} J -> {math.log10(E_neg_thick/E_fuel_01):.1f} orders above the outbound leg")

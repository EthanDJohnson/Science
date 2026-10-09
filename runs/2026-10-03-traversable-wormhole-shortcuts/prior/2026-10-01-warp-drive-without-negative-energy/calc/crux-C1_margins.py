"""Crux C1: small checks used in cruxes/C1.md.

1. C7's scaling law beta_max ~ k * C * (Delta/R2): test it on refuter 2's design-scan
   numbers (verdict C1-2 table, beta_NEC/C per geometry), all with R2 = 20 m except
   where the table's C differs (R2 fixed at 20 m in that scan; Delta = R2 - R1).
2. Thin-shell analytic necessary threshold beta_int = C/2 against caps 0.07-0.09 C
   (refuter 2's check), and the floor of the scanned family.
3. Linear dragging coefficient kappa = 4GM/(c^2 R) for the rebuild mass (C4 crux),
   and the NEC-capped shift as an order-of-magnitude scale for any shift-dependent
   correction to kappa (our assumption, stated in the crux).
Units: SI for G, c, M, R; beta and C dimensionless (units of c / geometric).
"""
G = 6.674e-11      # m^3 kg^-1 s^-2
c = 2.998e8        # m/s
M = 4.511e27       # kg, rebuild ADM mass (lens-constraints_shell.py)
R2 = 20.0          # m

# Refuter 2 table rows: (R1 [m], C, beta_NEC/C, required/achievable)
rows = [
    (10, 0.3334, 0.0743, 8.5),
    (10, 0.10, 0.0806, 7.9),
    (10, 0.60, 0.0613, 10.0),
    (16, 0.3334, 0.0224, 24.6),
    (5, 0.3334, 0.1349, 5.1),
    (2, 0.3334, 0.1727, 4.09),
    (1, 0.3334, 0.1830, 3.88),
    (0.5, 0.3334, 0.1871, 3.81),
    (2, 0.80, 0.0951, 6.36),
    (2, 0.85, 0.0758, 7.70),
    (0.5, 0.01, 0.2222, 3.38),
    (0.5, 0.10, 0.2102, 3.53),
]
print("1. C7 law test: k = (beta_NEC/C)/(Delta/R2), Delta = R2 - R1, R2 = 20 m")
ks = []
for R1, C, bc, ratio in rows:
    dr = (R2 - R1) / R2
    k = bc / dr
    ks.append((C, dr, k))
    print(f"   R1={R1:5.1f} m  C={C:.4f}  Delta/R2={dr:.3f}  beta_NEC/C={bc:.4f}  k={k:.3f}  req/ach={ratio}")
kC333 = [k for C, dr, k in ks if abs(C - 0.3334) < 1e-3]
print(f"   at C=0.333: k ranges {min(kC333):.3f}-{max(kC333):.3f} (C7 linear-theory k = 0.18-0.37)")
print(f"   thin wall (Delta/R2=0.2) k = {kC333[1]:.3f}; thick (0.975) k = {kC333[-1]:.3f}")

print("2. Thin-shell necessary threshold beta_int = C/2 against cap r*C")
for r in (0.07, 0.08, 0.09):
    print(f"   cap ratio {r}: required/achievable = {0.5 / r:.2f}")
print(f"   scanned-family floor (refuter 2): {min(r[3] for r in rows):.2f}")

print("3. Linear dragging coefficient kappa = 4GM/(c^2 R)")
for R in (20.0, 10.0):
    kap = 4 * G * M / (c**2 * R)
    print(f"   R = {R:.0f} m: kappa = {kap:.3f}")
beta_cap = 0.0239
print(f"   NEC-capped shift beta_crit = {beta_cap} (M-CONSTRAINTS-13): first-order shift "
      f"correction scale to kappa ~ beta = {beta_cap*100:.1f} % of kappa (assumption)")

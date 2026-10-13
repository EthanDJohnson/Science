#!/usr/bin/env python3
"""Challenge (spacetime, referee 1): where does r_min = lambda/2pi sit relative to a GW150914-like source?
ASSUMED input (not from B&O): total mass M = 65 Msun (GW150914-like); B&O's anchor nu_GW = 150 Hz.  Newtonian Kepler
separation a = (G M / Omega^2)^(1/3), Omega = pi nu_GW (orbital), compared with 1/k = c/(2 pi nu) and G M/c^2."""
import math
Gs, cs, Msun = 6.67430e-11, 2.99792458e8, 1.98847e30
M, nu = 65 * Msun, 150.0
Om = math.pi * nu
a = (Gs * M / Om ** 2) ** (1 / 3)
rg = Gs * M / cs ** 2
print(f"1/k = lambda/2pi = {cs/(2*math.pi*nu)/1e3:.1f} km; GM/c^2 = {rg/1e3:.1f} km; Kepler separation a = {a/1e3:.1f} km"
      f" (= {a/rg:.2f} GM/c^2, k a = {a*2*math.pi*nu/cs:.2f}); each body at ~a/2 = {a/2e3:.1f} km from the centre; v = Om a/c = {Om*a/cs:.2f}")

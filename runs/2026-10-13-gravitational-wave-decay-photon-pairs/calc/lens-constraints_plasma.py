"""Constraints lens: plasma kinematics for g g -> gamma gamma.

In a cold unmagnetised plasma a transverse photon obeys w^2 = k^2 + w_p^2 (effective mass m_gamma = hbar w_p).
Pair production g g -> gamma gamma then needs s >= 4 w_p^2. Two gravitons of angular frequency w have
s = 2 w^2 (1 - cos theta) <= 4 w^2, so production needs w > w_p AND theta >= theta_min = 2 arcsin(w_p/w).
Far from a source the available s of a locally-plane spherical wave is s ~ 4 w c / r (Fresnel-zone angular
spread theta^2 ~ c/(w r); see lens-constraints_farzone.py), so production in a medium also needs
r <= r_max = c w / w_p^2.

Units: SI unless stated; photon energies in eV.  f_pe = 8980 Hz sqrt(n_e / cm^-3) [D-07].
Cosmic plasma: n_e(z) = n_e0 (1+z)^3 x_e(z), n_e0 = 2.2e-7 cm^-3 for full ionisation of all baryons [D-40];
x_e = 1 before recombination (z > 1100, helium recombination ignored: at most a 8% change in n_e);
x_e ~ 2e-4 in the dark ages (assumed freeze-out value); x_e = 1 after reionisation (z < 7).
"""
import math

hbar_eVs = 6.582119569e-16
h_eVs = 4.135667696e-15
c = 2.99792458e8

def f_pe(ne_cm3):
    return 8980.0 * math.sqrt(ne_cm3)

print("=== 1. Local media: plasma frequency vs GW frequency (photon needs f_gamma > f_pe) ===")
media = [("IGM mean today, all baryons ionised [D-40]", 2.2e-7),
         ("IGM today, realistic mean (2.2e-7/8, [D-40 note])", 2.2e-7 / 8),
         ("hot ISM (assumed 3e-3 cm^-3)", 3e-3),
         ("warm ISM [D-40]", 0.03),
         ("VLISM (Voyager) [D-07]", 0.08),
         ("solar wind at 1 AU [D-40]", 5.0),
         ("ionosphere F layer [D-40]", 1e6)]
for name, ne in media:
    fp = f_pe(ne)
    print(f"  {name:50s} n_e = {ne:9.3e} cm^-3  f_pe = {fp:10.3e} Hz  hbar w_p = {h_eVs*fp:9.3e} eV")

print("\n=== 2. Kinematic window for g g -> gamma gamma at the GW150914 band ===")
for fgw in (35.0, 150.0, 250.0):
    w = 2 * math.pi * fgw
    for name, ne in media[:4]:
        fp = f_pe(ne)
        wp = 2 * math.pi * fp
        if fgw <= fp:
            print(f"  f_GW = {fgw:6.1f} Hz in {name[:28]:28s}: FORBIDDEN (f_GW/f_pe = {fgw/fp:.3g} < 1)")
        else:
            thmin = 2 * math.asin(fp / fgw)
            rmax = c * w / wp**2
            lam = c / fgw
            print(f"  f_GW = {fgw:6.1f} Hz in {name[:28]:28s}: allowed for theta > {math.degrees(thmin):6.2f} deg;"
                  f" far-zone production stops beyond r_max = c w/w_p^2 = {rmax:9.3e} m = {rmax/lam:9.3e} lambda")

print("\n=== 3. Cosmic plasma: minimum physical photon energy hbar w_p(z) for production at redshift z ===")
fp0 = f_pe(2.2e-7)
def xe(z):
    if z > 1100: return 1.0
    if z < 7: return 1.0
    return 2e-4
def hwp(z):
    return h_eVs * fp0 * (1 + z) ** 1.5 * math.sqrt(xe(z))
for z in (0, 6, 20, 100, 1000, 1101, 3e3, 1e4, 1e5, 3e5, 1e6, 2e6, 3e6):
    print(f"  z = {z:9.3g}: hbar w_p = {hwp(z):10.3e} eV  (f_p,phys = {hwp(z)/h_eVs:10.3e} Hz)")
print("  B&O y window 1e3 < z < 1e5 needs hbar w_s > %.2e .. %.2e eV" % (hwp(1101), hwp(1e5)))
print("  B&O mu window 1e5 < z < 3e6 needs hbar w_s > %.2e .. %.2e eV" % (hwp(1e5), hwp(3e6)))
print("  B&O Fig. 3 x-axis starts at hbar w_s = 1e-10 eV (f = %.3e Hz)" % (1e-10 / h_eVs))

print("\n=== 4. A GW observed today at f0 (a fixed comoving frequency, e.g. a primordial SGWB) ===")
print("  photon at f0(1+z) propagates/produced iff f0 > f_p0 sqrt(1+z) sqrt(x_e) (f_p0 = %.3f Hz)" % fp0)
for f0 in (1e-8, 25.0, 1e3, 1e4):
    zs = []
    for z in (10, 100, 1000, 1101, 1e4, 1e5, 1e6, 3e6):
        ok = f0 * (1 + z) > hwp(z) / h_eVs
        zs.append(f"z={z:.0e}:{'ok' if ok else 'NO'}")
    print(f"  f0 = {f0:8.1e} Hz: " + ", ".join(zs))
for f0 in (25.0,):
    print(f"  pre-recombination cut-off for f0 = {f0} Hz: 1+z < (f0/f_p0)^2 = {(f0/fp0)**2:.3g}"
          " (so forbidden at all z > 1100)")
print("  minimum f0 for production at z = 1e5: %.3e Hz; at z = 2e6: %.3e Hz" %
      (fp0 * math.sqrt(1e5), fp0 * math.sqrt(2e6)))

"""Falsifier C7-1 (evidence angle): checks on the C7 reframe.
Units: H0 in km/s/Mpc, r_d in Mpc, magnitudes in mag (astronomical units, not SI).

(a) DESI DR2 (arXiv:2503.14738, Table p.20, fetched): how far data-allowed late-time
    H(z) freedom (w0waCDM) moves the r_d-side H0, against the C7 prediction
    "no modification of H(z) at 0<z<2 changes the gap by more than ~0.5 sigma".
(b) The r_d "calibration" read as a pre-recombination expansion rate: uniform
    fractional increase x of H(z) for z > z_d gives r_d -> r_d/(1+x).
(c) Status of the anchor-free, r_d-free arbiters against the two poles.
"""
import math

H0DN, sH0DN = 73.264, 0.806          # D-22
LCDM = (68.17, 0.28)                 # DESI+CMB LCDM, DESI DR2 eq. 21
w0wa = {                             # DESI DR2 Table (p.20), w0waCDM
    "DESI+CMB": (63.6, 1.6),         # +1.6/-2.1, facing-side (upper) error used
    "DESI+CMB+Pantheon+": (67.51, 0.59),
    "DESI+CMB+Union3": (65.91, 0.84),
    "DESI+CMB+DESY5": (66.74, 0.56),
}

def z(a, sa, b, sb):
    return (a - b) / math.hypot(sa, sb)

print("(a) Late-time H(z) freedom (w0waCDM) vs LCDM, r_d-side H0")
gap0 = H0DN - LCDM[0]
s0 = math.hypot(sH0DN, LCDM[1])
z0 = gap0 / s0
print(f"  LCDM DESI+CMB: gap = {gap0:.3f} +- {s0:.3f} km/s/Mpc, tension = {z0:.2f} sigma")
for k, (h, s) in w0wa.items():
    g = H0DN - h
    sg = math.hypot(sH0DN, s)
    dH = LCDM[0] - h
    print(f"  {k:22s}: H0 = {h:6.2f}; shift dH = {-dH:+.2f} km/s/Mpc "
          f"= {dH/s0:.2f} x sigma_gap(LCDM) = {dH/gap0*100:.0f}% of gap; "
          f"5log10 shift = {5*math.log10(LCDM[0]/h):.3f} mag; "
          f"tension {g/sg:.2f} sigma (change {g/sg - z0:+.2f} sigma)")

print("\n(b) r_d as a pre-recombination expansion rate")
for rd_need in (138.6, 134.8):
    x = 147.0 / rd_need - 1
    print(f"  r_d 147.0 -> {rd_need} Mpc needs uniform H(z>z_d) increase of {100*x:.2f}%")
print(f"  compare H0 ratio H0DN/CMB-SPA - 1 = {100*(73.264/67.19-1):.2f}%")

print("\n(c) Arbiters (anchor-free, r_d-free) vs the two poles")
poles = {"r_d group": (67.51, 0.29), "anchor group": (73.02, 0.78)}
arbiters = {
    "TDCOSMO-2026 (71.1 +2.4/-2.3)": None,
    "one-step mean (M-DIALECTICIAN-07)": (71.27, 1.93),
    "swing class (M-EXAMINER-06)": (69.93, 1.17),
}
for k, v in arbiters.items():
    out = []
    lik = {}
    for pn, (pm, ps) in poles.items():
        if v is None:
            m = 71.1
            s = 2.3 if m > pm else 2.4   # facing-side error
        else:
            m, s = v
        zz = (m - pm) / math.hypot(s, ps)
        lik[pn] = math.exp(-0.5 * zz * zz) / math.hypot(s, ps)
        out.append(f"{pn}: {zz:+.2f} sigma")
    lr = lik["anchor group"] / lik["r_d group"]
    print(f"  {k:36s}: " + "; ".join(out) + f"; likelihood ratio anchor:r_d = {lr:.2f}")

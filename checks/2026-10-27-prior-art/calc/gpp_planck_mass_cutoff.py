"""Own extension (not prior art): coherence left in GPP eq. (5) when the remaining lifetime equals that of a
Planck-mass hole, i.e. where the semiclassical Hawking description is generally expected to stop (M ~ M_P).
Hawking lifetime tau(M) = 5120 pi G^2 M^3 /(hbar c^4). CODATA 2018 constants."""
from mpmath import mp, mpf, pi, sqrt, exp, log
mp.dps = 40
G = mpf("6.67430e-11"); hbar = mpf("1.054571817e-34"); c = mpf("299792458")
tP = sqrt(hbar*G/c**5); MP = sqrt(hbar*c/G)
def life(M): return 5120*pi*G**2*M**3/(hbar*c**4)
print("t_P = %s s, M_P = %s kg, lifetime of a Planck-mass hole = %s s = %s t_P" % (mp.nstr(tP,6), mp.nstr(MP,6), mp.nstr(life(MP),6), mp.nstr(life(MP)/tP,6)))
for name, M in (("solar mass", mpf("1.98847e30")), ("1e12 kg", mpf("1e12"))):
    Tmax = life(M)
    for lab, k in (("k=(8pi)^-2", 1/(8*pi)**2), ("k=(8pi)^-4", 1/(8*pi)**4)):
        for gapname, gap in (("1 t_P", tP), ("Planck-mass lifetime", life(MP))):
            coh = ((gap)/Tmax)**k
            print("%-11s %-11s gap=%-21s coherence left = %s" % (name, lab, gapname, mp.nstr(coh, 6)))

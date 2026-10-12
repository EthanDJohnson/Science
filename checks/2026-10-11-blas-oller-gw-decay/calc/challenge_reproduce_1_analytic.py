"""Challenge of Task A: hand-route (sympy) re-derivation of B&O eq. 8 / S6 and the scalar 7/(450 pi), plus T_eff.
Independent of bo_ring/bo_common.  omega_s = w, sigma = sg."""
import sympy as sp
import numpy as np

w, sg, K, G, N, th, al, ph, c = sp.symbols('omega sigma K G N theta alpha phi c', positive=True)
pi = sp.pi
# (1) S6 prefactor from eq. 7: A = 4piG/(2pi)^6 int d3k1/2k1 d3k2/2k2 f f (t^2+u^2)/s (2pi)^4 delta^4.
#     P = (1/2) sum_mu int d3q1 d3q2/((2pi)^6 4 q1 q2) |A|^2 ; sum_mu delta_{mu mu} -> 2 ; d^4Q/(2pi)^4 dOmega/(32 pi^2)
pref = sp.Rational(1, 2) * 2 * (4 * pi * G) ** 2 / ((2 * pi) ** 4 * (2 * w) ** 4) / (2 * pi) ** 4 / (32 * pi ** 2) / (2 * pi)
print('S6 prefactor derived:', sp.simplify(pref), '  B&O:', G ** 2 / (16384 * pi ** 9 * w ** 4),
      ' equal:', sp.simplify(pref - G ** 2 / (16384 * pi ** 9 * w ** 4)) == 0)
# (2) CM: graviton axis a(alpha) perp to K, photon n at polar theta from K: x = a.n = sin(theta) cos(alpha - phi)
s = 4 * w ** 2 - K ** 2
x = sp.sin(th) * sp.cos(al)
t_ = -s * (1 - x) / 2; u_ = -s * (1 + x) / 2
I_ph = sp.integrate(sp.expand((t_ ** 2 + u_ ** 2) / s), (al, 0, 2 * pi))
I_sc = sp.integrate(sp.expand(t_ * u_ / s), (al, 0, 2 * pi))
ang_ph = sp.integrate(sp.expand(I_ph ** 2) * sp.sin(th), (th, 0, pi)) * 2 * pi
ang_sc = sp.integrate(sp.expand(I_sc ** 2) * sp.sin(th), (th, 0, pi)) * 2 * pi
print('int dOmega [int dalpha (t^2+u^2)/s]^2 =', sp.factor(ang_ph), '  (claim 36 pi^3 s^2/5:', sp.simplify(ang_ph - 36 * pi ** 3 * s ** 2 / 5) == 0, ')')
# ring: exact Jacobian d3k = a b da db dalpha / K -> narrow band: (w sigma)^2 / K * dalpha ; f = Theta on band
Theta2 = 2 * pi ** 2 * N / (w * sg)
ringfac = (w * sg) ** 2 / K   # int da db a b / K
# 2pi delta(0) -> T: P/T = pref * Theta^4 * int d3K (ringfac)^2 [ang]/(2pi)... careful: int dalpha already in ang
# P/T = pref Theta^4 int 4 pi K^2 dK (ringfac)^2 * int dOmega [int dalpha F]^2 ; the S6 (2pi)delta -> T
rate_ph = sp.simplify(pref * Theta2 ** 2 * sp.integrate(4 * pi * K ** 2 * ringfac ** 2 * ang_ph, (K, 0, 2 * w)))
print('dP/dt photons (pairs per unit time) =', rate_ph, '  ratio to 3G^2N^2w^3sg^2/(25pi):', sp.simplify(rate_ph / (3 * G ** 2 * N ** 2 * w ** 3 * sg ** 2 / (25 * pi))))
# scalars: B&O-model amplitude (1/2) sum f f A = Theta^2 (A++ + A+-), m=0: A++=0, A+- = -8piG tu/s ; one final channel, 1/2 identical
# photons: (1/2) sum f f A_{mu mu} = (1/2) Theta^2 8piG (t^2+u^2)/s per mu, 2 mu's.  So relative to the photon S6 integrand
# [ (1/2)(t^2+u^2)/s ]^2 x 2 = (1/2)[(t^2+u^2)/s]^2  the scalar integrand is [tu/s]^2:
ratio_sc = sp.simplify(ang_sc / (ang_ph / 2))
print('scalar/photon (m=0, B&O model) =', ratio_sc, '-> C_scalar =', sp.simplify(ratio_sc * sp.Rational(3, 25) / pi), ' (claim 7/(450 pi))')
# (3) exact energy delta instead of 2pi delta(0)->T: int over four band offsets of delta(d1+d2-d1'-d2')
d = sp.symbols('d')
# density of d1+d2-d3-d4 for 4 iid uniform(-1/2,1/2) at 0 = Irwin-Hall(4) at its mean = 2/3
y = sp.symbols('y')
IH = sum((-1) ** k * sp.binomial(4, k) * sp.Max(0, y - k) ** 3 for k in range(5)) / sp.factorial(3)
dens = IH.subs(y, 2)
print('Irwin-Hall n=4 density at centre =', dens)
Teff = sp.simplify(2 * pi * dens * sg ** 3 / sg ** 4)
print('T_eff = 2 pi (2/3) sigma^3 / sigma^4 =', Teff, ' -> P_total/(G^2 N^2 w^3 sigma) =', sp.simplify(rate_ph * Teff / (G ** 2 * N ** 2 * w ** 3 * sg)))
rng = np.random.default_rng(0)
dd = rng.uniform(-0.5, 0.5, size=(4, 4_000_000)); z = dd[0] + dd[1] - dd[2] - dd[3]
print('MC density at 0 (bin 0.01):', np.mean(np.abs(z) < 0.005) / 0.01)

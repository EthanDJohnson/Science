"""Falsifier C3-2 (scale angle): does the retarded / time-symmetric yield ratio stay small
at the real bandwidth of GW150914 (sigma/w = 200/(2 pi 150) = 0.21) and for broader bursts?

Toy (natural units, w = 1, dimensionless): scalar monopole, phi_ret = g(t-r)/r,
phi_sym = [g(t-r) - g(t+r)]/r, g = A(t) cos t, A = exp(-sigma^2 t^2 / 2) (Gaussian envelope),
j = phi^2, yield Y = Int d^4q theta(q0) theta(q^2) (q^2)^p |J(q)|^2.  Only the sum-frequency
(g g fusion) part of j is kept, as in B&O's process.

Analytic reductions (own derivation, checked numerically below):
  sum-frequency part, F(x) = sqrt(pi)/sigma exp(-x^2/(4 sigma^2)):
  J_ret(q0,q) = (4 pi/q) * i artanh(q/q0) * F(q0-2)/4                      (q < q0)
  J_sym(q0,q) = -(4 pi/q) * (pi/4) * F(q0-2) * erf(q/(2 sigma))              (q < q0; self terms vanish)
  so ratio(p) = Int dq0 F^2 q0^(2p+1) Int_0^1 (1-x^2)^p artanh(x)^2 dx
              / Int dq0 F^2 q0^(2p+1) Int_0^1 (1-x^2)^p pi^2 erf(x q0/(2 sigma))^2 dx
Narrow-band limit: ratio_0 = 1/12, ratio_2 = 0.0200 (matches M-EXAMINER-03).
Also a brute-force check of J_sym by direct quadrature at one (q0, q) point.
"""
import mpmath as mp

mp.mp.dps = 12

def F(x, s):
    return mp.sqrt(mp.pi) / s * mp.e ** (-x * x / (4 * s * s))

def inner_ret(p):
    return mp.quad(lambda x: (1 - x * x) ** p * mp.atanh(x) ** 2, [0, 0.5, 0.9, 0.99, 1])

def inner_sym(p, q0, s):
    return mp.quad(lambda x: (1 - x * x) ** p * mp.pi ** 2 * mp.erf(x * q0 / (2 * s)) ** 2, [0, 0.1, 0.5, 1])

def ratio(p, s):
    lo = max(mp.mpf('1e-6'), 2 - 12 * s)
    hi = 2 + 12 * s
    num = mp.quad(lambda q0: F(q0 - 2, s) ** 2 * q0 ** (2 * p + 1), [lo, 2, hi]) * inner_ret(p)
    den = mp.quad(lambda q0: F(q0 - 2, s) ** 2 * q0 ** (2 * p + 1) * inner_sym(p, q0, s), [lo, 2, hi])
    return num / den

# brute-force check of J_sym's cross term at one point (sigma = 0.21, q0 = 2.05, q = 0.7)
def brute_Jsym(q0, q, s):
    # sum-frequency cross term: -2 * Int dt e^{i q0 t} [A(t-r)A(t+r) (1/2) cos 2t]_sumfreq ... done via t-integral numerically
    def C(r):
        f = lambda t: mp.e ** (-s * s * ((t - r) ** 2 + (t + r) ** 2) / 2) * 0.5 * mp.cos(2 * t) * mp.cos(q0 * t)
        return 2 * mp.quad(f, [0, 10 / s])  # even integrand in t (cos q0 t part; sin part vanishes)
    I = mp.quad(lambda r: C(r) * mp.sin(q * r) / r, [0, 2 / s, 6 / s, 12 / s])
    return (4 * mp.pi / q) * (-2) * I

s0, q0c, qc = mp.mpf('0.21'), mp.mpf('2.05'), mp.mpf('0.7')
analytic = -(4 * mp.pi / qc) * (mp.pi / 4) * (F(q0c - 2, s0) + F(q0c + 2, s0)) * mp.erf(qc / (2 * s0))
print("check J_sym cross term (sigma=0.21, q0=2.05, q=0.7): brute =", mp.nstr(brute_Jsym(q0c, qc, s0), 8),
      " analytic =", mp.nstr(analytic, 8))

print("narrow-band closed forms: p=0 ->", mp.nstr(inner_ret(0) / mp.pi ** 2, 6), "(1/12 =", mp.nstr(mp.mpf(1) / 12, 6), ")",
      " p=2 ->", mp.nstr(inner_ret(2) / (mp.pi ** 2 * mp.mpf(8) / 15), 6))
print("sigma/w   ratio_ret/sym(p=0)   ratio_ret/sym(p=2)   [p=2 is the graviton-fusion weight |M|^2 ~ s^2]")
for s in ['0.01', '0.1', '0.21', '0.3', '0.5', '0.7', '1.0']:
    s = mp.mpf(s)
    print(f"{float(s):6.2f}   {float(ratio(0, s)):.4f}               {float(ratio(2, s)):.4f}")

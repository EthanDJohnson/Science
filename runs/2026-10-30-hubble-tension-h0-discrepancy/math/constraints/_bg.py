"""Independent flat-FRW background toolkit for the constraints math check (written from definitions).

Units: H in km/s/Mpc, distances in Mpc, times in Gyr (cosmology units, not SI).
Physical densities omega_i = Omega_i h^2.  Radiation: photons (T = 2.7255 K) + N_eff * (7/8)(4/11)^(4/3).
Massive neutrino (sum m_nu = 0.06 eV) is folded into matter as omega_nu = 0.06/93.14.
z_* from the Hu & Sugiyama (1996) fit.  r_s = int_{z_*}^inf c_s dz / H, c_s = c / sqrt(3(1+R)), R = 3 omega_b / (4 omega_gamma) a.
Dark energy: Lambda, constant w, CPL, plus an optional early-dark-energy fluid
rho_EDE(a) = 2 rho_c / (1 + (a/a_c)^(3(1+w_n))), w_n = (n-1)/(n+1), f = rho_EDE(a_c)/rho_tot(a_c).
"""
import numpy as np

C = 299792.458            # km/s
OMG = 2.47282e-5          # omega_gamma for T = 2.7255 K
NUF = 7 / 8 * (4 / 11) ** (4 / 3)
ONU = 0.06 / 93.14


def omega_r(neff=3.044):
    return OMG * (1 + NUF * neff)


def zstar_hs(wb, wm):
    g1 = 0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * wb ** 1.81)
    return 1048 * (1 + 0.00124 * wb ** -0.738) * (1 + g1 * wm ** g2)


class Model:
    def __init__(self, h, wb, wc, neff=3.044, w0=-1.0, wa=0.0, f_ede=0.0, zc=3500.0, n_ede=3, me=1.0):
        self.h, self.wb, self.wc, self.neff = h, wb, wc, neff
        self.wm = wb + wc + ONU
        self.wr = omega_r(neff)
        self.w0, self.wa = w0, wa
        self.me = me
        self.f, self.ac, self.p = f_ede, 1 / (1 + zc), 3 * (1 + (n_ede - 1) / (n_ede + 1))
        if f_ede > 0:
            rest = self.wm * self.ac ** -3 + self.wr * self.ac ** -4
            self.rc = f_ede / (1 - f_ede) * rest
        else:
            self.rc = 0.0
        self.wde = h * h - self.wm - self.wr - self._ede(1.0)

    def _ede(self, a):
        return 0.0 if self.rc == 0 else 2 * self.rc / (1 + (a / self.ac) ** self.p)

    def E2(self, a):  # (H/100)^2
        de = self.wde * a ** (-3 * (1 + self.w0 + self.wa)) * np.exp(-3 * self.wa * (1 - a))
        return self.wr * a ** -4 + self.wm * a ** -3 + de + self._ede(a)

    def H(self, a):
        return 100 * np.sqrt(self.E2(a))

    @property
    def Om(self):
        return self.wm / self.h ** 2

    def zstar(self):
        return zstar_hs(self.wb, self.wm) * self.me  # z_* scales with m_e (binding energy)

    @staticmethod
    def _simpson(y, x):
        n = len(x) - 1
        hstep = (x[-1] - x[0]) / n
        return hstep / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())

    def rs(self, z, n=20000):
        lna = np.linspace(np.log(1e-9), np.log(1 / (1 + z)), n + 1)
        a = np.exp(lna)
        R = 3 * self.wb / (4 * OMG) * a
        cs = C / np.sqrt(3 * (1 + R))
        return self._simpson(cs / (a * self.H(a)), lna)

    def DM(self, z, n=20000):
        lna = np.linspace(np.log(1 / (1 + z)), 0.0, n + 1)
        a = np.exp(lna)
        return self._simpson(C / (a * self.H(a)), lna)

    def theta100(self):
        zs = self.zstar()
        return 100 * self.rs(zs) / self.DM(zs)

    def age(self, n=20000):
        lna = np.linspace(np.log(1e-10), 0.0, n + 1)
        a = np.exp(lna)
        return self._simpson(1 / self.H(a), lna) * 977.792  # (km/s/Mpc)^-1 -> Gyr

    def lookback(self, z, n=4000):
        lna = np.linspace(np.log(1 / (1 + z)), 0.0, n + 1)
        a = np.exp(lna)
        return self._simpson(1 / self.H(a), lna) * 977.792


def bisect(fun, lo, hi, tol=1e-10, it=200):
    flo = fun(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def near(name, got, want, tol):
    """PASS if |got - want| <= tol, via math_checks.inequality on numbers."""
    from math_checks import inequality
    got, want = float(got), float(want)
    print(f"  {name}: got {got:.6g}, lens {want:.6g}, tol {tol:g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<=", repr(float(tol)))

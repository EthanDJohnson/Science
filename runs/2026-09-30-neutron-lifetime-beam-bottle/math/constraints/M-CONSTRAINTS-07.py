"""M-CONSTRAINTS-07 (F10, K5): dark-decay kinematic window from atomic mass excesses (AME2020, keV).
Thresholds (atomic masses; electron counts balance):
 9Be -> 8Be + chi requires m_chi > m_n - S_n(9Be);  9Be -> 2 alpha + chi requires m_chi > m_n - S(9Be -> 2a + n).
 chi stable against chi -> p e nu: m_chi < m_p + m_e.  n -> chi e+ e-: m_chi < m_n - 2 m_e.
 p -> chi e+ nu forbidden: m_chi > m_p - m_e.  11Be -> 10Be + chi open if m_chi < m_n - S_n(11Be).
 E_gamma = (m_n^2 - m_chi^2)/(2 m_n)."""
from _common import near
from math_checks import identity, series, finish

ME = {"n": 8071.3181, "4He": 2424.9156, "8Be": 4941.672, "9Be": 11348.453, "10Be": 12607.49, "11Be": 20177.17}
mn, mp_, me = 939.56542, 938.27209, 0.51100
Sn9 = (ME["8Be"] + ME["n"] - ME["9Be"]) / 1e3
S2a = (2 * ME["4He"] + ME["n"] - ME["9Be"]) / 1e3
Sn11 = (ME["10Be"] + ME["n"] - ME["11Be"]) / 1e3
near("S_n(9Be) MeV", Sn9, 1.66454, 6e-5)
near("9Be -> 2a + n MeV", S2a, 1.57270, 6e-5)
near("S_n(11Be) MeV", Sn11, 0.50164, 6e-5)
lo2, lo1 = mn - S2a, mn - Sn9
near("F-G lower edge (FG print 937.900)", lo1, 937.900, 1.5e-3); near("3-body lower edge", lo2, 937.993, 6e-4)
near("tightening keV", 1e3 * (lo2 - lo1), 92, 0.6)
up_stab, up_ee, up_11 = mp_ + me, mn - 2 * me, mn - Sn11
near("chi stability", up_stab, 938.783, 6e-4); near("e+e- upper", up_ee, 938.543, 6e-4)
near("11Be open below", up_11, 939.064, 6e-4)
near("proton stability", mp_ - me, 937.761, 6e-4)
Eg = lambda m: (mn**2 - m**2) / (2 * mn)
near("E_gamma min", Eg(up_stab), 0.782, 6e-4); near("E_gamma max", Eg(lo2), 1.571, 6e-4)
w = up_ee - lo2
near("e+e- width keV", 1e3 * w, 551, 1.0)
gap_lo = up_ee - 0.032
near("PERKEO gap lower m_chi", gap_lo, 938.511, 6e-4)
near("gap fraction (narrowed)", 0.032 / w, 0.058, 6e-4)
near("gap fraction (F-G)", 0.032 / (up_ee - lo1), 0.050, 6e-4)
# limit check: E_gamma -> m_n - m_chi for m_chi -> m_n (recoil negligible)
series("(M**2 - (M - d)**2)/(2*M)", "d", 0, 3, "d - d**2/(2*M)", domain={"M": (900, 1000)})
identity("(mn**2 - m**2)/(2*mn)", "(mn - m)*(mn + m)/(2*mn)")
print(f"   note: chi+phi variant window reaches {mn:.3f} MeV > 11Be threshold {up_11:.3f} MeV,"
      f" so 11Be -> 10Be + chi + phi is closed for m_chi + m_phi in ({up_11:.3f}, {mn:.3f}) MeV")
raise SystemExit(finish())

"""M-ENGINEER-07 (F12): trip to alpha Cen, 4.37 ly, 1e5 kg payload. Ideal photon rocket.
Start and stop at v: mass ratio = [sqrt((1+v)/(1-v))]^2 = (1+v)/(1-v) = exp(2 artanh v); 1.0833 at 0.04c.
Propellant mass-energy = (ratio - 1) m_final c^2: shell + payload (4.51e27 kg) 3.4e43 J = 5.7e22 world-years
(22.75 orders); payload alone 7.5e20 J = 1.3 world-years. Coast 4.37/0.04 = 109 yr.
1 g accelerate-half / brake-half: phi = acosh(1 + a d/(2c^2)), ship time 2(c/a)phi = 3.58 yr,
Earth time 2(c/a) sinh(phi) = 6.00 yr, ratio exp(2 phi) = 40.4, energy (ratio-1) 1e5 c^2 = 3.5e23 J.
Shell/payload bill ratio 4.5e22 (22.65 orders). SI; year = 365.25 d."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, quantity, finish
from rocket_tools import trip, relativistic_mass_ratio, G0

v = sp.symbols("v", positive=True)
identity(sp.exp(2 * sp.atanh(v)), (1 + v) / (1 - v), domain={"v": (0.001, 0.99)})
limit((1 + v) / (1 - v), "v", 0, "1")
ratio = 1.04 / 0.96
near("photon start+stop ratio at 0.04c", ratio, 1.083, 0.001)
rt = relativistic_mass_ratio(v_exhaust=c, v_final=0.04 * c) ** 2
near("rocket_tools ratio^2", rt, 1.0833, 0.001)
Ms, mp_ = 4.511e27, 1e5
Es = (ratio - 1) * (Ms + mp_) * c**2
rel("shell propellant energy (J)", Es, 3.4e43, 0.02)
rel("in world-years", Es / WORLD_YR, 5.7e22, 0.02)
near("orders over one world-year", lg(Es / WORLD_YR), 22.75, 0.02)
Ep = (ratio - 1) * mp_ * c**2
rel("payload-alone energy (J)", Ep, 7.5e20, 0.01)
near("payload-alone world-years", Ep / WORLD_YR, 1.3, 0.05)
near("coast time (yr)", 4.37 / 0.04, 109, 0.5)
d, a = 4.37 * LY, G0
phi = math.acosh(1 + a * d / (2 * c**2))
tau = 2 * (c / a) * phi / YEAR
tE = 2 * (c / a) * math.sinh(phi) / YEAR
R1g = math.exp(2 * phi)
near("1 g ship time (yr)", tau, 3.58, 0.01)
near("1 g Earth time (yr)", tE, 6.00, 0.01)
near("1 g mass ratio", R1g, 40.4, 0.2)
t = trip(distance=d, accel=a, v_exhaust=c)
print(f"  rocket_tools trip: {t}")
rel("1 g propellant energy (J)", (R1g - 1) * mp_ * c**2, 3.5e23, 0.02)
near("shell/payload bill ratio (orders)", lg(Ms / mp_), 22.65, 0.01)
quantity("4.37 ly/(0.04 c)", "109.25 yr", rel_tol=1e-3)
raise SystemExit(finish())

"""M-CONSTRAINTS-15 (F2, K12): BBN linear scaling. dYp = 0.0010 per 5 s (Yeh et al.) and 0.0010 = 0.3 sigma_obs
=> 10 s gives dYp = 0.0020 = 0.6 sigma_obs (linear in dtau for small shifts)."""
from _common import near
from math_checks import identity, finish

identity("(k*d)*2", "k*(2*d)")
dY = 0.0010 / 5 * 10
near("dYp for 10 s", dY, 0.0020, 5e-5)
near("in sigma_obs", 0.3 * dY / 0.0010, 0.6, 0.006)
raise SystemExit(finish())

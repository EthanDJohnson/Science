"""Decomposer lens: does a Fierz term (aSPECT+PERKEO III combined fit, b = -0.0181(65), lambda = -1.2724(13))
move the SM arbitration? Units: energies in units of m_e (dimensionless), lifetimes in s (SI).
Model: dGamma ~ p E (W0 - E)^2 F(Z=1,E) (1 + b m_e/E); rate factor = 1 + b <m_e/E>.
Fermi function: relativistic-approx Fermi function from the toolkit if available; also shown without it.
Beam and bottle lifetimes both measure Gamma_total, so b cannot split them; b only moves the
(lambda, Vud) prediction tau_beta.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import neutron_beta_decay as nb

W0 = nb.endpoint_W0()
print(f"W0 (endpoint total energy / m_e) = {W0:.5f}")

def avg_m_over_E(fermi):
    N = 20000
    num = den = 0.0
    for i in range(1, N):
        W = 1 + (W0 - 1) * i / N
        p = math.sqrt(W * W - 1)
        F = nb.fermi_function(W, kind=fermi) if fermi else 1.0
        w = p * W * (W0 - W) ** 2 * F
        den += w; num += w / W
    return num / den

for fk in (None, "nonrel", "rel"):
    try:
        print(f"<m_e/E> with Fermi={fk}: {avg_m_over_E(fk):.4f}")
    except Exception as e:
        print(f"Fermi={fk}: {e}")
mE = avg_m_over_E("rel")

VUD, SVUD = 0.97361, 0.00032
for lab, lam, slam, b, sb in [("A-route SM (b=0)", 1.27623, 0.00050, 0.0, 0.0),
                              ("aSPECT SM (b=0)", 1.2668, 0.0027, 0.0, 0.0),
                              ("combined PIII+aSPECT with Fierz", 1.2724, 0.0013, -0.0181, 0.0065)]:
    r = nb.tau_beta(lam, slam, VUD, SVUD, rc_set="GS2023")
    fac = 1 + b * mE
    tau = r["tau"] / fac
    s_b = r["tau"] * mE * sb / fac**2
    s = math.hypot(r["sigma"], s_b)
    print(f"{lab:34s}: tau_beta = {tau:.2f} +- {s:.2f} s (b part {s_b:.2f} s); vs BL1 887.7(2.25): {(tau-887.7)/math.hypot(s,2.25):+.2f} sigma; vs UCNtau 877.82(0.29): {(tau-877.82)/math.hypot(s,0.29):+.2f} sigma")
print("Note: a Fierz b changes Gamma_total for every method alike; it cannot make beam and bottle differ.")

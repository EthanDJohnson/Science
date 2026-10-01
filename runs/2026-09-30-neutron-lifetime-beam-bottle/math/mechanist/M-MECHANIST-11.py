"""M-MECHANIST-11 (F11, O4): SNS regeneration and other classes.
Regeneration (n -> n' -> n through an absorber) ~ P1 * P2; with equal per-passage conversion P (the
lens's ASSUMPTION), ~P^2. Limit 2.5e-8 (D-62) caps P at sqrt(2.5e-8); beam shift then tau*(1/(1-P) - 1).
Material bottle: per-bounce loss = oscillation-averaged <P> = 2 eps^2/(delta^2 + 4 eps^2) ~ 2 theta0^2 at
mu*B << Dm (valid when Dm t_f / hbar >> 1). J-PARC: both the beta rate and the 3He capture rate count
the |n> density, so the n' admixture cancels in the ratio. s, neV (SI)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, inequality, finish

P = 1.13e-2
reg = P**2
print(f"P^2 = {reg:.3e}; excess = {reg/2.5e-8:.3e}")
quantity(f"{reg}", "1.3e-4", rel_tol=0.03)
quantity(f"{reg/2.5e-8}", "5.1e3", rel_tol=0.01)
Pcap = math.sqrt(2.5e-8)
sh = 877.82 * (1 / (1 - Pcap) - 1)
print(f"P cap = {Pcap:.3e}; beam shift cap = {sh:.4f} s = {sh/10.15*100:.2f} % of gap")
quantity(f"{Pcap}", "1.6e-4", rel_tol=0.02)
quantity(f"{sh} s", "0.14 s", rel_tol=0.02)
quantity(f"{sh/10.15}", "0.014", rel_tol=0.03)
# per-bounce in a microtesla bottle
th0, Dm, hbar = 1.66e-3, 280.0, 6.582119569e-7
eps = th0 * Dm
pb = 2 * eps**2 / (Dm**2 + 4 * eps**2)
print(f"per-bounce <P> = {pb:.3e}; Dm*t_f/hbar at t_f = 0.02 s: {Dm*0.02/hbar:.2e} (>> 1: averaging valid)")
quantity(f"{pb}", "5.5e-6", rel_tol=0.01)
for nu, claim in ((5, "2.8e-5"), (50, "2.8e-4")):
    print(f"rate at {nu}/s = {pb*nu:.3e} s^-1")
    quantity(f"{pb*nu} Hz", f"{claim} Hz", rel_tol=0.02)
# J-PARC: ratio of two rates both proportional to (1 - <P>) N_n -> P cancels
identity("(1 - q)*A/((1 - q)*B)", "A/B", domain={"q": (0, 0.5)})
# even without cancellation, <P>*tau is below 0.01 s
inequality(f"{pb*877.82}", "<", "0.01")
raise SystemExit(finish())

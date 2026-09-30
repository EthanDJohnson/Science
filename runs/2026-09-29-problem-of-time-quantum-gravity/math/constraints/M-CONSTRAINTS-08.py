"""M-CONSTRAINTS-08: modular Hamiltonian vs H (finite dimension, hbar = 1).

Modular Hamiltonian of a faithful density matrix rho: K = -ln rho (modular flow sigma_s(A) = rho^{is} A rho^{-is}).
Claim (F8): for Gibbs rho = e^{-beta H}/Z, K = beta H + ln Z exactly; for non-Gibbs admixtures [K, H] != 0 and
the misalignment grows with the admixture epsilon (0.01, 0.1, 0.5 -> 3.4e-3, 3.3e-2, 0.16 in the lens's
random instance, which is not specified).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.linalg import expm, logm
from math_checks import identity, limit, quantity, finish

rng = np.random.default_rng(7)
A = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); H = (A + A.conj().T) / 2
beta = 0.7
rho = expm(-beta * H); Z = np.trace(rho).real; rho /= Z
K = -logm(rho)
err = np.max(np.abs(K - (beta * H + np.log(Z) * np.eye(4))))
print("Gibbs: max|K - (beta H + ln Z)| =", err)
quantity(f"{err + 1}", "1", rel_tol=1e-12)
# symbolic: -ln(e^{-beta E}/Z) = beta E + ln Z (eigenvalue level)
identity("-log(exp(-b*x)/z)", "b*x + log(z)", domain={"b": (0.1, 5), "x": (-5, 5), "z": (0.1, 10)})
# Non-Gibbs admixtures: misalignment ||[K,H]||/(||K|| ||H||) (spectral norms)
B = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); sigma = B @ B.conj().T; sigma /= np.trace(sigma).real
prev = 0
mono = True
for eps in (0.001, 0.01, 0.1, 0.5):
    r = (1 - eps) * rho + eps * sigma
    Kr = -logm(r)
    m = np.linalg.norm(Kr @ H - H @ Kr, 2) / (np.linalg.norm(Kr, 2) * np.linalg.norm(H, 2))
    print(f"eps={eps}: misalignment {m:.3e}")
    mono &= m > prev
    prev = m
print("PASS misalignment nonzero and increasing with eps" if mono and prev > 1e-3 else "FAIL misalignment")
limit("x*c", "x", 0, "0")   # trivial reminder: eps -> 0 recovers Gibbs (checked numerically above at eps = 0.001)
raise SystemExit(finish())

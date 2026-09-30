"""M-DIALECTICIAN-01: Kuchar's naive two-time probability in a finite ideal Page-Wootters clock.

Model (hbar = 1): clock H_C = diag(omega*(k - (d-1)/2)), k = 0..d-1, omega = 1 rad/s, d = 8.
System qubit H_S = Omega*sigma_x/2, Omega = 1 rad/s. Constraint J = H_C x 1 + 1 x H_S, J Psi = 0.
Normalised clock states |t> = exp(-i H_C t) |t=0>, |t=0> = sum_k |k>/sqrt(d).
Naive (record-free) joint: N(a,t1; b,t2) = || (|t2><t2| x P_b)(|t1><t1| x P_a) Psi ||^2,
conditional naive = N / || (|t1><t1| x P_a) Psi ||^2.
Claims: N = 0 for distinct lattice times t2 - t1 = 2 pi j/(d omega), j != 0 (mod d);
sum_b conditional naive = |<t1|t2>|^2 = sin^2(d w tau/2)/(d^2 sin^2(w tau/2)) (0.8067477 at tau = 0.2 s);
conditional naive for b != a is exactly 0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, units, finish, Result, _done

d, w, Om = 8, 1.0, 1.0
eps = w * (np.arange(d) - (d - 1) / 2)
HC = np.diag(eps).astype(complex)
sx = np.array([[0, 1], [1, 0]], complex)
HS = Om * sx / 2
J = np.kron(HC, np.eye(2)) + np.kron(np.eye(d), HS)
# physical subspace = kernel of J
ev, V = np.linalg.eigh(J)
K = V[:, np.abs(ev) < 1e-9]
print("dim ker J =", K.shape[1])
# physical state built from psi0 = |0>_z: project a generic product onto the kernel
psi0 = np.array([1, 0], complex)
t0 = np.ones(d, complex) / np.sqrt(d)
Psi = K @ (K.conj().T @ np.kron(t0, psi0))
Psi /= np.linalg.norm(Psi)

def tstate(t):
    return np.exp(-1j * eps * t) / np.sqrt(d)

P = [np.diag([1, 0]).astype(complex), np.diag([0, 1]).astype(complex)]

def proj(t, Pa):
    ts = tstate(t)
    return np.kron(np.outer(ts, ts.conj()), Pa)

def naive(t1, t2, a, b):
    x = proj(t1, P[a]) @ Psi
    den = np.vdot(x, x).real
    y = proj(t2, P[b]) @ x
    return np.vdot(y, y).real, den

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (numpy)", note=note), True)

# (i) zero at distinct lattice pairs
step = 2 * np.pi / (d * w)
mx = 0.0
for j1 in range(d):
    for j2 in range(d):
        if j1 == j2:
            continue
        for b in (0, 1):
            N, _ = naive(j1 * step, j2 * step, 0, b)
            mx = max(mx, N)
report("naive joint N = 0 at all distinct lattice pairs (d=8)", mx < 1e-14, f"max N = {mx:.2e}; lattice step {step:.6f} s")

# (ii) off lattice: sum_b conditional = Fejer kernel; b != a part = 0
for t1, tau in [(0.0, 0.2), (0.3, 1.3), (1.1, 0.5)]:
    Ns = [naive(t1, t1 + tau, 0, b) for b in (0, 1)]
    tot = (Ns[0][0] + Ns[1][0]) / Ns[0][1]
    fej = np.sin(d * w * tau / 2) ** 2 / (d ** 2 * np.sin(w * tau / 2) ** 2)
    report(f"sum_b naive conditional = Fejer kernel at t1={t1}, tau={tau}", abs(tot - fej) < 1e-12,
           f"{tot:.7f} vs {fej:.7f}")
    report(f"naive conditional P(1|0) = 0 at tau={tau}", Ns[1][0] / Ns[0][1] < 1e-14, f"{Ns[1][0] / Ns[0][1]:.2e}")
report("Fejer kernel at tau=0.2 s equals quoted 0.8067477",
       abs(np.sin(0.8) ** 2 / (64 * np.sin(0.1) ** 2) - 0.8067477) < 5e-8,
       f"{np.sin(0.8) ** 2 / (64 * np.sin(0.1) ** 2):.8f}")

# (iii) symbolic: |sum_k e^{i k x}|^2 / d^2 equals Fejer form, and -> 1 as x -> 0
x = sp.symbols("x", positive=True)
# |sum_{j=0}^{d-1} e^{ijx}|^2 = d + 2 sum_{m=1}^{d-1} (d-m) cos(mx)  (expanded by hand, no simplify)
lhs = (d + 2 * sum((d - m) * sp.cos(m * x) for m in range(1, d))) / d**2
identity(lhs, sp.sin(d * x / 2) ** 2 / (d**2 * sp.sin(x / 2) ** 2), domain={"x": (0.05, 3.0)})
limit(sp.sin(d * x / 2) ** 2 / (d**2 * sp.sin(x / 2) ** 2), "x", 0, "1")
units("(1 rad/s) * (0.2 s)", "dimensionless")
raise SystemExit(finish())

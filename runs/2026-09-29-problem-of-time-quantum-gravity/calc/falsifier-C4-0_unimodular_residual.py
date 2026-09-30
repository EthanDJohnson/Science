"""Falsifier C4-0: does unimodular time make *every* Hamiltonian constraint linear in a clock momentum?

Lattice toy of Henneaux-Teitelboim unimodular gravity (model units, hbar = 1, dimensionless).
N spatial sites. At each site i: gravity-like pair (q_i, p_i) with local "Hamiltonian density"
h_i = p_i^2/2 - U(q_i) (indefinite, like the WDW kinetic term sign issue does not matter here) and
local volume element v_i = q_i**2 (>0).  Unimodular clock: densities tau_i with momenta L_i (= Lambda at site i).
Constraints (HT form):  C_i = h_i + L_i * v_i   (linear in L_i locally)
                        D_i = L_{i+1} - L_i      (discrete  d_i Lambda = 0)
D_i generate tau_i -> tau_i - eps, tau_{i+1} -> tau_{i+1} + eps, so gauge-invariant clock = T = sum tau_i.
On D = 0, all L_i = Lambda, and C_i = 0 for all i  <=>
   (a) h_1/v_1 + Lambda = 0              (one constraint, linear in Lambda = momentum of T: Schrodinger form)
   (b) R_k = h_k/v_k - h_1/v_1 = 0, k=2..N  (N-1 residual constraints)
We check: {R_k, T} = 0 (residuals do not involve the clock); R_k is quadratic in momenta and has no
term linear in any clock momentum; {R_k, q_1} != 0 (generates a nontrivial gauge flow: the relative
sector is 'frozen', a Wheeler-DeWitt-type constraint survives); first-class check {R_2, R_3}.
"""
import sympy as sp

N = 3
q = sp.symbols('q1:%d' % (N + 1), positive=True)
p = sp.symbols('p1:%d' % (N + 1), real=True)
tau = sp.symbols('tau1:%d' % (N + 1), real=True)
L = sp.symbols('L1:%d' % (N + 1), real=True)
Lam = sp.symbols('Lambda', real=True)
U = sp.Function('U')

h = [p[i]**2 / 2 - U(q[i]) for i in range(N)]
v = [q[i]**2 for i in range(N)]
coords = list(q) + list(tau)
moms = list(p) + list(L)


def PB(f, g):
    return sp.simplify(sum(sp.diff(f, coords[j]) * sp.diff(g, moms[j]) - sp.diff(f, moms[j]) * sp.diff(g, coords[j])
                           for j in range(len(coords))))


T = sum(tau)
C = [h[i] + L[i] * v[i] for i in range(N)]
D = [L[i + 1] - L[i] for i in range(N - 1)]

print("N sites =", N)
print("Local constraints C_i linear in local L_i:", [sp.degree(sp.expand(Ci), L[i]) for i, Ci in enumerate(C)])
print("{D_i, T} (D generate zero-4-volume relabelings; T invariant):", [PB(Di, T) for Di in D])
print("{D_1, tau_1} =", PB(D[0], tau[0]), " -> individual tau_i are gauge, only T = sum tau_i is a clock")

R = [sp.simplify(h[k] / v[k] - h[0] / v[0]) for k in range(1, N)]
for k, Rk in enumerate(R, start=2):
    polyp = sp.Poly(sp.expand(Rk * v[0] * v[k - 1]), *p)
    print(f"R_{k} = {Rk}")
    print(f"   {{R_{k}, T}} = {PB(Rk, T)}   (clock absent)")
    print(f"   degree in p's = {polyp.total_degree()},  depends on any L_i or Lambda: {any(Rk.has(x) for x in list(L) + [Lam])}")
    print(f"   {{R_{k}, q_1}} = {PB(Rk, q[0])}   (nonzero -> generates gauge flow on gravity variables)")
if N >= 3:
    print("{R_2, R_3} =", sp.simplify(PB(R[0], R[1])))
print(f"Count: {N} local Hamiltonian constraints -> 1 Schrodinger equation in T + {N-1} residual WDW-type constraints")
print("Continuum N -> infinity: one clock equation, infinitely many residual constraints h(x)/sqrt q(x) = const.")

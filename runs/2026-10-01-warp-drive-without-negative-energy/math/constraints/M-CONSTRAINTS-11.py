"""M-CONSTRAINTS-11: does a kink in the shift (jump in dX, X continuous) open the identity int rho_E = 0? (F12)

Lens claim: a nonzero bulk total needs a jump in dX across a surface, which contributes a surface term
-(1/16 pi) oint [V].dS, V = X theta - (X.grad)X.
Own derivation: X continuous across a smooth surface with unit normal n => tangential derivatives are
continuous, so [d_i X_j] = n_i a_j for some vector a. Then
  [V.n] = X.n [theta] - X_i [d_i X_j] n_j = (X.n)(n.a) - (X.n)(a.n) = 0.
So a kink contributes NO surface term; only a jump in X itself could.
Numeric example: radial curl-free X = Phi'(r) r_hat with Phi' a tent (kinks at three radii):
16 pi rho_E = theta^2 - K.K = 4 Phi'' Phi'/r + 2 Phi'^2/r^2 = (2/r^2) d/dr(r Phi'^2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, finish

n1, n2, n3, a1, a2, a3, X1, X2, X3 = sp.symbols("n1 n2 n3 a1 a2 a3 X1 X2 X3", real=True)
n = sp.Matrix([n1, n2, n3]); a = sp.Matrix([a1, a2, a3]); X = sp.Matrix([X1, X2, X3])
jump = n * a.T                      # [d_i X_j] = n_i a_j
jtheta = jump.trace()
jV = X * jtheta - (jump.T * X)      # [V_j] = X_j [theta] - X_i [d_i X_j]
expr = (jV.T * n)[0]
identity(sp.expand(expr.subs(n3, sp.sqrt(1 - n1**2 - n2**2))), 0,
         domain={"n1": (-0.5, 0.5), "n2": (-0.5, 0.5), "a1": (-3, 3), "a2": (-3, 3), "a3": (-3, 3),
                 "X1": (-3, 3), "X2": (-3, 3), "X3": (-3, 3)})

# radial example: Phi' = tent between r = 2 and r = 4 (continuous, kinks at 2, 3, 4)
r = sp.symbols("r", positive=True)
up = r - 2
down = 4 - r
def bulk(piece, lo, hi):
    P1 = piece
    P2 = sp.diff(P1, r)
    rho16 = 4 * P2 * P1 / r + 2 * P1**2 / r**2
    # K eigenvalues Phi'', Phi'/r, Phi'/r ; theta = Phi'' + 2 Phi'/r
    th = P2 + 2 * P1 / r
    identity(sp.expand(th**2 - (P2**2 + 2 * P1**2 / r**2) - rho16), 0)
    return sp.integrate(rho16 / (16 * sp.pi) * 4 * sp.pi * r**2, (r, lo, hi))
tot = sp.simplify(bulk(up, 2, 3) + bulk(down, 3, 4))
pos_neg = [sp.N(bulk(up, 2, 3)), sp.N(bulk(down, 3, 4))]
print("piece totals", pos_neg, " total", tot)
identity(tot, 0)
# contrast: a JUMP in X (Phi' = 1 on (2,4), 0 outside) gives bulk total (1/2)[r Phi'^2] jumps = (2 - 4)/2 = -1 != 0,
# but then K contains a delta and rho_E a delta^2: not distributionally defined.
jumpcase = sp.integrate((2 / r**2) * sp.diff(r * 1**2, r) / (16 * sp.pi) * 4 * sp.pi * r**2, (r, 2, 4))
print("bulk total with a jump in X:", jumpcase)
quantity(f"{float(jumpcase)}", "1", rel_tol=1e-12)
raise SystemExit(finish())

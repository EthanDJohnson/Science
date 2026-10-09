"""Crux C7: (1) axisymmetric gluings are aligned; (2) shortcut band vs misalignment angle;
(3) Shapiro correction to the 2d/c window for MM mouths (order of magnitude).

Units: SI for physical constants; years / light-years with c = 1 ly/yr for the window.
Point-mouth handle model of M-DECOMPOSER-08 / falsifier-C7-0: a ray entering A along u
leaves B along R u, R in SO(3) for an orientable handle; the achronal-ANEC barrier first
acts at Delta_a = T_thru - (d/c)|e.n|, n the axis of R, e the separation direction.
"""
import numpy as np

rng = np.random.default_rng(7)


def rot(axis, ang):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def axis_of(R):
    w, v = np.linalg.eig(R)
    i = np.argmin(abs(w - 1))
    n = np.real(v[:, i])
    return n / np.linalg.norm(n)


e = np.array([1.0, 0.0, 0.0])  # mouth separation direction

# (1) Centraliser test: an axisymmetric (about e) configuration requires R Q = Q R for every
# rotation Q about e. Check: among random R in SO(3), those that commute with a generic Q_e
# all have axis along e; and the commutator norm grows with the misalignment angle.
Qe = rot(e, 0.7314)  # generic angle (not a multiple of pi)
print("(1) centraliser of rotations about e inside SO(3)")
worst_aligned = 0.0
min_comm_misaligned = np.inf
for _ in range(20000):
    ax = rng.normal(size=3)
    ang = rng.uniform(0.05, np.pi)
    R = rot(ax, ang)
    comm = np.linalg.norm(R @ Qe - Qe @ R)
    n = axis_of(R)
    alpha = np.degrees(np.arccos(min(1.0, abs(n @ e))))
    if comm < 1e-9:
        worst_aligned = max(worst_aligned, alpha)
    if alpha > 1.0:
        min_comm_misaligned = min(min_comm_misaligned, comm)
print(f"  random R tested: 20000; largest axis angle among commuting R: {worst_aligned:.3g} deg")
print(f"  smallest |[R,Q_e]| among R with axis > 1 deg from e: {min_comm_misaligned:.3g} (nonzero => not axisymmetric)")
# explicit symmetric gluings
for name, R in [("midplane mirror R=diag(1,-1,-1)", np.diag([1.0, -1, -1])),
                ("twist by 40 deg about e", rot(e, np.radians(40))),
                ("half-turn about axis perpendicular to e", rot([0, 0, 1], np.pi))]:
    comm = np.linalg.norm(R @ Qe - Qe @ R)
    n = axis_of(R)
    print(f"  {name}: |[R,Q_e]| = {comm:.3g}, axis angle to e = {np.degrees(np.arccos(min(1, abs(n @ e)))):.3g} deg")

# (2) Shortcut band left ungoverned by the conjecture, versus misalignment angle alpha.
print("(2) ungoverned one-way-shortcut band (d/c)(1 - cos alpha), MM T_thru = pi*ell, ell = 3000 ly")
ell = 3000.0
T_thru = np.pi * ell
for d in (1000.0, 3000.0):
    print(f"  d = {d:.0f} ly: Delta_s = {T_thru - d:.1f} yr, Delta_CTC = {T_thru + d:.1f} yr, window = {2*d:.0f} yr")
    for a_deg in (0.1, 1.0, 2.56, 5.0, 10.0, 30.0, 90.0):
        band = d * (1 - np.cos(np.radians(a_deg)))
        print(f"    alpha = {a_deg:5.2f} deg: band = {band:.3g} yr ({band/(2*d):.3g} of window)")
a1 = np.degrees(np.arccos(1 - 1.0 / 1000.0))
print(f"  misalignment giving a 1 yr band at d = 1000 ly: alpha = {a1:.3g} deg")

# (3) Shapiro correction: T_ext vs d/c for MM mouths (order-of-magnitude upper estimate).
G = 6.674e-11
c = 2.998e8
M = 2.0e34      # kg per mouth, dossier Q-04
r_e = 1.5e7     # m, dossier Q-01
ly = 9.4607e15  # m
yr = 3.156e7    # s
d_m = 1000 * ly
shap = 2 * (4 * G * M / c**3) * np.log(2 * d_m / r_e)  # two mouths, generous log factor
print("(3) Shapiro delay of the exterior path, MM mouths (2 x 4GM/c^3 x ln(2d/r_e))")
print(f"  4GM/c^3 = {4*G*M/c**3:.3g} s; estimate = {shap:.3g} s = {shap/yr:.3g} yr")
print(f"  fractional change of the 2d/c = 2000 yr window: {shap/yr/2000:.3g}")

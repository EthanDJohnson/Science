"""My own transcription of dossier inputs (lifetimes in s, SI). Not copied from the lens script.
Asymmetric errors: symmetrised as mean of the two sides for chi^2 (the lens's stated convention);
side-facing values kept separately for tensions. stat and sys combined in quadrature."""
import math

def q(*a):
    return math.sqrt(sum(x * x for x in a))

# D-20 BL1
BL1 = (887.7, q(1.2, 1.9))
# D-22 Sussex-ILL (unverified lead)
SUSSEX = (889.2, q(3.0, 3.8))
# D-23 J-PARC 2024: 877.2 +- 1.7 (stat) +4.0/-3.6 (sys)
JP_X, JP_STAT, JP_UP, JP_DN = 877.2, 1.7, 4.0, 3.6
JPARC = (JP_X, q(JP_STAT, (JP_UP + JP_DN) / 2))
# D-27 UCNtau 2025: 877.82 +- 0.22 +0.20/-0.17
U_X, U_STAT, U_UP, U_DN = 877.82, 0.22, 0.20, 0.17
UCNTAU = (U_X, q(U_STAT, (U_UP + U_DN) / 2))
# D-30 Ezhov 2018
EZHOV = (878.3, q(1.6, 1.0))
# D-28 Gravitrap 2018
GRAV = (881.5, q(0.7, 0.6))
# D-29 older material bottles
SER05 = (878.5, q(0.7, 0.3))
MAMBO = (880.7, q(1.3, 1.2))
STEYERL = (882.5, q(1.4, 1.5))
ARZ = (880.2, 1.2)

PROTON = {"BL1": BL1, "Sussex": SUSSEX}
ELECTRON = {"JPARC": JPARC}
MATERIAL = {"Grav": GRAV, "Ser05": SER05, "MAMBO": MAMBO, "Steyerl": STEYERL, "Arz": ARZ}
MAGNETIC = {"UCNtau": UCNTAU, "Ezhov": EZHOV}

# lambda inputs (|lambda|), D-40..D-42
LAM = {
    "PERKEO III": (1.27641, q(0.00045, 0.00033)),
    "aSPECT 2024": (1.2668, 0.0027),
    "UCNA": (1.2772, 0.0020),
    "PERKEO II": (1.2748, q(0.0008, 0.00105)),
    "PDG 2024": (1.2754, 0.0013),
    "aCORN": (1.2796, 0.0062),
}
# Vud (Gorchtein-Seng, D-43) and DeltaR^V (GS2023, D-48)
VUD, SVUD = 0.97361, 0.00032
DRV, SDRV = 0.02479, 0.00021


def wmean(d):
    xs = list(d.values())
    W = sum(1 / s ** 2 for _, s in xs)
    m = sum(x / s ** 2 for x, s in xs) / W
    chi2 = sum((x - m) ** 2 / s ** 2 for x, s in xs)
    return m, 1 / math.sqrt(W), chi2, W


def grouped(classes):
    """classes: list of dicts. returns within chi2, dof_within, between chi2, dof_between."""
    allx = {}
    for c in classes:
        allx.update(c)
    m, _, chitot, _ = wmean(allx)
    within = 0.0
    dofw = 0
    between = 0.0
    for c in classes:
        mc, sc, ch, W = wmean(c)
        within += ch
        dofw += len(c) - 1
        between += W * (mc - m) ** 2
    return within, dofw, between, len(classes) - 1, chitot

"""My own SM master-formula helpers (lifetimes in s, SI; lambda, Vud dimensionless).
tau_beta = C / (Vud^2 (1 + 3 lam^2) (1 + dRV)), C = 5024.7 s (Gorchtein-Seng 2023, D-02) or
5024.46 s (Tan, D-02/D-49); dRV = 0.02479(21) paired with superallowed Vud = 0.97361(32) (D-43, U-01)."""
import math

C_GS = 5024.7
C_TAN = 5024.46
DRV = 0.02479; DRV_E = 0.00021
VUD = 0.97361; VUD_E = 0.00032
VUS = 0.22431; VUS_E = 0.00085   # D-45 PDG average
LAM = {  # |lambda|, sigma (stat (+) sys)
    "PERKEO III": (1.27641, math.hypot(0.00045, 0.00033)),
    "UCNA": (1.2772, 0.0020),
    "PERKEO II": (1.2748, math.hypot(0.0008, 0.00105)),
    "PDG 2024": (1.2754, 0.0013),
    "aSPECT 2024": (1.2668, 0.0027),
    "aCORN": (1.2796, 0.0062),
}

def tau_beta(lam, vud=VUD, C=C_GS, drv=DRV):
    return C / (vud ** 2 * (1 + 3 * lam ** 2) * (1 + drv))

def vud_from(tau, lam, C=C_GS, drv=DRV):
    return math.sqrt(C / (tau * (1 + 3 * lam ** 2) * (1 + drv)))

def dtau_dlam(lam, tau):
    return -tau * 6 * lam / (1 + 3 * lam ** 2)

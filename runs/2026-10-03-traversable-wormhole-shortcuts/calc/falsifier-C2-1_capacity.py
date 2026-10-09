"""Falsifier C2-1: how many quanta can an SM-embedded MMP wormhole pass per transit window?

Sources (quoted in verdict C2-1):
  MMP arXiv:1807.04726 p.19: binding energy ~1/(q l_p) "is larger than the gap by a factor of q".
  MMP eq. 5.31: l = 16 r_e^3/(G q), E_min = -G q^2/(256 r_e^3)  => |E_min| * l = q/16 (hbar = c = 1).
  MM arXiv:2008.06618 p.7: number of quanta of energy ~1/l "cannot exceed a number ~ c2";
     "information per unit time (namely of the order of ~ c2 qubits per l), rather than total".
Inputs are the run's own SM-MMP rows quoted in candidates.md C2 (sub-hypothesis a).
Units: SI unless stated; hbar*c in eV*m.
"""
import math

hbar_c_eVm = 1.97326980e-7   # eV m
c = 2.99792458e8             # m/s
m_e_eV = 0.51099895e6        # eV

rows = [
    # label, |E_min| (eV), throat length l (m), stated flux q, N_eff
    ("constraints N_f=1, g=e", 113e6, 0.23, 2.1e15, 1),
    ("engineer N_eff=1, g=0.06", 4.5e6, 1.1, 4.1e14, 1),
    ("engineer N_eff=54, g=0.06", 13e9, 0.021, 4.1e14, 54),
]

print("Check |E_min| * l / (hbar c) against N_eff*q/16 (MMP eq. 5.31):")
for lab, E, l, q, N in rows:
    lhs = E * l / hbar_c_eVm
    print(f"  {lab:28s}: |E_min| l/(hbar c) = {lhs:.3e};  N q/16 = {N*q/16:.3e};  ratio = {lhs/(N*q/16):.2f}")

print("\nGap-scale quanta per window (E_gap ~ hbar c / l, MMP/MM gap of order 1/l):")
for lab, E, l, q, N in rows:
    Egap = hbar_c_eVm / l
    n = E / Egap
    t_transit = math.pi * l / c
    print(f"  {lab:28s}: E_gap = {Egap:.2e} eV; N_quanta = |E_min|/E_gap = {n:.2e}; "
          f"transit pi*l/c = {t_transit:.2e} s; rate = {n/t_transit:.2e} quanta/s")

print("\nSM exterior: lightest charged fermion is the electron (m_e c^2 = 0.511 MeV).")
print("Electron-mediated quanta per window N_e = |E_min| / (m_e c^2), and rate N_e/(pi l / c):")
for lab, E, l, q, N in rows:
    ne = E / m_e_eV
    t_transit = math.pi * l / c
    bits_per_e = math.log2(q)  # lowest partial wave degeneracy ~ q (MMP p.8: degeneracy q)
    print(f"  {lab:28s}: N_e = {ne:.2e}; rate = {ne/t_transit:.2e} electrons/s; "
          f"label capacity log2(q) = {bits_per_e:.1f} bits/electron; "
          f"bits/s <= {ne*bits_per_e/t_transit:.2e}")

print("\nMM 2020 capacity statement: ~c2 qubits per l (a RATE). For the MM human-scale row,")
print("c2 ~ N_f > 1e52 (MM quote), l = 9.42e3 yr * c / pi:")
yr = 3.15576e7
l_MM = 9.42e3 * yr * c / math.pi
print(f"  l_MM = {l_MM:.3e} m; c2 = 1e52 qubits per l/c = {l_MM/c:.3e} s -> {1e52/(l_MM/c):.2e} qubits/s")

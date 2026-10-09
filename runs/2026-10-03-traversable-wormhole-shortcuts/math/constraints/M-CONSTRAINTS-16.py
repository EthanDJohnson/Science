"""M-CONSTRAINTS-16 (F19). SI checks with unit_tools.
MM: T < hbar c/(kB l), l = 3e3 ly: 8.1e-23 K = 6.9e-27 eV; CMB/that = 3.4e22.
SM-MMP: r_e = 2e-19 m, g = e: q = 2.1e15 (M-CONSTRAINTS-10); l = 16 r_e^3/(l_P^2 q) = 0.23 m; pi l/c = 2.4 ns;
E_min = -l_P^2 q^2 hbar c/(256 r_e^3) = -1.8e-11 J = -113 MeV; extremal mouth M = r_e c^2/G = 2.7e8 kg;
T < hbar c/(kB l) = 9.9e-3 K; |E_min|/(1 kg c^2) = 2.0e-28. MM: 4.5e26 J/(1 kg c^2) = 5.0e9; /70 = 7.2e7."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

quantity("hbar*c/(kB * 3000 ly)", "8.1e-23 K", rel_tol=5e-3)
quantity("hbar*c/(3000 ly)", "6.95e-27 eV", rel_tol=5e-3)  # lens prints 6.9e-27 (truncated; 6.95e-27)
quantity("2.725 K / (hbar*c/(kB * 3000 ly))", "3.4e22", rel_tol=0.01)
q = 2e-19 * 0.3028 / (3.141592653589793**0.5 * 1.616255e-35)
print("q =", q)
quantity(f"16 * (2e-19 m)^3 / (l_P^2 * {q})", "0.232 m", rel_tol=5e-3)
quantity(f"3.14159265 * 16 * (2e-19 m)^3 / (l_P^2 * {q}) / c", "2.43 ns", rel_tol=5e-3)
quantity(f"l_P^2 * {q}^2 * hbar * c / (256 * (2e-19 m)^3)", "1.80e-11 J", rel_tol=5e-3)
quantity(f"l_P^2 * {q}^2 * hbar * c / (256 * (2e-19 m)^3)", "112.5 MeV", rel_tol=5e-3)
quantity("2e-19 m * c^2/G", "2.69e8 kg", rel_tol=3e-3)
quantity(f"hbar*c/(kB * 16 * (2e-19 m)^3 / (l_P^2 * {q}))", "9.9e-3 K", rel_tol=5e-3)
quantity(f"l_P^2 * {q}^2 * hbar * c / (256 * (2e-19 m)^3) / (1 kg * c^2)", "2.0e-28", rel_tol=0.01)
quantity("4.5e26 J / (1 kg * c^2)", "5.0e9", rel_tol=0.01)
quantity("4.5e26 J / (70 kg * c^2)", "7.2e7", rel_tol=0.01)
units(f"l_P^2 * hbar * c / (2e-19 m)^3", "energy")
raise SystemExit(finish())

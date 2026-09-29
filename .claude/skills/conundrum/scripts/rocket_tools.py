#!/usr/bin/env python3
"""Rocket and interstellar-trip calculator for /conundrum (standard library only).

Classical and relativistic rocket equations, and trips at constant proper acceleration, so that
propulsion and travel-time questions get consistent, checked numbers.

    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from rocket_tools import C, G0, LY, trip, relativistic_mass_ratio
    t = trip(distance=4.37 * LY, accel=G0, v_exhaust=C)      # accelerate halfway, then brake
    t["ship_years"], t["earth_years"], t["peak_beta"], t["mass_ratio"]
    relativistic_mass_ratio(v_exhaust=0.1 * C, v_final=0.1 * C)   # 2.73

Physics: special relativity in flat spacetime, with no gravity from stars on the way, and a
rocket whose exhaust leaves at a fixed speed v_e in the ship's frame.
    Rapidity: phi = artanh(v/c). Speeds along a line add as rapidities.
    Tsiolkovsky:           dv = v_e ln(m0/m1)
    Ackeret (relativistic): v = c tanh((v_e/c) ln(m0/m1)), so m0/m1 = exp(phi c / v_e)
    Photon rocket (v_e = c): m0/m1 = sqrt((1 + beta)/(1 - beta))
    Constant proper acceleration a, from rest, after proper (ship) time tau:
        phi = a tau / c,  v = c tanh(phi),  t = (c/a) sinh(phi),  x = (c^2/a)(cosh(phi) - 1)
A mass ratio counts everything expelled or converted. For the photon rocket it is the ideal
limit of total conversion, where the propellant's mass-energy per kg of payload is
(mass ratio - 1) c^2. Real engines at the same v_e do worse, because of engine and tank mass
and energy lost as heat.

Command line (from the project root; quantities accept units via unit_tools.py):
    python3 .claude/skills/conundrum/scripts/rocket_tools.py trip --distance "4.37 ly" --accel "1 g0" --ve "c"
    python3 .claude/skills/conundrum/scripts/rocket_tools.py trip --distance "4.37 ly" --accel "0.1 g0" --cruise "0.2 c" --ve "0.05 c"
    python3 .claude/skills/conundrum/scripts/rocket_tools.py ratio --dv "0.1 c" --ve "0.03 c"
    python3 .claude/skills/conundrum/scripts/rocket_tools.py accel --accel "1 g0" --tau "1 yr"
    python3 .claude/skills/conundrum/scripts/rocket_tools.py selftest
"""
from __future__ import annotations

import math
import sys

C = 299_792_458.0
G0 = 9.80665
YEAR = 365.25 * 86400.0
LY = C * YEAR


def _beta_ok(beta: float) -> float:
    if not -1.0 < beta < 1.0:
        raise ValueError(f"speed must be below c (beta = {beta})")
    return beta


def gamma(beta: float) -> float:
    return 1.0 / math.sqrt(1.0 - _beta_ok(beta) ** 2)


def rapidity(beta: float) -> float:
    return math.atanh(_beta_ok(beta))


def isp_to_ve(isp_seconds: float) -> float:
    """Exhaust speed from specific impulse in seconds (by definition, times standard gravity)."""
    return isp_seconds * G0


def tsiolkovsky_dv(v_exhaust: float, mass_ratio: float) -> float:
    return v_exhaust * math.log(mass_ratio)


def tsiolkovsky_mass_ratio(v_exhaust: float, dv: float) -> float:
    return math.exp(dv / v_exhaust)


def relativistic_dv(v_exhaust: float, mass_ratio: float) -> float:
    """Ackeret's relativistic rocket equation: final speed from rest."""
    return C * math.tanh(v_exhaust / C * math.log(mass_ratio))


def mass_ratio_for_rapidity(v_exhaust: float, d_rapidity: float) -> float:
    if v_exhaust <= 0 or v_exhaust > C:
        raise ValueError("exhaust speed must be in (0, c]")
    return math.exp(d_rapidity * C / v_exhaust)


def relativistic_mass_ratio(v_exhaust: float, v_final: float) -> float:
    """Mass ratio to reach v_final from rest (one burn, no braking)."""
    return mass_ratio_for_rapidity(v_exhaust, rapidity(v_final / C))


def photon_rocket_mass_ratio(beta: float) -> float:
    return math.sqrt((1 + _beta_ok(beta)) / (1 - beta))


def kinetic_energy(mass: float, beta: float) -> float:
    return (gamma(beta) - 1.0) * mass * C**2


def hyperbolic(accel: float, tau: float = None, t: float = None, x: float = None, beta: float = None) -> dict:
    """Constant proper acceleration from rest. Give exactly one of proper time tau, coordinate time t,
    distance x or speed beta; get all of them back (SI units)."""
    if accel <= 0:
        raise ValueError("acceleration must be positive")
    given = [k for k, v in (("tau", tau), ("t", t), ("x", x), ("beta", beta)) if v is not None]
    if len(given) != 1:
        raise ValueError("give exactly one of tau, t, x, beta")
    if tau is not None:
        phi = accel * tau / C
    elif t is not None:
        phi = math.asinh(accel * t / C)
    elif x is not None:
        phi = math.acosh(1 + accel * x / C**2)
    else:
        phi = rapidity(beta)
    return {"phi": phi, "tau": C * phi / accel, "t": C / accel * math.sinh(phi),
            "x": C**2 / accel * (math.cosh(phi) - 1), "beta": math.tanh(phi), "gamma": math.cosh(phi)}


def trip(distance: float, accel: float, cruise_beta: float = None, v_exhaust: float = None) -> dict:
    """Start and end at rest, `distance` apart: accelerate at `accel` (proper), coast at cruise_beta
    if given and reachable before the midpoint, then brake at the same rate. SI units in, SI and
    convenience units out."""
    if distance <= 0:
        raise ValueError("distance must be positive")
    half = hyperbolic(accel, x=distance / 2)
    if cruise_beta is None or cruise_beta >= half["beta"]:
        phi_peak, tau, t, coast = half["phi"], 2 * half["tau"], 2 * half["t"], 0.0
        profile = "accelerate to the midpoint, then brake"
    else:
        burn = hyperbolic(accel, beta=cruise_beta)
        coast = distance - 2 * burn["x"]
        coast_t = coast / (cruise_beta * C)
        phi_peak = burn["phi"]
        tau = 2 * burn["tau"] + coast_t / burn["gamma"]
        t = 2 * burn["t"] + coast_t
        profile = f"accelerate to {cruise_beta:g} c, coast {coast / LY:.3g} ly, then brake"
    out = {"profile": profile, "ship_time_s": tau, "earth_time_s": t, "ship_years": tau / YEAR,
           "earth_years": t / YEAR, "peak_beta": math.tanh(phi_peak), "peak_gamma": math.cosh(phi_peak),
           "rapidity_change": 2 * phi_peak, "coast_distance_ly": coast / LY}
    if v_exhaust is not None:
        ratio = mass_ratio_for_rapidity(v_exhaust, 2 * phi_peak)
        out["mass_ratio"] = ratio
        out["propellant_per_kg_payload"] = ratio - 1.0
        if v_exhaust == C:
            out["propellant_energy_per_kg_payload_J"] = (ratio - 1.0) * C**2
    return out


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Check against closed forms and the published 1 g table. Returns True if all pass."""
    results = []

    def check(name, got, want, rel):
        ok = abs(got - want) <= rel * abs(want)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.6g} (expected {want:.6g})")

    check("Isp 450 s -> exhaust speed (definition, g0 = 9.80665)", isp_to_ve(450), 4412.9925, 1e-12)
    check("Tsiolkovsky: dv = v_e needs mass ratio e", tsiolkovsky_mass_ratio(3000.0, 3000.0), math.e, 1e-12)
    check("Ackeret with v_e = c equals the photon rocket at 0.6 c", relativistic_mass_ratio(C, 0.6 * C), 2.0, 1e-12)
    check("relativistic equation reduces to Tsiolkovsky at low speed",
          relativistic_dv(3000.0, 5.0), tsiolkovsky_dv(3000.0, 5.0), 1e-9)
    check("kinetic energy of 1 kg at 0.6 c is c^2/4", kinetic_energy(1.0, 0.6), C**2 / 4, 1e-12)
    check("flip-and-burn at low speed matches Newton, t = 2 sqrt(D/a)",
          trip(1e9, 10.0)["earth_time_s"], 2 * math.sqrt(1e9 / 10.0), 1e-6)
    # Gibbs & Baez (updated by Koks), "The Relativistic Rocket", Usenet Physics FAQ, 1 g = 9.81 m/s^2.
    one = hyperbolic(9.81, tau=YEAR)
    check("FAQ table, 1 year of ship time: Earth time 1.19 yr", one["t"] / YEAR, 1.19, 0.01)
    check("FAQ table, 1 year of ship time: distance 0.56 ly", one["x"] / LY, 0.56, 0.01)
    check("FAQ table, 1 year of ship time: speed 0.77 c", one["beta"], 0.77, 0.01)
    two = hyperbolic(9.81, tau=2 * YEAR)
    check("FAQ table, 2 years of ship time: Earth time 3.75 yr", two["t"] / YEAR, 3.75, 0.01)
    check("FAQ table, 2 years of ship time: distance 2.90 ly", two["x"] / LY, 2.90, 0.01)
    check("FAQ: 4.3 ly with 1 g flip-and-burn takes 3.6 yr of ship time", trip(4.3 * LY, 9.81)["ship_years"], 3.6, 0.02)
    check("FAQ: 4.3 ly with 1 g flip-and-burn takes 5.9 yr of Earth time", trip(4.3 * LY, 9.81)["earth_years"], 5.9, 0.02)
    check("FAQ: 30,000 ly (galactic centre) takes 20 yr of ship time", trip(3e4 * LY, 9.81)["ship_years"], 20.0, 0.02)
    back = hyperbolic(9.81, x=one["x"])
    check("inverse round trip: distance back to proper time", back["tau"], YEAR, 1e-9)
    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _q(text: str, kind: str) -> float:
    """Parse a quantity with units via unit_tools, check its kind, return SI."""
    from unit_tools import Q
    return Q(text).expect(kind).si


def main(argv=None) -> int:
    import argparse
    sys.path.insert(0, __import__("os").path.dirname(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    tp = sub.add_parser("trip", help="start and end at rest, constant proper acceleration, optional coast")
    tp.add_argument("--distance", required=True)
    tp.add_argument("--accel", required=True)
    tp.add_argument("--cruise", help="coast speed, e.g. '0.2 c'")
    tp.add_argument("--ve", help="exhaust speed, e.g. 'c' for a photon rocket or '0.05 c'")
    tp.add_argument("--isp", type=float, help="specific impulse in seconds, instead of --ve")
    rp = sub.add_parser("ratio", help="mass ratio for a speed change from rest (one burn)")
    rp.add_argument("--dv", required=True)
    rp.add_argument("--ve")
    rp.add_argument("--isp", type=float)
    hp = sub.add_parser("accel", help="constant proper acceleration from rest")
    hp.add_argument("--accel", required=True)
    for key in ("tau", "t", "x", "beta"):
        hp.add_argument(f"--{key}")
    sub.add_parser("selftest")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "trip":
            ve = isp_to_ve(args.isp) if args.isp else (_q(args.ve, "speed") if args.ve else None)
            cruise = _q(args.cruise, "speed") / C if args.cruise else None
            r = trip(_q(args.distance, "length"), _q(args.accel, "acceleration"), cruise, ve)
            print(f"profile: {r['profile']}")
            print(f"ship time {r['ship_years']:.4g} yr; Earth time {r['earth_years']:.4g} yr; "
                  f"peak speed {r['peak_beta']:.6g} c (gamma {r['peak_gamma']:.4g})")
            if "mass_ratio" in r:
                line = f"mass ratio {r['mass_ratio']:.4g} (propellant {r['propellant_per_kg_payload']:.4g} kg per kg payload)"
                if "propellant_energy_per_kg_payload_J" in r:
                    line += f"; photon-rocket propellant energy {r['propellant_energy_per_kg_payload_J']:.3e} J per kg payload"
                print(line)
        elif args.cmd == "ratio":
            ve = isp_to_ve(args.isp) if args.isp else _q(args.ve, "speed")
            dv = _q(args.dv, "speed")
            print(f"relativistic mass ratio {relativistic_mass_ratio(ve, dv):.6g}; "
                  f"Tsiolkovsky would give {tsiolkovsky_mass_ratio(ve, dv):.6g}")
        else:
            a = _q(args.accel, "acceleration")
            kw = {}
            if args.tau:
                kw["tau"] = _q(args.tau, "time")
            if args.t:
                kw["t"] = _q(args.t, "time")
            if args.x:
                kw["x"] = _q(args.x, "length")
            if args.beta:
                kw["beta"] = float(args.beta)
            r = hyperbolic(a, **kw)
            print(f"ship time {r['tau'] / YEAR:.4g} yr; Earth time {r['t'] / YEAR:.4g} yr; distance {r['x'] / LY:.4g} ly; "
                  f"speed {r['beta']:.6g} c (gamma {r['gamma']:.4g})")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Units and dimensions for /conundrum calculations (standard library only).

Parse a quantity with units, convert it, and check its dimensions, so that a unit slip (a missing
c^2, J against W, a year in days) shows up as an error instead of a wrong answer.

    from unit_tools import Q
    ke = Q("0.5 * 1000 kg * (3 km/s)^2")
    ke.to("MJ")               # 4500.0
    ke.kind                   # 'energy'
    Q("1 J").to("W")          # raises DimensionError: energy (M L^2 T^-2) is not power (M L^2 T^-3)
    Q("G * Msun / c^2").to("km")

Syntax:
    - Numbers: 3, 2.5e8, 1/3.
    - Operators: + - * / ^ (or **) and parentheses.
    - Juxtaposition multiplies, left to right: "3 km/s" is (3 km)/s. Write "J/(kg K)", not "J/kg K".
    - SI prefixes (y z a f p n u m c d da h k M G T P E Z Y) work on SI units and eV, L, t:
      MJ, GeV, kWh, um, ns, Mt, TW.
    - "h" is the hour, as in SI; Planck's constant is h_planck, the reduced one hbar.
    - "g" is the gram; standard gravity is g0.
    - Temperatures are in kelvin only; no Celsius offsets.

Constants use CODATA 2018 values, exact where SI defines them, and match gr_tensors.py. Masses of
the Sun and planets are IAU nominal values.

Command line (from the project root):
    python3 .claude/skills/conundrum/scripts/unit_tools.py "0.5*1000 kg*(3 km/s)^2" --to MJ --expect energy
    python3 .claude/skills/conundrum/scripts/unit_tools.py "G*Msun/c^2" --to km
    python3 .claude/skills/conundrum/scripts/unit_tools.py --list
    python3 .claude/skills/conundrum/scripts/unit_tools.py selftest
"""
from __future__ import annotations

import math
import re
import sys
from fractions import Fraction

DIMS = ("M", "L", "T", "I", "Θ", "N", "J")   # mass, length, time, current, temperature, amount, luminosity


def _d(**powers) -> tuple:
    keys = {"M": 0, "L": 1, "T": 2, "I": 3, "K": 4, "N": 5, "J": 6}
    out = [0] * 7
    for k, v in powers.items():
        out[keys[k]] = Fraction(v)
    return tuple(Fraction(x) for x in out)


NONE = _d()
KINDS = {
    _d(): "dimensionless",
    _d(M=1): "mass", _d(L=1): "length", _d(T=1): "time", _d(K=1): "temperature", _d(I=1): "current",
    _d(L=2): "area", _d(L=3): "volume", _d(T=-1): "frequency", _d(L=-2): "curvature (1/length^2)",
    _d(L=1, T=-1): "speed", _d(L=1, T=-2): "acceleration", _d(T=-2): "tidal gradient (acceleration per length)",
    _d(M=1, L=1, T=-1): "momentum", _d(M=1, L=1, T=-2): "force",
    _d(M=1, L=2, T=-2): "energy", _d(M=1, L=2, T=-3): "power", _d(M=1, L=2, T=-1): "action or angular momentum",
    _d(M=1, L=-1, T=-2): "pressure or energy density", _d(M=1, L=-3): "density",
    _d(M=1, T=-3): "intensity (power per area)", _d(L=2, T=-2): "specific energy (or speed^2)",
    _d(L=2, T=-3): "specific power (power per mass)", _d(M=1, T=-1): "mass flow rate",
    _d(I=1, T=1): "charge", _d(M=1, L=2, T=-3, I=-1): "voltage", _d(M=1, T=-2, I=-1): "magnetic field",
    _d(M=1, L=2, T=-2, K=-1): "entropy or heat capacity", _d(M=-1, L=3, T=-2): "gravitational constant",
}


class DimensionError(ValueError):
    pass


def dims_text(d: tuple) -> str:
    parts = []
    for sym, p in zip(DIMS, d):
        if p:
            parts.append(sym if p == 1 else f"{sym}^{p}")
    return " ".join(parts) or "1"


def kind_of(d: tuple) -> str:
    return KINDS.get(d, "")


class Quantity:
    """A value in SI units with its dimensions. Arithmetic checks dimensions."""
    __slots__ = ("si", "dims")

    def __init__(self, si: float, dims: tuple = NONE):
        self.si, self.dims = float(si), tuple(Fraction(x) for x in dims)

    # --- arithmetic
    def _coerce(self, other):
        return other if isinstance(other, Quantity) else Quantity(other)

    def __add__(self, other):
        other = self._coerce(other)
        if other.dims != self.dims:
            raise DimensionError(f"cannot add {self._label()} and {other._label()}")
        return Quantity(self.si + other.si, self.dims)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __neg__(self):
        return Quantity(-self.si, self.dims)

    def __mul__(self, other):
        other = self._coerce(other)
        return Quantity(self.si * other.si, tuple(a + b for a, b in zip(self.dims, other.dims)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._coerce(other)
        return Quantity(self.si / other.si, tuple(a - b for a, b in zip(self.dims, other.dims)))

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __pow__(self, p):
        p = Fraction(p).limit_denominator(1000) if not isinstance(p, Fraction) else p
        return Quantity(self.si ** float(p), tuple(a * p for a in self.dims))

    # --- conversion and inspection
    def to(self, unit) -> float:
        """Value in the given units (text like 'MJ' or 'km/s', or a Quantity). Raises on mismatched dimensions."""
        target = Q(unit) if isinstance(unit, str) else unit
        if target.dims != self.dims:
            raise DimensionError(f"{self._label()} cannot be expressed in {unit} ({target._label(False)})")
        return self.si / target.si

    @property
    def kind(self) -> str:
        return kind_of(self.dims)

    def expect(self, what) -> "Quantity":
        """Check dimensions against a kind name ('energy') or a unit ('J'); returns self, or raises."""
        want = next((d for d, k in KINDS.items() if k.split(" (")[0] == what), None)
        if want is None:
            want = Q(what).dims
        if want != self.dims:
            raise DimensionError(f"expected {what} ({dims_text(want)}), got {self._label()}")
        return self

    def _label(self, with_value=True) -> str:
        k = self.kind
        body = f"{k} ({dims_text(self.dims)})" if k else dims_text(self.dims)
        return f"{self.si:.6g} SI of {body}" if with_value else body

    def __repr__(self):
        return f"Quantity({self.si!r}, {dims_text(self.dims)})"

    def __float__(self):
        if self.dims != NONE:
            raise DimensionError(f"{self._label()} is not dimensionless")
        return self.si


# ---------------------------------------------------------------- unit table
C = 299_792_458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
H_PLANCK = 6.62607015e-34
K_B = 1.380649e-23
E_CHARGE = 1.602176634e-19
DAY = 86400.0
JULIAN_YEAR = 365.25 * DAY
AU = 1.495978707e11

_BASE = {
    # name: (SI factor, dims, takes SI prefixes)
    "m": (1.0, _d(L=1), True), "g": (1e-3, _d(M=1), True), "s": (1.0, _d(T=1), True),
    "A": (1.0, _d(I=1), True), "K": (1.0, _d(K=1), True), "mol": (1.0, _d(N=1), True), "cd": (1.0, _d(J=1), True),
    "N": (1.0, _d(M=1, L=1, T=-2), True), "J": (1.0, _d(M=1, L=2, T=-2), True), "W": (1.0, _d(M=1, L=2, T=-3), True),
    "Pa": (1.0, _d(M=1, L=-1, T=-2), True), "Hz": (1.0, _d(T=-1), True), "C": (1.0, _d(I=1, T=1), True),
    "V": (1.0, _d(M=1, L=2, T=-3, I=-1), True), "ohm": (1.0, _d(M=1, L=2, T=-3, I=-2), True),
    "T": (1.0, _d(M=1, T=-2, I=-1), True), "eV": (E_CHARGE, _d(M=1, L=2, T=-2), True),
    "L": (1e-3, _d(L=3), True), "t": (1000.0, _d(M=1), True), "Wh": (3600.0, _d(M=1, L=2, T=-2), True),
    # time and astronomy
    "min": (60.0, _d(T=1), False), "h": (3600.0, _d(T=1), False), "hr": (3600.0, _d(T=1), False),
    "day": (DAY, _d(T=1), False), "yr": (JULIAN_YEAR, _d(T=1), False), "year": (JULIAN_YEAR, _d(T=1), False),
    "kyr": (1e3 * JULIAN_YEAR, _d(T=1), False), "Myr": (1e6 * JULIAN_YEAR, _d(T=1), False),
    "Gyr": (1e9 * JULIAN_YEAR, _d(T=1), False),
    "au": (AU, _d(L=1), False), "ly": (C * JULIAN_YEAR, _d(L=1), False),
    "pc": (AU * 648000 / math.pi, _d(L=1), False), "kpc": (1e3 * AU * 648000 / math.pi, _d(L=1), False),
    "Mpc": (1e6 * AU * 648000 / math.pi, _d(L=1), False),
    "Msun": (1.3271244e20 / G, _d(M=1), False), "Mearth": (3.986004e14 / G, _d(M=1), False),
    "Mjup": (1.2668653e17 / G, _d(M=1), False), "Rsun": (6.957e8, _d(L=1), False),
    "Rearth": (6.3781e6, _d(L=1), False), "Lsun": (3.828e26, _d(M=1, L=2, T=-3), False),
    # other units
    "atm": (101325.0, _d(M=1, L=-1, T=-2), False), "bar": (1e5, _d(M=1, L=-1, T=-2), False),
    "erg": (1e-7, _d(M=1, L=2, T=-2), False), "dyn": (1e-5, _d(M=1, L=1, T=-2), False),
    "cal": (4.184, _d(M=1, L=2, T=-2), False), "kcal": (4184.0, _d(M=1, L=2, T=-2), False),
    "tonTNT": (4.184e9, _d(M=1, L=2, T=-2), False), "ktTNT": (4.184e12, _d(M=1, L=2, T=-2), False),
    "MtTNT": (4.184e15, _d(M=1, L=2, T=-2), False), "gauss": (1e-4, _d(M=1, T=-2, I=-1), False),
    "angstrom": (1e-10, _d(L=1), False), "barn": (1e-28, _d(L=2), False),
    "rad": (1.0, NONE, False), "percent": (0.01, NONE, False),
    # constants
    "c": (C, _d(L=1, T=-1), False), "G": (G, _d(M=-1, L=3, T=-2), False), "hbar": (HBAR, _d(M=1, L=2, T=-1), False),
    "h_planck": (H_PLANCK, _d(M=1, L=2, T=-1), False), "kB": (K_B, _d(M=1, L=2, T=-2, K=-1), False),
    "e": (E_CHARGE, _d(I=1, T=1), False), "g0": (9.80665, _d(L=1, T=-2), False),
    "me": (9.1093837015e-31, _d(M=1), False), "mp": (1.67262192369e-27, _d(M=1), False),
    "amu": (1.66053906660e-27, _d(M=1), False), "Da": (1.66053906660e-27, _d(M=1), False),
    "eps0": (8.8541878128e-12, _d(M=-1, L=-3, T=4, I=2), False), "mu0": (1.25663706212e-6, _d(M=1, L=1, T=-2, I=-2), False),
    "sigma_SB": (5.670374419e-8, _d(M=1, T=-3, K=-4), False), "NA": (6.02214076e23, _d(N=-1), False),
    "l_P": (math.sqrt(HBAR * G / C**3), _d(L=1), False), "t_P": (math.sqrt(HBAR * G / C**5), _d(T=1), False),
    "m_P": (math.sqrt(HBAR * C / G), _d(M=1), False), "pi": (math.pi, NONE, False),
}
_PREFIXES = {"Y": 1e24, "Z": 1e21, "E": 1e18, "P": 1e15, "T": 1e12, "G": 1e9, "M": 1e6, "k": 1e3, "h": 1e2,
             "da": 1e1, "d": 1e-1, "c": 1e-2, "m": 1e-3, "u": 1e-6, "µ": 1e-6, "n": 1e-9, "p": 1e-12,
             "f": 1e-15, "a": 1e-18, "z": 1e-21, "y": 1e-24}


def unit(name: str) -> Quantity:
    if name in _BASE:
        f, d, _ = _BASE[name]
        return Quantity(f, d)
    for plen in (2, 1):
        pre, rest = name[:plen], name[plen:]
        if pre in _PREFIXES and rest in _BASE and _BASE[rest][2]:
            f, d, _ = _BASE[rest]
            return Quantity(_PREFIXES[pre] * f, d)
    raise KeyError(f"unknown unit {name!r} (see --list)")


# ---------------------------------------------------------------- parser
_TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-zµ_][A-Za-z0-9µ_]*)|(\*\*|[-+*/^()]))")


def _tokens(text: str) -> list:
    pos, out = 0, []
    text = text.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise ValueError(f"cannot parse {text[pos:]!r}")
        num, name, op = m.groups()
        out.append(("num", float(num)) if num else ("name", name) if name else ("op", "^" if op == "**" else op))
        pos = m.end()
    return out


class _Parser:
    def __init__(self, text):
        self.toks, self.i = _tokens(text), 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def parse(self) -> Quantity:
        q = self.expr()
        if self.peek()[0] is not None:
            raise ValueError(f"unexpected {self.peek()[1]!r}")
        return q

    def expr(self):
        q = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            rhs = self.term()
            q = q + rhs if op == "+" else q - rhs
        return q

    def term(self):
        q = self.power()
        while True:
            kind, val = self.peek()
            if (kind, val) in (("op", "*"), ("op", "/")):
                self.take()
                rhs = self.power()
                q = q * rhs if val == "*" else q / rhs
            elif kind in ("num", "name") or (kind, val) == ("op", "("):
                q = q * self.power()              # juxtaposition
            else:
                return q

    def power(self):
        base = self.unary()
        if self.peek() == ("op", "^"):
            self.take()
            sign = -1 if self.peek() == ("op", "-") else 1
            if sign < 0:
                self.take()
            if self.peek() == ("op", "("):
                self.take()
                exp = self.expr()
                if self.take() != ("op", ")"):
                    raise ValueError("missing ) in exponent")
                p = float(exp)
            else:
                kind, val = self.take()
                if kind != "num":
                    raise ValueError("exponent must be a number")
                p = val
            return base ** (Fraction(sign * p).limit_denominator(1000))
        return base

    def unary(self):
        if self.peek() == ("op", "-"):
            self.take()
            return -self.unary()
        return self.atom()

    def atom(self):
        kind, val = self.take()
        if kind == "num":
            return Quantity(val)
        if kind == "name":
            return unit(val)
        if (kind, val) == ("op", "("):
            q = self.expr()
            if self.take() != ("op", ")"):
                raise ValueError("missing )")
            return q
        raise ValueError(f"unexpected {val!r}")


def Q(text) -> Quantity:
    """Parse a quantity such as '3.2 GW', '0.1 c' or '1/2 * 1 kg * (0.1 c)^2'."""
    if isinstance(text, Quantity):
        return text
    if isinstance(text, (int, float)):
        return Quantity(text)
    return _Parser(str(text)).parse()


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Check against exact SI and IAU definitions and well-known values. Returns True if all pass."""
    results = []

    def check(name, got, want, rel=1e-9):
        ok = abs(got - want) <= rel * abs(want)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g})")

    def raises(name, fn):
        try:
            fn()
            ok = False
        except DimensionError:
            ok = True
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}")

    check("1 eV in J (exact SI definition)", Q("1 eV").to("J"), 1.602176634e-19)
    check("1 ly in m (IAU: c x Julian year)", Q("1 ly").to("m"), 9.4607304725808e15)
    check("1 pc in m (IAU 2015: 648000/pi au)", Q("1 pc").to("m"), 3.0856775814913673e16)
    check("1 atm in Pa (exact)", Q("1 atm").to("Pa"), 101325.0)
    check("1 kWh in J (exact)", Q("1 kWh").to("J"), 3.6e6)
    check("1 kg c^2 in J (exact c)", Q("1 kg * c^2").to("J"), 8.987551787368176e16)
    check("100 km/h in m/s", Q("100 km/h").to("m/s"), 1000 / 36)
    check("KE of 1 t at 3 km/s in MJ", Q("0.5 * 1 t * (3 km/s)^2").to("MJ"), 4500.0)
    check("G Msun / c^2 in m (half the Sun's Schwarzschild radius)", Q("G*Msun/c^2").to("m"), 1476.625, rel=1e-5)
    check("kT at 300 K in meV", Q("kB * 300 K").to("meV"), 25.852, rel=1e-4)
    check("Planck length in m (CODATA 2018)", Q("l_P").to("m"), 1.616255e-35, rel=1e-6)
    check("1 g0 for 1 yr, as a fraction of c", Q("g0 * 1 yr / c").to("1"), 1.0323, rel=1e-4)
    check("sqrt of an area", Q("(4 m^2)^(1/2)").to("m"), 2.0)
    raises("J cannot be converted to W", lambda: Q("1 J").to("W"))
    raises("m + s is refused", lambda: Q("1 m + 1 s"))
    raises("expect('power') on an energy", lambda: Q("5 J").expect("power"))
    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("expr", nargs="?", help='quantity, for example "0.5*1000 kg*(3 km/s)^2", or "selftest"')
    ap.add_argument("--to", help="units to express the result in, for example MJ")
    ap.add_argument("--expect", help="a kind (energy, power, speed ...) or a unit the result must match")
    ap.add_argument("--list", action="store_true", help="list known units and prefixes")
    args = ap.parse_args(argv)
    if args.list:
        print("units:", " ".join(sorted(_BASE, key=str.lower)))
        print("SI prefixes (on m g s A K mol cd N J W Pa Hz C V ohm T eV L t Wh):", " ".join(_PREFIXES))
        return 0
    if args.expr == "selftest":
        return 0 if selftest() else 1
    if not args.expr:
        ap.print_help()
        return 1
    try:
        q = Q(args.expr)
        if args.expect:
            q.expect(args.expect)
        if args.to:
            print(f"{args.expr} = {q.to(args.to):.6g} {args.to}   [{q._label(False)}]")
        else:
            print(f"{args.expr} = {q.si:.6g} SI   [{q._label(False)}]")
    except (DimensionError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

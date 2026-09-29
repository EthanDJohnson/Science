#!/usr/bin/env python3
"""Independent checks of mathematical claims, for the /conundrum math checker.

Each check tries SymPy symbolically first. SymPy failing to simplify proves nothing, so an
identity it can't close is then compared at many random points in mpmath at high precision, and
a sign or inequality is sampled across its domain. A check returns a Result whose status is
"pass", "fail" (with a counterexample) or "undecided", and prints one line starting with PASS,
FAIL or UNDECIDED, which math_run.py counts.

    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from math_checks import identity, limit, series, sign, inequality, quantity, units, finish
    identity("sin(x)**2 + cos(x)**2", "1")                     # PASS, symbolic
    identity("(x + 1)**2", "x**2 + 1")                         # FAIL, with the point where they differ
    identity("atan(x) + atan(1/x)", "pi/2")                    # x > 0 by default
    limit("sin(x)/x", "x", 0, "1")
    series("sqrt(1 + x)", "x", 0, 3, "1 + x/2 - x**2/8")
    sign("-(v*r)**2", "negative")
    inequality("x**2 + 1", ">=", "2*x", domain={"x": (-10, 10)})
    quantity("G*Msun/c^2", "1476.6 m", rel_tol=1e-4)           # numbers with units, via unit_tools
    units("0.5 * 1 kg * (3 m/s)^2", "energy")                  # a kind, or a unit such as "J"
    raise SystemExit(finish())                                 # prints a summary; exit 1 if any check failed

Domains and assumptions:
- A symbol with no domain is taken as positive and sampled in [0.1, 10]. Give a domain, a
  (low, high) pair, for anything that can be negative, is bounded (a speed below 1) or needs
  another range. A positive range wider than 100x is sampled evenly in its logarithm.
- Symbols in a string take their assumptions from their domain: positive when low > 0,
  nonnegative when low == 0, real otherwise. Pass SymPy expressions to keep your own symbols.
- In strings SymPy's names apply. E is Euler's number and I the imaginary unit; N, S, Q, O,
  beta, gamma and zeta are functions. For physics symbols with those names, build the expression
  from sympy.symbols in your script and pass it in. A string that uses E or I gets a note.
- Numbers are compared at 30 significant digits. Values closer than 1e-25 count as equal, so
  rescale tiny SI quantities, or check them with quantity().
- Samples include the range's two ends, so a domain is a closed interval. To leave an end out,
  move the bound in slightly (0 becomes 1e-9).
- Samples use a fixed seed, so a rerun gives the same points.

Command line (from the project root):
    python3 .claude/skills/conundrum/scripts/math_checks.py identity "(x+1)**2" "x**2 + 2*x + 1"
    python3 .claude/skills/conundrum/scripts/math_checks.py sign "x**3 - x" positive --domain x=1.5:10
    python3 .claude/skills/conundrum/scripts/math_checks.py selftest
"""
from __future__ import annotations

import math
import random
import re
import sys
from dataclasses import dataclass

import mpmath as mp
import sympy as sp

SAMPLES = 50
DPS = 30
ABS_TOL = mp.mpf("1e-25")
POSITIVE = (0.1, 10.0)
SIGNS = {"positive": lambda v: v > 0, "negative": lambda v: v < 0, "nonnegative": lambda v: v >= 0,
         "nonpositive": lambda v: v <= 0, "zero": lambda v: v == 0}
RELATIONS = {">": "positive", ">=": "nonnegative", "<": "negative", "<=": "nonpositive"}
RESULTS: list = []


@dataclass
class Result:
    status: str                     # pass | fail | undecided
    check: str                      # what was checked
    method: str                     # how it was decided
    counterexample: dict | None = None
    note: str = ""

    def __bool__(self) -> bool:
        return self.status == "pass"

    def __str__(self) -> str:
        line = f"{self.status.upper()} {self.check}: {self.method}"
        if self.counterexample:
            line += "; counterexample " + ", ".join(f"{k} = {v}" for k, v in self.counterexample.items())
        return line + (f"; {self.note}" if self.note else "")


def _done(result: Result, verbose: bool) -> Result:
    RESULTS.append(result)
    if verbose:
        print(result)
    return result


def finish(verbose: bool = True) -> int:
    """Print a summary of every check run so far; return 1 if any failed, else 0."""
    counts = {s: sum(r.status == s for r in RESULTS) for s in ("pass", "fail", "undecided")}
    if verbose:
        print(f"SUMMARY: {counts['pass']} pass, {counts['fail']} fail, {counts['undecided']} undecided")
    return 1 if counts["fail"] else 0


# ---------------------------------------------------------------- parsing and sampling
def _parse(items, domain: dict | None):
    """SymPy expressions for the inputs, with each string's symbols given their domain's assumptions."""
    domain = domain or {}
    notes = []
    parsed = []
    for item in items:
        if isinstance(item, sp.Basic):
            parsed.append(item)
            continue
        text = str(item)
        if re.search(r"(?<![A-Za-z0-9_])E(?![A-Za-z0-9_(])", text):
            notes.append("E read as Euler's number")
        if re.search(r"(?<![A-Za-z0-9_])I(?![A-Za-z0-9_(])", text):
            notes.append("I read as the imaginary unit")
        expr = sp.sympify(text)
        swap = {}
        for s in expr.free_symbols:
            lo = domain.get(s.name, POSITIVE)[0]
            swap[s] = sp.Symbol(s.name, positive=True) if lo > 0 else \
                sp.Symbol(s.name, nonnegative=True) if lo == 0 else sp.Symbol(s.name, real=True)
        parsed.append(expr.xreplace(swap))
    return parsed, "; ".join(dict.fromkeys(notes))


def _ranges(symbols, domain: dict | None) -> dict:
    return {s: tuple(float(x) for x in (domain or {}).get(s.name, POSITIVE)) for s in symbols}


def _draw(rng: random.Random, lo: float, hi: float):
    if lo > 0 and hi / lo > 100:
        return mp.mpf(math.exp(rng.uniform(math.log(lo), math.log(hi))))
    return mp.mpf(rng.uniform(lo, hi))


def _points(symbols, domain, samples: int, seed: int):
    """The sample points: the range's midpoint, its two ends (where many claims break), then random points."""
    ranges = _ranges(symbols, domain)
    rng = random.Random(seed)
    yield {s: mp.mpf((lo + hi) / 2) for s, (lo, hi) in ranges.items()}
    if symbols:
        yield {s: mp.mpf(lo) for s, (lo, hi) in ranges.items()}
        yield {s: mp.mpf(hi) for s, (lo, hi) in ranges.items()}
    for _ in range(samples - 3):
        yield {s: _draw(rng, *ranges[s]) for s in symbols}


def _evaluate(fn, point: dict, symbols):
    try:
        with mp.workdps(DPS):
            value = fn(*[point[s] for s in symbols])
        value = mp.mpc(value) if isinstance(value, (complex, mp.mpc)) else mp.mpf(value)
    except (ArithmeticError, ValueError, TypeError, OverflowError):
        return None
    if isinstance(value, mp.mpc):
        if not (mp.isfinite(value.real) and mp.isfinite(value.imag)):
            return None
        if abs(value.imag) <= ABS_TOL * max(1, abs(value.real)):
            value = value.real
    elif not mp.isfinite(value):
        return None
    return value


def _close(a, b) -> bool:
    diff = abs(a - b)
    return diff <= ABS_TOL or diff <= mp.mpf(10) ** (-(DPS // 2)) * max(abs(a), abs(b))


def _show(point: dict) -> dict:
    return {str(k): mp.nstr(v, 8) for k, v in point.items()}


def _where(symbols, domain) -> str:
    ranges = _ranges(symbols, domain)
    return ", ".join(f"{s} in [{lo:g}, {hi:g}]" for s, (lo, hi) in sorted(ranges.items(), key=lambda x: x[0].name))


def _small(expr) -> bool:
    return sp.count_ops(expr) < 400


def _numeric(exprs, symbols):
    """mpmath functions for the expressions, or the reason there can't be any."""
    if any(e.has(sp.zoo, sp.nan) for e in exprs):
        return None, "an expression is undefined (complex infinity or NaN)"
    try:
        return [sp.lambdify(symbols, e, modules="mpmath") for e in exprs], ""
    except Exception as exc:   # SymPy can't print every object as mpmath code
        return None, f"can't be evaluated numerically ({type(exc).__name__})"


# ---------------------------------------------------------------- checks
def identity(lhs, rhs, domain: dict | None = None, samples: int = SAMPLES, seed: int = 1,
             verbose: bool = True) -> Result:
    """Is lhs == rhs for every point of the domain?"""
    (a, b), note = _parse([lhs, rhs], domain)
    check = f"{a} == {b}"
    diff = a - b
    try:
        if sp.expand(diff) == 0 or (_small(diff) and sp.simplify(diff) == 0):
            return _done(Result("pass", check, "symbolic", note=note), verbose)
    except Exception:   # SymPy can fail on exotic input; fall through to numbers
        pass
    symbols = sorted(diff.free_symbols, key=lambda s: s.name)
    fns, why = _numeric([a, b], symbols)
    if fns is None:
        return _done(Result("undecided", check, why, note=note), verbose)
    fa, fb = fns
    valid = 0
    for point in _points(symbols, domain, samples, seed):
        va, vb = _evaluate(fa, point, symbols), _evaluate(fb, point, symbols)
        if va is None or vb is None:
            continue
        valid += 1
        if not _close(va, vb):
            where = _show(point) or {"(no symbols)": "-"}
            return _done(Result("fail", check, f"numeric, {_where(symbols, domain) or 'constants'}",
                                where, f"lhs = {mp.nstr(va, 10)}, rhs = {mp.nstr(vb, 10)}" +
                                (f"; {note}" if note else "")), verbose)
    if valid < max(1, samples // 2):
        return _done(Result("undecided", check, f"only {valid} of {samples} points could be evaluated",
                            note=note), verbose)
    return _done(Result("pass", check, f"numeric at {valid} points, {_where(symbols, domain) or 'constants'}",
                        note=note), verbose)


def sign(expr, expected: str, domain: dict | None = None, samples: int = SAMPLES, seed: int = 1,
         verbose: bool = True) -> Result:
    """Is expr positive, negative, nonnegative, nonpositive or zero across the domain?"""
    if expected not in SIGNS:
        raise ValueError(f"expected must be one of {', '.join(SIGNS)}")
    (e,), note = _parse([expr], domain)
    check = f"{e} is {expected}"
    symbols = sorted(e.free_symbols, key=lambda s: s.name)
    fns, why = _numeric([e], symbols)
    if fns is None:
        return _done(Result("undecided", check, why, note=note), verbose)
    fn = fns[0]
    valid = 0
    for point in _points(symbols, domain, samples, seed):
        v = _evaluate(fn, point, symbols)
        if v is None or isinstance(v, mp.mpc):
            continue
        valid += 1
        if abs(v) <= ABS_TOL and expected in ("nonnegative", "nonpositive", "zero"):
            continue
        if not SIGNS[expected](v):
            return _done(Result("fail", check, f"numeric, {_where(symbols, domain) or 'constant'}",
                                _show(point) or {"value": mp.nstr(v, 10)}, f"value {mp.nstr(v, 10)}"), verbose)
    known = {"positive": e.is_positive, "negative": e.is_negative, "nonnegative": e.is_nonnegative,
             "nonpositive": e.is_nonpositive, "zero": e.is_zero}[expected]
    if known:
        return _done(Result("pass", check, f"symbolic, {_where(symbols, domain) or 'constant'}", note=note), verbose)
    if valid < max(1, samples // 2):
        return _done(Result("undecided", check, f"only {valid} of {samples} points gave real values",
                            note=note), verbose)
    return _done(Result("pass", check, f"numeric at {valid} points, {_where(symbols, domain) or 'constant'}",
                        note=note), verbose)


def inequality(lhs, relation: str, rhs, domain: dict | None = None, samples: int = SAMPLES, seed: int = 1,
               verbose: bool = True) -> Result:
    """Does lhs <relation> rhs hold across the domain? relation is one of > >= < <=."""
    if relation not in RELATIONS:
        raise ValueError("relation must be one of > >= < <=")
    (a, b), note = _parse([lhs, rhs], domain)
    result = sign(a - b, RELATIONS[relation], domain, samples, seed, verbose=False)
    RESULTS.pop()
    result.check = f"{a} {relation} {b}"
    result.note = "; ".join(x for x in (result.note, note) if x)
    return _done(result, verbose)


def limit(expr, var: str, point, expected, direction: str = "+-", domain: dict | None = None,
          verbose: bool = True) -> Result:
    """Does expr tend to expected as var -> point? point may be "oo" or "-oo"."""
    (e, want), note = _parse([expr, expected], domain)
    x = next((s for s in e.free_symbols if s.name == var), sp.Symbol(var))
    at = sp.sympify(point)
    check = f"lim {x}->{at} of {e} == {want}"
    try:
        got = sp.limit(e, x, at, dir=direction) if at.is_finite and direction != "+-" else sp.limit(e, x, at)
    except Exception:
        got = None
    if got is not None and not got.has(sp.Limit):
        agree = identity(got, want, domain=domain, verbose=False)
        RESULTS.pop()
        status = "pass" if agree.status == "pass" else agree.status
        return _done(Result(status, check, f"symbolic limit {got}", agree.counterexample, note), verbose)
    # numeric approach toward the point, other symbols at their range midpoints
    others = {s: mp.mpf(sum(_ranges([s], domain)[s]) / 2) for s in e.free_symbols | want.free_symbols if s != x}
    fe, why = _numeric([e], [x] + list(others))
    fw, why_w = _numeric([want], list(others))
    if fe is None or fw is None:
        return _done(Result("undecided", check, why or why_w, note=note), verbose)
    try:
        with mp.workdps(DPS):
            target = fw[0](*others.values())
            steps = [mp.mpf(10) ** k for k in range(4, 13)] if at in (sp.oo, -sp.oo) else \
                [mp.mpf(10) ** -k for k in range(4, 13)]
            sgn = -1 if at == -sp.oo or direction == "-" else 1
            base = 0 if at in (sp.oo, -sp.oo) else mp.mpf(sp.N(at, DPS))
            values = [fe[0](base + sgn * h, *others.values()) for h in steps]
    except (ArithmeticError, ValueError, TypeError, OverflowError) as exc:
        return _done(Result("undecided", check, f"numeric approach failed ({type(exc).__name__})", note=note), verbose)
    if _close(values[-1], target) and _close(values[-2], target):
        return _done(Result("pass", check, "numeric approach to the point", note=note), verbose)
    return _done(Result("fail" if abs(values[-1] - values[-2]) < abs(values[-1] - target) else "undecided",
                        check, f"numeric approach reached {mp.nstr(values[-1], 10)}", note=note), verbose)


def series(expr, var: str, point, order: int, expected, domain: dict | None = None, verbose: bool = True) -> Result:
    """Does expr's expansion about point, up to (not including) var**order, equal expected?"""
    (e, want), note = _parse([expr, expected], domain)
    x = next((s for s in e.free_symbols if s.name == var), sp.Symbol(var))
    at = sp.sympify(point)
    got = sp.series(e, x, at, order).removeO()
    check = f"series of {e} about {x} = {at} to order {order} == {want}"
    diff = sp.expand(got - want)
    if diff == 0 or sp.simplify(diff) == 0:
        return _done(Result("pass", check, f"symbolic: {got}", note=note), verbose)
    first = sp.Poly(diff, x - at).terms()[-1] if diff.is_polynomial(x) else None
    detail = f"expansion is {got}" + (f"; first difference at power {first[0][0]}" if first else "")
    return _done(Result("fail", check, "symbolic", note="; ".join(x for x in (detail, note) if x)), verbose)


def quantity(expr: str, expected: str, rel_tol: float = 1e-3, verbose: bool = True) -> Result:
    """Does a quantity with units (unit_tools syntax) equal expected, in dimension and value?"""
    import unit_tools as U   # noqa: PLC0415 (the toolkit folder is on the path when this module is)
    got, want = U.Q(expr), U.Q(expected)
    check = f"{expr} == {expected}"
    if got.dims != want.dims:
        return _done(Result("fail", check, "dimensions differ", note=f"{got.kind} vs {want.kind}"), verbose)
    ok = math.isclose(got.si, want.si, rel_tol=rel_tol)
    return _done(Result("pass" if ok else "fail", check, f"within {rel_tol:g}" if ok else f"relative tolerance {rel_tol:g}",
                        note=f"{got.si:.6g} vs {want.si:.6g} (SI)"), verbose)


def units(expr: str, expected: str, verbose: bool = True) -> Result:
    """Does a unit_tools expression have the expected dimension? expected is a kind or a unit."""
    import unit_tools as U   # noqa: PLC0415
    got = U.Q(expr)
    kinds = set(U.KINDS.values())
    want_dims = next((d for d, k in U.KINDS.items() if k == expected), None) if expected in kinds else U.Q(f"1 {expected}").dims
    check = f"{expr} has the dimension of {expected}"
    ok = got.dims == want_dims
    return _done(Result("pass" if ok else "fail", check, "dimensional analysis", note="" if ok else f"it is {got.kind}"),
                 verbose)


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Known identities, limits and expansions, true and false, must come out as expected."""
    q = lambda f, *a, **k: f(*a, verbose=False, **k).status   # noqa: E731
    cases = [
        ("Pythagorean identity (symbolic)", q(identity, "sin(x)**2 + cos(x)**2", "1"), "pass"),
        ("(x+1)^2 != x^2 + 1", q(identity, "(x + 1)**2", "x**2 + 1"), "fail"),
        ("atan(x) + atan(1/x) = pi/2 for x > 0", q(identity, "atan(x) + atan(1/x)", "pi/2"), "pass"),
        ("... but not for x < 0", q(identity, "atan(x) + atan(1/x)", "pi/2", domain={"x": (-10, -0.1)}), "fail"),
        ("Lorentz factor: 1/sqrt(1-v^2) = cosh(atanh v)",
         q(identity, "1/sqrt(1 - v**2)", "cosh(atanh(v))", domain={"v": (0, 0.99)}), "pass"),
        ("exp(x) is not its quadratic Taylor polynomial", q(identity, "exp(x)", "1 + x + x**2/2"), "fail"),
        ("sin x / x -> 1 at 0", q(limit, "sin(x)/x", "x", 0, "1"), "pass"),
        ("(1 + 1/n)^n -> e", q(limit, "(1 + 1/n)**n", "n", "oo", "exp(1)"), "pass"),
        ("sqrt(1+x) = 1 + x/2 - x^2/8 + O(x^3)", q(series, "sqrt(1 + x)", "x", 0, 3, "1 + x/2 - x**2/8"), "pass"),
        ("... and not + x^2/8", q(series, "sqrt(1 + x)", "x", 0, 3, "1 + x/2 + x**2/8"), "fail"),
        ("Alcubierre-type energy density is negative",
         q(sign, "-(v**2 * rho**2) / (32 * pi * r**2) * (2*r)**2", "negative"), "pass"),
        ("x^3 - x is not positive on [-2, 2]", q(sign, "x**3 - x", "positive", domain={"x": (-2, 2)}), "fail"),
        ("AM-GM: x^2 + 1 >= 2x", q(inequality, "x**2 + 1", ">=", "2*x", domain={"x": (-10, 10)}), "pass"),
        ("sqrt(1 - v^2) < 1 fails at the end v = 0", q(inequality, "sqrt(1 - v**2)", "<", "1", domain={"v": (0, 0.9)}), "fail"),
        ("G Msun / c^2 = 1476.6 m", q(quantity, "G*Msun/c^2", "1476.6 m", rel_tol=1e-4), "pass"),
        ("kinetic energy has the dimension of energy", q(units, "0.5 * 1 kg * (3 m/s)^2", "energy"), "pass"),
        ("... and not of power", q(units, "0.5 * 1 kg * (3 m/s)^2", "W"), "fail"),
    ]
    del RESULTS[-len(cases):]
    ok = 0
    for name, got, want in cases:
        passed = got == want
        ok += passed
        if verbose:
            print(f"{'PASS' if passed else 'FAIL'}  {name}: {got} (expected {want})")
    if verbose:
        print(f"{ok}/{len(cases)} checks passed")
    return ok == len(cases)


def _domain_args(values) -> dict:
    out = {}
    for item in values or []:
        name, _, span = item.partition("=")
        lo, _, hi = span.partition(":")
        out[name] = (float(lo), float(hi))
    return out


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("identity")
    p.add_argument("lhs")
    p.add_argument("rhs")
    p.add_argument("--domain", nargs="*", help="name=low:high")
    p = sub.add_parser("sign")
    p.add_argument("expr")
    p.add_argument("expected", choices=list(SIGNS))
    p.add_argument("--domain", nargs="*", help="name=low:high")
    p = sub.add_parser("units")
    p.add_argument("expr")
    p.add_argument("expected")
    sub.add_parser("selftest")
    args = ap.parse_args(argv)
    if args.command == "selftest":
        return 0 if selftest() else 1
    if args.command == "identity":
        result = identity(args.lhs, args.rhs, _domain_args(args.domain))
    elif args.command == "sign":
        result = sign(args.expr, args.expected, _domain_args(args.domain))
    else:
        result = units(args.expr, args.expected)
    return 0 if result.status == "pass" else 1


if __name__ == "__main__":
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    sys.exit(main())

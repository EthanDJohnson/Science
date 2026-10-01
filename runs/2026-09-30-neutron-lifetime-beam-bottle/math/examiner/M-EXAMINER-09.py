"""M-EXAMINER-09: UCNtau's inverse-variance weight among the seven bottle results (F15). Weights in s^-2."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
from math_checks import identity, finish
from _inputs import *
from _h import cmp

B = {**MATERIAL, **MAGNETIC}
W = {k: 1 / s**2 for k, (_, s) in B.items()}
tot = sum(W.values())
for k, w in W.items():
    print(f"  {k}: w = {w:.3f} s^-2 ({100*w/tot:.1f}%)")
print(f"total {tot:.2f} s^-2; UCNtau share {W['UCNtau']/tot:.3f}; with sigma=0.29: {1/0.29**2:.2f} / {tot - W['UCNtau'] + 1/0.29**2:.2f}")
cmp("UCNtau weight (lens 11.9 with 0.29 s)", 1 / 0.29**2, 11.9, 0.05, "s^-2")
cmp("total weight", tot, 16.3, 0.3, "s^-2")
cmp("share (lens ~73% / three-quarters)", W["UCNtau"] / tot, 0.73, 0.01)
m, s, _, _ = wmean(B)
print(f"bottle mean {m:.3f} +- {s:.3f} s")
raise SystemExit(finish())

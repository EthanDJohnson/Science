"""M-DECOMPOSER-06: light-shell advance (F5). Reuses our own axial integrator from M-DECOMPOSER-05.py
(our script, not the lens's): +x excess at beta = 0.04 for M = 0.01 and 0.1 x 4.49e27 kg, D = 1e3 m."""
import importlib.util
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
spec = importlib.util.spec_from_file_location(
    "m05", "runs/2026-10-01-warp-drive-without-negative-energy/math/decomposer/M-DECOMPOSER-05.py")
m05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m05)
m05.run("06")
raise SystemExit(m05.finish())

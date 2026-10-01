"""M-DECOMPOSER-07: advance thresholds in beta_warp at five masses (F7 table, last column).
Reuses our own axial integrator from M-DECOMPOSER-05.py; root of the +x excess (D = 1e3 m) by brentq."""
import importlib.util
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
spec = importlib.util.spec_from_file_location(
    "m05", "runs/2026-10-01-warp-drive-without-negative-energy/math/decomposer/M-DECOMPOSER-05.py")
m05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m05)
m05.run("07")
raise SystemExit(m05.finish())

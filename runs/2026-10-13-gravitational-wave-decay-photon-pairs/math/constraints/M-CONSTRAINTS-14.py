"""M-CONSTRAINTS-14: the conversion-fraction (06), overcount/energy-corner (07) and depletion (14) checks share one
independent script with M-CONSTRAINTS-05 (same SI constants and formulas); this file re-runs it so the log sits
beside this ID. See M-CONSTRAINTS-05.py for the statement of each check."""
import runpy
runpy.run_path("runs/2026-10-13-gravitational-wave-decay-photon-pairs/math/constraints/M-CONSTRAINTS-05.py", run_name="__main__")

"""M-DIALECTICIAN-09: shift caps; runs the cap branch of my own M-DIALECTICIAN-08.py (same model, see its docstring)."""
import os, runpy
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "M-DIALECTICIAN-08.py"), init_globals={"WHICH": "M-DIALECTICIAN-09"}, run_name="__main__")

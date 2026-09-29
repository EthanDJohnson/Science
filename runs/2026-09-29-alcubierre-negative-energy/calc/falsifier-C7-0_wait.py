"""Wait (up to 280 s) for the NEC-integral run to write its 'done' marker, then print its output."""
import time

P = "runs/2026-09-29-alcubierre-negative-energy/calc/falsifier-C7-0_nec_integral.out"
t0 = time.time()
while time.time() - t0 < 280:
    with open(P) as fh:
        s = fh.read()
    if s.rstrip().endswith("done"):
        break
    time.sleep(10)
print(s)
print(f"waited {time.time()-t0:.0f}s")

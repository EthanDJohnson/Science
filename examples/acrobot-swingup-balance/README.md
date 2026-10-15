# Worked example: Acrobot swing-up and balance

The validation of the toolkit's two dynamics-and-control calculators, `rigid_body.py` and
`control_tools.py`, on the standard underactuated-control benchmark: a double pendulum with
a motor at the elbow and nothing at the shoulder, swung up from hanging and balanced at the
top.

This is **not** a `/conundrum` run. There is no dossier, no candidate slate, no refuters and
no judge. It is one script, and it exists to show that the calculators the simulator lens
depends on produce verifiable numbers — and to be the thing to read when you want to know
what "run it in closed loop and find the failure boundary" means in practice.

```
python3 examples/acrobot-swingup-balance/acrobot_demo.py
```

About three minutes. `output.txt` is the run that produced the numbers quoted below.

## What it does

| Step | What it establishes |
|---|---|
| 1. Model verification | Energy conserved to 5e-13 over 20 s unforced; the passivity identity `Mdot = C + C^T` to 3e-10; RK4 converging at order 4.00; two independent dynamics implementations agreeing to 4e-10; both small-oscillation normal-mode periods matching the linearised prediction to 0.00% |
| 2. Balance controller | The upright pose confirmed to be an equilibrium (residual 2e-15); two unstable modes at ±6.09 and ±2.24 rad/s; controllable at rank 4 but conditioned at 3259; an LQR gain, its closed-loop poles, and the loop's margins |
| 3. Region of attraction | How far off upright the balance controller recovers, direction by direction, measured by simulation |
| 4. Full run | Hanging → energy pumping → handover → balanced, with the handover time, the peak torque, and the same result at a 4× coarser step |
| 5. Failure boundary | The torque limit, the parameter error and the sensor noise at which the whole thing stops working |

## The plant, stated outright

Two uniform rods: 1 kg and 1 m for the upper link, 1 kg and 2 m for the lower, so `lc = L/2`
and `izz = m L²/12` about each rod's centre of mass. Every number is derivable rather than
asserted.

These are **not** "the" Acrobot parameters. Published sets disagree, including on which
inertia convention they quote: two papers citing the same Spong work report different
inertias ([arXiv:1201.6583](https://arxiv.org/abs/1201.6583) uses unit inertias;
[arXiv:2012.11663](https://arxiv.org/abs/2012.11663) reports I₁ = 0.2 and I₂ = 1.0). A
swing-up result is not comparable across parameter sets, so this one says which it used. The
swing-up gains (α = 1.6, kₑ = 0.035, k₁ = 250) came from a grid search in **this** plant and
mean nothing in another.

What the calculators are validated against does not depend on the parameter set:
`rigid_body.py`'s self-test compares its mass matrix, its `C·q̇` product and its gravity
torque against the Acrobot and cart-pole matrices published in Russ Tedrake's
[*Underactuated Robotics*](https://underactuated.mit.edu/acrobot.html), for randomly drawn
parameters as well as the defaults.

## The method

**Swing-up** is Spong's energy-based scheme. The total energy of the hanging Acrobot is
−24.53 J and of the upright one +24.53 J, so the controller's job is to add 49 J through a
motor that cannot push the shoulder at all. It regulates the elbow to a reference that is
proportional (through a saturating `arctan`) to the shoulder rate times the energy error, so
the elbow folds in phase with the swing and each swing adds energy. The elbow's own loop is
closed by collocated partial feedback linearisation: solve the actuated row of the
manipulator equations for the torque that realises the elbow acceleration you want.

**Balance** is LQR on the linearisation about upright, with the angle errors taken around
the circle rather than along a line.

**The handover** happens when the LQR cost-to-go falls below a threshold — which is the step
that is usually guessed and is measured here instead.

## What the run shows that is worth knowing

**The balance basin cannot be widened by tuning.** It is 15.9° in the shoulder angle, and
raising R by four orders of magnitude changes that by under 20% while the gain stays near the
same floor. The plant's unstable pole at 6.09 rad/s forces a minimum gain, so the LQR cannot
be made gentle enough to catch a sloppier arrival. The swing-up has to arrive accurately, not
merely arrive — which is why the handover threshold is the interesting parameter and not an
implementation detail.

**The basin is not a level set of the LQR cost.** The cost-to-go at its edge spans 405 to
1200 across directions, a factor of 3, because the velocity directions reach further than the
cost weights say. A cost sublevel set is still the convenient test, but it has to be set from
the smallest edge cost, not an average.

**The peak torque is a requirement.** The nominal run peaks at 18.9 N·m; swing-up still
reaches the basin down to about 8.0 N·m and never gets there below about 7.8 N·m. The
boundary is sharp.

**±10% of parameter error already costs you runs.** Perturbing every plant parameter while
the controller keeps its nominal model: 12/12 reach the basin at ±5%, 10/12 at ±10%, 9/12 at
±20%. With 12 trials the 95% intervals are 0.76–1.00, 0.55–0.95 and 0.47–0.91 — wide enough
that the ±10% and ±20% rates are not distinguishable from each other. That is the honest
statement, and it is why `robustness_sweep` returns an interval rather than a rate.

**The delay margin bounds the sample rate.** 63.7 ms, so the loop cannot be run below about
8 Hz even with no computation delay — before any of it is spent on estimation lag.

## What it does not show

That this model matches any physical Acrobot. There is no joint friction beyond viscous
damping, no actuator dynamics or torque-speed envelope, no backlash, no link flexibility, no
state estimator and no computation delay. Each of those costs margin, and the delay margin
above says how little there is to spend. Nothing here is evidence about hardware; for that the
only evidence is hardware.

That separation is the point, and the adjudication rubric enforces it: a simulation is
evidence about its model, and about reality only as far as the model is verified.

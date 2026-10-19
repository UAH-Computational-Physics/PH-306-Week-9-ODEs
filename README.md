# PH306 Week 9: ODEs

## Instructions

Complete the TODOs in `ode.py`. This is the **primary student work file**
for this assignment (there is no notebook version this week).

Every function must be solved numerically with
[`scipy.integrate.solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)
and must return the `OdeResult` object produced by `solve_ivp` directly
(except for `pendulum_comparison`, which returns a `matplotlib` `Figure`).

## Problems

### Constant Acceleration

A particle moves with constant acceleration `a`. Its velocity obeys

$$\frac{dv}{dt} = a.$$

Given the initial velocity `v0`, solve for `v(t)` over `t_span`, evaluated at
`t_eval`.

### Time Dependent Force

A particle of mass `m` experiences a force that depends only on time,
`F(t)`. Its velocity obeys

$$\frac{dv}{dt} = \frac{F(t)}{m}.$$

Given the initial velocity `v0`, solve for `v(t)`. Note that `F(t)` should accept a Python callable (function).

### Velocity Dependent (Linear) Drag

A particle of mass `m` experiences linear (viscous) drag with coefficient
`k`. Its velocity obeys

$$\frac{dv}{dt} = -\frac{k}{m} v.$$

Given the initial velocity `v0`, solve for `v(t)`.

### RC Circuit Charging

A capacitor `C` charges through a resistor `R` toward a source voltage
`V_source`. The capacitor voltage obeys

$$\frac{dV}{dt} = \frac{V_{\text{source}} - V}{RC}.$$

Given the initial capacitor voltage `V0` and source voltage `V_source`, solve for `V(t)`.

### Quadratic (Velocity-Squared) Drag

A falling body of mass `m` experiences gravity `g` and quadratic air
resistance with coefficient `c`. Its velocity obeys

$$\frac{dv}{dt} = g - \frac{c}{m} v\,|v|.$$

Given the initial velocity `v0`, solve for `v(t)`.

### Logistic Population Growth

A population `N` grows at rate `r` toward a carrying capacity `K` according
to

$$\frac{dN}{dt} = r N \left(1 - \frac{N}{K}\right).$$

Given the initial population `N0`, solve for `N(t)`.

### Damped Harmonic Oscillator

A mass `m` on a spring with stiffness `k` and damping coefficient `b`
obeys

$$m \ddot{x} + b \dot{x} + k x = 0.$$

Given the initial position `x0` and velocity `v0`, rewrite this as a
first-order system and solve for `x(t)` and `v(t)`. Return the `OdeResult`
whose `y` array has position in row 0 and velocity in row 1.

### Pendulum

A pendulum of length `L` under gravity `g` obeys the full nonlinear
equation

$$\ddot{\theta} + \frac{g}{L}\sin\theta = 0.$$

For small angles, $\sin\theta \approx \theta$, giving the linear
small-angle approximation

$$\ddot{\theta} + \frac{g}{L}\theta = 0,$$

whose exact analytic solution (for initial angle `theta0` and initial
angular velocity `omega0`) is

$$\theta(t) = \theta_0 \cos\left(\sqrt{g/L}\, t\right)
            + \omega_0 \sqrt{L/g} \sin\left(\sqrt{g/L}\, t\right).$$

Given `theta0`, `omega0`, `g`, and `L`, produce a single `matplotlib`
figure plotting all three of the following over `t_span`:

1. The exact small-angle analytic solution.
2. The small-angle approximation solved with `solve_ivp`.
3. The full nonlinear equation solved with `solve_ivp`.

Include a legend identifying each of the three curves, and return the
`Figure` object (this plot will later be compared against a reference
image using `skimage`). The figure will be checked for $\theta_0 = \pi/3$,
$\omega_0 = 0$, $g = 9.8$, and $L = 1$ over the interval from $t = 0$ to
$t = 5$. The reference image can be found in this unit's module on Canvas.

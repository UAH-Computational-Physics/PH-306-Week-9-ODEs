import os

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import ode  # noqa: E402
from skimage.color import rgb2gray  # noqa: E402
from skimage.io import imread  # noqa: E402
from skimage.metrics import structural_similarity  # noqa: E402
from skimage.transform import resize  # noqa: E402


def test_constant_acceleration_velocity():
    v0, a = 3.0, 2.0
    t_eval = np.linspace(0, 4, 50)
    sol = ode.constant_acceleration_velocity(v0, a, (0, 4), t_eval)

    assert sol.success, "solve_ivp did not report success"
    expected = v0 + a * t_eval
    assert np.allclose(sol.y[0], expected, rtol=1e-4, atol=1e-4)


def test_time_dependent_force_velocity():
    v0, m = 1.0, 2.0
    force = lambda t: 6.0 + 0.0 * t  # constant force -> dv/dt = 3
    t_eval = np.linspace(0, 3, 50)
    sol = ode.time_dependent_force_velocity(v0, m, force, (0, 3), t_eval)

    assert sol.success, "solve_ivp did not report success"
    expected = v0 + 3.0 * t_eval
    assert np.allclose(sol.y[0], expected, rtol=1e-4, atol=1e-4)


def test_linear_drag_velocity():
    v0, m, k = 10.0, 1.0, 0.5
    t_eval = np.linspace(0, 5, 50)
    sol = ode.linear_drag_velocity(v0, m, k, (0, 5), t_eval)

    assert sol.success, "solve_ivp did not report success"
    expected = v0 * np.exp(-(k / m) * t_eval)
    assert np.allclose(sol.y[0], expected, rtol=1e-3, atol=1e-3)


def test_rc_circuit_charging_voltage():
    V0, V_source, R, C = 0.0, 5.0, 1000.0, 1e-3
    t_eval = np.linspace(0, 5, 50)
    sol = ode.rc_circuit_charging_voltage(
        V0, V_source, R, C, (0, 5), t_eval
    )

    assert sol.success, "solve_ivp did not report success"
    tau = R * C
    expected = V_source + (V0 - V_source) * np.exp(-t_eval / tau)
    assert np.allclose(sol.y[0], expected, rtol=1e-3, atol=1e-3)


def test_quadratic_drag_velocity():
    v0, m, g, c = 0.0, 80.0, 9.8, 0.25
    t_eval = np.linspace(0, 10, 50)
    sol = ode.quadratic_drag_velocity(v0, m, g, c, (0, 10), t_eval)

    assert sol.success, "solve_ivp did not report success"
    v_terminal = np.sqrt(g * m / c)
    expected = v_terminal * np.tanh(g * t_eval / v_terminal)
    assert np.allclose(sol.y[0], expected, rtol=1e-3, atol=1e-2)


def test_logistic_population_growth():
    N0, r, K = 10.0, 0.5, 100.0
    t_eval = np.linspace(0, 20, 50)
    sol = ode.logistic_population_growth(N0, r, K, (0, 20), t_eval)

    assert sol.success, "solve_ivp did not report success"
    expected = K / (1.0 + ((K - N0) / N0) * np.exp(-r * t_eval))
    assert np.allclose(sol.y[0], expected, rtol=1e-3, atol=1e-2)


def test_damped_harmonic_oscillator():
    x0, v0, m, b, k = 1.0, 0.0, 1.0, 0.4, 4.0
    t_eval = np.linspace(0, 5, 50)
    sol = ode.damped_harmonic_oscillator(x0, v0, m, b, k, (0, 5), t_eval)

    assert sol.success, "solve_ivp did not report success"
    assert sol.y.shape[0] == 2, "state vector must contain position and velocity"

    gamma = b / (2 * m)
    omega0 = np.sqrt(k / m)
    omega_d = np.sqrt(omega0**2 - gamma**2)
    expected_x = np.exp(-gamma * t_eval) * (
        x0 * np.cos(omega_d * t_eval)
        + (v0 + gamma * x0) / omega_d * np.sin(omega_d * t_eval)
    )
    assert np.allclose(sol.y[0], expected_x, rtol=1e-2, atol=1e-2)


def test_pendulum_comparison():
    theta0, omega0, g, L = 0.1, 0.0, 9.8, 1.0
    t_eval = np.linspace(0, 5, 200)
    fig = ode.pendulum_comparison(theta0, omega0, g, L, (0, 5), t_eval)

    assert isinstance(fig, plt.Figure), "pendulum_comparison must return a Figure"
    assert len(fig.axes) >= 1, "figure must contain at least one axes"

    ax = fig.axes[0]
    assert len(ax.lines) == 3, "figure must plot exactly 3 solutions for comparison"

    legend = ax.get_legend()
    assert legend is not None, "figure must include a legend identifying each curve"
    assert len(legend.get_texts()) == 3

    exact = theta0 * np.cos(np.sqrt(g / L) * t_eval)
    line_data = [line.get_ydata() for line in ax.lines]
    assert any(
        np.allclose(data, exact, rtol=1e-2, atol=1e-2) for data in line_data
    ), "one curve must match the exact small-angle analytic solution"


def test_pendulum_comparison_image():
    ref_path = os.path.join(
        os.environ.get("UPLOADED_FILES", "."), "PendulumCompare.png"
    )
    if not os.path.exists(ref_path):
        pytest.skip("reference image PendulumCompare.png not found")

    theta0, omega0, g, L = np.pi/3, 0.0, 9.8, 1.0
    t_eval = np.linspace(0, 5, 200)
    fig = ode.pendulum_comparison(theta0, omega0, g, L, (0, 5), t_eval)
    fig.canvas.draw()
    img = rgb2gray(np.asarray(fig.canvas.buffer_rgba())[..., :3])

    ref = imread(ref_path)[..., :3]
    ref = rgb2gray(ref[..., :3] if ref.dtype != np.uint8 else ref / 255.0)
    img = resize(img, ref.shape, anti_aliasing=True)

    score = structural_similarity(img, ref, data_range=1.0)
    assert score > 0.9, f"figure differs from reference image (SSIM={score:.2f})"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Alcubierre-Inspired Warp Bubble Visualization
#
# Top:
#   Animated warp bubble
#
# Middle:
#   Expansion scalar spacetime diagram
#
# Bottom:
#   Illustrative exotic energy density spacetime diagram
# ============================================================

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------

X_MIN = -20
X_MAX = 20

N_X = 1200

NUM_FRAMES = 200

R = 2.0          # Bubble radius
SIGMA = 3.0      # Wall sharpness

V_S = 1.0        # Bubble velocity scaling

LIGHT_BENDING = 1.5

# ------------------------------------------------------------
# Spatial Grid
# ------------------------------------------------------------

x = np.linspace(X_MIN, X_MAX, N_X)

dx = x[1] - x[0]

# Bubble trajectory

x0_values = np.linspace(
    -12,
    12,
    NUM_FRAMES
)

# ============================================================
# Alcubierre Shape Function
# ============================================================

def shape_function(x, x0, R, sigma):
    """
    Alcubierre-style shaping function.

    Produces:
        rear wall
        flat interior
        front wall
    """

    rs = np.abs(x - x0)

    numerator = (
        np.tanh(sigma * (rs + R))
        - np.tanh(sigma * (rs - R))
    )

    denominator = (
        2.0 * np.tanh(sigma * R)
    )

    return numerator / denominator


# ============================================================
# Light Distortion
# ============================================================

def light_ray(x, f):

    return (
        x
        + LIGHT_BENDING
        * np.sin(2 * np.pi * f)
    )


# ============================================================
# Precompute Spacetime Diagrams
# ============================================================

theta_history = np.zeros(
    (NUM_FRAMES, N_X)
)

energy_history = np.zeros(
    (NUM_FRAMES, N_X)
)

print("Precomputing spacetime diagrams...")

for i, x0 in enumerate(x0_values):

    f = shape_function(
        x,
        x0,
        R,
        SIGMA
    )

    dfdx = np.gradient(
        f,
        dx
    )

    theta = V_S * dfdx

    energy = -(
        V_S ** 2
    ) * (
        dfdx ** 2
    )

    theta_history[i] = theta

    energy_history[i] = energy

print("Done.")

# ============================================================
# Determine Color Limits
# ============================================================

theta_lim = np.max(
    np.abs(theta_history)
)

energy_min = np.min(
    energy_history
)

# ============================================================
# Figure Layout
# ============================================================

fig = plt.figure(
    figsize=(13, 10)
)

gs = fig.add_gridspec(
    3,
    1,
    height_ratios=[1.2, 1, 1]
)

# ============================================================
# TOP PANEL
# ============================================================

ax1 = fig.add_subplot(gs[0])

warp_line, = ax1.plot(
    [],
    [],
    lw=3,
    label="Shape Function f"
)

light_line, = ax1.plot(
    [],
    [],
    lw=2,
    alpha=0.7,
    label="Light Rays"
)

ship, = ax1.plot(
    [],
    [],
    "ko",
    markersize=8,
    label="Spacecraft"
)

ax1.set_xlim(
    X_MIN,
    X_MAX
)

ax1.set_ylim(
    -1.8,
    2.2
)

ax1.set_ylabel(
    "Warp Geometry"
)

ax1.grid(
    alpha=0.3
)

ax1.legend()

# ============================================================
# MIDDLE PANEL
# ============================================================

ax2 = fig.add_subplot(gs[1])

theta_img = ax2.imshow(
    theta_history,
    aspect="auto",
    origin="lower",
    extent=[
        X_MIN,
        X_MAX,
        0,
        NUM_FRAMES
    ],
    cmap="coolwarm",
    vmin=-theta_lim,
    vmax=theta_lim
)

ax2.set_title(
    r"Expansion Scalar $\theta$"
)

ax2.set_ylabel(
    "Time"
)

fig.colorbar(
    theta_img,
    ax=ax2,
    label=r"$\theta$"
)

# Current time indicator

theta_marker = ax2.axhline(
    0,
    color="k",
    linestyle="--",
    lw=1.5
)

# ============================================================
# BOTTOM PANEL
# ============================================================

ax3 = fig.add_subplot(gs[2])

energy_img = ax3.imshow(
    energy_history,
    aspect="auto",
    origin="lower",
    extent=[
        X_MIN,
        X_MAX,
        0,
        NUM_FRAMES
    ],
    cmap="plasma",
    vmin=energy_min,
    vmax=0
)

ax3.set_title(
    r"Illustrative Exotic Energy Density $T_{00}$"
)

ax3.set_xlabel(
    "Spatial Coordinate x"
)

ax3.set_ylabel(
    "Time"
)

fig.colorbar(
    energy_img,
    ax=ax3,
    label=r"$T_{00}$"
)

energy_marker = ax3.axhline(
    0,
    color="blue",
    linestyle="--",
    lw=1.5
)

# ============================================================
# Animation
# ============================================================

def init():

    warp_line.set_data([], [])
    light_line.set_data([], [])

    ship.set_data([], [])

    return (
        warp_line,
        light_line,
        ship,
        theta_marker,
        energy_marker
    )


def update(frame):

    x0 = x0_values[frame]

    f = shape_function(
        x,
        x0,
        R,
        SIGMA
    )

    light = light_ray(
        x,
        f
    )

    warp_line.set_data(
        x,
        f
    )

    light_line.set_data(
        x,
        light
    )

    ship.set_data(
        [x0],
        [1.0]
    )

    theta_marker.set_ydata(
        [frame, frame]
    )

    energy_marker.set_ydata(
        [frame, frame]
    )

    ax1.set_title(
    f"Alcubierre Warp Bubble   x = {x0:.2f}",
    pad=3
)

    return (
        warp_line,
        light_line,
        ship,
        theta_marker,
        energy_marker
    )


ani = FuncAnimation(
    fig,
    update,
    frames=NUM_FRAMES,
    init_func=init,
    interval=50,
    blit=False
)

plt.tight_layout()
plt.show()

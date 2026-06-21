import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Alcubierre Warp Bubble Grid Distortion Visualization
# ============================================================

R = 2.0
sigma = 3.0
v = 1.0

z_start = -4.0
dz = 0.08
n_frames = 120

# Grid for drawing coordinate lines
y_vals = np.linspace(-6, 6, 25)
z_vals = np.linspace(-8, 8, 35)

# ============================================================
# Shape function
# ============================================================

def shape_function(r):
    return (
        np.tanh(sigma * (r + R))
        - np.tanh(sigma * (r - R))
    ) / (2 * np.tanh(sigma * R))


# ============================================================
# Simple visualization warp mapping
#
# This is NOT the Alcubierre metric itself.
# It is an illustrative deformation field chosen to
# resemble compression ahead of the bubble and expansion
# behind it.
# ============================================================

def warp_displacement(Y, Z, z0):

    r = np.sqrt(Y**2 + (Z - z0)**2)

    f = shape_function(r)

    # Compression in front / expansion behind
    displacement = -0.8 * (Z - z0) * f

    return displacement


# ============================================================
# Figure
# ============================================================

fig, ax = plt.subplots(figsize=(10, 7))

def draw_grid(z0):

    ax.clear()

    # --------------------------------------------------------
    # Horizontal lines
    # --------------------------------------------------------

    z_dense = np.linspace(-8, 8, 500)

    for y0 in y_vals:

        Y = np.full_like(z_dense, y0)

        disp = warp_displacement(Y, z_dense, z0)

        z_warped = z_dense + disp

        ax.plot(
            z_warped,
            Y,
            lw=0.8
        )

    # --------------------------------------------------------
    # Vertical lines
    # --------------------------------------------------------

    y_dense = np.linspace(-6, 6, 400)

    for z0_line in z_vals:

        Z = np.full_like(y_dense, z0_line)

        disp = warp_displacement(y_dense, Z, z0)

        z_warped = Z + disp

        ax.plot(
            z_warped,
            y_dense,
            lw=0.8
        )

    # --------------------------------------------------------
    # Bubble boundary
    # --------------------------------------------------------

    circle = plt.Circle(
        (z0, 0),
        R,
        fill=False,
        color='black',
        linewidth=2.5
    )

    ax.add_patch(circle)

    # Bubble center

    ax.plot(
        z0,
        0,
        'ko',
        markersize=6
    )

    # Motion trail

    ax.plot(
        np.linspace(z_start, z0, 300),
        np.zeros(300),
        'k--',
        alpha=0.3
    )

    # Labels

    ax.set_xlim(-8, 8)
    ax.set_ylim(-6, 6)

    ax.set_aspect('equal')

    ax.set_xlabel("z")
    ax.set_ylabel("y")

    ax.set_title(
        "Illustrative Warp-Bubble Grid Distortion"
    )

    ax.text(
        0.02,
        0.98,
        (
            "Compressed grid ahead\n"
            "Expanded grid behind\n\n"
            "Conceptual visualization"
        ),
        transform=ax.transAxes,
        va='top',
        bbox=dict(
            boxstyle='round',
            facecolor='white',
            alpha=0.85
        )
    )

    return []


def update(frame):

    z0 = z_start + frame * dz

    draw_grid(z0)

    return []


ani = FuncAnimation(
    fig,
    update,
    frames=n_frames,
    interval=40,
    blit=False
)

plt.tight_layout()
plt.show()

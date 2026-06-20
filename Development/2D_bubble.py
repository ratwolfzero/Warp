import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Warp bubble parameters
R = 2.0          # bubble radius
sigma = 3.0      # wall sharpness
v = 1.0          # bubble velocity

# Grid
y = np.linspace(-6, 6, 120)
z = np.linspace(-8, 8, 160)
Y, Z = np.meshgrid(y, z)

def shape_function(r):
    return (
        np.tanh(sigma * (r + R))
        - np.tanh(sigma * (r - R))
    ) / (2 * np.tanh(sigma * R))

def dfdR(r):
    denom = 2 * np.tanh(sigma * R)

    term1 = sigma / np.cosh(sigma * (r + R))**2
    term2 = sigma / np.cosh(sigma * (r - R))**2

    return (term1 - term2) / denom

fig, ax = plt.subplots(figsize=(8, 6))

def update(frame):
    ax.clear()

    z0 = -4 + frame * 0.1

    r = np.sqrt(Y**2 + (Z - z0)**2)

    dfdr = dfdR(r)

    # Expansion scalar from paper Eq. (4)
    theta = v * (Z - z0) / np.maximum(r, 1e-8) * dfdr

    im = ax.contourf(
        Z, Y, theta,
        levels=60,
        cmap='RdBu_r'
    )

    # Bubble boundary
    circle = plt.Circle(
        (z0, 0),
        R,
        fill=False,
        color='black',
        linewidth=2
    )
    ax.add_patch(circle)

    ax.set_xlim(-8, 8)
    ax.set_ylim(-6, 6)

    ax.set_xlabel("z")
    ax.set_ylabel("y")
    ax.set_title("Alcubierre Warp Bubble")

    return [im]

ani = FuncAnimation(
    fig,
    update,
    frames=80,
    interval=50,
    blit=False
)

plt.show()

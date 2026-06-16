import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Alcubierre-Inspired Warp Bubble Visualization
# ============================================================
# Physically improved with:
#   - Correct expansion scalar (θ = -V_S * df/dx)
#   - Exotic energy density ∝ -(V_S df/dx)²
#   - Light ray dragging from shift vector
#   + Added: second light ray, shift vector curve, animated profiles
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
V_S = 1.0        # Bubble velocity (c = 1)

# Light bending factor: how strongly rays are dragged forward
LIGHT_DRAG = 2.0   # physical: Δx ∝ V_S * f(x)

# ------------------------------------------------------------
# Spatial Grid
# ------------------------------------------------------------
x = np.linspace(X_MIN, X_MAX, N_X)
dx = x[1] - x[0]

x0_values = np.linspace(-12, 12, NUM_FRAMES)

# ============================================================
# Alcubierre Shape Function (standard)
# ============================================================
def shape_function(x, x0, R, sigma):
    rs = np.abs(x - x0)
    numerator = np.tanh(sigma * (rs + R)) - np.tanh(sigma * (rs - R))
    denominator = 2.0 * np.tanh(sigma * R)
    return numerator / denominator

# ============================================================
# Physically Based Light Ray Distortion
# ============================================================
def light_ray(x, f):
    """
    Simulate the dragging of light by the warp bubble.
    In the Alcubierre metric, the effective coordinate speed of light
    is c_eff = 1 - V_S * f(x). This leads to a forward shift inside
    the bubble proportional to V_S * f.
    """
    return x + LIGHT_DRAG * V_S * f

# ============================================================
# Precompute Spacetime Diagrams
# ============================================================
theta_history = np.zeros((NUM_FRAMES, N_X))
energy_history = np.zeros((NUM_FRAMES, N_X))

print("Precomputing spacetime diagrams with improved physics...")

for i, x0 in enumerate(x0_values):
    f = shape_function(x, x0, R, SIGMA)
    dfdx = np.gradient(f, dx)

    # Correct expansion scalar: θ = -V_S * ∂f/∂x
    theta = -V_S * dfdx
    theta_history[i] = theta

    # Exotic energy density: T₀₀ ∝ - (V_S ∂f/∂x)²
    energy = - (V_S * dfdx) ** 2
    energy_history[i] = energy

print("Done.")

# ============================================================
# Determine Color Limits
# ============================================================
theta_lim = np.max(np.abs(theta_history))
energy_min = np.min(energy_history)   # negative, so vmin = energy_min, vmax = 0

# ============================================================
# Figure Layout
# ============================================================
fig = plt.figure(figsize=(13, 10))
gs = fig.add_gridspec(3, 1, height_ratios=[1.2, 1, 1])

# --- Top panel: Warp bubble, light rays, and shift vector ---
ax1 = fig.add_subplot(gs[0])
warp_line, = ax1.plot([], [], lw=3, label="Shape Function f")
light_line1, = ax1.plot([], [], lw=2, alpha=0.7, label="Light ray 1 (dragged)")
light_line2, = ax1.plot([], [], 'r--', lw=1.5, alpha=0.5, label="Light ray 2 (offset)")
shift_line, = ax1.plot([], [], 'g--', lw=1.5, alpha=0.8, label=r"Shift $\beta = -V_s f$")
ship, = ax1.plot([], [], "ko", markersize=8, label="Spacecraft")
ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(-1.8, 2.2)
ax1.set_ylabel("Warp Geometry")
ax1.grid(alpha=0.3)
ax1.legend(loc="upper left")

# --- Middle panel: Expansion scalar spacetime diagram ---
ax2 = fig.add_subplot(gs[1])
theta_img = ax2.imshow(theta_history, aspect="auto", origin="lower",
                       extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                       cmap="coolwarm", vmin=-theta_lim, vmax=theta_lim)
ax2.set_title(r"Expansion Scalar $\theta = -V_S \partial f/\partial x$")
ax2.set_ylabel("Time")
fig.colorbar(theta_img, ax=ax2, label=r"$\theta$")
theta_marker = ax2.axhline(0, color="k", linestyle="--", lw=1.5)
# Animated profile line for current θ
theta_profile, = ax2.plot(x, theta_history[0, :], 'k-', lw=1, alpha=0.8)

# --- Bottom panel: Exotic energy density spacetime diagram ---
ax3 = fig.add_subplot(gs[2])
energy_img = ax3.imshow(energy_history, aspect="auto", origin="lower",
                        extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                        cmap="plasma", vmin=energy_min, vmax=0)
ax3.set_title(r"Exotic Energy Density $T_{00} \propto -(V_S \partial f/\partial x)^2$")
ax3.set_xlabel("Spatial Coordinate x")
ax3.set_ylabel("Time")
fig.colorbar(energy_img, ax=ax3, label=r"$T_{00}$ (negative)")
energy_marker = ax3.axhline(0, color="blue", linestyle="--", lw=1.5)
# Animated profile line for current energy
energy_profile, = ax3.plot(x, energy_history[0, :], 'y-', lw=1, alpha=0.8)

# ============================================================
# Animation
# ============================================================
def init():
    warp_line.set_data([], [])
    light_line1.set_data([], [])
    light_line2.set_data([], [])
    shift_line.set_data([], [])
    ship.set_data([], [])
    theta_profile.set_data([], [])
    energy_profile.set_data([], [])
    # markers keep their initial positions
    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_marker, energy_marker, theta_profile, energy_profile)

def update(frame):
    x0 = x0_values[frame]
    f = shape_function(x, x0, R, SIGMA)

    # Top panel: shape function, light rays, shift vector
    warp_line.set_data(x, f)

    # First light ray (no offset)
    light1 = light_ray(x, f)
    light_line1.set_data(x, light1)

    # Second light ray (offset by +0.5 to distinguish)
    light2 = light_ray(x, f) + 0.5
    light_line2.set_data(x, light2)

    # Shift vector β = -V_s * f(x)
    beta = -V_S * f
    shift_line.set_data(x, beta)

    ship.set_data([x0], [1.0])

    # Mark current time in the spacetime diagrams
    theta_marker.set_ydata([frame, frame])
    energy_marker.set_ydata([frame, frame])

    # Animated profiles: show θ and energy at current time
    theta_profile.set_data(x, theta_history[frame, :])
    energy_profile.set_data(x, energy_history[frame, :])

    ax1.set_title(f"Alcubierre Warp Bubble   x = {x0:.2f}", pad=3)

    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_marker, energy_marker, theta_profile, energy_profile)

ani = FuncAnimation(fig, update, frames=NUM_FRAMES, init_func=init,
                    interval=50, blit=False)

plt.tight_layout()
plt.show()

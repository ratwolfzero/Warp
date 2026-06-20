import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Alcubierre Warp Bubble Visualization
# ============================================================


X_MIN = -20
X_MAX = 20
N_X = 1200
NUM_FRAMES = 200

R = 2.0          # Bubble radius
SIGMA = 3.0      # Wall sharpness
V_S = 1.0        # Bubble velocity (c = 1)
LIGHT_DRAG = 2.0 # Visual multiplier for light dragging

x = np.linspace(X_MIN, X_MAX, N_X)
dx = x[1] - x[0]
x0_values = np.linspace(-12, 12, NUM_FRAMES)

def shape_function(rs, R, sigma):
    """Alcubierre shape function f(rs)."""
    numerator = np.tanh(sigma * (rs + R)) - np.tanh(sigma * (rs - R))
    denominator = 2.0 * np.tanh(sigma * R)
    return numerator / denominator

def light_ray(x, f):
    """Simulate the positional dragging of light by the warp bubble."""
    return x + LIGHT_DRAG * V_S * f

theta_history = np.zeros((NUM_FRAMES, N_X))
energy_history = np.zeros((NUM_FRAMES, N_X))

print("Precomputing spacetime diagrams...")

for i, x0 in enumerate(x0_values):
    # On-axis calculations (rho = 0)
    rs_on = np.abs(x - x0)
    f_on = shape_function(rs_on, R, SIGMA)
    dfdx = np.gradient(f_on, dx)

    # 1. Expansion scalar (Expansion behind, contraction in front)
    theta = V_S * dfdx
    theta_history[i] = theta

    # 2. Exotic energy density evaluated at the off-axis torus (rho = R)
    rho = R
    rs_off = np.sqrt((x - x0)**2 + rho**2)
    f_off = shape_function(rs_off, R, SIGMA)
    
    df_dx_off = np.gradient(f_off, dx)
    drs_dx = (x - x0) / (rs_off + 1e-15) 
    df_drs = df_dx_off / (drs_dx + 1e-15)
    
    energy = - (V_S**2 * rho**2) / (4.0 * rs_off**2) * (df_drs)**2
    energy_history[i] = energy

print("Done.")

theta_lim = np.max(np.abs(theta_history))
energy_min = np.min(energy_history)

fig = plt.figure(figsize=(13, 10))
gs = fig.add_gridspec(3, 1, height_ratios=[1.2, 1, 1])

# --- Top panel: Warp bubble, Light Rays, and Shift Vector ---
ax1 = fig.add_subplot(gs[0])
warp_line, = ax1.plot([], [], lw=3, label="Shape Function f")
light_line1, = ax1.plot([], [], lw=2, alpha=0.7, label="Light ray 1 (dragged)")
light_line2, = ax1.plot([], [], 'r--', lw=1.5, alpha=0.5, label="Light ray 2 (offset)")
shift_line, = ax1.plot([], [], 'g--', lw=1.5, alpha=0.8, label="Shift vector beta")
ship, = ax1.plot([], [], "ko", markersize=8, label="Spacecraft")
ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(-2.2, 2.2)
ax1.set_ylabel("Warp Geometry")
ax1.grid(alpha=0.3)
ax1.legend(loc="upper left")

# --- Middle panel: Expansion scalar spacetime diagram ---
ax2 = fig.add_subplot(gs[1])
theta_img = ax2.imshow(theta_history, aspect="auto", origin="lower",
                       extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                       cmap="coolwarm", vmin=-theta_lim, vmax=theta_lim)
ax2.set_title("Expansion Scalar theta (Expansion > 0, Contraction < 0)")
ax2.set_ylabel("Time")
fig.colorbar(theta_img, ax=ax2, label="theta")
theta_marker = ax2.axhline(0, color="k", linestyle="--", lw=1.5)
theta_profile, = ax2.plot(x, theta_history[0, :], 'k-', lw=1, alpha=0.8)

# --- Bottom panel: Exotic energy density spacetime diagram ---
ax3 = fig.add_subplot(gs[2])
energy_img = ax3.imshow(energy_history, aspect="auto", origin="lower",
                        extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                        cmap="plasma", vmin=energy_min, vmax=0)
ax3.set_title("Exotic Energy Density T_00 (Evaluated at off-axis torus rho=R)")
ax3.set_xlabel("Spatial Coordinate x")
ax3.set_ylabel("Time")
fig.colorbar(energy_img, ax=ax3, label="T_00 (negative)")
energy_marker = ax3.axhline(0, color="blue", linestyle="--", lw=1.5)
energy_profile, = ax3.plot(x, energy_history[0, :], 'y-', lw=1, alpha=0.8)

def init():
    warp_line.set_data([], [])
    light_line1.set_data([], [])
    light_line2.set_data([], [])
    shift_line.set_data([], [])
    ship.set_data([], [])
    theta_profile.set_data([], [])
    energy_profile.set_data([], [])
    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_marker, energy_marker, theta_profile, energy_profile)

def update(frame):
    x0 = x0_values[frame]
    rs_on = np.abs(x - x0)
    f = shape_function(rs_on, R, SIGMA)

    # Top panel visuals
    warp_line.set_data(x, f)
    
    # Dragged light rays
    light1 = light_ray(x, f)
    light_line1.set_data(x, light1)
    
    light2 = light_ray(x, f) + 0.5
    light_line2.set_data(x, light2)

    # Shift vector
    beta = -V_S * f
    shift_line.set_data(x, beta)
    ship.set_data([x0], [1.0])

    # Markers and profiles for the bottom graphs
    theta_marker.set_ydata([frame, frame])
    energy_marker.set_ydata([frame, frame])
    theta_profile.set_data(x, theta_history[frame, :])
    energy_profile.set_data(x, energy_history[frame, :])

    ax1.set_title(f"Alcubierre Warp Bubble   x = {x0:.2f}", pad=3)

    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_marker, energy_marker, theta_profile, energy_profile)

ani = FuncAnimation(fig, update, frames=NUM_FRAMES, init_func=init,
                    interval=50, blit=False)

plt.tight_layout()

#ani.save('warp_drive_animation.gif', writer='pillow', fps=20, dpi=100)

plt.show()

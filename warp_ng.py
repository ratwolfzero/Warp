import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Alcubierre Warp Bubble Visualization - Cleaned 1D Version
# ============================================================

# Parameters
X_MIN = -20.0
X_MAX = 20.0
N_X = 800
NUM_FRAMES = 150
R = 2.0
SIGMA = 3.0
V_S = 1.0
LIGHT_DRAG = 2.0

x = np.linspace(X_MIN, X_MAX, N_X)
dx = x[1] - x[0]
x0_values = np.linspace(-12, 12, NUM_FRAMES)

def shape_function(rs, R, sigma):
    numerator = np.tanh(sigma * (rs + R)) - np.tanh(sigma * (rs - R))
    denominator = 2.0 * np.tanh(sigma * R)
    return numerator / denominator

def light_ray(x, f):
    return x + LIGHT_DRAG * V_S * f

print("Precomputing spacetime diagrams...")

theta_history = np.zeros((NUM_FRAMES, N_X))
energy_history = np.zeros((NUM_FRAMES, N_X))

for i, x0 in enumerate(x0_values):
    # Expansion Scalar (Panel 2)
    rs_on = np.abs(x - x0)
    f_on = shape_function(rs_on, R, SIGMA)
    dfdx = np.gradient(f_on, dx)
    theta = V_S * dfdx
    theta[np.abs(theta) < 1e-8] = 0.0
    theta_history[i] = theta

    # Exotic Energy Density (Panel 3)
    rho = R
    rs_off = np.sqrt((x - x0)**2 + rho**2)
    f_off = shape_function(rs_off, R, SIGMA)
    df_drs = np.gradient(f_off, rs_off)
    energy = - (V_S**2 * rho**2) / (4.0 * rs_off**2) * (df_drs)**2
    energy_history[i] = energy

print("Precomputation done.")

theta_lim = np.max(np.abs(theta_history))
energy_min = np.min(energy_history)

fig = plt.figure(figsize=(13, 10.5))
gs = fig.add_gridspec(3, 1, height_ratios=[1.25, 1, 1])

# Top panel
ax1 = fig.add_subplot(gs[0])
warp_line, = ax1.plot([], [], 'b-', lw=3, label="Shape Function f(rs)")
light_line1, = ax1.plot([], [], 'c-', lw=2, alpha=0.8, label="Light ray (dragged)")
light_line2, = ax1.plot([], [], 'r--', lw=1.8, alpha=0.6, label="Light ray (offset)")
shift_line, = ax1.plot([], [], 'g--', lw=1.8, alpha=0.85, label="Shift vector β")
ship, = ax1.plot([], [], "ko", markersize=10, label="Spacecraft")

ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(-2.3, 2.3)
ax1.set_ylabel("Warp Geometry")
ax1.grid(alpha=0.3)
ax1.legend(loc="upper left", fontsize=9)

# Middle panel - Expansion Scalar
ax2 = fig.add_subplot(gs[1])
theta_img = ax2.imshow(theta_history, aspect="auto", origin="lower",
                       extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                       cmap="coolwarm", vmin=-theta_lim, vmax=theta_lim)
ax2.set_title("Expansion Scalar θ\n"
              "Blue = Space Expansion (behind bubble) | Red = Space Contraction (in front)\n"
              "Diagonal bands = moving warp effect", fontsize=11)
ax2.set_ylabel("Time (frames)")
fig.colorbar(theta_img, ax=ax2, label="θ")
theta_marker = ax2.axhline(0, color="k", linestyle="--", lw=1.5)
theta_profile, = ax2.plot(x, theta_history[0, :], 'r-', lw=2.5, alpha=0.95)

# Bottom panel - Exotic Energy
ax3 = fig.add_subplot(gs[2])
energy_img = ax3.imshow(energy_history, aspect="auto", origin="lower",
                        extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                        cmap="plasma", vmin=energy_min, vmax=0)
ax3.set_title("Exotic Energy Density T₀₀ (at bubble wall ρ=R)\n"
              "Dark purple = Strong negative energy (required for warp bubble)\n"
              "Diagonal band = moving negative-energy torus", fontsize=11)
ax3.set_xlabel("Spatial Coordinate x")
ax3.set_ylabel("Time (frames)")
fig.colorbar(energy_img, ax=ax3, label="T₀₀")
energy_marker = ax3.axhline(0, color="cyan", linestyle="--", lw=1.5)
energy_profile, = ax3.plot(x, energy_history[0, :], 'y-', lw=2.5, alpha=0.95)

plt.tight_layout()

def init():
    warp_line.set_data([], [])
    light_line1.set_data([], [])
    light_line2.set_data([], [])
    shift_line.set_data([], [])
    ship.set_data([], [])
    theta_profile.set_data([], [])
    energy_profile.set_data([], [])
    theta_marker.set_ydata([0, 0])
    energy_marker.set_ydata([0, 0])
    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_profile, energy_profile, theta_marker, energy_marker)

def update(frame):
    x0 = x0_values[frame]
    rs_on = np.abs(x - x0)
    f = shape_function(rs_on, R, SIGMA)
    
    # Top panel
    warp_line.set_data(x, f)
    light1 = light_ray(x, f)
    light_line1.set_data(x, light1)
    light_line2.set_data(x, light1 + 0.5)
    beta = -V_S * f
    shift_line.set_data(x, beta)
    ship.set_data([x0], [1.1])
    
    # Spacetime panels
    theta_marker.set_ydata([frame, frame])
    energy_marker.set_ydata([frame, frame])
    theta_profile.set_data(x, theta_history[frame])
    energy_profile.set_data(x, energy_history[frame])
    
    ax1.set_title(f"Alcubierre Warp Bubble | x₀ = {x0:.1f} | v = {V_S}c", fontsize=13)
    
    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_profile, energy_profile, theta_marker, energy_marker)

ani = FuncAnimation(fig, update, frames=NUM_FRAMES, init_func=init,
                    interval=60, blit=False)

print("Animation ready! Close window to exit.")
plt.show()

#ani.save('warp_ng.gif', writer='pillow', fps=15, dpi=110)

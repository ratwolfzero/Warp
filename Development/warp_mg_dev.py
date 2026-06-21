import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

# ============================================================
# Shared parameters (bubble properties)
# ============================================================
R = 2.0
SIGMA = 3.0
V_S = 1.0

# 1D animation parameters
X_MIN = -20.0
X_MAX = 20.0
N_X = 800
NUM_FRAMES = 150
LIGHT_DRAG = 2.0

x = np.linspace(X_MIN, X_MAX, N_X)
dx = x[1] - x[0]
x0_values = np.linspace(-12, 12, NUM_FRAMES)   # bubble centre positions

# 2D grid parameters (use same bubble centre range)
Y_RANGE = (-6, 6)
Z_RANGE = (-15, 15)          # extended to see bubble at all positions
N_Y_LINES = 25
N_Z_LINES = 45
y_vals = np.linspace(*Y_RANGE, N_Y_LINES)
z_vals = np.linspace(*Z_RANGE, N_Z_LINES)

# ============================================================
# Shape function (common)
# ============================================================
def shape_function(r, R=R, sigma=SIGMA):
    return (np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))) / (2.0 * np.tanh(sigma * R))

# ============================================================
# 1D auxiliary functions
# ============================================================
def light_ray(x, f):
    return x + LIGHT_DRAG * V_S * f

# Precompute spacetime diagrams for the 1D panels
print("Precomputing spacetime diagrams...")
theta_history = np.zeros((NUM_FRAMES, N_X))
energy_history = np.zeros((NUM_FRAMES, N_X))

for i, x0 in enumerate(x0_values):
    # Expansion scalar
    rs_on = np.abs(x - x0)
    f_on = shape_function(rs_on)
    dfdx = np.gradient(f_on, dx)
    theta = V_S * dfdx
    theta[np.abs(theta) < 1e-8] = 0.0
    theta_history[i] = theta

    # Exotic energy density (at bubble wall rho=R)
    rho = R
    rs_off = np.sqrt((x - x0)**2 + rho**2)
    f_off = shape_function(rs_off)
    df_drs = np.gradient(f_off, rs_off)
    energy = - (V_S**2 * rho**2) / (4.0 * rs_off**2) * (df_drs)**2
    energy_history[i] = energy

theta_lim = np.max(np.abs(theta_history))
energy_min = np.min(energy_history)
print("Precomputation done.")

# ============================================================
# 2D warp displacement (illustrative)
# ============================================================
def warp_displacement(Y, Z, z0):
    r = np.sqrt(Y**2 + (Z - z0)**2)
    f = shape_function(r)
    return -0.8 * (Z - z0) * f

# ============================================================
# Function to draw the 2D grid on a given axis
# ============================================================
def draw_2d_grid(ax, z0):
    ax.clear()

    # Horizontal grid lines (constant y) – use default colour cycle
    z_dense = np.linspace(*Z_RANGE, 500)
    for y0 in y_vals:
        Y = np.full_like(z_dense, y0)
        disp = warp_displacement(Y, z_dense, z0)
        z_warped = z_dense + disp
        ax.plot(z_warped, Y, lw=0.8)          # no explicit colour → uses default cycle

    # Vertical grid lines (constant z)
    y_dense = np.linspace(*Y_RANGE, 400)
    for z0_line in z_vals:
        Z = np.full_like(y_dense, z0_line)
        disp = warp_displacement(y_dense, Z, z0)
        z_warped = Z + disp
        ax.plot(z_warped, y_dense, lw=0.8)    # no explicit colour

    # Bubble boundary (circle)
    circle = plt.Circle((z0, 0), R, fill=False, edgecolor='black', linewidth=2.5)
    ax.add_patch(circle)

    # Bubble centre
    ax.plot(z0, 0, 'ko', markersize=6)

    # Motion trail
    trail_z = np.linspace(x0_values[0], z0, 300)
    ax.plot(trail_z, np.zeros_like(trail_z), 'k--', alpha=0.3)

    ax.set_xlim(*Z_RANGE)
    ax.set_ylim(*Y_RANGE)
    ax.set_aspect('equal')
    ax.set_xlabel('z')
    ax.set_ylabel('y')
    ax.set_title('2D Grid Distortion (warp bubble)', fontsize=11)
    return []

# ============================================================
# Create figure with GridSpec: 3 rows, 2 columns
# Top row: left = 1D warp shape, right = 2D grid
# Second row: expansion scalar (spanning both columns)
# Third row: exotic energy (spanning both columns)
# ============================================================
fig = plt.figure(figsize=(16, 10.5))
gs = GridSpec(3, 2, height_ratios=[1.25, 1, 1], width_ratios=[1.5, 1.2])

# Top-left: 1D shape
ax1 = fig.add_subplot(gs[0, 0])
# Top-right: 2D grid
ax4 = fig.add_subplot(gs[0, 1])
# Middle: expansion scalar (full width)
ax2 = fig.add_subplot(gs[1, :])
# Bottom: exotic energy (full width)
ax3 = fig.add_subplot(gs[2, :])

# ------------------------------------------------------------
# Set up the 1D panels (lines, images, etc.)
# ------------------------------------------------------------

# Top-left: warp shape
warp_line, = ax1.plot([], [], 'b-', lw=3, label='Shape Function f(rs)')
light_line1, = ax1.plot([], [], 'c-', lw=2, alpha=0.8, label='Light ray (dragged)')
light_line2, = ax1.plot([], [], 'r--', lw=1.8, alpha=0.6, label='Light ray (offset)')
shift_line, = ax1.plot([], [], 'g--', lw=1.8, alpha=0.85, label='Shift vector β')
ship, = ax1.plot([], [], 'ko', markersize=10, label='Spacecraft')
ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(-2.3, 2.3)
ax1.set_ylabel('Warp Geometry')
ax1.grid(alpha=0.3)
ax1.legend(loc='upper left', fontsize=9)

# Middle: expansion scalar
theta_img = ax2.imshow(theta_history, aspect='auto', origin='lower',
                       extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                       cmap='coolwarm', vmin=-theta_lim, vmax=theta_lim)
ax2.set_title('Expansion Scalar θ\nBlue = expansion (behind) | Red = contraction (ahead)', fontsize=11)
ax2.set_ylabel('Time (frames)')
fig.colorbar(theta_img, ax=ax2, label='θ')
theta_marker = ax2.axhline(0, color='k', linestyle='--', lw=1.5)
theta_profile, = ax2.plot(x, theta_history[0, :], 'r-', lw=2.5, alpha=0.95)

# Bottom: exotic energy
energy_img = ax3.imshow(energy_history, aspect='auto', origin='lower',
                        extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                        cmap='plasma', vmin=energy_min, vmax=0)
ax3.set_title('Exotic Energy Density T₀₀ (at bubble wall ρ=R)\nDark purple = strong negative energy', fontsize=11)
ax3.set_xlabel('Spatial Coordinate x')
ax3.set_ylabel('Time (frames)')
fig.colorbar(energy_img, ax=ax3, label='T₀₀')
energy_marker = ax3.axhline(0, color='cyan', linestyle='--', lw=1.5)
energy_profile, = ax3.plot(x, energy_history[0, :], 'y-', lw=2.5, alpha=0.95)

plt.tight_layout()

# ============================================================
# Animation update function
# ============================================================
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

    # ---- Update 1D panels ----
    rs_on = np.abs(x - x0)
    f = shape_function(rs_on)

    warp_line.set_data(x, f)
    light1 = light_ray(x, f)
    light_line1.set_data(x, light1)
    light_line2.set_data(x, light1 + 0.5)      # offset light ray
    beta = -V_S * f
    shift_line.set_data(x, beta)
    ship.set_data([x0], [1.1])

    # Update spacetime markers and profiles
    theta_marker.set_ydata([frame, frame])
    energy_marker.set_ydata([frame, frame])
    theta_profile.set_data(x, theta_history[frame])
    energy_profile.set_data(x, energy_history[frame])

    ax1.set_title(f'Alcubierre Warp Bubble | x₀ = {x0:.1f} | v = {V_S}c', fontsize=13)

    # ---- Update 2D panel ----
    draw_2d_grid(ax4, x0)

    return (warp_line, light_line1, light_line2, shift_line, ship,
            theta_profile, energy_profile, theta_marker, energy_marker)

ani = FuncAnimation(fig, update, frames=NUM_FRAMES, init_func=init,
                    interval=50, blit=False)

print("Animation ready! Close the window to exit.")
plt.show()
#ani.save('warp_ng_d.gif', writer='pillow', fps=15, dpi=110)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec

# ============================================================
# Shared parameters (bubble properties)
# ============================================================
R = 2.0
SIGMA = 4.5
V_S = 1.0

# 1D animation parameters
X_MIN = -20.0
X_MAX = 20.0
N_X = 800
NUM_FRAMES = 150
LIGHT_DRAG = 2.0
SHIFT_SCALE = 1.0
ANIMATION_INTERVAL_MS = 70

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
z_dense = np.linspace(*Z_RANGE, 500)
y_dense = np.linspace(*Y_RANGE, 400)

# Precompute the 2D grid coordinates so the animation does not rebuild them every frame.
Y_h = np.repeat(y_vals[:, None], z_dense.size, axis=1)
Z_h = np.tile(z_dense[None, :], (y_vals.size, 1))
Y_v = np.tile(y_dense[None, :], (z_vals.size, 1))
Z_v = np.repeat(z_vals[:, None], y_dense.size, axis=1)

# ============================================================
# Shape function (common)
# ============================================================
def shape_function(r, R=R, sigma=SIGMA):
    numerator = np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))
    denominator = 2.0 * np.tanh(sigma * R)
    return numerator / denominator

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
# 2D warp displacement (Alcubierre-style shift field)
# ============================================================
def shift_field(Y, Z, z0):
    r = np.sqrt(Y**2 + (Z - z0)**2)
    f = shape_function(r)
    return -V_S * f


def warp_displacement(Y, Z, z0):
    return -SHIFT_SCALE * shift_field(Y, Z, z0)

# ============================================================
# Function to draw the 2D grid on a given axis
# ============================================================
def draw_2d_grid(ax, z0, grid_collection, bubble_circle, bubble_center, trail_line):
    segments = []

    # Horizontal grid lines (constant y)
    disp_h = warp_displacement(Y_h, Z_h, z0)
    z_warped_h = Z_h + disp_h
    for i in range(y_vals.size):
        segments.append(np.column_stack((z_warped_h[i], Y_h[i])))

    # Vertical grid lines (constant z)
    disp_v = warp_displacement(Y_v, Z_v, z0)
    z_warped_v = Z_v + disp_v
    for i in range(z_vals.size):
        segments.append(np.column_stack((z_warped_v[i], Y_v[i])))

    grid_collection.set_segments(segments)
    bubble_circle.center = (z0, 0.0)
    bubble_center.set_data([z0], [0.0])

    trail_z = np.linspace(x0_values[0], z0, 300)
    trail_line.set_data(trail_z, np.zeros_like(trail_z))

    ax.set_xlim(*Z_RANGE)
    ax.set_ylim(*Y_RANGE)
    ax.set_aspect('equal')
    ax.set_xlabel('z')
    ax.set_ylabel('y')
    ax.set_title('Illustrative coordinate grid under an Alcubierre-style shift field', fontsize=11)
    return []

# ============================================================
# Create figure with GridSpec: 3 rows, 2 columns
# Top row: left = 1D warp shape, right = 2D grid
# Second row: expansion scalar (spanning both columns)
# Third row: exotic energy (spanning both columns)
# ============================================================
fig = plt.figure(figsize=(16, 10.5), facecolor='white')
gs = GridSpec(3, 2, height_ratios=[1.25, 1, 1], width_ratios=[1.45, 1.15], wspace=0.22, hspace=0.30)

# Top-left: 1D shape
ax1 = fig.add_subplot(gs[0, 0])
# Top-right: 2D grid
ax4 = fig.add_subplot(gs[0, 1])
# Middle: expansion scalar (full width)
ax2 = fig.add_subplot(gs[1, :])
# Bottom: exotic energy (full width)
ax3 = fig.add_subplot(gs[2, :])

# 2D grid artists (reused every frame for smoother animation)
grid_collection = LineCollection([], linewidths=0.8, colors='k', alpha=0.8)
ax4.add_collection(grid_collection)
bubble_circle = plt.Circle((0, 0), R, fill=False, edgecolor='black', linewidth=2.5)
ax4.add_patch(bubble_circle)
bubble_center, = ax4.plot([], [], 'ko', markersize=6)
trail_line, = ax4.plot([], [], 'k--', alpha=0.3)
ax4.set_xlim(*Z_RANGE)
ax4.set_ylim(*Y_RANGE)
ax4.set_aspect('equal')
ax4.set_xlabel('z')
ax4.set_ylabel('y')
ax4.set_title('Coordinate grid distortion', fontsize=11)

# ------------------------------------------------------------
# Set up the 1D panels (lines, images, etc.)
# ------------------------------------------------------------

# Top-left: warp shape
warp_line, = ax1.plot([], [], 'b-', lw=3, label='Bubble profile f(r_s)')
light_line1, = ax1.plot([], [], 'c-', lw=2, alpha=0.8, label='Light ray (coordinate drag)')
light_line2, = ax1.plot([], [], 'r--', lw=1.8, alpha=0.6, label='Light ray (offset)')
shift_line, = ax1.plot([], [], 'g--', lw=1.8, alpha=0.85, label='Shift field β_x(r_s) = -v_s f(r_s)')
coord_trail, = ax1.plot([], [], 'k:', lw=1.6, alpha=0.75, label='Coordinate-frame path')
coord_marker, = ax1.plot([], [], 'o', color='orange', markersize=8, label='Bubble center')
ship, = ax1.plot([], [], 'ko', markersize=10, label='Local ship position')
ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(-2.3, 2.3)
ax1.set_ylabel('Warp Geometry')
ax1.set_title('Bubble profile and shift field', fontsize=12)
ax1.grid(alpha=0.3)
ax1.text(0.02, 0.94, 'In the simplest Alcubierre ansatz, β_x is proportional to -f(r_s) for a bubble moving in +x.',
         transform=ax1.transAxes, fontsize=8, va='top', color='dimgray')
ax1.legend(loc='upper left', fontsize=9)

# Middle: expansion scalar
theta_img = ax2.imshow(theta_history, aspect='auto', origin='lower',
                       extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                       cmap='coolwarm', vmin=-theta_lim, vmax=theta_lim)
ax2.contour(x, np.arange(NUM_FRAMES), theta_history, levels=[0.0], colors='white', linewidths=0.8, alpha=0.9)
ax2.set_title('Effective expansion scalar $\theta$', fontsize=11)
ax2.set_ylabel('Time (frames)')
fig.colorbar(theta_img, ax=ax2, label='$\theta$')
theta_marker = ax2.axhline(0, color='k', linestyle='--', lw=1.5)
ax2.axvline(0, color='gray', linestyle=':', lw=1.0, alpha=0.8)
theta_profile, = ax2.plot(x, theta_history[0, :], 'r-', lw=2.5, alpha=0.95)

# Bottom: exotic energy
energy_img = ax3.imshow(energy_history, aspect='auto', origin='lower',
                        extent=[X_MIN, X_MAX, 0, NUM_FRAMES],
                        cmap='plasma', vmin=energy_min, vmax=0)
ax3.set_title('Effective energy proxy $T_{00}$', fontsize=11)
ax3.set_xlabel('Spatial Coordinate x')
ax3.set_ylabel('Time (frames)')
fig.colorbar(energy_img, ax=ax3, label='$T_{00}$ proxy')
energy_marker = ax3.axhline(0, color='cyan', linestyle='--', lw=1.5)
energy_profile, = ax3.plot(x, energy_history[0, :], 'y-', lw=2.5, alpha=0.95)

fig.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.08, wspace=0.22, hspace=0.30)
fig.text(0.5, 0.01, 'Illustrative toy model based on the Alcubierre metric ansatz; not a feasible propulsion system.',
         ha='center', va='bottom', fontsize=9, style='italic', color='dimgray')

# ============================================================
# Animation update function
# ============================================================
def init():
    warp_line.set_data([], [])
    light_line1.set_data([], [])
    light_line2.set_data([], [])
    shift_line.set_data([], [])
    coord_trail.set_data([], [])
    coord_marker.set_data([], [])
    ship.set_data([], [])
    theta_profile.set_data([], [])
    energy_profile.set_data([], [])
    theta_marker.set_ydata([0, 0])
    energy_marker.set_ydata([0, 0])
    draw_2d_grid(ax4, x0_values[0], grid_collection, bubble_circle, bubble_center, trail_line)
    return (warp_line, light_line1, light_line2, shift_line, coord_trail,
            coord_marker, ship, theta_profile, energy_profile, theta_marker,
            energy_marker, grid_collection, bubble_circle, bubble_center, trail_line)

def update(frame):
    x0 = x0_values[frame]

    # ---- Update 1D panels ----
    rs_on = np.abs(x - x0)
    f = shape_function(rs_on)

    warp_line.set_data(x, f)
    light1 = light_ray(x, f)
    light_line1.set_data(x, light1)
    light_line2.set_data(x, light1 + 0.5)      # offset light ray
    beta = SHIFT_SCALE * shift_field(np.zeros_like(x), x, x0)
    shift_line.set_data(x, beta)
    coord_trail.set_data(x0_values[:frame + 1], np.full(frame + 1, 1.15))
    coord_marker.set_data([x0], [1.1])
    ship.set_data([x0], [0.85])

    # Update spacetime markers and profiles
    theta_marker.set_ydata([frame, frame])
    energy_marker.set_ydata([frame, frame])
    theta_profile.set_data(x, theta_history[frame])
    energy_profile.set_data(x, energy_history[frame])

    ax1.set_title(f'Alcubierre-style bubble | $x_0 = {x0:.1f}$ | $v = {V_S}c$', fontsize=13)

    # ---- Update 2D panel ----
    draw_2d_grid(ax4, x0, grid_collection, bubble_circle, bubble_center, trail_line)

    return (warp_line, light_line1, light_line2, shift_line, coord_trail,
            coord_marker, ship, theta_profile, energy_profile, theta_marker,
            energy_marker, grid_collection, bubble_circle, bubble_center, trail_line)

ani = FuncAnimation(fig, update, frames=NUM_FRAMES, init_func=init,
                    interval=ANIMATION_INTERVAL_MS, blit=True)

print("Animation ready! Close the window to exit.")
plt.show()
#ani.save('warp_ng_d.gif', writer='pillow', fps=15, dpi=110)
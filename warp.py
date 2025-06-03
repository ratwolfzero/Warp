import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image  # For GIF export (optional)

# ===== Physics Functions =====
def warp_bubble(x, x0, sigma, contraction_strength=1.0, expansion_strength=1.0):
    """Generates a warp bubble with contraction, expansion, and a wake effect."""
    bubble = np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
    contraction = -contraction_strength * bubble * (x < x0)
    expansion = expansion_strength * bubble * (x > x0)
    wake = 0.3 * np.exp(-((x - x0 + 3) ** 2)) * (x < x0)  # Trailing wake
    return contraction + expansion + wake

def light_ray_trajectory(x, warp_field, bending_strength=1.0):
    """Simulates light bending due to the warp field (nonlinear effect)."""
    return x + bending_strength * np.sin(warp_field)  # Nonlinear distortion

# ===== Animation Setup =====
def init_animation():
    """Initialize empty plot."""
    line_warp.set_data([], [])
    line_light.set_data([], [])
    spacecraft.set_data([], [])
    return line_warp, line_light, spacecraft

def update_animation(frame):
    """Update the plot for each frame."""
    x0 = x0_values[frame]
    warp_field = warp_bubble(x, x0, sigma, contraction_strength, expansion_strength)
    light_rays = light_ray_trajectory(x, warp_field, bending_strength)
    
    # Update plot data
    line_warp.set_data(x, warp_field)
    line_light.set_data(x, light_rays)
    spacecraft.set_data([x0], [0])
    
    # Dynamic y-axis scaling
    ax.set_ylim(np.min(warp_field) - 0.5, np.max(warp_field) + 0.5)
    ax.set_title(f"Warp Bubble Motion (x = {x0:.1f})")
    return line_warp, line_light, spacecraft

# ===== Main Simulation =====
def main(save_gif=False):
    global x, sigma, contraction_strength, expansion_strength, bending_strength
    global num_frames, x0_values, line_warp, line_light, spacecraft, ax

    # Parameters
    x = np.linspace(-20, 20, 1000)  # Space coordinates
    sigma = 1.0                      # Warp bubble width
    contraction_strength = 2.0       # Front contraction strength
    expansion_strength = 2.0         # Rear expansion strength
    bending_strength = 2.0           # Light bending magnitude
    num_frames = 100                 # Animation frames
    x0_values = np.linspace(-15, 15, num_frames)  # Warp bubble path

    # Plot setup
    fig, ax = plt.subplots(figsize=(10, 6))
    line_warp, = ax.plot([], [], label="Warp Field", color="blue", lw=2)
    line_light, = ax.plot([], [], label="Light Rays", color="red", lw=2, alpha=0.7)
    spacecraft, = ax.plot([], [], 'ko', markersize=10, label="Spacecraft")
    
    # Styling
    ax.set_xlim(-20, 20)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("Space (x)")
    ax.set_ylabel("Space Distortion")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")

    # Create animation
    ani = FuncAnimation(
        fig, update_animation, frames=num_frames,
        init_func=init_animation, blit=False, interval=70
    )

    # Save as GIF (optional)
    if save_gif:
        print("Saving GIF... (this may take a moment)")
        ani.save("warp_wave_simulation.gif", writer="pillow", fps=20, dpi=100)
        print("GIF saved as 'warp_drive.gif'")

    plt.show()

# ===== Run Simulation =====
if __name__ == "__main__":
    main(save_gif=False)  # Set `save_gif=False` to disable export

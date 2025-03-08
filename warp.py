import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the warp bubble function with space contraction and expansion
def warp_bubble(x, x0, sigma, contraction_strength=1.0, expansion_strength=1.0):
    """
    x: Position in space
    x0: Center of the warp bubble
    sigma: Width of the warp bubble
    contraction_strength: Strength of space contraction in front of the bubble
    expansion_strength: Strength of space expansion behind the bubble
    """
    # Gaussian-shaped warp bubble
    bubble = np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
    
    # Space contraction in front of the bubble (x < x0)
    contraction = -contraction_strength * bubble * (x < x0)
    
    # Space expansion behind the bubble (x > x0)
    expansion = expansion_strength * bubble * (x > x0)
    
    # Combine contraction and expansion
    return contraction + expansion

# Simulate light rays passing through the warp bubble
def light_ray_trajectory(x, warp_field, bending_strength=1.0):
    """
    Simulate light rays bending due to the warp bubble.
    bending_strength: Controls how much the light rays bend.
    """
    return x + bending_strength * warp_field  # Adjust bending strength

# Initialize the animation
def init_animation():
    """
    Initialize the animation with empty data.
    """
    line_warp.set_data([], [])
    line_light.set_data([], [])
    spacecraft.set_data([], [])
    return line_warp, line_light, spacecraft

# Update function for the animation
def update_animation(frame):
    """
    Update the animation for each frame.
    """
    x0 = x0_values[frame]  # Current position of the warp bubble
    warp_field = warp_bubble(x, x0, sigma, contraction_strength, expansion_strength)  # Calculate the warp bubble
    light_rays = light_ray_trajectory(x, warp_field, bending_strength)  # Calculate light ray trajectories
    
    # Update the plot
    line_warp.set_data(x, warp_field)
    line_light.set_data(x, light_rays)
    spacecraft.set_data([x0], [0])  # Spacecraft is at the center of the warp bubble
    return line_warp, line_light, spacecraft

# Main function to run the simulation
def main():
    """
    Main function to set up and run the warp drive simulation.
    """
    global x, sigma, contraction_strength, expansion_strength, bending_strength, num_frames, x0_values
    global line_warp, line_light, spacecraft

    # Parameters
    x = np.linspace(-20, 20, 1000)  # Space coordinates (extended range)
    sigma = 1  # Width of the warp bubble
    contraction_strength = 2.0  # Strength of space contraction
    expansion_strength = 2.0  # Strength of space expansion
    bending_strength = 2.0  # Increase bending effect for better visibility
    num_frames = 100  # Number of animation frames
    x0_values = np.linspace(-15, 15, num_frames)  # Move the warp bubble from x = -15 to x = 15

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    line_warp, = ax.plot([], [], label="Warp Bubble (Space Distortion)", color="blue", linewidth=2)
    line_light, = ax.plot([], [], label="Light Ray Trajectory", color="red", linewidth=2)
    spacecraft, = ax.plot([], [], 'ko', markersize=10, label="Spacecraft")  # Spacecraft marker
    ax.set_xlim(-20, 20)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("Space")
    ax.set_ylabel("Effect")
    ax.set_title("Warp Wave with Spacecraft")
    ax.legend()
    ax.grid()

    # Create the animation
    ani = FuncAnimation(fig, update_animation, frames=num_frames, init_func=init_animation, blit=True, interval=50)

    # Show the animation
    plt.show()

# Run the simulation
if __name__ == "__main__":
    main()

# Development Notes: Alcubierre-style Warp Bubble Visualisation

This folder contains a developmental visualisation of an Alcubierre-style warp-bubble toy model. It is intended as an educational and illustrative animation, not as a physically realistic propulsion device.

## Purpose

The script in this folder animates a simplified version of the Alcubierre warp-bubble idea in one and two spatial dimensions. The goal is to show how a smooth spacetime deformation can be represented visually through:

- a bubble profile $f(r_s)$,
- a shift field $eta_x(r_s)$,
- a coordinate-grid distortion in a 2D slice,
- and a pair of diagnostic panels for an effective expansion scalar and an effective energy proxy.

## Mathematical background

The simplest Alcubierre-inspired ansatz uses a smooth bubble profile $f(r_s)$ that is close to $1$ inside the bubble and close to $0$ outside. A common choice is

$$
 f(r_s) = \frac{\tanh[\sigma(r_s + R)] - \tanh[\sigma(r_s - R)]}{2\tanh(\sigma R)}
$$

where:

- $r_s = \sqrt{(x-x_0)^2 + y^2 + z^2}$ is the distance from the moving bubble center,
- $R$ is the effective bubble radius,
- $\\sigma$ controls the sharpness of the transition.

The corresponding shift field is then taken to be proportional to the same profile:

$$
\beta_x(r_s) \sim -v_s\,f(r_s)
$$

This is the key geometric ingredient in the Alcubierre metric ansatz. It does not represent a local material motion faster than light; rather, it describes how the coordinate system is distorted.

## What the script is showing

### 1. Bubble profile panel

The top-left panel shows the profile $f(r_s)$ as the bubble moves through the 1D coordinate line. This is the smooth transition region that defines the warp bubble.

### 2. Shift-field panel

The top-left panel also shows the shift field $\beta_x(r_s)$ as a dashed curve. In a toy interpretation, this is the coordinate distortion that accompanies the bubble profile.

### 3. 2D coordinate-grid distortion

The top-right panel shows a 2D slice of a coordinate grid being deformed by the same effective bubble geometry. The grid is not a literal physical medium; it is a visual representation of the warped coordinate frame.

### 4. Expansion scalar panel

The middle panel shows an effective expansion scalar computed from the profile gradient:

$$
\theta \sim v_s \frac{df}{dx}
$$

This is a qualitative diagnostic only. It is not the full spacetime expansion tensor of a rigorous solution.

### 5. Effective energy proxy panel

The bottom panel shows an effective energy-like quantity computed from the profile derivative at a fixed radius. In the toy model this is plotted as an illustrative negative-energy proxy:

$$
T_{00}^{\text{proxy}} \propto -\frac{v_s^2 \rho^2}{4r_s^2}\left(\frac{df}{dr_s}\right)^2
$$

This should be read as a schematic visualization only. It is not a full calculation of the stress-energy tensor for a genuine metric solution.

## Physics caution

This script is deliberately educational. It captures the spirit of the Alcubierre idea:

- a smooth spacetime deformation,
- a moving bubble region,
- and an associated shift field.

However, it does not represent a physically feasible propulsion system. A true Alcubierre metric would require exotic matter and a fully consistent solution to the Einstein equations, which are not addressed here.

## Files

- `warp_mg_dev.py` — the animated development version.
- `2D_bubble.py` — related exploratory script for 2D bubble visualisation.
- `warp_mg_dev.py` — the main development animation discussed here.

## Summary

This version is best understood as a visual toy model of the Alcubierre metric ansatz:

$$
 ds^2 = -dt^2 + \left(dx^i - \beta^i dt\right)^2
$$

with a smooth, moving bubble profile and an associated coordinate shift. It is useful for intuition, but it should not be interpreted as a working or physically realistic warp drive.

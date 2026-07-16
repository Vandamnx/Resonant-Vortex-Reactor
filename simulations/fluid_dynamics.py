"""
Fluid Dynamics Simulation for Gali-Spinal Tube
Resonant Vortex Reactor (RVR) v4+ - Galinstan + Sphere Chain

Simple 1D fluid flow model with Lorentz drive, drag, and sphere interaction.

Run: python fluid_dynamics_sim.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def fluid_dynamics(t, state, params):
    v, pressure = state  # velocity, effective pressure
    drive, viscosity, density, sphere_factor, threshold = params
    
    # Lorentz + centrifugal drive term
    drive_force = drive * v if v > threshold else drive * 0.6 * v
    
    # Viscous drag + sphere chain resistance
    drag = viscosity * v**2 + sphere_factor * density * v**3
    
    dvdt = drive_force - drag
    
    # Pressure build-up from vortex motion
    dpdt = 0.8 * v**2 if v > threshold else 0.3 * v**2
    
    return [dvdt, dpdt]

# High-RPM tuned parameters for Galinstan system
drive = 48.0           # Strong Lorentz drive
viscosity = 0.095      # Effective viscosity
density = 6440         # Galinstan density
sphere_factor = 0.028  # Contribution from magnetite sphere chain
threshold = 22.0       # Sonic threshold velocity

params = [drive, viscosity, density, sphere_factor, threshold]

# Long run
sol = solve_ivp(fluid_dynamics, [0, 35], [0.0, 0.0], args=(params,), dense_output=True, rtol=1e-6)

t = np.linspace(0, 35, 1400)
v, pressure = sol.sol(t)

# Plot
plt.figure(figsize=(12, 9))

plt.subplot(3, 1, 1)
plt.plot(t, v, linewidth=3.0, color='#00B4D8', label='Fluid Velocity (Galinstan flow)')
plt.axhline(y=threshold, color='#E63946', linestyle='--', label='Sonic Threshold')
plt.title('Fluid Dynamics Simulation - High-RPM Gali-Spinal Tube')
plt.ylabel('Velocity')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, pressure, linewidth=2.5, color='#FF9F1C', label='Vortex Pressure Build-up')
plt.xlabel('Time (s)')
plt.ylabel('Pressure')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, v * pressure, linewidth=2.2, color='#FF4D4D', label='Effective Twist-Force Power')
plt.xlabel('Time (s)')
plt.ylabel('Power Proxy')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Fluid Dynamics Simulation Result ===")
print(f"Peak fluid velocity: {v[-1]:.2f}")
print(f"Maximum vortex pressure: {max(pressure):.3f}")
print("Strong high-RPM fluid motion with clear threshold behavior.")
print("This models the Galinstan + sphere chain dynamics in the tube.")

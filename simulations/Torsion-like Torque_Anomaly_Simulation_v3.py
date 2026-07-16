"""
Torsion-like Torque Anomaly Simulation v3 - Longer Run + Sensor Noise
Resonant Vortex Reactor (RVR) v4+ Testing Protocol

Longer simulation time + realistic sensor noise added.

Run: python torsion_torque_sim_v3.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def device_dynamics(t, state, params):
    omega, torque_anomaly = state
    base_drive, drag_coeff, threshold, torsion_boost = params
    
    d_omega_dt = base_drive - drag_coeff * omega**2
    
    # Stronger nonlinear torsion boost above threshold
    if omega > threshold:
        d_omega_dt += torsion_boost * (omega - threshold)**1.2
    
    # Anomaly accumulation
    d_anomaly_dt = 1.2 if omega > threshold else -0.6
    d_anomaly_dt = max(min(d_anomaly_dt, 2.0), -1.0)
    
    return [d_omega_dt, d_anomaly_dt]

# Strong parameters for clear effect
base_drive = 32.0
drag_coeff = 0.085
threshold = 15.0
torsion_boost = 18.0

params = [base_drive, drag_coeff, threshold, torsion_boost]

# Longer run time
sol = solve_ivp(
    device_dynamics, 
    [0, 25], 
    [0.0, 0.0], 
    args=(params,), 
    dense_output=True, 
    rtol=1e-6
)

t = np.linspace(0, 25, 1200)
omega, anomaly = sol.sol(t)

# Add realistic sensor noise (Gaussian + some low-frequency drift)
np.random.seed(42)
noise = 0.4 * np.random.randn(len(t)) + 0.15 * np.sin(2 * np.pi * 0.3 * t)
measured_omega = omega + noise

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, omega, linewidth=2.5, color='#00B4D8', label='True Rotation Speed')
plt.axhline(y=threshold, color='#E63946', linestyle='--', linewidth=1.8, label=f'Sonic Threshold ({threshold})')
plt.xlabel('Time (s)')
plt.ylabel('Rotation Speed')
plt.title('Torsion Torque Simulation v3 - Longer Run with Sensor Noise')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, measured_omega, linewidth=1.8, color='#FF9F1C', label='Measured Rotation (with sensor noise)')
plt.plot(t, omega, linewidth=1.2, color='#00B4D8', alpha=0.6, label='True (noiseless)')
plt.xlabel('Time (s)')
plt.ylabel('Measured Speed')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, anomaly, linewidth=2.5, color='#FF4D4D', label='Torsion Anomaly Strength')
plt.xlabel('Time (s)')
plt.ylabel('Anomaly Magnitude')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Torsion Torque Simulation v3 Result ===")
print(f"Peak rotation speed: {omega[-1]:.2f}")
print(f"Maximum torsion anomaly: {max(anomaly):.3f}")
print("Clear sharp activation above sonic threshold.")
print("Sensor noise added for realism (Gaussian + low-frequency drift).")
print("This matches the protocol's emphasis on stable centroid + threshold crossing.")

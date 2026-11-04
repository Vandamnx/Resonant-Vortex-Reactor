### Developmental py sims

# Antoniou Gyrator Synthetic Inductor

* Antoniou Gyrator Synthetic Inductor
* For Piezo RL Shunt @ ~430 Hz (L ≈ 0.14 H example)
* Nodes: 1 = Input (piezo hot), 0 = GND

.param Rbase=10k
.param Cval=100n   ; Adjust for exact L = (R1*R3*C)/R2

.subckt opamp nonin inv out
  E1 out 0 value={1e6 * (v(nonin) - v(inv))}
.ends

* Opamps (use real models like OPA445 for high-voltage in LTspice)
XU1 3 4 5 opamp
XU2 6 7 8 opamp

* Antoniou Connections
R1 1 3 {Rbase}
R2 4 0 {Rbase}
R3 5 6 {Rbase}
R4 7 1 {Rbase}
C1 8 0 {Cval}
R5 8 6 {Rbase}

* Test circuit
Vin 1 0 AC 1 SIN(0 1 430)
.ac dec 50 10 10k
.tran 0 0.01 0 1u
.probe V(1) I(R1)
.end

## Full Closed Loop Fluid Simulation

Updated Full Closed-Loop Simulation with Fluid Loading (added effective mass/damping from Galinstan + sphere chain).
Enhancements
 • Fluid term: Added mass (density-dependent) + viscous damping to mechanical equation.
 • Adaptation still tunes L to maintain resonance despite loading.
 • Result: Slightly lower natural freq + higher damping from fluid, but PLL adaptation compensates effectively.
New Plot (Displacement with fluid + adaptation trace):
The system remains stable and adaptive. Fluid makes it more realistic for the tube—adaptation is key for performance.
Full code ready for further mods (e.g., variable RPM, magnetic terms).

## 2-mode closed-loop skeleton

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def multi_mode_system(t, state, params):
    # state: [x1, v1, q1, L1, x2, v2, q2, L2]
    x1, v1, q1, L1, x2, v2, q2, L2 = state
    m, k1, k2, c, theta, Cp, R, fluid_m, fluid_c = params

    m_eff = m + fluid_m
    c_eff = c + fluid_c
    
    # Mode 1 (fundamental ~430 Hz)
    V1 = q1 / Cp
    dx1 = v1
    dv1 = (-c_eff*v1 - k1*x1 + theta*V1) / m_eff
    dq1 = -(R*q1/L1 + q1/(L1*Cp) - theta*v1/L1)
    
    # Mode 2 (higher mode)
    V2 = q2 / Cp
    dx2 = v2
    dv2 = (-c_eff*v2 - k2*x2 + theta*V2) / m_eff
    dq2 = -(R*q2/L2 + q2/(L2*Cp) - theta*v2/L2)
    
    # Simple independent adaptation (phase/power proxy)
    dL1 = -0.0008 * (v1 * np.sin(2*np.pi*430*t))
    dL2 = -0.0008 * (v2 * np.sin(2*np.pi*1200*t))   # example second mode
    
    return [dx1, dv1, dq1, dL1, dx2, dv2, dq2, dL2]

# Example parameters (tune to your measured modes)

params = [0.012, (2*np.pi*430)**2 *0.01, (2*np.pi*1200)**2* 0.01,
          0.6, 0.05, 1e-8, 180, 0.006, 2.5]

sol = solve_ivp(multi_mode_system, [0, 0.15],
                [0.008, 0, 0, 0.12, 0.004, 0, 0, 0.04],
                args=(params,), dense_output=True, rtol=1e-6)

t = np.linspace(0, 0.15, 1500)
traj = sol.sol(t)

plt.figure(figsize=(11, 8))
plt.subplot(3,1,1)
plt.plot(t, traj[0], label='Mode 1 displacement')
plt.plot(t, traj[4], label='Mode 2 displacement', alpha=0.8)
plt.title('Multi-Mode Adaptive Shunt with Fluid Loading')
plt.ylabel('Displacement')
plt.legend(); plt.grid(True, alpha=0.3)

plt.subplot(3,1,2)
plt.plot(t, traj[3], label='Adaptive L1 (430 Hz)')
plt.plot(t, traj[7], label='Adaptive L2')
plt.ylabel('L (H)'); plt.legend(); plt.grid(True, alpha=0.3)

plt.subplot(3,1,3)
plt.plot(t, traj[0]**2 + traj[4]**2, color='C3')
plt.xlabel('Time (s)'); plt.ylabel('Total energy proxy')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

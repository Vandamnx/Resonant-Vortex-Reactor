
Extended Fluid + Triboelectric Charge + Residual-Gas Ionization
WITH ion-density feedback into effective conductivity and luminosity proxy

Three carrier fluids:
  1. Deionized / dark water
  2. Galinstan
  3. Mercury (simulation-only triboelectric benchmark)

State vector: [v, p, q, ni]
  v  = fluid velocity
  p  = effective pressure
  q  = net charge density proxy
  ni = ion number density in residual gas
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Fluid parameter sets
# ------------------------------------------------------------------
fluids = {
    "water": {
        "density": 1000.0,
        "viscosity": 0.001,
        "sigma0": 5.5e-6,         # base conductivity
        "alpha_tribo": 1.5e-6,
        "label": "Deionized Water",
        "color": "#00B4D8",
    },
    "galinstan": {
        "density": 6440.0,
        "viscosity": 0.0024,
        "sigma0": 3.4e6,
        "alpha_tribo": 8.0e-6,
        "label": "Galinstan",
        "color": "#FF9F1C",
    },
    "mercury": {
        "density": 13530.0,
        "viscosity": 0.0015,
        "sigma0": 1.0e6,
        "alpha_tribo": 4.5e-5,    # stronger triboelectric effect
        "label": "Mercury (sim only)",
        "color": "#E63946",
    },
}

# Shared parameters
drive = 48.0
sphere_factor = 0.018
threshold = 14.0
A_contact = 0.015
v_thresh = 3.5
tau_relax_base = 0.07
n_gas = 1.2e19
E_ion = 11.5
kT = 0.025
gamma = 1.5e-4
beta = 3.0e-22
delta = 1.6e-12
kappa = 2.0e-7

# New coupling coefficients
k_sigma = 2.5e-15      # how strongly ni boosts effective conductivity
k_luma  = 1.8e-12      # luminosity / glow proxy scale

def make_rhs(fluid_key):
    f = fluids[fluid_key]
    density = f["density"]
    viscosity = f["viscosity"]
    alpha = f["alpha_tribo"]
    sigma0 = f["sigma0"]

    def rhs(t, state):
        v, p, q, ni = state

        # Effective conductivity boosted by ionization
        sigma_eff = sigma0 + k_sigma * ni

        # Charge relaxation time shortens as conductivity rises
        tau_relax = tau_relax_base * (1e6 / (sigma_eff + 1e-6))**0.35

        # --- Velocity equation ---
        drive_force = drive * v if v > threshold else drive * 0.55 * v
        drag = viscosity * v**2 + sphere_factor * density * abs(v)**3
        F_electro = kappa * q * abs(q)
        dvdt = drive_force - drag + F_electro

        # --- Pressure ---
        dpdt = 0.78 * v**2 if v > threshold else 0.30 * v**2

        # --- Triboelectric charge generation ---
        q_dot_tribo = (
            alpha * density * abs(v) * np.sign(v) * A_contact
            * (1.0 if abs(v) > v_thresh else 0.18)
        )
        q_dot_leak = -q / max(tau_relax, 1e-6)

        # --- Residual-gas ionization ---
        field_assist = kT + gamma * abs(q)
        ion_source = beta * abs(q) * n_gas * np.exp(-E_ion / max(field_assist, 1e-9))
        recombination = delta * ni**2
        ni_dot = ion_source - recombination

        return [dvdt, dpdt, q_dot_tribo + q_dot_leak, ni_dot]

    return rhs

# ------------------------------------------------------------------
# Run simulations
# ------------------------------------------------------------------
t_span = (0.0, 32.0)
t_eval = np.linspace(0.0, 32.0, 1400)
initial = [1.2, 0.0, 0.0, 8.0e7]

results = {}
for key in fluids:
    sol = solve_ivp(
        make_rhs(key),
        t_span,
        initial,
        t_eval=t_eval,
        rtol=1e-6,
        atol=1e-8,
        method="RK45",
    )
    results[key] = sol

# ------------------------------------------------------------------
# Derived quantities: effective conductivity & luminosity proxy
# ------------------------------------------------------------------
def derived(sol, key):
    v, p, q, ni = sol.y
    sigma0 = fluids[key]["sigma0"]
    sigma_eff = sigma0 + k_sigma * ni
    luminosity = k_luma * ni * abs(q)          # simple glow proxy
    return sigma_eff, luminosity

# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------
fig, axes = plt.subplots(5, 1, figsize=(12, 13), sharex=True)

for key, sol in results.items():
    f = fluids[key]
    t = sol.t
    v, p, q, ni = sol.y
    sigma_eff, luma = derived(sol, key)

    axes[0].plot(t, v, color=f["color"], lw=2.0, label=f["label"])
    axes[1].plot(t, q, color=f["color"], lw=1.8, label=f["label"])
    axes[2].plot(t, ni, color=f["color"], lw=1.8, label=f["label"])
    axes[3].plot(t, sigma_eff, color=f["color"], lw=1.8, label=f["label"])
    axes[4].plot(t, luma, color=f["color"], lw=1.8, label=f["label"])

axes[0].axhline(threshold, color="gray", ls="--", alpha=0.7)
axes[0].set_ylabel("Velocity")
axes[0].set_title("Ion-Coupled Model: Conductivity & Luminosity Feedback")
axes[0].legend(loc="upper right")
axes[0].grid(True, alpha=0.3)

axes[1].set_ylabel("Charge proxy")
axes[1].legend(loc="upper right")
axes[1].grid(True, alpha=0.3)

axes[2].set_ylabel("Ion density")
axes[2].legend(loc="upper right")
axes[2].grid(True, alpha=0.3)

axes[3].set_ylabel("Ï_eff (S/m)")
axes[3].legend(loc="upper right")
axes[3].grid(True, alpha=0.3)

axes[4].set_ylabel("Luminosity proxy")
axes[4].set_xlabel("Time")
axes[4].legend(loc="upper right")
axes[4].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/home/workdir/artifacts/extended_fluid_ion_coupled.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
print("=== Ion-Coupled Extended Simulation ===")
print(f"{'Fluid':<22} {'Peak v':>8} {'Final q':>11} {'Final ni':>11} {'Final Ï_eff':>12} {'Luma':>10}")
print("-" * 78)
for key, sol in results.items():
    v, p, q, ni = sol.y
    sigma_eff, luma = derived(sol, key)
    print(f"{fluids[key]['label']:<22} {v[-1]:8.2f} {q[-1]:11.3e} {ni[-1]:11.3e} "
          f"{sigma_eff[-1]:12.3e} {luma[-1]:10.3e}")

print("\nPlot saved to: /home/workdir/artifacts/extended_fluid_ion_coupled.png")
print("Ion density now feeds back into effective conductivity and a luminosity/glow proxy.")
print("Mercury remains a simulation-only benchmark.")

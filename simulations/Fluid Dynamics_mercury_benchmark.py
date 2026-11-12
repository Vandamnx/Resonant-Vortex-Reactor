"""
Fluid Dynamics + Triboelectric Charge + Residual-Gas Ionization
Resonant Vortex Reactor / Gali-Spinal Tube

Three carrier fluids:
  1. Deionized / dark water
  2. Galinstan
  3. Mercury (simulation-only triboelectric benchmark)

State vector: [v, p, q, ni]
  v  = fluid velocity
  p  = effective pressure proxy
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
        "sigma0": 5.5e-6,
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
        "alpha_tribo": 4.5e-5,
        "label": "Mercury (sim only)",
        "color": "#E63946",
    },
}

# Balanced high-velocity parameters
drive = 145.0
sphere_factor = 0.00115
visc_scale = 0.18
threshold = 20.0
A_contact = 0.0165
v_thresh = 5.5
tau_relax_base = 0.05
n_gas = 1.25e19
E_ion = 11.0
kT = 0.025
gamma = 1.9e-4
beta = 3.8e-22
delta = 1.45e-12
kappa = 1.3e-7
k_sigma = 2.6e-15
k_luma = 2.1e-12


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
        tau_relax = tau_relax_base * (1e6 / (sigma_eff + 1e-6)) ** 0.35

        # Drive + drag + electrostatic body force
        drive_force = drive * v if v > threshold else drive * 0.68 * v
        drag = viscosity * visc_scale * v**2 + sphere_factor * density * abs(v) ** 1.75
        F_electro = kappa * q * abs(q)
        dvdt = drive_force - drag + F_electro

        # Pressure proxy
        dpdt = 0.88 * v**2 if v > threshold else 0.34 * v**2

        # Triboelectric charge generation + leakage
        q_dot_tribo = (
            alpha * density * abs(v) * np.sign(v) * A_contact
            * (1.0 if abs(v) > v_thresh else 0.23)
        )
        q_dot_leak = -q / max(tau_relax, 1e-6)

        # Residual-gas ionization + recombination
        field_assist = kT + gamma * abs(q)
        ion_source = beta * abs(q) * n_gas * np.exp(-E_ion / max(field_assist, 1e-9))
        recombination = delta * ni**2
        ni_dot = ion_source - recombination

        return [dvdt, dpdt, q_dot_tribo + q_dot_leak, ni_dot]

    return rhs


def derived(sol, key):
    v, p, q, ni = sol.y
    sigma0 = fluids[key]["sigma0"]
    sigma_eff = sigma0 + k_sigma * ni
    luminosity = k_luma * ni * abs(q)
    return sigma_eff, luminosity


# ------------------------------------------------------------------
# Run all three fluids
# ------------------------------------------------------------------
t_span = (0.0, 24.0)
t_eval = np.linspace(0.0, 24.0, 1300)
initial = [5.0, 0.0, 0.0, 1.1e8]

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
# Plotting
# ------------------------------------------------------------------
fig, axes = plt.subplots(5, 1, figsize=(12, 13), sharex=True)

for key, sol in results.items():
    f = fluids[key]
    t = sol.t
    v, p, q, ni = sol.y
    sigma_eff, luma = derived(sol, key)

    axes[0].plot(t, v, color=f["color"], lw=2.2, label=f["label"])
    axes[1].plot(t, q, color=f["color"], lw=1.9, label=f["label"])
    axes[2].plot(t, ni, color=f["color"], lw=1.9, label=f["label"])
    axes[3].plot(t, sigma_eff, color=f["color"], lw=1.8, label=f["label"])
    axes[4].plot(t, luma, color=f["color"], lw=1.8, label=f["label"])

axes[0].axhline(threshold, color="gray", ls="--", alpha=0.7, label="Threshold")
axes[0].set_ylabel("Velocity")
axes[0].set_title("RVR Fluid + Triboelectric Charge + Ionization (Balanced High Velocity)")
axes[0].legend(loc="upper right")
axes[0].grid(True, alpha=0.3)

axes[1].set_ylabel("Charge proxy")
axes[1].legend(loc="upper right")
axes[1].grid(True, alpha=0.3)

axes[2].set_ylabel("Ion density")
axes[2].legend(loc="upper right")
axes[2].grid(True, alpha=0.3)

axes[3].set_ylabel("σ_eff")
axes[3].legend(loc="upper right")
axes[3].grid(True, alpha=0.3)

axes[4].set_ylabel("Luminosity proxy")
axes[4].set_xlabel("Time (s)")
axes[4].legend(loc="upper right")
axes[4].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("fluid_dynamics_extended.png", dpi=150)
plt.show()

# ------------------------------------------------------------------
# Console summary
# ------------------------------------------------------------------
print("=== RVR Extended Fluid + Charge + Ionization ===")
print(f"{'Fluid':<22} {'Peak v':>8} {'Final v':>8} {'Final q':>11} {'Final ni':>11} {'Luma':>10}")
print("-" * 75)
for key, sol in results.items():
    v, p, q, ni = sol.y
    _, luma = derived(sol, key)
    print(
        f"{fluids[key]['label']:<22} {np.max(v):8.2f} {v[-1]:8.2f} "
        f"{q[-1]:11.3e} {ni[-1]:11.3e} {luma[-1]:10.3e}"
    )

print("\nMercury is simulation-only (triboelectric / ionization benchmark).")
print("Plot saved as fluid_dynamics_extended.png")
# Simulations

Python simulation suite for the Resonant Vortex Reactor (Gali-Spinal Tube).

## Main Scripts

| Script | Description |
|--------|-------------|
| `gali_spinal_cfd_dem_lbm.py` | Combined CFD-DEM + Lattice Boltzmann simulation of the magnetite sphere chain (recommended starting point) |
| `full_multi_test_dashboard_dmso_tree_sap.py` | Multi-test dashboard with fluid options |
| `fluid_dynamics.py` | Basic fluid dynamics model |
| `fluid_dynamics_with_csv.py` | Fluid dynamics with CSV output |
| `Torsion-like Torque_Anomaly_Simulation_v3.py` | Torsion-like torque exploration |
| `MHD_Lorentz_Sim.py` | Magnetohydrodynamic Lorentz force model |
| `Healing_head_sim.py` | Molecular Healing Head variant |
| `node_phase_shift_sim.py` | Node phase-shift behavior |
| `Schumann_harmonics_sim.py` | Schumann resonance harmonics |
| `closed loop piezo RL shunt.py` | Adaptive piezoelectric shunt with fluid loading |

## CFD-DEM + LBM Module

`gali_spinal_cfd_dem_lbm.py` is the primary physics simulation. It includes:

- D3Q19 Lattice Boltzmann fluid solver
- Discrete Element Method (DEM) for magnetite spheres
- Magnetic dipole–dipole forces
- Soft-sphere contact model
- Two-way momentum coupling
- Axial + rotational (whip) drive
- Optional synchronized snap impulses

### Quick Start

```bash
python gali_spinal_cfd_dem_lbm.py

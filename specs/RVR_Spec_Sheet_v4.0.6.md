# Resonant Vortex Reactor — Main Specification (v4.0.6)

**Status:** Active development — July 2026  
**Focus:** Modular platform architecture, MHD principles, materials, and development roadmap.

---

## Overview

The Resonant Vortex Reactor (RVR) is a modular conceptual platform built around the **Gali-Spinal Tube** architecture. It explores sustained twist-force standing waves, external centroid stability, and potential coupling to time-particle dynamics through macroscopic rotating magnetic-fluid systems.

Two primary head configurations are defined:

- **Molecular Healing Head (v4.1)** — Restorative, time-reversal-dominant operation with gentler coherence effects.
- **Magnetic Plasma Production Head (v4.0.6)** — Energy-oriented, time-forward-dominant operation with higher-intensity dynamics.

---

## Governing Physics

### Magnetohydrodynamic (MHD) Self-Sustaining Loop

The core mechanism relies on Lorentz-driven circulation of a conductive fluid (Galinstan or ionized carrier) through a structured magnetic field.

**Governing Force Balance (at equilibrium):**

When the Lorentz drive term balances fluid drag, a self-sustaining circulation can be maintained with minimal external input once initiated.

Key parameters:
- `σ` — Electrical conductivity of the working fluid
- `B` — Magnetic field strength from the ferrite core and return path
- `V`, `L` — Characteristic velocity and length scales
- `C_d`, `ρ`, `A` — Drag coefficient, density, and cross-sectional area

---

## Materials

| Component                  | Material                          | Key Properties                          | Notes |
|----------------------------|-----------------------------------|-----------------------------------------|-------|
| Structural tube            | Titanium carbide (TiC) + PTFE     | High strength, chemical inertness, low friction | Primary containment |
| Magnetite spheres          | Purified Fe₃O₄ (2–8 mm)           | High magnetic susceptibility            | Chain for twist-force generation |
| Core                       | Double-headed sliced ferrite      | Strong localized field                  | Starburst geometry |
| Magnetic return path       | Pure iron                         | High permeability, low losses           | Closes the magnetic circuit |
| Carrier fluid (variant)    | Deionized/dark water or Galinstan | Tunable conductivity and viscosity      | Healing vs. energy heads |
| Whip base (v4.3.2)         | Nitinol or 316L + microchannels   | Resonant mechanical properties          | Car-antenna style whip |

---

## Development Roadmap

- v4.0.6 — Magnetic Plasma Production Head baseline + initial MHD simulations
- v4.1 — Molecular Healing Head with Schumann + healing harmonic tuning
- v4.3.2 — Gali-Spinal Tube with car-antenna whip base and detailed resonance analysis
- v4+ — Experimental testing protocols and prototype refinement
- Future — Multi-unit phase-locking, environmental coupling studies, Observationalist integration concepts

---

## Related Documents

- `specs/v4.3.2.md` — Detailed Gali-Spinal Tube v4.3.2 construction and performance
- `Time-particle-theory.md` — Theoretical foundation (rigid-body instants, twist-force, dual polarity)
- `Experimental Testing – Torsion-like Signatures (v4+).md` — Proposed test protocols
- `simulations/` — Python stubs for MHD loop, harmonic fields, and healing coherence

---

**Status:** Living specification. Subject to iterative refinement as simulations, theory, and prototype work progress.

**Locked in.**
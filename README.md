<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Resonant Vortex Reactor — Gali Spinal Tube v5

Modular magneto-fluid platform: sealed TiC + PTFE column, magnetite sphere chain, DRSSTC-coupled resonance, dual Energy / Healing heads.

**Current line (September 2026):** Gali Spinal Tube **v5.0** is the column spec. **Sphere Head Loop v7.1** is the new head geometry (spinning wrap on a motionless hub). v4 remains in `specs/` as history.

How to read this repo: [docs/00-how-to-read.md](docs/00-how-to-read.md)  
Fact / Design / Vision stay separate.

---

## Status

Early-stage exploratory project. Architecture and materials are specified. Simulations exist. Bench parts and jar tests are in progress.

**Not claiming:** finished energy device, medical device, over-unity, or confirmed Time Particle Theory.

---

## What v5 is

Vertical sealed column:

- TiC outer wall + PTFE liner
- Size-scaled magnetite spheres (2–8 mm class)
- Carrier family: DMSO mix (Galinstan path optional / later)
- Unbalanced whip / antenna base
- Ferrite base + iron return (column) or N/S through the head (v7.1)
- DRSSTC driver on the column (IGBT bridge, MHz lock)
- Dual heads: Energy (ionizing) / Molecular Healing (softer envelope)

Full sheet: [specs/v5.0 Gali Spinal Tube.md](specs/v5.0%20Gali%20Spinal%20Tube.md)

---

## Head branch — Sphere Head Loop v7.1

Not a cap on the v5 tube. The head *is* the magnetic circuit:

- Lattice / wrap **spins**
- **Stationary hub** fixed to the spine
- Spheres lock on the race as it spins
- Whip of the springy steel antenna sends spheres north
- v7.2 sketches: double-sided serpentine tubes, split fluid, external snap weights

Page: [docs/variants/sphere-head-loop-v7.1.md](docs/variants/sphere-head-loop-v7.1.md)  
Catalog: [docs/variants/README.md](docs/variants/README.md)

---

## Physics in use (Fact)

- Centrifugal seating in a spinning race: \(a = \omega^2 r\)
- Lorentz / MHD on a conductor in **B**: \(\mathbf{f} = \mathbf{J}\times\mathbf{B}\)
- Unbalance force on snap weights: \(F = m e \omega^2\)
- Cavitation and sonoluminescence are real lab effects — not automatic in this device
- Drive vs drag sketch (not a surplus-energy proof):

\[
m\frac{dv}{dt} = (\sigma V B^{2} L)\,v - C_d\rho A v^{2}
\]

---

## Repo map

| Path | What |
| --- | --- |
| [docs/00-how-to-read.md](docs/00-how-to-read.md) | Fact / Design / Vision |
| [docs/variants/](docs/variants/) | Heads and scale variants |
| [docs/sketches/](docs/sketches/) | Notebook photos (add files here) |
| [specs/](specs/) | v4.x history through v5.0 |
| [simulations/](simulations/) | Python stubs and benches |
| [Time-particle-theory.md](Time-particle-theory.md) | Vision layer — labeled speculative |

---

## Next bench

1. DMSO + water/sap jar + a few magnetic spheres — mix or layers, roll or clump
2. Dry beads + whip — do they climb north
3. Photo of the wrap sketch into `docs/sketches/`

---

## License

See [License.md](License.md).python script_name.py
python script_name.py

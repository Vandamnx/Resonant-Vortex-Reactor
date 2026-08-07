def map_particles_to_fluid(particles, fluid_grid, cell_size):
    """
    Simple Particle-In-Cell style mapping.
    fluid_grid is a 3-D array of FluidCell.
    """
    # Reset
    for cell in fluid_grid.flat:
        cell.epsilon = 1.0
        cell.force_p2f[:] = 0.0

    inv_cell_vol = 1.0 / (cell_size**3)

    for p in particles:
        # Find cell index
        idx = np.floor((p.pos - domain_min) / cell_size).astype(int)
        idx = np.clip(idx, 0, np.array(fluid_grid.shape) - 1)

        cell = fluid_grid[tuple(idx)]

        # Volume occupied by particle
        vol_p = (4/3) * np.pi * p.radius**3
        cell.epsilon -= vol_p * inv_cell_vol
        cell.epsilon = max(cell.epsilon, 0.05)   # avoid division by zero

        # Momentum source (drag reaction)
        # We store the opposite of the force the fluid exerted on the particle
        # (this will be computed after drag is known)
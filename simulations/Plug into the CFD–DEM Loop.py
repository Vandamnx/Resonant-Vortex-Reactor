# Inside the coupling section of the main loop:

# A. Build force field from particles (Particle → Fluid)
force_field = np.zeros((nx, ny, nz, 3))
# ... map each particle's -drag force into the surrounding cells ...

# B. Optional void fraction field
epsilon_field = np.ones((nx, ny, nz))
# ... subtract particle volumes ...

# C. Advance fluid one LBM step
f, rho, ux, uy, uz = lbm_step(f, force_field, tau=0.8, epsilon=epsilon_field)

# D. Particles now read the new fluid velocity
# (interpolate ux,uy,uz at each particle position for the next DEM drag calculation)
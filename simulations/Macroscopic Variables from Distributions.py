def compute_macro(f):
    """f shape: (nx, ny, nz, 19)"""
    rho = np.sum(f, axis=-1)                          # density
    ux  = np.sum(f * c[:,0], axis=-1) / rho
    uy  = np.sum(f * c[:,1], axis=-1) / rho
    uz  = np.sum(f * c[:,2], axis=-1) / rho
    return rho, ux, uy, uz
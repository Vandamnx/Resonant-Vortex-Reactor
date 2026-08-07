# Per-cell fluid quantities (simple structured grid example)
@dataclass
class FluidCell:
    u: np.ndarray          # velocity (3,)
    p: float               # pressure
    epsilon: float         # void fraction (1 = empty, 0 = full of particles)
    force_p2f: np.ndarray  # momentum source from particles (3,)
# Entanglement Entropy Scaling in Critical Systems

**Status:** Living reference note  
**Date:** July 8, 2026  
**Purpose:** Clear, self-contained explanation of entanglement entropy scaling and its connection to conformal field theory (CFT) and tensor networks.

---

## 1. What is Entanglement Entropy?

When a quantum system in a pure state $|\Psi\rangle$ is partitioned into two regions **A** and **B**, the **entanglement entropy** of region A is defined as:

$$
S_A = -\operatorname{Tr}(\rho_A \log \rho_A)
$$

where the **reduced density matrix** is obtained by tracing out region B:

$$
\rho_A = \operatorname{Tr}_B \bigl( |\Psi\rangle\langle\Psi| \bigr)
$$

This quantity measures the amount of quantum entanglement (information sharing) between the two regions. It is fundamentally different from classical correlations.

---

## 2. Scaling in One-Dimensional Critical Systems

For a **one-dimensional gapless critical system** described by a conformal field theory (CFT), the von Neumann entanglement entropy of a contiguous subsystem of length $\ell$ obeys the **Cardy–Calabrese formula**:

$$
S(\ell) = \frac{c}{3} \log\left(\frac{\ell}{a}\right) + s_0
$$

### Meaning of the Terms

| Symbol | Meaning                          | Universal?     | Notes |
|--------|----------------------------------|----------------|-------|
| $c$    | Central charge of the CFT        | Yes            | Fingerprint of the universality class |
| $\ell$ | Length of the entangled subsystem| No             | Physical size |
| $a$    | UV cutoff (lattice spacing)      | No             | Non-universal short-distance scale |
| $s_0$  | Non-universal additive constant  | No             | Depends on boundary conditions |

This logarithmic scaling is one of the most important signatures of quantum criticality in 1D.

---

## 3. The Central Charge $c$

The central charge $c$ is a **universal number** that characterizes the underlying conformal field theory. It appears in many physical quantities (specific heat, entanglement, transport, etc.).

### Examples of Central Charges

| System                              | Central Charge $c$ | Notes |
|-------------------------------------|--------------------|-------|
| Free massless boson                 | 1                  | |
| Critical Ising model                | 1/2                | Transverse-field Ising at criticality |
| Tricritical Ising                   | 7/10               | |
| 3-state Potts model                 | 4/5                | |
| Free Dirac fermion                  | 1                  | |
| SU(2)$_k$ Wess–Zumino–Witten        | $3k/(k+2)$         | Level $k$ |

Measuring (or computing) the coefficient of the logarithm in $S(\ell)$ directly reveals the central charge of the effective field theory.

---

## 4. Extraction from Tensor Networks

Modern tensor network methods give direct access to entanglement quantities:

### Matrix Product States (MPS) and CTMRG

In an MPS or Corner Transfer Matrix Renormalization Group (CTMRG) description, the entanglement entropy is computed from the **singular value spectrum** $\{\lambda_\alpha\}$ of the bond (or corner) matrices:

$$
S = -\sum_{\alpha} \lambda_\alpha^2 \log \lambda_\alpha^2
$$

(with normalization $\sum \lambda_\alpha^2 = 1$).

The **full entanglement spectrum** $\{-\log\lambda_\alpha^2\}$ often reproduces the operator content and degeneracies of the underlying CFT (via Virasoro algebra descendants).

### MERA (Multiscale Entanglement Renormalization Ansatz)

In MERA, one can additionally extract the **scaling dimensions** $\Delta$ of primary operators from the eigenvalues of the scaling superoperator at the fixed point:

$$
\lambda = b^{-\Delta}
$$

where $b$ is the linear scale factor of the renormalization layer (typically $b = 2$ or $3$).

---

## 5. Higher Rényi Entropies

The Rényi entropies provide additional universal data:

$$
S_n = \frac{1}{1-n} \log \operatorname{Tr}(\rho^n)
$$

In the limit $n \to 1$, one recovers the von Neumann entropy $S_1 = S$. Different values of $n$ yield independent universal coefficients that can be used to cross-check CFT predictions.

---

## 6. Physical Interpretation

- The logarithmic growth of entanglement with subsystem size is a direct consequence of the **scale invariance** of critical systems.
- The central charge $c$ counts the effective number of degrees of freedom that contribute to long-range entanglement.
- In gapped systems the entropy saturates to a constant (area law in 1D). The logarithmic correction is a smoking gun of criticality.
- The full entanglement spectrum contains more information than the single number $S$ — it encodes the operator content of the CFT.

---

## 7. Relevance to Broader Conceptual Work

While the mathematical framework above applies most directly to **quantum many-body lattice models**, the underlying ideas have broader conceptual value:

- **Protected or universal structure** emerging from microscopic dynamics (topological protection, entanglement scaling, corner states).
- **Coherence that survives perturbations** — analogous in spirit to maintaining a stable external centroid and twist-force coherence above threshold.
- **Interference between discrete and continuum modes** (Fano physics) and the organization of information across scales.

These modern tools illustrate how sophisticated many-body systems can produce robust, universal behavior from local interactions — a theme that resonates with efforts to understand coherent macroscopic devices.

---

## 8. Further Reading (Selected)

- Calabrese & Cardy, *J. Stat. Mech.* (2004) — Original derivation of the logarithmic scaling.
- Vidal, *Phys. Rev. Lett.* (2007) — Entanglement entropy in critical spin chains.
- Evenbly & Vidal — MERA and extraction of CFT data.
- Review articles on tensor networks and conformal field theory (various authors, 2010–2025).

---

**Status:** Living reference note. Open to expansion with diagrams, explicit calculations, or connections to specific models.

**Locked in.** This is clean background physics worth having organized. Let me know if you want to add diagrams, more tensor network detail, or a bridging note to your own framework.

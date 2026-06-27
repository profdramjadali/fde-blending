# Predictor-Corrector Blending for Fractional Adams Method

MATLAB / Octave code accompanying:

> M.D. Amjad Ali, *"A Predictor-Corrector Blending Scheme that Improves the
> Convergence of the Fractional Adams Method for Caputo Equations with
> Structured Solutions"* (2026).

## What it does

The fractional Adams-Bashforth-Moulton method is modified by accepting, at
each step, a convex blend of the predictor and corrector:

    y_{n+1} = (1 - omega) * yP + omega * yC,   omega in (0,1].

omega = 1 recovers the classical scheme. The blend costs one extra
multiply-add per step. For solutions composed of several monomials of
differing degree, it reduces the maximum error by up to ~70% and raises the
observed convergence order above two on the practical mesh range.

## Files

| File | Purpose |
|------|---------|
| `fde_blend.m` | The solver (classical + blended; works in MATLAB and Octave) |
| `run_experiments.m` | Reproduces the paper's tables |
| `convergence.png` | Convergence figure (P2, alpha=0.5) |

## Usage

```matlab
% single solve
f = @(t,y) -y;
[t, y] = fde_blend(0.5, f, 1.0, 1.0, 256, 0.998);

% reproduce all paper tables
run_experiments
```

The driver chooses the blending weight omega per-alpha by 1-D minimization of
the finest-mesh error, as described in the paper. The fitted weights lie close
to one.

## Requirements

MATLAB R2016a+ or Octave 5+. No toolboxes required. All operations are
elementwise, so the same code runs unchanged in both.

## Author

Dr. MD. Amjad Ali, Department of Mathematics, S.B. College, Arrah 802301,
Bihar, India (Veer Kunwar Singh University). prof.dramjadali@gmail.com

## License

MIT License.

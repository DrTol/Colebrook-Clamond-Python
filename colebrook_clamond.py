# -*- coding: utf-8 -*-
"""
Colebrook friction factor via Clamond's quartic iterations (2008).

Developed on Fri Aug 29 20:19:22 2025

@author: Dr. Hakan İbrahim Tol

f_clamond(R, K=0.0, iters=2)
- R: Reynolds number (scalar or array), recommended R >= 2300 (turbulent).
- K: relative roughness epsilon/D (scalar or array, broadcastable with R), K >= 0.
- iters: number of quartic iterations; 2 achieves ~machine precision in double.

Returns:
- Darcy–Weisbach friction factor f (same shape as broadcasted R, K).

Reference:
Clamond, D. "Efficient resolution of the Colebrook equation", arXiv:0810.5564 (2008).

"""

import numpy as np
import warnings

# Constants used by Clamond’s scheme
_LOG10 = np.log(10.0)                       # ln(10)
_C1 = _LOG10 / 18.574                       # 0.123968186335417556
_C2 = np.log(1.0 / 5.02) + np.log(_LOG10)   # ln(ln(10)/5.02) = -0.779397488455682028
_A  = 1.151292546497022842                  # 0.5*ln(10) used in final mapping

def f_clamond(R, K=0.0, iters: int = 2):
    """
    Compute Darcy–Weisbach friction factor using Clamond's algorithm (quartic iterations).

    Parameters
    ----------
    R : float or np.ndarray
        Reynolds number (R > 0; turbulent validity typically R >= 2300).
    K : float or np.ndarray, optional
        Relative roughness epsilon/D (K >= 0). Default is 0.0.
    iters : int, optional
        Number of quartic iterations (>= 0). Default 2 (per paper).

    Returns
    -------
    f : float or np.ndarray
        Darcy–Weisbach friction factor (same shape as broadcasted R and K).
    """
    R = np.asarray(R, dtype=np.float64)
    K = np.asarray(K, dtype=np.float64)

    if np.any(R <= 0):
        raise ValueError("Reynolds number R must be positive.")
    if np.any(K < 0):
        raise ValueError("Relative roughness K must be non-negative.")
    if iters < 0:
        raise ValueError("iters must be >= 0.")

    # Practical validity note (Colebrook is turbulent): warn but proceed
    if np.any(R < 2300):
        warnings.warn("Colebrook equation is for turbulent flow (R >= 2300).", RuntimeWarning)

    # Vectorized initialization (X1, X2 same as paper)
    X1 = K * R * _C1                      # = K*R*ln(10)/18.574
    X2 = np.log(R) + _C2                  # = ln(R*ln(10)/5.02)

    # Initial guess F (named 'F' in Clamond's MATLAB/Fortran)
    F = X2 - 0.2

    # Ensure domain for log(X1 + F) remains valid during iterations
    # If not, raise a clear error (this should not happen for physical R,K with the standard initialization).
    def _check_log_domain(F_current):
        if np.any((X1 + F_current) <= 0.0):
            raise FloatingPointError(
                "Log domain error: X1 + F <= 0 in iteration. "
                "Check R, K values (R>3 is recommended in the paper) or reduce iters."
            )

    # Quartic iterations (usually 1–2 are enough for machine precision)
    for _ in range(iters):
        _check_log_domain(F)
        E = (np.log(X1 + F) + F - X2) / (1.0 + X1 + F)
        F = F - (1.0 + X1 + F + 0.5 * E) * E * (X1 + F) / (1.0 + X1 + F + E * (1.0 + E / 3.0))

    # Final mapping: f = ( (0.5*ln(10))/F )^2
    f = (_A / F) ** 2

    # Return scalar if input was scalar
    if f.shape == () and np.isscalar(R) and np.isscalar(K):
        return float(f)
    return f

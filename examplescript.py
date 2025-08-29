# -*- coding: utf-8 -*-
"""
Examples for computing Darcy–Weisbach friction factor using Clamond's algorithm
(colebrook_clamond.f_clamond). Focused on District Heating (DH) pipe cases.

Developed on Fri Aug 29 20:21:51 2025

@author: Dr. Hakan İbrahim Tol

Outputs per scenario:
- Reynolds number R
- Relative roughness K = epsilon / D
- Friction factor f (Darcy–Weisbach)
- Pressure gradient dp/dx = f * rho * V^2 / (2 * D)

Reference:
Clamond, D. "Efficient resolution of the Colebrook equation", arXiv:0810.5564 (2008).

"""
from colebrook_clamond import f_clamond
import numpy as np

""" SIMPLE EXAMPLE """

# Scalar
print(f_clamond(7e5, 0.01))     # ~ friction factor

# Arrays
R = np.array([3e3, 7e5, 1e7])
K = 0.01
print(f_clamond(R, K))          # vector output

""" EXAMPLE | DISTRICT HEATING """

# --------------------------- Helpers ---------------------------

def reynolds_number(rho: float, V: float, D: float, mu: float) -> float:
    """
    Compute Reynolds number: R = rho * V * D / mu

    Parameters
    ----------
    rho : fluid density [kg/m^3]
    V   : mean velocity [m/s]
    D   : inner diameter [m]
    mu  : dynamic viscosity [Pa·s = kg/(m·s)]

    Returns
    -------
    R : float
    """
    return (rho * V * D) / mu


def pressure_gradient(f: float, rho: float, V: float, D: float) -> float:
    """
    Darcy–Weisbach pressure gradient [Pa/m]: dp/dx = f * rho * V^2 / (2 * D)
    """
    return f * rho * V * V / (2.0 * D)

# --------------------------- DH-Oriented Constants ---------------------------

# Inner diameters (typical DH selections; adjust to your catalog as needed)
D_SERVICE = 0.050     # 50 mm service connection (approx inner diameter) [m]
D_FEEDER  = 0.100     # 100 mm feeder [m]
D_MAIN    = 0.200     # 200 mm main [m]

# Absolute roughness (commercial steel/new DH steel pipes; order 0.045–0.05 mm)
EPS_NEW_STEEL = 0.00005   # 0.05 mm [m]
# Older/roughened pipe example
EPS_OLD_STEEL = 0.00020   # 0.20 mm [m]

# Water properties (approximate) at common DH temps
# Source: standard engineering tables (rounded)
WATER_20C = dict(rho=998.0,  mu=1.002e-3)  # 20 °C
WATER_60C = dict(rho=983.0,  mu=0.467e-3)  # 60 °C
WATER_80C = dict(rho=971.0,  mu=0.355e-3)  # 80 °C

# --------------------------- Example Scenarios ---------------------------

def build_scenarios():
    """
    Build a list of contrasting DH scenarios to highlight the effects of
    diameter, roughness, velocity and temperature on f and dp/dx.
    """
    scenarios = [
        dict(
            name="S1: Service pipe, new steel, moderate V, 60°C",
            D=D_SERVICE, epsilon=EPS_NEW_STEEL, V=1.0, **WATER_60C
        ),
        dict(
            name="S2: Feeder pipe, new steel, higher V, 60°C",
            D=D_FEEDER, epsilon=EPS_NEW_STEEL, V=1.5, **WATER_60C
        ),
        dict(
            name="S3: Main pipe, new steel, typical V, 60°C",
            D=D_MAIN, epsilon=EPS_NEW_STEEL, V=1.5, **WATER_60C
        ),
        dict(
            name="S4: Service pipe, OLD steel (rough), moderate V, 60°C",
            D=D_SERVICE, epsilon=EPS_OLD_STEEL, V=1.0, **WATER_60C
        ),
        dict(
            name="S5: Feeder pipe, new steel, same V as S2 but 20°C (higher viscosity)",
            D=D_FEEDER, epsilon=EPS_NEW_STEEL, V=1.5, **WATER_20C
        ),
        dict(
            name="S6: Feeder pipe, new steel, same V as S2 but 80°C (lower viscosity)",
            D=D_FEEDER, epsilon=EPS_NEW_STEEL, V=1.5, **WATER_80C
        ),
    ]
    return scenarios


def run_scenarios(iters: int = 2):
    """
    Run all scenarios and print a compact table.
    iters: number of Clamond iterations (default 2 per the paper).
    """
    print(f"\nClamond Colebrook solver — iterations = {iters}\n")
    header = (
        f"{'Case':38s}  {'D [m]':>6s}  {'eps [mm]':>8s}  {'K=eps/D':>9s}  "
        f"{'V [m/s]':>7s}  {'rho [kg/m3]':>11s}  {'mu [mPa·s]':>10s}  {'R [-]':>12s}  "
        f"{'f [-]':>10s}  {'dp/dx [Pa/m]':>14s}"
    )
    print(header)
    print("-" * len(header))

    for sc in build_scenarios():
        D = sc["D"]
        eps = sc["epsilon"]
        V = sc["V"]
        rho = sc["rho"]
        mu = sc["mu"]

        R = reynolds_number(rho=rho, V=V, D=D, mu=mu)
        K = eps / D
        f = f_clamond(R, K, iters=iters)
        dpdx = pressure_gradient(f=f, rho=rho, V=V, D=D)

        print(
            f"{sc['name']:38s}  "
            f"{D:6.3f}  {eps*1e3:8.3f}  {K:9.5f}  "
            f"{V:7.3f}  {rho:11.1f}  {mu*1e3:10.3f}  {R:12.0f}  "
            f"{f:10.5f}  {dpdx:14.1f}"
        )


def compare_iterations():
    """
    Show how much (or little) results change with iters = 1 vs 2.
    Uses one representative scenario.
    """
    sc = dict(
        name="Feeder pipe, new steel, V=1.5 m/s, 60°C",
        D=D_FEEDER, epsilon=EPS_NEW_STEEL, V=1.5, **WATER_60C
    )
    D, eps, V, rho, mu = sc["D"], sc["epsilon"], sc["V"], sc["rho"], sc["mu"]
    R = reynolds_number(rho=rho, V=V, D=D, mu=mu)
    K = eps / D

    f1 = f_clamond(R, K, iters=1)
    f2 = f_clamond(R, K, iters=2)
    dp1 = pressure_gradient(f1, rho, V, D)
    dp2 = pressure_gradient(f2, rho, V, D)

    print("\nIteration sensitivity (iters=1 vs iters=2):")
    print(f"  R = {R:.0f}, K = {K:.5f}")
    print(f"  f(iters=1) = {f1:.8f},  dp/dx = {dp1:.2f} Pa/m")
    print(f"  f(iters=2) = {f2:.8f},  dp/dx = {dp2:.2f} Pa/m")
    rel = abs(f2 - f1) / f2 if f2 != 0 else np.nan
    print(f"  Relative difference in f: {rel:.3e}")


def main():
    # Default: two iterations (paper’s recommendation ~ machine precision)
    run_scenarios(iters=2)

    # (Optional) show effect of using fewer iterations:
    compare_iterations()

    # If you want to experiment:
    # run_scenarios(iters=1)  # faster, still very accurate for most cases
    # run_scenarios(iters=0)  # initial guess only (generally too rough)


if __name__ == "__main__":
    main()
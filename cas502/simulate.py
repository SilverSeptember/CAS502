"""This is the simulation runner for the CAS502 measles SIRS model.

This module is completely independent of the GUI — it returns data and never
plots.  The two main public objects are:

* ``Parameters`` is a dataclass holding every tuneable value with measles-like
  defaults and computed properties that stay consistent when base values change.
* ``run_simulation(params)`` — runs all three ODE integrations plus the
  coverage sweep and returns a ``SimulationResults`` container.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass

import numpy as np
from scipy.integrate import odeint

from cas502.model import (
    phi_I_combined,
    sir_rhs,
    sirs_rhs,
    sirs_rhs_migration,
)


#Parameters:

@dataclass
class Parameters:
    """All simulation parameters with measles-like defaults.

    Computed quantities (``beta0``, ``N_star``, ``Lambda``, ``t``) are exposed
    as ``@property`` methods so they stay consistent when base values change.
    """

    # Time grid
    t_max: float = 520.0          # weeks (10 years)
    t_points: int = 5201

    # Epidemiology
    gamma: float = 1.0            # recovery rate (1/week infectious period)
    R0_target: float = 15.0       # basic reproduction number

    # Waning immunity
    lam: float = 1.0 / (5.0 * 52.0)  # ~5-year duration

    # Vaccination
    coverage: float = 0.9126      # fraction of newborns vaccinated at birth
    nu: float = 0.005             # catch-up vaccination rate (per week)

    # Demography & disease mortality
    mu: float = 1.0 / (70.0 * 52.0)  # ~70-year life expectancy
    delta: float = 0.0002         # disease-induced mortality (per week)

    # Seasonality
    seasonal_amp: float = 0.12
    seasonal_T: float = 52.0

    # Initial conditions (counts)
    S0c: float = 9.9e5
    I0c: float = 100.0
    R0c: float = 0.0

    # Importation parameters
    eta_I: float = 0.05
    pulse_mag: float = 50.0
    pulse_times: tuple = (130.0, 390.0)
    pulse_half_width: float = 0.5

    # Migration flows (all zero by default)
    MS_in: float = 0.0
    MS_out: float = 0.0
    MI_in: float = 0.0
    MI_out: float = 0.0
    MR_in: float = 0.0
    MR_out: float = 0.0

    # Coverage sweep
    cov_low: float = 0.80
    cov_high: float = 0.98
    cov_points: int = 10

    # Proportional initial conditions
    S0p: float = 0.99
    I0p: float = 0.01
    R0p: float = 0.0

    # ── computed properties ──

    @property
    def beta0(self) -> float:
        return self.R0_target * self.gamma

    @property
    def N_star(self) -> float:
        return self.S0c + self.I0c + self.R0c

    @property
    def Lambda(self) -> float:
        """Birth rate chosen to balance deaths on average."""
        return self.mu * self.N_star

    @property
    def t(self) -> np.ndarray:
        return np.linspace(0, self.t_max, self.t_points)


#  Results container:  

@dataclass
class SimulationResults:
    """Container for all simulation outputs."""

    # Time grid
    t: np.ndarray

    # SIR / SIRS baseline solutions (proportions)
    sol_sir: np.ndarray
    sol_sirs: np.ndarray

    # Extended SIRS solution (counts)
    sol_ext: np.ndarray

    # Derived arrays
    S_c: np.ndarray
    I_c: np.ndarray
    R_c: np.ndarray
    N_c: np.ndarray
    Sp: np.ndarray
    Ip: np.ndarray
    Rp: np.ndarray

    # Summary scalars
    peak_I: float
    t_peak: float

    # Coverage sweep
    coverages: np.ndarray
    peaks: np.ndarray


#  helper  

def make_phi_func(params: Parameters):
    """Return a one-argument ``phi(t)`` from the parameterised importation."""
    return functools.partial(
        phi_I_combined,
        eta_I=params.eta_I,
        pulse_mag=params.pulse_mag,
        pulse_times=params.pulse_times,
        pulse_half_width=params.pulse_half_width,
    )


#   Main entry point 

def run_simulation(params: Parameters | None = None) -> SimulationResults:
    """Run all three ODE integrations and the coverage sweep.

    Returns a ``SimulationResults`` instance.  If *params* is ``None`` the
    measles-like defaults are used.
    """
    if params is None:
        params = Parameters()

    t = params.t
    beta0 = params.beta0
    gamma = params.gamma
    lam = params.lam
    nu = params.nu
    coverage = params.coverage
    seasonal_amp = params.seasonal_amp
    seasonal_T = params.seasonal_T
    mu = params.mu
    delta = params.delta
    Lambda = params.Lambda
    S0c, I0c, R0c = params.S0c, params.I0c, params.R0c

    phi_func = make_phi_func(params)

    # ── 1. SIR vs SIRS (proportions) ──
    y0p = [params.S0p, params.I0p, params.R0p]
    sol_sir = odeint(sir_rhs, y0p, t, args=(beta0, gamma))
    sol_sirs = odeint(sirs_rhs, y0p, t,
                      args=(beta0, gamma, lam, 0.0, seasonal_amp, seasonal_T))

    # ── 2. Extended SIRS (counts) ──
    y0c = [S0c, I0c, R0c]
    sol_ext = odeint(
        sirs_rhs_migration, y0c, t,
        args=(beta0, gamma, lam, nu,
              seasonal_amp, seasonal_T,
              Lambda, mu, delta,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              phi_func,
              coverage)
    )
    S_c, I_c, R_c = sol_ext.T
    N_c = S_c + I_c + R_c
    Sp, Ip, Rp = S_c / N_c, I_c / N_c, R_c / N_c

    peak_I = float(np.max(I_c))
    t_peak = float(t[np.argmax(I_c)])

    # ── 3. Coverage sweep ──
    coverages = np.linspace(params.cov_low, params.cov_high, params.cov_points)
    peaks = []
    for cov in coverages:
        sol_tmp = odeint(
            sirs_rhs_migration, y0c, t,
            args=(beta0, gamma, lam, nu, seasonal_amp, seasonal_T,
                  Lambda, mu, delta, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  phi_func, cov)
        )
        peaks.append(sol_tmp[:, 1].max() / (sol_tmp.sum(axis=1).max()))
    peaks = np.array(peaks)

    return SimulationResults(
        t=t,
        sol_sir=sol_sir,
        sol_sirs=sol_sirs,
        sol_ext=sol_ext,
        S_c=S_c, I_c=I_c, R_c=R_c, N_c=N_c,
        Sp=Sp, Ip=Ip, Rp=Rp,
        peak_I=peak_I, t_peak=t_peak,
        coverages=coverages, peaks=peaks,
    )

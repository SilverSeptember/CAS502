"""CAS502 — Epidemiological ODE models for measles (SIR / SIRS / SIRS+migration).

Time unit: weeks.  All transmission functions and righthand sides arepulled from the original Jupyter code and found here so that ``simulate.py`` and tests can import them without usng any plotting or GUI dependencies. 
"""

import numpy as np


# fmt: off
def beta_t(t, beta0, seasonal_amp = 0.0, seasonal_T = 52.0):
# Seasonal transmission: beta(t) = beta0 * (1 + a * sin(2pi t/T))
	if seasonal_amp == 0.0:
		return beta0
	return beta0 * (1.0 + seasonal_amp * np.sin(2.0 * np.pi * t / seasonal_T))
# fmt: on
  
def beta_t_termtime(t, beta0, b1=0.25, T=52.0, term_weeks=39.0):
    """Term-time (school) forcing with mean-preserving high/low segments.
    In the term weeks the transmision rate is boosted; outside the term it's reduced so that the time-average equals *beta0*.
    """
    p = term_weeks / T
    b_high = b1
    b_low = -(p / (1.0 - p)) * b1
    in_term = (t % T) < term_weeks
    factor = 1.0 + (b_high if in_term else b_low)
    return beta0 * factor


def sir_rhs(y, t, beta0, gamma):
    """Basic SIR right-hand side (proportions, no demography)."""
    S, I, R = y
    dSdt = -beta0 * S * I
    dIdt = beta0 * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def sirs_rhs(y, t, beta0, gamma, lam, nu=0.0, seasonal_amp=0.0, seasonal_T=52.0):
    """SIRS with waning immunity, vaccination, and seasonality (proportions)."""
    S, I, R = y
    b = beta_t(t, beta0, seasonal_amp, seasonal_T)
    dSdt = -b * S * I - nu * S + lam * R
    dIdt = b * S * I - gamma * I
    dRdt = gamma * I + nu * S - lam * R
    return [dSdt, dIdt, dRdt]


def sirs_rhs_migration(y, t,
                       beta0, gamma, lam, nu,
                       seasonal_amp, seasonal_T,
                       Lambda, mu, delta,
                       MS_in, MS_out,
                       MI_in, MI_out,
                       MR_in, MR_out,
                       phi_I_func,
                       coverage):
    """Extended SIRS (COUNTS) with demography, disease mortality, seasonality,importation, and birth vaccination coverage.
    *coverage*: fraction of newborns vaccinated at birth (sent to R instead of S).
    """
    S, I, R = y
    N = max(S + I + R, 1e-12)
    b = beta_t(t, beta0, seasonal_amp, seasonal_T)
    Phi_I = 0.0 if phi_I_func is None else float(phi_I_func(t))
    # Vaccination at birth split
    Lambda_S = (1.0 - coverage) * Lambda
    Lambda_R = coverage * Lambda

    dSdt = (Lambda_S - mu * S - b * (S * I) / N - nu * S + lam * R + MS_in - MS_out)
    dIdt = (b * (S * I) / N - (gamma + mu + delta) * I + Phi_I + MI_in - MI_out)
    dRdt = (gamma * I - mu * R - lam * R + nu * S + Lambda_R + MR_in - MR_out)
    return [dSdt, dIdt, dRdt]


def phi_I_combined(ti, eta_I=0.05, pulse_mag=50.0,
                   pulse_times=(130.0, 390.0), pulse_half_width=0.5):
    """Importation function: constant trickle + optional pulses.

    Parameters:
    
    ti : float
        Current time (weeks).
    eta_I : float
        Background trickle rate of imported infections per week.
    pulse_mag : float
        Magnitude of each pulse event.
    pulse_times : tuple of float
        Times at which pulses occur.
    pulse_half_width : float
        Half-width of each pulse window.
    """
    pulse = 0.0
    for pt in pulse_times:
        if abs(ti - pt) < pulse_half_width:
            pulse = pulse_mag
            break
    return eta_I + pulse

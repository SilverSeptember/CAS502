"""Unit tests forthe beta_t function in cas502/model.py."""

#imports for floating point math and the beta_t function we're testing
import math
from cas502.model import beta_t


"""
This test checks that when seasonality is turned off (seasonal_amp = 0), beta_t returns the baseline transmission rate beta0 unchanged.
This is the simplest possible case in that there is no sine wave modulation, just a constant rate. If this fails, it means that the function is modifying beta0 even when it shouldn't be.
"""
def test_beta_t_no_seasonal_returns_beta0():
    """With no seasonality, beta_t should return beta0"""
    assert beta_t(t=10.0, beta0=3.5, seasonal_amp=0.0, seasonal_T=52.0) == 3.5


"""
This test checks that at the peak of the seasonal sine wave, the transmission rate is increased by the right amount. 
The sine function hits its maximum of 1.0 at t = T/4 (a quarter of the way through the period). At that point, beta(t) should equal beta0 * (1 + seasonal_amp). 
This confirms the seasonal modulation is being applied correctly in the upward direction.
"""
def test_beta_t_at_peak_increases_by_amp():
    """At the sine peak (t = T/4), beta should be beta0 * (1 + amp)."""
    beta0 = 10.0
    a = 0.2
    T = 52.0
    #at t = T/4, sin(2*pi*t/T) = sin(pi/2) = 1.0
    t = T / 4.0
    # so beta(t) = beta0 * (1 + a * 1.0) = beta0 * (1 + a)
    expected = beta0 * (1.0 + a)
    got = beta_t(t=t, beta0=beta0, seasonal_amp=a, seasonal_T=T)
    assert math.isclose(got, expected, rel_tol=0, abs_tol=1e-12)


"""
This test checks the opposite of the peak test — at the trough of the seasonal sine wave, the transmission rate should be reduced by the amplitude. 
The sine function hits its minimum of -1.0 at t = 3T/4 (three quarters through the period). 
At that point beta(t) should equal beta0 * (1 - seasonal_amp). 
Together with the peak test, this confirms the full range of seasonal modulation works correctly in both directions.
"""
def test_beta_t_at_trough_decreases_by_amp():
    """At the sine trough (t = 3T/4),  beta shoud be beta0 * (1 - amp)."""
    beta0 = 10.0
    a = 0.2
    T = 52.0
    #at t = 3T/4, sin(2*pi*t/T) = sin(3*pi/2) = -1.0
    t = 3.0 * T / 4.0
    # so beta(t) = beta0 * (1 + a * (-1.0)) = beta0 * (1 - a)
    expected = beta0 * (1.0 - a)
    got = beta_t(t=t, beta0=beta0, seasonal_amp=a, seasonal_T=T)
    assert math.isclose(got, expected, rel_tol=0, abs_tol=1e-12)



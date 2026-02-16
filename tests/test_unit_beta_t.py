import math 
from cas502.model import beta_t

def test_beta_t_no_seasonal_returns_beta0():
	assert beta_t(t = 10.0, beta0 = 3.5, seasonal_amp = 0.0, seasonal_T = 52.0) == 3.5


def test_beta_t_at_peak_increases_by_amp():
	beta0 = 10.0
	a = 0.2
	T = 52.0 
	t = T / 4.0
	expected = beta0 * (1.0 + a)
	got = beta_t(t=t, beta0=beta0, seasonal_amp=a, seasonal_T=T)
	assert math.isclose(got, expected, rel_tol = 0, abs_tol = 1e-12)

def test_beta_t_at_trough_decreases_by_amp():
	beta0 = 10.0
	a = 0.2
	T = 52.0
	t = 3.0 * T / 4.0
	expected = beta0 * (1.0 - a)
	got = beta_t(t=t, beta0=beta0, seasonal_amp=a, seasonal_T=T)
	assert math.isclose(got, expected, rel_tol = 0, abs_tol = 1e-12)



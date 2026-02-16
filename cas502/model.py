import numpy as np

def beta_t(t, beta0, seasonal_amp = 0.0, seasonal_T = 52.0):
# Seasonal transmission: beta(t) = beta0 * (1 + a * sin(2pi t/T))
	if seasonal_amp == 0.0:
		return beta0
	return beta0 * (1.0 + seasonal_amp * np.sin(2.0 * np.pi * t / seasonal_T))


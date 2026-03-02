"""integration tests for the SIR / SIRS simulation pipeline."""

import numpy as np
import pytest

from cas502.simulate import Parameters


# ── SIR baseline ────────────────────────────────────────────────────────

class TestSIRBaseline:

    def test_proportions_sum_to_one(self, simulation_results):
        sol = simulation_results.sol_sir
        totals = sol.sum(axis=1)
        np.testing.assert_allclose(totals, 1.0, atol=1e-6)

    def test_no_negative_compartments(self, simulation_results):
        # ODE solver may produce tiny negative values (~1e-9) from numerical integration
        assert (simulation_results.sol_sir >= -1e-8).all()

    def test_infection_peaks_then_declines(self, simulation_results):
        I = simulation_results.sol_sir[:, 1]
        peak_idx = np.argmax(I)
        # peak is not at the very end — infection declines after peak
        assert peak_idx < len(I) - 1


# ── SIRS baseline ───────────────────────────────────────────────────────

class TestSIRSBaseline:

    def test_proportions_sum_to_one(self, simulation_results):
        sol = simulation_results.sol_sirs
        totals = sol.sum(axis=1)
        np.testing.assert_allclose(totals, 1.0, atol=1e-6)

    def test_recurrent_waves(self, simulation_results):
        """SIRS with seasonality should show multiple infection peaks."""
        I = simulation_results.sol_sirs[:, 1]
        # Count local maxima (I[i] > I[i-1] and I[i] > I[i+1])
        peaks = 0
        for i in range(1, len(I) - 1):
            if I[i] > I[i - 1] and I[i] > I[i + 1]:
                peaks += 1
        assert peaks >= 2, f"Expected multiple peaks, found {peaks}"


# ── Extended SIRS (counts) ──────────────────────────────────────────────

class TestExtendedSIRS:

    def test_population_positive(self, simulation_results):
        assert (simulation_results.N_c > 0).all()

    def test_peak_I_positive(self, simulation_results):
        assert simulation_results.peak_I > 0

    def test_t_peak_within_range(self, simulation_results):
        assert 0 <= simulation_results.t_peak <= simulation_results.t[-1]

    def test_final_proportions_sum_to_one(self, simulation_results):
        r = simulation_results
        total = r.Sp[-1] + r.Ip[-1] + r.Rp[-1]
        assert abs(total - 1.0) < 1e-6


# ── Coverage sweep ──────────────────────────────────────────────────────

class TestCoverageSweep:

    def test_ten_coverage_points(self, simulation_results):
        assert len(simulation_results.coverages) == 10

    def test_higher_coverage_reduces_peak(self, simulation_results):
        """The peak at the highest coverage should be <= the peak at the lowest."""
        assert simulation_results.peaks[-1] <= simulation_results.peaks[0]

    def test_all_peaks_positive(self, simulation_results):
        assert (simulation_results.peaks > 0).all()


# ── Parameter properties ────────────────────────────────────────────────

class TestParameterProperties:

    def test_beta0_equals_R0_times_gamma(self, default_params):
        assert default_params.beta0 == default_params.R0_target * default_params.gamma

    def test_N_star_sum(self, default_params):
        expected = default_params.S0c + default_params.I0c + default_params.R0c
        assert default_params.N_star == expected

    def test_Lambda_balances_deaths(self, default_params):
        expected = default_params.mu * default_params.N_star
        assert abs(default_params.Lambda - expected) < 1e-12

    def test_time_grid_length(self, default_params):
        assert len(default_params.t) == default_params.t_points

    def test_custom_parameter_overrides(self):
        p = Parameters(R0_target=10.0, gamma=2.0)
        assert p.beta0 == 20.0

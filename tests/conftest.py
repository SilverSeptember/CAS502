"""pytest fixtures for the CAS502 test suite"""

import pytest

from cas502.simulate import Parameters, run_simulation


@pytest.fixture
def default_params():
    """Return a Parameters instance with measles-like defaults."""
    return Parameters()


@pytest.fixture(scope="session")
def simulation_results():
    """run the full simulation once and share across all ofthe tests in the session."""
    return run_simulation()

"""System-level tests: imports, module structure, and script syntax."""

import importlib
import subprocess
import sys

import pytest

def test_package_imports():
    import cas502
    assert hasattr(cas502, "Parameters")
    assert hasattr(cas502, "run_simulation")


def test_model_functions_importable():
    from cas502.model import (
        beta_t,
        beta_t_termtime,
        sir_rhs,
        sirs_rhs,
        sirs_rhs_migration,
        phi_I_combined,
    )

def test_simulate_classes_importable():
    from cas502.simulate import Parameters, SimulationResults, run_simulation


def test_run_simulation_returns_valid_results(simulation_results):
    from cas502.simulate import SimulationResults
    assert isinstance(simulation_results, SimulationResults)
    assert simulation_results.peak_I > 0
    assert len(simulation_results.t) > 0


def test_gui_module_imports():
    try:
        import tkinter  # noqa: F401
    except ImportError:
        pytest.skip("Tkinter not available")
    from cas502.gui import MeaslesGUI, build_narrative_text

def test_build_narrative_text(simulation_results):
    try:
        import tkinter  # noqa: F401
    except ImportError:
        pytest.skip("Tkinter not available")
    from cas502.gui import build_narrative_text
    from cas502.simulate import Parameters

    text = build_narrative_text(Parameters(), simulation_results)
    assert "Disease Parameters:" in text
    assert "Simulation Results:" in text
    assert "Key Relationships:" in text
    assert len(text) > 100


def test_run_model_script_parses():
    """Verify scripts/run_model.py has no syntax errors."""
    result = subprocess.run(
        [sys.executable, "-c", "import py_compile; py_compile.compile('scripts/run_model.py', doraise=True)"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr

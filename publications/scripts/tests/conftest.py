"""Shared fixtures for ISRU model and MC tests."""

import numpy as np
import pytest

from isru_model import BASELINE


@pytest.fixture
def baseline():
    """Return a fresh copy of baseline parameters."""
    return BASELINE.copy()


@pytest.fixture
def rng():
    """Return a seeded random number generator for reproducible tests."""
    return np.random.default_rng(42)


@pytest.fixture
def optimistic_params():
    """Optimistic scenario: low capital, low launch cost."""
    p = BASELINE.copy()
    p["p_launch"] = 500
    p["K"] = 30e9
    return p


@pytest.fixture
def conservative_params():
    """Conservative scenario: high capital, high launch cost."""
    p = BASELINE.copy()
    p["p_launch"] = 2000
    p["K"] = 100e9
    return p

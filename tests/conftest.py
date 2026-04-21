"""
Shared pytest fixtures and configuration for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


# Store the original activities state
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """
    Fixture that provides a FastAPI TestClient for testing the app.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the global activities dictionary to its original state
    before each test. This ensures test isolation by preventing side effects
    from one test affecting another.
    """
    # Reset activities to original state before each test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Clean up after test (not strictly necessary, but good practice)
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))

"""
Root conftest.py for pytest configuration and shared fixtures.
Enables TEST_LOG environment variable for test log isolation.
"""
import os
from io import StringIO
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_logging():
    """Setup TEST_LOG environment variable for test isolation."""
    if "TEST_LOG" not in os.environ:
        os.environ["TEST_LOG"] = "memory"


@pytest.fixture
def test_log_stream():
    """Provide StringIO stream for TEST_LOG output during tests."""
    return StringIO()


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for test files."""
    return tmp_path

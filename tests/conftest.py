"""
    Dummy conftest.py for safe_security_logger.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html

    By convention storing fixutres in this file allows the fixture
    to be accessed by all the modules within the test package.
"""

import io
import logging
import sys

import pytest

import safe_security_logger as logger


@pytest.fixture(scope="class")
def get_safe_security_logger(request) -> logger:
    request.cls.logger: logging.Logger = logger.getLogger("test-safe-logger")


@pytest.fixture(scope="function")
def capture_stdout_output(monkeypatch) -> dict:
    """
    Returns a logoutput dictionary.
    Mocks the standard ouput write and captures data
    from logger.

    Uses monkeypatch fixture to do mocking.
    """
    logoutput: dict = {"record": [], "write_count": 0}

    def fake_write(log_data: str) -> dict:
        logoutput["record"].append(log_data)
        logoutput["write_count"] += 1
        return logoutput

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return logoutput


@pytest.fixture(scope="function")
def capture_open_output(monkeypatch) -> dict:
    logoutput: dict = {"record": [], "write_count": 0}

    def fake_write(log_data: str) -> dict:
        logoutput["record"].append(log_data)
        logoutput["write_count"] += 1
        return logoutput

    monkeypatch.setattr(io, "open", fake_write)
    return logoutput

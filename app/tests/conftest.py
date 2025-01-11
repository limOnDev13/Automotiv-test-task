"""Fixtures for tests."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Return FastAPI TestClient."""
    yield TestClient(app)

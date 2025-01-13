"""Fixtures for tests."""

from datetime import datetime
from typing import Any, Dict, Generator, List

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db.database import Base, engine
from app.db.repositories import HistoryRepository
from app.main import app


@pytest_asyncio.fixture()
async def db():
    """Drop and raise the base before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest.fixture
def history_rep(db):
    """Get the HistoryRepository object."""
    return HistoryRepository()


@pytest.fixture
def client(db) -> Generator[TestClient, None, None]:
    """Return FastAPI TestClient."""
    yield TestClient(app)


@pytest.fixture
def pc_metrics() -> List[Dict[str, Any]]:
    """Get test metrics."""
    return [
        {
            "time": datetime.now(),
            "pc_stats": {
                "CPU": "some_CPU1",
                "RAM": "some_RAM1",
                "ROM": "some_ROM1",
            },
        },
        {
            "time": datetime.now(),
            "pc_stats": {
                "CPU": "some_CPU2",
                "RAM": "some_RAM2",
                "ROM": "some_ROM2",
            },
        },
        {
            "time": datetime.now(),
            "pc_stats": {
                "CPU": "some_CPU3",
                "RAM": "some_RAM3",
                "ROM": "some_ROM3",
            },
        },
    ]

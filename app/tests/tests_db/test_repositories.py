"""The module responsible for testing database queries."""

from datetime import datetime
from typing import Any, Dict, List, Sequence

import pytest
from fastapi.testclient import TestClient

from app.db.models import Stat
from app.db.repositories import HistoryRepository


@pytest.mark.asyncio
async def test_history_repository_save(history_rep: HistoryRepository):
    """Test saving data in db."""
    test_data: Dict[str, Any] = {
        "time": datetime.now(),
        "pc_stats": {"smth_key": "smth_value"},
    }
    try:
        await history_rep.save(test_data)
    except Exception as exc:
        pytest.fail(str(exc))


@pytest.mark.asyncio
async def test_history_rep_save_invalid_data(history_rep: HistoryRepository):
    """Negative test saving invalid data."""
    invalid_data: Dict[str, Any] = {
        "invalid": "data",
    }
    with pytest.raises(TypeError):
        await history_rep.save(invalid_data)


@pytest.mark.asyncio
async def test_history_rep_get_all(
    client: TestClient, history_rep: HistoryRepository, pc_metrics: List[Dict[str, Any]]
):
    """Test getting the history."""
    for data in pc_metrics:
        await history_rep.save(data)

    history: Sequence[Stat] = await history_rep.get_all()

    for record, data in zip(history, sorted(pc_metrics, key=lambda rec: rec["time"])):
        assert record.time == data["time"]
        assert record.pc_stats == data["pc_stats"]

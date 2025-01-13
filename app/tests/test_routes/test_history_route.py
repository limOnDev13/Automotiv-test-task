"""The module responsible for testing the module history_route.py."""

from typing import Any, Dict, List

import bs4 as bs
import pytest
from httpx import ASGITransport, AsyncClient

from app.db.repositories import HistoryRepository
from app.main import create_app


@pytest.mark.asyncio
async def test_get_history(
    history_rep: HistoryRepository, pc_metrics: List[Dict[str, Any]]
):
    """Test the endpoint /history."""
    for data in pc_metrics:
        await history_rep.save(data)

    async with AsyncClient(
        transport=ASGITransport(app=create_app()), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/history")

    assert response.status_code == 200
    soup = bs.BeautifulSoup(response.text, "html.parser")
    find_table = soup.find("table")
    rows = find_table.find_all("tr")

    for row, data in zip(rows[1:], sorted(pc_metrics, key=lambda rec: rec["time"])):
        cells = row.find_all("td")
        assert cells[0].text == str(data["time"])
        assert cells[1].text == data["pc_stats"]["CPU"]
        assert cells[2].text == data["pc_stats"]["RAM"]
        assert cells[3].text == data["pc_stats"]["ROM"]

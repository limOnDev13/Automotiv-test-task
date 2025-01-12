"""The module responsible for the endpoints related to the measurement history."""

from typing import Sequence

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.repositories import HistoryRepository
from app.db.models import Stat

router: APIRouter = APIRouter()


@router.get("/history")
async def get_history():
    """Send PC data via a websocket."""
    history: Sequence[Stat] = await HistoryRepository().get_all()
    pass

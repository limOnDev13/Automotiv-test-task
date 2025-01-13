"""The module responsible for the endpoints related to the measurement history."""

from typing import Any, Dict, List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.repositories import HistoryRepository

router: APIRouter = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/history", response_class=HTMLResponse)
async def get_history(request: Request):
    """Send PC data via a websocket."""
    history_in_template: List[Dict[str, Any]] = [
        record.to_hash() for record in await HistoryRepository().get_all()
    ]

    return templates.TemplateResponse(
        request=request, name="history.html", context={"history": history_in_template}
    )

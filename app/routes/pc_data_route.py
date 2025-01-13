"""The module responsible for transmitting PC data via websockets."""

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config.app_config import Config
from app.services.history import HistoryManager

router: APIRouter = APIRouter()
templates = Jinja2Templates(directory="templates")

DELAY: int = Config().delay


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    """Get the main page."""
    return templates.TemplateResponse(request=request, name="index.html")


@router.websocket("/ws")
async def send_stats(websocket: WebSocket):
    """Send PC data via a websocket."""
    await websocket.accept()

    history: HistoryManager = HistoryManager(
        websocket=websocket,
        interval=DELAY,
    )

    await history.run()

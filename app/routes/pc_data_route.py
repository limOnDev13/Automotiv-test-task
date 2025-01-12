"""The module responsible for transmitting PC data via websockets."""

from fastapi import APIRouter, WebSocket

from app.config.app_config import Config
from app.services.history import HistoryManager

router: APIRouter = APIRouter()

DELAY: int = Config().delay


@router.websocket("/ws")
async def send_stats(websocket: WebSocket):
    """Send PC data via a websocket."""
    await websocket.accept()

    history: HistoryManager = HistoryManager(
        websocket=websocket,
        interval=DELAY,
    )
    await history.run()

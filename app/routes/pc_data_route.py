import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.pc_data import PCData

router: APIRouter = APIRouter()

DELAY: int = 1
pc_stats: PCData = PCData(DELAY)

@router.websocket("/ws")
async def send_stats(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json(pc_stats.data_dict)
            await asyncio.sleep(DELAY)
    except WebSocketDisconnect:
        print("Disconnected...")

"""The module responsible for generating the measurement history."""

import asyncio
import logging
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Set

from fastapi import WebSocket, WebSocketDisconnect

from app.db.repositories import HistoryRepository

from .pc_data import PCData

logger = logging.getLogger("main_logger.history_manager")


class HistoryManager(object):
    """
    The class responsible for generating the measurement history.

    Args:
        websocket (WebSocket) - The websocket object.
        The websocket must first be accepted (await websocket.accept())
        before passing it to the object.

        interval (float) - The delay between measurements.
    """

    __recording: bool = False
    __break: bool = False

    def __init__(self, websocket: WebSocket, interval: float = 1):
        """Initialize class."""
        self.__ws = websocket
        self.__pc_data = PCData()
        self.__interval = interval
        self.__repository = HistoryRepository()
        self.__background_tasks: Set[asyncio.Task] = set()
        self.__queue: asyncio.Queue = asyncio.Queue()

    async def __get_data(self) -> AsyncGenerator[Dict[str, str], None]:
        """Make a measurement and make a delay."""
        while not self.__break:
            data: Dict[str, str] = self.__pc_data.data_dict
            logger.debug("Measured CPU, RAM, and ROM loads: %s", str(data))

            yield data

            logger.debug("Fall asleep for %d seconds", self.__interval)
            await asyncio.sleep(self.__interval)

    async def __send_stat(self) -> None:
        """Send the first measurement data in the queue."""
        try:
            while not self.__break:
                data: Dict[str, str] = await self.__queue.get()
                logger.debug("Sending the data: %s", str(data))
                await self.__ws.send_json(data)
        except WebSocketDisconnect:
            logger.warning("Websocket was disconnected.")
            self.__break = True
        except RuntimeError as exc:
            logger.warning(str(exc))
            self.__break = True

    async def __update_mode(self):
        """Receive a message from the client from change mode."""
        try:
            while not self.__break:
                client_msg: str = await self.__ws.receive_text()
                logger.debug(
                    "The client has updated the recording mode: %s", str(client_msg)
                )
                if client_msg == "start":
                    logger.debug("Starting recording...")
                    self.__recording = True
                elif client_msg == "end":
                    logger.debug("Ending recording...")
                    self.__recording = False
                else:
                    logger.error(
                        "The client should send only the start or end."
                        " Received message: %s",
                        client_msg,
                    )
        except WebSocketDisconnect:
            logger.warning("Websocket was disconnected.")
            self.__break = True

    async def __save_stat(self, data: Dict[str, str]):
        """Save the measurement to the database."""
        logger.debug("Saving the data in the database...")
        stat_dict: Dict[str, Any] = {
            "time": datetime.now(),
            "pc_stats": data,
        }
        await self.__repository.save(stat_dict)

    async def __main_loop(self):
        """In an infinite generator, make measurements, save and send them."""
        try:
            async for data in self.__get_data():
                if self.__recording:
                    task_save_stat = asyncio.create_task(self.__save_stat(data))
                    self.__background_tasks.add(task_save_stat)
                    task_save_stat.add_done_callback(self.__background_tasks.discard)

                logger.debug("Adding the data to the queue...")
                await self.__queue.put(data)

        except WebSocketDisconnect:
            logger.warning("Websocket was disconnected.")
            return

    async def run(self):
        """
        Run all necessary tasks.

        The function starts tasks such as measuring CPU, RAM, and ROM data,
        sending this data to the client and, if necessary, saving it to the database,
        as well as listening to messages from the client
        to start and finish writing to the database.
        """
        await asyncio.gather(
            self.__main_loop(), self.__update_mode(), self.__send_stat()
        )

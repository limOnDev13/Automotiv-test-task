"""A module for building and launching an application."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes.pc_data_route import router as websocket_router

app = FastAPI()

app.include_router(websocket_router)

app.mount("/", StaticFiles(directory="app/static", html=True))

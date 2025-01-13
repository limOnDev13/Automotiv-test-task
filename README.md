# Automotiv-test-task

## Description
An application for viewing information about CPU, RAM,
and ROM usage in real time with the ability to save measurement history in a database.

## Demo

![alt text](demo.gif)

---
## Setup and launch
To run the application, you need to download the repository to the machine
(you don't need to download the setup.cfg files and the app/tests folder).
In the virtual environment, install dependencies with the ```poerty install``` command.
After that, add the environment variables (you can add them to the file .env)
based on the example from the .env.example file. You also need to raise the database
(to raise postgres in docker, run the ```docker compose up --build``` command).
To run it, run the command ```uvicorn app.main:app``` in the terminal.
Next, go to http://{host}:{port}/ (If the application is running on a local machine on desk 8000,
then you can go to http://localhost:8000/)
___

## Endpoints

- **GET "/"** - The main page, which shows the load on the CPU, RAM and ROM in real time
- **"/ws"** - The WebSocket endpoint
- **GET "/history"** - A page with the measurement history

___

## Stack
- FastAPI
- websockets
- Postgres
- SQLAlchemy
- Jinja2
- Docker
- Pytest

## Ways to improve

- Add more tests
- Add static output via Nginx
- Add the ability to interactively change the delay between measurements

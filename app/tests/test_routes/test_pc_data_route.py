"""The module responsible for testing the router from the module pc_data_route.py."""

from fastapi.testclient import TestClient


def test_sending_data_via_websocket(client: TestClient):
    """Test sending pc data via websockets."""
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert "CPU" in data
        assert "RAM" in data
        assert "ROM" in data

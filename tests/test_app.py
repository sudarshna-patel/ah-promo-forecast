import pytest
from unittest.mock import patch


@patch("app.main.configure_logs")
def test_home(mock_logs):
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

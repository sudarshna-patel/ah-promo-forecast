def test_home():
    from unittest.mock import patch

    with patch("app.main.configure_logs"):
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

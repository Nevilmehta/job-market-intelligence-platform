from tests.conftest import get_test_client

def test_health_check_returns_ok():
    client = get_test_client()

    response = client.get("/v1/health")
    
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data
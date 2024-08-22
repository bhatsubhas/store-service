def test_health_status_endpoint(client):
    response = client.get("/healthz/status")
    assert response.status_code == 200
    json_body = response.get_json()
    assert "service status is healthy" in json_body["message"]


def test_index_endpoint(client):
    response = client.get("/")
    assert response.status_code == 404

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert "environment" in json_data


def test_get_all_clips(client: TestClient, seed_test_clip):
    response = client.get("/play")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) >= 1
    assert json_data[0]["title"] == "Test Audio Clip"


def test_get_clip_stats_success_and_not_found(client: TestClient, seed_test_clip):
    # Test valid clip ID
    response = client.get(f"/play/{seed_test_clip.id}/stats")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == seed_test_clip.id
    assert json_data["title"] == "Test Audio Clip"
    assert json_data["play_count"] == 0

    # Test non-existent clip ID
    invalid_response = client.get("/play/99999/stats")
    assert invalid_response.status_code == 404
    error_data = invalid_response.json()
    assert error_data["error"] == "Clip not found"
    assert error_data["code"] == 404


def test_stream_clip_not_found(client: TestClient):
    response = client.get("/play/99999/stream")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "Clip not found"
    assert error_data["code"] == 404
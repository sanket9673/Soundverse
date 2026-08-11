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


def test_create_clip_success(client: TestClient):
    payload = {
        "title": "Lo-Fi Chill",
        "description": "Relaxing lo-fi track",
        "genre": "Lo-Fi",
        "duration": 120.5,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    }
    response = client.post("/play", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["genre"] == payload["genre"]
    assert data["duration"] == payload["duration"]
    assert data["audio_url"] == payload["audio_url"]
    assert data["play_count"] == 0
    assert "id" in data


def test_create_clip_validation_error(client: TestClient):
    payload = {
        "title": "Invalid Clip",
        "genre": "Ambient",
        "duration": -5.0,  # invalid duration <= 0
        "audio_url": "https://example.com/audio.mp3",
    }
    response = client.post("/play", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == 422
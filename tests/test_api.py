from fastapi.testclient import TestClient

from app.core.exception import ErrorCodes
from app.main import app

client = TestClient(app)

fallback_phrases = [
    "clarify",
    "don't have enough context",
    "do not have enough context"
]

def test_chat_returns_fallback_for_vague_question_in_new_session():
    session_id = "test-session-fallback"

    payload = {
        "session_id": session_id,
        "message": "Can you explain the second point in simple words?"
    }

    response = client.post("/chat/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session_id
    assert isinstance(data["answer"], str)
    assert data["sources"] == []

    assert any(phrase in data["answer"].lower() for phrase in fallback_phrases)

def test_chat_returns_grounded_answer_for_known_question():
    session_id = "test-session-grounded"
    payload = {
        "session_id": session_id,
        "message": "What are the key benefits and challenges of microservices?"
    }

    response = client.post("/chat/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session_id
    assert isinstance(data["answer"], str)
    assert data["answer"].strip() != ""
    
    assert not any(phrase in data["answer"].lower() for phrase in fallback_phrases)
    
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

    first_source = data["sources"][0]
    assert "faq_id" in first_source
    assert "category" in first_source

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_ready_endpoint():
    response = client.get("/ready")
    assert response.status_code in (200, 503)

# def test_not_found_error():
#     payload = {
#         "session_id": "test",
#         "message": "test"
#     }
#     response = client.post("/chat/", json=payload)

#     assert response.status_code == 404

#     data = response.json()

#     assert data["error"]["code"] == "resource_not_found"
#     assert "message" in data["error"]
#     assert "request_id" in data

def test_validation_error():
    response = client.post(
        "/chat/",
        json={
            "session_id": "test"
            # missing "message"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == ErrorCodes.INVALID_REQUEST
    assert "request_id" in data

def test_request_id_header():
    response = client.post(
        "/chat/",
        json={
            "session_id": "test",
            "message": "hello"
        }
    )

    assert "X-Request-ID" in response.headers
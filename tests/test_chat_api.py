from fastapi.testclient import TestClient

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

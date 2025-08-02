from fastapi.testclient import TestClient
from unittest.mock import patch
from app.infrastructure.entry_points.api import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

def test_ask_question_success():
    request_payload = {
        "question": "What is a movie about AI and humans?",
        "top_k": 2
    }

    expected_response = {
        "answer": "The movie you're thinking of is 'The Matrix'.",
        "documents": [
            {
                "title": "The Matrix",
                "image": "https://example.com/matrix.jpg",
                "similarity": 0.9876,
                "content": "A computer hacker learns about the true nature of his reality..."
            }
        ]
    }

    with patch("app.infrastructure.entry_points.api.run_rag", return_value=expected_response):
        client = TestClient(app)
        response = client.post("/ask", json=request_payload)

        assert response.status_code == 200
        assert response.json() == expected_response

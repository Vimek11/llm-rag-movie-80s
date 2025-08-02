import requests
from behave import given, when, then

BASE_URL = "http://localhost:8000"

@given("the movie question-and-answer system is available")
def step_system_is_available(context):
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200

@when('the user asks "{question}"')
def step_user_asks_question(context, question):
    payload = {
        "question": question,
        "top_k": 2
    }
    context.response = requests.post(f"{BASE_URL}/ask", json=payload)

@then("the system should return a relevant answer")
def step_should_return_answer(context):
    data = context.response.json()
    assert "answer" in data
    assert data["answer"].strip() != ""

@then("the system should include at least one matching movie")
def step_should_include_matching_movie(context):
    data = context.response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1

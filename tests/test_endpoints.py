from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommend_by_embedding():
    """
    Test the /recommend_by_embedding endpoint.
    """
    response = client.post(
        "/recommend_by_embedding",
        json={
            "ingredients": "tomato",
            "preferences": ["cheese", "basil"],
            "top_n": 2
        }
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert len(data) == 2, f"Expected 2 results, got {len(data)}"
    assert "title" in data[0] and "ingredients" in data[0], "Expected recipe structure is missing"

def test_query_recipe():
    """
    Test the /query_recipe endpoint.
    """
    response = client.post(
        "/query_recipe",
        json={
            "ingredients": "tofu",
            "preferences": ["spicy", "garlic"],
            "top_n": 1
        }
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert len(data) > 0, "Expected at least one result, but got none"
    assert "title" in data[0] and "ingredients" in data[0], "Expected recipe structure is missing"

def test_generate_ai_recipe():
    """
    Test the /generate_ai_recipe endpoint.
    """
    response = client.post(
        "/generate_ai_recipe",
        json={
            "ingredients": "tomato, garlic",
            "preferences": ["vegan"]
        }
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "ai_recipe" in data, "AI-generated recipe not found in the response"
    assert isinstance(data["ai_recipe"], str), "AI-generated recipe should be a string"

    # Validate the presence of key ingredients
    ai_recipe = data["ai_recipe"].lower()
    assert "tomato" in ai_recipe, "Generated recipe does not include the requested ingredient: tomato"
    assert "garlic" in ai_recipe, "Generated recipe does not include the requested ingredient: garlic"

    # Optionally, validate structure
    assert "step" in ai_recipe, "Generated recipe does not include clear steps."

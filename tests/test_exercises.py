import pytest
from fastapi.testclient import TestClient

def register_and_login(client, username="user1", password="pass"):
    # Helper function to register and then login a user.
    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post("/auth/login", json={"username": username, "password": password})
    tokens = response.json()
    # Return headers including the bearer token for authenticated requests.
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    return headers

def test_exercise_crud(client):
    headers = register_and_login(client, "user1", "pass")

    # Create an exercise via the POST endpoint.
    create_data = {"name": "Push Ups", "description": "Do push ups", "difficulty": 3, "is_public": True}
    response = client.post("/exercises/", json=create_data, headers=headers)
    assert response.status_code == 200
    exercise = response.json()
    exercise_id = exercise["id"]

    # Retrieve the created exercise using its ID.
    response = client.get(f"/exercises/{exercise_id}", headers=headers)
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["name"] == "Push Ups"

    # Update the exercise details using PUT.
    update_data = {"name": "Modified Push Ups", "description": "Do modified push ups", "difficulty": 4, "is_public": True}
    response = client.put(f"/exercises/{exercise_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Modified Push Ups"

    # Delete the exercise using DELETE.
    response = client.delete(f"/exercises/{exercise_id}", headers=headers)
    assert response.status_code == 204

def test_favorites_saves_ratings(client):
    headers = register_and_login(client, "user1", "pass")

    # Create a new exercise.
    create_data = {"name": "Squats", "description": "Do squats", "difficulty": 3, "is_public": True}
    response = client.post("/exercises/", json=create_data, headers=headers)
    exercise = response.json()
    exercise_id = exercise["id"]

    # Favorite the exercise.
    response = client.post(f"/favorites/{exercise_id}", headers=headers)
    assert response.status_code == 204

    # Save the exercise.
    response = client.post(f"/saves/{exercise_id}", headers=headers)
    assert response.status_code == 204

    # Rate the exercise (e.g., rating of 5).
    response = client.post(f"/ratings/{exercise_id}", json={"rating": 5}, headers=headers)
    assert response.status_code == 204

    # Retrieve the exercise to verify favorite/save counts and average rating.
    response = client.get(f"/exercises/{exercise_id}", headers=headers)
    fetched = response.json()
    assert fetched["favorite_count"] == 1
    assert fetched["save_count"] == 1
    # Confirm the average rating is calculated correctly.
    assert fetched["average_rating"] == 5.0

def test_search_and_sort(client):
    headers = register_and_login(client, "user2", "pass")

    # Create several exercises for testing search and sorting features.
    exercises_data = [
        {"name": "Exercise A", "description": "Desc A", "difficulty": 1, "is_public": True},
        {"name": "Exercise B", "description": "Desc B", "difficulty": 2, "is_public": True},
        {"name": "Exercise C", "description": "Desc C", "difficulty": 3, "is_public": True},
    ]
    exercise_ids = []
    for data in exercises_data:
        resp = client.post("/exercises/", json=data, headers=headers)
        exercise_ids.append(resp.json()["id"])

    # Simulate favorites and saves.
    client.post(f"/favorites/{exercise_ids[0]}", headers=headers)
    client.post(f"/favorites/{exercise_ids[1]}", headers=headers)
    client.post(f"/saves/{exercise_ids[0]}", headers=headers)

    # Rate the exercises with varying ratings.
    client.post(f"/ratings/{exercise_ids[0]}", json={"rating": 5}, headers=headers)
    client.post(f"/ratings/{exercise_ids[1]}", json={"rating": 3}, headers=headers)
    client.post(f"/ratings/{exercise_ids[2]}", json={"rating": 4}, headers=headers)

    # Test sorting by favorite_count.
    response = client.get("/exercises/?sortBy=favorite_count", headers=headers)
    exercises_sorted = response.json()
    # Check that the first exercise has at least as many favorites as the second.
    assert exercises_sorted[0]["favorite_count"] >= exercises_sorted[1]["favorite_count"]

    # Test sorting by save_count.
    response = client.get("/exercises/?sortBy=save_count", headers=headers)
    exercises_sorted = response.json()
    # Confirm that the save_count is sorted in descending order.
    assert exercises_sorted[0]["save_count"] >= exercises_sorted[1]["save_count"]

def test_view_users_endpoint(client):
    headers = register_and_login(client, "user3", "pass")

    # Create an exercise.
    create_data = {"name": "Planks", "description": "Do planks", "difficulty": 2, "is_public": True}
    response = client.post("/exercises/", json=create_data, headers=headers)
    exercise = response.json()
    exercise_id = exercise["id"]

    # Favorite and save the exercise.
    client.post(f"/favorites/{exercise_id}", headers=headers)
    client.post(f"/saves/{exercise_id}", headers=headers)

    # Retrieve the list of users who favorited or saved the exercise.
    response = client.get(f"/exercises/{exercise_id}/users", headers=headers)
    data = response.json()
    # Assert that the response contains lists for both favorited_by and saved_by.
    assert "favorited_by" in data and isinstance(data["favorited_by"], list)
    assert "saved_by" in data and isinstance(data["saved_by"], list)
def test_register_and_login(client):
    # Test user registration: send POST request to register endpoint.
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    # Assert that the registration was successful (HTTP 200 OK).
    assert response.status_code == 200
    data = response.json()
    # Check that an 'id' field is returned indicating a new user record.
    assert "id" in data

    # Test login: send POST request with credentials.
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    # Assert login is successful.
    assert response.status_code == 200
    data = response.json()
    # Check that the response contains both access and refresh tokens.
    assert "access_token" in data
    assert "refresh_token" in data

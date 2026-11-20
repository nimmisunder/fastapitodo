
import pytest
from fastapi.testclient import TestClient
from main import app, tasklist

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    tasklist.clear()
    yield
    tasklist.clear()


# Test 1: Create a task
def test_create_task():
    response = client.post("/add_item", json={
        "id": 1,
        "name": "Learn Python",
        "desc": "Practice FastAPI",
        "is_completed": False
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Learn Python"


# Test 2: Get all tasks
def test_get_all_tasks():
    client.post("/add_item", json={
        "id": 1,
        "name": "Learn Python",
        "desc": "Practice FastAPI",
        "is_completed": False
    })

    response = client.get("/alltask")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Test 3: Update a task
def test_update_task():
    client.post("/add_item", json={
        "id": 1,
        "name": "Learn Python",
        "desc": "Basics",
        "is_completed": False
    })

    response = client.put("/updatetask/1", json={
        "id": 1,
        "name": "Learn FastAPI",
        "desc": "CRUD operations",
        "is_completed": True
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Learn FastAPI"
    assert response.json()["is_completed"] is True


# Test 4: Delete a task
def test_delete_task():
    client.post("/add_item", json={
        "id": 1,
        "name": "Learn Python",
        "desc": "Basics",
        "is_completed": False
    })

    response = client.delete("/delete_task/1")

    assert response.status_code == 200
    assert len(tasklist) == 0


# Test 5: Get a non-existing task for update
def test_update_invalid_task():
    response = client.put("/updatetask/99", json={
        "id": 99,
        "name": "Test",
        "desc": "Test",
        "is_completed": False
    })

    assert response.status_code == 404


# Test 6: Delete a non-existing task
def test_delete_invalid_task():
    response = client.delete("/delete_task/99")

    assert response.status_code == 404


# Test 7: Invalid request data
def test_invalid_task():
    response = client.post("/add_item", json={
        "name": "Learn Python"
    })

    assert response.status_code == 422

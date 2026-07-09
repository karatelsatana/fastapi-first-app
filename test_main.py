from fastapi.testclient import TestClient
from main import app
import random

client = TestClient(app)

def test_read_root():
    response =client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "работает"}

def test_register_and_login():
    username = f"testuser{random.randint(1000, 999999)}"
    response = client.post("/register", json={
        "name": username,
        "age": 25,
        "password": "testpass123"
    })
    assert response.status_code == 200

    response = client.post("/login", json={
        "name": username,
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_notes_requires_auth():
    response = client.get("/notes")
    assert response.status_code == 401

def test_create_and_list_notes():
    login_response = client.post("/login", json={
        "name": "testuser123",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/notes", json={"text": "тестовая заметка"}, headers=headers)
    assert create_response.status_code == 200

    list_response = client.get("/notes", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0
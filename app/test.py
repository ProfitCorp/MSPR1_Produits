import pytest
from fastapi.testclient import TestClient
from main import app  # ton fichier FastAPI principal
from database import Base, engine, SessionLocal
from models import ProductDB
from schemas import Products, Details
from auth.auth import create_access_token

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {
    "get_db": override_get_db
}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def get_auth_headers():
    token = create_access_token({"user": "admin", "role": "admin", "id": 1})
    return {"Authorization": f"Bearer {token}"}

def test_get_empty_items():
    headers = get_auth_headers()
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_add_item():
    headers = get_auth_headers()
    item_data = {
        "name": "Ordinateur",
        "details": {
            "price": 999.99,
            "description": "Portable gamer",
            "color": "noir"
        },
        "stock": 5
    }
    response = client.post("/items/", json=item_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ordinateur"
    assert data["details"]["price"] == 999.99
    assert data["stock"] == 5
    assert "id" in data

def test_get_items_after_insert():
    headers = get_auth_headers()
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Ordinateur"

def test_update_item():
    headers = get_auth_headers()
    update_data = {
        "name": "Ordinateur modifié",
        "details": {
            "price": 899.99,
            "description": "MAJ description",
            "color": "gris"
        },
        "stock": 10
    }
    response = client.put("/items/1", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ordinateur modifié"
    assert data["details"]["price"] == 899.99

def test_delete_item():
    headers = get_auth_headers()
    response = client.delete("/items/1", headers=headers)
    assert response.status_code == 200

def test_get_items_after_delete():
    headers = get_auth_headers()
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_update_nonexistent_item():
    headers = get_auth_headers()
    update_data = {
        "name": "Ghost",
        "details": {
            "price": 1.0,
            "description": "N'existe pas",
            "color": "transparent"
        },
        "stock": 0
    }
    response = client.put("/items/999", json=update_data, headers=headers)
    assert response.status_code == 404

def test_delete_nonexistent_item():
    headers = get_auth_headers()
    response = client.delete("/items/999", headers=headers)
    assert response.status_code == 404

def test_coffee_route():
    response = client.get("/coffee/")
    assert response.status_code == 418
    assert response.json()["detail"] == "I'm a teapot"

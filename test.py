from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
import pytest
from main import app
import os

# === Crée une DB temporaire en mémoire ===
TEST_DB_FILE = "./test_items.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists(TEST_DB_FILE):
        engine.dispose()
        os.remove(TEST_DB_FILE)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_get_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_item():
    payload = {
        "name": "Test produit",
        "details": {
            "price": 19.99,
            "description": "Un produit de test",
            "color": "Rouge"
        },
        "stock": 10
    }

    response = client.post("/items/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test produit"
    assert data["details"]["price"] == 19.99
    assert data["stock"] == 10
    assert "id" in data  # L'ID doit être généré automatiquement

def test_get_items_after_post():
    response = client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Test produit"

def test_update_item():
    update_payload = {
        "name": "Produit modifié",
        "details": {
            "price": 29.99,
            "description": "Description mise à jour",
            "color": "Bleu"
        },
        "stock": 5
    }

    response = client.put("/items/1", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Produit modifié"
    assert data["details"]["price"] == 29.99
    assert data["stock"] == 5

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200

    # Confirme que le produit a été supprimé
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_coffee():
    response = client.get("/coffee/")
    assert response.status_code == 418

def test_type_validation():
    response = client.post("/items/", json={"name": 123})
    assert response.status_code == 422

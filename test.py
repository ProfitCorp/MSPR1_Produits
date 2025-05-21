from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import models

# === Crée une DB temporaire en mémoire ===
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === Setup la DB ===
Base.metadata.create_all(bind=engine)

# === Dépendance override ===
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

# def test_create_item():
#     payload = {
#         "name": "Test produit",
#         "details": {
#             "price": 19.99,
#             "description": "Un produit de test",
#             "color": "Rouge"
#         },
#         "stock": 10
#     }

#     response = client.post("/items/", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Test produit"
#     assert data["details"]["price"] == 19.99
#     assert data["stock"] == 10
#     assert "id" in data  # L'ID doit être généré automatiquement

# def test_get_items_after_post():
#     response = client.get("/items/")
#     assert response.status_code == 200
#     items = response.json()
#     assert len(items) == 1
#     assert items[0]["name"] == "Test produit"

# def test_update_item():
#     update_payload = {
#         "name": "Produit modifié",
#         "details": {
#             "price": 29.99,
#             "description": "Description mise à jour",
#             "color": "Bleu"
#         },
#         "stock": 5
#     }

#     response = client.put("/items/1", json=update_payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Produit modifié"
#     assert data["details"]["price"] == 29.99
#     assert data["stock"] == 5

# def test_delete_item():
#     response = client.delete("/items/1")
#     assert response.status_code == 200
#     assert "supprimé" in response.json()["message"]

#     # Confirme que le produit a été supprimé
#     response = client.get("/items/")
#     assert response.status_code == 200
#     assert response.json() == []
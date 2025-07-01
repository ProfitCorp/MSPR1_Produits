"""
API route definitions for item management.

This module defines the FastAPI router responsible for handling HTTP requests
related to item CRUD operations and a fun endpoint for testing HTTP status codes.

Endpoints include:
- Retrieving all items
- Adding a new item
- Updating an existing item
- Deleting an item
- Returning an HTTP 418 teapot status for fun

Dependencies:
- SQLAlchemy session dependency injected via FastAPI's Depends
- Controller functions to handle database logic
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers import get_all_items, create_item, update_item, delete_item
from database import get_db
from schemas import Products, ProductsGet, LoginInput
from auth.auth import create_access_token, authenticate_user
from auth.security import JWTBearer

router = APIRouter()

@router.get("/items/", response_model=list[ProductsGet])
def get_items(db: Session = Depends(get_db)):
    """
    Retrieve all items from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[ProductsGet]: List of product objects with details and IDs.
    """
    return get_all_items(db)

@router.post("/items/", dependencies=[Depends(JWTBearer())], response_model=ProductsGet)
def add_item(item: Products, db: Session = Depends(get_db)):
    """
    Create a new item in the database.

    Args:
        item (Products): Product data to insert.
        db (Session): SQLAlchemy session object.

    Returns:
        ProductsGet: The created product with its assigned ID.
    """
    return create_item(db, item)

@router.put("/items/{item_id}", dependencies=[Depends(JWTBearer())], response_model=ProductsGet)
def modify_item(item_id: int, item: Products, db: Session = Depends(get_db)):
    """
    Update an existing item in the database by its ID.

    Args:
        item_id (int): ID of the item to update.
        item (Products): Updated product data.
        db (Session): SQLAlchemy session object.

    Raises:
        HTTPException: If the item with the specified ID is not found.

    Returns:
        ProductsGet: The updated product with its details.
    """
    updated_item = update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", dependencies=[Depends(JWTBearer())])
def remove_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item from the database by its ID.

    Args:
        item_id (int): ID of the item to delete.
        db (Session): SQLAlchemy session object.

    Raises:
        HTTPException: If the item with the specified ID is not found.

    Returns:
        int: HTTP status 200 if deletion was successful.
    """
    deleted_item = delete_item(db, item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return 200

@router.get("/coffee/")
def get_coffee():
    """
    Just an EasterEgg :)
    """
    raise HTTPException(status_code = 418, detail = "I'm a teapot")


@router.post("/token")
def login_user(user: LoginInput):
    user = authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=401)

    token = create_access_token({
        "user": user.username,
        "role": user.role
        })
    return {"access_token": token, "token_type": "bearer"}
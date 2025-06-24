"""
Controllers module for managing Item entities.

This module provides CRUD (Create, Read, Update, Delete) operations
to interact with the database items through SQLAlchemy ORM sessions.
It converts database ORM objects into Pydantic schemas for API response consistency.

Functions:
- get_all_items: Retrieve all items from the database.
- create_item: Add a new item to the database.
- update_item: Modify an existing item identified by its ID.
- delete_item: Remove an item from the database by ID.
- itemdb_to_products: Helper function to convert ORM item objects to Pydantic models.
"""
from sqlalchemy.orm import Session
from models import ProductDB
from schemas import Details, Products, ProductsGet
from mq.publish import publish_product_delete, publish_product_update, publish_product_create

def get_all_items(db: Session):
    """
    Retrieve all items from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[ProductsGet]: List of all items converted to ProductsGet schema.
    """
    test = db.query(ProductDB).all()
    return [itemdb_to_products(test) for test in test]

def create_item(db: Session, item_data: Products):
    """
    Create a new item in the database.

    Args:
        db (Session): SQLAlchemy database session.
        item_data (Products): Data of the item to create.

    Returns:
        ProductsGet: The created item converted to ProductsGet schema.
    """
    db_item = ProductDB(
        name=item_data.name,
        price=item_data.details.price,
        description=item_data.details.description,
        color=item_data.details.color,
        stock=item_data.stock
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    publish_product_create(item_data.dict())
    return itemdb_to_products(db_item)

def update_item(db: Session, item_id: int, item_data: Products):
    """
    Update an existing item in the database.

    Args:
        db (Session): SQLAlchemy database session.
        item_id (int): ID of the item to update.
        item_data (Products): New data for the item.

    Returns:
        ProductsGet | None: Updated item converted to ProductsGet schema, or None if not found.
    """
    db_item = db.query(ProductDB).filter(ProductDB.id == item_id).first()
    if not db_item:
        return None
    db_item.name = item_data.name
    db_item.price = item_data.details.price
    db_item.description = item_data.details.description
    db_item.color = item_data.details.color
    db_item.stock = item_data.stock
    db.commit()
    db.refresh(db_item)
    publish_product_update(item_id, item_data.dict())
    return itemdb_to_products(db_item)

def delete_item(db: Session, item_id: int):
    """
    Delete an item from the database.

    Args:
        db (Session): SQLAlchemy database session.
        item_id (int): ID of the item to delete.

    Returns:
        ItemDB | None: Deleted item instance or None if not found.
    """
    db_item = db.query(ProductDB).filter(ProductDB.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    publish_product_delete(item_id)
    return db_item

def itemdb_to_products(item: ProductDB) -> ProductsGet:
    """
    Convert an ItemDB ORM object to a ProductsGet Pydantic model.

    Args:
        item (ItemDB): ORM item instance.

    Returns:
        ProductsGet: Pydantic model with item data.
    """
    return ProductsGet(
        name=item.name,
        details=Details(
            price=item.price,
            description=item.description,
            color=item.color
        ),
        stock=item.stock,
        id=item.id
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers import get_all_items, create_item, update_item, delete_item, itemdb_to_products
from database import get_db
from models import ItemDB
from schemas import *

router = APIRouter()

@router.get("/items/", response_model=list[ProductsGet])
def get_items(db: Session = Depends(get_db)):
    return get_all_items(db)

@router.post("/items/", response_model=ProductsGet)
def add_item(item: Products, db: Session = Depends(get_db)):
    # new_item = create_item(db, item)
    return create_item(db, item)

@router.put("/items/{item_id}", response_model=ProductsGet)
def modify_item(item_id: int, item: Products, db: Session = Depends(get_db)):
    updated_item = update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = delete_item(db, item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return 200

@router.get("/coffee/")
def get_coffee():
    raise HTTPException(status_code = 418, detail = "I'm a teapot")
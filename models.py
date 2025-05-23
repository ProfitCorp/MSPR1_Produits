"""
Database model definition for products.

This module defines the `ItemDB` class, which represents the structure of the `Products` table
in the database using SQLAlchemy's ORM.

Fields:
- `name`: The name of the product.
- `price`: The price of the product.
- `description`: A short description of the product.
- `color`: The color of the product.
- `stock`: Quantity in stock.
- `id`: Primary key, auto-incremented, uniquely identifies each product.
"""
from sqlalchemy import Column, Integer, String, Float
from database import Base

class ItemDB(Base): # pylint: disable=too-few-public-methods
    """
    SQLAlchemy ORM model for the 'Products' table.

    This class defines the schema for a product stored in the database.
    It includes details such as name, price, description, color, stock, and a unique identifier.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        description (str): A brief description of the product.
        color (str): The color of the product.
        stock (int): The available stock quantity.
        id (int): The primary key, uniquely identifying each product entry.
    """
    __tablename__ = "Products"
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    color = Column(String)
    stock = Column(Integer)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

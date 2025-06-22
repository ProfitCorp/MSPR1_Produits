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
from app.database import Base

class ProductDB(Base): # pylint: disable=too-few-public-methods
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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    price = Column(Float)
    description = Column(String(255))
    color = Column(String(255))
    stock = Column(Integer)
    

class CustomerDB(Base): # pylint: disable=too-few-public-methods
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
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    firstname = Column(String(255), nullable=False, default="John")
    lastname = Column(String(255), nullable=False, default="Doe")
    street_number = Column(String(5), nullable=False, default="123")
    street = Column(String(255), nullable=False, default="SomeStreet")
    postalcode = Column(String(5), nullable=False, default="12345")
    city = Column(String(255), nullable=False, default="SomeCity")
    company_name = Column(String(255), nullable=False, default="SomeCompany")


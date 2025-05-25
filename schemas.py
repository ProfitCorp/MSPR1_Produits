"""
Pydantic schema definitions for product data validation and serialization.

This module defines the data models used for input validation (e.g., creating or updating products)
and output serialization (e.g., returning product data with an ID). 
These schemas are used throughout
the application to ensure consistent data structures between the API and the database.
"""
from pydantic import BaseModel

class Details(BaseModel):
    """
    Schema representing the detailed attributes of a product.

    Attributes:
        price (float): The price of the product.
        description (str): A textual description of the product.
        color (str): The color of the product.
    """
    price: float
    description: str
    color: str

class Products(BaseModel):
    """
    Schema representing the attributes of a product.

    Attributes:
        name (str): The name of the product.
        detail (Details): An object which contains all details for Product.
        stock (int): Integer which indiquates how many pieces of this project in database.
    """
    name: str
    details: Details
    stock: int

class ProductsGet(BaseModel):
    """
    Schema representing the attributes of a product with Id.

    Attributes:
        name (str): The name of the product.
        detail (Details): An object which contains all details for Product.
        stock (int): Integer which indiquates how many pieces of this project in database.
        id (int): Id in database
    """
    name: str
    details: Details
    stock: int
    id: int

class LoginInput(BaseModel):
    username: str
    password: str
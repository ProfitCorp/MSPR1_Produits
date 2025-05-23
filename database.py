"""
Database configuration module.

This module initializes the connection to the SQLite database using SQLAlchemy,
sets up the engine with the appropriate parameters,
and creates a local session factory (SessionLocal) for managing transactions.

It also defines the declarative base class (Base) for ORM model creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./items.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Provide a database session generator.
    
    This function yields a new SQLAlchemy session for database operations
    and ensures that the session is properly closed after use,
    even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

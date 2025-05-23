"""
Database configuration module.

This module initializes the connection to the SQLite database using SQLAlchemy,
sets up the engine with the appropriate parameters,
and creates a local session factory (SessionLocal) for managing transactions.

It also defines the declarative base class (Base) for ORM model creation.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV == "prod":
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    connect_args = {}
else:
    DATABASE_URL = "sqlite:///./items.db"
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

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

"""
Main application entry point.

This module initializes the FastAPI application, sets up the database tables
by creating all defined models, and includes the API routes from the `routes` module.

- `Base.metadata.create_all(bind=engine)` ensures all tables defined in the ORM models are created.
- `FastAPI()` creates the app instance.
- `app.include_router(routes.router)` includes all route definitions from the routes module.
"""
from fastapi import FastAPI
from database import Base, engine
import routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)

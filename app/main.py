"""
Main application entry point.

This module initializes the FastAPI application, sets up the database tables
by creating all defined models, and includes the API routes from the `routes` module.

- `Base.metadata.create_all(bind=engine)` ensures all tables defined in the ORM models are created.
- `FastAPI()` creates the app instance.
- `app.include_router(routes.router)` includes all route definitions from the routes module.
- `init_admin_user` initialize admin user if doesn't exist
"""
from fastapi import FastAPI
from app.database import Base, engine
from app.init import init_admin_user
import app.routes as routes
import os

Base.metadata.create_all(bind=engine)

init_admin_user()

app = FastAPI(
    docs_url=None
)

app.include_router(routes.router)

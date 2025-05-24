"""
Main application entry point.

This module initializes the FastAPI application, sets up the database tables
by creating all defined models, and includes the API routes from the `routes` module.

- `Base.metadata.create_all(bind=engine)` ensures all tables defined in the ORM models are created.
- `FastAPI()` creates the app instance.
- `app.include_router(routes.router)` includes all route definitions from the routes module.
- `APP_ENV` define which environnement is used to run application.
"""
from fastapi import FastAPI
from database import Base, engine
import routes
import os

Base.metadata.create_all(bind=engine)

APP_ENV = os.getenv("APP_ENV", "dev")

app = FastAPI()

app.include_router(routes.router)

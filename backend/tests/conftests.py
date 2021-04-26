import warnings
import os

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config

#Applying migration before and after testing sessions
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
    
#Create new app for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    
    return get_application()

#Grab reference to db when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db

#Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
        app = app,
        base_url = "http://testserver",
        headers={"Content-Type": "applications/json"}
        ) as client:
            yield client
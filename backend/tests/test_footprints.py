import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from tests.conftests import client, app, db, apply_migrations

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED

from app.models.footprints import FootprintCreate

#decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_footprint():
    return FootprintCreate(
        category = "test category",
        subcategory = "test subcategory",
        item = "test item",
        footprint = 0
    )

class TestFootprintsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("footprints:create-footprints"), json = {})
        assert res.status_code != HTTP_404_NOT_FOUND
        
    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self,app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("footprints:create-footprints"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        
        
class TestCreateFootprint:
    async def test_valid_input_creates_footprint(
        self, app: FastAPI, client: AsyncClient, new_footprint: FootprintCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("footprints:create-footprints"), json={"new_footprint": new_footprint.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        
        created_footprint = FootprintCreate(**res.json())
        assert created_footprint == new_footprint
        
    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"category":"test category", "subcategory": "test subcategory", "item": "test item", "footprint": "test footprint"},422)
        )
    )
    
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("footprints:create-footprints"), json={"new_footprint": invalid_payload}
        )
        assert res.status_code == status_code
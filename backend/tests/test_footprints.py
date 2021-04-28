import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from tests.conftests import client, app, db, apply_migrations, test_footprint

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED, HTTP_200_OK

from app.models.footprints import FootprintCreate, FootprintInDB   
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
        
    
    class TestGetFootprint:
        async def test_get_footprint_by_id(self, app: FastAPI, client: AsyncClient, test_footprint: FootprintInDB) -> None:
            res = await client.get(app.url_path_for("footprints:get-footprint-by-id", id = test_footprint.id))
            assert res.status_code == HTTP_200_OK
            footprint = FootprintInDB(**res.json())
            assert footprint.id == test_footprint 
            
        @pytest.mark.parametrize(
            "id, status_code",
            (
                (500,404),
                (-1, 404),
                (None, 422)
            )
        )
        
        async def test_wrong_id_returns_error(
            self, app:FastAPI, client: AsyncClient, id: int, status_code: int    
        ) -> None:
            res = await client.get(app.url_path_for("footprints:get-footprint-by-id", id=id))
            assert res.status_code == status_code
            
        async def test_get_all_footprints_returns_valid_response(
            self, app: FastAPI, client: AsyncClient, test_footprint: FootprintInDB
        ) -> None:
            res = await client.get(app.url_path_for("footprints:get-all-footprints"))
            assert res.status_code == HTTP_200_OK
            assert isinstance(res.json(), list)
            assert len(res.json()) > 0
            footprints = [FootprintInDB(**l) for l in res.json()]
            assert test_footprint in footprints
            
            
    class TestDeleteFootprint:
        async def test_can_delete_footprint_successfully(
            self, app: FastAPI, client:AsyncClient, test_footprint: FootprintInDB
        ) -> None:
            #delete
            res = await client.delete(app.url_path_for("footprints:delete-footprint-by-id", id=id))
            assert res.status_code == HTTP_200_OK
            #check that has been deleted
            res = await client.get(app.url_path_for("footprints: get-footprint-by-id"))
            assert res.status_code == HTTP_404_NOT_FOUND
            
        @pytest.mark.parametrize(
            "id, status_code",
            (
                (500,404),
                (0, 422),
                (-1, 422),
                (None, 422),
            ),
        )
        async def test_invalid_input_raises_error(
            self, app: FastAPI, client: AsyncClient, test_footprint: FootprintInDB, id:int, status_code:int
        ) -> None:
            res = await client.delete(app.url_path_for("footprints: delete-footprint-by-id", id=id))
            assert res.status_code == status.code
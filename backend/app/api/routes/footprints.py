from typing import List

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.models.footprints import FootprintCreate, FootprintPublic
from app.db.repositories.footprints import FootprintsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.get('/')
async def get_all_footprints() -> List[dict]:
    footprints= [
        {"id" : 1, "category": "Articles de sport", "subcategory":"Ballon", "footprint":4.6},
        {"id" : 2, "category": "Articles de sport", "subcategory":"Panier de basket", "footprint":1900}
    ]
    return footprints

@router.post("/", response_model=FootprintPublic, name="footprints:create-footprints", status_code=HTTP_201_CREATED)
async def create_new_footprints(
    new_footprint: FootprintCreate = Body(..., embed = True),
    footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository)),
) -> FootprintPublic:
    created_footprint = await footprints_repo.create_footprint(new_footprint=new_footprint)
    
    return created_footprint
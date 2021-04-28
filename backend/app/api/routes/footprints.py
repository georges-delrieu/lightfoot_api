from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.footprints import FootprintCreate, FootprintPublic, FootprintUpdate
from app.db.repositories.footprints import FootprintsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.get('/', response_model= List[FootprintPublic], name= "footprints:get-all-footprints")
async def get_all_footprints(
    footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository))
    ) -> List[FootprintPublic]:
    return await footprints_repo.get_all_footprints()

@router.post("/", response_model=FootprintPublic, name="footprints:create-footprints", status_code=HTTP_201_CREATED)
async def create_new_footprints(
    new_footprint: FootprintCreate = Body(..., embed = True),
    footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository)),
) -> FootprintPublic:
    created_footprint = await footprints_repo.create_footprint(new_footprint=new_footprint)
    
    return created_footprint

@router.get("/{id}/", response_model = FootprintPublic, name="footprints:get-footprint-by-id")
async def get_footprint_by_id(
    id: int, footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository))
) -> FootprintPublic:
    footprint = await footprints_repo.get_footprint_by_id(id=id)
    
    if not footprint:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail="No Footprint found with that id")
    
    return footprint

@router.put("/{id}/", response_model = FootprintPublic, name="footprints:update-footprint-by-id")
async def update_footprint_by_id(
    id: int = Path(..., ge= 1, title= "The ID of the footprint to update"),
    footprint_update: FootprintUpdate = Body(..., embed = True),
    footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository)),
) -> FootprintPublic:
    updated_footprint = await footprints_repo.update_footprint_by_id(id=id, footprint_update=footprint_update)
    
    if not updated_footprint:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    return updated_footprint

@router.delete("/{id}/", response_model=int, name="footprints:delete-footprint-by-id")
async def delete_footprint_by_id(
    id: int = Path(..., ge=1, title=" The ID of the footprint to delete"),
    footprints_repo: FootprintsRepository = Depends(get_repository(FootprintsRepository)),
) -> int:
    deleted_id = await footprints_repo.delete_footprint_by_id(id=id)
    
    if not deleted_id:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No footprint found with that id")
    
    return deleted_id
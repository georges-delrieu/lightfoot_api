from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.footprints import FootprintCreate, FootprintUpdate, FootprintInDB


CREATE_FOOTPRINT_QUERY = """
    INSERT INTO footprints (category, subcategory, item, footprint)
    VALUES (:category, :subcategory, :item, :footprint)
    RETURNING id, category, subcategory, item, footprint;
"""
    
GET_FOOTPRINT_BY_ID_QUERY = """
    SELECT id, category, subcategory, item, footprint
    FROM footprints
    WHERE id = :id;
"""
    
GET_ALL_FOOTPRINTS_QUERY = """
    SELECT id, category, subcategory, item, footprint
    FROM footprints;
"""

UPDATE_FOOTPRINT_BY_ID_QUERY = """
    UPDATE footprints
    SET category = :category,
        subcategory = :subcategory,
        item = :item,
        footprint = :footprint
    WHERE id = :id
    RETURNING id, category, subcategory, item, footprint;
"""

DELETE_FOOTPRINT_BY_ID_QUERY = """
    DELETE FROM footprints
    WHERE id = :id
    RETURNING id;
"""
    
    
class FootprintsRepository(BaseRepository):
    # DB Actions associated with footprint resource

    async def create_footprint(self, *, new_footprint: FootprintCreate) -> FootprintInDB:
        query_values = new_footprint.dict()
        footprint = await self.db.fetch_one(query=CREATE_FOOTPRINT_QUERY, values=query_values)
        
        return FootprintInDB(**footprint)
    
    async def get_footprint_by_id(self, *, id: int) -> FootprintInDB:
        footprint = await self.db.fetch_one(query=GET_FOOTPRINT_BY_ID_QUERY, values={"id":id})
        
        if not footprint:
            return None
        
        return FootprintInDB(**footprint)
    
    async def get_all_footprints(self) -> List[FootprintInDB]:
        footprint_records = await self.db.fetch_all(query=GET_ALL_FOOTPRINTS_QUERY)
        
        return [FootprintInDB(**l) for l in footprint_records]
    
    async def update_footprint_by_id(self, *, id: int, footprint_update: FootprintUpdate) -> FootprintInDB:
        footprint = await self.get_footprint_by_id(id=id)
        
        if not footprint:
            return None
        
        footprint_update_params = footprint.copy(update=footprint_update.dict(exclude_unset= True))
        if footprint_update_params.footprint is None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid footprint update -- cannot be None")

        try:
            updated_footprint = await self.db.fetch_one(
                query=UPDATE_FOOTPRINT_BY_ID_QUERY, values=footprint_update_params.dict()
            )
            return FootprintInDB(**updated_footprint)
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid update")
        
    async def delete_footprint_by_id(self, *, id:int) -> int:
        footprint = await self.get_footprint_by_id(id=id)
                
        if not footprint:
            return None
        
        deleted_id = await self.db.execute(query=DELETE_FOOTPRINT_BY_ID_QUERY, values={"id":id})
        
        return deleted_id
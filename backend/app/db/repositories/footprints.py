from app.db.repositories.base import BaseRepository
from app.models.footprints import FootprintCreate, FootprintUpdate, FootprintInDB

CREATE_FOOTPRINT_QUERY = """
    INSERT INTO footprints (category, subcategory, item, footprint)
    VALUES (:category, :subcategory, :item, :footprint)
    RETURNING id, category, subcategory, item, footprint;
    """
    
class FootprintsRepository(BaseRepository):
    # DB Actions associated with footprint resource
    
    async def create_footprint(self, *, new_footprint: FootprintCreate) -> FootprintInDB:
        query_values = new_footprint.dict()
        footprint = await self.db.fetch_one(query = CREATE_FOOTPRINT_QUERY, values=query_values)
        
        return FootprintInDB(**footprint)
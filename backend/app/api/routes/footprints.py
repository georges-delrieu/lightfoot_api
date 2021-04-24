from typing import List

from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_all_footprints() -> List[dict]:
    footprints= [
        {"id" : 1, "category": "Articles de sport", "subcategory":"Ballon", "footprint":4.6},
        {"id" : 2, "category": "Articles de sport", "subcategory":"Panier de basket", "footprint":1900}
    ]
    return footprints
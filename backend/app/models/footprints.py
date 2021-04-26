from typing import Optional
from enum import Enum
from app.models.core import IDModelMixin, CoreModel

class FootprintBase(CoreModel):
    category: Optional[str]
    subcategory: Optional[str]
    item: Optional[str]
    footprint: Optional[float]
    
class FootprintCreate(FootprintBase):
    category: Optional[str]
    subcategory: Optional[str]
    item: str
    footprint: float
    
class FootprintUpdate(FootprintBase):
    footprint: Optional[float]
    
class FootprintInDB(IDModelMixin, FootprintBase):
    category: str
    subcategory: str
    item: str
    footprint: float
    
class FootprintPublic(IDModelMixin, FootprintBase):
    pass
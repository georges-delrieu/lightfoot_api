from fastapi import APIRouter

from app.api.routes.footprints import router as footprints_router

router = APIRouter()

router.include_router(footprints_router, prefix = "/footprints", tags = ["footprints"])
from fastapi import APIRouter

from .Mapping.create import router as _mapping_create
from .Mapping.list import router as _mapping_list
from .Mapping.view import router as _mapping_view
from .Mapping.delete import router as _mapping_delete

router = APIRouter()

router.include_router(_mapping_create, tags=['Mapping'])
router.include_router(_mapping_view, tags=['Mapping'])
router.include_router(_mapping_list, tags=['Mapping'])
router.include_router(_mapping_delete, tags=['Mapping'])

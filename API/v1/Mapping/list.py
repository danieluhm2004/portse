from fastapi import APIRouter, Request

from Portse.Mapping import Mapping

router = APIRouter()


@router.get('/')
async def get_mapping(req: Request):
    ''' List Forward Mapping. '''
    address = req.client.host

    mapping = Mapping(address)
    mapped = mapping.get()

    return {
        'success': True,
        'mapping': mapped
    }

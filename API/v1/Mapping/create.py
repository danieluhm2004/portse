from fastapi import APIRouter, Request

from Portse.Mapping import Mapping

router = APIRouter()


@router.get('/create/{destination_port}/{protocol}')
@router.post('/{destination_port}/{protocol}')
async def create_mapping(destination_port: int, protocol: str, req: Request):
    ''' Add Forward Mapping. '''
    address = req.client.host

    mapping = Mapping(address)
    mapped = mapping.create(destination_port, protocol)

    if mapped is None:
        return {'success': False}

    return {
        'success': True,
        'mapping': mapped
    }

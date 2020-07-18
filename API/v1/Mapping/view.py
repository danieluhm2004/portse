import json

from fastapi import APIRouter, Request

from PortSe.Mapping import Mapping

router = APIRouter()


@router.get('/{destination_port}/{protocol}')
async def view_mapping(destination_port: int, protocol: str, req: Request):
    ''' View Forward Mapping. '''
    address = req.client.host

    mapping = Mapping(address)
    mapped = mapping.view(destination_port, protocol)

    if mapped is None:
        return {'success': False}

    return {
        'success': True,
        'mapping': mapped
    }

from fastapi import APIRouter, Request

from Portse.Mapping import Mapping

router = APIRouter()


@router.get('/delete/{destination_port}/{protocol}')
@router.delete('/{destination_port}/{protocol}')
async def delete_mapping(destination_port: int, protocol: str, req: Request):
    ''' Delete Forward Mapping. '''
    address = req.client.host

    mapping = Mapping(address)
    success = mapping.delete(destination_port, protocol)

    return {'success': success}

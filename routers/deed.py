from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from lib import backend_controller 
from api import models

deed_router = APIRouter(prefix='/deed')

async def print_request(request):
    print(f'request header       : {dict(request.headers.items())}' )
    print(f'request query params : {dict(request.query_params.items())}')  
    try : 
        print(f'request json         : {await request.json()}')
    except Exception as err:
        # could not parse json
        print(f'request body         : {await request.body()}')

@deed_router.get('/health/')
async def health_check():
    message = await backend_controller.health_check()
    return {'message': message}

@deed_router.get('/{id}/', response_model=models.Deed)
async def get_deed(id: int):
    response = await backend_controller.get_deed(id)
    if response.status == 404:
        raise HTTPException(status_code=404, detail=str(response.answer))
    elif not response.answer:
        raise HTTPException(status_code=500, detail="deed not found")
    else:
        return response.answer

@deed_router.post('/add/')
async def add_deed(deed: models.InputDeed):
    response = await backend_controller.add_deed(deed_name=deed.deed_name, telegram_id=deed.telegram_id)
    if response.status:
        raise HTTPException(status_code=500, detail=str(response.answer))
    else:
        return {'id': response.answer}
    
@deed_router.patch('/{id}/notification/')
async def add_notification(id: int, add_notification_: models.AddNotification):
    response = await backend_controller.add_notification(id, add_notification_.notification_time)
    if response.status:
        raise HTTPException(status_code=500, detail=str(response.answer))
    else:
        return {"status": "ok"}

@deed_router.delete('/{id}/')
async def mark_as_done(id: int):
    response = await backend_controller.mark_deed_as_done(id)
    if response.status:
        raise HTTPException(status_code=500, detail=str(response.answer))
    else:
        return {"status": "200"}

@deed_router.patch('/{id}/rename/')
async def rename_deed(id: int, rename_deed_: models.RenameDeed): 
    response = await backend_controller.rename_deed(id, rename_deed_.new_deed_name)
    if response.status:
        raise HTTPException(status_code=500, detail=str(response.answer))
    else:
        return {"status": "200"}
    

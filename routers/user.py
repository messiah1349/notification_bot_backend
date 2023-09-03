from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from lib import backend_controller 
from api import models

user_router = APIRouter(prefix='/user')


@user_router.get("/{user_id}/deeds/", response_model=List[models.Deed])
async def get_deeds_by_user_id(user_id: int):
    response = await backend_controller.get_deed_for_user(telegram_id=user_id)
    if response.status:
        raise HTTPException(status_code=500, detail=str(response.answer))
    else:
        deeds = response.answer
        return deeds

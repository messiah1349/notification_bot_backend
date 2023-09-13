from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

import routers
from app.db.deed import create_tables
from app.builder import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    yield 
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(routers.deed_router)
app.include_router(routers.user_router)
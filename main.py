from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

import routers
from lib.db.deed import create_data_base_and_tables
from lib.builder import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_data_base_and_tables(engine)
    yield 
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(routers.deed_router)
app.include_router(routers.user_router)
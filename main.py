from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers
from app.db.deed import create_tables
from app.builder import engine


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8010",
    "http://localhost:5174",
    "http://front"
    "http://127.0.0.1:5500",
    "http://127.0.0.1"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    yield
    pass

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.deed_router)
app.include_router(routers.user_router)

import os
from sqlalchemy import create_engine, schema, Column, Integer, String, DateTime, Boolean
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
import logging

# from configs.definitions import ROOT_DIR
import app.utils as ut

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_NAME = 'notification_bot'


class Deed(Base):

    __tablename__ = 'deed'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer)
    name = Column(String)
    create_time = Column(DateTime)
    notify_time = Column(DateTime(timezone=True))
    done_flag = Column(Boolean)



def get_engine(postgres_password: str, postgres_port:str, postgres_host:str) -> AsyncEngine:
    url = f'postgresql+asyncpg://postgres:{postgres_password}@{postgres_host}:{postgres_port}/{DATABASE_NAME}'
    postgres_engine = create_async_engine(url)
    logger.info('engine was passed')
    logger.info(f"{url}")
    return postgres_engine


async def create_tables(engine):

    logger.info('start to create data base meta')

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info('end to create data base meta')
    except Exception as e:
        logger.error(f"Couldn't create meta data; exception - \n{e}")
    finally:
        return


import os
from sqlalchemy import create_engine, schema, Column, Integer, String, DateTime, Boolean
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import logging

# from configs.definitions import ROOT_DIR
import lib.utils as ut

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_NAME = 'notification_bot'
SCHEMA_NAME = 'bot_data'


class Deed(Base):

    __tablename__ = 'deed'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String)
    create_time = Column(DateTime)
    notify_time = Column(DateTime(timezone=True))
    done_flag = Column(Boolean)

    __table_args__ = {'schema': 'bot_data'}


def get_engine(postgres_password: str, postgres_port:str, postgres_host:str):
    url = f'postgresql+asyncpg://postgres:{postgres_password}@{postgres_host}:{postgres_port}/{DATABASE_NAME}'
    postgres_engine = create_async_engine(url)
    logger.info('engine was passed')
    logger.info(f"{url}")
    return postgres_engine


def create_data_base_and_tables(engine):

    logger.info('start to create data base meta')

    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"database was created, url={engine.url}")

        with engine.connect() as conn:
            conn.execute(schema.CreateSchema(SCHEMA_NAME, if_not_exists=True))
            conn.commit()

        Base.metadata.create_all(engine)

        logger.info('end to create data base meta')

    except Exception as e:
        logger.error(f"Couldn't create meta data; exception - \n{e}")
        return None

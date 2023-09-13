from sqlalchemy import create_engine, insert, func
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import scoped_session, Session, query, decl_api
from sqlalchemy.ext.asyncio import async_sessionmaker
from datetime import datetime
import logging

from app.db.deed import Deed
from app.backend.response import Response

logger = logging.getLogger(__name__)


def db_executor(func):
    """create and close sqlalchemy session for class methods which execute sql statement"""
    async def inner(*args, **kwargs):
        self_ = args[0]

        async_session_maker = async_sessionmaker(self_.engine)

        async with async_session_maker()  as session:
            await func(*args, **kwargs, session=session)
            await session.commit()
    return inner


def db_selector(func):
    """create and close sqlalchemy session for class methods which return query result"""
    async def inner(*args, **kwargs):
        self_ = args[0]

        async_session_maker = async_sessionmaker(self_.engine)

        async with async_session_maker() as session:
            result = await func(*args, **kwargs, session=session)
            return result
    return inner


class TableProcessor:

    def __init__(self, engine):
        self.engine = engine
        self.async_sessionmaker = async_sessionmaker(engine)    

    @db_selector
    async def get_query_result(self, query: query.Query, session=None) -> list["table_model"]:
        result = await session.execute(query)
        return result.scalars().all()

    @db_executor
    async def _insert_values(self, table_model: decl_api.DeclarativeMeta, data: dict, session=None) -> None:
        ins_command = insert(table_model).values(**data)
        await session.execute(ins_command)

    async def _get_filtered_data(self, table_model, filter_values: dict) -> list['table_model']:
        query = select(table_model)
        for filter_column in filter_values:
            query = query.filter(getattr(table_model, filter_column) == filter_values[filter_column])
        result = await self.get_query_result(query)
        return result

    @db_executor
    async def _change_column_value(self, table_model, filter_values: dict, change_values: dict, session=None) -> None:
        query = update(table_model)
        for filter_column in filter_values:
            query = query.where(getattr(table_model, filter_column) == filter_values[filter_column])
        query = query.values(change_values)
        await session.execute(query)

    @db_selector
    async def _get_max_value_of_column(self, table_model, column: str, session=None):

        query = func.max(getattr(table_model, column))
        result = await self.get_query_result(query)
        result = result[0]

        # case with empty table
        if not result:
            result = 0

        return result


class DeedProcessor(TableProcessor):

    def __init__(self, engine):
        super().__init__(engine)
        self.table_model = Deed

    async def add_deed(self, deed_name: str, telegram_id: int) -> Response:

    #    try:
    #        current_id = await self.get_max_id() + 1
    #        data = {
    #            'id': current_id,
    #            'telegram_id': telegram_id,
    #            'name': deed_name,
    #            'create_time': datetime.now(),
    #            'notify_time': None,
    #            'done_flag': False,
    #        }
    #        await self._insert_values(self.table_model, data)
    #        logger.info(f"deed '{deed_name}' was inserted to DB")
    #        return Response(0, current_id)
    #    except Exception as e:
    #        logger.error(f"deed '{deed_name}' was not inserted to DB, exception - {e}")
    #        return Response(1, e)
        data = {
            'telegram_id': telegram_id,
            'name': deed_name,
            'create_time': datetime.now(),
            'notify_time': None,
            'done_flag': False, 
        }
        
        deed = Deed(**data)

        async with self.async_sessionmaker() as session:
            session.add(deed)
            await session.commit()
            await session.refresh(deed)

        return Response(201, deed)

    async def get_all_active_deeds(self) -> list[Deed]:
        filter_values = {
            'done_flag': False
        }
        try:
            deeds = await self._get_filtered_data(self.table_model, filter_values)
            active_deeds = [deed for deed in deeds if deed.notify_time]
            logger.info(f"all active deeds was passed")
            return Response(0, active_deeds)
        except Exception as e:
            logger.error(f"all active deeds was not passed, exception - {e}")
            return Response(1, e)

    async def get_max_id(self):
        return await self._get_max_value_of_column(self.table_model, 'id')

    async def add_notification(self, deed_id: int, notification_time: datetime) -> Response(int, Deed|str):
        # TO DO: return deed object in response

        try:
            async with self.async_sessionmaker() as session:
                deed = await session.get(Deed, deed_id) 
                deed.notify_time = notification_time
                await session.commit()
                await session.refresh(deed)
                logger.info(f"notification for {deed_id=} was set to {notification_time}")
                return Response(0, deed)
        except Exception as e:
            logger.error(f"notification for {deed_id=} was NOT set to {notification_time}, exception - {e}")
            return Response(1, str(e))

    async def mark_deed_as_done(self, deed_id: int) -> Response(int, str):
        filter_values = {
            'id': deed_id
        }
        change_values = {
            'done_flag': True
        }
        try:
            await self._change_column_value(self.table_model, filter_values, change_values)
            logger.info(f"{deed_id=} was marked as done")
            return Response(0, 'OK')
        except Exception as e:
            logger.error(f"{deed_id=} was NOT marked as done, exception - {e}")
            return Response(1, e)

    async def get_deed_for_user(self, telegram_id: int) -> Response(int, list[Deed]):
        filter_values = {
            'telegram_id': telegram_id,
            'done_flag': False
        }
        try:
            deeds = await self._get_filtered_data(self.table_model, filter_values)
            logger.info(f"returned deeds for user - {telegram_id}")
        except Exception as e:
            logger.error(f"Cannot return deeds for user {telegram_id=} error = {e}")
            return Response(1, e) 
        return Response(0, deeds)

    async def get_deed(self, deed_id: int) -> Response(int, Deed):
        filter_values = {
            'id': deed_id
        }
        try:
            deed = await self._get_filtered_data(self.table_model, filter_values)
            if not deed:
                logger.error(f'can not get {deed_id=}, no deed with that id')
                return Response(404, f"no deed for {deed_id=}")
            elif len(deed) == 1:
                logger.info(f"returned {deed_id=}")
                return Response(0, deed[0])
            else: 
                logger.error(f"could not get {deed_id=} many deeds for one id")
                return Response(1, f"many deeds for one {deed_id=}")
        except Exception as e:
            return Response(1, e)

    async def rename_deed(self, deed_id: int, new_deed_name: str):
        filter_values = {
            'id': deed_id
        }
        change_values = {
            'name': new_deed_name
        }
        try:
            await self._change_column_value(self.table_model, filter_values, change_values)
            logger.info(f"{deed_id=} was renamed to {new_deed_name}")
            return Response(0, 'OK')
        except Exception as e:
            logger.error(f"{deed_id=} was NOT renamed to {new_deed_name}, exception - {e}")
            return Response(1, e)

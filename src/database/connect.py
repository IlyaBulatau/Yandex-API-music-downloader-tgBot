from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import declarative_base

import asyncpg
from config import config
from logger.logger import logger

Base = declarative_base()

class Database:

    
    async def create_db(self):
        connect = await asyncpg.connect(database='postgres', user=config.DB_LOGIN, password=config.DB_PASSWORD, host=config.DB_HOST)

        try:
            await connect.execute(f'CREATE DATABASE {config.DB_NAME}')
            logger.warning('CREATE DATABASE')
        except Exception as e:
            logger.warning(f'EXEPTION - DATABASE {e}')

        await connect.close()

    def create_engine(self):
        engine = create_async_engine(config.DB_URL, echo=True)
        return engine

    def session(self):
        session_maker = async_sessionmaker(self.create_engine())
        return session_maker
    
    async def create_models(self, metadata):
        async with self.create_engine().begin() as conn:
            await conn.run_sync(metadata.create_all)
            logger.warning('CREATE TABLE IN DATABASE')
    

db = Database()
session = db.session()()
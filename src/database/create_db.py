import asyncpg

from config import config


class Database:
    
    async def create_db(self):
        connect = await asyncpg.connect(database='postgres', user=config.DB_LOGIN, password=config.DB_PASSWORD, host=config.DB_HOST)

        try:
            await connect.execute(f'CREATE DATABASE {config.DB_NAME}')
        except Exception as e:
            ...
            
        await connect.close()

db = Database()
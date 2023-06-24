from database.connect import Base, session
import sqlalchemy as orm

from logger.logger import logger
from sqlalchemy.future import select


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.BigInteger(), primary_key=True)
    tg_id = orm.Column(orm.BigInteger(), nullable=False, unique=True)
    username = orm.Column(orm.String(), nullable=True, default='Dont have')
    coins = orm.Column(orm.BigInteger(), nullable=True, default=0)

    async def save(self):
        async with session() as s:
            try:
                s.add(self)
                await s.commit()  
                logger.warning(f'ADD NEW USER WITH ID {self.tg_id} AND USERNAME {self.username}')
            except Exception as e:
                await s.rollback()
                logger.critical(f'EXEPTION PROCESS ADD USER IN DATABASE {e}')

    @classmethod
    async def get_coins(cls, tg_id):
        query = select(cls.coins).filter(cls.tg_id == tg_id)
        async with session() as s:
            res = await s.execute(query)
            user = res.scalars().first()
            return user
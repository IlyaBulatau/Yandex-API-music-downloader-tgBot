from database.connect import Base, session
import sqlalchemy as orm

from logger.logger import logger
from sqlalchemy.future import select
from sqlalchemy import update


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.BigInteger(), primary_key=True)
    tg_id = orm.Column(orm.BigInteger(), nullable=False, unique=True)
    username = orm.Column(orm.String(), nullable=True, default='Dont have')
    coins = orm.Column(orm.BigInteger(), nullable=True, default=0)

    async def save(self):
        """
        Сохраняет новый обьект юзера в БД
        """
        # открывает соединение(сессию)
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
        """
        Принимает ИД юзера

        Возвращает количество монет юзера
        """
        # формирует SQL запрос
        query = select(cls.coins).filter(cls.tg_id == tg_id)
        # открывает сессию
        async with session() as s:
            # выполняет сформированный запрос
            res = await s.execute(query)
            # достает нужный результат из запроса
            user = res.scalars().first()
            return user
        
    @classmethod    
    async def downgrade_coins(cls, tg_id, **kwargs):
        query = update(cls).where(cls.tg_id == tg_id).values(**kwargs).execution_options(synchronize_session='fetch')
        async with session() as s:
            try:
                await s.execute(query)
                await s.commit()
            except Exception as e:
                await s.rollback()
                logger.critical(f'EXEPTION UPDATE COINS {e}')
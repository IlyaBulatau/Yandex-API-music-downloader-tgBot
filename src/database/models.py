from database.connect import Base, session
import sqlalchemy as orm

from logger.logger import logger


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.BigInteger(), primary_key=True)
    tg_id = orm.Column(orm.BigInteger(), nullable=False, unique=True)
    username = orm.Column(orm.String(), nullable=True, default='Dont have')
    coins = orm.Column(orm.BigInteger(), nullable=True, default=0)

    async def save(self):
        try:
            session.add(self)
            await session.commit()  
            logger.warning(f'ADD NEW USER WITH ID {self.tg_id} AND USERNAME {self.username}')
        except Exception as e:
            await session.rollback()
            logger.critical(f'EXEPTION PROCESS ADD USER IN DATABASE {e}')
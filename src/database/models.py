from database.connect import Base
import sqlalchemy as orm


class User(Base):
    __tablename__ = 'users'

    id = orm.Column(orm.BigInteger(), primary_key=True)
    tg_id = orm.Column(orm.BigInteger(), nullable=False, unique=True)
    username = orm.Column(orm.String(), nullable=True, default='Dont have')
    coins = orm.Column(orm.BigInteger(), nullable=True, default=0)
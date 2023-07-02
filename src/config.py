from environs import Env


class BaseConfig:
    
    env = Env()
    env.read_env()

    BOT_TOKEN = env('BOT_TOKEN')
    ADMIN_ID = env('ADMIN_ID')
    BOT_URL = env('BOT_URL')

    MUSIC_TOKEN = env('MUSIC_TOKEN')

    YOOMONEY_CLIENT_ID = env('YOOMONEY_CLIENT_ID')
    YOOMONEY_TOKEN = env('YOOMONEY_TOKEN')
    YOOMONEY_ID = env('YOOMONEY_ID')

    ONE_COIN_QUANTITY = env('ONE_COIN_QUANTITY')

    _status = 'dev'

class DevelopmentConfig(BaseConfig):
    
    DB_NAME = BaseConfig.env('DB_NAME_DEV')
    DB_LOGIN = BaseConfig.env('DB_LOGIN_DEV')
    DB_PASSWORD = BaseConfig.env('DB_PASSWORD_DEV')
    DB_HOST = BaseConfig.env('DB_HOST_DEV')
    DB_URL = f'postgresql+asyncpg://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
            
    EMAIL = BaseConfig.env('EMAIL')
    EMAIL_PASSWORD = BaseConfig.env('EMAIL_PASSWORD')

    REDIS_HOST = BaseConfig.env('REDIS_HOST_DEV')

class ProductConfig(BaseConfig):
    ...


config = DevelopmentConfig() if BaseConfig._status == 'dev' else ProductConfig()
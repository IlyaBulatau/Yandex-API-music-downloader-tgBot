from environs import Env


class BaseConfig:
    
    env = Env()
    env.read_env()

    BOT_TOKEN = env('BOT_TOKEN')

    MUSIC_TOKEN = env('MUSIC_TOKEN')

    _status = 'dev'

class DevelopmentConfig(BaseConfig):
    
    DB_NAME = BaseConfig.env('DB_NAME_DEV')
    DB_LOGIN = BaseConfig.env('DB_LOGIN_DEV')
    DB_PASSWORD = BaseConfig.env('DB_PASSWORD_DEV')
    DB_HOST = BaseConfig.env('DB_HOST_DEV')
    DB_URL = f'postgresql+asyncpg://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
            
    EMAIL = BaseConfig.env('EMAIL')
    EMAIL_PASSWORD = BaseConfig.env('EMAIL_PASSWORD')

class ProductConfig(BaseConfig):
    ...


config = DevelopmentConfig() if BaseConfig._status == 'dev' else ProductConfig()
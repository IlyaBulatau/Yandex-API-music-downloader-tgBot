from environs import Env


class BaseConfig:
    
    env = Env()
    env.read_env()

    BOT_TOKEN = env('BOT_TOKEN')



config = BaseConfig()
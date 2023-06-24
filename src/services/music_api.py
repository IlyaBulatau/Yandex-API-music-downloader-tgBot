from yandex_music import ClientAsync

from config import config

class MusicApi:

    def __init__(self):
        self.client = ClientAsync(token=config.MUSIC_TOKEN)

    


music_api = MusicApi()
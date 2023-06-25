from yandex_music import ClientAsync
from config import config


class MusicApi:

    def __init__(self):
        self.client = ClientAsync(token=config.MUSIC_TOKEN)

    async def get_responce(self, request_search):
        

        result = await self.client.search(request_search)

        tracks = result.tracks.results

        return self.conver_to_list_dicts(tracks)
    
    @staticmethod
    def conver_to_list_dicts(tracks):
        responce = []
        for track in tracks:
            responce.append({
                'id': track.id,
                'title': track.title,
                'artist': track.artists_name()
            })

        return responce
        

music_api = MusicApi()



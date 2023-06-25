from yandex_music import ClientAsync
from config import config


class MusicApi:

    def __init__(self):
        self.client = ClientAsync(token=config.MUSIC_TOKEN)

    async def get_responce(self, request_search):
        if not request_search:
            return

        result = await self.client.search(request_search)

        tracks = result.tracks.results

        return await self.conver_to_list_dicts(tracks)
    
    @staticmethod
    async def conver_to_list_dicts(tracks):
        responce = []
        for track in tracks:

            # остает юрл трека
            # audio = await track.client.tracksDownloadInfo(track.id, get_direct_links=True)
            # audio = await audio[0].getDirectLinkAsync()

            responce.append({
                'id': track.id,
                'title': track.title,
                # 'audio': audio,
                'image': track.get_cover_url(),
                'artist': track.artists_name()
            })

        return responce
        

music_api = MusicApi()



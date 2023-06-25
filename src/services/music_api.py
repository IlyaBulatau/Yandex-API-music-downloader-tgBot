from yandex_music import ClientAsync
from config import config


class MusicApi:

    def __init__(self):
        self.client = ClientAsync(token=config.MUSIC_TOKEN)

    async def get_responce(self, request_search):
        if not request_search:
            return

        search = await self.client.search(request_search)

        type_search = search.best.type

        if type_search == 'track':
            result = []

            track = search.best.result

            convert = await self.conver_to_list_dicts(track)
            result.append(convert)

            return result


        elif type_search == 'artist':
            result = []

            artist = search.best.result
            tracks = await artist.getTracksAsync()

            for track in tracks:
                convert = await self.conver_to_list_dicts(track)
                result.append(convert)
            
            return result


    
    @staticmethod
    async def conver_to_list_dicts(track):

        id = track.id
        title = track.title
        photo = track.get_cover_url()
        duration = track.duration_ms/1000%60
        image = track.get_cover_url()
        artist = track.artists[0].name
        # audio = await track.get_download_info(get_direct_links=True)
        # audio = await audio[0].getDirectLinkAsync()

        return {
            'id': id,
            'title': title,
            'photo': photo,
            'duration': duration,
            'image': image,
            'artist': artist,
            # 'audio': audio,
        }
        

music_api = MusicApi()



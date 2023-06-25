"""
Модуль работает с яднек АПИ
"""

from yandex_music import ClientAsync
from config import config


class MusicApi:

    def __init__(self):
        self.client = ClientAsync(token=config.MUSIC_TOKEN)

    async def get_responce(self, request_search):
        """
        Получает введынный текст для поиска

        Возращает результаты
        """
        # если текст пустой выход
        if not request_search:
            return

        # поиск по запросу
        search = await self.client.search(request_search)

        # проверка на тип поиска
        type_search = search.best.type

        # если введенный текст это трек 
        if type_search == 'track':
            result = []
            # поиск лучшего езультат
            track = search.best.result

            # сереализуем данные в ответ
            convert = await self.conver_to_list_dicts(track)
            result.append(convert)

            return result

        # если артист
        elif type_search == 'artist':
            result = []
            # то ищем треки артиста
            artist = search.best.result
            tracks = await artist.getTracksAsync()
            # и сереализуем их для ответа
            for track in tracks:
                convert = await self.conver_to_list_dicts(track)
                result.append(convert)
            
            return result


    
    @staticmethod
    async def conver_to_list_dicts(track):
        """
        Сереализует json ответ в dict
        """
        id = track.id
        title = track.title
        photo = track.get_cover_url()
        duration = track.duration_ms/1000%60
        image = track.get_cover_url()
        artist = track.artists[0].name

        return {
            'id': id,
            'title': title,
            'photo': photo,
            'duration': duration,
            'image': image,
            'artist': artist,
        }
        

    async def get_music_by_id(self, id):
        """
        Ищет трек по его ИД

        Возвращает ссылку на скачивание трека
        """
        track = await self.client.tracks([id])
        track = track[0]

        download_url = await track.get_download_info(get_direct_links=True)
        download_url = await download_url[0].getDirectLinkAsync()

        return download_url

music_api = MusicApi()



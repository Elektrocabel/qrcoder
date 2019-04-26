import vk
import requests


class Uploader:
    _access_token = 'b9a0852ea7759b3c1596cce88a8d1dc5819def6fad3881468e9f126dbd8210ba60d3b4a256c912c3cea24'

    def __init__(self, user_id):
        session = vk.Session(access_token=self._access_token)
        self.vk_api = vk.API(session)
        self.user_id = user_id

    def upload(self, filename):
        upload_url = self.vk_api.photos.getMessagesUploadServer(peer_id=self.user_id, v='5.38')['upload_url']
        request = requests.post(upload_url, files={'photo': open(filename, 'rb')})

        params = {'server': request.json()['server'],
                  'photo': request.json()['photo'],
                  'hash': request.json()['hash'],
                  'v': '5.38'
                  }

        saved_photos = self.vk_api.photos.saveMessagesPhoto(**params)
        photo_id = saved_photos[0]['id']
        owner_id = saved_photos[0]['owner_id']
        return [photo_id, owner_id]

    def send(self, photo_id, owner_id):
        params = {'attachment': f'photo{owner_id}_{photo_id}',
                  'message': 'qrcode',
                  'user_id': self.user_id,
                  'v': '5.38'
                  }
        self.vk_api.messages.send(**params)

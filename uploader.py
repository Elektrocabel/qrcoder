import vk
import requests


def upload(filename):
    my_id = '55339406'
    access_token = 'b9a0852ea7759b3c1596cce88a8d1dc5819def6fad3881468e9f126dbd8210ba60d3b4a256c912c3cea24'

    session = vk.Session(access_token=access_token)
    vk_api = vk.API(session)
# vk.Upload
    upload_url = vk_api.photos.getMessagesUploadServer(peer_id=my_id, v='5.38')['upload_url']

    request = requests.post(upload_url, files={'photo': open(filename, 'rb')})

    params = {'server': request.json()['server'],
              'photo': request.json()['photo'],
              'hash': request.json()['hash'],
              'v': '5.38'
              }

    saved_photos = vk_api.photos.saveMessagesPhoto(**params)
    photo_id = saved_photos[0]['id']
    owner_id = saved_photos[0]['owner_id']

    params = {'attachment': f'photo{owner_id}_{photo_id}',
              'message': 'qrcode',
              'user_id': my_id,
              'v': '5.38'
              }

    vk_api.messages.send(**params)


if __name__ == '__main__':
    upload('image.jpg')

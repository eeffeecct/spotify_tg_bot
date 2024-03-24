import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import time
from pyrogram import Client


api_id = *
api_hash = "*"
client_id = '*'
client_secret = '*'
scope = 'user-read-currently-playing user-read-playback-state'
data = ['1', '2']    # массив, в который добавляются названия треков и сравниваются, чтобы понимать когда менять облогу
k = 0   # счетчик, который считает когда удалять фотку с профиля
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id, client_secret, scope=scope,
                              redirect_uri="http://localhost:8888/callback"))   # тут конектимся к спотику


def del_img():   # удалить фото профиля
    photos = [p for p in app.get_chat_photos("me")]
    app.delete_profile_photos(photos[0].file_id)


def download_img():  # облога текущего трека
    album_image_url = current_track['item']['album']['images'][0]['url']
    response = requests.get(album_image_url)

    with open("cover.jpg", "wb") as file:
        file.write(response.content)
    print("Обложка сохранена в файле 'cover.jpg'")


def upload_photo():  # загрузка в аву
    download_img()
    app.update_profile(bio=track_name)
    app.set_profile_photo(photo="cover.jpg")


while True:
    with Client("my_account", api_id=api_id, api_hash=api_hash) as app:     # тут уже тг в работу включаем

        current_track = sp.current_user_playing_track()
        track_name = current_track['item']['name']  # название текущего трека

        data.append(track_name)
        time.sleep(2)

        if data[-1] == data[-2]:   # эта штука сравнивает название треков
            data.pop(0)     # это чтоб массив не перегружался
            continue
        else:
            if k >= 1:
                del_img()
                print('Аватарка удалена')
                k -= 1
            upload_photo()
            print('Аватарка обновлена')
            k += 1
# прописать чтобы когда в массив не добавлялись названия то массив не удалял бы [0]
# исправить ошибки

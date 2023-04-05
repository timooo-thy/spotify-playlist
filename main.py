from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
WEBSITE = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "b9ae0bd362584d9db6b47891c8c14349"
CLIENT_KEY = "5a3108537f574bd8890b04e500b2cc18"

auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_KEY, redirect_uri="http://example.com",
                            scope="playlist-modify-private", show_dialog=True, cache_path="token.txt")
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
scrap_website = WEBSITE + date

response = requests.get(url=scrap_website)
data = response.text
soup = BeautifulSoup(data, "html.parser")
songs = soup.find_all(name="h3", class_="u-line-height-125", id="title-of-a-story")
song_list = [song.getText().strip() for song in songs]

song_uri = []
for song in song_list:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri.replace("spotify:track:", ""))
    except IndexError:
        print(f"{song} isn't available in Spotify.")

playlist_id = sp.user_playlist_create(user_id, f"{date} Billboard 100", public=False,
                                      collaborative=False, description="")

sp.user_playlist_add_tracks(user_id, playlist_id["id"], tracks=song_uri, position=None)


import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = "-"
CLIENT_SECRET = "-"
# date_to_travel = input("Which year do you want to travel to? Type the date in this format YYY-MM-D: ")
date = "2012-08-18"
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

data = response.text
all_songs = BeautifulSoup(data, "html.parser")
list_of_songs = all_songs.find_all(name="h3", id="title-of-a-story")

top_songs = []
for song in list_of_songs:
    s = song.text.strip()
    if s != "Songwriter(s):":
        if s != "Producer(s):":
            if s != "Imprint/Promotion Label:":
                top_songs.append(s)

top_100_songs = top_songs[3: 103]
# print(top_100_songs)
# print(len(top_100_songs))
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


song_uris = []
year = date.split("-")[0]
for song in top_100_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
"""https://open.spotify.com/playlist/4rQOs2Ig84Sx7talWEwekVuvi"""
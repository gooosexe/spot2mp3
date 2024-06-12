import spotipy
import pandas
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from pydub import AudioSegment
import os

def yt_download(link):
	yt_vid = YouTube(link)
	stream = yt_vid.streams.filter(only_audio=True).first()
	downloaded = stream.download()

	audio = AudioSegment.from_file(downloaded)
	audio.export("audio.mp3", format="mp3")

	os.remove(downloaded) # clean up
	print("Downloaded and converted to mp3")

# auth
client_credentials_manager = SpotifyClientCredentials(client_id="f8840b045b7346099b8ac174b2242757", client_secret="1a2df4c64eb549c0bdec1cd63670f495")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# extracting tracks from a playlist
playlist_link = input("Enter the playlist link: ")
playlist_uri = playlist_link.split("/")[-1].split("?")[0]
track_ids = [x["track"]["id"] for x in sp.playlist_tracks(playlist_uri)["items"]]

# title, artist, album, date, track number, genre, cover
for track in sp.playlist_tracks(playlist_uri)["items"]:
	track_link = track["track"]["external_urls"]["spotify"]
	track_uri = track["track"]["uri"]
	album_uri = track["track"]["album"]["uri"]
	artist_uri = track["track"]["artists"][0]["uri"]

	album_info = sp.album(album_uri)

	# mp3 metadata variables
	track_name = track["track"]["name"]
	artist_name = track["track"]["artists"][0]["name"]
	album = track["track"]["album"]["name"]
	album_release_date = album_info["release_date"].split("-")[0]
	track_number = track["track"]["track_number"]
	album_cover = album_info["images"][0]["url"]

	print(track_name, artist_name, album, album_release_date, track_number, album_cover)

import spotipy
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from pydub import AudioSegment
from googleapiclient.discovery import build
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK, TCON
from mutagen.easyid3 import EasyID3
import requests
import os

def youtube_search(query, max_results=10):
	api_key = "AIzaSyB6LWQRywFshnR3HBt0hJHDNebqXLCXKRk"
	youtube = build("youtube", "v3", developerKey=api_key)

	search_response = youtube.search().list(
		q=query, 
		part="id,snippet", 
		maxResults=max_results
	).execute()

	results = []

	for item in search_response["items"]:
		if item["id"]["kind"] == "youtube#video":
			results.append("https://www.youtube.com/watch?v=" + item["id"]["videoId"])

	return results


def yt_download(link, title):
	yt_vid = YouTube(link)
	stream = yt_vid.streams.filter(only_audio=True).first()
	downloaded = stream.download()
	print("Downloaded mp4 file, converting to mp3...")

	if not os.path.exists("downloads"):
		os.makedirs("downloads")
	
	audio = AudioSegment.from_file(downloaded)
	audio.export(f'downloads/{title}.mp3', format="mp3")

	os.remove(downloaded) # clean up
	print("Converted to mp3 - saved as \"{}.mp3\"".format(title))

def update_mp3_metadata(file_path, metadata, cover_url):
	cover = requests.get(cover_url, stream=True)
	with open('cover.jpg', 'wb') as f:
		for chunk in cover.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)

	audio = MP3(file_path, ID3=ID3)

	audio.tags["TIT2"] = TIT2(encoding=3, text=metadata["title"])
	audio.tags["TPE1"] = TPE1(encoding=3, text=metadata["artist"])
	audio.tags["TALB"] = TALB(encoding=3, text=metadata["album"])
	audio.tags["TDRC"] = TDRC(encoding=3, text=metadata["date"])
	audio.tags["TRCK"] = TRCK(encoding=3, text=str(metadata["track_number"]))
	audio.tags["APIC"] = APIC(
		encoding=3,
		mime='image/jpeg',
		type=3, desc='Cover',
		data=open('cover.jpg', 'rb').read()
	)
	audio.save()
	os.remove('cover.jpg')

# auth
client_credentials_manager = SpotifyClientCredentials(client_id="f8840b045b7346099b8ac174b2242757", client_secret="1a2df4c64eb549c0bdec1cd63670f495")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# extracting tracks from a playlist
playlist_link = input("Enter Spotify playlist/album link: ")
if playlist_link.split("/")[3] == "playlist":
	playlist_uri = playlist_link.split("/")[-1].split("?")[0]
	tracklist = sp.playlist_tracks(playlist_uri)["items"]
else:
	album_uri = playlist_link.split("/")[-1].split("?")[0]
	tracklist = sp.album_tracks(album_uri)["items"]

# title, artist, album, date, track number, genre, cover
for track in tracklist:
	# track_link = track["track"]["external_urls"]["spotify"]
	# track_uri = track["track"]["uri"]
	# album_uri = track["track"]["album"]["uri"]
	# artist_uri = track["track"]["artists"][0]["uri"]

	album_info = sp.album(album_uri)

	# mp3 metadata variables
	track_name = track["track"]["name"]
	artist_name = track["track"]["artists"][0]["name"]
	album = track["track"]["album"]["name"]
	album_release_date = album_info["release_date"].split("-")[0]
	track_number = track["track"]["track_number"]
	album_cover = album_info["images"][0]["url"]

	metadata = {
		"title": track_name,
		"artist": artist_name,
		"album": album,
		"date": album_release_date,
		"track_number": track_number,
	}

	print(f'Searching with query \"{track_name} by {artist_name}\"...')
	yt_download(youtube_search(f'{track_name} by {artist_name}')[0], track_name)
	print("Editing metadata...")
	update_mp3_metadata(f'downloads/{track_name}.mp3', metadata, album_cover)
	print("Done!")

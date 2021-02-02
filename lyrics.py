import asyncio
import requests
from bs4 import BeautifulSoup, Comment


#Lyrics__Container-sc-1ynbvzw-2

class Lyric():
	def __init__(self, artist, song_name):
		self.artist = artist
		self.song_name = song_name
		self.get_lyric(self.artist, self.song_name)

	def get_lyric(self, artist, song_name):
		
		search_song = f'{artist} {song_name}'
		search_song = search_song.replace(' ', '-')
		print(search_song)
		url = f'https://genius.com/{search_song}-lyrics'
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'lxml')
		print(soup.select('.song_body-lyrics'))

		lyric = soup.select('.song_body-lyrics .lyrics p')
		print(lyric)
		tags = lyric[0].find_all(['a', 'i'])
		print('タグです。')
		print(tags)
		for tag in tags:
			tag.unwrap()
		
		print('ここから歌詞です。')
		print(lyric[0].text)
		
		


Lyric = Lyric('joji', 'pretty boy')

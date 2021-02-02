import asyncio
import requests
from bs4 import BeautifulSoup, Comment


#Lyrics__Container-sc-1ynbvzw-2

class Lyric():
	def __init__(self, artist, song_name):
		self.artist = artist
		self.song_name = song_name
		self.__gtask = []
		self.__canceled = False
		self.__lyric = ''

		
		self.genius_url = self.make_genius_url(artist, song_name)
		lyric = self.lyric_from_genius(self.genius_url)
		print(lyric)
	
	def make_genius_url(self, artist, song_name):
		search_song = f'{artist} {song_name}'
		search_song = search_song.replace(' ', '-')
		print(search_song)
		return f'https://genius.com/{search_song}-lyrics'
	

	def get_soup(self, url):
		r = requests.get(url)
		if r.status_code == 200:
			soup = BeautifulSoup(r.content, 'lxml')
			return soup
		else:
			return False
	
	def scrape_genius(self, url):
		if not self.__canceled:
			soup = self.get_soup(url)
		if soup and not self.__canceled:
			lyric_soup = soup.select('.song_body-lyrics .lyrics p')
			if lyric_soup:
				self.__canceled = True
				tags = lyric_soup[0].find_all(['a', 'i'])
				for tag in tags:
					tag.unwrap()
				print('ここから歌詞です。')
				print(lyric_soup[0].text)
				self.__lyric = lyric_soup[0].text
				self.__gtask.cancel()
			else:
				print('歌詞情報を取得出来なかった。')
		else:
			print('歌詞情報がない')
			self.__gtask.cancel()


	def lyric_from_genius(self, url):

		async def main_loop(url):
			async def get_lyric_soup(url):
				await self.loop.run_in_executor(None, self.scrape_genius, url)
			
			#main_loopの処理		
			for _ in range(5):
				self.__gtask += [get_lyric_soup(url)]
			return await asyncio.gather(*self.__gtask)
		
		try:
			self.loop = asyncio.new_event_loop()
			self.loop.run_until_complete(main_loop(url))
		except asyncio.exceptions.CancelledError as e:
			print("*** CancelledError ***", e)
		finally:
			if self.__lyric:
				return self.__lyric
			else:
				print('5回のリクエストで曲情報が取れなかった。')
		
		


Lyric = Lyric('kamal', 'blue')

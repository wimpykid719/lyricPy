import asyncio
import requests
from bs4 import BeautifulSoup, Comment


#Lyrics__Container-sc-1ynbvzw-2

class Lyric():
	def __init__(self, artist, song_name, max_recur=3):
		self.artist = artist
		self.song_name = song_name
		self.__gtask = []
		self.__canceled = False
		self.__lyric = ''
		self.__max_recur = max_recur


		
		self.genius_url = self.make_genius_url(artist, song_name)
		lyric = self.lyric_from_genius(self.genius_url, self.__max_recur)
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
			if self.__canceled:
				print('歌詞取得した')
			else:
				print('歌詞情報がない')
			self.__gtask.cancel()


	def lyric_from_genius(self, url, depth):
		print('再帰の回数確認depth: ', self.__max_recur - depth)

		async def main_loop(url):
			async def get_lyric_soup(url):
				await self.loop.run_in_executor(None, self.scrape_genius, url)
			
			#main_loopの処理		
			for _ in range(1):#タスクキャンセルいれてもここでエラーにならないのか?...キャンセルしたタスクに新しいタスクが追加される？
				self.__gtask += [get_lyric_soup(url)]
			return await asyncio.gather(*self.__gtask)
		try:
			self.loop = asyncio.new_event_loop()
			self.loop.run_until_complete(main_loop(url))
		except asyncio.exceptions.CancelledError as e:
			print("*** CancelledError ***", e)
		finally:
			if self.__lyric or depth <= 0:
				return self.__lyric
			else:
				print('2回のリクエストで曲情報が取れなかった。')
				return self.lyric_from_genius(url, depth - 1)
		
		


Lyric = Lyric('kamal', 'blue')

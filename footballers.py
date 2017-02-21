import requests
from bs4 import BeautifulSoup
import json

class GameData:
	def __init__(self):
		all_data_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
		self.data = soupify(all_data_url)
		self.player_data = {}

	def soupify(url):
		htmltext = requests.get(url)
		soup = BeautifulSoup(htmltext.text, 'lxml')
		content = soup.find('p').getText()
		data = json.loads(content)
		return data

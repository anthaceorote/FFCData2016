import requests
from bs4 import BeautifulSoup
import json
from GameData import get_player_dir

class Player:
	def __init__(self, fpl_id, ffc_team):
		self.fpl_id = fpl_id
		self.ffc_team = ffc_team
		self.player_name = ""
		self.player_fpl_team_name = ""
		self.overall_points = 0
		self.overall_rank = 0

	def info(self):
		url = "https://fantasy.premierleague.com/drf/entry/%d/history" % self.fpl_id
		player_info = soupify(url)

		assert self.fpl_id == int(player_info['entry']['id']), "FPL ID Mismatch - %d expected, %d received" % (self.fpl_id, int(player_info['entry']['id']))
		
		self.player_name = player_info['entry']['player_first_name'] + " " + player_info['entry']['player_last_name']
		self.player_fpl_team_name = player_info['entry']['name']
		self.overall_points = player_info['entry']['summary_overall_points']
		self.overall_rank = player_info['entry']['summary_overall_rank']


	def get_gameweek_team(self, gameweek):
		entry_url = "https://fantasy.premierleague.com/drf/entry/%d/event/%d" % (self.fpl_id, gameweek)
		team_info = soupify(entry_url)

		current_team, bench = [], []
		for pick in team_info['picks']:
			if not pick['is_sub']:
				current_team.append(player_dir[pick['element']])
			else: bench.append(player_dir[pick['element']])
		return current_team, bench

	def get_gameweek_points(self, gameweek):
		entry_url = "https://fantasy.premierleague.com/drf/entry/%d/event/%d" % (self.fpl_id, gameweek)
		team_info = soupify(entry_url)

		gw_points = team_info['points']
		gw_hits = team_info['entry_history']['event_transfers_cost']

		return gw_points - gw_hits, gw_hits


	def soupify(url):
		htmltext = requests.get(url)
		soup = BeautifulSoup(htmltext.text, 'lxml')
		content = soup.find('p').getText()
		data = json.loads(content)
		return data
#<a href="/a/team/503882/event/1" class="ismjs-show-event ismjs-link">GW1</a>
#import sys
#reload(sys)
#sys.setdefaultencoding('UTF8')
# -*- coding: utf-8 -*-


from lxml import html
import requests
from bs4 import BeautifulSoup

filename = "team.txt"
player_code_table = {}
target = open(filename, 'r')
for line in target:
	if ',' not in line:
		team_name = line
		continue
	else:	
		line = line.split(',')
		player_name = line[0]
		player_url = line[1]
		player_id = [int(num) for num in line[1].split('/') if num.isdigit()][0]
		player_code_table[player_name] = (player_id, player_url)

def print_team(player_code_table):
	for player, pid in player_code_table.items():
		print('{} : {}'.format(player, pid[0]))

temp = "https://fantasy.premierleague.com/a/leagues/standings/211281/classic"
page = requests.get(temp)
soup = BeautifulSoup(page.text, "lxml")

tree = html.fromstring(page.content)
xp = "/html"
points = tree.xpath(xp)

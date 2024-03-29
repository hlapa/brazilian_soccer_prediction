import time
import numpy as np
from random_ua import get_random_ua
import re

def GameFeatures(url):

	def prepareDoc(url):
		'''
		This function retrieve and parse the data
		'''
		headers = utils.default_headers()
		#headers['User-Agent'] = get_random_ua()
        #headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		response = get(url, headers = headers, verify=False)
		time.sleep(1)
		doc = BeautifulSoup(response.content, 'html.parser')
		return doc

	def getInfo(doc):
		'''
		This function retrieves information that are not contained in tables,
		they are returned in this order: home_team, away_team, score, 
		'''
		home_team = doc.findAll('td', 'stats-game-head-teamname hide-mobile')[0].text.strip()
		away_team = doc.findAll('td', 'stats-game-head-teamname hide-mobile')[1].text.strip()
		score = doc.findAll('span', 'match-full-result')
		home_team_score = score[0].text.split()[0]
		away_team_score = score[0].text.split()[2]
		referee = doc.findAll('table', id='linups')[1].a.text.strip()
		stadium = doc.findAll('table', 'match-stadium')[0].findAll('td')[1].text
		city = doc.findAll('table', 'match-stadium')[0].findAll('td')[3].text
		datetime = doc.findAll('li', 'gamehead')[1].text
		game_text = doc.findAll('li', 'gamehead')[4].text.strip()
		game_match = re.findall("[0-3]*[0-9]", game_text)
		game = -1 if len(game_match)== 0 else int(game_match[0])
		return home_team, away_team, home_team_score, away_team_score, referee, stadium, city, datetime, game

	def prepareEventsTag(doc):
		'''
		This function prepares de events element, this element contais data about goals, cards and substitution
		'''
		#prepareEventsTag2(doc)
		events = doc.findAll('tbody', 'stat-quarts-padding')
		first_half = events[0]
		second_half = events[1]
		events1st = first_half.findAll('tr')
		events2nd = second_half.findAll('tr')
		return events1st, events2nd	
	
	def prepareEventsTag2(doc):
		'''
		This function prepares de events element, this element contais data about goals, cards and substitution
		'''
		events = doc.findAll('tbody', 'stat-quarts-padding')
		first_half = doc.find('table', id='first-half-summary')
		second_half = doc.find('table', id='second-half-summary')
		events1st = first_half.tbody.findAll('tr')
		events2nd = second_half.tbody.findAll('tr')
		return events1st, events2nd	
	

	def getEvents(events):
		'''
		This function gets all the events from a half-time element and return them as dictonaries
		'''

		eventList=[]
		
		for n in range(1,len(events)):
			kind = events[n].span.get('title')
			if events[n].div.get('style') == 'float:left':
			    time = events[n].td.text
			    hometeam = True
			elif events[n].div.get('style') == 'float:right':
			    time = events[n].findAll('td', 'match-sum-wd-minute')[1].text
			    hometeam = False
			else:
			    hometeam = np.nan()
			if kind != 'Substitute in':
			    name = events[n].div.text.strip()
			    eventDict = {'time':time,
			                'kind':kind,
			                'hometeam':hometeam,
			                'player':name
			                }
			else:
			    playerIn = events[n].div.text.strip()
			    playerOut = 'PLAYER OUT NOT DEFINED'
			    if (len(events[n].findAll('a')) == 2):
    				    playerOut = events[n].findAll('a')[1].text.strip()
				
			    eventDict = {'time':time,
			                'kind':kind,
			                'hometeam':hometeam,
			                'playerIn':playerIn,
			                'playerOut':playerOut
			                }
			eventList.append(eventDict)
		return eventList

	def prepareLineup(doc):
		'''
		This function prepares de lineup element, this element contais data about the players
		'''
		lineup = doc.findAll('table', id='team-lineups')[0]
		sublineup = doc.findAll('table', id='team-sub-lineups')[0]
		return lineup, sublineup

	def getLineup(lineup):
	    '''
	    This function recieves a single input with the lineup element and returns two lists of tuples that contais the id and name of the players, 
	    it works both for the lineup and the sublineup.
	    '''    
	    home = []
	    away = []
	    lineupdiv = lineup.findAll('div')
	    for x in lineupdiv:
	        id = x.get('class')[0]
	        name = x.text.strip()
	        if id.split('-')[0] == 'person':
	            if x.get('style') == 'float:left':
	                home.append((id,name))
	            else:
	                away.append((id,name))
	    return home, away

	def getStats(doc):
	    statsHome={}
	    statsAway={}
	    stats = doc.findAll('table', 'match_stats_center')[0].findAll('tr')
	    for n in range(len(stats)):
	        td_stat = stats[n].findAll('td')
	        stat = td_stat[2].text.strip()
	        home_stat = td_stat[1].text.strip()
	        away_stat = td_stat[3].text.strip()
	        statsHome[f'h_{stat}'] = home_stat
	        statsAway[f'a_{stat}'] = away_stat
	    return statsHome, statsAway


	'''
	This function captures features
	'''
	from requests import get, utils
	from bs4 import BeautifulSoup

    
	doc = prepareDoc(url)
	home_team, away_team, home_team_score, away_team_score, referee, stadium, city, datetime, game = getInfo(doc)
	events1st, events2nd = prepareEventsTag2(doc)	
	eventList1st = getEvents(events1st)
	eventList2nd = getEvents(events2nd)
	lineup, sublineup = prepareLineup(doc)
	lineupList = getLineup(lineup)
	sublineupList = getLineup(sublineup)
	statsHome, statsAway = getStats(doc)

	return home_team, away_team, home_team_score, away_team_score, referee, stadium, city, datetime, game, eventList1st, eventList2nd, lineupList, sublineupList, statsHome, statsAway
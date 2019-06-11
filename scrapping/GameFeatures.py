def GameFeatures(url):

	def prepareDoc(url):
		'''
		This function retrieve and parse the data
		'''
		response = get(url, verify=False)
		doc = BeautifulSoup(response.content, 'html.parser')
		return doc

	def getInfo(doc):
		'''
		This function retrieves information that are not contained in tables,
		they are returned in this order: home_team, away_team, score, 
		'''
		home_team = doc.findAll('td', 'stats-game-head-teamname hide-mobile')[0].text.split()[0]
		away_team = doc.findAll('td', 'stats-game-head-teamname hide-mobile')[1].text.split()[0]
		score = doc.findAll('span', 'match-full-result')
		home_team_score = score[0].text.split()[0]
		away_team_score = score[0].text.split()[2]
		referee = doc.findAll('table', id='linups')[1].a.text.strip()
		stadium = doc.findAll('table', 'match-stadium')[0].findAll('td')[1].text
		city = doc.findAll('table', 'match-stadium')[0].findAll('td')[3].text
		return home_team, away_team, home_team_score, away_team_score, referee, stadium, city

	def prepareEventsTag(doc):
		'''
		This function prepares de events element, this element contais data about goals, cards and substitution
		'''
		events = doc.findAll('tbody', 'stat-quarts-padding')
		first_half = events[0]
		second_half = events[1]
		events1st = first_half.findAll('tr')
		events2nd = second_half.findAll('tr')
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


	'''
	This function captures soccer games features from academiadasapostasbrasil.com. The input is the URL from a game and the output are:
	home_team, away_team, home_team_score, away_team_score, referee, stadium, city,eventList1st, eventList2nd, lineupList, sublineupList
	'''
	from requests import get
	from bs4 import BeautifulSoup

	doc = prepareDoc(url)
	home_team, away_team, home_team_score, away_team_score, referee, stadium, city = getInfo(doc)
	events1st, events2nd = prepareEventsTag(doc)	
	eventList1st = getEvents(events1st)
	eventList2nd = getEvents(events2nd)
	lineup, sublineup = prepareLineup(doc)
	lineupList = getLineup(lineup)
	sublineupList = getLineup(sublineup)

	return home_team, away_team, home_team_score, away_team_score, referee, stadium, city,eventList1st, eventList2nd, lineupList, sublineupList 



from requests import get
from bs4 import BeautifulSoup

class PreGameFeatures:
    	
	def __init__(self, url):
		self.content_parsed = self.document_parser(url)
		#self.build()

	def build(self):
		'''
		This function build the entire object
		'''
		print('HOME TEAM:')
		self.home_last_game_results(self.content_parsed)
		print('\n AWAY TEAM:')
		self.away_last_game_results(self.content_parsed)

	def document_parser(self, url):
		'''
		This function retrieve and parse the data
		'''
		response = get(url, verify=False)
		doc = BeautifulSoup(response.content, 'html.parser')
		return doc

	def home_last_game_results(self, doc):
    		self.last_game_results(doc, 0 )

	def away_last_game_results(self, doc):
			self.last_game_results(doc, 1 )

	def element_game_results(self, doc):
    		return doc.find('span', class_='stats-title-wrapper', string='Percurso:').find_parent('tr').find_next('tr').findAll('td', recursive=False)

	def last_game_results(self, doc, team_index):
		'''
		This function retrieves information about the current season from home team or away team
		team_index: 0 - HOME, 1 - AWAY
		'''
		home = 1
		away = 2
		global_ = 3

		teams_games = self.element_game_results(doc)
		last_games = teams_games[team_index].find('tbody').find_all('tr')
		
		current_wins = last_games[0].find_all('td')
		current_draws = last_games[1].find_all('td')
		current_loss = last_games[2].find_all('td')
		games_without_win = last_games[3].find_all('td')
		games_without_draw = last_games[4].find_all('td')
		games_without_lose = last_games[5].find_all('td')
		
		#current_wins
		current_wins_home = current_wins[home].text
		current_wins_away = current_wins[away].text
		current_wins_global = current_wins[global_].text

		#current_draws
		current_draws_home = current_draws[home].text
		current_draws_away = current_draws[away].text
		current_draws_global = current_draws[global_].text

		#current_loss
		current_loss_home = current_loss[home].text
		current_loss_away = current_loss[away].text
		current_loss_global = current_loss[global_].text

		#games_without_win
		games_without_win_home = games_without_win[home].text
		games_without_win_away = games_without_win[away].text
		games_without_win_global = games_without_win[global_].text
		
		#games_without_draw
		games_without_draw_home = games_without_draw[home].text
		games_without_draw_away = games_without_draw[away].text
		games_without_draw_global = games_without_draw[global_].text

		#games_without_lose
		games_without_lose_home = games_without_lose[home].text
		games_without_lose_away = games_without_lose[away].text
		games_without_lose_global = games_without_lose[global_].text

		print(f'Current_wins :{current_wins_home}, {current_wins_away}, {current_wins_global}')
		print(f'Current_draws :{current_draws_home}, {current_draws_away}, {current_draws_global}')
		print(f'Current_loss :{current_loss_home}, {current_loss_away}, {current_loss_global}')
		print(f'Games_without_win : {games_without_win_home}, {games_without_win_away}, {games_without_win_global}')
		print(f'Games_without_draw :{games_without_draw_home}, {games_without_draw_away}, {games_without_draw_global}')
		print(f'Games_without_lose :{games_without_lose_home}, {games_without_lose_away}, {games_without_lose_global}')
		
		#return ?

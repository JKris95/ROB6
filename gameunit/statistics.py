import pandas as pd

class GameStats():
	def __init__(self):
		pass

	def df_from_excel(self, filename, sheetname = None, sheet_index = None):
		xl = pd.ExcelFile('gameunit/{}'.format(filename) )
		if sheetname:
			df = xl.parse(sheetname)
			return df
		elif sheet_index+1: # Adding 1 in case 0 is passed as sheet_index
			df = xl.parse(sheet_index)
			print(type(df))
			return df

	def filter_with_equality(self, df, cols, eq_constraints):
		for col, constraint in zip(cols, eq_constraints):
			new_df = df[df[col] == constraint]
		return new_df
	
	def divide_in_teams(self, df):
		team_names = []
		team_dfs = []
		for team in df['team'].values:
			if team not in team_names:
				team_names.append(team)
		for team in team_names:
			team_dfs.append(self.filter_with_equality(df, ['team'], [team]))
		return team_dfs

	def divide_by_players(self):
		pass

	def player_wins(self, teams):
		for team in teams:


	def player_time(self):
		pass


if __name__ == '__main__':
	game_stats = GameStats()
	results = game_stats.df_from_excel('dummy_data.xlsx', sheet_index=0)
  #  print(df.head())
	battle_results = game_stats.filter_with_equality(results, ['game_type'], ['battle'])    
	print(battle_results)
"""
	teams = game_stats.divide_in_teams(battle_results)
	for i in teams:
		print(i.head())
"""
teams = battle_results['team'].values
print(teams)
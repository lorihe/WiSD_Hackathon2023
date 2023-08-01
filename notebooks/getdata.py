import json
import numpy as np
import pandas as pd
from datetime import datetime
import os
import jsonlines

def load_jsonl_file(file_path):
    with jsonlines.open(file_path, 'r') as file:
        data = [line for line in file]
    return data

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

folder_path = '../data/'

files = []
for file in os.listdir('../data'):
    files.append(file)

game_files = files[:-3]
game_ids = []
for game in game_files:
    game_id = game.split('_')[0]
    game_ids.append(game_id)

metadata = load_json_file('../data/metadata.json')
teams = load_json_file('../data/metadata_teams.json')
players = load_json_file('../data/metadata_players.json')

metadata_df = pd.DataFrame(metadata['games'])
metadata_df['date'] = pd.to_datetime(metadata_df[['month', 'day', 'year']]).dt.strftime('%m-%d-%Y')

metadata_df = metadata_df[metadata_df['nbaId'].isin(game_ids)]

teams_df = pd.DataFrame(teams['teams'])

players_df = pd.DataFrame(players['players'])
players_df['fullName'] = players_df['firstName'] + ' ' + players_df['lastName']
players_df['position'] = players_df['position'].replace({'F-G': 'G-F', 'C-F':'F-C'})


def get_nbaId(date):
    nbaId = metadata_df.loc[metadata_df['date'] == date]['nbaId'].item()
    return nbaId

def get_date(nbaId):
    date = metadata_df.loc[metadata_df['nbaId'] == nbaId]['date'].item()
    return date

def get_playerInfo(input_info, input_col, out_col):    
    player_info = players_df[players_df[input_col] == input_info][out_col].item()
    return player_info

def get_homeTeam(nbaId):
    homeTeamId = metadata_df[metadata_df['nbaId'] == nbaId]['homeTeamId'].item()
    homeTeam = teams_df[teams_df['id'] == homeTeamId]['name'].item()
    return homeTeam

def get_awayTeam(nbaId):
    awayTeamId = metadata_df[metadata_df['nbaId'] == nbaId]['awayTeamId'].item()
    awayTeam = teams_df[teams_df['id'] == awayTeamId]['name'].item()
    return awayTeam

def get_home_players(nbaId):
    '''
    Get home players names of specified game.
    
    Arg: nbaId(str)
    Return: list
    '''
    event = load_jsonl_file('../data/'+str(nbaId)+'_events.jsonl')
    event_df = pd.DataFrame(event)
    
    home_players_ids = event_df['homePlayers'].apply(pd.Series)
    home_players_ids = home_players_ids.values.flatten()
    home_players_ids = list(set(home_players_ids))
    
    home_players = []
    for player_id in home_players_ids:
        player_name = players_df[players_df['id']==player_id]['firstName'].item()+' '+ \
        players_df[players_df['id']==player_id]['lastName'].item()
        home_players.append(player_name)       
    
    return home_players


def get_away_players(nbaId):
    '''
    Get away players names of specified game.
    
    Arg: nbaId(str)
    Return: list
    '''
    event = load_jsonl_file('../data/'+str(nbaId)+'_events.jsonl')
    event_df = pd.DataFrame(event)
    
    away_players_ids = event_df['awayPlayers'].apply(pd.Series)
    away_players_ids = away_players_ids.values.flatten()
    away_players_ids = list(set(away_players_ids))
    
    away_players = []
    for player_id in away_players_ids:
        player_name = players_df[players_df['id']==player_id]['firstName'].item()+' '+ \
        players_df[players_df['id']==player_id]['lastName'].item()
        away_players.append(player_name)       
    
    return away_players

def get_tracking(nbaId):
    tracking = load_jsonl_file('../data/'+str(nbaId)+'_tracking.jsonl')
    tracking_df = pd.DataFrame(tracking)
    
    return tracking_df

def get_xy_df(nbaId, player_id, home=True):
    '''
    Get coordinate info of specified player in specified game. Exclude coordinates out of the court. Drop rows with duplicated 
    (period, gameClock).
       
    Args: nbaId(str)
    player_id(str)
    home(boolean)
    
    Return: dataframe
    '''

    player_data = []

    if home:
        players_key = 'homePlayers'
    else:
        players_key = 'awayPlayers'

    # Function to process the JSON object and extract relevant data
    def process_data(data):
        for player in data[players_key]:
            if player['playerId'] == player_id and -47 <= player['xyz'][0] <= 47 and -25 <= player['xyz'][1] <= 25:
                player_data.append({
                    'period': data['period'],
                    'gameClock': data['gameClock'],
                    'x': player['xyz'][0],
                    'y': player['xyz'][1]
                })

    file_path = '../data/' + str(nbaId) + '_tracking.jsonl'

    # Read the JSONL file and process each JSON object
    with jsonlines.open(file_path) as reader:
        for item in reader:
            process_data(item)

    # Create the DataFrame from the processed data
    xy_df = pd.DataFrame(player_data)
    xy_df.drop_duplicates(subset=['gameClock', 'period'], keep='last', inplace=True)

    return xy_df







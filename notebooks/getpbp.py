import json
import pandas as pd
import urllib3

header_data = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'stats.nba.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

http = urllib3.PoolManager()

def play_by_play_url(game_id):
    return "https://stats.nba.com/stats/playbyplayv2/?gameId={0}&startPeriod=0&endPeriod=14".format(game_id)
    
def extract_data(game_id):
    '''
    Extract play by play data of specified game.
    
    Arg: game_id(str)
    Return: dataframe
    '''
    url = play_by_play_url(game_id)
    r = http.request('GET', url, headers=header_data)
    resp = json.loads(r.data)
    results = resp['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    frame = pd.DataFrame(rows)
    frame.columns = headers
    return frame

def get_shot(game_id, player):
    '''
    Get rows that contain scored shots and missed shots, not including free throws, from play by play data of specified player in a 
    specified game.
    
    Args: game_id(str)
          player(str): player name
    
    Return: dataframe
    '''
    df = extract_data(game_id)
    all_shots = df[(df['EVENTMSGTYPE'] == 1) | (df['EVENTMSGTYPE'] == 2)]
    player_shots = all_shots[all_shots['PLAYER1_NAME'] == player].reset_index(drop = True)
    player_shots = player_shots[['EVENTNUM', 'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION']]
    return player_shots
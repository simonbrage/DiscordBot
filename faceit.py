import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

header = {'accept': 'application/json', 'Authorization': 'Bearer {}'.format(API_KEY)}
url = 'https://open.faceit.com/data/v4'

# PLAYER INFORMATION
def faceit_get_player_id(nickname):
    query_params = {'nickname': nickname}
    response = requests.get(url + '/players', headers=header, params=query_params)

    return response.json()['player_id']

def faceit_get_player_country(nickname):
    query_params = {'nickname': nickname}
    response = requests.get(url + '/players', headers=header, params=query_params)

    return response.json()['country']

def faceit_get_player_avatar(nickname):
    query_params = {'nickname': nickname}
    response = requests.get(url + '/players', headers=header, params=query_params)

    return response.json()['avatar']

def faceit_get_player_level(nickname):
    query_params = {'nickname': nickname}
    response = requests.get(url + '/players', headers=header, params=query_params)

    return response.json()['games']['csgo']['skill_level']

def faceit_get_player_elo(nickname):
    query_params = {'nickname': nickname}
    response = requests.get(url + '/players', headers=header, params=query_params)

    return response.json()['games']['csgo']['faceit_elo']

# ---- Information on infractions no longer supported in FACEIT API ----
#def faceit_get_player_infractions(nickname):
#    query_params = {'nickname': nickname}
#    response = requests.get(url + '/players', headers=header, params=query_params)
#
#    return response.json()['infractions']

# PLAYER LIFETIME STATS
def faceit_get_lifetime_stats(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']

def faceit_get_lifetime_stats_total_matches(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Matches']

def faceit_get_lifetime_stats_kd_ratio(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Average K/D Ratio']

def faceit_get_lifetime_stats_win_rate(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Win Rate %']

def faceit_get_lifetime_stats_hs_rate(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Average Headshots %']

def faceit_get_lifetime_stats_recent_results(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    results = response.json()['lifetime']['Recent Results']
    results_string = ''
    for r in results:
        if r == '1':
            results_string += '**W** '
        else:
            results_string += 'L '
    
    return results_string

def faceit_get_win_streak(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Current Win Streak']

def faceit_get_longest_win_streak(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo'}
    response = requests.get(url + '/players/{}/stats/{}'.format(player_id, 'csgo'), headers=header, params=query_params)

    return response.json()['lifetime']['Longest Win Streak']

# PLAYER RANKINGS    
def faceit_get_country_ranking(player_id, country):
    query_params = {'player_id': player_id, 'game_id': 'csgo', 'region': 'EU', 'country': country}
    response = requests.get(url + '/rankings/games/{}/regions/{}/players/{}'.format('csgo', 'EU', player_id), headers=header, params=query_params)

    return response.json()['position']

def faceit_get_region_ranking(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo', 'region': 'EU', 'country': ''}
    response = requests.get(url + '/rankings/games/{}/regions/{}/players/{}'.format('csgo', 'EU', player_id), headers=header, params=query_params)

    return response.json()['position']

# PLAYER MATCHES AND MATCH STATISTICS        
def faceit_get_matches(player_id):
    query_params = {'player_id': player_id, 'game_id': 'csgo', 'offset': '0', 'limit': '20'}
    response = requests.get(url + '/players/{}/history'.format(player_id), headers=header, params=query_params)

    return response.json()

def faceit_get_match_stats(match_id):
    query_params = {'match_id': match_id}
    response = requests.get(url + '/matches/{}/stats'.format(match_id), headers=header, params=query_params)

    return response.json()
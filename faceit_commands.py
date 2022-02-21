# Commands for FACEIT 

from faceit_api import *

# Implements aliases for often used names
def check_nickname(nickname):
    if nickname.lower() == 'doomyo': nickname = 'Doomyo'
    elif nickname.lower() == 'grunk' or nickname.lower() == 'grunk_' or nickname.lower() == 'grundt': nickname = 'xGrunk'
    elif nickname.lower() == 'brage' or nickname.lower() == 'bragi' or nickname.lower() == 'goat': nickname = 'bragi'
    elif nickname.lower() == 'friis' or nickname.lower() == 'friis007' or nickname.lower() == 'lordfriis': nickname = 'Friis007'
    
    return nickname

# Profile method
def find_profile(nickname):
    d = dict()

    nickname = check_nickname(nickname)

    player_id = faceit_get_player_id(nickname)
    player_country = faceit_get_player_country(nickname)
    d['player_id'] = faceit_get_player_id(nickname)
    d['player_country'] = faceit_get_player_country(nickname)
    d['player_avatar'] = faceit_get_player_avatar(nickname)
    
    player_level = str(faceit_get_player_level(nickname))
    if player_level == '10': player_level = '<:faceit10:838215465859940364>' 
    d['player_level'] = player_level
    d['player_elo'] = faceit_get_player_elo(nickname)

    d['total_matches_played'] = faceit_get_lifetime_stats_total_matches(player_id)
    d['kd_ratio'] = faceit_get_lifetime_stats_kd_ratio(player_id)
    d['win_rate'] = faceit_get_lifetime_stats_win_rate(player_id)
    d['hs_rate'] = faceit_get_lifetime_stats_hs_rate(player_id)
    d['results'] = faceit_get_lifetime_stats_recent_results(player_id)
    d['longest_win_streak'] = faceit_get_longest_win_streak(player_id)

    d['country_ranking'] = faceit_get_country_ranking(player_id, player_country)
    d['region_ranking'] = faceit_get_region_ranking(player_id)

    return d

# Stats method
def find_stats(nickname):
    d = dict()

    nickname = check_nickname(nickname)

    player_id = faceit_get_player_id(nickname)
    player_country = faceit_get_player_country(nickname)
    d['player_id'] = faceit_get_player_id(nickname)
    d['player_country'] = faceit_get_player_country(nickname)
    d['player_avatar'] = faceit_get_player_avatar(nickname)
    
    player_level = str(faceit_get_player_level(nickname))
    if player_level == '10': player_level = '<:faceit10:838215465859940364>' 
    d['player_level'] = player_level
    d['player_elo'] = faceit_get_player_elo(nickname)

    d['results'] = faceit_get_lifetime_stats_recent_results(player_id)

    d['country_ranking'] = faceit_get_country_ranking(player_id, player_country)
    d['region_ranking'] = faceit_get_region_ranking(player_id)    

    match_list = faceit_get_matches(player_id)['items']
    matches_length = len(match_list)
    d['matches_length'] = matches_length

    avg_kills = 0.0
    avg_kr_ratio = 0.0
    avg_hs_ratio = 0.0
    avg_kd_ratio = 0.0
    win_rate = 0.0
    
    for m in range(matches_length):
        match_id = match_list[m]['match_id']
        player = faceit_get_match_stats(match_id)['rounds'][0]['teams']
        for p in range(2):
            for i in range(len(player[p]['players'])):
                if player[p]['players'][i]['player_id'] == player_id:
                    avg_kills += float(player[p]['players'][i]['player_stats']['Kills'])
                    avg_kr_ratio += float(player[p]['players'][i]['player_stats']['K/R Ratio'])
                    avg_hs_ratio += float(player[p]['players'][i]['player_stats']['Headshots %'])
                    avg_kd_ratio += float(player[p]['players'][i]['player_stats']['K/D Ratio'])
                    win_rate += float(player[p]['players'][i]['player_stats']['Result'])
    d['avg_kills'] = round((avg_kills/matches_length))
    d['avg_kr_ratio'] = round((avg_kr_ratio/matches_length),2)
    d['avg_hs_ratio'] = str(round((avg_hs_ratio/matches_length)))
    d['avg_kd_ratio'] = round((avg_kd_ratio/matches_length),2)
    d['win_rate'] = str(round(win_rate*(100/matches_length)))

    return d
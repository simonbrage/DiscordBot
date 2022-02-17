import os
import discord
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from faceit import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Rewrites the 'No category' in the help-command
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('-'),
    help_command = help_command
)

# Start-up
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='-help'))
    print(f'{bot.user.name} is connected.')

# ----------------------------------------------
# ------------------ COMMANDS ------------------
# ----------------------------------------------
@bot.command(name='backflip', help='Displays a backflip GIF.')
async def backflip(ctx):
    await ctx.send('https://giphy.com/gifs/officialfiym-forever-in-your-mind-fiym-xT0xetpPHT8UryiiqY')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='-help'))

# Displays lifetime stats, current ranking, and results of last five games (W or L)
@bot.command(name='profile', help='Displays Faceit profile of a player.')
async def profile(ctx, nickname):
    previous_status = bot.guilds[0].get_member(bot.user.id).activity

    if nickname.lower() == 'doomyo': nickname = 'Doomyo'
    elif nickname.lower() == 'grunk' or nickname.lower() == 'grunk_' or nickname.lower() == 'grundt': nickname = 'xGrunk'
    elif nickname.lower() == 'brage' or nickname.lower() == 'bragi' or nickname.lower() == 'goat': nickname = 'bragi'

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}'s career".format(nickname)))

    date = datetime.datetime.now()
    try:
        player_id = faceit_get_player_id(nickname)
        player_country = faceit_get_player_country(nickname)
        player_avatar = faceit_get_player_avatar(nickname)
    
        player_level = str(faceit_get_player_level(nickname))
        if player_level == '10': player_level = '<:faceit10:838215465859940364>'
        player_elo = faceit_get_player_elo(nickname)

        total_matches_played = faceit_get_lifetime_stats_total_matches(player_id)
        kd_ratio = faceit_get_lifetime_stats_kd_ratio(player_id)
        win_rate = faceit_get_lifetime_stats_win_rate(player_id)
        hs_rate = faceit_get_lifetime_stats_hs_rate(player_id)
        results = faceit_get_lifetime_stats_recent_results(player_id)
        longest_win_streak = faceit_get_longest_win_streak(player_id)

        country_ranking = faceit_get_country_ranking(player_id, player_country)
        region_ranking = faceit_get_region_ranking(player_id)

        embed=discord.Embed(title='Career - **{}**'.format(nickname),  url='https://www.faceit.com/en/players/{}'.format(nickname), color=0x824dff)
        embed.set_thumbnail(url=player_avatar)
        embed.add_field(name='Level', value=player_level, inline=True)
        embed.add_field(name='ELO', value=player_elo, inline=True)
        embed.add_field(name='Matches', value=total_matches_played, inline=True)
        embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
        embed.add_field(name='K/D', value=kd_ratio, inline=True)
        embed.add_field(name='HS%', value=hs_rate + '%', inline=True)
        embed.add_field(name='Win%', value=win_rate + '%', inline=True)
        embed.add_field(name='Best Win Streak', value=longest_win_streak + ' games', inline=True)
        embed.add_field(name='Past results', value=results, inline=True)
        embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
        embed.add_field(name='Ranking :flag_dk:', value=country_ranking, inline=True)
        embed.add_field(name='Ranking :flag_eu:', value=region_ranking, inline=True)
        embed.set_footer(text=date)

        await ctx.send(embed=embed)
        await bot.change_presence(activity=previous_status)

    except KeyError as err:
        print('A faulty name has been put in. \n Error: {}'.format(err))
        await ctx.send('Did you type that name right? <:ezy:558785929171697695>')
        await bot.change_presence(activity=previous_status)
        return

# Displays player stats from last twenty matches.
@bot.command(name='stats', help='Displays stats of last 20 matches.')
async def stats(ctx, nickname):
    previous_status = bot.guilds[0].get_member(bot.user.id).activity

    if nickname.lower() == 'doomyo': nickname = 'Doomyo'
    elif nickname.lower() == 'grunk' or nickname.lower() == 'grunk_' or nickname.lower() == 'grundt': nickname = 'xGrunk'
    elif nickname.lower() == 'brage' or nickname.lower() == 'bragi' or nickname.lower() == 'goat': nickname = 'bragi'

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}'s stats".format(nickname)))

    date = datetime.datetime.now()

    try:

        player_id = faceit_get_player_id(nickname)
    except KeyError as err:
        print('A faulty name has been put in. \n Error: {}'.format(err))
        await ctx.send('Did you type that name right? <:ezy:558785929171697695>')
        await bot.change_presence(activity=previous_status)
        return

    player_country = faceit_get_player_country(nickname)
    player_avatar = faceit_get_player_avatar(nickname)
    player_level = str(faceit_get_player_level(nickname))
    if player_level == '10': player_level = '<:faceit10:838215465859940364>'
    player_elo = faceit_get_player_elo(nickname)

    results = faceit_get_lifetime_stats_recent_results(player_id)

    country_ranking = faceit_get_country_ranking(player_id, player_country)
    region_ranking = faceit_get_region_ranking(player_id)    

    match_list = faceit_get_matches(player_id)['items']
    matches_length = len(match_list)

    avg_kills = 0.0
    avg_kr_ratio = 0.0
    avg_hs_ratio = 0.0
    avg_kd_ratio = 0.0
    win_rate = 0.0
    
    try:
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
        avg_kills = round((avg_kills/matches_length))
        avg_kr_ratio = round((avg_kr_ratio/matches_length),2)
        avg_hs_ratio = str(round((avg_hs_ratio/matches_length)))
        avg_kd_ratio = round((avg_kd_ratio/matches_length),2)
        win_rate = str(round(win_rate*(100/matches_length)))
    except IndexError as err:
        print('Error: {} \n'.format(err))
        await ctx.send('Something is interfering with the match data <:pepehands:834501916754837594> \n\nCheck your stats on https://www.faceit.com/en/players/{}'.format(nickname))
        await bot.change_presence(activity=previous_status)
        return
        

    embed=discord.Embed(title='Last {} matches - **{}**'.format(matches_length, nickname),  url='https://www.faceit.com/en/players/{}'.format(nickname), color=0x824dff)
    embed.set_thumbnail(url=player_avatar)
    embed.add_field(name='Level', value=player_level, inline=True)
    embed.add_field(name='ELO', value=player_elo, inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='Avg. kills', value=avg_kills, inline=True)
    embed.add_field(name='Avg. HS%', value=avg_hs_ratio + '%', inline=True)
    embed.add_field(name='Avg. K/D', value=avg_kd_ratio, inline=True)
    embed.add_field(name='Avg. K/R', value=avg_kr_ratio, inline=True)
    embed.add_field(name='Win%', value=win_rate + '%', inline=True)
    embed.add_field(name='Past results', value=results, inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='Ranking :flag_dk:', value=country_ranking, inline=True)
    embed.add_field(name='Ranking :flag_eu:', value=region_ranking, inline=True)
    embed.set_footer(text=date)

    await ctx.send(embed=embed)
    await bot.change_presence(activity=previous_status)

# ---- Information on infractions no longer supported by FACEIT API ----
# Displays infractions (AFK, leave, no check-in)
#@bot.command(name='infractions', help='How naughty have you been?')
#async def infractions(ctx, nickname):
#    if nickname.lower() == 'doomyo': nickname = 'Doomyo'
#    elif nickname.lower() == 'grunk' or nickname.lower() == 'grunk_' or nickname.lower() == 'grundt': nickname = 'xGrunk'
#    elif nickname.lower() == 'brage' or nickname.lower() == 'bragi' or nickname.lower() == 'goat': nickname = 'bragi'

#    try:      
#        date = faceit_get_player_infractions(nickname)['last_infraction_date']
#        if date == '':
#            await ctx.send('**{}** has **0** infractions. :partying_face:'.format(nickname))
#        else:
#            infractions = faceit_get_player_infractions(nickname)
#            afk = infractions['afk']
#            leaver = infractions['leaver']
#            not_checked_in = infractions['qm_not_checkedin']
#            await ctx.send('**{}\'s** last infraction was on {}\n  AFK: {}\n  Leaver: {}\n  Not checked in: {}'.format(nickname, date, afk, leaver, not_checked_in))
#    except KeyError as err:
#       print('A faulty name has been put in. \n Error: {}'.format(err))
#        await ctx.send('Did you type that name right? <:ezy:558785929171697695>')

bot.run(TOKEN)
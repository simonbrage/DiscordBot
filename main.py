import os
import discord
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from faceit_api import *
from faceit_commands import *

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
    message = ctx.message
    await message.add_reaction("<:ezy:558785929171697695>")

# Displays lifetime stats, current ranking, and results of last five games (W or L)
@bot.command(name='profile', help='Displays Faceit profile of a player.')
async def profile(ctx, nickname):
    previous_status = bot.guilds[0].get_member(bot.user.id).activity

    message = ctx.message
    await message.add_reaction("<:ezy:558785929171697695>")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}'s career".format(nickname)))

    date = datetime.datetime.now()

    try:
        profile = find_profile(nickname)
    except KeyError as err:
        print('A faulty name has been put in. \n Error: {}'.format(err))
        await ctx.send('Did you type that name right? <:ezy:558785929171697695>')
        await bot.change_presence(activity=previous_status)
        return

    embed=discord.Embed(title='Career - **{}**'.format(nickname),  url='https://www.faceit.com/en/players/{}'.format(nickname), color=0x824dff)
    embed.set_thumbnail(url=profile['player_avatar'])
    embed.add_field(name='Level', value=profile['player_level'], inline=True)
    embed.add_field(name='ELO', value=profile['player_elo'], inline=True)
    embed.add_field(name='Matches', value=profile['total_matches_played'], inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='K/D', value=profile['kd_ratio'], inline=True)
    embed.add_field(name='HS%', value=profile['hs_rate'] + '%', inline=True)
    embed.add_field(name='Win%', value=profile['win_rate'] + '%', inline=True)
    embed.add_field(name='Best Win Streak', value=profile['longest_win_streak'] + ' games', inline=True)
    embed.add_field(name='Past results', value=profile['results'], inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='Ranking :flag_dk:', value=profile['country_ranking'], inline=True)
    embed.add_field(name='Ranking :flag_eu:', value=profile['region_ranking'], inline=True)
    embed.set_footer(text=date)

    await ctx.send(embed=embed)
    await bot.change_presence(activity=previous_status)

# Displays player stats from last twenty matches.
@bot.command(name='stats', help='Displays stats of last 20 matches.')
async def stats(ctx, nickname):
    previous_status = bot.guilds[0].get_member(bot.user.id).activity
    
    message = ctx.message
    await message.add_reaction("<:ezy:558785929171697695>")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}'s stats".format(nickname)))

    date = datetime.datetime.now()

    try:
        stats = find_stats(nickname)
    except KeyError as err:
        print('A faulty name has been put in. \n Error: {}'.format(err))
        await ctx.send('Did you type that name right? <:ezy:558785929171697695>')
        await bot.change_presence(activity=previous_status)
        return
    except IndexError as err:
        print('Error: {} \n'.format(err))
        await ctx.send('Something is interfering with the match data <:pepehands:834501916754837594> \n\nCheck your stats on https://www.faceit.com/en/players/{}'.format(nickname))
        await bot.change_presence(activity=previous_status)
        return

    embed=discord.Embed(title='Last {} matches - **{}**'.format(stats['matches_length'], nickname),  url='https://www.faceit.com/en/players/{}'.format(nickname), color=0x824dff)
    embed.set_thumbnail(url=stats['player_avatar'])
    embed.add_field(name='Level', value=stats['player_level'], inline=True)
    embed.add_field(name='ELO', value=stats['player_elo'], inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='Avg. kills', value=stats['avg_kills'], inline=True)
    embed.add_field(name='Avg. HS%', value=stats['avg_hs_ratio'] + '%', inline=True)
    embed.add_field(name='Avg. K/D', value=stats['avg_kd_ratio'], inline=True)
    embed.add_field(name='Avg. K/R', value=stats['avg_kr_ratio'], inline=True)
    embed.add_field(name='Win%', value=stats['win_rate'] + '%', inline=True)
    embed.add_field(name='Past results', value=stats['results'], inline=True)
    embed.add_field(name='\u200b', value='━━━━━━━━━━━━━━━', inline=False)
    embed.add_field(name='Ranking :flag_dk:', value=stats['country_ranking'], inline=True)
    embed.add_field(name='Ranking :flag_eu:', value=stats['region_ranking'], inline=True)
    embed.set_footer(text=date)

    await ctx.send(embed=embed)
    await bot.change_presence(activity=previous_status)

bot.run(TOKEN)
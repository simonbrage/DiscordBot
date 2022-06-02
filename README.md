# DiscordBot

Small Discord bot with commands that allows users of the Discord server to access their Faceit (CS:GO) stats, profiles, and more. Utilizes the [discordpy](https://discordpy.readthedocs.io/en/stable/) library. I use [Heroku](https://www.heroku.com/)'s free plan to deploy.

## Setting up

What you'll need:
1. **a)** A Heroku account (free is fine, but won't cover uptime for the bot for an entire month), or **b)** a local machine to run the app.
2. A [Faceit developer](https://developers.faceit.com/) account with your own Faceit app (to get the API key).
3. A fork of this repository.

### With Heroku

1. Create an app on Heroku.
2. Under App -> Deploy, connect to your forked repository.
3. Under App -> Settings, press *Reveal Config Vars* and add two new variables:
   - ```DISCORD_TOKEN = {your-discord-token}```
   - ```API_KEY = {your-faceit-api-key}```
4. Under App -> Deploy, press *Deploy Branch* and enable automatic deploys.

After this you should be good to go.

### On a local machine

1. Clone the forked repository to the machine you want to use.
2. Create a ```.env```-file and add two new variables:
   - ```DISCORD_TOKEN = {your-discord-token}```
   - ```API_KEY = {your-faceit-api-key}```
3. Run ```main.py``` from your machine.

## Current available commands

The bot currently supports the following commands:

**Faceit:**
- `-profile`  Displays Faceit profile of a player.
- `-stats`    Displays stats of last 20 matches.
  
**Miscellaneous:**
- `-backflip` Displays a backflip GIF.
- `-poll`     Take a vote on important matters.
- `-roll`     Pick a random number between 1 and your number (defaults to 6).
  
**Default:**
- `-help`     Shows embed with list of available commands.

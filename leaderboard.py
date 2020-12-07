import discord
import requests
import os
from prettytable import PrettyTable
from datetime import datetime as dt
from pytz import timezone as tz

API_KEY = os.getenv('API_KEY')
cookie = {'session': os.getenv('SESSION_COOKIE')}
url = os.getenv('LEADERBOARD_API_URL')

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        try:
            response = requests.request("GET", url, cookies=cookie).json()
            message_to_client = PrettyTable(
                ['Name', 'Stars', 'Local Score', 'Last Star Timestamp'])

            for key in response['members']:
                name = response['members'][key]['name']
                stars = response['members'][key]['stars']
                local_score = response['members'][key]['local_score']
                # global_score = response['members'][key]['global_score']
                # player_id = response['members'][key]['id']
                last_star_ts = dt.fromtimestamp(int(response['members'][key]['last_star_ts']), tz(
                    'US/Eastern')).strftime("%a, %b %d %Y at %H:%M:%S EST")
                message_to_client.add_row(
                    [name, stars, local_score, last_star_ts])
            await message.channel.send("```"+message_to_client.get_string(sortby="Stars", reversesort=True)+"```")
        except Exception as e:
            print(e)
            await message.channel.send("Could not retreive the leaderboard")


client.run(API_KEY)

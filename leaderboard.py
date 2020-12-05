import discord
import requests
import os
from prettytable import PrettyTable

API_KEY = os.getenv('API_KEY')
session_value = os.getenv('SESSION_COOKIE')
cookie={'session': session_value}
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
            response = requests.request("GET",url,cookies=cookie).json()
            message_to_client= PrettyTable(['ID','Name', 'Stars', 'Global Score', 'Local Score'])

            for key in response['members']:
                name = response['members'][key]['name']
                stars= response['members'][key]['stars']
                local_score = response['members'][key]['local_score']
                global_score = response['members'][key]['global_score']
                player_id = response['members'][key]['id']
                message_to_client.add_row([player_id,name,stars, global_score, local_score])
            await message.channel.send(message_to_client.get_string(sortby="Stars",reversesort=True))
        except:
            await message.channel.send("Could not retreive the leaderboard")
        
        
client.run(API_KEY)